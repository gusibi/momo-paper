import { App, PluginSettingTab, Setting } from "obsidian";
import type MarkdownToMpPlugin from "./main";
import { THEMES, ThemeId } from "./themes";

export type ImageHostProvider = "none" | "r2" | "s3";

export interface ImageHostSettings {
  provider: ImageHostProvider;
  /** R2: 账号 ID（用于拼接 endpoint）。S3: 留空。 */
  accountId: string;
  /** S3 自定义 endpoint（可选，留空使用 AWS 默认）。R2 可留空，会用 accountId 拼接。 */
  endpoint: string;
  region: string;
  bucket: string;
  accessKeyId: string;
  secretAccessKey: string;
  /** 上传后用于拼接公开访问 URL 的前缀，例如 https://img.example.com/ 或 https://pub-xxx.r2.dev/ */
  publicBaseUrl: string;
  /** 对象 key 前缀，例如 wechat/ */
  keyPrefix: string;
}

export interface MarkdownToMpSettings {
  theme: ThemeId;
  /** 复制前若检测到本地图片是否弹窗询问上传。false 则永不上传，直接复制（图片可能无法显示）。 */
  askBeforeUpload: boolean;
  imageHost: ImageHostSettings;
  /** 已上传图片缓存：内容哈希(含图床标识) → 公开 URL，避免重复上传。 */
  uploadCache: Record<string, string>;
}

export const DEFAULT_SETTINGS: MarkdownToMpSettings = {
  theme: "momo-paper",
  askBeforeUpload: true,
  imageHost: {
    provider: "none",
    accountId: "",
    endpoint: "",
    region: "auto",
    bucket: "",
    accessKeyId: "",
    secretAccessKey: "",
    publicBaseUrl: "",
    keyPrefix: "",
  },
  uploadCache: {},
};

export class MarkdownToMpSettingTab extends PluginSettingTab {
  plugin: MarkdownToMpPlugin;

  constructor(app: App, plugin: MarkdownToMpPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    containerEl.createEl("h2", { text: "排版样式" });

    new Setting(containerEl)
      .setName("主题风格")
      .setDesc("选择公众号排版使用的设计风格。")
      .addDropdown((dd) => {
        for (const id of Object.keys(THEMES) as ThemeId[]) {
          dd.addOption(id, THEMES[id].label);
        }
        dd.setValue(this.plugin.settings.theme).onChange(async (v) => {
          this.plugin.settings.theme = v as ThemeId;
          await this.plugin.saveSettings();
        });
      });

    containerEl.createEl("h2", { text: "图片上传（图床）" });
    containerEl.createEl("p", {
      text: "微信公众号无法直接粘贴本地图片。配置图床后，复制时可将本地图片自动上传并替换为公开链接。仅支持 Cloudflare R2 与 S3（均为 S3 兼容协议）。",
      cls: "setting-item-description",
    });

    new Setting(containerEl)
      .setName("检测到本地图片时弹窗询问")
      .setDesc("开启后，复制时若发现本地图片会询问是否上传；关闭则直接复制（本地图片在公众号中无法显示）。")
      .addToggle((t) =>
        t.setValue(this.plugin.settings.askBeforeUpload).onChange(async (v) => {
          this.plugin.settings.askBeforeUpload = v;
          await this.plugin.saveSettings();
        })
      );

    const cacheCount = Object.keys(this.plugin.settings.uploadCache || {}).length;
    new Setting(containerEl)
      .setName("已上传缓存")
      .setDesc(
        `已缓存 ${cacheCount} 张图片的上传记录，相同图片不会重复上传。若已在图床删除文件，可清除缓存以便重新上传。`
      )
      .addButton((b) =>
        b.setButtonText("清除缓存").onClick(async () => {
          this.plugin.settings.uploadCache = {};
          await this.plugin.saveSettings();
          this.display();
        })
      );

    const host = this.plugin.settings.imageHost;

    new Setting(containerEl)
      .setName("图床服务商")
      .addDropdown((dd) => {
        dd.addOption("none", "不使用");
        dd.addOption("r2", "Cloudflare R2");
        dd.addOption("s3", "Amazon S3 / 兼容");
        dd.setValue(host.provider).onChange(async (v) => {
          host.provider = v as ImageHostProvider;
          if (v === "r2" && !host.region) host.region = "auto";
          await this.plugin.saveSettings();
          this.display();
        });
      });

    if (host.provider === "none") return;

    if (host.provider === "r2") {
      new Setting(containerEl)
        .setName("Account ID")
        .setDesc("Cloudflare 账号 ID，用于拼接 endpoint（https://<accountId>.r2.cloudflarestorage.com）。")
        .addText((t) =>
          t.setValue(host.accountId).onChange(async (v) => {
            host.accountId = v.trim();
            await this.plugin.saveSettings();
          })
        );
    } else {
      new Setting(containerEl)
        .setName("Endpoint（可选）")
        .setDesc("自定义 S3 endpoint，例如 https://s3.us-east-1.amazonaws.com。留空则使用 AWS 默认。")
        .addText((t) =>
          t.setValue(host.endpoint).onChange(async (v) => {
            host.endpoint = v.trim();
            await this.plugin.saveSettings();
          })
        );
    }

    new Setting(containerEl).setName("Region").setDesc("R2 填 auto；S3 填存储桶区域，如 us-east-1。").addText((t) =>
      t.setValue(host.region).onChange(async (v) => {
        host.region = v.trim();
        await this.plugin.saveSettings();
      })
    );

    new Setting(containerEl).setName("Bucket").addText((t) =>
      t.setValue(host.bucket).onChange(async (v) => {
        host.bucket = v.trim();
        await this.plugin.saveSettings();
      })
    );

    new Setting(containerEl).setName("Access Key ID").addText((t) => {
      t.setValue(host.accessKeyId).onChange(async (v) => {
        host.accessKeyId = v.trim();
        await this.plugin.saveSettings();
      });
    });

    new Setting(containerEl).setName("Secret Access Key").addText((t) => {
      t.inputEl.type = "password";
      t.setValue(host.secretAccessKey).onChange(async (v) => {
        host.secretAccessKey = v.trim();
        await this.plugin.saveSettings();
      });
    });

    new Setting(containerEl)
      .setName("公开访问前缀 URL")
      .setDesc(
        "上传后用于拼接图片链接的前缀。R2 需绑定公开域名或开启 r2.dev，例如 https://pub-xxxx.r2.dev/ ；S3 例如 https://<bucket>.s3.<region>.amazonaws.com/ 。"
      )
      .addText((t) =>
        t.setValue(host.publicBaseUrl).onChange(async (v) => {
          host.publicBaseUrl = v.trim();
          await this.plugin.saveSettings();
        })
      );

    new Setting(containerEl)
      .setName("对象 key 前缀（可选）")
      .setDesc("上传对象的路径前缀，例如 wechat/。")
      .addText((t) =>
        t.setValue(host.keyPrefix).onChange(async (v) => {
          host.keyPrefix = v.trim();
          await this.plugin.saveSettings();
        })
      );
  }
}
