/**
 * 全局消息去重/合并。
 *
 * 请求层拦截器与页面 catch 都可能弹消息；同一个请求成功/失败时往往会在极短时间内
 * 触发多次 ElMessage.success / ElMessage.error。这里按级别把 80ms 内的消息合并，
 * 并关闭同级别的上一条提示，避免页面叠出多个相同/相关 toast。
 */
import { ElMessage } from "element-plus";

type MessageOptions = Parameters<typeof ElMessage.error>[0];
type MessageHandler = ReturnType<typeof ElMessage.error>;
type Level = "success" | "error";

interface QueueState {
  timer?: ReturnType<typeof setTimeout>;
  active?: MessageHandler;
  pending: Set<string>;
}

const queues: Record<Level, QueueState> = {
  success: { pending: new Set() },
  error: { pending: new Set() },
};

function textOf(options: MessageOptions): string {
  if (typeof options === "string") return options;
  if (options && typeof options === "object" && "message" in options) {
    return String(options.message ?? "");
  }
  return "";
}

function installLevel(level: Level, duration: number): void {
  const raw = (level === "success" ? ElMessage.success : ElMessage.error).bind(ElMessage);
  const state = queues[level];

  const wrapped = (options: MessageOptions) => {
    const text = textOf(options);
    if (!text) return raw(options);

    state.pending.add(text);
    if (state.timer) clearTimeout(state.timer);
    state.timer = setTimeout(() => {
      const message = Array.from(state.pending).join("；");
      state.pending.clear();
      state.timer = undefined;
      state.active?.close();
      state.active = raw({ message, grouping: true, duration });
    }, 80);

    // 调用方通常不使用返回值；返回一个可 close 的占位句柄，避免空引用。
    return { close: () => {} } as MessageHandler;
  };

  if (level === "success") {
    ElMessage.success = wrapped as typeof ElMessage.success;
  } else {
    ElMessage.error = wrapped as typeof ElMessage.error;
  }
}

export function installMessageDedupe(): void {
  installLevel("success", 2800);
  installLevel("error", 3500);
}
