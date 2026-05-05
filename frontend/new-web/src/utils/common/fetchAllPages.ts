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
 * import { fetchAllPages } from '@/utils/fetchAllPages';
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
