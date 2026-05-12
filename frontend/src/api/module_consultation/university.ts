import request from "@/utils/request";

const API_PATH = "/consultation/university";

/**
 * 高校信息API
 */
export const UniversityAPI = {
  /** 获取高校列表 */
  getList(params: UniversityQuery) {
    return request<ApiResponse<PageResult<UniversityItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  /** 获取高校详情 */
  getDetail(id: number) {
    return request<ApiResponse<UniversityItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  /** 获取高校下拉选项 */
  getOptions() {
    return request<ApiResponse<UniversityOption[]>>({
      url: `${API_PATH}/options`,
      method: "get",
    });
  },

  /** 创建高校 */
  create(data: UniversityForm) {
    return request<ApiResponse<UniversityItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  /** 更新高校 */
  update(id: number, data: UniversityForm) {
    return request<ApiResponse<UniversityItem>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data,
    });
  },

  /** 删除高校 */
  delete(id: number) {
    return request<ApiResponse<null>>({
      url: `${API_PATH}/delete/${id}`,
      method: "delete",
    });
  },
};

/** 高校信息 */
export interface UniversityItem {
  id: number;
  name: string;
  code?: string;
  abbreviation?: string;
  contact_person?: string;
  contact_phone?: string;
  contact_email?: string;
  province?: string;
  city?: string;
  address?: string;
  description?: string;
  website?: string;
  status: string;
  created_time?: string;
  updated_time?: string;
}

/** 高校下拉选项 */
export interface UniversityOption {
  id: number;
  name: string;
  code?: string;
}

/** 高校查询参数 */
export interface UniversityQuery {
  page?: number;
  pageSize?: number;
  name?: string;
  code?: string;
  province?: string;
  city?: string;
  status?: string;
}

/** 高校表单数据 */
export interface UniversityForm {
  name: string;
  code?: string;
  abbreviation?: string;
  contact_person?: string;
  contact_phone?: string;
  contact_email?: string;
  province?: string;
  city?: string;
  address?: string;
  description?: string;
  website?: string;
  status?: string;
}

export default UniversityAPI;
