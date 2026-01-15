import { defaultSettings } from "@/settings";
import { SidebarColor, ThemeMode } from "@/enums/settings/theme.enum";
import type { LayoutMode } from "@/enums/settings/layout.enum";
import { applyTheme, generateThemeColors, toggleDarkMode, toggleSidebarColor } from "@/utils/theme";
import { SETTINGS_KEYS } from "@/constants";

// 🎯 设置项类型定义
interface SettingsState {
  // 界面显示设置
  settingsVisible: boolean;
  showTagsView: boolean;
  showAppLogo: boolean;
  showWatermark: boolean;
  showSettings: boolean;
  showGuide: boolean;

  // 桌面端工具显示设置
  showMenuSearch: boolean;
  showFullscreen: boolean;
  showSizeSelect: boolean;
  showLangSelect: boolean;
  showNotification: boolean;

  // 布局设置
  layout: LayoutMode;
  sidebarColorScheme: string;
  grayMode: boolean;
  userEnableAi: boolean;

  // 主题设置
  theme: ThemeMode;
  themeColor: string;
}

// 🎯 可变更的设置项类型
type MutableSetting = Exclude<keyof SettingsState, "settingsVisible">;
type SettingValue<K extends MutableSetting> = SettingsState[K];

export const useSettingsStore = defineStore("setting", () => {
  // 🎯 基础设置 - 非持久化
  const settingsVisible = ref<boolean>(false);

  // 🎯 界面显示设置 - 持久化
  const showTagsView = useStorage<boolean>(
    SETTINGS_KEYS.SHOW_TAGS_VIEW,
    defaultSettings.showTagsView
  );
  const showAppLogo = useStorage<boolean>(SETTINGS_KEYS.SHOW_APP_LOGO, defaultSettings.showAppLogo);
  // 是否显示水印
  const showWatermark = useStorage<boolean>(
    SETTINGS_KEYS.SHOW_WATERMARK,
    defaultSettings.showWatermark
  );

  // 是否显示系统设置
  const showSettings = useStorage<boolean>(
    SETTINGS_KEYS.SHOW_SETTINGS,
    defaultSettings.showSettings
  );

  // 是否显示引导功能
  const showGuide = useStorage<boolean>(SETTINGS_KEYS.SHOW_GUIDE, defaultSettings.showGuide); // 引导功能开关

  // 🎯 桌面端工具设置 - 持久化
  const showMenuSearch = useStorage<boolean>(
    SETTINGS_KEYS.SHOW_MENU_SEARCH,
    defaultSettings.showMenuSearch
  );

  // 是否显示全屏切换
  const showFullscreen = useStorage<boolean>(
    SETTINGS_KEYS.SHOW_FULLSCREEN,
    defaultSettings.showFullscreen
  );

  // 是否显示布局大小选择
  const showSizeSelect = useStorage<boolean>(
    SETTINGS_KEYS.SHOW_SIZE_SELECT,
    defaultSettings.showSizeSelect
  );

  // 是否显示语言选择
  const showLangSelect = useStorage<boolean>(
    SETTINGS_KEYS.SHOW_LANG_SELECT,
    defaultSettings.showLangSelect
  );

  // 是否显示通知
  const showNotification = useStorage<boolean>(
    SETTINGS_KEYS.SHOW_NOTIFICATION,
    defaultSettings.showNotification
  );

  // 🎯 布局和主题设置 - 持久化
  const sidebarColorScheme = useStorage<string>(
    SETTINGS_KEYS.SIDEBAR_COLOR_SCHEME,
    defaultSettings.sidebarColorScheme
  );

  // 布局设置
  const layout = useStorage<LayoutMode>(SETTINGS_KEYS.LAYOUT, defaultSettings.layout as LayoutMode);
  // 主题颜色
  const themeColor = useStorage<string>(SETTINGS_KEYS.THEME_COLOR, defaultSettings.themeColor);
  // 主题模式
  const theme = useStorage<ThemeMode>(SETTINGS_KEYS.THEME, defaultSettings.theme);

  // 是否开启灰色模式
  const grayMode = useStorage<boolean>(SETTINGS_KEYS.GRAY_MODE, defaultSettings.grayMode);
  // 是否开启AI助手
  const userEnableAi = useStorage<boolean>(SETTINGS_KEYS.AI_ENABLED, defaultSettings.aiEnabled);

  // 🎯 设置项映射
  const settingsMap = {
    showTagsView,
    showAppLogo,
    showWatermark,
    showSettings,
    showGuide,
    showMenuSearch,
    showFullscreen,
    showSizeSelect,
    showLangSelect,
    showNotification,
    sidebarColorScheme,
    layout,
    grayMode,
    userEnableAi,
  } as const;

  // 🎯 监听器 - 主题变化
  watch(
    [theme, themeColor],
    ([newTheme, newThemeColor]) => {
      toggleDarkMode(newTheme === ThemeMode.DARK);
      const colors = generateThemeColors(newThemeColor, newTheme);
      applyTheme(colors);
    },
    { immediate: true }
  );

  // 🎯 监听器 - 侧边栏配色方案变化
  watch(
    [sidebarColorScheme],
    ([newSidebarColorScheme]) => {
      toggleSidebarColor(newSidebarColorScheme === SidebarColor.CLASSIC_BLUE);
    },
    { immediate: true }
  );

  // 灰色模式监听
  watch(
    grayMode,
    (v) => {
      document.documentElement.style.filter = v ? "grayscale(100%)" : "";
    },
    { immediate: true }
  );

  // 🎯 统一的设置更新方法 - 类型安全
  function updateSetting<K extends keyof typeof settingsMap>(key: K, value: SettingValue<K>): void {
    const setting = settingsMap[key];
    if (setting) {
      (setting as Ref<any>).value = value;
    }
  }

  // 🎯 主题相关的专用更新方法
  function updateTheme(newTheme: ThemeMode): void {
    theme.value = newTheme;
  }

  // 更新主题颜色
  function updateThemeColor(newColor: string): void {
    themeColor.value = newColor;
  }

  // 更新侧边栏配色方案
  function updateSidebarColorScheme(newScheme: string): void {
    sidebarColorScheme.value = newScheme;
  }

  // 更新布局
  function updateLayout(newLayout: LayoutMode): void {
    layout.value = newLayout;
  }

  // 🎯 设置面板显示控制
  function toggleSettingsPanel(): void {
    settingsVisible.value = !settingsVisible.value;
  }

  // 显示设置面板
  function showSettingsPanel(): void {
    settingsVisible.value = true;
  }

  // 隐藏设置面板
  function hideSettingsPanel(): void {
    settingsVisible.value = false;
  }

  // 更新AI助手状态
  function updateUserEnableAi(newValue: boolean): void {
    userEnableAi.value = newValue;
  }

  // 更新灰色模式状态
  function updateGrayMode(newValue: boolean): void {
    grayMode.value = newValue;
  }

  // 🎯 批量重置设置
  function resetSettings(): void {
    // 界面显示设置
    showTagsView.value = defaultSettings.showTagsView;
    showAppLogo.value = defaultSettings.showAppLogo;
    showWatermark.value = defaultSettings.showWatermark;
    showSettings.value = defaultSettings.showSettings;
    showGuide.value = defaultSettings.showGuide;

    // 桌面端工具设置
    showMenuSearch.value = defaultSettings.showMenuSearch;
    showFullscreen.value = defaultSettings.showFullscreen;
    showSizeSelect.value = defaultSettings.showSizeSelect;
    showLangSelect.value = defaultSettings.showLangSelect;
    showNotification.value = defaultSettings.showNotification;

    // 布局和主题设置
    sidebarColorScheme.value = defaultSettings.sidebarColorScheme;
    layout.value = defaultSettings.layout as LayoutMode;
    themeColor.value = defaultSettings.themeColor;
    theme.value = defaultSettings.theme;

    // 系统设置
    grayMode.value = defaultSettings.grayMode;
    userEnableAi.value = defaultSettings.aiEnabled;
  }

  return {
    // 🎯 基础状态
    settingsVisible,

    // 🎯 界面显示状态
    showTagsView,
    showAppLogo,
    showWatermark,
    showSettings,
    showGuide,

    // 🎯 桌面端工具状态
    showMenuSearch,
    showFullscreen,
    showSizeSelect,
    showLangSelect,
    showNotification,

    // 🎯 布局和主题状态
    sidebarColorScheme,
    layout,
    themeColor,
    theme,

    // 🎯 更新方法
    updateSetting,
    updateTheme,
    updateThemeColor,
    updateSidebarColorScheme,
    updateLayout,

    // 🎯 面板控制
    toggleSettingsPanel,
    showSettingsPanel,
    hideSettingsPanel,

    // 🎯 系统设置状态
    grayMode,
    userEnableAi,

    // 🎯 更新系统设置方法
    updateUserEnableAi,
    updateGrayMode,

    // 🎯 重置功能
    resetSettings,
  };
});
