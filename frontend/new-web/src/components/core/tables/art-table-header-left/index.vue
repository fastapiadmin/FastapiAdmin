<!-- 列表页左侧工具栏：1) configButtons 与 CrudContent 配置驱动一致 2) perm 预设「新增/导入/导出/批删/更多」 3) 默认插槽可整块替换 -->
<template>
  <div class="data-table__toolbar--left inline-flex flex-wrap items-center gap-2">
    <template v-if="configButtons && configButtons.length">
      <template v-for="(btn, index) in configButtons" :key="index">
        <ElButton
          v-hasPerm="btn.perm ?? '*:*:*'"
          v-bind="btn.attrs"
          :disabled="btn.name === 'delete' && removeIds.length === 0"
          @click="$emit('toolbar', btn.name)"
        >
          {{ btn.text }}
        </ElButton>
      </template>
    </template>
    <slot v-else>
      <slot>
        <ElSpace>
          <ElButton
            v-if="permCreate"
            v-hasPerm="permCreate"
            type="success"
            :icon="Plus"
            @click="$emit('add')"
            plain
          >
            新增
          </ElButton>
          <ElButton
            v-if="permImport"
            v-hasPerm="permImport"
            v-ripple
            type="warning"
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
            type="primary"
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
            批量删除
          </ElButton>
          <ElDropdown v-if="permPatch" v-hasPerm="permPatch" trigger="click">
            <ElButton type="default" :disabled="removeIds.length === 0 || moreDisabled">
              <template #icon>
                <ArrowDown />
              </template>
              更多
            </ElButton>
            <template #dropdown>
              <ElDropdownMenu>
                <ElDropdownItem icon="Check" @click="$emit('more', '0')">批量启用</ElDropdownItem>
                <ElDropdownItem icon="CircleClose" @click="$emit('more', '1')">
                  批量停用
                </ElDropdownItem>
              </ElDropdownMenu>
            </template>
          </ElDropdown>
        </ElSpace>
      </slot>
    </slot>
  </div>
</template>

<script setup lang="ts">
import { ArrowDown, Delete, Download, Plus, Upload } from "@element-plus/icons-vue";
import { computed } from "vue";
import type { ArtTableHeaderLeftConfigButton } from "@/components/Core/modal/types";

const props = withDefaults(
  defineProps<{
    /** 与 CrudContent `toolbarLeftBtn` 一致时走配置驱动（与 handleToolbar 对齐） */
    configButtons?: ArtTableHeaderLeftConfigButton[];
    /** 勾选行主键，用于禁用批删 / 更多（插槽完全自定义时可不传） */
    removeIds?: Array<string | number>;
    /** 新增按钮权限，不传则不显示（configButtons 未传时） */
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
  }>(),
  {
    removeIds: () => [],
    deleteLoading: false,
    importLoading: false,
    exportLoading: false,
  }
);

defineEmits<{
  /** 配置模式：与 CrudContent handleToolbar 一致 */
  toolbar: [name: string];
  add: [];
  import: [];
  export: [];
  delete: [];
  more: [value: string];
}>();

const moreDisabled = computed(() => props.removeIds.length === 0 || props.deleteLoading);
</script>
