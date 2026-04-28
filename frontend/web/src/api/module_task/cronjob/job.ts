import request from '@/utils/http';

const API_PATH = '/task/cronjob/job';

const JobAPI = {
  /**
   * 获取任务调度器状态
   * @returns 任务调度器状态
   */
  getSchedulerStatus() {
    return request<ApiResponse<SchedulerStatus>>({
      url: `${API_PATH}/scheduler/status`,
      method: 'get',
    });
  },

  /**
   * 获取任务调度器所有任务
   * @returns 任务调度器所有任务
   */
  getSchedulerJobs() {
    return request<ApiResponse<SchedulerJob[]>>({
      url: `${API_PATH}/scheduler/jobs`,
      method: 'get',
    });
  },

  /**
   * 启动任务调度器
   */
  startScheduler() {
    return request({
      url: `${API_PATH}/scheduler/start`,
      method: 'post',
    });
  },

  /**
   * 暂停任务调度器
   */
  pauseScheduler() {
    return request({
      url: `${API_PATH}/scheduler/pause`,
      method: 'post',
    });
  },

  /**
   * 恢复任务调度器
   */
  resumeScheduler() {
    return request({
      url: `${API_PATH}/scheduler/resume`,
      method: 'post',
    });
  },

  /**
   * 关闭任务调度器
   */
  shutdownScheduler() {
    return request({
      url: `${API_PATH}/scheduler/shutdown`,
      method: 'post',
    });
  },

  /**
   * 清除所有任务
   */
  clearAllJobs() {
    return request({
      url: `${API_PATH}/scheduler/jobs/clear`,
      method: 'delete',
    });
  },

  /**
   * 获取任务调度器控制台输出
   * @returns 任务调度器控制台输出
   */
  getSchedulerConsole() {
    return request<ApiResponse<string>>({
      url: `${API_PATH}/scheduler/console`,
      method: 'get',
    });
  },

  /**
   * 同步任务到数据库
   * @returns 同步任务到数据库的记录数
   */
  syncJobsToDb() {
    return request<ApiResponse<number>>({
      url: `${API_PATH}/scheduler/sync`,
      method: 'post',
    });
  },

  /**
   * 暂停任务
   * @param jobId 任务ID
   */
  pauseJob(jobId: string) {
    return request({
      url: `${API_PATH}/task/pause/${jobId}`,
      method: 'post',
    });
  },

  /**
   * 恢复任务
   * @param jobId 任务ID
   */
  resumeJob(jobId: string) {
    return request({
      url: `${API_PATH}/task/resume/${jobId}`,
      method: 'post',
    });
  },

  /**
   * 立即运行任务
   * @param jobId 任务ID
   */
  runJobNow(jobId: string) {
    return request({
      url: `${API_PATH}/task/run/${jobId}`,
      method: 'post',
    });
  },

  /**
   * 删除任务
   * @param jobId 任务ID
   */
  removeJob(jobId: string) {
    return request({
      url: `${API_PATH}/task/remove/${jobId}`,
      method: 'delete',
    });
  },

  /**
   * 获取任务日志列表
   * @param query 查询参数
   * @returns 任务日志列表
   */
  getJobLogList(query: JobLogPageQuery) {
    return request<PageResult<JobLogTable[]>>({
      url: `${API_PATH}/log/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取任务日志详情
   * @param id 任务日志ID
   * @returns 任务日志详情
   */
  getJobLogDetail(id: number) {
    return request<ApiResponse<JobLogTable>>({
      url: `${API_PATH}/log/detail/${id}`,
      method: 'get',
    });
  },

  /**
   * 删除任务日志
   * @param ids 任务日志ID列表
   */
  deleteJobLog(ids: number[]) {
    return request({
      url: `${API_PATH}/log/delete`,
      method: 'delete',
      data: ids,
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
  next_run_time?: string;
  job_state?: string;
  result?: string;
  error?: string;
  created_time?: string;
  updated_time?: string;
}
