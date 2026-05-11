/**
 * 表格列表工具：`useTable`、缓存与分页响应适配。
 *
 * - 接口约定：分页列表返回体须符合全局 `PageResult`（或包在标准 `data` 内），见 `defaultResponseAdapter`。
 * - 缓存：`TableCache` 按参数 hash + 标签失效；策略枚举供 `useTable.clearCache` 使用。
 */

import { h } from "vue";
import type { VNode } from "vue";
import { ElTooltip } from "element-plus";
import { hash } from "ohash";
import ArtButtonMore from "@/components/forms/fa-button-more/index.vue";
import type { ButtonMoreItem } from "@/components/forms/fa-button-more/index.vue";
import ArtButtonTable from "@/components/forms/fa-button-table/index.vue";

// --- 全局分页字段名（与 PageQuery 对齐） ---

/** 仅保留与全局 `PageQuery` / `PageResult` 对齐的分页参数字段名（供 useTable 合并请求参数） */
export const tableConfig = {
  paginationKey: {
    current: "page_no",
    size: "page_size",
  },
} as const;

/** 与 `global.d.ts` 中 `PageResult` 字段一致；分页列表接口必须返回该结构（或包在 ApiResponse.data 内） */
function isPageResultPayload(o: unknown): o is PageResult<unknown> {
  if (!o || typeof o !== "object" || Array.isArray(o)) return false;
  const r = o as Record<string, unknown>;
  return (
    Array.isArray(r.items) &&
    typeof r.total === "number" &&
    typeof r.page_no === "number" &&
    typeof r.page_size === "number" &&
    typeof r.has_next === "boolean"
  );
}

/** 将常见分页形状（含 MyBatis-Plus / 旧字段名）规范为全局 `PageResult` */
function normalizePageResultLike(raw: unknown): PageResult<unknown> | null {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null;
  const o = raw as Record<string, unknown>;

  const items =
    (Array.isArray(o.items) && o.items) ||
    (Array.isArray(o.records) && o.records) ||
    (Array.isArray(o.list) && o.list) ||
    (Array.isArray(o.rows) && o.rows) ||
    null;
  if (!items) return null;

  const totalRaw = o.total;
  const total =
    typeof totalRaw === "number" ? totalRaw : typeof totalRaw === "string" ? Number(totalRaw) : NaN;
  if (!Number.isFinite(total)) return null;

  const pageNoRaw = o.page_no ?? o.current ?? o.page;
  const page_no =
    typeof pageNoRaw === "number"
      ? pageNoRaw
      : typeof pageNoRaw === "string"
        ? Number(pageNoRaw)
        : NaN;
  if (!Number.isFinite(page_no)) return null;

  const pageSizeRaw = o.page_size ?? o.size ?? o.limit ?? o.pageSize;
  const page_size =
    typeof pageSizeRaw === "number"
      ? pageSizeRaw
      : typeof pageSizeRaw === "string"
        ? Number(pageSizeRaw)
        : NaN;
  if (!Number.isFinite(page_size)) return null;

  let has_next: boolean;
  if (typeof o.has_next === "boolean") {
    has_next = o.has_next;
  } else if (typeof o.hasNext === "boolean") {
    has_next = o.hasNext;
  } else {
    has_next = page_no * page_size < total;
  }

  return { items, total, page_no, page_size, has_next };
}

// --- 缓存 ---

export enum CacheInvalidationStrategy {
  CLEAR_ALL = "clear_all",
  CLEAR_CURRENT = "clear_current",
  CLEAR_PAGINATION = "clear_pagination",
  KEEP_ALL = "keep_all",
}

/** useTable 内部使用的规范化分页响应（由 PageResult 映射而来） */
export interface ApiResponse<T = unknown> {
  records: T[];
  total: number;
  current?: number;
  size?: number;
  has_next?: boolean;
  [key: string]: unknown;
}

export interface CacheItem<T> {
  data: T[];
  response: ApiResponse<T>;
  timestamp: number;
  params: string;
  tags: Set<string>;
  accessCount: number;
  lastAccessTime: number;
}

export class TableCache<T> {
  private cache = new Map<string, CacheItem<T>>();
  private cacheTime: number;
  private maxSize: number;
  private enableLog: boolean;

