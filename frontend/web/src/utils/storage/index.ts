/**
 * LocalStorage 兼容性检查 + 异常恢复。
 *
 * ── 职责边界 ──
 * - `markStorageInvalidated` / `checkStorageInvalidated` / `resetStorageInvalidated`
 *   构成轻量标志位机制，由路由守卫消费，避免本模块直接操作 Pinia/router（循环依赖）。
 * - `checkStorageCompatibility()` / `validateStorageData()`  存储健康检查。
 * - `StorageKeyManager` / `Storage`  版本化键值存取工具。
 */

// ---------------------------------------------------------------------------
// 存储失效标志位（路由守卫消费）
// ---------------------------------------------------------------------------

/** 标志：存储数据已因异常而被清除，等待路由守卫处理登出 */
let invalidated = false;

/** 标记存储已失效，路由守卫将在下次导航时执行登出 */
export function markStorageInvalidated(): void {
  invalidated = true;
}

/** 查询存储是否已失效 */
export function checkStorageInvalidated(): boolean {
  return invalidated;
}

/** 守卫处理完毕后重置标志位，避免同一会话内重复拦截 */
export function resetStorageInvalidated(): void {
  invalidated = false;
}

/** Storage config + versioned key helpers. */
export class StorageConfig {
  /** 当前应用版本 */
  static readonly CURRENT_VERSION = __APP_VERSION__;

  /** 存储键前缀 */
  static readonly STORAGE_PREFIX = "sys-v";

  /** 版本键名 */
  static readonly VERSION_KEY = "sys-version";

  /** 主题键名（index.html中使用了，如果修改，需要同步修改） */
  static readonly THEME_KEY = "sys-theme";

  /** 上次登录用户ID键名（用于判断是否为同一用户登录） */
  static readonly LAST_USER_ID_KEY = "sys-last-user-id";

  /** 响应式布局切换时暂存桌面端菜单类型 */
  static readonly RESPONSIVE_MENU_TYPE_KEY = "sys-responsive-menu-type";

  /** 跳过升级检查的版本 */
  static readonly SKIP_UPGRADE_VERSION = "1.0.0";

  /** 升级处理延迟时间（毫秒） */
  static readonly UPGRADE_DELAY = 1000;

  /** 登出延迟时间（毫秒） */
  static readonly LOGOUT_DELAY = 1000;

  /**
   * 生成版本化的存储键名
   * @param storeId 存储ID
   * @param version 版本号，默认使用当前版本
   */
  static generateStorageKey(storeId: string, version: string = this.CURRENT_VERSION): string {
    return `${this.STORAGE_PREFIX}${version}-${storeId}`;
  }

  /**
   * 生成旧版本的存储键名（不带分隔符）
   * @param version 版本号，默认使用当前版本
   */
  static generateLegacyKey(version: string = this.CURRENT_VERSION): string {
    return `${this.STORAGE_PREFIX}${version}`;
  }

  /**
   * 创建存储键匹配的正则表达式
   * @param storeId 存储ID
   */
  static createKeyPattern(storeId: string): RegExp {
    return new RegExp(`^${this.STORAGE_PREFIX}[^-]+-${storeId}$`);
  }

  /**
   * 创建当前版本存储键匹配的正则表达式
   */
  static createCurrentVersionPattern(): RegExp {
    return new RegExp(`^${this.STORAGE_PREFIX}${this.CURRENT_VERSION}-`);
  }

  /**
   * 创建任意版本存储键匹配的正则表达式
   */
  static createVersionPattern(): RegExp {
    return new RegExp(`^${this.STORAGE_PREFIX}`);
  }

  /**
   * 检查是否为当前版本的键
   */
  static isCurrentVersionKey(key: string): boolean {
    return key.startsWith(`${this.STORAGE_PREFIX}${this.CURRENT_VERSION}`);
  }

