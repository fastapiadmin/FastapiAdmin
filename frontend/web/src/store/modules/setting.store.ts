/**
 * 全局界面设置：布局、主题、页签、水印、工具栏显隐等；部分字段持久化（useStorage / persist）。
 * `reload` 翻转 `refresh` 布尔值，触发 `ArtPageContent` 重建 RouterView（与 useCommon.refresh 一致）。
 */
import { defineStore } from "pinia";
import { ref, computed, watch } from "vue";
import { MenuThemeType } from "@/types/store";
import AppConfig from "@/config";
import { SystemThemeEnum, MenuThemeEnum, MenuTypeEnum, ContainerWidthEnum } from "@/enums/appEnum";
import { SETTING_DEFAULT_CONFIG } from "@/config/setting";
import {
  setElementThemeColor,
  formatToDate,
  StorageConfig,
  applyTheme,
  generateThemeColors,
  toggleDarkMode,
  toggleSidebarColor,
} from "@utils";
import { SETTINGS_KEYS } from "@/constants";
import { useStorage } from "@vueuse/core";
import { defaultSettings } from "@/config/setting";
import { SidebarColor, ThemeMode } from "@/enums/settings/theme.enum";
import type { LayoutMode } from "@/enums/settings/layout.enum";
import type { Ref } from "vue";