  constructor(cacheTime = 5 * 60 * 1000, maxSize = 50, enableLog = false) {
    this.cacheTime = cacheTime;
    this.maxSize = maxSize;
    this.enableLog = enableLog;
  }

  private log(message: string, ...args: any[]) {
    if (this.enableLog) console.log(`[TableCache] ${message}`, ...args);
  }

  private generateKey(params: unknown): string {
    return hash(params);
  }

  private generateTags(params: Record<string, unknown>): Set<string> {
    const tags = new Set<string>();

    const searchKeys = Object.keys(params).filter(
      (key) =>
        !["current", "size", "total", "page_no", "page_size"].includes(key) &&
        params[key] !== undefined &&
        params[key] !== "" &&
        params[key] !== null
    );

    if (searchKeys.length > 0) {
      const searchTag = searchKeys.map((key) => `${key}:${String(params[key])}`).join("|");
      tags.add(`search:${searchTag}`);
    } else {
      tags.add("search:default");
    }

    const ps = params as Record<string, unknown>;
    const pageSizeVal = ps.page_size ?? ps.size;
    tags.add(`pagination:${typeof pageSizeVal === "number" ? pageSizeVal : 10}`);
    tags.add("pagination");
    return tags;
  }

  private evictLRU(): void {
    if (this.cache.size <= this.maxSize) return;

    let lruKey = "";
    let minAccessCount = Infinity;
    let oldestTime = Infinity;

    for (const [key, item] of this.cache.entries()) {
      if (
        item.accessCount < minAccessCount ||
        (item.accessCount === minAccessCount && item.lastAccessTime < oldestTime)
      ) {
        lruKey = key;
        minAccessCount = item.accessCount;
        oldestTime = item.lastAccessTime;
      }
    }

    if (lruKey) {
      this.cache.delete(lruKey);
      this.log(`LRU 清理缓存: ${lruKey}`);
    }
  }

  set(params: unknown, data: T[], response: ApiResponse<T>): void {
    const key = this.generateKey(params);
    const tags = this.generateTags(params as Record<string, unknown>);
    const now = Date.now();

    this.evictLRU();

    this.cache.set(key, {
      data,
      response,
      timestamp: now,
      params: key,
      tags,
      accessCount: 1,
      lastAccessTime: now,
    });
  }

  get(params: unknown): CacheItem<T> | null {
    const key = this.generateKey(params);
    const item = this.cache.get(key);
    if (!item) return null;

    if (Date.now() - item.timestamp > this.cacheTime) {
      this.cache.delete(key);
      return null;
    }

    item.accessCount++;
    item.lastAccessTime = Date.now();
    return item;
  }

  clearByTags(tags: string[]): number {
    let clearedCount = 0;

    for (const [key, item] of this.cache.entries()) {
      const hasMatchingTag = tags.some((tag) =>
        Array.from(item.tags).some((itemTag) => itemTag.includes(tag))
      );

      if (hasMatchingTag) {
        this.cache.delete(key);
        clearedCount++;
      }
    }

    return clearedCount;
  }

  clearCurrentSearch(params: unknown): number {
    const key = this.generateKey(params);
    const deleted = this.cache.delete(key);
    return deleted ? 1 : 0;
  }

  clearPagination(): number {
    return this.clearByTags(["pagination"]);
  }

  clear(): void {
    this.cache.clear();
  }

  getStats(): { total: number; size: string; hitRate: string } {
    const total = this.cache.size;
    let totalSize = 0;
    let totalAccess = 0;

    for (const item of this.cache.values()) {
      totalSize += JSON.stringify(item.data).length;
      totalAccess += item.accessCount;
    }

    const sizeInKB = (totalSize / 1024).toFixed(2);
    const avgHits = total > 0 ? (totalAccess / total).toFixed(1) : "0";

    return { total, size: `${sizeInKB}KB`, hitRate: `${avgHits} avg hits` };
  }

  cleanupExpired(): number {
    let cleanedCount = 0;
    const now = Date.now();

    for (const [key, item] of this.cache.entries()) {
      if (now - item.timestamp > this.cacheTime) {
        this.cache.delete(key);
        cleanedCount++;
      }
    }

    return cleanedCount;
  }
}

