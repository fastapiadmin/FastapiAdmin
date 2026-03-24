import { LayoutMode, ComponentSize, ThemeMode, LanguageEnum } from "./enums";

const env = import.meta.env;
const { pkg } = __APP_INFO__;

// 检查用户的操作系统是否使用深色模式
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

export const defaultSettings: AppSettings = {
  name: pkg.name as string,
  // 系统Title
  title: (env.VITE_APP_TITLE as string) || pkg.name,
  // 系统版本
  version: pkg.version as string,
  // 是否显示设置按钮
  showSettings: true,
  // 桌面端工具项单独控制
  showMenuSearch: true,
  showFullscreen: true,
  showSizeSelect: true,
  showLangSelect: true,
  // 是否显示通知
  showNotification: true,
  // 是否显示标签视图
  showTagsView: true,
  // 是否显示应用Logo
  showAppLogo: true,
  // 布局方式，默认为左侧布局
  layout: LayoutMode.LEFT,
  // 主题，根据操作系统的色彩方案自动选择
  theme: prefersDark ? ThemeMode.DARK : ThemeMode.LIGHT,
  // 组件大小 default | medium | small | large
  size: ComponentSize.DEFAULT,
  // 语言
  language: LanguageEnum.ZH_CN,
  // 主题颜色 - 修改此值时需同步修改 src/styles/variables.scss
  themeColor: "#3b82f6",
  // 是否显示水印 (修改默认开启水印)
  showWatermark: false,
  // 水印内容
  watermarkContent: pkg.name,
  // 项目引导
  guideVisible: false,
  /** 是否启动引导 */
  showGuide: true,
  /** 是否开启AI助手 */
  aiEnabled: false,
  /** 是否开启灰色模式 */
  grayMode: false,
  /** 页面切换动画 */
  pageSwitchingAnimation: "fade-slide",
};

/**
 * 主题色预设 - 现代化配色方案
 *
 * 设计原则：
 * 1. 颜色分类：按色系分组，便于用户选择
 * 2. 深浅搭配：每个色系提供浅、中、深三种选择
 * 3. 视觉协调：所有颜色都经过视觉测试，确保在不同主题下都有良好表现
 *
 * 注意：修改默认主题色时，需要同步修改以下文件：
 * - src/styles/variables.scss
 * - src/styles/theme/element-light.scss
 * - src/styles/theme/element-dark.scss
 */
export const themeColorPresets = [
  // ==================== 精选推荐 - 最受欢迎的颜色 ====================
  "#3b82f6", // 现代蓝 - 默认主题色，专业稳重
  "#5dc0ff", // 淡蓝色 - 清新明亮，亮暗主题皆宜
  "#10b981", // 翡翠绿 - 清新自然，活力健康
  "#8b5cf6", // 紫罗兰 - 创意优雅，现代时尚
  "#f59e0b", // 琥珀橙 - 温暖活力，积极向上
  "#06b6d4", // 青蓝色 - 科技清新，年轻活力
  "#ef4444", // 鲜红色 - 醒目强烈，热情奔放
  "#ec4899", // 玫瑰粉 - 浪漫温馨，时尚个性
  "#34d399", // 浅绿色 - 清新明亮，生机盎然
];
