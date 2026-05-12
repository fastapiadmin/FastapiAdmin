import request from "@/utils/request";

const API_PATH = "/consultation/info-collection";

const ConsultationInfoAPI = {
  /** 获取咨询会信息详情 */
  getDetail(id: number) {
    return request<ApiResponse<ConsultationInfoItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  /** 获取咨询会信息列表 */
  getList(params: ConsultationInfoQuery) {
    return request<ApiResponse<PageResult<ConsultationInfoItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  /** 创建咨询会信息 */
  create(data: ConsultationInfoForm) {
    return request<ApiResponse<ConsultationInfoItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  /** 更新咨询会信息 */
  update(id: number, data: ConsultationInfoForm) {
    return request<ApiResponse<ConsultationInfoItem>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data,
    });
  },

  /** 删除咨询会信息 */
  delete(id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete/${id}`,
      method: "delete",
    });
  },

  /** 批量删除咨询会信息 */
  batchDelete(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/batch-delete`,
      method: "delete",
      data: ids,
    });
  },

  /** 审核通过 */
  approve(id: number, reviewComment?: string) {
    return request<ApiResponse<ConsultationInfoItem>>({
      url: `${API_PATH}/approve/${id}`,
      method: "post",
      params: { review_comment: reviewComment },
    });
  },

  /** 审核拒绝 */
  reject(id: number, reviewComment: string) {
    return request<ApiResponse<ConsultationInfoItem>>({
      url: `${API_PATH}/reject/${id}`,
      method: "post",
      params: { review_comment: reviewComment },
    });
  },

  /** 归档 */
  archive(id: number) {
    return request<ApiResponse<ConsultationInfoItem>>({
      url: `${API_PATH}/archive/${id}`,
      method: "post",
    });
  },

  /** 更新合规评分 */
  updateComplianceScore(
    id: number,
    data: {
      compliance_score: number;
      compliance_level: string;
      risk_factors?: string[];
    }
  ) {
    return request<ApiResponse<ConsultationInfoItem>>({
      url: `${API_PATH}/compliance-score/${id}`,
      method: "post",
      data,
    });
  },

  /** 手动触发爬虫抓取 */
  crawl() {
    return request<ApiResponse<CrawlResult>>({
      url: `${API_PATH}/crawl`,
      method: "post",
    });
  },

  /** 获取已审核咨询会下拉选项 */
  getApprovedOptions() {
    return request<ApiResponse<ConsultationOption[]>>({
      url: `${API_PATH}/approved-options`,
      method: "get",
    });
  },
};

export default ConsultationInfoAPI;

/** 咨询会信息查询参数 */
export interface ConsultationInfoQuery extends PageQuery {
  /** 标题 */
  title?: string;
  /** 主办方 */
  organizer?: string;
  /** 省份 */
  province?: string;
  /** 城市 */
  city?: string;
  /** 开始日期范围-开始 */
  start_date_begin?: string;
  /** 开始日期范围-结束 */
  start_date_end?: string;
  /** 状态 */
  status?: string;
  /** 信息来源 */
  source_type?: string;
  /** 是否归档 */
  is_archived?: boolean;
  /** 创建时间范围 */
  created_time?: string[];
  /** 开始日期范围（前端搜索用） */
  start_date_range?: string[];
}

/** 咨询会信息表单 */
export interface ConsultationInfoForm {
  /** 标题 */
  title: string;
  /** 描述 */
  description?: string;
  /** 主办方 */
  organizer: string;
  /** 主办方类型 */
  organizer_type?: string;
  /** 开始日期 */
  start_date: string;
  /** 结束日期 */
  end_date?: string;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
  /** 省份 */
  province?: string;
  /** 城市 */
  city?: string;
  /** 区县 */
  district?: string;
  /** 详细地址 */
  address?: string;
  /** 参与高校列表 */
  participating_universities?: {
    id: number;
    name: string;
    code?: string;
  }[];
  /** 预计参观人数 */
  estimated_visitors?: number;
  /** 展位费用 */
  booth_fee?: number;
  /** 信息来源 */
  source_type?: string;
  /** 来源链接 */
  source_url?: string;
}

/** 咨询会信息项 */
export interface ConsultationInfoItem extends ConsultationInfoForm, BaseType {
  /** UUID */
  uuid: string;
  /** 参与高校数量 */
  university_count: number;
  /** 状态 */
  status: string;
  /** 审核意见 */
  review_comment?: string;
  /** 审核人ID */
  reviewed_by?: number;
  /** 审核时间 */
  reviewed_time?: string;
  /** 合规评分 */
  compliance_score?: number;
  /** 合规等级 */
  compliance_level?: string;
  /** 风险因素列表 */
  risk_factors?: string[];
  /** 是否归档 */
  is_archived: boolean;
  /** 归档时间 */
  archived_time?: string;
  /** 归档人ID */
  archived_by?: number;
  /** 创建人 */
  created_by?: CommonType;
  /** 更新人 */
  updated_by?: CommonType;
  /** 创建时间 */
  created_time: string;
  /** 更新时间 */
  updated_time: string;
}

/** 爬虫抓取结果 */
export interface CrawlResult {
  /** 抓取总数 */
  total_fetched: number;
  /** 保存成功数 */
  total_saved: number;
  /** 跳过重复数 */
  total_skipped: number;
}

/** 咨询会下拉选项 */
export interface ConsultationOption {
  /** 咨询会ID */
  id: number;
  /** 咨询会标题 */
  title: string;
  /** 开始日期 */
  start_date: string;
  /** 结束日期 */
  end_date?: string;
  /** 城市 */
  city?: string;
  /** 详细地址 */
  address?: string;
}
