/**
 * 通用工具函数模块
 *
 * 提供项目中常用的通用工具函数，包括：
 * - 问候语生成
 * - 日期范围处理
 * - 树形结构转换
 * - 对象深拷贝
 * - 空值判断
 * - Blob 格式验证
 *
 * @module utils/common
 */

import { reactive, toRefs } from "vue";
import { tryOnMounted, tryOnUnmounted } from "@vueuse/core";
import dayjs from "dayjs";
import { ElMessage } from "element-plus";

/**
 * 根据当前时间生成问候语
 *
 * 根据当前小时返回不同的问候语，支持中文问候和特殊时段的温馨提示
 *
 * @returns {string} 问候语字符串
 *
 * @example
 * ```typescript
 * const greeting = greetings();
 * console.log(greeting); // 输出："上午好！" 或其他时段的问候语
 * ```
 */
export function greetings(): string {
  const currentDate = new Date();
  const hours = currentDate.getHours();

  if (hours >= 6 && hours < 8) {
    return "晨起披衣出草堂，轩窗已自喜微凉🌅！";
  } else if (hours >= 8 && hours < 12) {
    return "上午好！";
  } else if (hours >= 12 && hours < 14) {
    return "中午好！";
  } else if (hours >= 14 && hours < 18) {
    return "下午好！";
  } else if (hours >= 18 && hours < 24) {
    return "晚上好！";
  } else {
    return "偷偷向银河要了一把碎星，只等你闭上眼睛撒入你的梦中，晚安🌛！";
  }
}

/**
 * 获取日期范围内的所有日期
 *
 * 根据起始日期和结束日期，生成期间所有日期的字符串数组
 * 使用 dayjs 简化日期计算逻辑
 *
 * @param startDate - 起始日期
 * @param endDate - 结束日期
 * @returns 日期字符串数组，格式为 YYYY-MM-DD
 *
 * @example
 * ```typescript
 * const dates = getRangeDate('2024-01-30', '2024-02-02');
 * // 输出：['2024-01-30', '2024-01-31', '2024-02-01', '2024-02-02']
 * ```
 */
export function getRangeDate(
  startDate: string | number | Date,
  endDate: string | number | Date
): string[] {
  const start = dayjs(startDate);
  const end = dayjs(endDate);
  const dates: string[] = [];

  // 验证日期有效性
  if (!start.isValid() || !end.isValid()) {
    return dates;
  }

  // 确保 start <= end
  const [actualStart, actualEnd] = start.isAfter(end) ? [end, start] : [start, end];

  let current = actualStart;
  while (current.isBefore(actualEnd) || current.isSame(actualEnd, "day")) {
    dates.push(current.format("YYYY-MM-DD"));
    current = current.add(1, "day");
  }

  return dates;
}

/**
 * 树形节点基础接口
 * 用于 listToTree 和 formatTree 函数
 */
export interface TreeNode {
  id?: string | number;
  parent_id?: string | number | null;
  name?: string;
  status?: boolean | string | number;
  children?: TreeNode[];
}

/**
 * 级联选择器节点接口
 */
export interface CascaderNode {
  value: string | number;
  label: string;
  disabled: boolean;
  children?: CascaderNode[];
}

/**
 * 将扁平列表转换为树形结构
 *
 * 通过 parent_id 字段将扁平数组转换为嵌套的树形结构
 * 保留原始数据的所有字段
 *
 * @param list - 扁平列表数据，每个项必须包含 id 和 parent_id 字段
 * @returns 树形结构数组
 *
 * @example
 * ```typescript
 * const list = [
 *   { id: 1, name: '节点1', parent_id: null },
 *   { id: 2, name: '节点2', parent_id: 1 },
 * ];
 * const tree = listToTree(list);
 * // 输出：[{ id: 1, name: '节点1', parent_id: null, children: [{ id: 2, name: '节点2', parent_id: 1 }] }]
 * ```
 */
export function listToTree<
  T extends { id?: string | number; parent_id?: string | number | null; children?: T[] },
