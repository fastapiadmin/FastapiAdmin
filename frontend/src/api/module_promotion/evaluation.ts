import request from "@/utils/request";

const API_PATH = "/promotion/evaluation";

const EvaluationAPI = {
  getDetail(id: number) {
    return request<ApiResponse<EvaluationItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: EvaluationQuery) {
    return request<ApiResponse<PageResult<EvaluationItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: EvaluationForm) {
    return request<ApiResponse<EvaluationItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: EvaluationForm) {
    return request<ApiResponse<EvaluationItem>>({
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

export default EvaluationAPI;

export interface EvaluationQuery {
  evaluation_no?: string;
  evaluation_type?: string;
  personnel_name?: string;
  evaluation_status?: string;
}

export interface EvaluationForm {
  evaluation_no?: string;
  evaluation_type?: string;
  activity_id?: number;
  activity_name?: string;
  personnel_id?: number;
  personnel_name?: string;
  evaluation_date?: string;
  evaluation_score?: number;
  evaluation_result?: string;
  evaluation_content?: string;
  attachment_url?: string;
  evaluation_status?: string;
  remark?: string;
}

export interface EvaluationItem extends EvaluationForm, BaseType {
  evaluation_no: string;
  evaluation_type: string;
  evaluation_status: string;
}
