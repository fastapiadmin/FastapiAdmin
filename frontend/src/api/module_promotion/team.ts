import request from "@/utils/request";

const API_PATH = "/promotion/team";

const TeamAPI = {
  getDetail(id: number) {
    return request<ApiResponse<TeamItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: TeamQuery) {
    return request<ApiResponse<PageResult<TeamItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: TeamForm) {
    return request<ApiResponse<TeamItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: TeamForm) {
    return request<ApiResponse<TeamItem>>({
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

export default TeamAPI;

export interface TeamQuery {
  team_name?: string;
  team_code?: string;
  team_level?: string;
  team_status?: string;
}

export interface TeamForm {
  team_name: string;
  team_code?: string;
  team_level?: string;
  parent_id?: number;
  parent_name?: string;
  leader_name?: string;
  leader_phone?: string;
  member_count?: number;
  team_status?: string;
  display_order?: number;
  remark?: string;
}

export interface TeamItem extends TeamForm, BaseType {
  team_no: string;
  team_level: string;
  team_status: string;
}
