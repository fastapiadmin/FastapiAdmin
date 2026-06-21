import { request } from "@utils";

const API_PATH = "/platform/plugin";

const PluginAPI = {
  // 超管：插件列表
  list(page: PageQuery, search?: PluginQueryParam) {
    return request<ApiResponse<PageResult<PluginTable>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: { ...page, ...search },
    });
  },

  // 超管：插件详情
  detail(id: number) {
    return request<ApiResponse<PluginTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 超管：创建插件
  create(body: PluginForm) {
    return request<ApiResponse<PluginTable>>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 超管：更新插件
  update(id: number, body: PluginForm) {
    return request<ApiResponse<PluginTable>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 超管：删除插件
  delete(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 租户：插件市场
  marketplace(page: PageQuery, category?: string) {
    return request<ApiResponse<PageResult<PluginTable>>>({
      url: `${API_PATH}/marketplace`,
      method: "get",
      params: { ...page, category },
    });
  },

  // 租户：安装插件
  install(pluginId: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/install`,
      method: "post",
      data: { plugin_id: pluginId },
    });
  },

  // 租户：卸载插件
  uninstall(pluginId: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/uninstall`,
      method: "post",
      data: { plugin_id: pluginId },
    });
  },

  // 租户：启用/禁用插件
  toggle(pluginId: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/toggle`,
      method: "post",
      data: { plugin_id: pluginId },
    });
  },

  // 租户：我的插件
  myPlugins() {
    return request<ApiResponse<PluginTable[]>>({
      url: `${API_PATH}/my`,
      method: "get",
    });
  },

  // 超管：热重载插件路由
  reload() {
    return request<ApiResponse<string>>({
      url: `${API_PATH}/reload`,
      method: "post",
    });
  },
};

export default PluginAPI;

export interface PluginQueryParam extends PageQuery, UserByQueryParams, TenantByQueryParams {
  name?: string;
  category?: string;
}

export interface PluginTable extends BaseType {
  name: string;
  code: string;
  category?: string;
  icon?: string;
  version?: string;
  price?: number;
  installed?: boolean;
  author?: string;
  menu_path?: string;
  permission_prefix?: string;
  dependencies?: string;
  sort?: number;
  status?: number;
  description?: string;
}

export interface PluginForm extends BaseFormType {
  name?: string;
  code?: string;
  category?: string;
  icon?: string;
  version?: string;
  price?: number;
  sort?: number;
  author?: string;
  menu_path?: string;
  permission_prefix?: string;
  dependencies?: string;
  status?: number;
  description?: string;
}
