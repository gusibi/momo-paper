import { requestUrl } from "obsidian";
import type { ImageHostSettings } from "./settings";

/**
 * S3 兼容图床上传（适用于 Cloudflare R2 与 Amazon S3）。
 * 使用 AWS Signature V4 对 PUT 请求签名，通过 Obsidian 的 requestUrl 发送以绕过 CORS。
 */

const enc = new TextEncoder();

async function sha256Hex(data: ArrayBuffer | string): Promise<string> {
  const buf = typeof data === "string" ? enc.encode(data) : new Uint8Array(data);
  const hash = await crypto.subtle.digest("SHA-256", buf as unknown as BufferSource);
  return toHex(new Uint8Array(hash));
}

async function hmac(key: ArrayBuffer | Uint8Array, data: string): Promise<ArrayBuffer> {
  const keyData = (key instanceof Uint8Array ? key : new Uint8Array(key)) as unknown as BufferSource;
  const cryptoKey = await crypto.subtle.importKey(
    "raw",
    keyData,
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  return crypto.subtle.sign("HMAC", cryptoKey, enc.encode(data) as unknown as BufferSource);
}

function toHex(bytes: Uint8Array): string {
  let s = "";
  for (const b of bytes) s += b.toString(16).padStart(2, "0");
  return s;
}

/** 计算字节内容的 SHA-256（十六进制），用于内容寻址去重。 */
export async function hashBytes(body: ArrayBuffer): Promise<string> {
  return sha256Hex(body);
}

/** RFC3986 编码 key 中的每个路径段（不编码 /）。 */
function encodeKey(key: string): string {
  return key
    .split("/")
    .map((seg) =>
      encodeURIComponent(seg).replace(/[!'()*]/g, (c) => "%" + c.charCodeAt(0).toString(16).toUpperCase())
    )
    .join("/");
}

function resolveEndpoint(host: ImageHostSettings): { host: string; protocol: string } {
  let raw = host.endpoint.trim();
  if (!raw) {
    if (host.provider === "r2") {
      if (!host.accountId) throw new Error("R2 需要填写 Account ID 或 Endpoint。");
      raw = `https://${host.accountId}.r2.cloudflarestorage.com`;
    } else {
      raw = `https://s3.${host.region || "us-east-1"}.amazonaws.com`;
    }
  }
  if (!/^https?:\/\//.test(raw)) raw = "https://" + raw;
  const u = new URL(raw);
  return { host: u.host, protocol: u.protocol.replace(":", "") };
}

export interface UploadResult {
  key: string;
  url: string;
}

/** 上传单个对象，返回公开访问 URL。 */
export async function uploadObject(
  host: ImageHostSettings,
  key: string,
  body: ArrayBuffer,
  contentType: string
): Promise<UploadResult> {
  if (!host.accessKeyId || !host.secretAccessKey) throw new Error("缺少 Access Key。");
  if (!host.bucket) throw new Error("缺少 Bucket。");

  const { host: endpointHost, protocol } = resolveEndpoint(host);
  const region = host.region || (host.provider === "r2" ? "auto" : "us-east-1");
  const service = "s3";

  // path-style: /<bucket>/<key>
  const canonicalUri = "/" + encodeKey(host.bucket) + "/" + encodeKey(key);
  const fullUrl = `${protocol}://${endpointHost}${canonicalUri}`;

  const now = new Date();
  const amzDate = now.toISOString().replace(/[:-]|\.\d{3}/g, ""); // YYYYMMDDTHHMMSSZ
  const dateStamp = amzDate.slice(0, 8);

  const payloadHash = await sha256Hex(body);

  const headers: Record<string, string> = {
    host: endpointHost,
    "content-type": contentType,
    "x-amz-content-sha256": payloadHash,
    "x-amz-date": amzDate,
  };

  const signedHeaderKeys = Object.keys(headers).sort();
  const canonicalHeaders = signedHeaderKeys.map((k) => `${k}:${headers[k].trim()}\n`).join("");
  const signedHeaders = signedHeaderKeys.join(";");

  const canonicalRequest = ["PUT", canonicalUri, "", canonicalHeaders, signedHeaders, payloadHash].join("\n");

  const algorithm = "AWS4-HMAC-SHA256";
  const credentialScope = `${dateStamp}/${region}/${service}/aws4_request`;
  const stringToSign = [algorithm, amzDate, credentialScope, await sha256Hex(canonicalRequest)].join("\n");

  const kDate = await hmac(enc.encode("AWS4" + host.secretAccessKey), dateStamp);
  const kRegion = await hmac(kDate, region);
  const kService = await hmac(kRegion, service);
  const kSigning = await hmac(kService, "aws4_request");
  const signature = toHex(new Uint8Array(await hmac(kSigning, stringToSign)));

  const authorization = `${algorithm} Credential=${host.accessKeyId}/${credentialScope}, SignedHeaders=${signedHeaders}, Signature=${signature}`;

  // 注意：不要显式发送 host 头。Electron / requestUrl 会把 Host 当作禁止头，
  // 手动设置会抛 net::ERR_INVALID_ARGUMENT。它会根据 URL 自动补上正确的 Host，
  // 与签名里的 host 一致即可。
  const sendHeaders: Record<string, string> = { Authorization: authorization };
  for (const k of Object.keys(headers)) {
    if (k.toLowerCase() === "host") continue;
    sendHeaders[k] = headers[k];
  }

  const resp = await requestUrl({
    url: fullUrl,
    method: "PUT",
    headers: sendHeaders,
    body,
    throw: false,
  });

  if (resp.status < 200 || resp.status >= 300) {
    throw new Error(`上传失败 (${resp.status}): ${resp.text?.slice(0, 300) || "未知错误"}`);
  }

  const base = host.publicBaseUrl.replace(/\/+$/, "");
  const url = base ? `${base}/${encodeKey(key)}` : fullUrl;
  return { key, url };
}
