import request from "@/utils/request";

const API_PATH = "/generator/gencode";

const GencodeAPI = {
  // 查询生成表数据
  listTable(query: GenTablePageQuery) {
    return request<ApiResponse<PageResult<GenTableSchema[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 查询db数据库列表
  listDbTable(query: DBTablePageQuery) {
    return request<ApiResponse<PageResult<DBTableSchema[]>>>({
      url: `${API_PATH}/db/list`,
      method: "get",
      params: query,
    });
  },

  // 导入表
  importTable(table_names: string[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: table_names,
    });
  },

  // 查询表详细信息
  detailTable(table_id: number) {
    return request<ApiResponse<GenTableSchema>>({
      url: `${API_PATH}/detail/${table_id}`,
      method: "get",
    });
  },

  // 创建表
  createTable(sql: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: sql,
    });
  },

  // 更新表信息
  updateTable(data: GenTableSchema, table_id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${table_id}`,
      method: "put",
      data,
    });
  },

  // 删除表数据
  deleteTable(table_ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: table_ids,
    });
  },

  // 批量生成代码
  batchGenCode(table_names: string[]) {
    return request<Blob>({
      url: `${API_PATH}/batch/output`,
      method: "patch",
      data: table_names,
      responseType: "blob",
    });
  },

  // 生成代码到指定路径
  genCodeToPath(table_name: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/output/${table_name}`,
      method: "post",
    });
  },

  // 预览生成代码
  previewTable(id: number) {
    return request<ApiResponse<Record<string, string>>>({
      url: `${API_PATH}/preview/${id}`,
      method: "get",
    });
  },

  // 同步数据库
  syncDb(table_name: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/sync_db/${table_name}`,
      method: "post",
    });
  },
};

export default GencodeAPI;

/** 代码生成预览对象 */
export interface GeneratorPreviewVO {
  /** 文件生成路径 */
  path: string;
  /** 文件名称 */
  file_name: string;
  /** 文件内容 */
  content: string;
}

/** 代码生成表分页查询参数 */
export interface DBTablePageQuery extends PageQuery {
  /** 表名称 */
  table_name?: string;
  /** 表描述 */
  table_comment?: string;
}

/**数据库表基本信息接口 */
export interface DBTableSchema {
  database_name?: string;
  table_name?: string;
  table_comment?: string;
  table_type?: string;
}

/** 代码生成表分页查询参数 */
export interface GenTablePageQuery extends PageQuery {
  /** 表名称 */
  table_name?: string;
  /** 表描述 */
  table_comment?: string;
}

/** 代码生成业务表模型 */
export interface GenTableSchema extends BaseType {
  /** 表名称 */
  table_name?: string;
  /** 表描述 */
  table_comment?: string;
  /** 关联子表的表名 */
  sub_table_name?: string;
  /** 关联子表的外键名 */
  sub_table_fk_name?: string;
  /** 实体类名称 */
  class_name?: string;
  /** 生成包路径 */
  package_name?: string;
  /** 生成模块名 */
  module_name?: string;
  /** 生成业务名 */
  business_name?: string;
  /** 生成功能名 */
  function_name?: string;
  /** 所属父级分类 */
  parent_menu_id?: number;
  /** 表列信息 */
  columns: GenTableColumnSchema[];
  /** 主键信息 */
  pk_column?: GenTableColumnSchema;
  /** 子表信息 */
  sub_table?: GenTableSchema;
  /** 是否为子表 */
  sub?: boolean;
  created_by?: creatorType;
  updated_by?: updatorType;
}

/** 代码生成业务表列模型 */
export interface GenTableColumnSchema extends BaseType {
  /** 归属表编号 */
  table_id?: number;
  /** 列名称 */
  column_name: string;
  /** 列描述 */
  column_comment?: string;
  /** 列类型 */
  column_type?: string;
  /** 列长度 */
  column_length?: string;
  /** 列默认值 */
  column_default?: string;
  /** PYTHON类型 */
  python_type?: string;
  /** PYTHON字段名 */
  python_field?: string;
  /** 是否主键（1是） */
  is_pk?: boolean;
  /** 是否自增（1是） */
  is_increment?: boolean;
  /** 是否必填（1是） */
  is_nullable?: boolean;
  /** 是否唯一（1是） */
  is_unique?: boolean;
  /** 是否为新增字段（1是） */
  is_insert?: boolean;
  /** 是否编辑字段（1是） */
  is_edit?: boolean;
  /** 是否列表字段（1是） */
  is_list?: boolean;
  /** 是否查询字段（1是） */
  is_query?: boolean;
  /** 查询方式（等于、不等于、大于、小于、范围） */
  query_type?: string;
  /** 显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件） */
  html_type?: string;
  /** 字典类型 */
  dict_type?: string;
  /** 排序 */
  sort?: number;
  created_by?: creatorType;
  updated_by?: updatorType;
}
