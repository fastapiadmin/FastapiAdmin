/** Table helpers (flattened). */

import { h } from "vue";
import type { VNode } from "vue";
import { ElTooltip } from "element-plus";
import { hash } from "ohash";
import ArtButtonMore from "@/components/Core/forms/art-button-more/index.vue";
import type { ButtonMoreItem } from "@/components/Core/forms/art-button-more/index.vue";
import ArtButtonTable from "@/components/Core/forms/art-button-table/index.vue";

// -----------------------------
// Config
// -----------------------------

export const tableConfig = {
  recordFields: ["list", "data", "records", "items", "result", "rows"],
  totalFields: ["total", "count"],
  currentFields: ["current", "page", "pageNum", "page_no"],
  sizeFields: ["size", "pageSize", "limit", "page_size"],
  paginationKey: {
    current: "current",
    size: "size",
  },
};

// -----------------------------
// Cache
// -----------------------------

export enum CacheInvalidationStrategy {
  CLEAR_ALL = "clear_all",
  CLEAR_CURRENT = "clear_current",
  CLEAR_PAGINATION = "clear_pagination",
  KEEP_ALL = "keep_all",
}

export interface ApiResponse<T = unknown> {
  records?: T[];
  data?: T[];
  total?: number;
  current?: number;
  size?: number;
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
        !["current", "size", "total"].includes(key) &&
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

    tags.add(`pagination:${params.size || 10}`);
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

// -----------------------------
// Utils
// -----------------------------

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

export interface BaseRequestParams extends PageQuery {
  [key: string]: unknown;
}

export interface TableError {
  code: string;
  message: string;
  details?: unknown;
}

function extractRecords<T>(obj: Record<string, unknown>, fields: string[]): T[] {
  for (const field of fields) {
    if (field in obj && Array.isArray(obj[field])) return obj[field] as T[];
  }
  return [];
}

function extractTotal(obj: Record<string, unknown>, records: unknown[], fields: string[]): number {
  for (const field of fields) {
    if (field in obj && typeof obj[field] === "number") return obj[field] as number;
  }
  return records.length;
}

function extractPagination(
  obj: Record<string, unknown>,
  data?: Record<string, unknown>
): Pick<ApiResponse<unknown>, "current" | "size"> | undefined {
  const result: Partial<Pick<ApiResponse<unknown>, "current" | "size">> = {};
  const sources = [obj, data ?? {}];

  for (const src of sources) {
    for (const field of tableConfig.currentFields) {
      if (field in src && typeof src[field] === "number") {
        result.current = src[field] as number;
        break;
      }
    }
    if (result.current !== undefined) break;
  }

  for (const src of sources) {
    for (const field of tableConfig.sizeFields) {
      if (field in src && typeof src[field] === "number") {
        result.size = src[field] as number;
        break;
      }
    }
    if (result.size !== undefined) break;
  }

  if (result.current === undefined && result.size === undefined) return undefined;
  return result;
}

export const defaultResponseAdapter = <T>(response: unknown): ApiResponse<T> => {
  const recordFields = tableConfig.recordFields;

  response = unwrapAxiosResponseBody(response);

  if (!response) return { records: [], total: 0 };
  if (Array.isArray(response)) return { records: response, total: response.length };

  if (typeof response !== "object") {
    console.warn(
      "[tableUtils] 无法识别的响应格式，支持的格式包括: 数组、包含" +
        recordFields.join("/") +
        "字段的对象、嵌套data对象。当前格式:",
      response
    );
    return { records: [], total: 0 };
  }

  const res = response as Record<string, unknown>;
  let records: T[] = [];
  let total = 0;
  let pagination: Pick<ApiResponse<unknown>, "current" | "size"> | undefined;

  records = extractRecords(res, recordFields);
  total = extractTotal(res, records, tableConfig.totalFields);
  pagination = extractPagination(res);

  if (records.length === 0 && "data" in res && typeof res.data === "object") {
    const data = res.data as Record<string, unknown>;
    records = extractRecords(data, ["list", "records", "items"]);
    total = extractTotal(data, records, tableConfig.totalFields);
    pagination = extractPagination(res, data);

    if (Array.isArray(res.data)) {
      records = res.data as T[];
      total = records.length;
    }
  }

  if (!recordFields.some((field) => field in res) && records.length === 0) {
    console.warn("[tableUtils] 无法识别的响应格式");
    console.warn("支持的字段包括: " + recordFields.join("、"), response);
    console.warn("扩展字段请到 utils/table/tableConfig 文件配置");
  }

  const result: ApiResponse<T> = { records, total };
  if (pagination) Object.assign(result, pagination);
  return result;
};

export const extractTableData = <T>(response: ApiResponse<T>): T[] => {
  const data = response.records || response.data || [];
  return Array.isArray(data) ? data : [];
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

// -----------------------------
// Operation cell renderer
// -----------------------------

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
