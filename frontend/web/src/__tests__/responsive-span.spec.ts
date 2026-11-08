import { describe, expect, it } from "vitest";
import { calculateResponsiveSpan, createResponsiveSpanCalculator } from "@/utils/form";

describe("responsive span", () => {
  it("lg/xl 不降级", () => {
    expect(calculateResponsiveSpan(4, 8, "lg")).toBe(4);
    expect(calculateResponsiveSpan(undefined, 8, "xl")).toBe(8);
  });
  it("md 小于 8 回退 8", () => {
    expect(calculateResponsiveSpan(4, 8, "md")).toBe(8);
    expect(calculateResponsiveSpan(8, 8, "md")).toBe(8);
  });
  it("xs 小于 12 回退 24", () => {
    expect(calculateResponsiveSpan(6, 8, "xs")).toBe(24);
    expect(calculateResponsiveSpan(12, 8, "xs")).toBe(12);
  });
  it("sm 小于 12 回退 12", () => {
    expect(calculateResponsiveSpan(6, 8, "sm")).toBe(12);
    expect(calculateResponsiveSpan(12, 8, "sm")).toBe(12);
  });
  it("工厂函数绑定默认 span", () => {
    const calc = createResponsiveSpanCalculator(8);
    expect(calc(undefined, "md")).toBe(8);
    expect(calc(4, "md")).toBe(8);
  });
});
