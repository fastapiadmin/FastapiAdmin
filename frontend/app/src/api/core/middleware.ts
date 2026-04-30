/**
 * 延迟加载中间件
 * 延迟显示加载状态，防止快速请求导致的闪烁
 * @param delay 显示加载状态前的延迟时间（毫秒）
 * @returns Alova 中间件
 */
export function createDelayLoadingMiddleware(delay = 300) {
  return async (context: any, next: any) => {
    context.controlLoading()

    const { loading } = context.proxyStates

    const timer = setTimeout(() => {
      loading.v = true
    }, delay)

    await next()

    loading.v = false
    clearTimeout(timer)
  }
}

/**
 * 全局加载中间件
 * 为所有请求显示全局加载指示器，支持延迟显示
 *
 * 使用示例：
 * ```typescript
 * // 1. 基本用法
 * const { send: submit } = useRequest(method, {
 *   middleware: createGlobalLoadingMiddleware()
 * });
 *
 * // 2. 自定义延迟时间和加载文本
 * const { send: submit } = useRequest(method, {
 *   middleware: createGlobalLoadingMiddleware({
 *     delay: 500,           // 延迟 500ms 显示加载指示器，防止闪烁
 *     loadingText: '正在提交...', // 自定义加载文本
 *   })
 * });
 * ```
 *
 * @param options 加载选项
 * @param options.delay 显示加载指示器前的延迟时间（毫秒），默认 300ms
 * @param options.loadingText 加载指示器显示的文本，默认为 'Loading...'
 * @returns Alova 中间件
 */
export function createGlobalLoadingMiddleware(options: {
  delay?: number
  loadingText?: string
} = {}) {
  const {
    delay = 0,
    loadingText = 'Loading...',
  } = options

  return async (ctx: any, next: any) => {
    // 自行控制loading
    ctx.controlLoading()

    const globalLoading = useGlobalLoading()
    let timer: ReturnType<typeof setTimeout> | null = null

    // 如果delay为0或未设置，直接显示loading
    if (delay <= 0) {
      globalLoading.loading(loadingText)
    }
    else {
      // 延迟特定时间显示全局loading
      timer = setTimeout(() => {
        globalLoading.loading(loadingText)
      }, delay)
    }

    try {
      await next()
    }
    finally {
      // 清除定时器并关闭loading
      if (timer) {
        clearTimeout(timer)
      }
      globalLoading.close()
    }
  }
}

// 导出延迟加载中间件作为默认中间件
export const defaultMiddleware = createDelayLoadingMiddleware()

export default defaultMiddleware
