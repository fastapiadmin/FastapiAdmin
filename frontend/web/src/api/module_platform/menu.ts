import { request } from "@utils";

const API_PATH = "/platform/menu";

const MenuAPI = {
  listMenu(query?: MenuPageQuery) {
    return request<ApiResponse<MenuTable[]>>({
      url: `${API_PATH}/tree`,
      method: "get",
      params: query,
    });
  },

  detailMenu(query: number) {
    return request<ApiResponse<MenuTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createMenu(body: MenuForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateMenu(id: number, body: MenuForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteMenu(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  batchMenu(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/status/batch`,
      method: "patch",
      data: body,
    });
  },
};

export default MenuAPI;

export interface MenuPageQuery extends BaseQueryParams {
  name?: string;
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
  link?: string;
  is_iframe?: boolean;
  is_hide_tab?: boolean;
  active_path?: string;
  show_badge?: boolean;
  show_text_badge?: string;
  scope?: "platform" | "tenant";
  status?: number;
  description?: string;
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
  link?: string;
  is_iframe?: boolean;
  is_hide_tab?: boolean;
  active_path?: string;
  show_badge?: boolean;
  show_text_badge?: string;
  scope?: "platform" | "tenant";
  status?: number;
  description?: string;
}

export interface KeyValue {
  key: string;
  value: string;
}
