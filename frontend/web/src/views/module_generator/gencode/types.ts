/** 预览文件树节点 */
export interface TreeNode {
  label: string;
  /** 仅文件节点：完整生成路径（相对项目根），用于展示 */
  full_path?: string;
  content?: string;
  children?: TreeNode[];
}
