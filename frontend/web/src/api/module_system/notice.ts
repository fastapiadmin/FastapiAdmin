import { request } from "@utils";

const API_PATH = "/system/notice";

const NoticeAPI = {
  listNotice(query: NoticePageQuery) {
    return request<ApiResponse<PageResult<NoticeTable>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  listNoticeAvailable() {
    return request<ApiResponse<PageResult<NoticeTable>>>({
      url: `${API_PATH}/available`,
      method: "get",
    });
  },

  detailNotice(query: number) {
    return request<ApiResponse<NoticeTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createNotice(body: NoticeForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateNotice(id: number, body: NoticeForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteNotice(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  batchNotice(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/status/batch`,
      method: "patch",
      data: body,
    });
  },

  exportNotice(body: NoticePageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  readNotice(id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/read/${id}`,
      method: "post",
    });
  },

  readAllNotice() {
    return request<ApiResponse>({
      url: `${API_PATH}/read-all`,
      method: "post",
    });
  },

  getUnreadCount() {
    return request<ApiResponse<number>>({
      url: `${API_PATH}/unread-count`,
      method: "get",
    });
  },

  getNotificationPanel() {
    return request<ApiResponse<NotificationPanel>>({
      url: `${API_PATH}/panel`,
      method: "get",
    });
  },
};

export default NoticeAPI;

export interface NoticePageQuery extends PageQuery, UserByQueryParams {
  notice_title?: string;
  notice_type?: string;
}

export interface NoticeTable extends BaseType {
  notice_title?: string;
  notice_type?: string;
  notice_content?: string;
  status?: number;
  description?: string;
}

export interface NoticeForm extends BaseFormType {
  notice_title?: string;
  notice_type?: string;
  notice_content?: string;
  status?: number;
  description?: string;
}

export interface NotificationPanelMessage {
  id?: number;
  title: string;
  content?: string;
  time: string;
  type?: string;
}

export interface NotificationPanel {
  notices: NoticeTable[];
  messages: NotificationPanelMessage[];
  pendings: NotificationPanelMessage[];
}
