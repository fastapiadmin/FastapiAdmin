import { ThemeMode } from "@/enums";

const COLOR_VARIANT_LEVELS = [0.08, 0.16, 0.24, 0.32, 0.4, 0.52, 0.64, 0.76, 0.88];

function normalizeHexColor(hex: string): string {
  return hex.length === 9 ? hex.slice(0, 7) : hex;
}

function hexToRgb(hex: string): [number, number, number] {
  const cleanHex = normalizeHexColor(hex);
  const bigint = parseInt(cleanHex.slice(1), 16);
  return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255];
}

function rgbToHex(r: number, g: number, b: number): string {
  return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
}

function getLuminance(hex: string): number {
  const rgb = hexToRgb(hex);
  const [r, g, b] = rgb.map((val) => {
    const s = val / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function getDarkColor(color: string, level: number): string {
  const rgb = hexToRgb(color);
  for (let i = 0; i < 3; i++) rgb[i] = Math.round(20.5 * level + rgb[i] * (1 - level));
  return rgbToHex(rgb[0], rgb[1], rgb[2]);
}

function getLightColor(color: string, level: number): string {
  const rgb = hexToRgb(color);
  for (let i = 0; i < 3; i++) rgb[i] = Math.round(255 * level + rgb[i] * (1 - level));
  return rgbToHex(rgb[0], rgb[1], rgb[2]);
}

function blendTwoColors(baseColor: string, mixColor: string, ratio: number): string {
  const rgb1 = hexToRgb(baseColor);
  const rgb2 = hexToRgb(mixColor);
  const w = ratio * 2 - 1;
  const w1 = (w + 1) / 2;
  const w2 = 1 - w1;
  const r = Math.round(rgb1[0] * w2 + rgb2[0] * w1);
  const g = Math.round(rgb1[1] * w2 + rgb2[1] * w1);
  const b = Math.round(rgb1[2] * w2 + rgb2[2] * w1);
  return rgbToHex(r, g, b);
}

interface ColorVariants {
  light: string[];
  dark: string;
}

function generateColorVariants(baseColor: string): ColorVariants {
  const light = COLOR_VARIANT_LEVELS.map((level) => getLightColor(baseColor, level));
  const dark = getDarkColor(baseColor, 0.15);
  return { light, dark };
}

function generateDarkModeVariants(baseColor: string): ColorVariants {
  const light = COLOR_VARIANT_LEVELS.map((level) => getDarkColor(baseColor, level));
  const dark = getLightColor(baseColor, 0.15);
  return { light, dark };
}

interface ColorScheme {
  bg: {
    primary: string;
    secondary: string;
    tertiary: string;
    overlay?: string;
  };
  fill: {
    base: string;
    light: string;
    lighter: string;
    extraLight: string;
    dark: string;
    darker: string;
  };
  shadow: {
    base: string;
    light: string;
    lighter: string;
    dark: string;
  };
  border: {
    base: string;
    light: string;
    lighter: string;
    extraLight: string;
    dark: string;
    darker: string;
  };
  sidebar: {
    background: string;
    text: string;
    activeText: string;
    activeBg: string;
    activeHoverBg: string;
    hover: string;
  };
  menu: {
    background: string;
    text: string;
    activeText: string;
    activeBg: string;
    hover: string;
  };
  text: {
    primary: string;
    secondary: string;
    tertiary: string;
    disabled: string;
  };
}

interface CoreThemeTokens {
  brandPrimary: string;
  layoutBgPrimary: string;
  layoutBgSecondary: string;
  layoutBgTertiary: string;
  layoutSidebarBg: string;
  layoutSidebarText: string;
  layoutSidebarActiveText: string;
  layoutSidebarActiveBg: string;
  layoutSidebarActiveHoverBg: string;
  layoutSidebarHover: string;
  layoutMenuActiveBg: string;
  layoutHeaderBg: string;
  layoutHeaderText: string;
  layoutHeaderBorder: string;
  layoutTagsBg: string;
  layoutTagsBorder: string;
  layoutTagsItemBg: string;
  layoutTagsItemText: string;
  layoutTagsItemActiveBg: string;
  layoutTagsItemActiveText: string;
  layoutContentBg: string;
  layoutContentSurfaceBg: string;
}

const LIGHT_TEXT_SCHEME: ColorScheme["text"] = {
  primary: "#0f172a",
  secondary: "#475569",
  tertiary: "#64748b",
  disabled: "#94a3b8",
};

const DARK_TEXT_SCHEME: ColorScheme["text"] = {
  primary: "#f8fafc",
  secondary: "#cbd5e1",
  tertiary: "#94a3b8",
  disabled: "#64748b",
};

const LIGHT_SHADOW_SCHEME: ColorScheme["shadow"] = {
  base: `0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)`,
  light: `0 1px 2px 0 rgba(0, 0, 0, 0.05)`,
  lighter: `0 1px 1px 0 rgba(0, 0, 0, 0.03)`,
  dark: `0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)`,
};

const DARK_SHADOW_SCHEME: ColorScheme["shadow"] = {
  base: `0 1px 3px 0 rgba(0, 0, 0, 0.4), 0 1px 2px 0 rgba(0, 0, 0, 0.24)`,
  light: `0 1px 2px 0 rgba(0, 0, 0, 0.2)`,
  lighter: `0 1px 1px 0 rgba(0, 0, 0, 0.12)`,
  dark: `0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.24)`,
};

const ENTERPRISE_LIGHT_NEUTRAL = {
  bgPrimary: "#f5f7fb",
  bgSecondary: "#ffffff",
  bgTertiary: "#f8fafc",
  fillBase: "#eef3fb",
  fillLight: "#f7f9fd",
  fillLighter: "#ffffff",
  borderBase: "#d8e2f0",
  borderLight: "#e7edf5",
  borderLighter: "#f0f4fa",
};

const ENTERPRISE_DARK_NEUTRAL = {
  bgPrimary: "#0b1220",
  bgSecondary: "#111a2c",
  bgTertiary: "#17233a",
  fillBase: "#141f33",
  fillLight: "#1b2a45",
  fillLighter: "#111a2c",
  borderBase: "#253858",
  borderLight: "#31486b",
  borderLighter: "#3f5c86",
};

function createCoreThemeTokens(scheme: ColorScheme, primary: string): CoreThemeTokens {
  const isDarkScheme = scheme.text.primary === DARK_TEXT_SCHEME.primary;
  const headerBg = blendTwoColors(scheme.menu.background, scheme.bg.secondary, 0.18);
  const tagsBg = blendTwoColors(scheme.bg.secondary, scheme.fill.light, 0.28);
  const tagsItemBg = blendTwoColors(scheme.bg.secondary, scheme.fill.light, 0.18);
  const tagsItemActiveBg = isDarkScheme
    ? blendTwoColors(scheme.fill.light, primary, 0.28)
    : blendTwoColors(scheme.fill.light, primary, 0.2);
  const tagsItemActiveText = isDarkScheme
    ? getLightColor(primary, 0.1)
    : getDarkColor(primary, 0.08);
  // 内容区分为两层：页面底色 + 容器(padding空白区)底色，提升层次感
  const contentBg = blendTwoColors(scheme.bg.primary, scheme.fill.light, 0.08);
  const contentSurfaceBg = blendTwoColors(scheme.bg.secondary, scheme.fill.base, 0.22);

  return {
    brandPrimary: primary,
    layoutBgPrimary: scheme.bg.primary,
    layoutBgSecondary: scheme.bg.overlay ?? scheme.bg.secondary,
    layoutBgTertiary: scheme.bg.tertiary,
    layoutSidebarBg: scheme.sidebar.background,
    layoutSidebarText: scheme.sidebar.text,
    layoutSidebarActiveText: scheme.sidebar.activeText,
    layoutSidebarActiveBg: scheme.sidebar.activeBg,
    layoutSidebarActiveHoverBg: scheme.sidebar.activeHoverBg,
    layoutSidebarHover: scheme.sidebar.hover,
    layoutMenuActiveBg: scheme.menu.activeBg,
    layoutHeaderBg: headerBg,
    layoutHeaderText: scheme.text.primary,
    layoutHeaderBorder: scheme.border.light,
    layoutTagsBg: tagsBg,
    layoutTagsBorder: scheme.border.light,
    layoutTagsItemBg: tagsItemBg,
    layoutTagsItemText: scheme.text.primary,
    layoutTagsItemActiveBg: tagsItemActiveBg,
    layoutTagsItemActiveText: tagsItemActiveText,
    layoutContentBg: contentBg,
    layoutContentSurfaceBg: contentSurfaceBg,
  };
}

function generateLightThemeScheme(primary: string): ColorScheme {
  const activeBg = blendTwoColors(ENTERPRISE_LIGHT_NEUTRAL.fillLight, primary, 0.18);
  const activeHoverBg = blendTwoColors(ENTERPRISE_LIGHT_NEUTRAL.fillBase, primary, 0.24);

  return {
    bg: {
      primary: ENTERPRISE_LIGHT_NEUTRAL.bgPrimary,
      secondary: ENTERPRISE_LIGHT_NEUTRAL.bgSecondary,
      tertiary: ENTERPRISE_LIGHT_NEUTRAL.bgTertiary,
    },
    fill: {
      base: ENTERPRISE_LIGHT_NEUTRAL.fillBase,
      light: ENTERPRISE_LIGHT_NEUTRAL.fillLight,
      lighter: ENTERPRISE_LIGHT_NEUTRAL.fillLighter,
      extraLight: "#ffffff",
      dark: blendTwoColors(ENTERPRISE_LIGHT_NEUTRAL.fillBase, primary, 0.12),
      darker: blendTwoColors(ENTERPRISE_LIGHT_NEUTRAL.borderBase, primary, 0.16),
    },
    shadow: LIGHT_SHADOW_SCHEME,
    border: {
      base: blendTwoColors(ENTERPRISE_LIGHT_NEUTRAL.borderBase, primary, 0.1),
      light: blendTwoColors(ENTERPRISE_LIGHT_NEUTRAL.borderLight, primary, 0.08),
      lighter: blendTwoColors(ENTERPRISE_LIGHT_NEUTRAL.borderLighter, primary, 0.05),
      extraLight: "#ffffff",
      dark: blendTwoColors("#94a3b8", primary, 0.15),
      darker: blendTwoColors("#64748b", primary, 0.2),
    },
    sidebar: {
      background: blendTwoColors(ENTERPRISE_LIGHT_NEUTRAL.bgSecondary, primary, 0.06),
      text: "#1e293b",
      activeText: getDarkColor(primary, 0.1),
      activeBg,
      activeHoverBg,
      hover: blendTwoColors(ENTERPRISE_LIGHT_NEUTRAL.fillLight, primary, 0.15),
    },
    menu: {
      background: blendTwoColors(ENTERPRISE_LIGHT_NEUTRAL.bgSecondary, primary, 0.04),
      text: "#1e293b",
      activeText: getDarkColor(primary, 0.1),
      activeBg,
      hover: blendTwoColors(ENTERPRISE_LIGHT_NEUTRAL.fillLight, primary, 0.08),
    },
    text: LIGHT_TEXT_SCHEME,
  };
}

function generateDarkThemeScheme(primary: string): ColorScheme {
  const baseDarkBg = blendTwoColors(ENTERPRISE_DARK_NEUTRAL.bgPrimary, primary, 0.04);
  const secondaryDarkBg = blendTwoColors(ENTERPRISE_DARK_NEUTRAL.bgSecondary, primary, 0.06);
  const tertiaryDarkBg = blendTwoColors(ENTERPRISE_DARK_NEUTRAL.bgTertiary, primary, 0.08);
  const activeBg = blendTwoColors(ENTERPRISE_DARK_NEUTRAL.fillLight, primary, 0.22);
  const activeHoverBg = blendTwoColors(ENTERPRISE_DARK_NEUTRAL.fillLight, primary, 0.28);

  return {
    bg: {
      primary: baseDarkBg,
      secondary: secondaryDarkBg,
      tertiary: tertiaryDarkBg,
      overlay: secondaryDarkBg,
    },
    fill: {
      base: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.fillBase, primary, 0.08),
      light: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.fillLight, primary, 0.12),
      lighter: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.fillLighter, primary, 0.06),
      extraLight: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.bgPrimary, primary, 0.04),
      dark: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.borderLight, primary, 0.16),
      darker: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.borderLighter, primary, 0.18),
    },
    shadow: DARK_SHADOW_SCHEME,
    border: {
      base: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.borderBase, primary, 0.1),
      light: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.borderLight, primary, 0.14),
      lighter: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.borderLighter, primary, 0.16),
      extraLight: blendTwoColors("#64748b", primary, 0.2),
      dark: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.bgSecondary, primary, 0.08),
      darker: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.bgPrimary, primary, 0.06),
    },
    sidebar: {
      background: secondaryDarkBg,
      text: "#e2e8f0",
      activeText: getLightColor(primary, 0.15),
      activeBg,
      activeHoverBg,
      hover: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.fillLight, primary, 0.14),
    },
    menu: {
      background: secondaryDarkBg,
      text: "#e2e8f0",
      activeText: getLightColor(primary, 0.15),
      activeBg,
      hover: blendTwoColors(ENTERPRISE_DARK_NEUTRAL.fillLight, primary, 0.14),
    },
    text: DARK_TEXT_SCHEME,
  };
}

