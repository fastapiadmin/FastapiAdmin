/**
 * 存储键名常量
 *
 * @description
 * 统一管理所有 localStorage/sessionStorage 的键名
 * 命名规则：{APP_PREFIX}:{分类}:{具体名称}
 */

// 🔐 用户认证相关
export const ACCESS_TOKEN_KEY = "access_token";
export const REFRESH_TOKEN_KEY = "refresh_token";
export const REMEMBER_ME_KEY = "remember_me";

// 📊 数据缓存相关
export const DICT_CACHE_KEY = "dict_cache";

// 🎨 系统设置相关
export const SHOW_TAGS_VIEW_KEY = "showTagsView";
export const SHOW_APP_LOGO_KEY = "showAppLogo";
export const SHOW_WATERMARK_KEY = "showWatermark";
export const SHOW_SETTINGS_KEY = "showSettings";
export const SHOW_MENU_SEARCH_KEY = "showMenuSearch";
export const SHOW_FULLSCREEN_KEY = "showFullscreen";
export const SHOW_SIZE_SELECT_KEY = "showSizeSelect";
export const SHOW_LANG_SELECT_KEY = "showLangSelect";
export const SHOW_NOTIFICATION_KEY = "showNotification";
export const SHOW_GUIDE_KEY = "showGuide"; // 引导功能开关
export const LAYOUT_KEY = "layout";
export const SIDEBAR_COLOR_SCHEME_KEY = "sidebarColorScheme";
export const THEME_KEY = "theme";
export const THEME_COLOR_KEY = "themeColor";
export const GRAY_MODE_KEY = "grayMode";
export const AI_ENABLED_KEY = "aiEnabled";
export const PAGE_SWITCHING_ANIMATION_KEY = "pageSwitchingAnimation";

export const ROLE_ROOT = "ADMIN"; // 超级管理员角色

// 🎯 功能分组的键映射对象

// 认证相关键集合
export const AUTH_KEYS = {
  ACCESS_TOKEN: ACCESS_TOKEN_KEY,
  REFRESH_TOKEN: REFRESH_TOKEN_KEY,
  REMEMBER_ME: REMEMBER_ME_KEY,
} as const;

// 缓存相关键集合
export const CACHE_KEYS = {
  DICT_CACHE: DICT_CACHE_KEY,
} as const;

// 设置相关键集合
export const SETTINGS_KEYS = {
  SHOW_TAGS_VIEW: SHOW_TAGS_VIEW_KEY,
  SHOW_APP_LOGO: SHOW_APP_LOGO_KEY,
  SHOW_WATERMARK: SHOW_WATERMARK_KEY,
  SHOW_SETTINGS: SHOW_SETTINGS_KEY,
  SHOW_MENU_SEARCH: SHOW_MENU_SEARCH_KEY,
  SHOW_FULLSCREEN: SHOW_FULLSCREEN_KEY,
  SHOW_SIZE_SELECT: SHOW_SIZE_SELECT_KEY,
  SHOW_LANG_SELECT: SHOW_LANG_SELECT_KEY,
  SHOW_NOTIFICATION: SHOW_NOTIFICATION_KEY,
  SHOW_GUIDE: SHOW_GUIDE_KEY,
  SIDEBAR_COLOR_SCHEME: SIDEBAR_COLOR_SCHEME_KEY,
  LAYOUT: LAYOUT_KEY,
  THEME_COLOR: THEME_COLOR_KEY,
  THEME: THEME_KEY,
  GRAY_MODE: GRAY_MODE_KEY,
  AI_ENABLED: AI_ENABLED_KEY,
  PAGE_SWITCHING_ANIMATION: PAGE_SWITCHING_ANIMATION_KEY,
} as const;

// 📦 所有存储键的统一集合
export const ALL_STORAGE_KEYS = {
  ...AUTH_KEYS,
  ...CACHE_KEYS,
  ...SETTINGS_KEYS,
} as const;
