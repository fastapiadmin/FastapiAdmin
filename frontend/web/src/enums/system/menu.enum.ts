// 核心枚举定义
export enum MenuTypeEnum {
  CATALOG = 1, // 目录
  MENU = 2, // 菜单
  BUTTON = 3, // 按钮
  EXTLINK = 4, // 外链
}

/** 菜单终端（与后端 sys_menu.client 一致） */
export enum MenuClientEnum {
  PC = "pc",
  APP = "app",
}