// --- 响应解析与防抖 ---

function unwrapAxiosResponseBody(response: unknown): unknown {
  if (response === null || typeof response !== "object") return response;
  const r = response as Record<string, unknown>;

  if (
    "data" in r &&
    "status" in r &&
    typeof r.status === "number" &&
    "config" in r &&
    typeof r.config === "object"
  ) {
    return r.data;
  }

  return response;
}

/**
 * 从 axios 原始响应或已解包 body 中取出唯一合法的 `PageResult`。
 * 支持：① 严格 `PageResult`；② `ApiResponse.data` 嵌套；③ `records/current/size` 等常见变体。
 */
function extractPageResultPayload(response: unknown): PageResult<unknown> | null {
  const candidates: unknown[] = [];

  const push = (x: unknown) => {
    if (x !== undefined && x !== null) candidates.push(x);
  };

  push(response);
  push(unwrapAxiosResponseBody(response));

  for (let i = 0; i < candidates.length; i++) {
    const x = candidates[i];
    if (isPageResultPayload(x)) {
      return x;
    }
    const normalized = normalizePageResultLike(x);
    if (normalized) {
      return normalized;
    }
    if (x && typeof x === "object" && !Array.isArray(x) && "data" in x) {
      const inner = (x as Record<string, unknown>).data;
      push(inner);
      if (inner && typeof inner === "object" && !Array.isArray(inner) && "data" in inner) {
        push((inner as Record<string, unknown>).data);
      }
    }
  }

  return null;
}

export interface BaseRequestParams extends PageQuery {
  [key: string]: unknown;
}

export interface TableError {
  code: string;
  message: string;
  details?: unknown;
}

export const defaultResponseAdapter = <T>(response: unknown): ApiResponse<T> => {
  const pr = extractPageResultPayload(response);
  if (!pr) {
    console.error(
      "[tableUtils] 分页列表响应必须符合全局 PageResult<T>（items、total、page_no、page_size、has_next）；或为 ApiResponse 且 data 为该结构。收到:",
      response
    );
    return { records: [], total: 0, current: 1, size: 10 };
  }

  return {
    records: pr.items as T[],
    total: pr.total,
    current: pr.page_no,
    size: pr.page_size,
    has_next: pr.has_next,
  };
};

export const extractTableData = <T>(response: ApiResponse<T>): T[] => {
  const rows = response.records;
  return Array.isArray(rows) ? rows : [];
};

export const updatePaginationFromResponse = <T>(
  pagination: { total: number },
  response: ApiResponse<T>
): void => {
  const total = response.total;
  if (typeof total === "number") (pagination as Record<string, unknown>).total = total;
};

export const createSmartDebounce = <T extends (...args: any[]) => Promise<any>>(
  fn: T,
  delay: number
): T & { cancel: () => void; flush: () => Promise<any> } => {
  let timeoutId: NodeJS.Timeout | null = null;
  let lastArgs: Parameters<T> | null = null;
  let lastResolve: ((value: any) => void) | null = null;
  let lastReject: ((reason: any) => void) | null = null;

  const debouncedFn = (...args: Parameters<T>): Promise<any> => {
    return new Promise((resolve, reject) => {
      if (timeoutId) clearTimeout(timeoutId);
      lastArgs = args;
      lastResolve = resolve;
      lastReject = reject;
      timeoutId = setTimeout(async () => {
        try {
          const result = await fn(...args);
          resolve(result);
        } catch (error) {
          reject(error);
        } finally {
          timeoutId = null;
          lastArgs = null;
          lastResolve = null;
          lastReject = null;
        }
      }, delay);
    });
  };

  debouncedFn.cancel = () => {
    if (timeoutId) clearTimeout(timeoutId);
    timeoutId = null;
    lastArgs = null;
    lastResolve = null;
    lastReject = null;
  };

  debouncedFn.flush = async () => {
    if (timeoutId && lastArgs && lastResolve && lastReject) {
      clearTimeout(timeoutId);
      timeoutId = null;
      const args = lastArgs;
      const resolve = lastResolve;
      const reject = lastReject;
      lastArgs = null;
      lastResolve = null;
      lastReject = null;

      try {
        const result = await fn(...args);
        resolve(result);
        return result;
      } catch (error) {
        reject(error);
        throw error;
      }
    }
  };

  return debouncedFn as T & { cancel: () => void; flush: () => Promise<any> };
};

