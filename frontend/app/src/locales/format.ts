/**
 * 小程序端 vue-i18n 运行时无法编译带参数的文案，`t(key, params)` 会原样返回 `{count}`。
 * 这里在 t 的结果上再做一次占位符替换：H5 已插值则无变化，MP 则补上参数。
 */
export function formatMessage(
  t: (key: string, params?: Record<string, unknown>) => unknown,
  key: string,
  params: Record<string, string | number> = {},
): string {
  const text = String(t(key, params))
  return text.replace(/\{(\w+)\}/g, (raw, name: string) => {
    const value = params[name]
    return value == null ? raw : String(value)
  })
}
