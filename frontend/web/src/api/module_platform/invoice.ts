import { request } from "@utils";

const PLATFORM_API = "/platform/invoice";
const TENANT_API = "/platform/tenant/invoice";

const InvoiceAPI = {
  // ─── 平台端 ───
  listInvoices(query?: InvoicePageQuery) {
    return request<ApiResponse<{ list: InvoiceTable[]; total: number }>>({
      url: `${PLATFORM_API}/list`,
      method: "get",
      params: query,
    });
  },

  issueInvoice(invoiceId: number, body: { pdf_url?: string; api_response?: string }) {
    return request<ApiResponse>({
      url: `${PLATFORM_API}/issue/${invoiceId}`,
      method: "put",
      data: body,
    });
  },

  voidInvoice(invoiceId: number, reason?: string) {
    return request<ApiResponse>({
      url: `${PLATFORM_API}/void/${invoiceId}`,
      method: "put",
      data: { description: reason },
    });
  },

  // ─── 租户端 ───
  tenantListInvoices(query?: InvoicePageQuery) {
    return request<ApiResponse<{ list: InvoiceTable[]; total: number }>>({
      url: `${TENANT_API}/list`,
      method: "get",
      params: query,
    });
  },

  applyInvoice(body: InvoiceApplyForm) {
    return request<ApiResponse>({
      url: `${TENANT_API}/apply`,
      method: "post",
      data: body,
    });
  },

  downloadInvoice(invoiceId: number) {
    return request<Blob>({
      url: `${TENANT_API}/${invoiceId}/download`,
      method: "get",
      responseType: "blob",
    });
  },
};

export default InvoiceAPI;

export interface InvoicePageQuery extends PageQuery, TenantByQueryParams {
  invoice_type?: string;
}

export interface InvoiceTable {
  id: number;
  tenant_id: number;
  order_id: number;
  invoice_no: string;
  invoice_type: string;
  title: string;
  tax_no?: string;
  amount: number;
  tax_amount: number;
  status: number;
  bank_info?: string;
  address_info?: string;
  pdf_url?: string;
  oss_license_pdf_url?: string;
  api_response?: string;
  description?: string;
  created_time?: string;
}

export interface InvoiceApplyForm {
  order_id: number;
  invoice_type: string;
  title: string;
  tax_no?: string;
  address_info?: string;
  bank_info?: string;
  description?: string;
}
