import request from "@/utils/request";

const API_PATH = "/application/myapp";

export const ApplicationAPI = {
  /**
   * 获取应用详情
   * @param id 应用ID
   */
  detailApp(id: number) {
    return request<ApiResponse<ApplicationInfo>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  /**
   * 查询应用列表
   * @param query 查询参数
   */
  listApp(query: ApplicationPageQuery) {
    return request<ApiResponse<PageResult<ApplicationInfo[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  /**
   * 创建应用
   * @param body 应用信息
   */
  createApp(body: ApplicationForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  /**
   * 修改应用
   * @param id 应用ID
   * @param body 应用信息
   */
  updateApp(id: number, body: ApplicationForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  /**
   * 删除应用
   * @param body 应用ID数组
   */
  deleteApp(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  /**
   * 批量修改应用状态
   * @param body 批量操作参数
   */
  batchApp(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },
};

export default ApplicationAPI;

/**
 * 应用分页查询参数
 */
export interface ApplicationPageQuery extends PageQuery {
  name?: string;
  status?: string;
  created_id?: number;
  created_time?: string[];
  updated_id?: number;
  updated_time?: string[];
}

/**
 * 应用信息
 */
export interface ApplicationInfo extends BaseType {
  name?: string;
  access_url?: string;
  icon_url?: string;
  created_by?: creatorType;
  updated_by?: updatorType;
}

/**
 * 应用表单
 */
export interface ApplicationForm extends BaseFormType {
  name: string;
  access_url: string;
  icon_url: string;
}
