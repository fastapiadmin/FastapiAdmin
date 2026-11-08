import { describe, expect, it, vi } from "vitest";
vi.mock("@utils", () => ({ Auth: { getAccessToken: () => "" }, StorageConfig: { appName: "app", CURRENT_VERSION: "1.0" } }));
vi.mock("@stores", () => ({ useUserStore: () => ({}) }));
import { scriptErrorHandler, vueErrorHandler } from "@/utils/sys";

describe("sys error handler", () => {
  it("忽略 ResizeObserver 噪声", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    expect(scriptErrorHandler("ResizeObserver loop limit exceeded")).toBe(true);
    expect(spy).not.toHaveBeenCalled();
    spy.mockRestore();
  });
  it("忽略跨域 Script error", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    expect(scriptErrorHandler("Script error.", "")).toBe(true);
    expect(spy).not.toHaveBeenCalled();
    spy.mockRestore();
  });
  it("普通字符串记录错误", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    expect(scriptErrorHandler("boom", "a.js")).toBe(true);
    expect(spy).toHaveBeenCalled();
    spy.mockRestore();
  });
  it("Event 的 message 被读取", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    expect(scriptErrorHandler({ message: "ResizeObserver loop completed with undelivered notifications." } as any)).toBe(true);
    expect(spy).not.toHaveBeenCalled();
    spy.mockRestore();
  });
  it("Vue 错误处理只记录", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    vueErrorHandler(new Error("x"), {}, "render");
    expect(spy).toHaveBeenCalled();
    spy.mockRestore();
  });
});