const SEMANTIC_COLORS = {
  success: "#10b981",
  warning: "#f59e0b",
  danger: "#ef4444",
  info: "#2f86ff",
} as const;

function assignThemeRoleColors(colors: Record<string, string>, scheme: ColorScheme): void {
  // Element Plus 核心变量
  colors["el-bg-color"] = scheme.bg.primary;
  colors["el-bg-color-page"] = scheme.bg.primary;
  colors["el-bg-color-overlay"] = scheme.bg.overlay ?? scheme.bg.secondary;

  // 边框颜色
  colors["el-border-color"] = scheme.border.base;
  colors["el-border-color-light"] = scheme.border.light;
  colors["el-border-color-lighter"] = scheme.border.lighter;
  colors["el-border-color-extra-light"] = scheme.border.extraLight;
  colors["el-border-color-dark"] = scheme.border.dark;
  colors["el-border-color-darker"] = scheme.border.darker;

  // 填充颜色
  colors["el-fill-color"] = scheme.fill.base;
  colors["el-fill-color-light"] = scheme.fill.light;
  colors["el-fill-color-lighter"] = scheme.fill.lighter;
  colors["el-fill-color-extra-light"] = scheme.fill.extraLight;
  colors["el-fill-color-dark"] = scheme.fill.dark;
  colors["el-fill-color-darker"] = scheme.fill.darker;

  // 阴影效果
  colors["el-box-shadow"] = scheme.shadow.base;
  colors["el-box-shadow-light"] = scheme.shadow.light;
  colors["el-box-shadow-lighter"] = scheme.shadow.lighter;
  colors["el-box-shadow-dark"] = scheme.shadow.dark;

  // 抽屉背景色
  colors["el-drawer-bg-color"] = scheme.fill.base;

  // 菜单 / 侧边栏由 layout-* 语义变量统一驱动（见 assignCoreLayoutTokens）
}

