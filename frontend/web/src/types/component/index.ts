/** 搜索组件类型 */
export type SearchComponentType =
  | "input"
  | "select"
  | "radio"
  | "checkbox"
  | "date"
  | "datetime"
  | "daterange"
  | "datetimerange"
  | "month"
  | "monthrange"
  | "year"
  | "yearrange"
  | "week"
  | "time"
  | "timerange";

/** 搜索框值变化参数 */
export interface SearchChangeParams {
  prop: string;
  val: unknown;
}

/** 状态列配置（自动渲染 StatusTag） */
export interface StatusColumnItem {
  type: "primary" | "success" | "warning" | "danger" | "info";
  text: string;
  size?: "large" | "default" | "small";
  effect?: "light" | "dark" | "plain";
}

/** 部分映射：只需列出需要配置的值对应的状态项 */
export type StatusColumnConfig = Partial<Record<string, StatusColumnItem>>;

/** 表格列配置接口 */
export interface ColumnOption<T = any> {
  type?: "selection" | "expand" | "index" | "globalIndex";
  prop?: string;
  label?: string;
  width?: string | number;
  minWidth?: string | number;
  fixed?: boolean | "left" | "right";
  sortable?: boolean | "custom";
  filters?: any[];
  filterMethod?: (value: any, row: any) => boolean;
  filterPlacement?: string;
  disabled?: boolean;
  visible?: boolean;
  checked?: boolean;
  formatter?: (row: T) => any;
  status?: StatusColumnConfig;
  useSlot?: boolean;
  slotName?: string;
  useHeaderSlot?: boolean;
  headerSlotName?: string;
  [key: string]: any;
}

/** 分页配置 */
export interface PaginationConfig {
  currentPage: number;
  pageSize: number;
  total: number;
  pageSizes?: number[];
  layout?: string;
  small?: boolean;
}

/** 表单规则 */
export interface FormRule {
  required?: boolean;
  message?: string;
  trigger?: string | string[];
  min?: number;
  max?: number;
  pattern?: RegExp;
  validator?: (rule: any, value: any, callback: any) => void;
}

/** 对话框配置 */
export interface DialogConfig {
  title: string;
  visible: boolean;
  width?: string | number;
  closeOnClickModal?: boolean;
  closeOnPressEscape?: boolean;
  showClose?: boolean;
  lockScroll?: boolean;
  modal?: boolean;
  customClass?: string;
}
