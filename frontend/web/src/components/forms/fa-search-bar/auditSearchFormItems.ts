import type { SearchFormItem } from "./index.vue";

/** 与创建/更新人、时间范围配套的后端查询字段（可与其他业务条件组合） */
export type AuditSearchFormParams = {
  created_id?: number | null;
  updated_id?: number | null;
  created_time?: string[];
  updated_time?: string[];
};

export interface GetAuditSearchFormItemsOptions {
  /** 栅格列宽，与 FaSearchBar `span` 一致时建议传相同值，默认 6 */
  span?: number;
  createdByLabel?: string;
  updatedByLabel?: string;
  createdTimeLabel?: string;
  updatedTimeLabel?: string;
  createdByPlaceholder?: string;
  updatedByPlaceholder?: string;
  /** 日期时间范围 valueFormat，默认 YYYY-MM-DD HH:mm:ss */
  valueFormat?: string;
  rangeSeparator?: string;
  startPlaceholder?: string;
  endPlaceholder?: string;
}

/**
 * 常见「创建人 / 更新人 / 创建时间 / 更新时间」搜索项，供 FaSearchBar `items` 使用。
 * 当 FaSearchBar 设置 `includeAudit` 为 true 时，会自动追加这四个字段。
 * 创建人、更新人插槽由 FaSearchBar 内置提供，也可通过 `#created_id`、`#updated_id` 覆盖。
 */
export function getAuditSearchFormItems(
  options?: GetAuditSearchFormItemsOptions
): SearchFormItem[] {
  const span = options?.span ?? 6;
  const valueFormat = options?.valueFormat ?? "YYYY-MM-DD HH:mm:ss";
  const rangeSep = options?.rangeSeparator ?? "至";
  const sp = options?.startPlaceholder ?? "开始";
  const ep = options?.endPlaceholder ?? "结束";

  return [
    {
      label: options?.createdByLabel ?? "创建人",
      key: "created_id",
      type: "input",
      props: {
        placeholder: options?.createdByPlaceholder ?? "请选择创建人",
        style: { width: "100%" },
      },
      span,
    },
    {
      label: options?.updatedByLabel ?? "更新人",
      key: "updated_id",
      type: "input",
      props: {
        placeholder: options?.updatedByPlaceholder ?? "请选择更新人",
        style: { width: "100%" },
      },
      span,
    },
    {
      label: options?.createdTimeLabel ?? "创建时间",
      key: "created_time",
      type: "datetimerange",
      props: {
        style: { width: "100%" },
        type: "datetimerange",
        rangeSeparator: rangeSep,
        startPlaceholder: sp,
        endPlaceholder: ep,
        valueFormat,
      },
      span,
    },
    {
      label: options?.updatedTimeLabel ?? "更新时间",
      key: "updated_time",
      type: "datetimerange",
      props: {
        style: { width: "100%" },
        type: "datetimerange",
        rangeSeparator: rangeSep,
        startPlaceholder: sp,
        endPlaceholder: ep,
        valueFormat,
      },
      span,
    },
  ];
}
