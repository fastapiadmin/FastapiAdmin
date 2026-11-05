import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  success: vi.fn(() => ({ close: vi.fn() })),
  error: vi.fn(() => ({ close: vi.fn() })),
}));
vi.mock("element-plus", () => ({
  ElMessage: {
    success: (options: unknown) => mocks.success(options),
    error: (options: unknown) => mocks.error(options),
  },
}));

import { ElMessage } from "element-plus";
import { installMessageDedupe } from "@/utils/message";

describe("message dedupe", () => {
  beforeEach(() => { vi.useFakeTimers(); mocks.success.mockClear(); mocks.error.mockClear(); });
  afterEach(() => vi.useRealTimers());

  it("合并同级别短时间消息并关闭上一条", () => {
    installMessageDedupe();
    ElMessage.success({ message: "a" });
    ElMessage.success({ message: "b" });
    vi.advanceTimersByTime(80);
    expect(mocks.success).toHaveBeenCalledTimes(1);
    expect(mocks.success).toHaveBeenCalledWith(expect.objectContaining({ message: "a；b", grouping: true }));
  });

  it("error 级别同样合并", () => {
    installMessageDedupe();
    ElMessage.error("x");
    ElMessage.error("y");
    vi.advanceTimersByTime(80);
    expect(mocks.error).toHaveBeenCalledWith(expect.objectContaining({ message: "x；y" }));
  });

  it("空文本直接透传原始提示", () => {
    installMessageDedupe();
    ElMessage.success("");
    expect(mocks.success).toHaveBeenCalledWith("");
  });
});