>(list: T[]): T[] {
  const map = new Map<string | number, T>();
  const tree: T[] = [];

  // 创建映射表（过滤掉 id 为空的项）
  for (const item of list) {
    if (item.id != null) {
      map.set(item.id, { ...item });
    }
  }

  // 构建树形结构
  for (const item of list) {
    if (item.id == null) continue;

    const node = map.get(item.id);
    if (!node) continue;

    const parentId = item.parent_id;

    if (parentId != null && map.has(parentId)) {
      const parent = map.get(parentId)!;
      if (!parent.children) parent.children = [];
      parent.children.push(node);
    } else if (parentId == null) {
      tree.push(node);
    }
  }

  return tree;
}

/**
 * 格式化树形结构为级联选择器格式
 *
 * 将树形数据转换为适合 Element Plus Cascader 组件使用的格式
 * 包含 value、label、disabled 和 children 字段
 *
 * @param nodes - 树形结构数据
 * @returns 格式化后的级联选择器节点数组
 *
 * @example
 * ```typescript
 * const nodes = [{ id: 1, name: '部门1', status: true, children: [...] }];
 * const formatted = formatTree(nodes);
 * // 输出：[{ value: 1, label: '部门1', disabled: false, children: [...] }]
 * ```
 */
export function formatTree(nodes: TreeNode[]): CascaderNode[] {
  return nodes.map((node) => {
    const formatted: CascaderNode = {
      value: node.id ?? "",
      label: node.name ?? "",
      disabled: node.status === false || String(node.status) === "false",
    };

    if (node.children && node.children.length > 0) {
      formatted.children = formatTree(node.children);
    }

    return formatted;
  });
}

/**
 * 检查元素是否包含指定 CSS 类
 */
export function hasClass(ele: HTMLElement, cls: string): boolean {
  return ele.classList.contains(cls);
}

/**
 * 为元素添加 CSS 类
 */
export function addClass(ele: HTMLElement, cls: string): void {
  ele.classList.add(cls);
}

/**
 * 从元素移除 CSS 类
 */
export function removeClass(ele: HTMLElement, cls: string): void {
  ele.classList.remove(cls);
}

export function isExternal(path: string): boolean {
  return /^(https?:|http?:|mailto:|tel:)/.test(path);
}

/**
 * 判断字符串是否为空
 *
 * 检查字符串是否为 undefined、null 或空字符串
 *
 * @param {string | null | undefined} obj - 需要检查的字符串
 * @returns {boolean} 是否为空
 *
 * @example
 * ```typescript
 * isEmpty('');      // true
 * isEmpty(null);    // true
 * isEmpty(undefined); // true
 * isEmpty('hello'); // false
 * ```
 */
export function isEmpty(obj: string | null | undefined): boolean {
  return obj === undefined || obj === null || obj === "";
}

/**
 * 验证数据是否为 Blob 格式
 *
 * 通过检查 Content-Type 是否为 application/json 来判断
 *
 * @param {Blob} data - 需要验证的数据
 * @returns {boolean} 是否为 Blob 格式
 *
 * @example
 * ```typescript
 * const blob = new Blob(['test'], { type: 'text/plain' });
 * blobValidate(blob); // true
 * ```
 */
export function blobValidate(data: Blob): boolean {
  return data.type !== "application/json";
}

/** Date helpers (dayjs). */

const DATE_TIME_FORMAT = "YYYY-MM-DD HH:mm:ss";

const DATE_FORMAT = "YYYY-MM-DD";

export function formatToDateTime(
  date?: dayjs.ConfigType,
  format: string = DATE_TIME_FORMAT
): string {
  return dayjs(date).format(format);
}

export function formatToDate(date?: dayjs.ConfigType, format: string = DATE_FORMAT): string {
  return dayjs(date).format(format);
}

export function formatToTime(time?: dayjs.ConfigType, format: string = "HH:mm:ss"): string {
  return dayjs(time).format(format);
}

