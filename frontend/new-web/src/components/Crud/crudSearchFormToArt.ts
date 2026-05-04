import type { SearchFormItem } from "@/components/Core/forms/art-search-bar/index.vue";
import type { IFormItems, ISearchComponent } from "./types";
import { unref } from "vue";

/**
 * 与 legacy `CrudSearch` onMounted 赋值逻辑一致，需在挂载 ArtSearchBar 之前同步执行，
 * 以便 ArtSearchBar 内部 `initialModelValue` 快照正确。
 */
export function createCrudSearchInitialParams(
  items: IFormItems<ISearchComponent>,
  getCustomComponent: (componentName: string) => unknown
): Record<string, unknown> {
  const q: Record<string, unknown> = {};
  for (const item of items) {
    if (getCustomComponent(item.type ?? "")) {
      q[item.prop] = item.initialValue ?? null;
    } else if (["input-tag", "custom-tag", "cascader"].includes(item?.type ?? "")) {
      q[item.prop] = Array.isArray(item.initialValue) ? item.initialValue : [];
    } else if (
      item.type === "date-picker" &&
      String(item.attrs?.type ?? "")
        .toLowerCase()
        .includes("range")
    ) {
      q[item.prop] = item.initialValue ?? [];
    } else if (item.type === "select") {
      q[item.prop] = item.initialValue !== undefined ? item.initialValue : null;
    } else if (item.type === "input-number") {
      q[item.prop] = item.initialValue ?? null;
    } else {
      q[item.prop] = item.initialValue ?? "";
    }
  }
  return q;
}

export type MapCrudSearchToArtOptions = {
  customComponents?: Record<string, any>;
  /** 筛选控件最大宽度，透传到各 `props.style.maxWidth`（`false` 表示不限制） */
  fieldMaxWidth?: string | false;
};

function artSpanFromCol(col: unknown): number | undefined {
  if (col && typeof col === "object" && "span" in col) {
    const s = (col as { span?: number }).span;
    return typeof s === "number" ? s : undefined;
  }
  return undefined;
}

function mapDatePickerType(attrs: IFormItems<ISearchComponent>[number]["attrs"]): string {
  const t = String(attrs?.type ?? "date").toLowerCase();
  if (t.includes("datetimerange")) return "datetimerange";
  if (t.includes("daterange")) return "daterange";
  if (t.includes("datetime")) return "datetime";
  return "date";
}

/**
 * 将 Crud `ISearchConfig.formItems` 转为 ArtSearchBar `items`。
 */
export function mapCrudSearchFormItemsToArt(
  formItems: IFormItems<ISearchComponent>,
  options?: MapCrudSearchToArtOptions
): SearchFormItem[] {
  const { customComponents, fieldMaxWidth } = options ?? {};

  const maxStyle =
    fieldMaxWidth === undefined || fieldMaxWidth === false
      ? undefined
      : { maxWidth: fieldMaxWidth };

  return formItems.map((item) => {
    const attrs = item.attrs ?? {};
    const prevStyle = attrs.style && typeof attrs.style === "object" ? attrs.style : {};
    const baseProps = {
      ...attrs,
      ...(maxStyle ? { style: { ...prevStyle, ...maxStyle } } : {}),
    };

    const custom = item.type ? customComponents?.[item.type as string] : undefined;
    if (custom) {
      return {
        key: item.prop,
        label: item.label,
        hidden: item.hidden,
        span: artSpanFromCol(item.col),
        render: custom,
        props: baseProps,
      };
    }

    const span = artSpanFromCol(item.col);
    const optsRaw = item.options ? unref(item.options) : undefined;
    const selectOptions = Array.isArray(optsRaw)
      ? optsRaw.map((o) => ({ label: o.label, value: o.value, ...o }))
      : undefined;

    switch (item.type) {
      case "input":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "input",
          props: baseProps,
        };
      case "select":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "select",
          props: { ...baseProps, ...(selectOptions ? { options: selectOptions } : {}) },
        };
      case "input-number":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "number",
          props: baseProps,
        };
      case "cascader":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "cascader",
          props: baseProps,
        };
      case "tree-select":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "treeselect",
          props: baseProps,
        };
      case "date-picker": {
        const artType = mapDatePickerType(item.attrs);
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: artType,
          props: baseProps,
        };
      }
      case "time-picker":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "timepicker",
          props: baseProps,
        };
      case "time-select":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "timeselect",
          props: baseProps,
        };
      case "input-tag":
      case "custom-tag":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "inputTag",
          props: baseProps,
        };
      case "radio":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "radiogroup",
          props: { ...baseProps, ...(selectOptions ? { options: selectOptions } : {}) },
        };
      case "checkbox":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "checkboxgroup",
          props: { ...baseProps, ...(selectOptions ? { options: selectOptions } : {}) },
        };
      case "switch":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "switch",
          props: baseProps,
        };
      case "rate":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "rate",
          props: baseProps,
        };
      case "slider":
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "slider",
          props: baseProps,
        };
      default:
        return {
          key: item.prop,
          label: item.label,
          hidden: item.hidden,
          span,
          type: "input",
          props: baseProps,
        };
    }
  });
}
