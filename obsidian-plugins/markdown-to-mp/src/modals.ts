import { App, Modal, Setting } from "obsidian";

export type UploadChoice = "upload" | "skip" | "cancel";

/** 检测到本地图片时询问是否上传到图床。 */
export class UploadConfirmModal extends Modal {
  private count: number;
  private resolve!: (c: UploadChoice) => void;

  constructor(app: App, count: number) {
    super(app);
    this.count = count;
  }

  openAndWait(): Promise<UploadChoice> {
    return new Promise((res) => {
      this.resolve = res;
      this.open();
    });
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.createEl("h3", { text: "检测到本地图片" });
    contentEl.createEl("p", {
      text: `当前笔记包含 ${this.count} 张本地图片。微信公众号无法显示本地图片，是否先上传到图床并替换为公开链接？`,
    });

    new Setting(contentEl)
      .addButton((b) =>
        b
          .setButtonText("上传并复制")
          .setCta()
          .onClick(() => this.done("upload"))
      )
      .addButton((b) => b.setButtonText("不上传，直接复制").onClick(() => this.done("skip")))
      .addButton((b) => b.setButtonText("取消").onClick(() => this.done("cancel")));
  }

  private done(choice: UploadChoice) {
    this.resolve(choice);
    this.close();
  }

  onClose() {
    this.contentEl.empty();
    // 若用户直接关闭弹窗，按取消处理
    if (this.resolve) this.resolve("cancel");
  }
}