function assignCoreLayoutTokens(colors: Record<string, string>, coreTokens: CoreThemeTokens): void {
  colors["el-color-primary"] = coreTokens.brandPrimary;
  colors["layout-bg-primary"] = coreTokens.layoutBgPrimary;
  colors["layout-bg-secondary"] = coreTokens.layoutBgSecondary;
  colors["layout-bg-tertiary"] = coreTokens.layoutBgTertiary;
  colors["layout-sidebar-bg"] = coreTokens.layoutSidebarBg;
  colors["layout-sidebar-text"] = coreTokens.layoutSidebarText;
  colors["layout-sidebar-active-text"] = coreTokens.layoutSidebarActiveText;
  colors["layout-sidebar-active-bg"] = coreTokens.layoutSidebarActiveBg;
  colors["layout-sidebar-active-hover-bg"] = coreTokens.layoutSidebarActiveHoverBg;
  colors["layout-sidebar-hover"] = coreTokens.layoutSidebarHover;
  colors["layout-header-bg"] = coreTokens.layoutHeaderBg;
  colors["layout-header-text"] = coreTokens.layoutHeaderText;
  colors["layout-header-border"] = coreTokens.layoutHeaderBorder;
  colors["layout-tags-bg"] = coreTokens.layoutTagsBg;
  colors["layout-tags-border"] = coreTokens.layoutTagsBorder;
  colors["layout-tags-item-bg"] = coreTokens.layoutTagsItemBg;
  colors["layout-tags-item-text"] = coreTokens.layoutTagsItemText;
  colors["layout-tags-item-active-bg"] = coreTokens.layoutTagsItemActiveBg;
  colors["layout-tags-item-active-text"] = coreTokens.layoutTagsItemActiveText;
  colors["layout-content-bg"] = coreTokens.layoutContentBg;
  colors["layout-content-surface-bg"] = coreTokens.layoutContentSurfaceBg;
  colors["layout-menu-bg"] = coreTokens.layoutSidebarBg;
  colors["layout-menu-text"] = coreTokens.layoutSidebarText;
  colors["layout-menu-active-text"] = coreTokens.layoutSidebarActiveText;
  colors["layout-menu-active-bg"] = coreTokens.layoutMenuActiveBg;
  colors["layout-menu-hover"] = coreTokens.layoutSidebarHover;
  colors["layout-logo-bg"] = coreTokens.layoutSidebarBg;
  colors["layout-logo-text"] = coreTokens.layoutSidebarActiveText;
  colors["layout-text-primary"] = colors["layout-text-primary"] ?? "#0f172a";
  colors["layout-text-secondary"] = colors["layout-text-secondary"] ?? "#475569";
  colors["layout-text-tertiary"] = colors["layout-text-tertiary"] ?? "#64748b";
  colors["layout-text-disabled"] = colors["layout-text-disabled"] ?? "#94a3b8";
}

