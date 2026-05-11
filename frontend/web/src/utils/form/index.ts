/** Form helpers: validation + responsive layout. */

// -----------------------------
// Responsive layout
// -----------------------------

export type ResponsiveBreakpoint = "xs" | "sm" | "md" | "lg" | "xl";

interface BreakpointConfig {
  threshold: number;
  fallback: number;
}

const BREAKPOINT_CONFIG: Record<ResponsiveBreakpoint, BreakpointConfig | null> = {
  xs: { threshold: 12, fallback: 24 },
  sm: { threshold: 12, fallback: 12 },
  md: { threshold: 8, fallback: 8 },
  lg: null,
  xl: null,
};

export function calculateResponsiveSpan(
  itemSpan: number | undefined,
  defaultSpan: number,
  breakpoint: ResponsiveBreakpoint
): number {
  const finalSpan = itemSpan ?? defaultSpan;
  const config = BREAKPOINT_CONFIG[breakpoint];
  if (!config) return finalSpan;
  return finalSpan >= config.threshold ? finalSpan : config.fallback;
}

export function createResponsiveSpanCalculator(defaultSpan: number) {
  return (itemSpan: number | undefined, breakpoint: ResponsiveBreakpoint): number => {
    return calculateResponsiveSpan(itemSpan, defaultSpan, breakpoint);
  };
}

// -----------------------------
// Validation
// -----------------------------

export enum PasswordStrength {
  WEAK = "弱",
  MEDIUM = "中",
  STRONG = "强",
}

export function trimSpaces(value: string): string {
  if (typeof value !== "string") return "";
  return value.trim();
}

export function validatePhone(value: string): boolean {
  if (!value || typeof value !== "string") return false;
  const phoneRegex = /^1[3-9]\d{9}$/;
  return phoneRegex.test(value.trim());
}

export function validateTelPhone(value: string): boolean {
  if (!value || typeof value !== "string") return false;
  const telRegex = /^0\d{2,3}-?\d{7,8}$/;
  return telRegex.test(value.trim().replace(/\s+/g, ""));
}

export function validateAccount(value: string): boolean {
  if (!value || typeof value !== "string") return false;
  const accountRegex = /^[a-zA-Z][a-zA-Z0-9_]{4,19}$/;
  return accountRegex.test(value.trim());
}

export function validatePassword(value: string): boolean {
  if (!value || typeof value !== "string") return false;
  const trimmedValue = value.trim();

  if (trimmedValue.length < 6 || trimmedValue.length > 20) return false;

  const hasLetter = /[a-zA-Z]/.test(trimmedValue);
  const hasNumber = /\d/.test(trimmedValue);
  return hasLetter && hasNumber;
}

export function validateStrongPassword(value: string): boolean {
  if (!value || typeof value !== "string") return false;
  const trimmedValue = value.trim();

  if (trimmedValue.length < 8 || trimmedValue.length > 20) return false;

  const hasUpperCase = /[A-Z]/.test(trimmedValue);
  const hasLowerCase = /[a-z]/.test(trimmedValue);
  const hasNumber = /\d/.test(trimmedValue);
  const hasSpecialChar = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(trimmedValue);
  return hasUpperCase && hasLowerCase && hasNumber && hasSpecialChar;
}

export function getPasswordStrength(value: string): PasswordStrength {
  if (!value || typeof value !== "string") return PasswordStrength.WEAK;
  const trimmedValue = value.trim();
  if (trimmedValue.length < 6) return PasswordStrength.WEAK;

  const hasUpperCase = /[A-Z]/.test(trimmedValue);
  const hasLowerCase = /[a-z]/.test(trimmedValue);
  const hasNumber = /\d/.test(trimmedValue);
  const hasSpecialChar = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(trimmedValue);
  const typeCount = [hasUpperCase, hasLowerCase, hasNumber, hasSpecialChar].filter(Boolean).length;

  if (typeCount >= 3) return PasswordStrength.STRONG;
  if (typeCount >= 2) return PasswordStrength.MEDIUM;
  return PasswordStrength.WEAK;
}

export function validateIPv4Address(value: string): boolean {
  if (!value || typeof value !== "string") return false;
  const trimmedValue = value.trim();
  const ipRegex = /^((25[0-5]|2[0-4]\d|[01]?\d{1,2})\.){3}(25[0-5]|2[0-4]\d|[01]?\d{1,2})$/;

  if (!ipRegex.test(trimmedValue)) return false;

  const segments = trimmedValue.split(".");
  return segments.every((segment) => {
    const num = parseInt(segment, 10);
    return num >= 0 && num <= 255;
  });
}

export function validateEmail(value: string): boolean {
  if (!value || typeof value !== "string") return false;
  const trimmedValue = value.trim();

  const emailRegex =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
  return emailRegex.test(trimmedValue) && trimmedValue.length <= 254;
}

export function validateURL(value: string): boolean {
  if (!value || typeof value !== "string") return false;

  try {
    new URL(value.trim());
    return true;
  } catch {
    return false;
  }
}

export function validateChineseIDCard(value: string): boolean {
  if (!value || typeof value !== "string") return false;
  const trimmedValue = value.trim();

  const idCardRegex =
    /^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/;
  if (!idCardRegex.test(trimmedValue)) return false;

  const weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
  const checkCodes = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"];

  let sum = 0;
  for (let i = 0; i < 17; i++) sum += parseInt(trimmedValue[i]) * weights[i];

  const checkCode = checkCodes[sum % 11];
  return trimmedValue[17].toUpperCase() === checkCode;
}

export function validateBankCard(value: string): boolean {
  if (!value || typeof value !== "string") return false;
  const trimmedValue = value.trim().replace(/\s+/g, "");

  if (!/^\d{13,19}$/.test(trimmedValue)) return false;

  let sum = 0;
  let shouldDouble = false;

  for (let i = trimmedValue.length - 1; i >= 0; i--) {
    let digit = parseInt(trimmedValue[i]);

    if (shouldDouble) {
      digit *= 2;
      if (digit > 9) digit = (digit % 10) + 1;
    }

    sum += digit;
    shouldDouble = !shouldDouble;
  }

  return sum % 10 === 0;
}
