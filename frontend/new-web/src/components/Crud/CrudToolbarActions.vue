<!--
  Legacy（el-table）列表：渲染 defaultToolbar 配置的图标按钮（刷新、筛选、导入、导出等）。
  Art 栈请勿使用 — 右侧能力由 ArtTableHeader 提供；业务按钮写在 #toolbar。
-->
<template>
  <div class="crud-toolbar-actions flex flex-wrap items-center gap-2">
    <slot name="prepend" />
    <template v-for="(btn, index) in buttons" :key="index">
      <el-popover v-if="btn.name === 'filter'" placement="bottom" trigger="click">
        <template #reference>
          <el-button v-bind="toolbarBtnAttrs(btn.attrs)">
            <template v-if="toolbarIcon(btn.attrs)" #icon>
              <component :is="toolbarIcon(btn.attrs)" />
            </template>
            <span v-if="toolbarShowLabel(btn)">{{ btn.text }}</span>
          </el-button>
        </template>
        <el-scrollbar max-height="350px">
          <template v-for="c in cols" :key="c.prop">
            <el-checkbox v-if="c.prop" v-model="c.show" :label="c.label" />
          </template>
        </el-scrollbar>
      </el-popover>
      <el-tooltip v-else-if="toolbarUseTooltip(btn)" :content="tooltipContent(btn.name)!">
        <el-button
          v-hasPerm="btn.perm ?? '*:*:*'"
          v-bind="toolbarBtnAttrs(btn.attrs)"
          @click="onToolbar(btn.name)"
        >
          <template v-if="toolbarIcon(btn.attrs)" #icon>
            <component :is="toolbarIcon(btn.attrs)" />
          </template>
          <span v-if="toolbarShowLabel(btn)">{{ btn.text }}</span>
        </el-button>
      </el-tooltip>
      <el-button
        v-else
        v-hasPerm="btn.perm ?? '*:*:*'"
        v-bind="toolbarBtnAttrs(btn.attrs)"
        @click="onToolbar(btn.name)"
      >
        <template v-if="toolbarIcon(btn.attrs)" #icon>
          <component :is="toolbarIcon(btn.attrs)" />
        </template>
        <span v-if="toolbarShowLabel(btn)">{{ btn.text }}</span>
      </el-button>
    </template>
  </div>
</template>

<script setup lang="ts">
import type { ButtonProps } from "element-plus";
import type { CSSProperties, Component } from "vue";
import {
  Delete,
  Download,
  Edit,
  Operation,
  Plus,
  Refresh,
  Upload,
  View,
} from "@element-plus/icons-vue";

const ICON_MAP: Record<string, Component> = {
  plus: Plus,
  delete: Delete,
  upload: Upload,
  download: Download,
  refresh: Refresh,
  operation: Operation,
  edit: Edit,
  view: View,
};

/** 与 CrudContent `createToolbar` 产出的右侧按钮结构一致 */
export type CrudToolbarActionButton = {
  name: string;
  text?: string;
  attrs?: Partial<ButtonProps> & { style?: CSSProperties };
  perm?: string | string[] | null;
};

defineProps<{
  buttons: CrudToolbarActionButton[];
  cols: Array<{ prop?: string; label?: string; show?: boolean }>;
  onToolbar: (name: string) => void;
}>();

const TOOLTIPS: Record<string, string> = {
  import: "导入",
  export: "导出",
  filter: "筛选",
  refresh: "刷新",
};

function tooltipContent(name: string): string | undefined {
  return TOOLTIPS[name];
}

/** Element Plus `ButtonProps.circle` 类型较窄，显式按 boolean 判断标签与 tooltip */
function toolbarCircle(attrs?: CrudToolbarActionButton["attrs"]): boolean | undefined {
  return (attrs as { circle?: boolean } | undefined)?.circle;
}

function toolbarShowLabel(btn: CrudToolbarActionButton): boolean {
  return Boolean(btn.text && toolbarCircle(btn.attrs) === false);
}

function toolbarUseTooltip(btn: CrudToolbarActionButton): boolean {
  const tip = tooltipContent(btn.name);
  return Boolean(tip && toolbarCircle(btn.attrs) !== false);
}

function toolbarBtnAttrs(attrs?: Partial<ButtonProps> & { style?: CSSProperties }) {
  if (!attrs) return {};
  const rest = { ...attrs } as Record<string, unknown>;
  delete rest.icon;
  return rest as Partial<ButtonProps> & { style?: CSSProperties };
}

function toolbarIcon(attrs?: Partial<ButtonProps>): Component | null {
  const raw = attrs?.icon;
  if (typeof raw !== "string") return null;
  return ICON_MAP[raw] ?? null;
}
</script>
