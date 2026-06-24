import { Component, MarkdownView, Notice, Plugin, TFile, WorkspaceLeaf, debounce } from "obsidian";
import {
  DEFAULT_SETTINGS,
  MarkdownToMpSettings,
  MarkdownToMpSettingTab,
} from "./settings";
import { THEMES, ThemeId } from "./themes";
import { scanLocalImages, rewriteMarkdown, LocalImage } from "./images";
import { convertMarkdownToHtml } from "./converter";
import { copyHtml } from "./clipboard";
import { uploadObject, hashBytes } from "./uploader";
import { UploadConfirmModal } from "./modals";
import { MpPreviewView, VIEW_TYPE_MP_PREVIEW } from "./view";

export default class MarkdownToMpPlugin extends Plugin {
  settings!: MarkdownToMpSettings;

  async onload() {
    await this.loadSettings();

    this.registerView(VIEW_TYPE_MP_PREVIEW, (leaf) => new MpPreviewView(leaf, this));

    this.addRibbonIcon("clipboard-copy", "打开公众号预览", () => this.activateView());

    this.addCommand({
      id: "open-preview",
      name: "打开公众号预览面板",
      callback: () => this.activateView(),
    });

    this.addCommand({
      id: "copy-to-wechat",
      name: "复制为公众号格式",
      callback: () => this.copyActiveNote(this.settings.theme),
    });

    // 切换笔记 / 编辑内容时刷新预览面板
    const refresh = debounce(() => this.refreshPreview(), 400, true);
    this.registerEvent(this.app.workspace.on("active-leaf-change", () => refresh()));
    this.registerEvent(this.app.workspace.on("file-open", () => refresh()));
    this.registerEvent(this.app.workspace.on("editor-change", () => refresh()));

    this.addSettingTab(new MarkdownToMpSettingTab(this.app, this));
  }

  onunload() {
    this.app.workspace.detachLeavesOfType(VIEW_TYPE_MP_PREVIEW);
  }

  /** 在右侧边栏打开（或聚焦）预览面板。 */
  async activateView() {
    const { workspace } = this.app;
    let leaf = workspace.getLeavesOfType(VIEW_TYPE_MP_PREVIEW)[0];
    if (!leaf) {
      leaf = workspace.getRightLeaf(false) as WorkspaceLeaf;
      await leaf.setViewState({ type: VIEW_TYPE_MP_PREVIEW, active: true });
    }
    workspace.revealLeaf(leaf);
  }

  private refreshPreview() {
    for (const leaf of this.app.workspace.getLeavesOfType(VIEW_TYPE_MP_PREVIEW)) {
      const view = leaf.view;
      if (view instanceof MpPreviewView) view.render();
    }
  }

  async loadSettings() {
    const loaded = await this.loadData();
    this.settings = Object.assign({}, DEFAULT_SETTINGS, loaded);
    this.settings.imageHost = Object.assign({}, DEFAULT_SETTINGS.imageHost, loaded?.imageHost);
    this.settings.uploadCache = loaded?.uploadCache ?? {};
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }

  async getActiveMarkdown(): Promise<{ file: TFile; content: string } | null> {
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (view?.file && view.getMode() === "source") {
      return { file: view.file, content: view.editor.getValue() };
    }
    // 预览面板聚焦时 getActiveViewOfType 为空，退回最近打开的 markdown 文件
    const file = view?.file ?? this.app.workspace.getActiveFile();
    if (file && file.extension === "md") {
      const content = await this.app.vault.read(file);
      return { file, content };
    }
    return null;
  }

  /**
   * 生成预览 HTML（不上传图片，本地图片用 Obsidian 资源直接显示）。
   * 供右侧预览面板使用，component 用于渲染生命周期管理。
   */
  async buildPreviewHtml(
    themeId: ThemeId,
    component: Component
  ): Promise<{ html: string; fileName: string; hasLocalImage: boolean } | null> {
    const active = await this.getActiveMarkdown();
    if (!active) return null;
    const theme = THEMES[themeId];
    const { html, hasLocalImage } = await convertMarkdownToHtml(
      this.app,
      active.content,
      active.file.path,
      theme,
      component
    );
    return { html, fileName: active.file.basename, hasLocalImage };
  }

