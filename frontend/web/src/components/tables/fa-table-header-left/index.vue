<!-- 列表页左侧工具栏：perm 预设「新增/导入/导出/批删/更多」，默认插槽可整块替换 -->
<template>
  <div class="data-table__toolbar--left inline-flex max-w-full flex-wrap items-center gap-2">
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
        >
          {{ $t("common.addNew") }}
        </ElButton>
        <ElButton
          v-if="permImport"
          v-hasPerm="permImport"
          v-ripple
          :loading="importLoading"
          :icon="Upload"
          @click="$emit('import')"
          plain
        >
          {{ $t("common.import") }}
        </ElButton>
        <ElButton
          v-if="permExport"
          v-hasPerm="permExport"
          v-ripple
          :loading="exportLoading"
          :icon="Download"
          @click="$emit('export')"
          plain
        >
          {{ $t("common.export") }}
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
          {{
            removeIds.length > 0
              ? `${$t("common.batchDelete")} (${removeIds.length})`
              : $t("common.batchDelete")
          }}
        </ElButton>
        <ElDropdown
          v-if="permPatch"
          v-hasPerm="permPatch"
          trigger="click"
          type="info"
          :disabled="removeIds.length === 0 || deleteLoading || moreLoading"
        >
          <ElButton :loading="moreLoading">
            {{ $t("common.more") }}
            <ElIcon class="el-icon--right">
              <ArrowDown />
            </ElIcon>
          </ElButton>
          <template #dropdown>
            <ElDropdownMenu>
              <ElDropdownItem
                v-for="action in resolvedMoreActions"
                :key="action.value"
                :icon="action.icon"
                @click="$emit('more', action.value)"
              >
                {{ action.label }}
              </ElDropdownItem>
            </ElDropdownMenu>
          </template>
        </ElDropdown>
      </ElSpace>
    </slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { ArrowDown, Delete, Download, Plus, Upload } from "@element-plus/icons-vue";

defineOptions({ name: "FaTableHeaderLeft" });

interface MoreAction {
  /** 下拉项文案（已翻译） */
  label: string;
  /** 回传给业务页的动作标识（沿用启用/停用语义，文案可自定义） */
  value: "enable" | "disable";
  /** Element Plus 图标名 */
  icon?: string;
}

interface Props {
  /** 自定义「更多」动作；不传时回退为批量启用/停用 */
  moreActions?: MoreAction[];
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

const props = withDefaults(defineProps<Props>(), {
  removeIds: () => [],
  deleteLoading: false,
  importLoading: false,
  exportLoading: false,
  createLoading: false,
  moreLoading: false,
  moreActions: undefined,
});

const { t } = useI18n();

const resolvedMoreActions = computed<MoreAction[]>(() => {
  if (props.moreActions?.length) return props.moreActions;
  return [
    { label: t("common.batchEnable"), value: "enable", icon: "Check" },
    { label: t("common.batchDisable"), value: "disable", icon: "CircleClose" },
  ];
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
