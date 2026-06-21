import { request } from "@utils";

const API_PATH = "/platform/email";

const EmailAPI = {
  // ─── SMTP 配置 ────────────────────────────────────────────
  listConfig(query?: EmailConfigPageQuery) {
    return request<ApiResponse<PageResult<EmailConfigTable>>>({
      url: `${API_PATH}/config/list`,
      method: "get",
      params: query,
    });
  },

  detailConfig(id: number) {
    return request<ApiResponse<EmailConfigTable>>({
      url: `${API_PATH}/config/detail/${id}`,
      method: "get",
    });
  },

  createConfig(body: EmailConfigCreateForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/config/create`,
      method: "post",
      data: body,
    });
  },

  updateConfig(id: number, body: EmailConfigUpdateForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/config/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteConfig(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/config/delete`,
      method: "delete",
      data: ids,
    });
  },

  testConfig(body: EmailTestForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/config/test`,
      method: "post",
      data: body,
    });
  },

  // ─── 邮件模板 ────────────────────────────────────────────
  listTemplate(query?: EmailTemplatePageQuery) {
    return request<ApiResponse<PageResult<EmailTemplateTable>>>({
      url: `${API_PATH}/template/list`,
      method: "get",
      params: query,
    });
  },

  detailTemplate(id: number) {
    return request<ApiResponse<EmailTemplateTable>>({
      url: `${API_PATH}/template/detail/${id}`,
      method: "get",
    });
  },

  createTemplate(body: EmailTemplateCreateForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/template/create`,
      method: "post",
      data: body,
    });
  },

  updateTemplate(id: number, body: EmailTemplateUpdateForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/template/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteTemplate(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/template/delete`,
      method: "delete",
      data: ids,
    });
  },

  // ─── 手动发送 ────────────────────────────────────────────
  sendEmail(body: EmailSendForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/send`,
      method: "post",
      data: body,
    });
  },

  // ─── 发送日志 ────────────────────────────────────────────
  listLog(query?: EmailLogPageQuery) {
    return request<ApiResponse<PageResult<EmailLogTable>>>({
      url: `${API_PATH}/log/list`,
      method: "get",
      params: query,
    });
  },
};

export default EmailAPI;

// ─── EmailConfig 类型 ──────────────────────────────────────

export interface EmailConfigPageQuery extends PageQuery, UserByQueryParams {
  name?: string;
  is_default?: boolean;
}

export interface EmailConfigTable extends BaseType {
  name: string;
  smtp_host: string;
  smtp_port: number;
  smtp_user: string;
  from_name: string;
  use_tls: boolean;
  is_default: boolean;
  timeout: number;
  status?: number;
  description?: string;
}

export interface EmailConfigCreateForm {
  name: string;
  smtp_host: string;
  smtp_port: number;
  smtp_user: string;
  smtp_password: string;
  from_name?: string;
  use_tls?: boolean;
  is_default?: boolean;
  timeout?: number;
  status?: number;
  description?: string;
}

export interface EmailConfigUpdateForm {
  name?: string;
  smtp_host?: string;
  smtp_port?: number;
  smtp_user?: string;
  smtp_password?: string;
  from_name?: string;
  use_tls?: boolean;
  is_default?: boolean;
  timeout?: number;
  status?: number;
  description?: string;
}

export interface EmailTestForm {
  config_id: number;
  to_email: string;
}

// ─── EmailTemplate 类型 ──────────────────────────────────────

export interface EmailTemplatePageQuery extends PageQuery, UserByQueryParams {
  name?: string;
  template_code?: string;
}

export interface EmailTemplateTable extends BaseType {
  name: string;
  template_code: string;
  subject: string;
  body_html: string;
  body_text?: string;
  variables?: string;
  status?: number;
  description?: string;
}

export interface EmailTemplateCreateForm {
  name: string;
  template_code: string;
  subject: string;
  body_html: string;
  body_text?: string;
  variables?: string;
  description?: string;
}

export interface EmailTemplateUpdateForm {
  name?: string;
  template_code?: string;
  subject?: string;
  body_html?: string;
  body_text?: string;
  variables?: string;
  description?: string;
}

// ─── EmailLog 类型 ──────────────────────────────────────────

export interface EmailLogPageQuery extends PageQuery, UserByQueryParams {
  to_email?: string;
  biz_type?: string;
  template_code?: string;
}

export interface EmailLogTable {
  id: number;
  config_id?: number;
  template_code?: string;
  to_email: string;
  to_name?: string;
  subject: string;
  biz_type: string;
  status: number;
  error_msg?: string;
  retry_count: number;
  tenant_id?: number;
  created_time?: string;
  sent_time?: string;
}

export interface EmailSendForm {
  to_email: string;
  to_name?: string;
  template_code: string;
  variables?: Record<string, unknown>;
  config_id?: number;
  biz_type?: string;
}
