import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import Module from "node:module";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import esbuild from "esbuild";

const root = path.resolve(import.meta.dirname, "..");
const temp = fs.mkdtempSync(path.join(os.tmpdir(), "markdown-to-mp-test-"));

try {
  const failures = [];
  for (const [name, test] of [
    ["clipboard fallback after upload", testClipboardFallback],
    ["WeChat list content grouping", testWechatListContentGrouping],
  ]) {
    try {
      await test();
      console.log(`ok - ${name}`);
    } catch (error) {
      failures.push(error);
      console.error(`not ok - ${name}: ${error.message}`);
    }
  }
  if (failures.length) throw new AggregateError(failures, `${failures.length} regression(s) failed`);
  console.log("regressions ok");
} finally {
  fs.rmSync(temp, { recursive: true, force: true });
}

async function testClipboardFallback() {
  const outfile = path.join(temp, "clipboard.cjs");
  await esbuild.build({
    entryPoints: [path.join(root, "src/clipboard.ts")],
    outfile,
    bundle: true,
    format: "cjs",
    platform: "node",
    external: ["electron"],
  });

  const electronWrites = [];
  const originalLoad = Module._load;
  Module._load = function (request, parent, isMain) {
    if (request === "electron") {
      return { clipboard: { write: (payload) => electronWrites.push(payload) } };
    }
    return originalLoad.call(this, request, parent, isMain);
  };

  Object.defineProperty(globalThis, "navigator", {
    configurable: true,
    value: {
      clipboard: {
        write: async () => {
          throw new DOMException("Write permission denied after upload", "NotAllowedError");
        },
      },
    },
  });
  globalThis.ClipboardItem = class ClipboardItem {
    constructor(data) {
      this.data = data;
    }
  };
  globalThis.document = {
    createElement() {
      return {
        style: {},
        setAttribute() {},
        remove() {},
        set innerHTML(value) {
          this.textContent = value.replace(/<[^>]+>/g, "");
        },
        textContent: "",
      };
    },
    body: { appendChild() {} },
    createRange() {
      return { selectNodeContents() {} };
    },
    execCommand() {
      return false;
    },
  };
  globalThis.window = { getSelection: () => null };

  try {
    const { copyHtml } = await import(`${pathToFileURL(outfile).href}?t=${Date.now()}`);
    await copyHtml("<p>uploaded image</p>");
    assert.deepEqual(electronWrites, [
      { html: "<p>uploaded image</p>", text: "uploaded image" },
    ]);
  } finally {
    Module._load = originalLoad;
  }
}

async function testWechatListContentGrouping() {
  const entry = path.join(temp, "list-entry.ts");
  const script = path.join(temp, "list-test.js");
  const html = path.join(temp, "list-test.html");
  fs.writeFileSync(
    entry,
    `import { styleLists } from ${JSON.stringify(path.join(root, "src/lists.ts"))};\n` +
      `import { THEMES } from ${JSON.stringify(path.join(root, "src/themes.ts"))};\n` +
      `const root = document.querySelector('#root');\n` +
      `styleLists(root, THEMES['momo-paper']);\n` +
      `const li = root.querySelector('li');\n` +
      `for (const node of [...li.childNodes]) {\n` +
      `  if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {\n` +
      `    const section = document.createElement('section');\n` +
      `    const leaf = document.createElement('span');\n` +
      `    leaf.setAttribute('leaf', '');\n` +
      `    leaf.textContent = node.textContent;\n` +
      `    section.appendChild(leaf);\n` +
      `    li.replaceChild(section, node);\n` +
      `  }\n` +
      `}\n` +
      `for (const span of li.querySelectorAll(':scope > span')) {\n` +
      `  const leaf = document.createElement('span');\n` +
      `  leaf.setAttribute('leaf', '');\n` +
      `  leaf.textContent = span.textContent;\n` +
      `  span.replaceChildren(leaf);\n` +
      `}\n` +
      `for (const section of li.querySelectorAll(':scope > section')) {\n` +
      `  for (const node of [...section.childNodes]) {\n` +
      `    if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {\n` +
      `      const leaf = document.createElement('span');\n` +
      `      leaf.setAttribute('leaf', '');\n` +
      `      leaf.textContent = node.textContent;\n` +
      `      section.replaceChild(leaf, node);\n` +
      `    }\n` +
      `  }\n` +
      `}\n` +
      `const content = li.firstElementChild;\n` +
      `const pass = li.children.length === 2 && content?.tagName === 'SECTION' && ` +
      `content.querySelector(':scope > span')?.textContent.startsWith('◆') && ` +
      `content.textContent.includes('图片生成是同步返回') && ` +
      `li.lastElementChild?.tagName === 'UL';\n` +
      `document.body.dataset.result = pass ? 'pass' : 'fail';\n`
  );
  await esbuild.build({
    entryPoints: [entry],
    outfile: script,
    bundle: true,
    format: "iife",
    platform: "browser",
    external: ["obsidian"],
  });
  fs.writeFileSync(
    html,
    `<!doctype html><body><div id="root"><ul><li><p>图片生成是同步返回，还是异步任务？</p>` +
      `<ul><li><p>嵌套列表仍需保留</p></li></ul></li></ul></div>` +
      `<script>${fs.readFileSync(script, "utf8")}</script></body>`
  );

  const chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
  const output = execFileSync(chrome, [
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--dump-dom",
    pathToFileURL(html).href,
  ], { encoding: "utf8" });
  assert.match(output, /data-result="pass"/);
}