  /**
   * 检查是否为版本化的键
   */
  static isVersionedKey(key: string): boolean {
    return key.startsWith(this.STORAGE_PREFIX);
  }

  /**
   * 从存储键中提取版本号
   */
  static extractVersionFromKey(key: string): string | null {
    const match = key.match(new RegExp(`^${this.STORAGE_PREFIX}([^-]+)`));
    return match ? match[1] : null;
  }

  /**
   * 从存储键中提取存储ID
   */
  static extractStoreIdFromKey(key: string): string | null {
    const match = key.match(new RegExp(`^${this.STORAGE_PREFIX}[^-]+-(.+)$`));
    return match ? match[1] : null;
  }
}

class StorageCompatibilityManager {
  /**
   * 获取系统版本号
   */
  getSystemVersion(): string | null {
    return localStorage.getItem(StorageConfig.VERSION_KEY);
  }

  /**
   * 获取系统存储数据（兼容旧格式）
   */
  getSystemStorage(): any {
    const version = this.getSystemVersion() || StorageConfig.CURRENT_VERSION;
    const legacyKey = StorageConfig.generateLegacyKey(version);
    const data = localStorage.getItem(legacyKey);
    return data ? JSON.parse(data) : null;
  }

  /**
   * 单次遍历 localStorage key，同时判定「是否有当前版本数据」「是否有任意版本数据」。
   * 替代分别调用 hasCurrentVersionStorage / hasAnyVersionStorage 造成的重复遍历。
   */
  private analyzeStorageKeys(): { hasCurrent: boolean; hasAny: boolean } {
    const keys = Object.keys(localStorage);
    const currentPtrn = StorageConfig.createCurrentVersionPattern();
    const anyPtrn = StorageConfig.createVersionPattern();
    let hasCurrent = false;
    let hasAny = false;

    for (const key of keys) {
      if (!hasCurrent && currentPtrn.test(key) && localStorage.getItem(key) !== null) {
        hasCurrent = true;
        if (hasAny) break;
      }
      if (!hasAny && anyPtrn.test(key) && localStorage.getItem(key) !== null) {
        hasAny = true;
        if (hasCurrent) break;
      }
    }
    return { hasCurrent, hasAny };
  }

  /**
   * 获取旧格式的本地存储数据
   */
  private getLegacyStorageData(): Record<string, any> {
    try {
      const systemStorage = this.getSystemStorage();
      return systemStorage || {};
    } catch (error) {
      console.warn("[Storage] 解析旧格式存储数据失败:", error);
      return {};
    }
  }

  /**
   * 显示存储错误消息
   */
  private showStorageError(): void {
    ElMessage({
      type: "error",
      offset: 40,
      duration: 5000,
      message: "系统检测到本地数据异常，请重新登录系统恢复使用！",
    });
  }

  /**
   * 标记存储失效并触发路由守卫登出流程。
   *
   * 流程：
   *   1. 清除 localStorage（Pinia 持久化数据）
   *   2. 设置标志位，供路由守卫检查
   *   3. 派发自定义事件 → App.vue 监听后执行 router.push()
   *   4. 路由守卫检测到标志位 → 调用 userStore.logout() 重置内存状态
   *
   * 使用 CustomEvent 而非 window.location.href 可避免全量页面刷新，
   * 保留 Pinia 和 Vue 实例，仅通过路由导航完成登出。
   */
  private performSystemLogout(): void {
    setTimeout(() => {
      try {
        localStorage.clear();
        markStorageInvalidated();
        console.info("[Storage] 已标记存储失效，触发路由守卫登出流程");
        window.dispatchEvent(new CustomEvent("app:storage-invalidated"));
      } catch (error) {
        console.error("[Storage] 标记存储失效失败:", error);
      }
    }, StorageConfig.LOGOUT_DELAY);
  }

  /**
   * 处理存储异常
   */
  private handleStorageError(): void {
    this.showStorageError();
    this.performSystemLogout();
  }

