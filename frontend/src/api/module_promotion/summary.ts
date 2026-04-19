import request from "@/utils/request";

const API_PATH = "/promotion/summary";

const SummaryAPI = {
  getDetail(id: number) {
    return request<ApiResponse<SummaryItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: SummaryQuery) {
    return request<ApiResponse<PageResult<SummaryItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: SummaryForm) {
    return request<ApiResponse<SummaryItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: SummaryForm) {
    return request<ApiResponse<SummaryItem>>({
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

export default SummaryAPI;

export interface SummaryQuery {
  summary_no?: string;
  activity_id?: number;
  summary_type?: string;
  summary_status?: string;
}

export interface SummaryForm {
  summary_no?: string;
  activity_id?: number;
  activity_name?: string;
  summary_type?: string;
  summary_date?: string;
  submitter_id?: number;
  submitter_name?: string;
  summary_content?: string;
  attachment_url?: string;
  summary_status?: string;
  remark?: string;
}

export interface SummaryItem extends SummaryForm, BaseType {
  summary_no: string;
  summary_type: string;
  summary_status: string;
}