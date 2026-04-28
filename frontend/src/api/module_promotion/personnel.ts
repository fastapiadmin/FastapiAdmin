import request from "@/utils/request";

const API_PATH = "/promotion/personnel";

const PersonnelAPI = {
  getDetail(id: number) {
    return request<ApiResponse<PersonnelItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: PersonnelQuery) {
    return request<ApiResponse<PageResult<PersonnelItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: PersonnelForm) {
    return request<ApiResponse<PersonnelItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: PersonnelForm) {
    return request<ApiResponse<PersonnelItem>>({
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

export default PersonnelAPI;

export interface PersonnelQuery {
  personnel_name?: string;
  personnel_code?: string;
  personnel_type?: string;
  team_id?: number;
  team_name?: string;
  personnel_status?: string;
}

export interface PersonnelForm {
  personnel_name: string;
  personnel_code?: string;
  personnel_type?: string;
  team_id?: number;
  team_name?: string;
  id_card?: string;
  phone?: string;
  email?: string;
  join_date?: string;
  personnel_status?: string;
  display_order?: number;
  remark?: string;
}

export interface PersonnelItem extends PersonnelForm, BaseType {
  personnel_no: string;
  personnel_type: string;
  personnel_status: string;
}
