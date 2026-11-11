import { describe, expect, it } from "vitest";
import { checkStorageInvalidated, markStorageInvalidated, resetStorageInvalidated, StorageConfig } from "@/utils/storage";

describe("storage config", () => {
  it("失效标志位可设置/重置", () => {
    resetStorageInvalidated();
    expect(checkStorageInvalidated()).toBe(false);
    markStorageInvalidated();
    expect(checkStorageInvalidated()).toBe(true);
    resetStorageInvalidated();
    expect(checkStorageInvalidated()).toBe(false);
  });
  it("生成版本化/旧版键名", () => {
    expect(StorageConfig.generateStorageKey("user", "1.0")).toBe("sys-v1.0-user");
    expect(StorageConfig.generateLegacyKey("1.0")).toBe("sys-v1.0");
  });
  it("当前版本键匹配", () => {
    const p = StorageConfig.createCurrentVersionPattern();
    expect(p.test(StorageConfig.generateStorageKey("user"))).toBe(true);
    expect(p.test("other")).toBe(false);
  });
  it("任意版本键匹配", () => {
    const p = StorageConfig.createVersionPattern();
    expect(p.test("sys-v1.0-user")).toBe(true);
    expect(p.test("sys-v2.0-user")).toBe(true);
    expect(p.test("x")).toBe(false);
  });
  it("指定 storeId 键匹配", () => {
    const p = StorageConfig.createKeyPattern("user");
    expect(p.test("sys-v1.0-user")).toBe(true);
    expect(p.test("sys-v1.0-role")).toBe(false);
  });
});