  /** 完整流程：按需上传本地图片 → 转换 → 复制到剪贴板。 */
  async copyActiveNote(themeId: ThemeId) {
    const active = await this.getActiveMarkdown();
    if (!active) {
      new Notice("请先在编辑器中打开一篇 Markdown 笔记。");
      return;
    }
    const { file } = active;
    let markdown = active.content;
    const theme = THEMES[themeId];
    const host = this.settings.imageHost;

    const locals = scanLocalImages(this.app, markdown, file.path);

    if (locals.length > 0) {
      if (host.provider === "none") {
        new Notice("检测到本地图片，但未配置图床，公众号中将无法显示。可在设置中配置 R2 / S3。", 6000);
      } else if (this.settings.askBeforeUpload) {
        const choice = await new UploadConfirmModal(this.app, locals.length).openAndWait();
        if (choice === "cancel") return;
        if (choice === "upload") {
          const map = await this.uploadAll(locals);
          if (!map) return;
          markdown = rewriteMarkdown(markdown, map);
        }
      } else {
        const map = await this.uploadAll(locals);
        if (!map) return;
        markdown = rewriteMarkdown(markdown, map);
      }
    }

    const component = new Component();
    component.load();
    try {
      const { html } = await convertMarkdownToHtml(this.app, markdown, file.path, theme, component);
      await this.doCopy(html);
    } catch (e) {
      console.error(e);
      new Notice("转换失败：" + (e as Error).message);
    } finally {
      component.unload();
    }
  }

  private async doCopy(html: string) {
    try {
      await copyHtml(html);
      new Notice("已复制公众号格式，可直接粘贴到公众号编辑器。");
    } catch (e) {
      console.error(e);
      new Notice("复制失败：" + (e as Error).message);
    }
  }

  /** 上传全部本地图片，返回 raw→url 映射；失败返回 null。相同内容只上传一次（内容寻址 + 持久缓存）。 */
  private async uploadAll(locals: LocalImage[]): Promise<Map<string, string> | null> {
    const host = this.settings.imageHost;
    const cache = this.settings.uploadCache;
    const map = new Map<string, string>();
    const notice = new Notice(`正在处理图片 0/${locals.length}…`, 0);
    try {
      let i = 0;
      let uploaded = 0;
      let reused = 0;
      let dirty = false;
      // 本次运行内按内容哈希去重
      const seen = new Map<string, string>();
      for (const item of locals) {
        i++;
        notice.setMessage(`正在处理图片 ${i}/${locals.length}…`);
        const data = await this.app.vault.readBinary(item.file);
        const hash = await hashBytes(data);
        // 缓存键带上图床标识，换桶/换域名后不会误用旧链接
        const cacheKey = `${host.provider}:${host.bucket}:${host.publicBaseUrl}:${hash}`;

        let url = seen.get(cacheKey) ?? cache[cacheKey];
        if (url) {
          reused++;
        } else {
          notice.setMessage(`正在上传图片 ${i}/${locals.length}…`);
          const prefix = host.keyPrefix ? host.keyPrefix.replace(/^\/+|\/+$/g, "") + "/" : "";
          const key = prefix + buildKey(item.file, hash);
          const res = await uploadObject(host, key, data, mimeOf(item.file.extension));
          url = res.url;
          cache[cacheKey] = url;
          dirty = true;
          uploaded++;
        }
        seen.set(cacheKey, url);
        map.set(item.raw, url);
      }
      if (dirty) await this.saveSettings();
      notice.hide();
      new Notice(`图片处理完成：上传 ${uploaded} 张，复用 ${reused} 张（已存在未重传）。`);
      return map;
    } catch (e) {
      notice.hide();
      console.error(e);
      new Notice("图片上传失败：" + (e as Error).message, 8000);
      return null;
    }
  }
}

function buildKey(file: TFile, hash: string): string {
  // 内容寻址：相同内容得到相同 key，重复上传只会覆盖同一对象，不产生副本
  const base = file.basename.replace(/[^\w.\-]+/g, "_").slice(0, 40) || "img";
  return `${base}-${hash.slice(0, 16)}.${file.extension}`;
}

function mimeOf(ext: string): string {
  const e = ext.toLowerCase();
  const m: Record<string, string> = {
    png: "image/png",
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    gif: "image/gif",
    webp: "image/webp",
    bmp: "image/bmp",
    svg: "image/svg+xml",
    avif: "image/avif",
  };
  return m[e] || "application/octet-stream";
}
