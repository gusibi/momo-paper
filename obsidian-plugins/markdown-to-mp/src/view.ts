import { ItemView, WorkspaceLeaf } from "obsidian";
import type MarkdownToMpPlugin from "./main";
import { THEMES, ThemeId } from "./themes";

export const VIEW_TYPE_MP_PREVIEW = "markdown-to-mp-preview";

/** 右侧边栏的公众号预览面板：可切换模板、实时预览、一键复制。 */
export class MpPreviewView extends ItemView {
  private plugin: MarkdownToMpPlugin;
  private themeId: ThemeId;
  private previewEl!: HTMLElement;
  private titleEl!: HTMLElement;
  private rendering = false;

  constructor(leaf: WorkspaceLeaf, plugin: MarkdownToMpPlugin) {
    super(leaf);
    this.plugin = plugin;
    this.themeId = plugin.settings.theme;
  }

  getViewType(): string {
    return VIEW_TYPE_MP_PREVIEW;
  }

  getDisplayText(): string {
    return "公众号预览";
  }

  getIcon(): string {
    return "clipboard-copy";
  }

  async onOpen() {
    const root = this.contentEl;
    root.empty();
    root.addClass("mp-preview-view");

    // 工具栏
    const bar = root.createDiv({ cls: "mp-preview-toolbar" });

    const select = bar.createEl("select", { cls: "dropdown mp-preview-select" });
    for (const id of Object.keys(THEMES) as ThemeId[]) {
      const opt = select.createEl("option", { text: THEMES[id].label, value: id });
      if (id === this.themeId) opt.selected = true;
    }
    select.addEventListener("change", async () => {
      this.themeId = select.value as ThemeId;
      this.plugin.settings.theme = this.themeId;
      await this.plugin.saveSettings();
      this.render();
    });

    const copyBtn = bar.createEl("button", { text: "复制", cls: "mod-cta mp-preview-copy" });
    copyBtn.addEventListener("click", () => this.plugin.copyActiveNote(this.themeId));

    const refreshBtn = bar.createEl("button", { text: "刷新" });
    refreshBtn.addEventListener("click", () => this.render());

    this.titleEl = root.createDiv({ cls: "mp-preview-filename" });

    // 预览区（白底，模拟公众号画布）
    this.previewEl = root.createDiv({ cls: "mp-preview-canvas" });

    this.render();
  }

  /** 切换到给定主题（供命令调用）。 */
  setTheme(id: ThemeId) {
    this.themeId = id;
    const sel = this.contentEl.querySelector(".mp-preview-select") as HTMLSelectElement | null;
    if (sel) sel.value = id;
    this.render();
  }

  /** 重新生成预览（不上传图片，本地图片用 Obsidian 资源直接显示）。 */
  async render() {
    if (!this.previewEl) return;
    if (this.rendering) return;
    this.rendering = true;
    try {
      const result = await this.plugin.buildPreviewHtml(this.themeId, this);
      if (!result) {
        this.titleEl.setText("");
        this.previewEl.empty();
        this.previewEl.createDiv({ cls: "mp-preview-empty", text: "请在编辑器中打开一篇 Markdown 笔记。" });
        return;
      }
      this.titleEl.setText(result.fileName + (result.hasLocalImage ? "（含本地图片，复制时可上传图床）" : ""));
      this.previewEl.empty();
      const holder = this.previewEl.createDiv();
      holder.innerHTML = result.html;
    } finally {
      this.rendering = false;
    }
  }

  async onClose() {
    this.contentEl.empty();
  }
}
