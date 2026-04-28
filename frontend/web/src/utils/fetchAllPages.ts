/**
 * 按分页拉取全量列表（用于 ExportModal 等「全量数据」场景）
 */
export async function fetchAllPages<T>(options: {
  /** 每页条数，默认 1000 */
  pageSize?: number;
  /** 初始查询条件（会拷贝后写入 page_no / page_size） */
  initialQuery: Record<string, unknown>;
  /** 页码字段名，默认 page_no */
  pageNoKey?: string;
  /** 每页条数字段名，默认 page_size */
  pageSizeKey?: string;
  /** 拉取一页，返回 total 与 list */
  fetchPage: (query: Record<string, unknown>) => Promise<{ total: number; list: T[] }>;
}): Promise<T[]> {
  const pageSize = options.pageSize ?? 1000;
  const pageNoKey = options.pageNoKey ?? 'page_no';
  const pageSizeKey = options.pageSizeKey ?? 'page_size';
  const query = { ...options.initialQuery };
  query[pageNoKey] = 1;
  query[pageSizeKey] = pageSize;
  const all: T[] = [];
  while (true) {
    const { total, list } = await options.fetchPage(query);
    all.push(...list);
    if (all.length >= total || list.length === 0) break;
    query[pageNoKey] = (query[pageNoKey] as number) + 1;
  }
  return all;
}
