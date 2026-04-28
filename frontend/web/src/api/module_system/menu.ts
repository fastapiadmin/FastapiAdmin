import request from '@/utils/http';

const API_PATH = '/system/menu';

const MenuAPI = {
  /**
   * 获取菜单树
   * @param query 查询参数
   * @returns 菜单树
   */
  listMenu(query?: MenuPageQuery) {
    return request<ApiResponse<MenuTable[]>>({
      url: `${API_PATH}/tree`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取菜单详情
   * @param query 菜单ID
   * @returns 菜单详情
   */
  detailMenu(query: number) {
    return request<ApiResponse<MenuTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 创建菜单
   * @param body 菜单信息
   */
  createMenu(body: MenuForm) {
    return request({
      url: `${API_PATH}/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新菜单
   * @param id 菜单ID
   * @param body 菜单信息
   */
  updateMenu(id: number, body: MenuForm) {
    return request({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除菜单
   * @param body 菜单ID列表
   */
  deleteMenu(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 批量设置菜单状态
   * @param body 批量操作参数
   */
  batchMenu(body: BatchType) {
    return request({
      url: `${API_PATH}/available/setting`,
      method: 'patch',
      data: body,
    });
  },
};

export default MenuAPI;

export interface MenuPageQuery {
  name?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
  /** 与后端 Query `menu_client` 一致：pc | app；菜单管理 Tab 切换时传入 */
  menu_client?: "pc" | "app";
}

export interface MenuTable extends BaseType {
  name?: string;
  type?: number;
  icon?: string;
  order?: number;
  permission?: string;
  route_name?: string;
  route_path?: string;
  component_path?: string;
  redirect?: string;
  parent_id?: number;
  parent_name?: string;
  keep_alive?: boolean;
  hidden?: boolean;
  always_show?: boolean;
  title?: string;
  params?: { key: string; value: string }[];
  affix?: boolean;
  children?: MenuTable[];
  client?: "pc" | "app";
}

export interface MenuForm extends BaseFormType {
  name?: string;
  type?: number;
  icon?: string;
  order?: number;
  permission?: string;
  route_name?: string;
  route_path?: string;
  component_path?: string;
  redirect?: string;
  parent_id?: number;
  keep_alive?: boolean;
  hidden?: boolean;
  always_show?: boolean;
  title?: string;
  params?: KeyValue[];
  affix?: boolean;
  client?: "pc" | "app";
}

export interface KeyValue {
  key: string;
  value: string;
}
