import request from "@/utils/request";

const API_PATH = "/application/job";

const JobAPI = {
  listJob(query: JobPageQuery) {
    return request<ApiResponse<PageResult<JobTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailJob(query: number) {
    return request<ApiResponse<JobTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createJob(body: JobForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateJob(id: number, body: JobForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteJob(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  exportJob(body: JobPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  clearJob() {
    return request<ApiResponse>({
      url: `${API_PATH}/clear`,
      method: "delete",
    });
  },

  OptionJob(params: JobOptionData) {
    return request<ApiResponse>({
      url: `${API_PATH}/option`,
      method: "put",
      data: params,
    });
  },

  // 获取定时任务运行日志（实时状态）
  getJobRunLog() {
    return request<ApiResponse<JobRunLog[]>>({
      url: `${API_PATH}/log`,
      method: "get",
    });
  },

  // 获取定时任务日志详情
  detailJobLog(id: number) {
    return request<ApiResponse<JobLogDetail>>({
      url: `${API_PATH}/log/detail/${id}`,
      method: "get",
    });
  },

  // 查询定时任务日志列表
  listJobLog(query: JobLogPageQuery) {
    return request<ApiResponse<PageResult<JobLogTable[]>>>({
      url: `${API_PATH}/log/list`,
      method: "get",
      params: query,
    });
  },

  // 删除定时任务日志
  deleteJobLog(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/log/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 清空定时任务日志
  clearJobLog() {
    return request<ApiResponse>({
      url: `${API_PATH}/log/clear`,
      method: "delete",
    });
  },

  // 导出定时任务日志
  exportJobLog(query: JobLogPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/log/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },
};

export default JobAPI;

export interface JobPageQuery extends PageQuery {
  name?: string;
  status?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

export interface JobLogPageQuery extends PageQuery {
  job_id?: number;
  job_name?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
}

export interface JobOptionData {
  id?: number;
  option?: number; //操作类型 1: 暂停 2: 恢复 3: 重启
}

export interface JobTable extends BaseType {
  name: string;
  func?: string;
  trigger?: string;
  args?: string;
  kwargs?: string;
  coalesce?: boolean;
  max_instances?: number;
  jobstore?: string;
  executor?: string;
  trigger_args?: string;
  start_date?: string;
  end_date?: string;
  created_by?: creatorType;
  updated_by?: updatorType;
}

export interface JobForm extends BaseFormType {
  name?: string;
  func?: string;
  trigger?: string;
  args?: string;
  kwargs?: string;
  coalesce?: boolean;
  max_instances?: number;
  jobstore?: string;
  executor?: string;
  trigger_args?: string;
  start_date?: string;
  end_date?: string;
}

// 定时任务运行日志接口（对应Scheduler实时状态）
export interface JobRunLog extends BaseType {
  name: string;
  trigger: string;
  executor: string;
  func: string;
  func_ref: string;
  args: any[];
  kwargs: any;
  misfire_grace_time: number;
  coalesce: boolean;
  max_instances: number;
  next_run_time: string;
}

// 定时任务日志详情接口（对应数据库日志表）
export interface JobLogDetail extends BaseType {
  job_name: string;
  job_group: string;
  job_executor: string;
  invoke_target: string;
  job_args?: string;
  job_kwargs?: string;
  job_trigger?: string;
  job_message?: string;
  exception_info?: string;
}

// 定时任务日志列表接口（对应数据库日志表）
export interface JobLogTable extends BaseType {
  job_name: string;
  job_group: string;
  job_executor: string;
  invoke_target: string;
  job_args?: string;
  job_kwargs?: string;
  job_trigger?: string;
  job_message?: string;
  exception_info?: string;
}
