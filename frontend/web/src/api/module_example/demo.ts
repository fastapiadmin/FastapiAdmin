import request from '@/utils/http';

const API_PATH = '/example/demo';

const DemoAPI = {
  /**
   * 查询演示列表
   * @param query 查询参数
   */
  getDemoList(query: DemoPageQuery) {
    return request<PageResult<DemoTable[]>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 查询演示详情
   * @param query 演示ID
   */
  getDemoDetail(query: number) {
    return request<ApiResponse<DemoTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 创建演示
   * @param body 演示信息
   */
  createDemo(body: DemoForm) {
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
  updateDemo(id: number, body: DemoForm) {
    return request({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除演示
   * @param body 演示ID数组
   */
  deleteDemo(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 批量操作演示
   * @param body 批量操作参数
   */
  batchDemo(body: BatchType) {
    return request({
      url: `${API_PATH}/available/setting`,
      method: 'patch',
      data: body,
    });
  },

  /**
   * 导出演示
   * @param body 导出参数
   */
  exportDemo(body: DemoPageQuery) {
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
  downloadTemplateDemo() {
    return request({
      url: `${API_PATH}/download/template`,
      method: 'post',
      responseType: 'blob',
    });
  },

  /**
   * 导入演示
   * @param body 导入参数
   */
  importDemo(body: FormData) {
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

export default DemoAPI;

export interface DemoPageQuery extends PageQuery {
  name?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
  created_id?: number;
  updated_id?: number;
}

export interface DemoTable extends BaseType {
  name?: string;
  status?: string;
  description?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
  deleted_by?: CommonType;
  a?: number;
  b?: number;
  c?: number;
  d?: boolean;
  e?: string;
  f?: string;
  g?: string;
  h?: string;
  i?: Record<string, any>;
}

export interface DemoForm extends BaseFormType {
  name?: string;
  status?: string;
  description?: string;
  a?: number;
  b?: number;
  c?: number;
  d?: boolean;
  e?: string;
  f?: Date | string;
  g?: Date | string;
  h?: string;
  i?: Record<string, any>;
}
