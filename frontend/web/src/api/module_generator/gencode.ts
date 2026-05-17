import { request } from "@utils";

const API_PATH = "/generator/gencode";

const GencodeAPI = {
  // 查询生成表数据
  listTable(query: GenTablePageQuery) {
    return request<ApiResponse<PageResult<GenTableSchema>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 查询db数据库列表
  listDbTable(query: DBTablePageQuery) {
    return request<ApiResponse<PageResult<DBTableSchema>>>({
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

  // 创建表（与后端 GenCreateTableSqlBody 一致）
  createTable(sql: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: { sql },
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

  // 同步数据库差异预览（不落库）
  syncDbPreview(table_name: string) {
    return request<ApiResponse<GenSyncPreviewSchema>>({
      url: `${API_PATH}/sync_db/preview/${table_name}`,
      method: "get",
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

/** 业务表结构 */
export interface GenTableSchema extends BaseType {
  table_name?: string;
  table_comment?: string;
  class_name?: string;
  package_name?: string;
  module_name?: string;
  business_name?: string;
  function_name?: string;
  description?: string;
  parent_menu_id?: number;
  sub?: boolean;
  sub_table_name?: string;
  sub_table_fk_name?: string;
  master_sub_hint?: string | null;
  pk_column?: GenTableColumnSchema;
  columns: GenTableColumnSchema[];
  sub_table?: GenTableSchema;
}

export interface GenTableColumnSchema extends BaseType {
  table_id?: number;
  column_name?: string;
  column_comment?: string;
  column_type?: string;
  column_length?: string;
  column_default?: string;
  is_pk?: boolean;
  is_increment?: boolean;
  is_nullable?: boolean;
  is_unique?: boolean;
  sort?: number;
  python_type?: string;
  python_field?: string;
  html_type?: string | null;
  dict_type?: string;
  is_insert?: boolean | null;
  is_edit?: boolean | null;
  is_list?: boolean | null;
  is_query?: boolean | null;
  query_type?: string | null;
}

/** 查询参数：生成表 */
export interface GenTablePageQuery extends PageQuery {
  table_name?: string;
  table_comment?: string;
}

/** 查询参数：DB 表 */
export interface DBTablePageQuery extends PageQuery {
  table_name?: string;
  table_comment?: string;
}

export interface DBTableSchema {
  table_name: string;
  table_comment?: string;
  create_time?: string;
  update_time?: string;
}

export interface GenSyncColumnChange {
  column_name: string;
  before?: Record<string, any> | null;
  after?: Record<string, any> | null;
  changed_keys?: string[];
}

export interface GenSyncPreviewSchema {
  table_name: string;
  added: string[];
  removed: string[];
  unchanged: string[];
  changed: GenSyncColumnChange[];
  sub_tables?: GenSyncPreviewSchema[];
}
