/**
 * 主题定义：每个主题给出公众号正文各元素的内联样式，以及代码高亮的 token 配色。
 *
 * 公众号编辑器会丢弃 <style>、class 和自定义 web 字体，因此所有样式必须内联，
 * 字体只能使用系统字体栈。
 */

export type ThemeId = "momo-paper" | "vercel";

/** 代码高亮配色：键对应 Prism 的 token class（Obsidian 内置 Prism 输出）。 */
export interface CodeColors {
  background: string;
  border: string;
  text: string;
  comment: string;
  keyword: string;
  string: string;
  number: string;
  function: string;
  className: string;
  operator: string;
  punctuation: string;
  variable: string;
  property: string;
  /** 行内 code 的背景/文字 */
  inlineBg: string;
  inlineText: string;
}

export interface Theme {
  label: string;
  /** 选择此主题时附带的高亮样式说明（用于 README / 提示）。 */
  codeStyleName: string;
  /** 最外层容器样式（设置正文基础字号、颜色、字体）。 */
  container: string;
  styles: {
    h1: string;
    h2: string;
    h3: string;
    h4: string;
    h5: string;
    h6: string;
    p: string;
    a: string;
    strong: string;
    em: string;
    del: string;
    ul: string;
    ol: string;
    li: string;
    blockquote: string;
    hr: string;
    img: string;
    figcaption: string;
    pre: string;
    table: string;
    th: string;
    td: string;
  };
  list: ListStyle;
  code: CodeColors;
}

/**
 * 列表样式。公众号会丢弃原生 marker 与伪元素，因此转换器会给每个 <li>
 * 注入一个内联样式的 marker 元素，并用 text-indent 实现悬挂缩进。
 */
export interface ListStyle {
  ul: string;
  ol: string;
  /** 普通 li（含悬挂缩进与 marker 占位宽度） */
  li: string;
  /** 任务列表 li（带 checkbox，不注入 marker） */
  liTask: string;
  /** marker 占位 span 的基础样式（宽度需与 li 的 text-indent 对应） */
  marker: string;
  /** 无序列表各层级的 marker 字符 */
  bullets: string[];
  /** 各层级 marker 颜色 */
  bulletColors: string[];
  /** bullet 字号 */
  bulletSize: string;
  /** 有序列表数字颜色 */
  orderedColor: string;
  /** 有序列表数字附加样式（字体/字重） */
  orderedExtra: string;
}

const SANS =
  "-apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif";
const SERIF = "'Songti SC', 'Noto Serif SC', Georgia, 'Times New Roman', serif";
const MONO = "'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace";

