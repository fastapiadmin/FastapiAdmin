/**
 * 表单组件公共组合式函数 —— 提取 FaForm 与 FaSearchBar 的共享逻辑。
 *
 * 共享函数：cloneModelValue / isRichTextEmpty / sanitizeOutputValue / getProps / getSlots / getColSpan
 */
import { computed, toRaw, type Component } from "vue";
import { type VNode } from "vue";
import { calculateResponsiveSpan, type ResponsiveBreakpoint } from "@utils";

// ── 类型定义 ──

export interface FormItemBase {
  key: string;
  label?: string | (() => VNode) | Component;
  labelWidth?: string | number;
  type?: string;
  hidden?: boolean;
  span?: number;
  slots?: Record<string, (() => any) | undefined>;
  props?: Record<string, any>;
  [key: string]: any;
}

export interface SanitizeOutputOptions {
  removeEmptyString: boolean;
  removeEmptyArray: boolean;
  removeEmptyObject: boolean;
  removeEmptyRichText: boolean;
  keepZero: boolean;
  keepFalse: boolean;
}

/** 传递给组件时需排除的表单配置属性 */
const ROOT_PROPS = ["label", "labelWidth", "key", "type", "hidden", "span", "slots"];

/** 日期选择器类型列表（getProps 中用于传递 type 到 FaDatePicker） */
const DATE_PICKER_TYPES = ["date", "daterange", "datetime", "datetimerange", "monthrange"];

// ── 公共函数 ──

/**
 * 深拷贝表单数据（toRaw + 递归，避免 getSanitizedOutput 残留响应式代理）
 */
export const cloneModelValue = (value: Record<string, any> | undefined): Record<string, any> => {
  if (!value) return {};

  const deepClone = (source: unknown): unknown => {
    if (Array.isArray(source)) {
      return source.map((item) => deepClone(item));
    }

    if (source && typeof source === "object") {
      const rawSource = toRaw(source);
      return Object.keys(rawSource).reduce<Record<string, unknown>>((accumulator, key) => {
        accumulator[key] = deepClone((rawSource as Record<string, unknown>)[key]);
        return accumulator;
      }, {});
    }

    return source;
  };

  return deepClone(toRaw(value)) as Record<string, any>;
};

/**
 * 判断富文本内容是否仅包含占位标签（空内容）
 */
export const isRichTextEmpty = (value: string): boolean => {
  if (/<(img|video|audio|iframe|embed|object)\b/i.test(value)) {
    return false;
  }

  return (
    value
      .replace(/&nbsp;/gi, "")
      .replace(/<br\s*\/?>/gi, "")
      .replace(/<[^>]*>/g, "")
      .trim() === ""
  );
};

/**
 * 清洗输出值 —— 按配置移除空字符串/空数组/空对象/空富文本
 */
export const sanitizeOutputValue = (value: unknown, options: SanitizeOutputOptions): unknown => {
  if (Array.isArray(value)) {
    const sanitizedArray = value
      .map((item) => sanitizeOutputValue(item, options))
      .filter((item) => item !== undefined);
    return sanitizedArray.length === 0 && options.removeEmptyArray ? undefined : sanitizedArray;
  }

  if (value && typeof value === "object") {
    const rawValue = toRaw(value);
    const sanitizedObject = Object.entries(rawValue).reduce<Record<string, unknown>>(
      (accumulator, [key, item]) => {
        const sanitizedItem = sanitizeOutputValue(item, options);
        if (sanitizedItem !== undefined) {
          accumulator[key] = sanitizedItem;
        }
        return accumulator;
      },
      {}
    );
    return Object.keys(sanitizedObject).length === 0 && options.removeEmptyObject
      ? undefined
      : sanitizedObject;
  }

  if (typeof value === "string") {
    if (options.removeEmptyString && value.trim() === "") {
      return undefined;
    }
    if (options.removeEmptyRichText && isRichTextEmpty(value)) {
      return undefined;
    }
    return value;
  }

  if (value === 0) {
    return options.keepZero ? value : undefined;
  }

  if (value === false) {
    return options.keepFalse ? value : undefined;
  }

  return value ?? undefined;
};

/**
 * 构建清洗配置 computed，与组件 props.sanitizeOutput 合并默认值
 */
export const useSanitizeOutputOptions = (sanitizeOutput: Partial<SanitizeOutputOptions>) => {
  return computed<SanitizeOutputOptions>(() => ({
    removeEmptyString: true,
    removeEmptyArray: true,
    removeEmptyObject: true,
    removeEmptyRichText: true,
    keepZero: true,
    keepFalse: true,
    ...sanitizeOutput,
  }));
};

/**
 * 获取组件 props —— 从 FormItem 中分离表单配置属性，保留组件所需属性
 */
export const getProps = (item: FormItemBase): Record<string, any> => {
  if (item.props) {
    const props = { ...item.props };
    if (item.type && DATE_PICKER_TYPES.includes(item.type) && !props.type) {
      props.type = item.type;
    }
    return props;
  }

  const props = { ...item };
  ROOT_PROPS.forEach((key) => delete (props as Record<string, any>)[key]);

  // 日期选择器需要传递 type 到 FaDatePicker
  if (item.type && DATE_PICKER_TYPES.includes(item.type) && !props.type) {
    props.type = item.type;
  }

  return props;
};

/**
 * 获取插槽 —— 过滤掉未定义的插槽
 */
export const getSlots = (item: FormItemBase): Record<string, () => any> => {
  if (!item.slots) return {};
  const validSlots: Record<string, () => any> = {};
  Object.entries(item.slots).forEach(([key, slotFn]) => {
    if (slotFn) {
      validSlots[key] = slotFn;
    }
  });
  return validSlots;
};

/**
 * 获取列宽 span 值 —— 根据屏幕尺寸智能降级
 */
export const getColSpan = (
  itemSpan: number | undefined,
  span: number,
  breakpoint: ResponsiveBreakpoint
): number => {
  return calculateResponsiveSpan(itemSpan, span, breakpoint);
};
