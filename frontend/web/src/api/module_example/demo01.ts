import request from '@/utils/http';

const API_PATH = '/example/demo01';

const Demo01API = {
  /**
   * 查询演示列表
   * @param query 查询参数
   */
  getDemo01List(query: Demo01PageQuery) {
    return request<PageResult<Demo01Table[]>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 查询演示详情
   * @param id 演示ID
   */
  getDemo01Detail(id: number) {
    return request<ApiResponse<Demo01Table>>({
      url: `${API_PATH}/detail/${id}`,
      method: 'get',
    });
  },

  /**
   * 创建演示
   * @param body 演示信息
   */
  createDemo01(body: Demo01Form) {
    return request({
      url: `${API_PATH}/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新演示
   * @param id 演示ID
   * @param body 演示信息
   */
  updateDemo01(id: number, body: Demo01Form) {
    return request({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除演示
   * @param body 演示ID列表
   */
  deleteDemo01(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 批量设置演示状态
   * @param body 批量设置参数
   */
  batchDemo01(body: BatchType) {
    return request({
      url: `${API_PATH}/available/setting`,
      method: 'patch',
      data: body,
    });
  },

  /**
   * 导出演示
   * @param body 漼示参数
   */
  exportDemo01(body: Demo01PageQuery) {
    return request<ApiResponse<Blob>>({
      url: `${API_PATH}/export`,
      method: 'post',
      data: body,
      responseType: 'blob',
    });
  },

  /**
   * 下载演示模板
   */
  downloadDemo01Template() {
    return request({
      url: `${API_PATH}/download/template`,
      method: 'post',
      responseType: 'blob',
    });
  },

  /**
   * 导入演示
   * @param body 演示数据
   */
  importDemo01(body: FormData) {
    return request({
      url: `${API_PATH}/import`,
      method: 'post',
      data: body,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

export default Demo01API;

export interface Demo01PageQuery extends PageQuery {
  /** 与后端 Demo01QueryParam 一致 */
  name?: string;
  description?: string;
  /** 是否启用：0 启用 / 1 禁用（字符串） */
  status?: string;
  created_time?: string[];
  updated_time?: string[];
  created_id?: number;
  updated_id?: number;
}

/**
 * 与后端 Demo01OutSchema 一致：
 * Demo01CreateSchema(name,status,description) + BaseSchema + UserBySchema
 */
export interface Demo01Table extends BaseType {
  name?: string;
  status?: string;
  description?: string;
  created_id?: number;
  updated_id?: number;
  created_by?: CommonType;
  updated_by?: CommonType;
  deleted_by?: CommonType;
}

/** 与后端 Demo01CreateSchema / Demo01UpdateSchema 一致（不含 id，更新走 URL） */
export interface Demo01Form extends BaseFormType {
  name?: string;
  status?: string;
  description?: string;
}
