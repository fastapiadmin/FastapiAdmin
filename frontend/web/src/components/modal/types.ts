import type {
  DialogProps,
  DrawerProps,
  FormItemRule,
  FormRules,
  PaginationProps,
} from "element-plus";
import type { FormProps, ColProps, ButtonProps, CardProps } from "element-plus";
import type CrudContent from "./CrudContent.vue";
import type CrudFormModal from "./CrudFormModal.vue";
import type CrudSearch from "./CrudSearch.vue";
import type { CSSProperties } from "vue";

export type CrudSearchInstance = InstanceType<typeof CrudSearch>;
export type CrudContentInstance = InstanceType<typeof CrudContent>;
export type CrudFormModalInstance = InstanceType<typeof CrudFormModal>;

/**
 * 通用对象类型
 */
export type IObject = Record<string, any>;

/**
 * 组件类型定义
 */
type DateComponent = "date-picker" | "time-picker" | "time-select" | "custom-tag" | "input-tag";
type InputComponent = "input" | "select" | "input-number" | "cascader" | "tree-select";
type OtherComponent =
  | "text"
  | "radio"
  | "checkbox"
  | "switch"
  | "rate"
  | "slider"
  | "icon-select"
  | "custom";
export type ISearchComponent =
  | DateComponent
  | InputComponent
  | "radio"
  | "checkbox"
  | "switch"
  | "rate"
  | "slider"
  /** 在 customComponents 中注册的自定义搜索控件类型 */
  | "user-table-select";
export type IComponentType = DateComponent | InputComponent | OtherComponent;

/**
 * 工具按钮类型定义
 */
type ToolbarLeft = "add" | "delete" | "patch";
type ToolbarRight = "refresh" | "filter" | "import" | "export";
type ToolbarTable = "edit" | "view" | "delete";

/**
 * 工具按钮接口
 */
export type IToolsButton = {
  /** 按钮名称 */
  name: string;
  /** 按钮文本 */
  text?: string;
  /** 权限标识(可以是完整权限字符串如'sys:user:add'或操作权限如'add') */
  perm?: Array<string> | string;
  /** 按钮属性 */
  attrs?: Partial<ButtonProps> & { style?: CSSProperties };
  /** 条件渲染 */
  render?: (row: IObject) => boolean;
  /** 按钮提示（支持字符串或Tooltip属性对象） */
  tooltip?: string | IObject;
};

/**
 * 工具按钮默认类型
 */
export type IToolsDefault = ToolbarLeft | ToolbarRight | ToolbarTable | IToolsButton;

/**
 * 操作数据接口
 */
export interface IOperateData {
  /** 操作名称 */
  name: string;
  /** 行数据 */
  row: IObject;
  /** 列数据 */
  column: IObject;
  /** 行索引 */
  $index: number;
}

/**
 * 搜索配置接口
 */
