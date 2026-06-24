import { App, TFile } from "obsidian";

export interface LocalImage {
  /** 在 markdown 中出现的原始整体文本，例如 ![[a.png]] 或 ![alt](a.png) */
  raw: string;
  file: TFile;
  alt: string;
}

const WIKI_EMBED = /!\[\[([^\]|]+?)(?:\|([^\]]*))?\]\]/g;
const MD_IMAGE = /!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g;

function isRemote(src: string): boolean {
  return /^(https?:)?\/\//.test(src) || src.startsWith("data:");
}

function resolve(app: App, linkpath: string, sourcePath: string): TFile | null {
  const clean = decodeURIComponent(linkpath.split("#")[0].trim());
  const dest = app.metadataCache.getFirstLinkpathDest(clean, sourcePath);
  return dest ?? null;
}

const IMAGE_EXT = ["png", "jpg", "jpeg", "gif", "webp", "bmp", "svg", "avif"];

function isImageFile(file: TFile): boolean {
  return IMAGE_EXT.includes(file.extension.toLowerCase());
}

/** 扫描 markdown 中引用的本地图片（去重，保持出现顺序）。 */
export function scanLocalImages(app: App, markdown: string, sourcePath: string): LocalImage[] {
  const found: LocalImage[] = [];
  const seenRaw = new Set<string>();

  const push = (raw: string, linkpath: string, alt: string) => {
    if (seenRaw.has(raw)) return;
    if (isRemote(linkpath)) return;
    const file = resolve(app, linkpath, sourcePath);
    if (!file || !isImageFile(file)) return;
    seenRaw.add(raw);
    found.push({ raw, file, alt });
  };

  let m: RegExpExecArray | null;
  WIKI_EMBED.lastIndex = 0;
  while ((m = WIKI_EMBED.exec(markdown))) push(m[0], m[1], m[2] || "");
  MD_IMAGE.lastIndex = 0;
  while ((m = MD_IMAGE.exec(markdown))) push(m[0], m[2], m[1] || "");

  return found;
}

/** 用上传后的 URL 重写 markdown 中的本地图片引用。 */
export function rewriteMarkdown(markdown: string, urlMap: Map<string, string>): string {
  let out = markdown;
  for (const [raw, url] of urlMap) {
    // 提取 alt：wiki 嵌入 ![[file|alt]] 取 alt（无则为空，不能回退到普通图片正则，
    // 否则会把内层的 [ 当成 alt，生成 ![[..](url) 这种坏语法）。
    let alt = "";
    if (raw.startsWith("![[")) {
      const w = raw.match(/^!\[\[[^\]|]+\|([^\]]*)\]\]$/);
      alt = w ? w[1] : "";
    } else {
      const m = raw.match(/^!\[([^\]]*)\]/);
      alt = m ? m[1] : "";
    }
    // 清掉会破坏 markdown 图片语法的字符
    alt = alt.replace(/[\[\]\r\n]/g, "").trim();
    out = out.split(raw).join(`![${alt}](${url})`);
  }
  return out;
}
