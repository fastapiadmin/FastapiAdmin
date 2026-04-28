import request from "@/utils/request";

const API_PATH = "/promotion/document";

const DocumentAPI = {
  getDetail(id: number) {
    return request<ApiResponse<DocumentItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: DocumentQuery) {
    return request<ApiResponse<PageResult<DocumentItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: DocumentForm) {
    return request<ApiResponse<DocumentItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: DocumentForm) {
    return request<ApiResponse<DocumentItem>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data,
    });
  },

  delete(id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete/${id}`,
      method: "delete",
    });
  },

  batchDelete(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/batch-delete`,
      method: "delete",
      data: ids,
    });
  },
};

export default DocumentAPI;

export interface DocumentQuery {
  document_no?: string;
  document_type?: string;
  author_name?: string;
  document_status?: string;
}

export interface DocumentForm {
  document_no?: string;
  document_type?: string;
  title?: string;
  author_id?: number;
  author_name?: string;
  document_content?: string;
  attachment_url?: string;
  published_date?: string;
  document_status?: string;
  remark?: string;
}

export interface DocumentItem extends DocumentForm, BaseType {
  document_no: string;
  document_type: string;
  document_status: string;
}