export const useSettingsStore = defineStore(
  "settingStore",
  () => {
    // 菜单
    const menuType = ref(SETTING_DEFAULT_CONFIG.menuType);
    const menuOpenWidth = ref(SETTING_DEFAULT_CONFIG.menuOpenWidth);
    const menuOpen = ref(SETTING_DEFAULT_CONFIG.menuOpen);
    const dualMenuShowText = ref(SETTING_DEFAULT_CONFIG.dualMenuShowText);

    // 主题
    const systemThemeType = ref(SETTING_DEFAULT_CONFIG.systemThemeType);
    const systemThemeMode = ref(SETTING_DEFAULT_CONFIG.systemThemeMode);
    const menuThemeType = ref(SETTING_DEFAULT_CONFIG.menuThemeType);
    const systemThemeColor = ref(SETTING_DEFAULT_CONFIG.systemThemeColor);

    // 显示
    const showMenuButton = ref(SETTING_DEFAULT_CONFIG.showMenuButton);
    const showFastEnter = ref(SETTING_DEFAULT_CONFIG.showFastEnter);
    const showRefreshButton = ref(SETTING_DEFAULT_CONFIG.showRefreshButton);
    const showCrumbs = ref(SETTING_DEFAULT_CONFIG.showCrumbs);
    const showWorkTab = ref(SETTING_DEFAULT_CONFIG.showWorkTab);
    const showLanguage = ref(SETTING_DEFAULT_CONFIG.showLanguage);
    const showNprogress = ref(SETTING_DEFAULT_CONFIG.showNprogress);
    const showSettingGuide = ref(SETTING_DEFAULT_CONFIG.showSettingGuide);
    const showFestivalText = ref(SETTING_DEFAULT_CONFIG.showFestivalText);
    const watermarkVisible = ref(SETTING_DEFAULT_CONFIG.watermarkVisible);

    // 功能
    const autoClose = ref(SETTING_DEFAULT_CONFIG.autoClose);
    const uniqueOpened = ref(SETTING_DEFAULT_CONFIG.uniqueOpened);
    const colorWeak = ref(SETTING_DEFAULT_CONFIG.colorWeak);
    /** 供布局监听：`reload()` 取反以触发主内容区整页刷新 */
    const refresh = ref(SETTING_DEFAULT_CONFIG.refresh);
    const holidayFireworksLoaded = ref(SETTING_DEFAULT_CONFIG.holidayFireworksLoaded);

    // 样式
    const boxBorderMode = ref(SETTING_DEFAULT_CONFIG.boxBorderMode);
    const pageTransition = ref(SETTING_DEFAULT_CONFIG.pageTransition);
    const tabStyle = ref(SETTING_DEFAULT_CONFIG.tabStyle);
    const customRadius = ref(SETTING_DEFAULT_CONFIG.customRadius);
    const containerWidth = ref(SETTING_DEFAULT_CONFIG.containerWidth);

    // 节日
    const festivalDate = ref("");

    // 面板开关（非持久化）
    const settingsVisible = ref<boolean>(false);

    // 持久化（web-style：useStorage）
    const showTagsView = useStorage<boolean>(
      SETTINGS_KEYS.SHOW_TAGS_VIEW,
      defaultSettings.showTagsView
    );
    const showAppLogo = useStorage<boolean>(
      SETTINGS_KEYS.SHOW_APP_LOGO,
      defaultSettings.showAppLogo
    );
    const showWatermark = useStorage<boolean>(
      SETTINGS_KEYS.SHOW_WATERMARK,
      defaultSettings.showWatermark
    );
    const showSettings = useStorage<boolean>(
      SETTINGS_KEYS.SHOW_SETTINGS,
      defaultSettings.showSettings
    );
    const showGuide = useStorage<boolean>(SETTINGS_KEYS.SHOW_GUIDE, defaultSettings.showGuide);

    // 桌面端工具设置 - 持久化
    const showMenuSearch = useStorage<boolean>(
      SETTINGS_KEYS.SHOW_MENU_SEARCH,
      defaultSettings.showMenuSearch
    );
    const showFullscreen = useStorage<boolean>(
      SETTINGS_KEYS.SHOW_FULLSCREEN,
      defaultSettings.showFullscreen
    );
    const showSizeSelect = useStorage<boolean>(
      SETTINGS_KEYS.SHOW_SIZE_SELECT,
      defaultSettings.showSizeSelect
    );
    const showLangSelect = useStorage<boolean>(
      SETTINGS_KEYS.SHOW_LANG_SELECT,
      defaultSettings.showLangSelect
    );
    const showNotification = useStorage<boolean>(
      SETTINGS_KEYS.SHOW_NOTIFICATION,
      defaultSettings.showNotification
    );

    // 布局和主题设置 - 持久化
    const sidebarColorScheme = useStorage<string>(
      SETTINGS_KEYS.SIDEBAR_COLOR_SCHEME,
      defaultSettings.sidebarColorScheme
    );
    const layout = useStorage<LayoutMode>(
      SETTINGS_KEYS.LAYOUT,
      defaultSettings.layout as LayoutMode
    );
    const themeColor = useStorage<string>(SETTINGS_KEYS.THEME_COLOR, defaultSettings.themeColor);
    const theme = useStorage<ThemeMode>(SETTINGS_KEYS.THEME, defaultSettings.theme);

    // 系统设置 - 持久化
    const grayMode = useStorage<boolean>(SETTINGS_KEYS.GRAY_MODE, defaultSettings.grayMode);
    const userEnableAi = useStorage<boolean>(SETTINGS_KEYS.AI_ENABLED, defaultSettings.aiEnabled);
    const pageSwitchingAnimation = useStorage<string>(
      SETTINGS_KEYS.PAGE_SWITCHING_ANIMATION,
      defaultSettings.pageSwitchingAnimation
    );

    const getMenuTheme = computed((): MenuThemeType => {
      const list = AppConfig.themeList.filter((item) => item.theme === menuThemeType.value);
      if (isDark.value) {
        return AppConfig.darkMenuStyles[0];
      } else {
        return list[0];
      }
    });

    const isDark = computed((): boolean => {
      return systemThemeType.value === SystemThemeEnum.DARK;
    });

    const getMenuOpenWidth = computed((): string => {
      return (menuOpenWidth.value ?? SETTING_DEFAULT_CONFIG.menuOpenWidth) + "px";
    });

    const getCustomRadius = computed((): string => {
      return (customRadius.value ?? SETTING_DEFAULT_CONFIG.customRadius) + "rem";
    });

    /** festivalDate 存「上次完成烟花播放」的自然日 YYYY-MM-DD，与今天相同则当天不再播 */
    const isShowFireworks = computed((): boolean => {
      const today = formatToDate(new Date());
      return festivalDate.value !== today;
    });

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

    watch(
      [theme, themeColor],
      ([newTheme, newThemeColor]) => {
        try {
          toggleDarkMode(newTheme === ThemeMode.DARK);
          const colors = generateThemeColors(newThemeColor, newTheme);
          applyTheme(colors);
        } catch (error) {
          console.error("[SettingStore] 主题初始化失败:", error);
        }
      },
      { immediate: true }
    );

    watch(
      [sidebarColorScheme],
      ([newSidebarColorScheme]) => {
        toggleSidebarColor(newSidebarColorScheme === SidebarColor.CLASSIC_BLUE);
      },
      { immediate: true }
    );

    watch(
      grayMode,
      (v) => {
        document.documentElement.style.filter = v ? "grayscale(100%)" : "";
      },
      { immediate: true }
    );

    const switchMenuLayouts = (type: MenuTypeEnum) => {
      menuType.value = type;
    };

    const setMenuOpenWidth = (width: number) => {
      menuOpenWidth.value = width;
    };

    const setGlopTheme = (theme: SystemThemeEnum, themeMode: SystemThemeEnum) => {
      systemThemeType.value = theme;
      systemThemeMode.value = themeMode;
      localStorage.setItem(StorageConfig.THEME_KEY, theme);
    };

    const switchMenuStyles = (theme: MenuThemeEnum) => {
      menuThemeType.value = theme;
    };

    const setElementTheme = (theme: string) => {
      systemThemeColor.value = theme;
      setElementThemeColor(theme);
    };

    const setBorderMode = () => {
      boxBorderMode.value = !boxBorderMode.value;
    };

    const setContainerWidth = (width: ContainerWidthEnum) => {
      containerWidth.value = width;
    };

    const setUniqueOpened = () => {
      uniqueOpened.value = !uniqueOpened.value;
    };

    const setButton = () => {
      showMenuButton.value = !showMenuButton.value;
    };

    const setFastEnter = () => {
      showFastEnter.value = !showFastEnter.value;
    };

    const setAutoClose = () => {
      autoClose.value = !autoClose.value;
    };

    const setShowRefreshButton = () => {
      showRefreshButton.value = !showRefreshButton.value;
    };

    const setCrumbs = () => {
      showCrumbs.value = !showCrumbs.value;
    };

    const setWorkTab = (show: boolean) => {
      showWorkTab.value = show;
    };

    const setLanguage = () => {
      showLanguage.value = !showLanguage.value;
    };

    const setNprogress = () => {
      showNprogress.value = !showNprogress.value;
    };

    const setColorWeak = () => {
      colorWeak.value = !colorWeak.value;
    };

    const hideSettingGuide = () => {
      showSettingGuide.value = false;
    };

    const openSettingGuide = () => {
      showSettingGuide.value = true;
    };

    const setPageTransition = (transition: string) => {
      pageTransition.value = transition;
    };

    const setTabStyle = (style: string) => {
      tabStyle.value = style;
    };

    const setMenuOpen = (open: boolean) => {
      menuOpen.value = open;
    };

    /** 切换 `refresh`，驱动 `layouts/art-page-content` 内 `v-if="isRefresh"` 重建视图 */
    const reload = () => {
      refresh.value = !refresh.value;
    };

    const setWatermarkVisible = (visible: boolean) => {
      watermarkVisible.value = visible;
    };

    const setCustomRadius = (radius: string) => {
      customRadius.value = radius;
      document.documentElement.style.setProperty("--custom-radius", `${radius}rem`);
    };

    const setholidayFireworksLoaded = (isLoad: boolean) => {
      holidayFireworksLoaded.value = isLoad;
    };

    const setShowFestivalText = (show: boolean) => {
      showFestivalText.value = show;
    };

    const setFestivalDate = (date: string) => {
      festivalDate.value = date;
    };

    const setDualMenuShowText = (show: boolean) => {
      dualMenuShowText.value = show;
    };

    function updateSetting<K extends keyof typeof settingsMap>(
      key: K,
      value: boolean | string
    ): void {
      const setting = settingsMap[key];
      if (setting) {
        (setting as Ref<any>).value = value;
      }
    }

    function updateTheme(newTheme: ThemeMode): void {
      theme.value = newTheme;
    }

    function updateThemeColor(newColor: string): void {
      themeColor.value = newColor;
    }

    function updateSidebarColorScheme(newScheme: string): void {
      sidebarColorScheme.value = newScheme;
    }

    function updateLayout(newLayout: LayoutMode): void {
      layout.value = newLayout;
    }

    function toggleSettingsPanel(): void {
      settingsVisible.value = !settingsVisible.value;
    }

    function showSettingsPanel(): void {
      settingsVisible.value = true;
    }

    function hideSettingsPanel(): void {
      settingsVisible.value = false;
    }

    function updateUserEnableAi(newValue: boolean): void {
      userEnableAi.value = newValue;
    }

    function updateGrayMode(newValue: boolean): void {
      grayMode.value = newValue;
    }

    function updatePageSwitchingAnimation(newValue: string): void {
      pageSwitchingAnimation.value = newValue;
    }

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
      pageSwitchingAnimation.value = defaultSettings.pageSwitchingAnimation;
    }

    // ==============================================
    // 返回所有状态和方法
    // ==============================================

    return {
      // 从 setting.ts 来的状态
      menuType,
      menuOpenWidth,
      menuOpen,
      dualMenuShowText,
      systemThemeType,
      systemThemeMode,
      menuThemeType,
      systemThemeColor,
      showMenuButton,
      showFastEnter,
      showRefreshButton,
      showCrumbs,
      showWorkTab,
      showLanguage,
      showNprogress,
      showSettingGuide,
      showFestivalText,
      watermarkVisible,
      autoClose,
      uniqueOpened,
      colorWeak,
      refresh,
      holidayFireworksLoaded,
      boxBorderMode,
      pageTransition,
      tabStyle,
      customRadius,
      containerWidth,
      festivalDate,

      // 从 settings.store.ts 来的状态
      settingsVisible,
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
      themeColor,
      theme,
      grayMode,
      userEnableAi,
      pageSwitchingAnimation,

      // 计算属性
      getMenuTheme,
      isDark,
      getMenuOpenWidth,
      getCustomRadius,
      isShowFireworks,

      // 从 setting.ts 来的方法
      switchMenuLayouts,
      setMenuOpenWidth,
      setGlopTheme,
      switchMenuStyles,
      setElementTheme,
      setBorderMode,
      setContainerWidth,
      setUniqueOpened,
      setButton,
      setFastEnter,
      setAutoClose,
      setShowRefreshButton,
      setCrumbs,
      setWorkTab,
      setLanguage,
      setNprogress,
      setColorWeak,
      hideSettingGuide,
      openSettingGuide,
      setPageTransition,
      setTabStyle,
      setMenuOpen,
      reload,
      setWatermarkVisible,
      setCustomRadius,
      setholidayFireworksLoaded,
      setShowFestivalText,
      setFestivalDate,
      setDualMenuShowText,

      // 从 settings.store.ts 来的方法
      updateSetting,
      updateTheme,
      updateThemeColor,
      updateSidebarColorScheme,
      updateLayout,
      toggleSettingsPanel,
      showSettingsPanel,
      hideSettingsPanel,
      updateUserEnableAi,
      updateGrayMode,
      updatePageSwitchingAnimation,
      resetSettings,
    };
  },
  {
    persist: {
      key: "setting",
      storage: localStorage,
    },
  }
);
