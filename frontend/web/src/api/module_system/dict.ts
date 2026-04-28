import request from '@/utils/http';

const API_PATH = '/system/dict';

const DictAPI = {
  /**
   * 获取字典类型列表
   * @param query 查询参数
   * @returns 字典类型列表
   */
  listDictType(query: DictPageQuery) {
    return request<PageResult<DictTable[]>>({
      url: `${API_PATH}/type/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取字典类型选项选择列表
   * @returns 字典类型选项选择列表
   */
  optionDictType() {
    return request({
      url: `${API_PATH}/type/optionselect`,
      method: 'get',
    });
  },

  /**
   * 获取字典类型详情
   * @param query 字典类型ID
   * @returns 字典类型详情
   */
  detailDictType(query: number) {
    return request<ApiResponse<DictTable>>({
      url: `${API_PATH}/type/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 创建字典类型
   * @param body 字典类型信息
   */
  createDictType(body: DictForm) {
    return request({
      url: `${API_PATH}/type/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新字典类型
   * @param id 字典类型ID
   * @param body 字典类型信息
   */
  updateDictType(id: number, body: DictForm) {
    return request({
      url: `${API_PATH}/type/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除字典类型
   * @param body 字典类型ID列表
   */
  deleteDictType(body: number[]) {
    return request({
      url: `${API_PATH}/type/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 批量设置字典类型状态
   * @param body 批量设置字典类型状态请求体
   */
  batchDictType(body: BatchType) {
    return request({
      url: `${API_PATH}/type/available/setting`,
      method: 'patch',
      data: body,
    });
  },

  /**
   * 导出字典类型
   * @param body 查询参数
   * @returns 字典类型导出文件
   */
  exportDictType(body: DictPageQuery) {
    return request<ApiResponse<Blob>>({
      url: `${API_PATH}/type/export`,
      method: 'post',
      data: body,
      responseType: 'blob',
    });
  },

  /**
   * 获取字典数据列表
   * @param query 查询参数
   * @returns 字典数据列表
   */
  listDictData(query: DictDataPageQuery) {
    return request<PageResult<DictDataTable[]>>({
      url: `${API_PATH}/data/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取字典数据详情
   * @param query 字典数据ID
   * @returns 字典数据详情
   */
  detailDictData(query: number) {
    return request<ApiResponse<DictDataTable>>({
      url: `${API_PATH}/data/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 创建字典数据
   * @param body 字典数据信息
   */
  createDictData(body: DictDataForm) {
    return request({
      url: `${API_PATH}/data/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新字典数据
   * @param id 字典数据ID
   * @param body 字典数据信息
   */
  updateDictData(id: number, body: DictDataForm) {
    return request({
      url: `${API_PATH}/data/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除字典数据
   * @param body 字典数据ID列表
   */
  deleteDictData(body: number[]) {
    return request({
      url: `${API_PATH}/data/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 批量设置字典数据状态
   * @param body 批量设置字典数据状态请求体
   */
  batchDictData(body: BatchType) {
    return request({
      url: `${API_PATH}/data/available/setting`,
      method: 'patch',
      data: body,
    });
  },

  /**
   * 导出字典数据
   * @param body 查询参数
   * @returns 字典数据导出文件
   */
  exportDictData(body: DictDataPageQuery) {
    return request<ApiResponse<Blob>>({
      url: `${API_PATH}/data/export`,
      method: 'post',
      data: body,
      responseType: 'blob',
    });
  },

  /**
   * 获取初始化字典数据
   * @param dict_type 字典类型
   * @returns 初始化字典数据
   */
  getInitDict(dict_type: string) {
    return request({
      url: `${API_PATH}/data/info/${dict_type}`,
      method: 'get',
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