  /**
   * 验证存储数据完整性。
   *
   * 检测策略（按优先级）：
   *   1. 存在当前版本数据 → 正常
   *   2. 存在其他版本数据 → 可迁移，正常
   *   3. 存在旧格式（无 storeId）数据 → 正常
   *   4. 完全无数据：
   *      - requireAuth=false（首次访问 / 静态路由）→  正常
   *      - requireAuth=true                        →  触发系统登出
   *
   * @param requireAuth  为 true 时，空存储将触发 performSystemLogout
   */
  validateStorageData(requireAuth: boolean = false): boolean {
    try {
      const { hasCurrent, hasAny } = this.analyzeStorageKeys();

      // 1. 当前版本 → 一切正常
      if (hasCurrent) return true;

      // 2. 其他版本 → 待迁移，暂时也能用
      if (hasAny) return true;

      // 3. 旧格式（无 storeId 的老系统）
      const legacyData = this.getLegacyStorageData();
      if (Object.keys(legacyData).length > 0) {
        console.debug("[Storage] 发现旧版本存储数据");
        return true;
      }

      // 4. 完全空存储
      if (requireAuth) {
        console.warn("[Storage] 未发现任何存储数据，需要重新登录");
        this.performSystemLogout();
        return false;
      }
      // 首次访问或静态路由无需登出
      return true;
    } catch (error) {
      console.error("[Storage] 存储数据验证失败:", error);
      if (requireAuth) {
        this.handleStorageError();
        return false;
      }
      return true;
    }
  }
}

// 创建存储兼容性管理器实例
const storageManager = new StorageCompatibilityManager();

/**
 * 获取系统存储数据
 */
export function getSystemStorage(): any {
  return storageManager.getSystemStorage();
}

/**
 * 获取系统版本号
 */
export function getSysVersion(): string | null {
  return storageManager.getSystemVersion();
}

/**
 * 验证本地存储数据
 * @param requireAuth 是否需要验证登录状态（默认 false）
 */
export function validateStorageData(requireAuth: boolean = false): boolean {
  return storageManager.validateStorageData(requireAuth);
}

/**
 * 检查存储兼容性（带 try-catch 的 validateStorageData 包装）。
 *
 * @param requireAuth  是否需要验证登录状态（默认 false）
 *                     为 true 时，空存储将触发系统登出
 */
export function checkStorageCompatibility(requireAuth: boolean = false): boolean {
  try {
    return storageManager.validateStorageData(requireAuth);
  } catch (error) {
    console.error("[Storage] 兼容性检查异常:", error);
    return false;
  }
}

export class StorageKeyManager {
  private getCurrentVersionKey(storeId: string): string {
    return StorageConfig.generateStorageKey(storeId);
  }

  private hasCurrentVersionData(key: string): boolean {
    return localStorage.getItem(key) !== null;
  }

  private findExistingKey(storeId: string): string | null {
    const storageKeys = Object.keys(localStorage);
    const pattern = StorageConfig.createKeyPattern(storeId);
    return storageKeys.find((key) => pattern.test(key) && localStorage.getItem(key)) || null;
  }

  private migrateData(fromKey: string, toKey: string): void {
    try {
      const existingData = localStorage.getItem(fromKey);
      if (existingData) {
        localStorage.setItem(toKey, existingData);
        console.info(`[Storage] 已迁移数据: ${fromKey} → ${toKey}`);
      }
    } catch (error) {
      console.warn(`[Storage] 数据迁移失败: ${fromKey}`, error);
    }
  }

  getStorageKey(storeId: string): string {
    const currentKey = this.getCurrentVersionKey(storeId);
    if (this.hasCurrentVersionData(currentKey)) return currentKey;

    const existingKey = this.findExistingKey(storeId);
    if (existingKey) this.migrateData(existingKey, currentKey);
    return currentKey;
  }
}
