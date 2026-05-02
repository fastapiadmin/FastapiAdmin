/**
 * 系统设置默认值配置
 *
 * 统一管理系统设置的所有默认值
 *
 * ## 主要功能
 *
 * - 菜单相关默认配置
 * - 主题相关默认配置
 * - 界面显示默认配置
 * - 功能开关默认配置
 * - 样式相关默认配置
 *
 * ## 注意事项
 *
 * 1. 修改此文件的配置项时，需要同步更新以下文件：
 *    - src/components/core/layouts/art-settings-panel/widget/SettingActions.vue（复制配置和重置配置逻辑）
 *    - src/store/modules/setting.ts（Store 状态定义）
 * 2. 可以通过设置面板的"复制配置"按钮快速生成配置代码
 * 3. 枚举类型的值需要与 src/enums/appEnum.ts 中的定义保持一致
 */

import AppConfig from "@/config";
import { SystemThemeEnum, MenuThemeEnum, MenuTypeEnum, ContainerWidthEnum } from "@/enums/appEnum";
import { LayoutMode, ComponentSize, SidebarColor, ThemeMode, LanguageEnum } from "@/enums";

const env = import.meta.env;
const { pkg } = __APP_INFO__;

// 检查用户的操作系统是否使用深色模式
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

/**
 * 系统设置默认值配置
 */
export const SETTING_DEFAULT_CONFIG = {
  /** 项目名称 */
  name: pkg.name as string,
  /** 系统标题 */
  title: (env.VITE_APP_TITLE as string) || pkg.name,
  /** 系统版本 */
  version: pkg.version as string,
  /** 是否显示设置按钮 */
  showSettings: true,
  /** 是否显示菜单搜索 */
  showMenuSearch: true,
  /** 是否显示全屏按钮 */
  showFullscreen: true,
  /** 是否显示尺寸选择 */
  showSizeSelect: true,
  /** 是否显示语言选择 */
  showLangSelect: true,
  /** 是否显示通知 */
  showNotification: true,
  /** 是否显示标签视图 */
  showTagsView: true,
  /** 是否显示应用Logo */
  showAppLogo: true,
  /** 布局方式 */
  layout: LayoutMode.LEFT,
  /** 主题模式 */
  theme: prefersDark ? ThemeMode.DARK : ThemeMode.LIGHT,
  /** 组件大小 */
  size: ComponentSize.DEFAULT,
  /** 语言 */
  language: LanguageEnum.ZH_CN,
  /** 主题颜色 */
  themeColor: "#4080FF",
  /** 是否显示水印 */
  showWatermark: false,
  /** 水印内容 */
  watermarkContent: pkg.name,
  /** 侧边栏配色方案 */
  sidebarColorScheme: SidebarColor.CLASSIC_BLUE,
  /** 项目引导可见性 */
  guideVisible: false,
  /** 是否启动引导 */
  showGuide: true,
  /** 是否开启AI助手 */
  aiEnabled: false,
  /** 是否开启灰色模式 */
  grayMode: false,
  /** 页面切换动画 */
  pageSwitchingAnimation: "fade-slide",

  // === 新版本原有字段 ===

  /** 菜单类型 */
  menuType: MenuTypeEnum.LEFT,
  /** 菜单展开宽度 */
  menuOpenWidth: 230,
  /** 菜单是否展开 */
  menuOpen: true,
  /** 双菜单是否显示文本 */
  dualMenuShowText: false,
  /** 系统主题类型 */
  systemThemeType: SystemThemeEnum.AUTO,
  /** 系统主题模式 */
  systemThemeMode: SystemThemeEnum.AUTO,
  /** 菜单风格 */
  menuThemeType: MenuThemeEnum.DESIGN,
  /** 系统主题颜色 */
  systemThemeColor: AppConfig.systemMainColor[0],
  /** 是否显示菜单按钮 */
  showMenuButton: true,
  /** 是否显示快速入口 */
  showFastEnter: true,
  /** 是否显示刷新按钮 */
  showRefreshButton: true,
  /** 是否显示面包屑 */
  showCrumbs: true,
  /** 是否显示工作台标签 */
  showWorkTab: true,
  /** 是否显示语言切换 */
  showLanguage: true,
  /** 是否显示进度条 */
  showNprogress: false,
  /** 是否显示设置引导 */
  showSettingGuide: true,
  /** 是否显示节日文本 */
  showFestivalText: false,
  /** 是否显示水印（新版本字段） */
  watermarkVisible: false,
  /** 是否自动关闭 */
  autoClose: false,
  /** 是否唯一展开 */
  uniqueOpened: true,
  /** 是否色弱模式 */
  colorWeak: false,
  /** 是否刷新 */
  refresh: false,
  /** 是否加载节日烟花 */
  holidayFireworksLoaded: false,
  /** 边框模式 */
  boxBorderMode: true,
  /** 页面过渡效果 */
  pageTransition: "slide-left",
  /** 标签页样式 */
  tabStyle: "tab-default",
  /** 自定义圆角 */
  customRadius: "0.75",
  /** 容器宽度 */
  containerWidth: ContainerWidthEnum.FULL,
  /** 节日日期 */
  festivalDate: "",
};

