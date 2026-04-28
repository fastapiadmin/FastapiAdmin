import request from '@/utils/http';

const API_PATH = '/system/log';

const LogAPI = {
  /**
   * 获取日志列表
   * @param query 查询参数
   * @returns 日志列表
   */
  listLog(query: LogPageQuery) {
    return request<PageResult<LogTable[]>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取日志详情
   * @param query 日志ID
   * @returns 日志详情
   */
  detailLog(query: number) {
    return request<ApiResponse<LogTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 删除日志
   * @param body 日志ID列表
   */
  deleteLog(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 导出日志
   * @param body 查询参数
   * @returns 日志导出文件
   */
  exportLog(body: LogPageQuery) {
    return request<ApiResponse<Blob>>({
      url: `${API_PATH}/export`,
      method: 'post',
      data: body,
      responseType: 'blob',
    });
  },
};

export default LogAPI;

export interface LogPageQuery extends PageQuery {
  type?: number;
  request_path?: string;
  creator_name?: string;
  created_time?: string[];
  updated_time?: string[];
  created_id?: number;
  updated_id?: number;
}

export interface LogTable extends BaseType {
  type?: number; // 1 登录日志 2 操作日志
  request_path?: string;
  request_method?: string;
  request_ip?: string;
  login_location?: string;
  request_browser?: string;
  request_os?: string;
  response_code?: number;
  request_payload?: string;
  response_json?: string;
  process_time?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
  deleted_by?: CommonType;
}
