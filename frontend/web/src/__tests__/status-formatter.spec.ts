import { describe, expect, it, vi } from "vitest";
vi.mock("@/components/display/fa-status-tag/index.vue", () => ({ default: { name: "StatusTag" } }));

import { makeStatusFormatter, resolveStatusColumns } from "@/utils/table/statusFormatter";

describe("status formatter", () => {
  const map = { 0: { type: "success" as const, text: "启用" }, 1: { type: "danger" as const, text: "停用" } };
  it("valueGetter 命中", () => {
    const vnode = makeStatusFormatter({ valueGetter: (r: any) => r.status, map })({ status: 0 });
    expect(vnode.props?.label).toBe("启用");
  });
  it("回退默认", () => {
    const vnode = makeStatusFormatter({ valueGetter: (r: any) => r.status, map })({ status: 9 });
    expect(vnode.props?.label).toBe("—");
  });
  it("直接 value 模式", () => {
    const vnode = makeStatusFormatter({ map })(1);
    expect(vnode.props?.label).toBe("停用");
  });
  it("resolveStatusColumns 保留显式 formatter 并转换 status", () => {
    const cols = resolveStatusColumns(() => [
      { prop: "a", label: "A", formatter: () => "x" },
      { prop: "status", label: "S", status: map },
      { prop: "b", label: "B" },
    ])();
    expect(cols[0].formatter).toBeDefined();
    expect(cols[1].status).toBeUndefined();
    expect((cols[1].formatter as any)({ status: 1 }).props?.label).toBe("停用");
    expect(cols[2].formatter).toBeUndefined();
  });
});
