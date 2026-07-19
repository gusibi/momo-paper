import type { Theme } from "./themes";

/** 列表层级（相对 root 的 ul/ol 嵌套深度）。 */
function listDepth(list: HTMLElement, root: HTMLElement): number {
  let depth = 0;
  let p = list.parentElement;
  while (p && p !== root) {
    if (p.tagName === "UL" || p.tagName === "OL") depth++;
    p = p.parentElement;
  }
  return depth;
}

/**
 * 重排列表：清掉原生 marker，给每个 <li> 注入内联样式的 marker，
 * 用 text-indent 悬挂缩进保证换行对齐。公众号会丢弃 ::marker / 伪元素，
 * 所以必须注入真实元素。
 */
export function styleLists(root: HTMLElement, theme: Theme) {
  const L = theme.list;
  root.querySelectorAll("ul, ol").forEach((listNode) => {
    const list = listNode as HTMLElement;
    const ordered = list.tagName === "OL";
    list.setAttribute("style", ordered ? L.ol : L.ul);

    const level = listDepth(list, root);
    let n = ordered ? parseInt(list.getAttribute("start") || "1", 10) || 1 : 1;

    Array.from(list.children).forEach((child) => {
      const li = child as HTMLElement;
      if (li.tagName !== "LI") return;

      // 任务列表（直接子级含 checkbox）：不注入 marker，保留勾选框
      if (li.querySelector(":scope > input[type=checkbox]")) {
        li.setAttribute("style", L.liTask);
        return;
      }

      li.setAttribute("style", L.li);

      // Obsidian 会把列表正文包在块级 <p> 中；插件预览的全局 CSS 会把它
      // 显示成同行，但公众号按块级元素渲染，导致 marker 独占一行。
      const firstBlock = li.firstElementChild;
      if (firstBlock?.tagName === "P") {
        while (firstBlock.firstChild) li.insertBefore(firstBlock.firstChild, firstBlock);
        firstBlock.remove();
      }

      const marker = document.createElement("span");
      if (ordered) {
        marker.setAttribute("style", `${L.marker}${L.orderedExtra}color:${L.orderedColor};`);
        marker.textContent = `${n}.`;
        n++;
      } else {
        const i = Math.min(level, L.bullets.length - 1);
        marker.setAttribute(
          "style",
          `${L.marker}font-size:${L.bulletSize};color:${L.bulletColors[i]};`
        );
        marker.textContent = L.bullets[i];
      }

      // 公众号会把 <li> 的裸文本另包成块级 <section>。预先把 marker 与首段
      // 行内正文放进同一个 section，使公众号规范化 DOM 后也不会把两者拆行。
      const lineNodes: ChildNode[] = [];
      for (const node of Array.from(li.childNodes)) {
        if (isListBlockBoundary(node)) break;
        lineNodes.push(node);
      }
      const line = document.createElement("section");
      li.insertBefore(line, li.firstChild);
      line.appendChild(marker);
      lineNodes.forEach((node) => line.appendChild(node));
    });
  });
}

function isListBlockBoundary(node: ChildNode): boolean {
  if (node.nodeType !== Node.ELEMENT_NODE) return false;
  return ["UL", "OL", "P", "DIV", "SECTION", "BLOCKQUOTE", "PRE", "TABLE"].includes(
    (node as HTMLElement).tagName
  );
}
