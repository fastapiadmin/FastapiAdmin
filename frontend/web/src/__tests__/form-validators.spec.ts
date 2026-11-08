import { describe, expect, it } from "vitest";
import {
  PasswordStrength, getPasswordStrength, trimSpaces, validateAccount, validateBankCard,
  validateChineseIDCard, validateEmail, validateIPv4Address, validatePassword,
  validatePhone, validateStrongPassword, validateTelPhone, validateURL,
} from "@/utils/form";

describe("form validators", () => {
  it("trimSpaces 非字符串回退空串", () => {
    expect(trimSpaces("  x ")).toBe("x");
    expect(trimSpaces(undefined as any)).toBe("");
  });
  it("手机号/固话", () => {
    expect(validatePhone("13800138000")).toBe(true);
    expect(validatePhone("123")).toBe(false);
    expect(validateTelPhone("010-12345678")).toBe(true);
  });
  it("账号/普通密码", () => {
    expect(validateAccount("abc_123")).toBe(true);
    expect(validateAccount("1abc")).toBe(false);
    expect(validatePassword("abc123")).toBe(true);
    expect(validatePassword("abcdef")).toBe(false);
  });
  it("强密码/强度", () => {
    expect(validateStrongPassword("Abc123!x")).toBe(true);
    expect(validateStrongPassword("abc123")).toBe(false);
    expect(getPasswordStrength("Abc123!x")).toBe(PasswordStrength.STRONG);
    expect(getPasswordStrength("abcdef")).toBe(PasswordStrength.WEAK);
  });
  it("邮箱/URL/IPv4", () => {
    expect(validateEmail("a@b.com")).toBe(true);
    expect(validateEmail("bad")).toBe(false);
    expect(validateURL("https://x.com")).toBe(true);
    expect(validateURL("x")).toBe(false);
    expect(validateIPv4Address("192.168.1.1")).toBe(true);
    expect(validateIPv4Address("999.1.1.1")).toBe(false);
  });
  it("身份证/银行卡", () => {
    expect(validateChineseIDCard("11010519491231002X")).toBe(true);
    expect(validateChineseIDCard("bad")).toBe(false);
    expect(validateBankCard("4111 1111 1111 1111")).toBe(true);
    expect(validateBankCard("1234")).toBe(false);
  });
});
