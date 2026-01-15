declare global {
  /**
   * 响应数据
   */
  interface ApiResponse<T = any> {
    code: number;
    data: T;
    msg: string;
    status_code: number;
    success: boolean;
  }

  /**
   * 分页查询参数
   */
  interface PageQuery {
    /** 当前页码 */
    page_no: number;
    /** 每页条数 */
    page_size: number;
  }

  /**
   * 分页响应对象
   */
  interface PageResult<T> {
    /** 数据列表 */
    items: T;
    /** 总数 */
    total: number;
    page_no: number;
    page_size: number;
    has_next: boolean;
  }

  /**
   * 页签对象
   */
  interface TagView {
    /** 页签名称 */
    name: string;
    /** 页签标题 */
    title: string;
    /** 页签路由路径 */
    path: string;
    /** 页签路由完整路径 */
    fullPath: string;
    /** 页签图标 */
    icon?: string;
    /** 是否固定页签 */
    affix?: boolean;
    /** 是否开启缓存 */
    keepAlive?: boolean;
    /** 路由查询参数 */
    query?: any;
  }

  /**
   * 系统设置
   */
  interface AppSettings {
    /** 系统名称 */
    name: string;
    /** 系统标题 */
    title: string;
    /** 系统版本 */
    version: string;
    /** 是否显示设置按钮 */
    showSettings: boolean;
    /** 是否显示菜单搜索 */
    showMenuSearch: boolean;
    /** 是否显示全屏切换 */
    showFullscreen: boolean;
    /** 是否显示布局大小 */
    showSizeSelect: boolean;
    /** 是否显示语言选择 */
    showLangSelect: boolean;
    /** 是否显示通知 */
    showNotification: boolean;
    /** 是否显示多标签导航 */
    showTagsView: boolean;
    /** 是否显示应用Logo */
    showAppLogo: boolean;
    /** 导航栏布局(left|top|mix) */
    layout: "left" | "top" | "mix";
    /** 主题颜色 */
    themeColor: string;
    /** 主题模式(dark|light) */
    theme: import("@/enums/settings/theme.enum").ThemeMode;
    /** 布局大小(default |large |small) */
    size: string;
    /** 语言( zh-cn| en) */
    language: string;
    /** 是否显示水印 */
    showWatermark: boolean;
    /** 水印内容 */
    watermarkContent: string;
    /** 侧边栏配色方案 */
    sidebarColorScheme: "classic-blue" | "minimal-white";
    /** 项目引导 */
    guideVisible: boolean;
    /** 是否启动引导 */
    showGuide: boolean;
    /** 是否开启AI助手 */
    aiEnabled: boolean;
    /** 是否开启灰色模式 */
    grayMode: boolean;
  }

  /**
   * 下拉选项数据类型
   */
  interface OptionType {
    /** 值 */
    value: string | number;
    /** 文本 */
    label: string;
    /** 子列表  */
    children?: OptionType[];
  }

  /**
   * 导入结果
   */
  interface ExcelResult {
    /** 状态码 */
    code: string;
    /** 无效数据条数 */
    invalidCount: number;
    /** 有效数据条数 */
    validCount: number;
    /** 错误信息 */
    messageList: Array<string>;
  }

  /**
   * 创建人
   */
  interface CommonType {
    id?: number;
    name?: string;
  }

  /**
   * 基础类型
   */
  interface BaseType {
    index?: number;
    id?: number;
    uuid?: string;
    status?: string;
    description?: string;
    created_time?: string;
    updated_time?: string;
  }

  /**
   * 基础类型
   */
  interface BaseFormType {
    id?: number;
    status?: string;
    description?: string;
  }

  /**
   * 上传文件返回
   */
  interface UploadFilePath {
    file_path: string;
    file_name: string;
    origin_name: string;
    file_url: string;
  }

  /**
   * 批量启用、停用
   */
  export interface BatchType {
    ids?: number[];
    status?: string;
  }
}
export {};
