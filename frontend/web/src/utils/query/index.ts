/**
 * 清理查询参数中的空数组字段，避免将 [] 传给后端
 *
 * @example
 * ```ts
 * const query = cleanEmptyArrayParams(searchParams, ["created_time", "updated_time"]);
 * // { created_time: [], ... } → { created_time: undefined, ... }
 * ```
 */
export function cleanEmptyArrayParams<T extends Record<string, unknown>>(
  params: T,
  arrayKeys: string[] = ["created_time", "updated_time"]
): T {
  const p = { ...params } as Record<string, unknown>;
  for (const key of arrayKeys) {
    if (Array.isArray(p[key]) && (p[key] as unknown[]).length === 0) {
      p[key] = undefined;
    }
  }
  return p as T;
}

/**
 * 从搜索参数中移除分页字段，生成导出查询参数
 */
export function stripPaginationParams<T extends Record<string, unknown>>(
  params: T,
  pagKeys: string[] = ["current", "size", "page_no", "page_size"]
): Record<string, unknown> {
  const p = { ...(params as object) } as Record<string, unknown>;
  for (const key of pagKeys) {
    delete p[key];
  }
  return p;
}
