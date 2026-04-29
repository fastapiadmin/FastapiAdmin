import { LayoutMode, ComponentSize, SidebarColor, ThemeMode, LanguageEnum } from "./enums";

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
  themeColor: "#4080FF",
  // 是否显示水印 (修改默认开启水印)
  showWatermark: false,
  // 水印内容
  watermarkContent: pkg.name,
  // 侧边栏配色方案
  sidebarColorScheme: SidebarColor.CLASSIC_BLUE,
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
