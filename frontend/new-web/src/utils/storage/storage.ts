/**
 * 存储兼容性管理模块
 *
 * 提供完整的本地存储兼容性检查和数据验证功能
 *
 * 主要功能
 *
 * - 多版本存储数据检测和验证
 * - 新旧存储格式兼容处理
 * - 存储数据完整性校验
 * - 存储异常自动恢复（清理+登出）
 * - 登录状态验证
 * - 存储为空检测
 * - 版本号管理
 *
 * ## 使用场景
 *
 * - 应用启动时检查存储数据有效性
 * - 路由守卫中验证登录状态
 * - 版本升级时的数据兼容性检查
 * - 存储异常时的自动恢复
 * - 防止因存储数据损坏导致的系统异常
 *
 * ## 工作流程
 *
 * 1. 优先检查当前版本的存储数据
 * 2. 检查其他版本的存储数据
 * 3. 兼容旧格式的存储数据
 * 4. 验证数据完整性
 * 5. 异常时提示用户并执行登出
 *
 * @module utils/storage/storage
 * @author FastapiAdmin Team
 */
import { router } from "@/router";
import { useUserStore } from "@/store/modules/user.store";
import { StorageConfig } from "@/utils/storage/storage-config";

/**
 * 存储兼容性管理器
 * 负责处理不同版本间的存储兼容性检查和数据验证
 */
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
      try {
        localStorage.clear();
        useUserStore().logout();
        router.push({ name: "Login" });
        console.info("[Storage] 已执行系统登出");
      } catch (error) {
        console.error("[Storage] 系统登出失败:", error);
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