/* ------------------------------------------------------------------ */
/* Momo Paper —— 暖米色书卷风，搭配「Warm Paper」高亮（自定义浅色调，    */
/* 背景取设计系统的 surface 暖色，token 用导航蓝 / 赤陶 / 墨绿，低对比、 */
/* 与正文同源，编辑感强。                                               */
/* ------------------------------------------------------------------ */
const momoPaper: Theme = {
  label: "Momo Paper（暖米书卷）",
  codeStyleName: "Warm Paper（暖纸浅色，导航蓝/赤陶/墨绿）",
  container: `font-family:${SANS};font-size:16px;line-height:1.75;color:#172033;background:#FAF8F4;letter-spacing:0.2px;word-break:break-word;padding:32px 24px;`,
  styles: {
    h1: `font-family:${SERIF};font-size:27px;font-weight:700;line-height:1.3;color:#172033;margin:8px 0 24px;letter-spacing:-0.01em;text-align:center;`,
    h2: `font-family:${SERIF};font-size:21px;font-weight:700;line-height:1.35;color:#244C7A;margin:34px 0 16px;text-align:center;letter-spacing:-0.01em;`,
    h3: `font-family:${SERIF};font-size:18px;font-weight:600;line-height:1.4;color:#172033;margin:26px 0 12px;padding-left:12px;border-left:3px solid #B65C3A;`,
    h4: `font-family:${SANS};font-size:16px;font-weight:600;color:#172033;margin:22px 0 10px;`,
    h5: `font-family:${SANS};font-size:15px;font-weight:600;color:#4C566A;margin:18px 0 8px;`,
    h6: `font-family:${SANS};font-size:14px;font-weight:600;color:#4C566A;margin:16px 0 8px;letter-spacing:0.04em;text-transform:uppercase;`,
    p: `margin:0 0 18px;color:#172033;line-height:1.8;`,
    a: `color:#244C7A;border-bottom:1px solid #DCE7F2;text-decoration:none;`,
    strong: `font-weight:700;color:#172033;`,
    em: `font-style:italic;color:#4C566A;`,
    del: `text-decoration:line-through;color:#8a8472;`,
    ul: `margin:0 0 18px;padding-left:24px;`,
    ol: `margin:0 0 18px;padding-left:24px;`,
    li: `margin:6px 0;line-height:1.8;`,
    blockquote: `margin:18px 0;padding:14px 18px;background:#F2E1D9;border-left:4px solid #B65C3A;border-radius:8px;color:#5b4a40;`,
    hr: `border:none;border-top:1px solid #D8D2C4;margin:32px 0;`,
    img: `display:block;max-width:100%;margin:24px auto;border-radius:10px;border:1px solid #E3DAC9;box-shadow:0 2px 4px rgba(23,32,51,0.06),0 14px 30px -12px rgba(23,32,51,0.20);`,
    figcaption: `text-align:center;font-size:13px;color:#8a8472;margin-top:-8px;margin-bottom:18px;`,
    pre: `margin:18px 0;padding:16px 18px;border-radius:8px;overflow-x:auto;font-family:${MONO};font-size:13px;line-height:1.6;`,
    table: `width:100%;border-collapse:collapse;margin:18px 0;font-size:14px;`,
    th: `border:1px solid #D8D2C4;background:#F2EFE8;padding:8px 12px;text-align:left;font-weight:600;color:#172033;`,
    td: `border:1px solid #D8D2C4;padding:8px 12px;color:#172033;`,
  },
  list: {
    ul: `margin:16px 0;padding-left:0.4em;list-style:none;text-indent:0;`,
    ol: `margin:16px 0;padding-left:0.4em;list-style:none;text-indent:0;`,
    li: `margin:9px 0;padding-left:1.7em;text-indent:-1.7em;line-height:1.8;list-style:none;color:#172033;`,
    liTask: `margin:9px 0;padding-left:0;line-height:1.8;list-style:none;color:#172033;`,
    marker: `display:inline-block;width:1.7em;text-indent:0;`,
    bullets: ["◆", "▸", "▪"],
    bulletColors: ["#B65C3A", "#244C7A", "#8a8170"],
    bulletSize: "0.8em",
    orderedColor: "#244C7A",
    orderedExtra: `font-family:${SERIF};font-weight:700;`,
  },
  code: {
    background: "#F4EFE6",
    border: "#E3DAC9",
    text: "#3a3530",
    comment: "#9a917f",
    keyword: "#244C7A",
    string: "#2F6B4F",
    number: "#B65C3A",
    function: "#3C6587",
    className: "#A46A21",
    operator: "#6b6357",
    punctuation: "#8a8170",
    variable: "#9A3D3D",
    property: "#244C7A",
    inlineBg: "#F2E1D9",
    inlineText: "#9A3D3D",
  },
};

