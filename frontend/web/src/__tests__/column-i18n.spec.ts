import { describe, expect, it } from "vitest";
import { translateColumnLabels, translateFormLabels, translateStatusText } from "@/utils/table/columnLabelI18n";

const t = (k: string) => `T:${k}`;

describe("column label i18n", () => {
  it("翻译已知表头", () => {
    expect(translateColumnLabels([{ prop: "a", label: "状态" }], t)[0]!.label).toBe("T:common.table.status");
  });
  it("未知/非字符串表头保留", () => {
    expect(translateColumnLabels([{ prop: "a", label: "自定义" }], t)[0]!.label).toBe("自定义");
  });
  it("状态文本命中与未命中", () => {
    expect(translateStatusText("启用", t)).toBe("T:common.enabled");
    expect(translateStatusText("未知状态", t)).toBe("未知状态");
  });
  it("表单 label/placeholder 翻译", () => {
    const out = translateFormLabels([{ label: "账号", placeholder: "请输入账号" }], t);
    expect(out[0]).toEqual({ label: "T:common.account", placeholder: "T:common.placeholder.account" });
  });
  it("无匹配字段原样返回", () => {
    const item = { label: "其他" };
    expect(translateFormLabels([item], t)[0]).toEqual(item);
  });
});
