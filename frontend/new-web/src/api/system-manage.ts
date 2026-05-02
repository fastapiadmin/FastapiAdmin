/**
 * 系统管理相关聚合接口（表格示例、views/system/* 等使用的 `@/api/system-manage`）
 * 内部委托至 `module_system` 下各 API，并做分页字段与行展示字段映射。
 */
import MenuAPI, { type MenuTable } from "@/api/module_system/menu";
import RoleAPI, { type RoleTable, type TablePageQuery } from "@/api/module_system/role";
import UserAPI, { type UserInfo, type UserPageQuery } from "@/api/module_system/user";
import type { AppRouteRecord } from "@/types/router";
import { ResultEnum } from "@/enums/api/result.enum";

function assertSuccess<T>(res: { data: ApiResponse<T> }, fallbackMsg: string): T {
  if (res.data.code !== ResultEnum.SUCCESS || res.data.data == null) {
    throw new Error(res.data.msg || fallbackMsg);
  }
  return res.data.data;
}

/** useTable 传入 current / size 及演示页自定义筛选字段 */
export async function fetchGetUserList(params: Record<string, unknown>) {
  const q: UserPageQuery = {
    page_no: Number(params.current) || 1,
    page_size: Number(params.size) || 20,
    username: (params.userName ?? params.name) as string | undefined,
    name: params.name as string | undefined,
    mobile: (params.userPhone ?? params.phone) as string | undefined,
    email: (params.userEmail ?? params.email) as string | undefined,
    status: params.status as string | undefined,
  };

  const res = await UserAPI.listUser(q);
  const page = assertSuccess(res, "获取用户列表失败");

  const items = (page.items || []).map((u) => mapUserToListRow(u));

  return {
    items,
    total: page.total,
    page_no: page.page_no,
    page_size: page.page_size,
    has_next: page.has_next,
  };
}

function mapUserToListRow(u: UserInfo) {
  return {
    id: u.id,
    nickName: u.name ?? u.username,
    userName: u.username,
    userGender: u.gender,
    userPhone: u.mobile,
    userEmail: u.email,
    avatar: u.avatar,
    status: u.status,
  };
}

export async function fetchGetRoleList(params: Record<string, unknown>) {
  const q: TablePageQuery = {
    page_no: Number(params.current) || 1,
    page_size: Number(params.size) || 20,
    name: params.roleName as string | undefined,
    status:
      params.enabled !== undefined && params.enabled !== null && params.enabled !== ""
        ? String(params.enabled)
        : undefined,
  };

  const res = await RoleAPI.listRole(q);
  const page = assertSuccess(res, "获取角色列表失败");

  const items = (page.items || []).map((r) => mapRoleToListRow(r));

  return {
    items,
    total: page.total,
    page_no: page.page_no,
    page_size: page.page_size,
    has_next: page.has_next,
  };
}

function mapRoleToListRow(r: RoleTable) {
  return {
    roleId: r.id,
    roleName: r.name,
    roleCode: r.code,
    description: r.description,
    enabled: r.status === "0",
    createTime: r.created_time,
  };
}

function mapMenuTableToRoute(m: MenuTable): AppRouteRecord {
  const childrenRaw = m.children?.filter(Boolean) ?? [];
  const children = childrenRaw.length ? childrenRaw.map(mapMenuTableToRoute) : undefined;

  return {
    path: (m.route_path ?? "").trim(),
    name: m.route_name,
    meta: {
      title: m.title ?? m.name ?? "",
      icon: m.icon,
      hidden: m.hidden,
      keepAlive: m.keep_alive,
    },
    children,
  };
}

/** 菜单管理演示页：树形表格数据 */
export async function fetchGetMenuList(): Promise<AppRouteRecord[]> {
  const res = await MenuAPI.listMenu({});
  const tree = assertSuccess(res, "获取菜单失败");
  return (tree || []).map(mapMenuTableToRoute);
}
