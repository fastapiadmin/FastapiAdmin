/** FaButtonMore 组件相关类型 */

export interface ButtonMoreItem {
  /** 按钮标识，可用于点击事件 */
  key: string | number;
  /** 按钮文本 */
  label: string;
  /** 是否禁用 */
  disabled?: boolean;
  /** 权限标识 */
  auth?: string;
  /** 图标组件 */
  icon?: string;
  /** 文本颜色 */
  color?: string;
  /** 图标颜色（优先级高于 color） */
  iconColor?: string;
}
