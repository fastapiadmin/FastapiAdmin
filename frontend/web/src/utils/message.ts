/**
 * 全局消息去重/合并。
 *
 * 请求层拦截器与页面 catch 都可能弹错误消息；同一个请求失败时往往会在极短时间内
 * 触发多次 ElMessage.error。这里在全局入口把 80ms 内的错误合并成一条，并关闭上一条
 * 错误提示，避免页面叠出多个相同/相关 toast。
 */
import { ElMessage } from "element-plus";

type ErrorOptions = Parameters<typeof ElMessage.error>[0];
type MessageHandler = ReturnType<typeof ElMessage.error>;

let timer: ReturnType<typeof setTimeout> | undefined;
let activeError: MessageHandler | undefined;
const pending = new Set<string>();

function textOf(options: ErrorOptions): string {
  if (typeof options === "string") return options;
  if (options && typeof options === "object" && "message" in options) {
    return String(options.message ?? "");
  }
  return "";
}

export function installMessageDedupe(): void {
  const rawError = ElMessage.error.bind(ElMessage);

  ElMessage.error = ((options: ErrorOptions) => {
    const text = textOf(options);
    if (!text) return rawError(options);

    pending.add(text);
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      const message = Array.from(pending).join("；");
      pending.clear();
      timer = undefined;
      activeError?.close();
      activeError = rawError({ message, grouping: true, duration: 3500 });
    }, 80);

    // 调用方通常不使用返回值；返回一个可 close 的占位句柄，避免空引用。
    return { close: () => {} } as MessageHandler;
  }) as typeof ElMessage.error;
}
