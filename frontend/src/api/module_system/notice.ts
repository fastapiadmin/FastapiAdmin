import request from "@/utils/request";

const API_PATH = "/system/notice";

const NoticeAPI = {
  listNotice(query: NoticePageQuery) {
    return request<ApiResponse<PageResult<NoticeTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  listNoticeAvailable() {
    return request<ApiResponse<PageResult<NoticeTable[]>>>({
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
      url: `${API_PATH}/available/setting`,
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
  created_by?: creatorType;
  updated_by?: updatorType;
}

export interface NoticeForm extends BaseFormType {
  notice_title?: string;
  notice_type?: string;
  notice_content?: string;
}
