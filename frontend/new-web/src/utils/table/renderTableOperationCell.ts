/**
 * 表格操作列：最多展示 `maxInline` 个 ArtButtonTable，其余收入 ArtButtonMore（与 demo 一致）。
 */
import { h } from "vue";
import type { VNode } from "vue";
import { ElTooltip } from "element-plus";
import ArtButtonTable from "@/components/Core/forms/art-button-table/index.vue";
import ArtButtonMore from "@/components/Core/forms/art-button-more/index.vue";
import type { ButtonMoreItem } from "@/components/Core/forms/art-button-more/index.vue";

/** 默认外露操作数：超过则出现「更多」 */
export const DEFAULT_MAX_INLINE_TABLE_OPERATIONS = 3;

export interface TableOperationAction {
  key: string | number;
  label: string;
  artType: "add" | "edit" | "delete" | "view" | "more";
  icon?: string;
  /** 权限码，传给 ArtButtonMore 的 auth */
  perm?: string;
  disabled?: boolean;
  /** 图标颜色（外露按钮与「更多」内图标）；不传则按 artType 使用主题变量 */
  iconColor?: string;
  /** 「更多」里文字颜色；不传时对 key 为 delete 默认红色 */
  color?: string;
  run: () => void;
}

export interface RenderTableOperationCellOptions {
  maxInline?: number;
  /** 包裹容器 class */
  wrapperClass?: string;
  emptyText?: string;
}

/** 与 `ArtButtonTable` 各 type 默认图标一致，保证「更多」里每项都有图标 */
const ART_TYPE_DEFAULT_ICONS: Record<TableOperationAction["artType"], string> = {
  add: "ri:add-fill",
  edit: "ri:pencil-line",
  delete: "ri:delete-bin-5-line",
  view: "ri:eye-line",
  more: "ri:more-2-fill",
};

function iconForOperation(a: TableOperationAction): string {
  return a.icon ?? ART_TYPE_DEFAULT_ICONS[a.artType];
}

/** 与 Element Plus 语义色一致，便于各操作图标区分 */
const ART_TYPE_ICON_COLORS: Record<TableOperationAction["artType"], string> = {
  add: "var(--el-color-primary)",
  edit: "var(--el-color-success)",
  delete: "var(--el-color-danger)",
  view: "var(--el-color-info)",
  more: "var(--el-text-color-regular)",
};

function iconColorForOperation(a: TableOperationAction): string | undefined {
  if (a.iconColor != null) return a.iconColor;
  return ART_TYPE_ICON_COLORS[a.artType];
}

function defaultMoreItemColor(a: TableOperationAction): string | undefined {
  if (a.color != null) return a.color;
  return String(a.key) === "delete" ? "var(--el-color-danger)" : undefined;
}

export function renderTableOperationCell(
  actions: TableOperationAction[],
  options?: RenderTableOperationCellOptions
): VNode {
  const maxInline = options?.maxInline ?? DEFAULT_MAX_INLINE_TABLE_OPERATIONS;
  const wrapperClass =
    options?.wrapperClass ?? "inline-flex flex-wrap items-center justify-end gap-1";
  const emptyText = options?.emptyText ?? "—";

  if (actions.length === 0) {
    return h("span", { class: "text-g-400" }, emptyText);
  }

  const inline = actions.slice(0, maxInline);
  const overflow = actions.slice(maxInline);

  const inlineNodes = inline.map((a) =>
    h(ElTooltip, { content: a.label, placement: "top" }, () =>
      h(
        "span",
        {
          class: a.disabled ? "inline-flex opacity-40 pointer-events-none" : "inline-flex",
        },
        [
          h(ArtButtonTable, {
            type: a.artType,
            icon: iconForOperation(a),
            iconColor: iconColorForOperation(a),
            onClick: a.run,
          }),
        ]
      )
    )
  );

  if (overflow.length === 0) {
    return h("div", { class: wrapperClass }, inlineNodes);
  }

  const moreDropdown = h(ArtButtonMore, {
    list: overflow.map((a) => ({
      key: a.key,
      label: a.label,
      icon: iconForOperation(a),
      auth: a.perm,
      disabled: a.disabled,
      iconColor: iconColorForOperation(a),
      color: defaultMoreItemColor(a),
    })),
    onClick: (item: ButtonMoreItem) => {
      const act = overflow.find((x) => String(x.key) === String(item.key));
      act?.run();
    },
  });

  return h("div", { class: wrapperClass }, [...inlineNodes, moreDropdown]);
}
