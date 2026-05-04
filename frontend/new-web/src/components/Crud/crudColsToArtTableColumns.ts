import dayjs from "dayjs";
import type { ColumnOption } from "@/types/component";
import type { IContentConfig } from "./types";

type CrudCol = IContentConfig["cols"][number];

/** 不参与透传给 ElTableColumn 的 Crud 扩展字段 */
const CRUD_META_KEYS = new Set([
  "templet",
  "slotName",
  "selectList",
  "dateFormat",
  "operat",
  "imageWidth",
  "imageHeight",
  "priceFormat",
  "activeValue",
  "inactiveValue",
  "activeText",
  "inactiveText",
  "inputType",
  "initFn",
  "disabled",
]);

function passthroughColumn(col: CrudCol): ColumnOption {
  const raw = col as Record<string, unknown>;
  const out: Record<string, unknown> = {};
  for (const key of Object.keys(raw)) {
    if (CRUD_META_KEYS.has(key)) continue;
    if (key === "show") continue;
    out[key] = raw[key];
  }
  if (col.show !== undefined) {
    out.checked = col.show;
    out.visible = col.show;
  }
  return out as ColumnOption;
}

/**
 * 将 Crud `cols` 转为 ArtTable / ArtTableHeader 使用的 `ColumnOption[]`。
 * - `templet: custom` → `useSlot`
 * - `templet: date` → `formatter`（dayjs）
 * - `templet: list` → `formatter`（selectList）
 * - 其余带 `templet` 且无法在 Art 列模型表达的，仍走 `useSlot`，由页面提供同名插槽
 */
export function mapCrudColsToArtColumns(items: CrudCol[]): ColumnOption[] {
  const out: ColumnOption[] = [];

  for (const col of items) {
    if (col.show === false) continue;

    if (col.type === "selection" || col.type === "index") {
      out.push(passthroughColumn(col));
      continue;
    }

    const base = passthroughColumn(col);

    if (col.templet === "custom" && col.prop) {
      out.push({
        ...base,
        useSlot: true,
        slotName: col.slotName ?? col.prop,
      });
      continue;
    }

    if (col.templet === "date" && col.prop) {
      const fmt = col.dateFormat ?? "YYYY-MM-DD HH:mm:ss";
      const prop = col.prop;
      out.push({
        ...base,
        formatter: (row: Record<string, unknown>) => {
          const v = row[prop];
          return v ? dayjs(v as string | number | Date).format(fmt) : "";
        },
      });
      continue;
    }

    if (col.templet === "list" && col.prop && col.selectList) {
      const prop = col.prop;
      const sl = col.selectList as Record<string, unknown>;
      out.push({
        ...base,
        formatter: (row: Record<string, unknown>) =>
          sl[row[prop] as string] != null ? String(sl[row[prop] as string]) : "",
      });
      continue;
    }

    if (!col.templet) {
      out.push(base);
      continue;
    }

    /* 其余 templet 优先走单元格展示兜底（复杂控件请改用 templet: custom + 插槽，或继续使用 legacy 表格） */
    if (col.prop) {
      out.push({
        ...base,
        formatter: (row: Record<string, unknown>) => row[col.prop!] ?? "",
      });
    } else {
      out.push(base);
    }
  }

  return out;
}
