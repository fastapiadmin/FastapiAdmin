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
    return request<ApiResponse<NoticeTable[]>>({
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
};

export default NoticeAPI;

export interface NoticePageQuery extends PageQuery, UserByQueryParams {
  notice_title?: string;
  notice_type?: string;
  status?: number;
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
