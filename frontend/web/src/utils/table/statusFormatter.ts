/**
 * 表格列 status formatter 工具函数
 *
 * 解决项目里 50+ 处 `h(ElTag, { type }, () => text)` 重复模式。
 *
 * 用法：
 *   import { makeStatusFormatter } from "@utils";
 *   import { h } from "vue";
 *
 *   // 1) 二元状态（最常见）
 *   formatter: makeStatusFormatter({
 *     value: row.status,
 *     map: {
 *       0: { type: "success", text: "启用" },
 *       1: { type: "danger", text: "停用" },
 *     },
 *   })
 *
 *   // 2) 自定义渲染（更复杂场景）
 *   formatter: (row) => h(StatusTag, { type: "primary", label: row.dict_type })
 *
 *   // 3) 整列快捷配置（推荐；自动生成 formatter）：
 *   columnsFactory: () => resolveStatusColumns(() => [
 *     { prop: "status", label: "状态", width: 88, status: {
 *       0: { type: "success", text: "启用" },
 *       1: { type: "danger", text: "停用" },
 *     }},
 *   ])
 */
import { h, type VNode } from "vue";
import StatusTag from "@/components/others/fa-status-tag/index.vue";
import type { ColumnOption, StatusColumnConfig } from "@/types/component";

/** ElTag 支持的 type */
export type StatusType = "primary" | "success" | "warning" | "danger" | "info";

/** 单个状态配置 */
export interface StatusItem {
  /** ElTag 类型 */
  type: StatusType;
  /** 显示文本 */
  text: string;
  /** 可选：size（默认 "default"） */
  size?: "large" | "default" | "small";
  /** 可选：theme effect（默认 "light"） */
  effect?: "light" | "dark" | "plain";
}

/** 状态映射：value -> StatusItem */
export type StatusMap = Record<string | number, StatusItem>;

/**
 * 创建表格列 formatter：根据 value 查找对应状态配置并渲染 StatusTag
 *
 * @param options.valueGetter 从 row 取出要匹配的 value（默认直接取 row 本身）
 * @param options.map value -> { type, text } 映射
 * @param options.fallback 未匹配时的回退（默认 { type: "info", text: "—" }）
 */
export function makeStatusFormatter<T = Record<string, unknown>>(
  options:
    | {
        valueGetter: (row: T) => unknown;
        map: StatusMap;
        fallback?: StatusItem;
      }
    | {
        map: StatusMap;
        fallback?: StatusItem;
      }
): (row: T) => VNode {
  // 重载 2：传了 valueGetter
  if ("valueGetter" in options) {
    const { valueGetter, map, fallback } = options;
    const fb: StatusItem = fallback ?? { type: "info", text: "—" };
    return (row: T) => {
      const value = valueGetter(row);
      const item = map[value as string | number] ?? fb;
      return h(StatusTag, {
        type: item.type,
        label: item.text,
        size: item.size,
        effect: item.effect,
      });
    };
  }
  // 重载 1：value 就是 row 本身
  const { map, fallback } = options as { map: StatusMap; fallback?: StatusItem };
  const fb: StatusItem = fallback ?? { type: "info", text: "—" };
  return (row: T) => {
    const item = map[row as unknown as string | number] ?? fb;
    return h(StatusTag, {
      type: item.type,
      label: item.text,
    });
  };
}

/**
 * 把 ColumnOption.status 快捷配置转换为 formatter。
 *
 * 用法（在 columnsFactory 里包一层）：
 *   columnsFactory: () => resolveStatusColumns(() => [
 *     { prop: "status", label: "状态", width: 88, status: { 0: { type: "success", text: "启用" }, 1: { type: "danger", text: "停用" } } },
 *   ])
 *
 * 行为：
 * - 已有 formatter 的列：保留 formatter（用户显式优先）
 * - 有 status 但无 formatter：根据 prop 从 row 取值并渲染 StatusTag
 * - 无 status 的列：原样返回
 */
export function resolveStatusColumns<T = Record<string, unknown>>(
  factory: () => ColumnOption<T>[]
): () => ColumnOption<T>[] {
  return () => {
    const cols = factory();
    return cols.map((col) => {
      if (!col.status || col.formatter) return col;
      const map: StatusColumnConfig = col.status;
      return {
        ...col,
        formatter: (row: T) => {
          const rawValue = col.prop ? (row as Record<string, unknown>)[col.prop] : row;
          // boolean 值转换为字符串键进行查找
          const value = typeof rawValue === "boolean" ? String(rawValue) : rawValue;
          const item = map[value as string | number] ?? { type: "info" as const, text: "—" };
          return h(StatusTag, {
            type: item.type,
            label: item.text,
            size: item.size,
            effect: item.effect,
          });
        },
        status: undefined,
      };
    });
  };
}
