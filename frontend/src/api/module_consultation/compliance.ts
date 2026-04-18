import request from "@/utils/request";

const API_PATH = "/consultation";

const ComplianceAPI = {
  getDiagnosisDetail(id: number) {
    return request<ApiResponse<DiagnosisItem>>({
      url: `${API_PATH}/diagnosis/detail/${id}`,
      method: "get",
    });
  },

  getDiagnosisList(params: DiagnosisQuery) {
    return request<ApiResponse<PageResult<DiagnosisItem[]>>>({
      url: `${API_PATH}/diagnosis/list`,
      method: "get",
      params,
    });
  },

  createDiagnosis(data: DiagnosisForm) {
    return request<ApiResponse<DiagnosisItem>>({
      url: `${API_PATH}/diagnosis/create`,
      method: "post",
      data,
    });
  },

  updateDiagnosis(id: number, data: DiagnosisForm) {
    return request<ApiResponse<DiagnosisItem>>({
      url: `${API_PATH}/diagnosis/update/${id}`,
      method: "put",
      data,
    });
  },

  deleteDiagnosis(id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/diagnosis/delete/${id}`,
      method: "delete",
    });
  },

  batchDeleteDiagnosis(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/diagnosis/batch-delete`,
      method: "delete",
      data: ids,
    });
  },

  getLatestDiagnosis(consultationId: number) {
    return request<ApiResponse<DiagnosisItem>>({
      url: `${API_PATH}/diagnosis/latest/${consultationId}`,
      method: "get",
    });
  },

  checkCompliance(consultationId: number) {
    return request<ApiResponse<CheckResult>>({
      url: `${API_PATH}/diagnosis/check`,
      method: "post",
      data: { consultation_id: consultationId },
    });
  },

  getRuleDetail(id: number) {
    return request<ApiResponse<RuleItem>>({
      url: `${API_PATH}/rule/detail/${id}`,
      method: "get",
    });
  },

  getRuleList(params: RuleQuery) {
    return request<ApiResponse<PageResult<RuleItem[]>>>({
      url: `${API_PATH}/rule/list`,
      method: "get",
      params,
    });
  },

  createRule(data: RuleForm) {
    return request<ApiResponse<RuleItem>>({
      url: `${API_PATH}/rule/create`,
      method: "post",
      data,
    });
  },

  updateRule(id: number, data: RuleForm) {
    return request<ApiResponse<RuleItem>>({
      url: `${API_PATH}/rule/update/${id}`,
      method: "put",
      data,
    });
  },

  deleteRule(id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/rule/delete/${id}`,
      method: "delete",
    });
  },

  batchDeleteRule(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/rule/batch-delete`,
      method: "delete",
      data: ids,
    });
  },

  toggleRuleStatus(id: number) {
    return request<ApiResponse<RuleItem>>({
      url: `${API_PATH}/rule/toggle/${id}`,
      method: "post",
    });
  },
};

export default ComplianceAPI;

export interface DiagnosisQuery extends PageQuery {
  consultation_id?: number;
  compliance_level?: string;
  is_high_risk?: boolean;
}

export interface DiagnosisForm {
  consultation_id: number;
  compliance_score: number;
  compliance_level: string;
  risk_factors?: string[];
  diagnosis_details?: any;
  improvement_suggestions?: string[];
  is_high_risk?: boolean;
  risk_warning?: string;
}

export interface DiagnosisItem extends DiagnosisForm, BaseType {
  diagnosis_time: string;
  is_latest: boolean;
}

export interface RuleQuery extends PageQuery {
  name?: string;
  rule_type?: string;
  risk_level?: string;
  is_active?: boolean;
}

export interface RuleForm {
  name: string;
  description?: string;
  rule_type: string;
  rule_condition: any;
  rule_weight?: number;
  risk_level: string;
  is_active?: boolean;
  order?: number;
}

export interface RuleItem extends RuleForm, BaseType {}

export interface CheckResult {
  consultation_id: number;
  compliance_score: number;
  compliance_level: string;
  risk_factors: string[];
  improvement_suggestions: string[];
  is_high_risk: boolean;
  passed_rules: string[];
  failed_rules: string[];
}
