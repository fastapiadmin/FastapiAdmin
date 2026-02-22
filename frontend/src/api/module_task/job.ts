import request from "@/utils/request";

const API_PATH = "/task/job";

const JobAPI = {
  getSchedulerStatus() {
    return request<ApiResponse<SchedulerStatus>>({
      url: `${API_PATH}/scheduler/status`,
      method: "get",
    });
  },

  getSchedulerJobs() {
    return request<ApiResponse<SchedulerJob[]>>({
      url: `${API_PATH}/scheduler/jobs`,
      method: "get",
    });
  },

  startScheduler() {
    return request<ApiResponse>({
      url: `${API_PATH}/scheduler/start`,
      method: "post",
    });
  },

  pauseScheduler() {
    return request<ApiResponse>({
      url: `${API_PATH}/scheduler/pause`,
      method: "post",
    });
  },

  resumeScheduler() {
    return request<ApiResponse>({
      url: `${API_PATH}/scheduler/resume`,
      method: "post",
    });
  },

  shutdownScheduler() {
    return request<ApiResponse>({
      url: `${API_PATH}/scheduler/shutdown`,
      method: "post",
    });
  },

  clearAllJobs() {
    return request<ApiResponse>({
      url: `${API_PATH}/scheduler/jobs/clear`,
      method: "delete",
    });
  },

  getSchedulerConsole() {
    return request<ApiResponse<string>>({
      url: `${API_PATH}/scheduler/console`,
      method: "get",
    });
  },

  syncJobsToDb() {
    return request<ApiResponse<number>>({
      url: `${API_PATH}/scheduler/sync`,
      method: "post",
    });
  },

  pauseJob(jobId: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/task/pause/${jobId}`,
      method: "post",
    });
  },

  resumeJob(jobId: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/task/resume/${jobId}`,
      method: "post",
    });
  },

  runJobNow(jobId: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/task/run/${jobId}`,
      method: "post",
    });
  },

  removeJob(jobId: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/task/remove/${jobId}`,
      method: "delete",
    });
  },

  getJobLogList(query: JobLogPageQuery) {
    return request<ApiResponse<PageResult<JobLogTable[]>>>({
      url: `${API_PATH}/log/list`,
      method: "get",
      params: query,
    });
  },

  getJobLogDetail(id: number) {
    return request<ApiResponse<JobLogTable>>({
      url: `${API_PATH}/log/detail/${id}`,
      method: "get",
    });
  },

  deleteJobLog(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/log/delete`,
      method: "delete",
      data: ids,
    });
  },

  clearJobLog() {
    return request<ApiResponse>({
      url: `${API_PATH}/log/clear`,
      method: "delete",
    });
  },
};

export default JobAPI;

export interface SchedulerStatus {
  status: string;
  is_running: boolean;
  job_count: number;
}

export interface SchedulerJob {
  id: string;
  name: string;
  trigger: string;
  next_run_time?: string;
  status: string;
}

export interface JobLogPageQuery extends PageQuery {
  job_id?: string;
  job_name?: string;
  status?: string;
  trigger_type?: string;
}

export interface JobLogTable extends BaseType {
  job_id: string;
  job_name?: string;
  trigger_type?: string;
  status: string;
  result?: string;
  error?: string;
  created_time?: string;
  updated_time?: string;
}
