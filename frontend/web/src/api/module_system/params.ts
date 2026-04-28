import request from '@/utils/http';

const API_PATH = '/system/param';

const ParamsAPI = {
  /**
   * 上传文件
   * @param body 文件数据
   * @returns 上传后的文件路径
   */
  uploadFile(body: any) {
    return request<ApiResponse<UploadFilePath>>({
      url: `${API_PATH}/upload`,
      method: 'post',
      data: body,
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  /**
   * 获取初始化配置
   * @returns 初始化配置列表
   */
  getInitConfig() {
    return request<ApiResponse<ConfigTable[]>>({
      url: `${API_PATH}/info`,
      method: 'get',
    });
  },

  /**
   * 获取参数列表
   * @param query 查询参数
   * @returns 参数列表
   */
  listParams(query: ConfigPageQuery) {
    return request<PageResult<ConfigTable[]>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取参数详情
   * @param query 参数ID
   * @returns 参数详情
   */
  detailParams(query: number) {
    return request<ApiResponse<ConfigTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 创建参数
   * @param body 参数信息
   */
  createParams(body: ConfigForm) {
    return request({
      url: `${API_PATH}/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新参数
   * @param id 参数ID
   * @param body 参数信息
   */
  updateParams(id: number, body: ConfigForm) {
    return request({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除参数
   * @param body 参数ID列表
   */
  deleteParams(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 导出参数
   * @param body 查询参数
   * @returns 导出的参数文件
   */
  exportParams(body: ConfigPageQuery) {
    return request<ApiResponse<Blob>>({
      url: `${API_PATH}/export`,
      method: 'post',
      data: body,
      responseType: 'blob',
    });
  },
};

export default ParamsAPI;

export interface ConfigPageQuery extends PageQuery {
  config_name?: string;
  config_key?: string;
  config_type?: boolean;
  created_time?: string[];
  updated_time?: string[];
}

export interface ConfigTable extends BaseType {
  config_name?: string;
  config_key?: string;
  config_value?: string;
  config_type?: boolean;
}

export interface ConfigForm extends BaseFormType {
  config_name?: string;
  config_key?: string;
  config_value?: string;
  config_type?: boolean;
}
