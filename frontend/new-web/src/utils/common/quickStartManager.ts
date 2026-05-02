/**
 * 快速开始链接管理器
 *
 * 管理工作台「我的收藏」功能，支持添加、删除、更新和监听快速链接
 *
 * ## 功能特性
 *
 * - 支持收藏数量上限（默认 15 个）
 * - 自动持久化到 localStorage
 * - 支持观察者模式，数据变化时通知监听者
 * - 支持从路由信息自动创建链接
 *
 * @module utils/quickStartManager
 */

import { ElMessage } from "element-plus";

/** 收藏数量上限（工作台「我的收藏」为 3 列 × 最多 5 排，共 15 个） */
export const QUICK_LINK_MAX = 15;

/**
 * 快速链接数据类型
 */
export interface QuickLink {
  /** 链接标题 */
  title: string;
  /** 图标名称 */
  icon: string;
  /** 跳转路径 */
  href: string;
  /** 唯一标识（可选） */
  id?: string;
}

/**
 * 快速开始管理器类
 *
 * 提供快速链接的增删改查功能，并支持观察者模式
 */
class QuickStartManager {
  /** 本地存储键名 */
  private storageKey = "quick-start-links";

  /** 监听器列表 */
  private listeners: Array<(links: QuickLink[]) => void> = [];

  /**
   * 获取所有快速链接
   *
   * @returns {QuickLink[]} 快速链接数组
   *
   * @example
   * ```typescript
   * const links = quickStartManager.getQuickLinks();
   * console.log(links);
   * ```
   */
  getQuickLinks(): QuickLink[] {
    try {
      const stored = localStorage.getItem(this.storageKey);
      return stored ? JSON.parse(stored) : this.getDefaultLinks();
    } catch (error) {
      console.error("Failed to load quick links:", error);
      return this.getDefaultLinks();
    }
  }

  /**
   * 获取默认链接（空数组）
   *
   * @returns {QuickLink[]} 默认链接数组
   */
  private getDefaultLinks(): QuickLink[] {
    return [];
  }

