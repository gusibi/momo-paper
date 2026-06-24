/** 将富文本 HTML 写入剪贴板，使其可粘贴到公众号编辑器。 */
export async function copyHtml(html: string): Promise<void> {
  // 优先使用异步 Clipboard API（同时写 html 与纯文本）
  try {
    if (navigator.clipboard && typeof ClipboardItem !== "undefined") {
      const item = new ClipboardItem({
        "text/html": new Blob([html], { type: "text/html" }),
        "text/plain": new Blob([stripHtml(html)], { type: "text/plain" }),
      });
      await navigator.clipboard.write([item]);
      return;
    }
  } catch (e) {
    // 落到 execCommand 兜底
  }

  // 兜底：隐藏 contenteditable + execCommand('copy')
  const holder = document.createElement("div");
  holder.setAttribute("contenteditable", "true");
  holder.style.position = "fixed";
  holder.style.left = "-99999px";
  holder.style.top = "0";
  holder.innerHTML = html;
  document.body.appendChild(holder);
  try {
    const range = document.createRange();
    range.selectNodeContents(holder);
    const sel = window.getSelection();
    sel?.removeAllRanges();
    sel?.addRange(range);
    const ok = document.execCommand("copy");
    sel?.removeAllRanges();
    if (!ok) throw new Error("execCommand copy failed");
  } finally {
    holder.remove();
  }
}

function stripHtml(html: string): string {
  const tmp = document.createElement("div");
  tmp.innerHTML = html;
  return tmp.textContent || "";
}
