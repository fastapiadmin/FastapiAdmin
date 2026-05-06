/** UI helpers (flattened). */

import NProgress from "nprogress";
import "nprogress/nprogress.css";
import { ThemeMode } from "@/enums";
import { useSettingsStore } from "@/store/modules/setting.store";
import { fourDotsSpinnerSvg } from "@/assets/svg/loading";
import { useCommon } from "@/hooks/core/useCommon";
import { useTheme } from "@/hooks/core/useTheme";
import { SystemThemeEnum } from "@/enums/appEnum";

// -----------------------------
// NProgress
// -----------------------------

NProgress.configure({
  easing: "ease",
  speed: 500,
  showSpinner: false,
  trickleSpeed: 200,
  minimum: 0.3,
});

export { NProgress };

// -----------------------------
// Colors
// -----------------------------

interface RgbaResult {
  red: number;
  green: number;
  blue: number;
  rgba: string;
}

export function getCssVar(name: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(name);
}

function isValidHexColor(hex: string): boolean {
  const cleanHex = hex.trim().replace(/^#/, "");
  return /^[0-9A-Fa-f]{3}$|^[0-9A-Fa-f]{6}$/.test(cleanHex);
}

function isValidRgbValue(r: number, g: number, b: number): boolean {
  const isValid = (value: number) => Number.isInteger(value) && value >= 0 && value <= 255;
  return isValid(r) && isValid(g) && isValid(b);
}

export function hexToRgba(hex: string, opacity: number): RgbaResult {
  if (!isValidHexColor(hex)) throw new Error("Invalid hex color format");

  let cleanHex = hex.trim().replace(/^#/, "").toUpperCase();
  if (cleanHex.length === 3) {
    cleanHex = cleanHex
      .split("")
      .map((char) => char.repeat(2))
      .join("");
  }

  const [red, green, blue] = cleanHex.match(/\w\w/g)!.map((x) => parseInt(x, 16));
  const validOpacity = Math.max(0, Math.min(1, opacity));
  const rgba = `rgba(${red}, ${green}, ${blue}, ${validOpacity.toFixed(2)})`;
  return { red, green, blue, rgba };
}

export function hexToRgb(hexColor: string): number[] {
  if (!isValidHexColor(hexColor)) {
    ElMessage.warning("输入错误的hex颜色值");
    throw new Error("Invalid hex color format");
  }

  const cleanHex = hexColor.replace(/^#/, "");
  let hex = cleanHex;
  if (hex.length === 3) {
    hex = hex
      .split("")
      .map((char) => char.repeat(2))
      .join("");
  }

  const hexPairs = hex.match(/../g);
  if (!hexPairs) throw new Error("Invalid hex color format");
  return hexPairs.map((hexPair) => parseInt(hexPair, 16));
}

export function rgbToHex(r: number, g: number, b: number): string {
  if (!isValidRgbValue(r, g, b)) {
    ElMessage.warning("输入错误的RGB颜色值");
    throw new Error("Invalid RGB color values");
  }

  const toHex = (value: number) => {
    const hex = value.toString(16);
    return hex.length === 1 ? `0${hex}` : hex;
  };

  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}

export function colourBlend(color1: string, color2: string, ratio: number): string {
  const validRatio = Math.max(0, Math.min(1, Number(ratio)));
  const rgb1 = hexToRgb(color1);
  const rgb2 = hexToRgb(color2);

  const blendedRgb = rgb1.map((value1, index) => {
    const value2 = rgb2[index];
    return Math.round(value1 * (1 - validRatio) + value2 * validRatio);
  });

  return rgbToHex(blendedRgb[0], blendedRgb[1], blendedRgb[2]);
}

export function getLightColor(color: string, level: number, isDark: boolean = false): string {
  if (!isValidHexColor(color)) {
    ElMessage.warning("输入错误的hex颜色值");
    throw new Error("Invalid hex color format");
  }

  if (isDark) return getDarkColor(color, level);

  const rgb = hexToRgb(color);
  const lightRgb = rgb.map((value) => Math.floor((255 - value) * level + value));
  return rgbToHex(lightRgb[0], lightRgb[1], lightRgb[2]);
}

export function getDarkColor(color: string, level: number): string {
  if (!isValidHexColor(color)) {
    ElMessage.warning("输入错误的hex颜色值");
    throw new Error("Invalid hex color format");
  }

  const rgb = hexToRgb(color);
  const darkRgb = rgb.map((value) => Math.floor(value * (1 - level)));
  return rgbToHex(darkRgb[0], darkRgb[1], darkRgb[2]);
}

export function handleElementThemeColor(theme: string, isDark: boolean = false): void {
  document.documentElement.style.setProperty("--el-color-primary", theme);

  for (let i = 1; i <= 9; i++) {
    document.documentElement.style.setProperty(
      `--el-color-primary-light-${i}`,
      getLightColor(theme, i / 10, isDark)
    );
  }

  for (let i = 1; i <= 9; i++) {
    document.documentElement.style.setProperty(
      `--el-color-primary-dark-${i}`,
      getDarkColor(theme, i / 10)
    );
  }
}

export function setElementThemeColor(color: string): void {
  const mixColor = "#ffffff";
  const elStyle = document.documentElement.style;

  elStyle.setProperty("--el-color-primary", color);
  handleElementThemeColor(color, useSettingsStore().isDark);

  for (let i = 1; i < 16; i++) {
    const itemColor = colourBlend(color, mixColor, i / 16);
    elStyle.setProperty(`--el-color-primary-custom-${i}`, itemColor);
  }
}

// -----------------------------
// Theme utils
// -----------------------------

export function generateThemeColors(primary: string, theme: ThemeMode): Record<string, string> {
  const colors: Record<string, string> = { primary };

  for (let i = 1; i <= 9; i++) {
    colors[`primary-light-${i}`] =
      theme === ThemeMode.LIGHT
        ? `${getLightColor(primary, i / 10)}`
        : `${getDarkColor(primary, i / 10)}`;
  }

  colors["primary-dark-2"] =
    theme === ThemeMode.LIGHT ? `${getLightColor(primary, 0.2)}` : `${getDarkColor(primary, 0.3)}`;

  return colors;
}

export function applyTheme(colors: Record<string, string>): void {
  const el = document.documentElement;

  Object.entries(colors).forEach(([key, value]) => {
    el.style.setProperty(`--el-color-${key}`, value);
  });

  requestAnimationFrame(() => {
    el.style.setProperty("--theme-update-trigger", Date.now().toString());
  });
}

export function toggleDarkMode(isDark: boolean): void {
  if (isDark) document.documentElement.classList.add(ThemeMode.DARK);
  else document.documentElement.classList.remove(ThemeMode.DARK);
}

export function toggleSidebarColor(isBlueSidebar: boolean): void {
  if (isBlueSidebar) document.documentElement.classList.add("sidebar-color-blue");
  else document.documentElement.classList.remove("sidebar-color-blue");
}

// -----------------------------
// Loading
// -----------------------------

const getLoadingBackground = (): string => {
  const isDark = document.documentElement.classList.contains("dark");
  return isDark ? "rgba(7, 7, 7, 0.85)" : "#fff";
};

const DEFAULT_LOADING_CONFIG = {
  lock: true,
  get background() {
    return getLoadingBackground();
  },
  svg: fourDotsSpinnerSvg,
  svgViewBox: "0 0 40 40",
  customClass: "art-loading-fix",
} as const;

interface LoadingInstance {
  close: () => void;
}

let loadingInstance: LoadingInstance | null = null;

export const loadingService = {
  showLoading(): () => void {
    if (!loadingInstance) {
      const config = { ...DEFAULT_LOADING_CONFIG, background: getLoadingBackground() };
      loadingInstance = ElLoading.service(config);
    }
    return () => loadingService.hideLoading();
  },

  hideLoading(): void {
    if (!loadingInstance) return;
    loadingInstance.close();
    loadingInstance = null;
  },
};

// -----------------------------
// Tabs config
// -----------------------------

export const TAB_CONFIG = {
  "tab-default": { openTop: 106, closeTop: 60, openHeight: 121, closeHeight: 75 },
  "tab-card": { openTop: 122, closeTop: 78, openHeight: 139, closeHeight: 95 },
  "tab-google": { openTop: 122, closeTop: 78, openHeight: 139, closeHeight: 95 },
};

export const getTabConfig = (style: string) =>
  TAB_CONFIG[style as keyof typeof TAB_CONFIG] || TAB_CONFIG["tab-card"];

// -----------------------------
// EmojiText (default export-compatible)
// -----------------------------

export const EmojiText: { [key: string]: string } = {
  "0": "O_O",
  "200": "^_^",
  "400": "T_T",
  "500": "X_X",
};

// -----------------------------
// Theme animation
// -----------------------------

const { LIGHT, DARK } = SystemThemeEnum;

export const themeAnimation = (e: any) => {
  const x = e.clientX;
  const y = e.clientY;
  const endRadius = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));

  document.documentElement.style.setProperty("--x", x + "px");
  document.documentElement.style.setProperty("--y", y + "px");
  document.documentElement.style.setProperty("--r", endRadius + "px");

  if (document.startViewTransition) document.startViewTransition(() => toggleTheme());
  else toggleTheme();
};

const toggleTheme = () => {
  useTheme().switchThemeStyles(useSettingsStore().systemThemeType === LIGHT ? DARK : LIGHT);
  useCommon().refresh();
};

export const toggleTransition = (enable: boolean) => {
  const body = document.body;

  if (enable) body.classList.add("theme-change");
  else {
    setTimeout(() => {
      body.classList.remove("theme-change");
    }, 300);
  }
};