/** 与 Store / App 中使用的默认设置别名（同 SETTING_DEFAULT_CONFIG） */
export const defaultSettings = SETTING_DEFAULT_CONFIG;

/**
 * 获取设置默认值
 * @returns 设置默认值对象
 */
export function getSettingDefaults() {
  return { ...SETTING_DEFAULT_CONFIG };
}

/**
 * 重置为默认设置
 * @param currentSettings 当前设置对象
 */
export function resetToDefaults(currentSettings: Record<string, any>) {
  const defaults = getSettingDefaults();
  Object.keys(defaults).forEach((key) => {
    if (key in currentSettings) {
      currentSettings[key] = defaults[key as keyof typeof defaults];
    }
  });
}

// 主题色预设 - 现代化配色方案
// 注意：修改默认主题色时，需要同步修改 src/styles/variables.scss 中的 primary.base 值
export const themeColorPresets = [
  // === 精选常用颜色 - 多样化色系 ===
  "#4080FF", // Arco Design 蓝 - 现代感强
  "#52C41A", // 成功绿 - 活力清新
  "#722ED1", // 优雅紫 - 高端大气
  "#FA8C16", // 活力橙 - 温暖友好
  "#13C2C2", // 青色 - 科技感
  "#F5222D", // 警示红 - 醒目强烈
  "#EB2F96", // 品红 - 时尚个性
  "#EC4899", // 玫瑰粉 - 浪漫温馨
  "#10B981", // 翠绿色 - 清新自然

  // === 蓝色系 - 科技与专业 ===
  "#409EFF", // Element Plus 蓝 - 清新自然
  "#2F54EB", // 深蓝 - 稳重专业
  "#1E40AF", // 深蓝色 - 商务精英
  "#1D4ED8", // 皇家蓝 - 高端商务

  // === 绿色系 - 自然与活力 ===
  "#10B981", // 翠绿色 - 清新自然
  "#059669", // 森林绿 - 生态环保
  "#16A34A", // 草绿色 - 健康活力
  "#15803D", // 深绿色 - 稳重大气

  // === 紫色系 - 创意与优雅 ===
  "#7C3AED", // 紫罗兰 - 创意无限
  "#8B5CF6", // 浅紫色 - 时尚现代
  "#6D28D9", // 深紫色 - 神秘高端
  "#5B21B6", // 皇家紫 - 王者风范

  // === 橙色系 - 温暖与活力 ===
  "#F97316", // 火橙色 - 热情奔放
  "#EA580C", // 深橙色 - 阳光活力
  "#DC2626", // 珊瑚红 - 温暖亲切

  // === 青色系 - 科技与清新 ===
  "#0891B2", // 天蓝色 - 清新自然
  "#0E7490", // 深青色 - 专业科技
  "#06B6D4", // 青蓝色 - 海洋清新

  // === 红色系 - 激情与警示 ===
  "#DC2626", // 猩红色 - 激情四射
  "#B91C1C", // 深红色 - 庄重严肃

  // === 粉色系 - 温柔与时尚 ===
  "#EC4899", // 玫瑰粉 - 浪漫温馨
  "#F472B6", // 浅粉色 - 柔美可爱

  // === 灰色系 - 简约与现代 ===
  "#6B7280", // 经典灰 - 简约现代
  "#4B5563", // 深灰色 - 商务专业
  "#374151", // 石板灰 - 高端商务
];
