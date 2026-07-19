import { App, Component, MarkdownRenderer } from "obsidian";
import { Theme, CodeColors } from "./themes";
import { styleLists } from "./lists";

/**
 * 将 markdown 渲染为「内联样式」HTML，可直接粘贴到公众号编辑器。
 * 复用 Obsidian 自带的 Markdown / Prism 渲染，再把 class 转成内联 style。
 */

const TAG_TO_KEY: Record<string, keyof Theme["styles"]> = {
  H1: "h1",
  H2: "h2",
  H3: "h3",
  H4: "h4",
  H5: "h5",
  H6: "h6",
  P: "p",
  A: "a",
  STRONG: "strong",
  B: "strong",
  EM: "em",
  I: "em",
  DEL: "del",
  S: "del",
  UL: "ul",
  OL: "ol",
  LI: "li",
  BLOCKQUOTE: "blockquote",
  HR: "hr",
  IMG: "img",
  FIGCAPTION: "figcaption",
  TABLE: "table",
  TH: "th",
  TD: "td",
};

// 渲染产物里需要直接删掉的元素
const STRIP_SELECTORS = [
  ".frontmatter",
  ".frontmatter-container",
  ".metadata-container",
  ".markdown-preview-pusher",
  ".copy-code-button",
  ".edit-block-button",
  ".collapse-indicator",
  ".heading-collapse-indicator",
  "button",
];

function tokenColor(classList: DOMTokenList, c: CodeColors): string | null {
  const has = (n: string) => classList.contains(n);
  if (has("comment") || has("prolog") || has("doctype") || has("cdata")) return c.comment;
  if (has("keyword") || has("boolean") || has("important") || has("atrule") || has("selector")) return c.keyword;
  if (has("string") || has("char") || has("attr-value") || has("regex") || has("url") || has("inserted"))
    return c.string;
  if (has("number") || has("constant") || has("symbol")) return c.number;
  if (has("function") || has("function-name")) return c.function;
  if (has("class-name") || has("builtin") || has("namespace")) return c.className;
  if (has("operator") || has("entity")) return c.operator;
  if (has("punctuation")) return c.punctuation;
  if (has("variable") || has("deleted")) return c.variable;
  if (has("property") || has("attr-name") || has("tag") || has("property-access")) return c.property;
  return null;
}

function styleCodeBlock(pre: HTMLElement, theme: Theme) {
  const c = theme.code;
  let style = theme.styles.pre;
  style += `background:${c.background};border:1px solid ${c.border};color:${c.text};`;
  pre.setAttribute("style", style);
  // <code> 容器透明化
  pre.querySelectorAll("code").forEach((code) => {
    code.setAttribute("style", `background:transparent;padding:0;color:${c.text};font-family:inherit;font-size:inherit;`);
  });
  // token 上色
  pre.querySelectorAll("span").forEach((span) => {
    const color = tokenColor(span.classList, c);
    span.setAttribute("style", color ? `color:${color};` : `color:${c.text};`);
    span.removeAttribute("class");
  });
}

function applyStyles(root: HTMLElement, theme: Theme) {
  const c = theme.code;
  const walk = (el: HTMLElement) => {
    const tag = el.tagName;

    if (tag === "PRE") {
      styleCodeBlock(el, theme);
      return; // 内部已处理
    }

    if (tag === "CODE") {
      // 行内 code（不在 pre 内，否则上面已 return）
      el.setAttribute(
        "style",
        `background:${c.inlineBg};color:${c.inlineText};padding:2px 6px;border-radius:5px;border:1px solid ${c.border};font-family:'SFMono-Regular',Menlo,Consolas,monospace;font-size:0.92em;`
      );
      el.removeAttribute("class");
      return;
    }

    const key = TAG_TO_KEY[tag];
    if (key) {
      el.setAttribute("style", theme.styles[key]);
    } else if (tag === "DIV" && el.classList.contains("callout")) {
      el.setAttribute("style", theme.styles.blockquote);
    } else if (tag === "SPAN" || tag === "DIV" || tag === "SECTION") {
      el.removeAttribute("style");
    }
    el.removeAttribute("class");

    Array.from(el.children).forEach((child) => walk(child as HTMLElement));
  };
  Array.from(root.children).forEach((child) => walk(child as HTMLElement));
}

export interface ConvertResult {
  html: string;
  /** 是否存在非 http(s) 的本地图片（粘贴到公众号无法显示）。 */
  hasLocalImage: boolean;
}

export async function convertMarkdownToHtml(
  app: App,
  markdown: string,
  sourcePath: string,
  theme: Theme,
  component: Component
): Promise<ConvertResult> {
  const sandbox = document.createElement("div");
  sandbox.style.position = "fixed";
  sandbox.style.left = "-99999px";
  sandbox.style.top = "0";
  document.body.appendChild(sandbox);

  try {
    await MarkdownRenderer.render(app, markdown, sandbox, sourcePath, component);

    STRIP_SELECTORS.forEach((sel) => sandbox.querySelectorAll(sel).forEach((n) => n.remove()));

    let hasLocalImage = false;
    sandbox.querySelectorAll("img").forEach((img) => {
      const src = img.getAttribute("src") || "";
      if (!/^(https?:)?\/\//.test(src) && !src.startsWith("data:")) hasLocalImage = true;
    });

    applyStyles(sandbox, theme);
    styleLists(sandbox, theme);

    const section = document.createElement("section");
    section.setAttribute("style", theme.container);
    section.innerHTML = sandbox.innerHTML;

    return { html: section.outerHTML, hasLocalImage };
  } finally {
    sandbox.remove();
  }
}
