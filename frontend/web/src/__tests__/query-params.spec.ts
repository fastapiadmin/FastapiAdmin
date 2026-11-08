import { describe, expect, it } from "vitest";
import { cleanEmptyArrayParams, stripPaginationParams } from "@/utils/query";

describe("query utils", () => {
  it("清理默认空数组", () => {
    expect(cleanEmptyArrayParams({ created_time: [], updated_time: [], name: "x" }))
      .toEqual({ created_time: undefined, updated_time: undefined, name: "x" });
  });
  it("非空数组保留", () => {
    expect(cleanEmptyArrayParams({ created_time: ["2024"] }).created_time).toEqual(["2024"]);
  });
  it("支持自定义键", () => {
    expect(cleanEmptyArrayParams({ ids: [], other: [] }, ["ids"])).toEqual({ ids: undefined, other: [] });
  });
  it("移除分页字段且不改原对象", () => {
    const input = { current: 1, size: 10, page_no: 1, page_size: 10, name: "x" };
    const out = stripPaginationParams(input);
    expect(out).toEqual({ name: "x" });
    expect(input.page_no).toBe(1);
  });
});
