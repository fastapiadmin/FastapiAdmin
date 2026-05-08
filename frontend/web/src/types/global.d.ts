declare global {
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
    /** 页面切换动画 */
    pageSwitchingAnimation: string;
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
   * 基础响应结构
   */
  interface ApiResponse<T = any> {
    code: number;
    data: T;
    msg: string;
    status_code: number;
    success: boolean;
  }

  /**
   * 兼容 web 工程遗留的 `Api.*` 命名空间类型引用
   * web 目前以真实接口模块导出的类型为准，这里先提供最小声明避免 vue-tsc 阻断。
   */
  namespace Api {
    namespace Auth {
      interface UserInfo {
        [key: string]: unknown;
      }
    }
  }

  /**
   * 分页查询参数
   */
  interface PageQuery {
    page_no: number;
    page_size: number;
  }

  /**
   * 分页响应对象
   */
  interface PageResult<T = any> {
    items: T[];
    total: number;
    page_no: number;
    page_size: number;
    has_next: boolean;
  }

  /**
   * 创建人
   */
  interface CommonType {
    id?: number;
    name?: string;
  }

  /**
   * 租户
   */
  interface TenantType {
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
    deleted_time?: string;
    deleted_id?: number;
  }

  /**
   * 基础表单类型
   */
  interface BaseFormType {
    id?: number;
    status?: string;
    description?: string;
    remark?: string;
    order?: number;
  }

  /**
   * 批量操作类型
   */
  interface BatchType {
    ids: number[];
    status: string;
  }

  /**
   * 上传文件路径
   */
  interface UploadFilePath {
    file_path: string;
    file_name: string;
    origin_name: string;
    file_url: string;
  }

  /**
   * 通用搜索参数
   */
  type CommonSearchParams = Pick<PageQuery, "page_no" | "page_size">;

  /**
   * 启用状态
   */
  type EnableStatus = "0" | "1";

  /**
   * 登录参数
   */
  interface LoginParams {
    username: string;
    password: string;
    captcha_key?: string;
    captcha?: string;
    remember?: boolean;
    login_type?: string;
  }

  /**
   * 登录响应
   */
  interface LoginResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
    expires_in: number;
  }

  /**
   * 用户信息
   */
  interface UserInfo {
    user_id: number;
    username: string;
    nickname?: string;
    email?: string;
    avatar?: string;
    phone?: string;
    roles?: RoleInfo[];
    permissions?: string[];
    menus?: MenuTable[];
    created_at?: string;
    updated_at?: string;
  }

  /**
   * 角色信息
   */
  interface RoleInfo {
    id?: number;
    name?: string;
    code?: string;
    menus?: any[];
  }

  /**
   * 验证码信息
   */
  interface CaptchaInfo {
    enable: boolean;
    key: string;
    img_base: string;
  }

  /**
   * 用户列表
   */
  type UserList = PageResult<UserListItem>;

  /**
   * 用户列表项
   */
  interface UserListItem {
    id: number;
    avatar: string;
    status: string;
    userName: string;
    userGender: string;
    nickName: string;
    userPhone: string;
    userEmail: string;
    userRoles: string[];
    createBy: string;
    createTime: string;
    updateBy: string;
    updateTime: string;
  }

  /**
   * 用户搜索参数
   */
  type UserSearchParams = Partial<
    Pick<UserListItem, "id" | "userName" | "userGender" | "userPhone" | "userEmail" | "status"> &
      CommonSearchParams
  >;

  /**
   * 角色列表
   */
  type RoleList = PaginatedResponse<RoleListItem>;

  /**
   * 角色列表项
   */
  interface RoleListItem {
    roleId: number;
    roleName: string;
    roleCode: string;
    description: string;
    enabled: boolean;
    createTime: string;
  }

  /**
   * 角色搜索参数
   */
  type RoleSearchParams = Partial<
    Pick<RoleListItem, "roleId" | "roleName" | "roleCode" | "description" | "enabled"> &
      CommonSearchParams & {
        startTime: string | null;
        endTime: string | null;
      }
  >;
}

export {};
