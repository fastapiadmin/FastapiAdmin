/** System helpers (flattened). */

import type { App } from "vue";
import mitt, { type Emitter } from "mitt";
import { upgradeLogList } from "@/mock/upgrade/changeLog";
import { ElNotification } from "element-plus";
import { useUserStore } from "@/store/modules/user.store";
import { StorageConfig } from "@/utils/storage";

// -----------------------------
// Console banner
// -----------------------------

export function printConsoleBanner(): void {
  // ANSI escape codes via https://patorjk.com/software/taag/#p=display&f=Big&t=ABB%0A
  const asciiArt = `
\x1b[32m欢迎使用 Fastapi Admin！
\x1b[0m
\x1b[36m哇！你居然在用我的项目～ 好用的话别忘了去 GitHub 点个 ★Star 呀，你的支持就是我更新的超强动力！祝使用体验满分💯
\x1b[0m
\x1b[33mGitHub: https://github.com/fastapiadmin/FastapiAdmin
\x1b[0m
\x1b[31m技术支持（社区群）: https://service.fastapiadmin.com/about/，和开发者一起交流～ 群里有小伙伴实时答疑，遇到问题不用慌！
\x1b[0m
`;

  console.log(asciiArt);
}

// -----------------------------
// Mitt bus
// -----------------------------

type SysEvents = {
  triggerFireworks: string | undefined;
  openSetting: void;
  openSearchDialog: void;
  openChat: void;
  openLockScreen: void;
};

export const mittBus: Emitter<SysEvents> = mitt<SysEvents>();

// -----------------------------
// Error handling
// -----------------------------

const IGNORABLE_SCRIPT_ERRORS = [
  "ResizeObserver loop completed with undelivered notifications.",
  "ResizeObserver loop limit exceeded",
];

function normalizeErrorMessage(message: Event | string): string {
  if (typeof message === "string") return message;
  if ("message" in message && typeof message.message === "string") return message.message;
  return "";
}

function isIgnorableScriptError(message: Event | string, source?: string): boolean {
  const normalizedMessage = normalizeErrorMessage(message);
  if (!normalizedMessage) return false;

  if (IGNORABLE_SCRIPT_ERRORS.some((item) => normalizedMessage.includes(item))) {
    // 浏览器/扩展在布局抖动时常见的 ResizeObserver 噪声，不作为真实异常处理
    return true;
  }

  // 浏览器扩展注入脚本偶发的跨域 Script error 也没有排查价值
  if (normalizedMessage === "Script error." && source === "") return true;
  return false;
}

export function vueErrorHandler(err: unknown, instance: any, info: string) {
  console.error("[VueError]", err, info, instance);
}

export function scriptErrorHandler(
  message: Event | string,
  source?: string,
  lineno?: number,
  colno?: number,
  error?: Error
): boolean {
  if (isIgnorableScriptError(message, source)) return true;
  console.error("[ScriptError]", { message, source, lineno, colno, error });
  return true;
}

export function registerPromiseErrorHandler() {
  window.addEventListener("unhandledrejection", (event) => {
    console.error("[PromiseError]", event.reason);
  });
}

export function registerResourceErrorHandler() {
  window.addEventListener(
    "error",
    (event: Event) => {
      const target = event.target as HTMLElement;
      if (
        target &&
        (target.tagName === "IMG" || target.tagName === "SCRIPT" || target.tagName === "LINK")
      ) {
        console.error("[ResourceError]", {
          tagName: target.tagName,
          src:
            (target as HTMLImageElement).src ||
            (target as HTMLScriptElement).src ||
            (target as HTMLLinkElement).href,
        });
      }
    },
    true
  );
}

export function initErrorHandle(app: App) {
  app.config.errorHandler = vueErrorHandler;
  window.onerror = scriptErrorHandler;
  registerPromiseErrorHandler();
  registerResourceErrorHandler();
}

// -----------------------------
// Upgrade
// -----------------------------

class VersionManager {
  private normalizeVersion(version: string): string {
    return version.replace(/^v/, "");
  }

  private getStoredVersion(): string | null {
    return localStorage.getItem(StorageConfig.VERSION_KEY);
  }

  private setStoredVersion(version: string): void {
    localStorage.setItem(StorageConfig.VERSION_KEY, version);
  }

  private shouldSkipUpgrade(): boolean {
    return StorageConfig.CURRENT_VERSION === StorageConfig.SKIP_UPGRADE_VERSION;
  }

  private isFirstVisit(storedVersion: string | null): boolean {
    return !storedVersion;
  }

  private isSameVersion(storedVersion: string): boolean {
    return storedVersion === StorageConfig.CURRENT_VERSION;
  }

