import request from '@/utils/http';

const API_PATH = '/system/notice';

const NoticeAPI = {
  /**
   * 获取通知列表
   * @param query 查询参数
   * @returns 通知列表
   */
  listNotice(query: NoticePageQuery) {
    return request<PageResult<NoticeTable[]>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取可用通知列表
   * @returns 通知列表
   */
  listNoticeAvailable() {
    return request<PageResult<NoticeTable[]>>({
      url: `${API_PATH}/available`,
      method: 'get',
    });
  },

  /**
   * 获取通知详情
   * @param query 通知ID
   * @returns 通知详情
   */
  detailNotice(query: number) {
    return request<ApiResponse<NoticeTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 创建通知
   * @param body 通知信息
   */
  createNotice(body: NoticeForm) {
    return request({
      url: `${API_PATH}/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新通知
   * @param id 通知ID
   * @param body 通知信息
   */
  updateNotice(id: number, body: NoticeForm) {
    return request({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除通知
   * @param body 通知ID列表
   */
  deleteNotice(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 批量设置通知状态
   * @param body 批量操作参数
   */
  batchNotice(body: BatchType) {
    return request({
      url: `${API_PATH}/available/setting`,
      method: 'patch',
      data: body,
    });
  },

  /**
   * 导出通知
   * @param body 查询参数
   * @returns 通知导出文件
   */
  exportNotice(body: NoticePageQuery) {
    return request<ApiResponse<Blob>>({
      url: `${API_PATH}/export`,
      method: 'post',
      data: body,
      responseType: 'blob',
    });
  },
};

export default NoticeAPI;

export interface NoticePageQuery extends PageQuery {
  notice_title?: string;
  notice_type?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
  created_id?: number;
  updated_id?: number;
}

export interface NoticeTable extends BaseType {
  notice_title?: string;
  notice_type?: string;
  notice_content?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
  deleted_by?: CommonType;
}

export interface NoticeForm extends BaseFormType {
  notice_title?: string;
  notice_type?: string;
  notice_content?: string;
}
