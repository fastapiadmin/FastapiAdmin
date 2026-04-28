import { ElMessage } from 'element-plus';

/** 收藏数量上限（工作台「我的收藏」为 3 列 × 最多 5 排，共 15 个） */
export const QUICK_LINK_MAX = 15;

// 快速链接数据类型
export interface QuickLink {
  title: string;
  icon: string;
  href: string;
  id?: string;
}

// 快速开始管理器类
class QuickStartManager {
  private storageKey = 'quick-start-links';
  private listeners: Array<(links: QuickLink[]) => void> = [];

  // 获取所有快速链接
  getQuickLinks(): QuickLink[] {
    try {
      const stored = localStorage.getItem(this.storageKey);
      return stored ? JSON.parse(stored) : this.getDefaultLinks();
    } catch (error) {
      console.error('Failed to load quick links:', error);
      return this.getDefaultLinks();
    }
  }

  // 获取默认链接
  private getDefaultLinks(): QuickLink[] {
    return [];
  }

  // 保存快速链接
  saveQuickLinks(links: QuickLink[]): void {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(links));
      this.notifyListeners(links);
    } catch (error) {
      console.error('Failed to save quick links:', error);
    }
  }

  /**
   * 添加或更新快速链接。
   * @returns 是否已保存；新增时若已达上限则提示并返回 false
   */
  addQuickLink(link: QuickLink): boolean {
    const links = this.getQuickLinks();

    const existingIndex = links.findIndex((l) => l.href === link.href);
    if (existingIndex !== -1) {
      links[existingIndex] = { ...links[existingIndex], ...link };
      ElMessage.success(`已更新快速链接：${link.title}`);
      this.saveQuickLinks(links);
      return true;
    }

    if (links.length >= QUICK_LINK_MAX) {
      ElMessage.warning(`收藏已满（最多 ${QUICK_LINK_MAX} 个），请先移除后再添加`);
      return false;
    }

    links.push(link);
    this.saveQuickLinks(links);
    return true;
  }

  // 删除快速链接
  removeQuickLink(id: string): void {
    const links = this.getQuickLinks();
    const filteredLinks = links.filter((link) => link.id !== id);

    if (filteredLinks.length < links.length) {
      this.saveQuickLinks(filteredLinks);
    }
  }

  /** 无 id 的旧数据可按路由路径移除 */
  removeQuickLinkByHref(href: string): void {
    const links = this.getQuickLinks();
    const filteredLinks = links.filter((link) => link.href !== href);
    if (filteredLinks.length < links.length) {
      this.saveQuickLinks(filteredLinks);
    }
  }

  // 清空所有快速链接
  clearQuickLinks(): void {
    this.saveQuickLinks([]);
  }
  // 从路由或菜单信息创建快速链接
  createQuickLinkFromRoute(route: any, customTitle?: string): QuickLink {
    // 确定最终使用的标题 - 优先使用route.title
    const finalTitle = customTitle || route.title || route.name || '未命名页面';

    return {
      title: finalTitle,
      icon: route.icon,
      href: route.fullPath || route.path,
      id: `route-${route.path.replace(/\//g, '-')}-${Date.now()}`,
    };
  }

  // 添加监听器
  addListener(callback: (links: QuickLink[]) => void): void {
    this.listeners.push(callback);
  }

  // 移除监听器
  removeListener(callback: (links: QuickLink[]) => void): void {
    const index = this.listeners.indexOf(callback);
    if (index > -1) {
      this.listeners.splice(index, 1);
    }
  }

  // 通知所有监听器
  private notifyListeners(links: QuickLink[]): void {
    this.listeners.forEach((callback) => {
      try {
        callback(links);
      } catch (error) {
        console.error('Error in quick start listener:', error);
      }
    });
  }

  // 检查链接是否已存在
  isLinkExists(href: string): boolean {
    const links = this.getQuickLinks();
    return links.some((link) => link.href === href);
  }
}

// 创建全局实例
export const quickStartManager = new QuickStartManager();
