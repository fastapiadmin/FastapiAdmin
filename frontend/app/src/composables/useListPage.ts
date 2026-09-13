import type { AlovaGenerics, Method } from 'alova'
import { usePagination } from 'alova/client'
import { computed, ref } from 'vue'

export interface ListPageParams {
  page_no: number
  page_size: number
}

export interface ListPageOptions<AG extends AlovaGenerics = AlovaGenerics> {
  fetcher: (params: ListPageParams) => Method<AG>
  pageSize?: number
  onError?: (error: unknown) => void
}

/**
 * 通用列表分页逻辑（基于 alova usePagination 封装）
 * 底层使用 alova 状态管理，统一暴露 list/total/loading/error 三态与翻页动作
 * 说明：fetcher 需返回 alova Method（http 层 get/post 均为 Method 实例），
 *      请求发送与错误处理完全交给 alova hook 管理
 */
export function useListPage<T, AG extends AlovaGenerics = AlovaGenerics>(options: ListPageOptions<AG>) {
  const { fetcher, pageSize = 10, onError } = options

  const pageParams = ref<ListPageParams>({ page_no: 1, page_size: pageSize })

  const {
    data,
    total,
    loading,
    error,
    send,
    refresh,
    reload: reloadPagination,
    onError: onPageError,
  } = usePagination<AG, T[], any[]>(
    (pageNo: number, pageSizeNo: number) => {
      const method = fetcher({ page_no: pageNo, page_size: pageSizeNo })
      // 列表页要求实时数据，禁用 alova GET 默认 5 分钟请求缓存
      method.config.cacheFor = 0
      return method
    },
    {
      initialPage: 1,
      initialPageSize: pageSize,
      // 由页面手动触发（onLoad/搜索/翻页），禁用自动监听与预加载
      immediate: false,
      watchingStates: [],
      preloadNextPage: false,
      preloadPreviousPage: false,
      // 响应已由 http 层 responded 解包为业务结构 { list, total }
      data: res => (res as PageResult<T>).list ?? [],
      total: res => (res as PageResult<T>).total ?? 0,
    },
  )

  onPageError(({ error: e }) => {
    onError?.(e)
  })

  /** 加载当前页数据（翻页用，命中 usePagination 分页缓存时不重复请求） */
  async function loadData() {
    try {
      await send(pageParams.value.page_no, pageParams.value.page_size)
    }
    catch {
      // 错误已由 onPageError → onError 统一处理，避免未捕获 Promise 告警
    }
    finally {
      // 收起下拉刷新指示器（onPullDownRefresh → loadData 场景；非刷新场景调用无害）
      uni.stopPullDownRefresh()
    }
  }

  /** 强制刷新当前页（忽略缓存重新请求，下拉刷新场景） */
  async function refreshData() {
    try {
      await refresh(pageParams.value.page_no)
    }
    catch {}
    finally {
      uni.stopPullDownRefresh()
    }
  }

  /** 从第 1 页重新加载并清除分页缓存（创建/更新/删除后调用，确保看到最新数据） */
  async function reload() {
    pageParams.value.page_no = 1
    try {
      await reloadPagination()
    }
    catch {}
    finally {
      uni.stopPullDownRefresh()
    }
  }

  /** 上一页 */
  async function loadPrev() {
    if (pageParams.value.page_no <= 1)
      return
    pageParams.value.page_no -= 1
    await loadData()
  }

  /** 下一页 */
  async function loadNext() {
    pageParams.value.page_no += 1
    await loadData()
  }

  /** 跳回第一页（搜索/重置时使用） */
  async function toFirst() {
    pageParams.value.page_no = 1
    await loadData()
  }

  return {
    list: computed<T[]>(() => data.value ?? []),
    total: computed<number>(() => total.value ?? 0),
    loading,
    error,
    pageParams,
    loadData,
    refreshData,
    reload,
    loadPrev,
    loadNext,
    toFirst,
  }
}