export interface ISearchConfig {
  /** 权限前缀(如sys:user，用于组成权限标识)，不提供则不进行权限校验 */
  permPrefix?: string;
  /** 标签冒号(默认：false) */
  colon?: boolean;
  /** 表单项(默认：[]) */
  formItems?: IFormItems<ISearchComponent>;
  /** 是否开启展开和收缩(默认：true) */
  isExpandable?: boolean;
  /** 默认展示的表单项数量(默认：3) */
  showNumber?: number;
  /** 卡片属性 */
  cardAttrs?: Partial<CardProps> & { style?: CSSProperties };
  /** form组件属性 */
  form?: IForm;
  /** 启用等宽网格布局；为 "right" 时操作按钮靠行末 */
  grid?: boolean | "left" | "right";
  /** 自定义组件映射 */
  customComponents?: Record<string, any>;
  /** 是否显示搜索按钮(默认：true) */
  showSearchButton?: boolean;
  /** 是否显示重置按钮(默认：true) */
  showResetButton?: boolean;
  /** 搜索按钮权限 */
  searchButtonPerm?: string | string[];
  /** 重置按钮权限 */
  resetButtonPerm?: string | string[];
  /**
   * 搜索区形态：与「高级表格」示例一致用 `art`（FaSearchBar + fa-card-xs）；
   * `grid` 等复杂布局仍走 `legacy`（或显式传 legacy）
   */
  searchVariant?: "legacy" | "art";
  /**
   * FaSearchBar `span`（不传则组件默认 6）。
   * 若需与 legacy `showNumber` 折叠条数对齐，可自行传入 `computeFaSearchSpan(showNumber)` 的结果。
   */
  artSearchSpan?: number;
  /** FaSearchBar `showExpand`（不传则 `isExpandable !== false`，否则与组件默认 true 一致） */
  artSearchShowExpand?: boolean;
  /** FaSearchBar 栅格 gutter（不传则用组件默认 12） */
  artSearchGutter?: number;
  /** art 搜索区默认展开全部筛选项（对应 FaSearchBar defaultExpanded） */
  searchDefaultExpanded?: boolean;
  /**
   * art 搜索区内控件最大宽度（不传则不限制，与 FaSearchBar 示例一致）。
   * 需要限制时再传，如 `"200px"`、`"min(100%, 280px)"`；`false` 显式铺满栅格列。
   */
  artSearchFieldMaxWidth?: string | false;
  /** 透传 FaSearchBar → ElForm.rules */
  artSearchRules?: FormRules;
  /** 透传 FaSearchBar `sanitizeOutput`，控制搜索提交前清洗空值等行为 */
  artSearchSanitizeOutput?: IObject;
  /** 透传 FaSearchBar `buttonLeftLimit`（表单项数 ≤ 该值时操作按钮靠左，默认 2） */
  artSearchButtonLeftLimit?: number;
  /** 透传 FaSearchBar `disabledSearch`，为 true 时禁用查询按钮 */
  artSearchDisabledSearch?: boolean;
  /**
   * 透传 FaSearchBar `isExpand`：为 true 时始终展示全部筛选项（不出现「展开更多」）。
   * 不传时：`isExpandable === false` 自动为 true（与 legacy 全展示一致）；可折叠搜索时为 false。
   */
  artSearchIsExpand?: boolean;
  /** 自定义按钮组 */
  customButtons?: Array<{
    /** 按钮唯一标识 */
    key: string;
    /** 按钮文本 */
    text: string;
    /** 按钮属性 */
    attrs?: IObject;
    /** 按钮权限 */
    perm?: string | string[];
    /** 点击事件处理函数 */
    handler?: (params: IObject, instance: any) => void;
  }>;
}

/**
 * 内容配置接口
 */
