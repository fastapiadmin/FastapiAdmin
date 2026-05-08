/** LocalStorage compatibility checks + recovery helpers.
 *
 * 禁止在此文件顶层 `import "@/router"` / user store：会触发
 * router → guards → navigation → locales → storage 的循环依赖，
 * 并在 locales 同步导入 storage 时出现 StorageKeyManager TDZ。
 * 登出逻辑在 `performSystemLogout` 内动态 import。
 */

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
   * 检查当前版本是否有存储数据
   */
  private hasCurrentVersionStorage(): boolean {
    const storageKeys = Object.keys(localStorage);
    const currentVersionPattern = StorageConfig.createCurrentVersionPattern();

    return storageKeys.some(
      (key) => currentVersionPattern.test(key) && localStorage.getItem(key) !== null
    );
  }

  /**
   * 检查是否存在任何版本的存储数据
   */
  private hasAnyVersionStorage(): boolean {
    const storageKeys = Object.keys(localStorage);
    const versionPattern = StorageConfig.createVersionPattern();

    return storageKeys.some(
      (key) => versionPattern.test(key) && localStorage.getItem(key) !== null
    );
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
   * 执行系统登出
   */
  private performSystemLogout(): void {
    setTimeout(() => {
      void (async () => {
        try {
          localStorage.clear();
          const [{ router }, { useUserStore }] = await Promise.all([
            import("@/router"),
            import("@stores/modules/user.store"),
          ]);
          useUserStore().logout();
          await router.push({ name: "Login" });
          console.info("[Storage] 已执行系统登出");
        } catch (error) {
          console.error("[Storage] 系统登出失败:", error);
        }
      })();
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
   * 验证存储数据完整性
   * @param requireAuth 是否需要验证登录状态（默认 false）
   */
  validateStorageData(requireAuth: boolean = false): boolean {
    try {
      // 优先检查新版本存储结构
      if (this.hasCurrentVersionStorage()) {
        // console.debug('[Storage] 发现当前版本存储数据')
        return true;
      }

      // 检查是否有任何版本的存储数据
      if (this.hasAnyVersionStorage()) {
        // console.debug('[Storage] 发现其他版本存储数据，可能需要迁移')
        return true;
      }

      // 检查旧版本存储结构
      const legacyData = this.getLegacyStorageData();
      if (Object.keys(legacyData).length === 0) {
        // 只有在需要验证登录状态时才执行登出操作
        if (requireAuth) {
          console.warn("[Storage] 未发现任何存储数据，需要重新登录");
          this.performSystemLogout();
          return false;
        }
        // 首次访问或访问静态路由，不需要登出
        // console.debug('[Storage] 未发现存储数据，首次访问或访问静态路由')
        return true;
      }

      console.debug("[Storage] 发现旧版本存储数据");
      return true;
    } catch (error) {
      console.error("[Storage] 存储数据验证失败:", error);
      // 只有在需要验证登录状态时才处理错误
      if (requireAuth) {
        this.handleStorageError();
        return false;
      }
      return true;
    }
  }

  /**
   * 检查存储是否为空
   */
  isStorageEmpty(): boolean {
    // 检查新版本存储结构
    if (this.hasCurrentVersionStorage()) {
      return false;
    }

    // 检查是否有任何版本的存储数据
    if (this.hasAnyVersionStorage()) {
      return false;
    }

    // 检查旧版本存储结构
    const legacyData = this.getLegacyStorageData();
    return Object.keys(legacyData).length === 0;
  }

  /**
   * 检查存储兼容性
   * @param requireAuth 是否需要验证登录状态（默认 false）
   */
  checkCompatibility(requireAuth: boolean = false): boolean {
    try {
      const isValid = this.validateStorageData(requireAuth);
      const isEmpty = this.isStorageEmpty();

      if (isValid || isEmpty) {
        // console.debug('[Storage] 存储兼容性检查通过')
        return true;
      }

      console.warn("[Storage] 存储兼容性检查失败");
      return false;
    } catch (error) {
      console.error("[Storage] 兼容性检查异常:", error);
      return false;
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
 * 检查存储兼容性
 * @param requireAuth 是否需要验证登录状态（默认 false）
 */
export function checkStorageCompatibility(requireAuth: boolean = false): boolean {
  return storageManager.checkCompatibility(requireAuth);
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

export class Storage {
  /**
   * localStorage 存储数据
   *
   * 将数据序列化为 JSON 字符串后存储到 localStorage
   *
   * @param {string} key - 存储键名
   * @param {any} value - 要存储的数据
   *
   * @example
   * ```typescript
   * Storage.set('user', { name: 'John', age: 25 });
   * ```
   */
  static set(key: string, value: any): void {
    localStorage.setItem(key, JSON.stringify(value));
  }

  /**
   * localStorage 读取数据
   *
   * 从 localStorage 读取数据并反序列化为指定类型
   * 如果解析失败，返回原始字符串
   *
   * @param {string} key - 存储键名
   * @param {T} [defaultValue] - 默认值，当键不存在时返回
   * @returns {T} 解析后的数据或默认值
   *
   * @example
   * ```typescript
   * const user = Storage.get<User>('user', { name: '', age: 0 });
   * ```
   */
  static get<T>(key: string, defaultValue?: T): T {
    const value = localStorage.getItem(key);
    if (!value) return defaultValue as T;

    try {
      return JSON.parse(value);
    } catch {
      // 如果解析失败，返回原始字符串
      return value as unknown as T;
    }
  }

  /**
   * localStorage 删除数据
   *
   * 从 localStorage 中删除指定键的数据
   *
   * @param {string} key - 要删除的键名
   *
   * @example
   * ```typescript
   * Storage.remove('user');
   * ```
   */
  static remove(key: string): void {
    localStorage.removeItem(key);
  }

  /**
   * localStorage 清空所有数据
   *
   * 清除 localStorage 中的所有数据
   *
   * @example
   * ```typescript
   * Storage.clear();
   * ```
   */
  static clear(): void {
    localStorage.clear();
  }

  /**
   * sessionStorage 存储数据
   *
   * 将数据序列化为 JSON 字符串后存储到 sessionStorage
   *
   * @param {string} key - 存储键名
   * @param {any} value - 要存储的数据
   *
   * @example
   * ```typescript
   * Storage.sessionSet('temp', { token: 'abc123' });
   * ```
   */
  static sessionSet(key: string, value: any): void {
    sessionStorage.setItem(key, JSON.stringify(value));
  }

  /**
   * sessionStorage 读取数据
   *
   * 从 sessionStorage 读取数据并反序列化为指定类型
   * 如果解析失败，返回原始字符串
   *
   * @param {string} key - 存储键名
   * @param {T} [defaultValue] - 默认值，当键不存在时返回
   * @returns {T} 解析后的数据或默认值
   *
   * @example
   * ```typescript
   * const temp = Storage.sessionGet<string>('temp', '');
   * ```
   */
  static sessionGet<T>(key: string, defaultValue?: T): T {
    const value = sessionStorage.getItem(key);
    if (!value) return defaultValue as T;

    try {
      return JSON.parse(value);
    } catch {
      // 如果解析失败，返回原始字符串
      return value as unknown as T;
    }
  }

  /**
   * sessionStorage 删除数据
   *
   * 从 sessionStorage 中删除指定键的数据
   *
   * @param {string} key - 要删除的键名
   *
   * @example
   * ```typescript
   * Storage.sessionRemove('temp');
   * ```
   */
  static sessionRemove(key: string): void {
    sessionStorage.removeItem(key);
  }

  /**
   * sessionStorage 清空所有数据
   *
   * 清除 sessionStorage 中的所有数据
   *
   * @example
   * ```typescript
   * Storage.sessionClear();
   * ```
   */
  static sessionClear(): void {
    sessionStorage.clear();
  }
}
