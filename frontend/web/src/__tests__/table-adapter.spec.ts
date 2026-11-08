import { describe, expect, it, vi } from "vitest";
if (typeof window !== "undefined" && !window.matchMedia) {
  (window as any).matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
}
const { defaultResponseAdapter, extractTableData, updatePaginationFromResponse } = await import("@/utils/table");

const page = { items: [{ id: 1 }], total: 1, page_no: 1, page_size: 10, has_next: false };

describe("table response adapter", () => {
  it("直接 PageResult", () => {
    expect(defaultResponseAdapter(page)).toEqual({ records: [{ id: 1 }], total: 1, current: 1, size: 10, has_next: false });
  });
  it("标准 data 包装", () => {
    expect(defaultResponseAdapter({ data: page }).total).toBe(1);
  });
  it("非法响应回退默认", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    expect(defaultResponseAdapter({})).toEqual({ records: [], total: 0, current: 1, size: 10 });
    spy.mockRestore();
  });
  it("extractTableData 缺失回退空数组", () => {
    expect(extractTableData({ records: [{ id: 1 }] } as any)).toEqual([{ id: 1 }]);
    expect(extractTableData({} as any)).toEqual([]);
  });
  it("分页总数更新", () => {
    const p = { total: 0 };
    updatePaginationFromResponse(p, { total: 5 } as any);
    expect(p.total).toBe(5);
  });
});