export interface IContentConfig<T = any> {
  /** 权限前缀(如sys:user，用于组成权限标识)，不提供则不进行权限校验 */
  permPrefix?: string;
  /** table组件属性（用 IObject 避免与 el-table TableProps.context 等内部类型不兼容） */
  table?: IObject;
  /** 页面标题与提示（用于卡片头部显示） */
  title?: string;
  /** 提示信息 */
  tooltip?: string | IObject;
  /** 分页组件位置(默认：left) */
  pagePosition?: "left" | "right";
  /** pagination组件属性 */
  pagination?:
    | boolean
    | Partial<
        Omit<
          PaginationProps,
          "v-model:page-size" | "v-model:current-page" | "total" | "currentPage"
        >
      >;
  /** 列表的网络请求函数(需返回promise) */
  indexAction: (queryParams: T) => Promise<any>;
  /**
   * 是否在挂载时立即请求列表（默认 true）。
   * 若需在父组件合并 CrudSearch 与额外条件后再请求，可设为 false，并在 onMounted 中自行调用 fetchPageData。
   */
  initialFetch?: boolean;
  /** 默认的分页相关的请求参数 */
  request?: {
    page_no: string;
    page_size: string;
  };
  /** 数据格式解析的回调函数 */
  parseData?: (res: any) => {
    total: number;
    list: IObject[];
    [key: string]: any;
  };
  /** 修改属性的网络请求函数(需返回promise) */
  modifyAction?: (data: {
    [key: string]: any;
    field: string;
    value: boolean | string | number;
  }) => Promise<any>;
  /** 删除的网络请求函数(需返回promise) */
  deleteAction?: (ids: string) => Promise<any>;
  /** 删除确认弹窗（不传则标题「警告」、内容「确认删除?」） */
  deleteConfirm?: {
    title?: string;
    message?: string;
    confirmButtonText?: string;
    cancelButtonText?: string;
    type?: "warning" | "info" | "success" | "error";
  };
  /** 后端导出的网络请求函数(需返回promise) */
  exportAction?: (queryParams: T) => Promise<any>;
  /** 前端全量导出的网络请求函数(需返回promise) */
  exportsAction?: (queryParams: T) => Promise<IObject[]>;
  /** 服务端导出 Excel 二进制（与 exportsAction 二选一用于「全量远程」导出） */
  exportsBlobAction?: (queryParams: T) => Promise<Blob>;
  /** 导入模板 */
  importTemplate?: string | (() => Promise<any>);
  /** 后端导入的网络请求函数(需返回promise) */
  importAction?: (file: File) => Promise<any>;
  /** 前端导入的网络请求函数(需返回promise) */
  importsAction?: (data: IObject[]) => Promise<any>;
  /** 主键名(默认为id) */
  pk?: string;
  /** 表格工具栏(默认:add,delete,export,也可自定义) */
  toolbar?: Array<ToolbarLeft | IToolsButton>;
  /**
   * 表格工具栏右侧图标（仅 **legacy** `el-table` 栈由 `CrudToolbarActions` 渲染）。
   * **tableVariant: 'art'** 时刷新/列设置等由 `FaTableHeader` 自带；导入导出请用 `#toolbar` 插槽自建。
   */
  defaultToolbar?: Array<ToolbarRight | IToolsButton>;
  /** 为 true 时隐藏 FaTableHeader「列筛选」按钮（默认 false，显示列筛选） */
  hideColumnFilter?: boolean;
  /**
   * 表格栈：`art` 时使用 FaTableHeader + FaTable；
   * `legacy` 为内置 el-table（默认）。
   */
  tableVariant?: "legacy" | "art";
  /** 内容区外层 el-card 额外 class（默认已含 `fa-table-card`） */
  cardClass?: string;
  /** el-card 阴影（默认 never，与 Element Plus el-card shadow 一致） */
  cardShadow?: "always" | "hover" | "never";
  /** 是否显示表格上方工具条（默认 true；纯卡片/无按钮时可设为 false） */
  showToolbar?: boolean;
  /** FaTableHeader 布局（不传则用内置默认） */
  artToolbarLayout?: string;
  /** 表格全屏区域 class，传给 FaTableHeader fullClass */
  artFullScreenClass?: string;
  /** 更多操作按钮配置 */
  moreButtons?: Array<IToolsButton>;
  /** table组件列属性(额外的属性templet,operat,slotName) */
  cols: Array<{
    /** 列类型 */
    type?: "default" | "selection" | "index" | "expand";
    /** 列标签 */
    label?: string;
    /** 列属性 */
    prop?: string;
    /** 列宽度 */
    width?: string | number;
    /** 最小列宽度 */
    minWidth?: string | number;
    /** 对齐方式 */
    align?: "left" | "center" | "right";
    /** 列键名 */
    columnKey?: string;
    /** 是否保留选择 */
    reserveSelection?: boolean;
    /** 列是否显示 */
    show?: boolean;
    /** 模板类型 */
    templet?:
      | "image"
      | "list"
      | "url"
      | "switch"
      | "input"
      | "price"
      | "percent"
      | "icon"
      | "date"
      | "tool"
      | "custom";
    /** image模板相关参数 */
    imageWidth?: number;
    /** image模板相关参数 */
    imageHeight?: number;
    /** list模板相关参数 */
    selectList?: IObject;
    /** switch模板相关参数 */
    activeValue?: boolean | string | number;
    /** switch模板相关参数 */
    inactiveValue?: boolean | string | number;
    /** switch模板相关参数 */
    activeText?: string;
    /** switch模板相关参数 */
    inactiveText?: string;
    /** input模板相关参数 */
    inputType?: string;
    /** price模板相关参数 */
    priceFormat?: string;
    /** date模板相关参数 */
    dateFormat?: string;
    /** tool模板相关参数 */
    operat?: Array<ToolbarTable | IToolsButton>;
    /** filter值拼接符 */
    filterJoin?: string;
    /** 初始化数据函数 */
    initFn?: (item: IObject) => void;
    /** 是否禁用 */
    disabled?: boolean;
    /** 固定列 */
    fixed?: boolean | "left" | "right";
    /** 权限 */
    perm?: string;
    [key: string]: any;
  }>;
}

