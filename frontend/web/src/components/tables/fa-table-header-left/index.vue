<!-- 列表页左侧工具栏：perm 预设「新增/导入/导出/批删/更多」，默认插槽可整块替换 -->
<template>
  <div class="data-table__toolbar--left inline-flex flex-wrap items-center gap-2">
    <slot>
      <!-- 默认插槽回退内容：预设按钮 -->
      <ElSpace>
        <ElButton
          v-if="permCreate"
          v-hasPerm="permCreate"
          type="primary"
          :icon="Plus"
          :loading="createLoading"
          @click="$emit('add')"
          plain
        >
          新增
        </ElButton>
        <ElButton
          v-if="permImport"
          v-hasPerm="permImport"
          v-ripple
          type="success"
          :loading="importLoading"
          :icon="Upload"
          @click="$emit('import')"
          plain
        >
          导入
        </ElButton>
        <ElButton
          v-if="permExport"
          v-hasPerm="permExport"
          v-ripple
          type="warning"
          :loading="exportLoading"
          :icon="Download"
          @click="$emit('export')"
          plain
        >
          导出
        </ElButton>
        <ElButton
          v-if="permDelete"
          v-hasPerm="permDelete"
          type="danger"
          :loading="deleteLoading"
          :disabled="removeIds.length === 0"
          :icon="Delete"
          @click="$emit('delete')"
          plain
        >
          {{ removeIds.length > 0 ? `批量删除 (${removeIds.length})` : "批量删除" }}
        </ElButton>
        <ElDropdown
          v-if="permPatch"
          v-hasPerm="permPatch"
          trigger="click"
          type="info"
          :disabled="removeIds.length === 0 || deleteLoading || moreLoading"
        >
          <ElButton type="info" plain :loading="moreLoading">
            更多
            <ElIcon class="el-icon--right">
              <ArrowDown />
            </ElIcon>
          </ElButton>
          <template #dropdown>
            <ElDropdownMenu>
              <ElDropdownItem icon="Check" @click="$emit('more', 'enable')"
                >批量启用</ElDropdownItem
              >
              <ElDropdownItem icon="CircleClose" @click="$emit('more', 'disable')">
                批量停用
              </ElDropdownItem>
            </ElDropdownMenu>
          </template>
        </ElDropdown>
      </ElSpace>
    </slot>
  </div>
</template>

<script setup lang="ts">
import { ArrowDown, Delete, Download, Plus, Upload } from "@element-plus/icons-vue";

defineOptions({ name: "FaTableHeaderLeft" });

interface Props {
  /** 勾选行主键，用于禁用批删 / 更多（插槽完全自定义时可不传） */
  removeIds?: Array<string | number>;
  /** 新增按钮权限，不传则不显示 */
  permCreate?: string | string[];
  /** 导入按钮权限，不传则不显示；顺序在新增之后、批量删除之前 */
  permImport?: string | string[];
  /** 导出按钮权限，不传则不显示 */
  permExport?: string | string[];
  /** 导入按钮 loading */
  importLoading?: boolean;
  /** 导出按钮 loading */
  exportLoading?: boolean;
  /** 批量删除权限，不传则不显示 */
  permDelete?: string | string[];
  /** 「更多」下拉权限，不传则不显示 */
  permPatch?: string | string[];
  /** 批量删除中（按钮 loading，并禁用「更多」） */
  deleteLoading?: boolean;
  /** 新增按钮 loading（防止重复点击触发多次创建） */
  createLoading?: boolean;
  /** 「更多」下拉项（启用/停用）loading */
  moreLoading?: boolean;
}

withDefaults(defineProps<Props>(), {
  removeIds: () => [],
  deleteLoading: false,
  importLoading: false,
  exportLoading: false,
  createLoading: false,
  moreLoading: false,
});

interface Emits {
  add: [];
  import: [];
  export: [];
  delete: [];
  more: [value: "enable" | "disable"];
}

defineEmits<Emits>();
</script>