export const useNow = (immediate: boolean = true) => {
  let timer: ReturnType<typeof setInterval>;

  const state = reactive({
    year: 0,
    month: 0,
    week: "",
    day: 0,
    hour: "",
    minute: "",
    second: 0,
    meridiem: "",
  });

  const update = () => {
    const now = dayjs();

    const h = now.format("HH");
    const m = now.format("mm");
    const s = now.get("s");

    state.year = now.get("y");
    state.month = now.get("M") + 1;
    state.week = "星期" + ["日", "一", "二", "三", "四", "五", "六"][now.day()];
    state.day = now.get("date");
    state.hour = h;
    state.minute = m;
    state.second = s;
    state.meridiem = now.format("A");
  };

  function start(): void {
    update();
    clearInterval(timer);
    timer = setInterval(() => update(), 1000);
  }

  function stop(): void {
    clearInterval(timer);
  }

  tryOnMounted(() => {
    if (immediate) {
      start();
    }
  });

  tryOnUnmounted(() => {
    stop();
  });

  return {
    ...toRefs(state),
    start,
    stop,
  };
};

/**
 * 分页数据全量获取工具
 *
 * 用于需要获取全量数据的场景，如数据导出、批量操作等
 * 自动处理分页逻辑，将多页数据合并为一个完整的数组
 *
 * @module utils/fetchAllPages
 */

/**
 * fetchAllPages 函数的配置选项类型
 */
export interface FetchAllPagesOptions<T> {
  /** 每页条数，默认 1000 */
  pageSize?: number;
  /** 初始查询条件（会被拷贝后写入 page_no / page_size） */
  initialQuery: Record<string, unknown>;
  /** 页码字段名，默认 'page_no' */
  pageNoKey?: string;
  /** 每页条数字段名，默认 'page_size' */
  pageSizeKey?: string;
  /**
   * 拉取单页数据的函数
   * @param query - 查询参数，包含分页信息
   * @returns Promise<{ total: number; list: T[] }> - 包含总数和当前页数据
   */
  fetchPage: (query: Record<string, unknown>) => Promise<{ total: number; list: T[] }>;
}

/**
 * 按分页拉取全量列表
 *
 * 自动遍历所有分页，将数据合并为一个完整的数组返回
 * 适用于数据导出等需要全量数据的场景
 *
 * @template T - 数据项类型
 * @param {FetchAllPagesOptions<T>} options - 配置选项
 * @returns {Promise<T[]>} 合并后的全量数据数组
 *
 * @example
 * ```typescript
 * import { fetchAllPages } from '@utils/fetchAllPages';
 *
 * // 获取所有用户数据
 * const allUsers = await fetchAllPages<User>({
 *   pageSize: 500,
 *   initialQuery: { status: 'active' },
 *   fetchPage: async (query) => {
 *     const response = await api.get({ url: '/users', params: query });
 *     return {
 *       total: response.data.total,
 *       list: response.data.list,
 *     };
 *   },
 * });
 * ```
 */
export async function fetchAllPages<T>(options: FetchAllPagesOptions<T>): Promise<T[]> {
  const pageSize = options.pageSize ?? 1000;
  const pageNoKey = options.pageNoKey ?? "page_no";
  const pageSizeKey = options.pageSizeKey ?? "page_size";
  const query = { ...options.initialQuery };
  query[pageNoKey] = 1;
  query[pageSizeKey] = pageSize;
  const all: T[] = [];

  while (true) {
    const { total, list } = await options.fetchPage(query);
    all.push(...list);

    // 当已获取的数据达到总数或当前页为空时停止
    if (all.length >= total || list.length === 0) {
      break;
    }

    query[pageNoKey] = (query[pageNoKey] as number) + 1;
  }

  return all;
}

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
 * import { quickStartManager } from '@utils/common/quickStartManager';
 *
 * // 获取所有链接
 * const links = quickStartManager.getQuickLinks();
 *
 * // 添加新链接
 * quickStartManager.addQuickLink({ title: '设置', icon: 'settings', href: '/settings' });
 * ```
 */
export const quickStartManager = new QuickStartManager();