export function generateThemeColors(primary: string, theme: ThemeMode) {
  const cleanPrimary = normalizeHexColor(primary);
  const colors: Record<string, string> = {
    primary: cleanPrimary,
    ...SEMANTIC_COLORS,
  };

  const rgb = hexToRgb(cleanPrimary);

  const isDarkMode = theme === ThemeMode.DARK;
  const primaryVariants = isDarkMode
    ? generateDarkModeVariants(cleanPrimary)
    : generateColorVariants(cleanPrimary);

  // 生成颜色变体，使用 Element Plus 标准命名
  primaryVariants.light.forEach((color, i) => {
    colors[`primary-light-${i + 1}`] = color;
  });
  colors["primary-dark-2"] = primaryVariants.dark;

  Object.entries(SEMANTIC_COLORS).forEach(([name, color]) => {
    const variants = isDarkMode ? generateDarkModeVariants(color) : generateColorVariants(color);
    variants.light.forEach((c, i) => {
      colors[`${name}-light-${i + 1}`] = c;
    });
    colors[`${name}-dark-2`] = variants.dark;
  });

  // 品牌颜色 RGB 值，用于科技感效果
  colors["brand-primary-rgb"] = `${rgb[0]}, ${rgb[1]}, ${rgb[2]}`;
  Object.entries(SEMANTIC_COLORS).forEach(([name, color]) => {
    const c = hexToRgb(color);
    colors[`brand-${name}-rgb`] = `${c[0]}, ${c[1]}, ${c[2]}`;
  });

  // 生成主题方案
  const scheme = isDarkMode
    ? generateDarkThemeScheme(cleanPrimary)
    : generateLightThemeScheme(cleanPrimary);

  // 文本语义变量
  colors["layout-text-primary"] = scheme.text.primary;
  colors["layout-text-secondary"] = scheme.text.secondary;
  colors["layout-text-tertiary"] = scheme.text.tertiary;
  colors["layout-text-disabled"] = scheme.text.disabled;

  // 角色色和核心 token（主题控制主入口）
  assignThemeRoleColors(colors, scheme);
  const coreTokens = createCoreThemeTokens(scheme, cleanPrimary);

  assignCoreLayoutTokens(colors, coreTokens);

  return colors;
}