  private findLegacyStorage(): { oldSysKey: string | null; oldVersionKeys: string[] } {
    const storageKeys = Object.keys(localStorage);
    const currentVersionPrefix = StorageConfig.generateStorageKey("").slice(0, -1);

    const oldSysKey =
      storageKeys.find(
        (key) =>
          StorageConfig.isVersionedKey(key) && key !== currentVersionPrefix && !key.includes("-")
      ) || null;

    const oldVersionKeys = storageKeys.filter(
      (key) =>
        StorageConfig.isVersionedKey(key) &&
        !StorageConfig.isCurrentVersionKey(key) &&
        key.includes("-")
    );

    return { oldSysKey, oldVersionKeys };
  }

  private shouldRequireReLogin(storedVersion: string): boolean {
    const normalizedCurrent = this.normalizeVersion(StorageConfig.CURRENT_VERSION);
    const normalizedStored = this.normalizeVersion(storedVersion);

    return upgradeLogList.value.some((item) => {
      const itemVersion = this.normalizeVersion(item.version);
      return (
        item.requireReLogin && itemVersion > normalizedStored && itemVersion <= normalizedCurrent
      );
    });
  }

  private buildUpgradeMessage(requireReLogin: boolean): string {
    const { title: content } = upgradeLogList.value[0];
    const messageParts = [
      `<p style="color: var(--art-gray-800) !important; padding-bottom: 5px;">`,
      `系统已升级到 ${StorageConfig.CURRENT_VERSION} 版本，此次更新带来了以下改进：`,
      `</p>`,
      content,
    ];

    if (requireReLogin) {
      messageParts.push(
        `<p style="color: var(--theme-color); padding-top: 5px;">升级完成，请重新登录后继续使用。</p>`
      );
    }

    return messageParts.join("");
  }

  private showUpgradeNotification(message: string): void {
    ElNotification({
      title: "系统升级公告",
      message,
      duration: 0,
      type: "success",
      dangerouslyUseHTMLString: true,
    });
  }

  private cleanupLegacyData(oldSysKey: string | null, oldVersionKeys: string[]): void {
    if (oldSysKey) {
      localStorage.removeItem(oldSysKey);
      console.info(`[Upgrade] 已清理旧存储: ${oldSysKey}`);
    }

    oldVersionKeys.forEach((key) => {
      localStorage.removeItem(key);
      console.info(`[Upgrade] 已清理旧存储: ${key}`);
    });
  }

  private performLogout(): void {
    try {
      useUserStore().logout();
      console.info("[Upgrade] 已执行升级后登出");
    } catch (error) {
      console.error("[Upgrade] 升级后登出失败:", error);
    }
  }

  private async executeUpgrade(
    storedVersion: string,
    legacyStorage: ReturnType<typeof this.findLegacyStorage>
  ): Promise<void> {
    try {
      if (!upgradeLogList.value.length) {
        console.warn("[Upgrade] 升级日志列表为空");
        return;
      }

      const requireReLogin = this.shouldRequireReLogin(storedVersion);
      const message = this.buildUpgradeMessage(requireReLogin);

      this.showUpgradeNotification(message);
      this.setStoredVersion(StorageConfig.CURRENT_VERSION);
      this.cleanupLegacyData(legacyStorage.oldSysKey, legacyStorage.oldVersionKeys);
      if (requireReLogin) this.performLogout();

      console.info(`[Upgrade] 升级完成: ${storedVersion} → ${StorageConfig.CURRENT_VERSION}`);
    } catch (error) {
      console.error("[Upgrade] 系统升级处理失败:", error);
    }
  }

  async processUpgrade(): Promise<void> {
    if (this.shouldSkipUpgrade()) {
      console.debug("[Upgrade] 跳过版本升级检查");
      return;
    }

    const storedVersion = this.getStoredVersion();
    if (this.isFirstVisit(storedVersion)) {
      this.setStoredVersion(StorageConfig.CURRENT_VERSION);
      console.info("[Upgrade] 首次访问，已设置当前版本");
      return;
    }

    if (this.isSameVersion(storedVersion!)) {
      console.debug("[Upgrade] 版本相同，无需升级");
      return;
    }

    const legacyStorage = this.findLegacyStorage();
    if (!legacyStorage.oldSysKey && legacyStorage.oldVersionKeys.length === 0) {
      this.setStoredVersion(StorageConfig.CURRENT_VERSION);
      console.info("[Upgrade] 无旧数据，已更新版本号");
      return;
    }

    await this.executeUpgrade(storedVersion!, legacyStorage);
  }
}

export async function processUpgrade(): Promise<void> {
  const versionManager = new VersionManager();
  await versionManager.processUpgrade();
}

export function systemUpgrade(): void {
  setTimeout(() => {
    void processUpgrade();
  }, StorageConfig.UPGRADE_DELAY);
}