/**
 * CrudContent 左侧 `createToolbar` 产物，供 CrudToolbarLeft 的 `configButtons` 使用。
 */
export type FaTableHeaderLeftConfigButton = {
  name: string;
  text?: string;
  attrs?: Record<string, unknown>;
  perm?: string | string[] | null;
};

/**
 * 模态框配置接口
 */
export interface IModalConfig<T = any> {
  /** 权限前缀(如sys:user，用于组成权限标识)，不提供则不进行权限校验 */
  permPrefix?: string;
  /** 标签冒号(默认：false) */
  colon?: boolean;
  /** 主键名(主要用于编辑数据,默认为id) */
  pk?: string;
  /** 组件类型(默认：dialog) */
  component?: "dialog" | "drawer";
  /** dialog组件属性（默认可拖拽；全屏由 core/overlays/FaDialog 标题栏按钮切换） */
  dialog?: Partial<Omit<DialogProps, "modelValue">> & { draggable?: boolean };
  /** drawer组件属性 */
  drawer?: Partial<Omit<DrawerProps, "modelValue">>;
  /** 查看模式渲染方式(默认：form；可选：descriptions) */
  viewMode?: "form" | "descriptions";
  /** descriptions组件属性（当 viewMode 为 descriptions 时生效） */
  descriptions?: IObject;
  /** form组件属性 */
  form?: IForm;
  /** 表单项 */
  formItems: IFormItems<IComponentType>;
  /** 提交之前处理 */
  beforeSubmit?: (data: T) => void;
  /** 提交的网络请求函数(需返回promise) */
  formAction?: (data: T) => Promise<any>;
}

/**
 * 表单属性类型
 */
export type IForm = Partial<Omit<FormProps, "model" | "rules">>;

/**
 * 表单项类型
 */
export type IFormItems<T = IComponentType> = Array<{
  /** 组件类型(如input,select,radio,custom等) */
  type: T;
  /** 标签提示 */
  tips?: string | IObject;
  /** 标签 */
  label: string;
  /** 属性名 */
  prop: string;
  /** 属性 */
  attrs?: IObject;
  /** 选项 */
  options?: Array<{ label: string; value: any; [key: string]: any }> | Ref<any[]>;
  /** 规则 */
  rules?: FormItemRule[];
  /** 初始值 */
  initialValue?: any;
  /** 插槽名称 */
  slotName?: string;
  /** 是否隐藏 */
  hidden?: boolean;
  /** 列属性 */
  col?: Partial<ColProps>;
  /** 事件 */
  events?: Record<string, (...args: any) => void>;
  /** 初始化函数 */
  initFn?: (item: IObject) => void;
}>;

/**
 * 页面表单接口
 */
export interface IPageForm {
  /** 主键 */
  pk?: string;
  /** 表单属性 */
  form?: IForm;
  /** 表单项 */
  formItems: IFormItems<IComponentType>;
}