  /**
   * 保存快速链接到本地存储
   *
   * @param {QuickLink[]} links - 要保存的快速链接数组
   */
  saveQuickLinks(links: QuickLink[]): void {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(links));
      this.notifyListeners(links);
    } catch (error) {
      console.error("Failed to save quick links:", error);
    }
  }

  /**
   * 添加或更新快速链接
   *
   * 如果链接已存在（通过 href 判断），则更新该链接；否则添加新链接
   * 如果收藏数量已达上限，则提示并返回 false
   *
   * @param {QuickLink} link - 要添加或更新的快速链接
   * @returns {boolean} 是否已保存成功
   *
   * @example
   * ```typescript
   * const success = quickStartManager.addQuickLink({
   *   title: '仪表盘',
   *   icon: 'dashboard',
   *   href: '/dashboard',
   * });
   * ```
   */
  addQuickLink(link: QuickLink): boolean {
    const links = this.getQuickLinks();

    // 检查是否已存在相同 href 的链接
    const existingIndex = links.findIndex((l) => l.href === link.href);
    if (existingIndex !== -1) {
      // 更新现有链接
      links[existingIndex] = { ...links[existingIndex], ...link };
      ElMessage.success(`已更新快速链接：${link.title}`);
      this.saveQuickLinks(links);
      return true;
    }

    // 检查是否达到收藏上限
    if (links.length >= QUICK_LINK_MAX) {
      ElMessage.warning(`收藏已满（最多 ${QUICK_LINK_MAX} 个），请先移除后再添加`);
      return false;
    }

    // 添加新链接
    links.push(link);
    this.saveQuickLinks(links);
    return true;
  }

  /**
   * 根据 id 删除快速链接
   *
   * @param {string} id - 要删除的链接 id
   *
   * @example
   * ```typescript
   * quickStartManager.removeQuickLink('link-123');
   * ```
   */
  removeQuickLink(id: string): void {
    const links = this.getQuickLinks();
    const filteredLinks = links.filter((link) => link.id !== id);

    if (filteredLinks.length < links.length) {
      this.saveQuickLinks(filteredLinks);
    }
  }

  /**
   * 根据路由路径删除快速链接
   *
   * 用于兼容没有 id 的旧数据
   *
   * @param {string} href - 要删除的链接路径
   *
   * @example
   * ```typescript
   * quickStartManager.removeQuickLinkByHref('/dashboard');
   * ```
   */
  removeQuickLinkByHref(href: string): void {
    const links = this.getQuickLinks();
    const filteredLinks = links.filter((link) => link.href !== href);
    if (filteredLinks.length < links.length) {
      this.saveQuickLinks(filteredLinks);
    }
  }

  /**
   * 清空所有快速链接
   *
   * @example
   * ```typescript
   * quickStartManager.clearQuickLinks();
   * ```
   */
  clearQuickLinks(): void {
    this.saveQuickLinks([]);
  }

  /**
   * 从路由或菜单信息创建快速链接
   *
   * @param {any} route - 路由或菜单对象
   * @param {string} [customTitle] - 自定义标题（可选）
   * @returns {QuickLink} 创建的快速链接对象
   *
   * @example
   * ```typescript
   * const link = quickStartManager.createQuickLinkFromRoute(route);
   * quickStartManager.addQuickLink(link);
   * ```
   */
  createQuickLinkFromRoute(route: any, customTitle?: string): QuickLink {
    // 确定最终使用的标题 - 优先使用 customTitle
    const finalTitle = customTitle || route.title || route.name || "未命名页面";

    return {
      title: finalTitle,
      icon: route.icon,
      href: route.fullPath || route.path,
      id: `route-${route.path.replace(/\//g, "-")}-${Date.now()}`,
    };
  }

  /**
   * 添加数据变化监听器
   *
   * @param {(links: QuickLink[]) => void} callback - 回调函数，当数据变化时触发
   *
   * @example
   * ```typescript
   * const callback = (links) => {
   *   console.log('链接列表已更新:', links);
   * };
   * quickStartManager.addListener(callback);
   * ```
   */
  addListener(callback: (links: QuickLink[]) => void): void {
    this.listeners.push(callback);
  }

  /**
   * 移除数据变化监听器
   *
   * @param {(links: QuickLink[]) => void} callback - 要移除的回调函数
   *
   * @example
   * ```typescript
   * quickStartManager.removeListener(callback);
   * ```
   */
  removeListener(callback: (links: QuickLink[]) => void): void {
    const index = this.listeners.indexOf(callback);
    if (index > -1) {
      this.listeners.splice(index, 1);
    }
  }

  /**
   * 通知所有监听器数据已变化
   *
   * @param {QuickLink[]} links - 当前的快速链接数组
   */
  private notifyListeners(links: QuickLink[]): void {
    this.listeners.forEach((callback) => {
      try {
        callback(links);
      } catch (error) {
        console.error("Error in quick start listener:", error);
      }
    });
  }

  /**
   * 检查链接是否已存在
   *
   * @param {string} href - 要检查的链接路径
   * @returns {boolean} 是否存在
   *
   * @example
   * ```typescript
   * const exists = quickStartManager.isLinkExists('/dashboard');
   * ```
   */
  isLinkExists(href: string): boolean {
    const links = this.getQuickLinks();
    return links.some((link) => link.href === href);
  }
}

/**
 * 快速开始管理器全局实例
 *
 * @example
 * ```typescript
 * import { quickStartManager } from '@/utils/common/quickStartManager';
 *
 * // 获取所有链接
 * const links = quickStartManager.getQuickLinks();
 *
 * // 添加新链接
 * quickStartManager.addQuickLink({ title: '设置', icon: 'settings', href: '/settings' });
 * ```
 */
export const quickStartManager = new QuickStartManager();
