import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ user: {} as any }));
vi.mock("@stores", () => ({ useUserStore: () => mocks.user }));
vi.mock("@/constants", () => ({ ROLE_ROOT: "root" }));

import { checkPerm } from "@/utils/checkPerm";

describe("checkPerm", () => {
  beforeEach(() => { mocks.user = {}; });
  it("空权限视为有权限", () => expect(checkPerm()).toBe(true));
  it("未登录返回 false", () => expect(checkPerm("a:b:c")).toBe(false));
  it("超级管理员放行", () => {
    mocks.user = { basicInfo: { is_superuser: true }, prems: [] };
    expect(checkPerm("a:b:c")).toBe(true);
  });
  it("ROLE_ROOT 放行", () => {
    mocks.user = { basicInfo: { is_superuser: false, roles: [{ code: "root" }] }, prems: [] };
    expect(checkPerm("a:b:c")).toBe(true);
  });
  it("通配符放行", () => {
    mocks.user = { basicInfo: { is_superuser: false, roles: [] }, prems: ["*:*:*"] };
    expect(checkPerm("a:b:c")).toBe(true);
  });
  it("精确权限放行", () => {
    mocks.user = { basicInfo: { is_superuser: false, roles: [] }, prems: ["a:b:c"] };
    expect(checkPerm("a:b:c")).toBe(true);
  });
  it("无权限拒绝", () => {
    mocks.user = { basicInfo: { is_superuser: false, roles: [] }, prems: ["x"] };
    expect(checkPerm("a:b:c")).toBe(false);
  });
});
