import request from "@/utils/request";

const API_PATH = "/system/dict";

const DictAPI = {
  listDictType(query: DictPageQuery) {
    return request<ApiResponse<PageResult<DictTable[]>>>({
      url: `${API_PATH}/type/list`,
      method: "get",
      params: query,
    });
  },

  optionDictType() {
    return request<ApiResponse>({
      url: `${API_PATH}/type/optionselect`,
      method: "get",
    });
  },

  detailDictType(query: number) {
    return request<ApiResponse<DictTable>>({
      url: `${API_PATH}/type/detail/${query}`,
      method: "get",
    });
  },

  createDictType(body: DictForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/type/create`,
      method: "post",
      data: body,
    });
  },

  updateDictType(id: number, body: DictForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/type/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteDictType(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/type/delete`,
      method: "delete",
      data: body,
    });
  },

  batchDictType(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/type/available/setting`,
      method: "patch",
      data: body,
    });
  },

  exportDictType(body: DictPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/type/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  listDictData(query: DictDataPageQuery) {
    return request<ApiResponse<PageResult<DictDataTable[]>>>({
      url: `${API_PATH}/data/list`,
      method: "get",
      params: query,
    });
  },

  detailDictData(query: number) {
    return request<ApiResponse<DictDataTable>>({
      url: `${API_PATH}/data/detail/${query}`,
      method: "get",
    });
  },

  createDictData(body: DictDataForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/data/create`,
      method: "post",
      data: body,
    });
  },

  updateDictData(id: number, body: DictDataForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/data/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteDictData(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/data/delete`,
      method: "delete",
      data: body,
    });
  },

  batchDictData(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/data/available/setting`,
      method: "patch",
      data: body,
    });
  },

  exportDictData(body: DictDataPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/data/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  getInitDict(dict_type: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/data/info/${dict_type}`,
      method: "get",
    });
  },
};

export default DictAPI;

export interface DictPageQuery extends PageQuery {
  dict_name?: string;
  dict_type?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
}

export interface DictDataPageQuery extends PageQuery {
  dict_label?: string;
  dict_type?: string;
  dict_type_id?: number;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
}

export interface DictTable extends BaseType {
  dict_name?: string;
  dict_type?: string;
}

export interface DictForm extends BaseFormType {
  dict_name?: string;
  dict_type?: string;
}

export interface DictDataTable extends BaseType {
  dict_sort?: number;
  dict_label?: string;
  dict_value?: string;
  dict_type_id?: number;
  dict_type?: string;
  css_class?: string;
  list_class?: string;
  is_default?: boolean;
}

export interface DictDataForm extends BaseFormType {
  dict_sort?: number;
  dict_label?: string;
  dict_value?: string;
  dict_type_id?: number;
  dict_type?: string;
  css_class?: string;
  list_class?: string;
  is_default?: boolean;
}