export function applyTheme(colors: Record<string, string>) {
  const el = document.documentElement;

  const setVar = (key: string, value: string) => {
    el.style.setProperty(`--${key}`, value);
  };

  const pickColor = (keys: string[]) => keys.map((k) => colors[k]).find(Boolean);
  const isDirectCssVar = (key: string) =>
    key.startsWith("el-") || key.startsWith("brand-") || key.startsWith("layout-");

  // 仅允许核心调色板变量走 --el-color-*，避免无关变量污染 :root
  const isAllowedElColorToken = (key: string) =>
    /^(primary|success|warning|danger|info)$/.test(key) ||
    /^(primary|success|warning|danger|info)-light-[1-9]$/.test(key) ||
    /^(primary|success|warning|danger|info)-dark-2$/.test(key);

  Object.entries(colors).forEach(([key, value]) => {
    if (isDirectCssVar(key)) {
      setVar(key, value);
      return;
    }
    if (isAllowedElColorToken(key)) {
      // Element Plus 色板变量（--el-color-primary-light-1 等）
      setVar(`el-color-${key}`, value);
    }
  });

  // 确保布局相关的背景变量也被设置
  setVar("bg-primary", pickColor(["layout-bg-primary", "el-bg-color"]) ?? "");
  setVar("bg-secondary", pickColor(["layout-bg-secondary", "el-bg-color-overlay"]) ?? "");
  setVar("bg-tertiary", pickColor(["layout-bg-tertiary", "el-bg-color-overlay"]) ?? "");

  // 触发主题更新动画
  requestAnimationFrame(() => {
    el.style.setProperty("--theme-update-trigger", Date.now().toString());
  });
}

export function toggleDarkMode(isDark: boolean) {
  if (isDark) {
    document.documentElement.classList.add(ThemeMode.DARK);
  } else {
    document.documentElement.classList.remove(ThemeMode.DARK);
  }
}

export function getThemeColorInfo(hex: string) {
  const luminance = getLuminance(hex);
  const rgb = hexToRgb(hex);
  return {
    hex,
    rgb,
    luminance,
    isLight: luminance > 0.5,
    isDark: luminance <= 0.5,
    contrast: luminance > 0.5 ? "light" : "dark",
  };
}

export { getDarkColor, getLightColor, blendTwoColors };
