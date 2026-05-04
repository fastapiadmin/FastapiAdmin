import { AppRouteRecord } from "@/types/router";

/** Art 模板自带演示路由：与后端「系统管理」路径隔离，避免合并时被覆盖或冲突 */
export const systemRoutes: AppRouteRecord = {
  path: "/art-system",
  name: "ArtSystem",
  component: "/index/index",
  meta: {
    title: "menus.system.title",
    icon: "ri:user-3-line",
  },
  children: [
    {
      path: "user",
      name: "ArtTplUser",
      component: "/system/user",
      meta: {
        title: "menus.system.user",
        icon: "ri:user-line",
        keepAlive: true,
      },
    },
    {
      path: "role",
      name: "ArtTplRole",
      component: "/system/role",
      meta: {
        title: "menus.system.role",
        icon: "ri:user-settings-line",
        keepAlive: true,
      },
    },
    {
      path: "menu",
      name: "ArtTplMenus",
      component: "/system/menu",
      meta: {
        title: "menus.system.menu",
        icon: "ri:menu-line",
        keepAlive: true,
        authList: [
          { title: "新增", authMark: "add" },
          { title: "编辑", authMark: "edit" },
          { title: "删除", authMark: "delete" },
        ],
      },
    },
  ],
};
