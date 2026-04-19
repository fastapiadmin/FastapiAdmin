import request from "@/utils/request";

const API_PATH = "/promotion/expense";

const ExpenseAPI = {
  getDetail(id: number) {
    return request<ApiResponse<ExpenseItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: ExpenseQuery) {
    return request<ApiResponse<PageResult<ExpenseItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: ExpenseForm) {
    return request<ApiResponse<ExpenseItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: ExpenseForm) {
    return request<ApiResponse<ExpenseItem>>({
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

export default ExpenseAPI;

export interface ExpenseQuery {
  expense_no?: string;
  expense_type?: string;
  expense_status?: string;
}

export interface ExpenseForm {
  expense_no?: string;
  expense_type?: string;
  activity_id?: number;
  activity_name?: string;
  personnel_id?: number;
  personnel_name?: string;
  expense_date?: string;
  amount?: number;
  description?: string;
  invoice_status?: string;
  expense_status?: string;
  remark?: string;
}

export interface ExpenseItem extends ExpenseForm, BaseType {
  expense_no: string;
  expense_type: string;
  expense_status: string;
}