export const createErrorHandler = (
  onError?: (error: TableError) => void,
  enableLog: boolean = false
) => {
  return (error: any, defaultMessage: string = "操作失败"): TableError => {
    const tableError: TableError = {
      code: error?.code || "UNKNOWN_ERROR",
      message: error?.message || defaultMessage,
      details: error,
    };

    if (enableLog) {
      console.error("[tableUtils]", tableError);
    }

    onError?.(tableError);
    return tableError;
  };
};

// --- 操作列渲染（表格单元格内按钮 + 溢出「更多」） ---

export const DEFAULT_MAX_INLINE_TABLE_OPERATIONS = 3;

export interface TableOperationAction {
  key: string | number;
  label: string;
  artType: "add" | "edit" | "delete" | "view" | "more";
  icon?: string;
  perm?: string;
  disabled?: boolean;
  iconColor?: string;
  color?: string;
  run: () => void;
}

export interface RenderTableOperationCellOptions {
  maxInline?: number;
  wrapperClass?: string;
  emptyText?: string;
}

const ART_TYPE_DEFAULT_ICONS: Record<TableOperationAction["artType"], string> = {
  add: "ri:add-fill",
  edit: "ri:pencil-line",
  delete: "ri:delete-bin-5-line",
  view: "ri:eye-line",
  more: "ri:more-2-fill",
};

function iconForOperation(a: TableOperationAction): string {
  return a.icon ?? ART_TYPE_DEFAULT_ICONS[a.artType];
}

const ART_TYPE_ICON_COLORS: Record<TableOperationAction["artType"], string> = {
  add: "var(--el-color-primary)",
  edit: "var(--el-color-success)",
  delete: "var(--el-color-danger)",
  view: "var(--el-color-info)",
  more: "var(--el-text-color-regular)",
};

function iconColorForOperation(a: TableOperationAction): string | undefined {
  if (a.iconColor != null) return a.iconColor;
  return ART_TYPE_ICON_COLORS[a.artType];
}

function defaultMoreItemColor(a: TableOperationAction): string | undefined {
  if (a.color != null) return a.color;
  return String(a.key) === "delete" ? "var(--el-color-danger)" : undefined;
}

export function renderTableOperationCell(
  actions: TableOperationAction[],
  options?: RenderTableOperationCellOptions
): VNode {
  const maxInline = options?.maxInline ?? DEFAULT_MAX_INLINE_TABLE_OPERATIONS;
  const wrapperClass =
    options?.wrapperClass ?? "inline-flex flex-wrap items-center justify-end gap-1";
  const emptyText = options?.emptyText ?? "—";

  if (actions.length === 0) return h("span", { class: "text-g-400" }, emptyText);

  const inline = actions.slice(0, maxInline);
  const overflow = actions.slice(maxInline);

  const inlineNodes = inline.map((a) =>
    h(ElTooltip, { content: a.label, placement: "top" }, () =>
      h(
        "span",
        { class: a.disabled ? "inline-flex opacity-40 pointer-events-none" : "inline-flex" },
        [
          h(ArtButtonTable, {
            type: a.artType,
            icon: iconForOperation(a),
            iconColor: iconColorForOperation(a),
            onClick: a.run,
          }),
        ]
      )
    )
  );

  if (overflow.length === 0) return h("div", { class: wrapperClass }, inlineNodes);

  const moreDropdown = h(ArtButtonMore, {
    list: overflow.map((a) => ({
      key: a.key,
      label: a.label,
      icon: iconForOperation(a),
      auth: a.perm,
      disabled: a.disabled,
      iconColor: iconColorForOperation(a),
      color: defaultMoreItemColor(a),
    })),
    onClick: (item: ButtonMoreItem) => {
      const act = overflow.find((x) => String(x.key) === String(item.key));
      act?.run();
    },
  });

  return h("div", { class: wrapperClass }, [...inlineNodes, moreDropdown]);
}