/* ------------------------------------------------------------------ */
/* Vercel Geist —— 极简黑白，蓝色点缀；搭配「Geist Minimal」高亮：       */
/* 近白底、灰边框，token 以灰阶为主，关键字用紫、字符串用绿、函数用蓝，   */
/* 全部取自 Geist 调色板，干净克制。                                    */
/* ------------------------------------------------------------------ */
const vercel: Theme = {
  label: "Vercel Geist（极简）",
  codeStyleName: "Geist Minimal（近白底，灰阶为主，紫/绿/蓝点缀）",
  container: `font-family:${SANS};font-size:16px;line-height:1.7;color:#171717;background:#ffffff;word-break:break-word;padding:32px 24px;`,
  styles: {
    h1: `font-size:30px;font-weight:700;line-height:1.2;color:#171717;margin:8px 0 8px;letter-spacing:-0.03em;text-align:center;`,
    h2: `font-size:22px;font-weight:600;line-height:1.3;color:#171717;margin:36px 0 16px;letter-spacing:-0.02em;text-align:center;padding-bottom:8px;border-bottom:1px solid #ebebeb;`,
    h3: `font-size:18px;font-weight:600;line-height:1.4;color:#171717;margin:28px 0 10px;letter-spacing:-0.01em;padding-left:10px;border-left:3px solid #006bff;`,
    h4: `font-size:16px;font-weight:600;color:#171717;margin:22px 0 8px;letter-spacing:-0.01em;`,
    h5: `font-size:15px;font-weight:600;color:#4d4d4d;margin:18px 0 8px;`,
    h6: `font-size:12px;font-weight:600;color:#8f8f8f;margin:16px 0 8px;letter-spacing:0.06em;text-transform:uppercase;`,
    p: `margin:0 0 18px;color:#333333;line-height:1.75;`,
    a: `color:#006bff;font-weight:500;text-decoration:none;border-bottom:1px solid #94ccff;`,
    strong: `font-weight:600;color:#171717;`,
    em: `font-style:italic;color:#4d4d4d;`,
    del: `text-decoration:line-through;color:#8f8f8f;`,
    ul: `margin:0 0 18px;padding-left:24px;`,
    ol: `margin:0 0 18px;padding-left:24px;`,
    li: `margin:5px 0;line-height:1.75;`,
    blockquote: `margin:20px 0;padding:14px 18px;background:#f0f7ff;border:1px solid #dfefff;border-left:3px solid #006bff;border-radius:6px;color:#3a3f47;`,
    hr: `border:none;border-top:1px solid #eaeaea;margin:32px 0;`,
    img: `display:block;max-width:100%;margin:24px auto;border-radius:12px;border:1px solid #eaeaea;box-shadow:0 1px 2px rgba(0,0,0,0.04),0 14px 30px -12px rgba(0,0,0,0.14);`,
    figcaption: `text-align:center;font-size:13px;color:#8f8f8f;margin-top:-8px;margin-bottom:18px;`,
    pre: `margin:18px 0;padding:16px 18px;border-radius:8px;overflow-x:auto;font-family:${MONO};font-size:13px;line-height:1.6;`,
    table: `width:100%;border-collapse:collapse;margin:18px 0;font-size:14px;`,
    th: `border:1px solid #eaeaea;background:#fafafa;padding:8px 12px;text-align:left;font-weight:600;color:#171717;`,
    td: `border:1px solid #eaeaea;padding:8px 12px;color:#333333;`,
  },
  list: {
    ul: `margin:16px 0;padding-left:0.4em;list-style:none;text-indent:0;`,
    ol: `margin:16px 0;padding-left:0.4em;list-style:none;text-indent:0;`,
    li: `margin:8px 0;padding-left:1.7em;text-indent:-1.7em;line-height:1.75;list-style:none;color:#333333;`,
    liTask: `margin:8px 0;padding-left:0;line-height:1.75;list-style:none;color:#333333;`,
    marker: `display:inline-block;width:1.7em;text-indent:0;`,
    bullets: ["▪", "–", "·"],
    bulletColors: ["#006bff", "#8f8f8f", "#c9c9c9"],
    bulletSize: "0.95em",
    orderedColor: "#006bff",
    orderedExtra: `font-weight:600;`,
  },
  code: {
    background: "#fafafa",
    border: "#eaeaea",
    text: "#171717",
    comment: "#8f8f8f",
    keyword: "#8500d1",
    string: "#28a948",
    number: "#ffa600",
    function: "#006bff",
    className: "#00927f",
    operator: "#4d4d4d",
    punctuation: "#8f8f8f",
    variable: "#d8001b",
    property: "#006bff",
    inlineBg: "#f2f2f2",
    inlineText: "#d8001b",
  },
};

export const THEMES: Record<ThemeId, Theme> = {
  "momo-paper": momoPaper,
  vercel,
};
