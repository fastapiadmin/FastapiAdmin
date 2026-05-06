<template>
  <ElRow v-loading="previewLoading" element-loading-text="正在加载预览…">
    <ElCol v-if="!previewLoading && isTreeEmpty" :span="24">
      <ElEmpty>
        <template #description>
          <p class="mb-1 font-medium">暂无预览文件</p>
          <p class="gencode-preview-empty-tip">
            若刚保存过仍为空，可将「预览范围」改为「全部」；或返回上一步检查字段与主子表后重新进入。
          </p>
        </template>
      </ElEmpty>
    </ElCol>
    <template v-else>
      <ElCol :span="24" class="mb-2">
        <div class="flex items-center gap-3">
          <span class="text-sm text-[#909399]">预览范围</span>
          <ElRadioGroup v-model="previewScope" size="small">
            <ElRadioButton value="all">全部</ElRadioButton>
            <ElRadioButton value="frontend">前端</ElRadioButton>
            <ElRadioButton value="backend">后端</ElRadioButton>
          </ElRadioGroup>
          <span class="ml-3 text-sm text-[#909399]">类型</span>
          <ElCheckboxGroup v-model="previewTypes" size="small">
            <ElCheckboxButton v-for="t in previewTypeOptions" :key="t" :value="t">
              {{ t }}
            </ElCheckboxButton>
          </ElCheckboxGroup>
        </div>
      </ElCol>
      <ElCol :span="6">
        <ElScrollbar max-height="72vh">
          <ElTree
            :data="filteredTreeData"
            default-expand-all
            highlight-current
            @node-click="onTreeNodeClick"
          >
            <template #default="{ data }">
              <ArtSvgIcon
                :icon="resolveIconForArtSvgIcon(getFileTreeNodeIcon(data.label))"
                class="inline shrink-0 text-base"
              />
              <span class="ml-1" :title="data.full_path || data.label">
                {{ data.label }}
              </span>
            </template>
          </ElTree>
        </ElScrollbar>
      </ElCol>
      <ElCol :span="18">
        <ElScrollbar max-height="72vh">
          <div class="absolute z-36 right-5 top-2">
            <ElLink type="primary" @click="emit('copy-code')">
              <ElIcon>
                <CopyDocument />
              </ElIcon>
              复制代码
            </ElLink>
          </div>

          <Codemirror
            ref="cmRef"
            v-model:value="code"
            :options="cmOptions"
            border
            :readonly="true"
            height="100%"
            width="100%"
          />
        </ElScrollbar>
      </ElCol>
    </template>
  </ElRow>
</template>

<script setup lang="ts">
import "codemirror/mode/javascript/javascript.js";
import "codemirror/mode/python/python.js";
import "codemirror/mode/htmlmixed/htmlmixed.js";
import "codemirror/theme/dracula.css";
import { computed, inject, onUnmounted, ref, watch } from "vue";
import Codemirror from "codemirror-editor-vue3";
import type { EditorConfiguration } from "codemirror";
import type { CmComponentRef } from "codemirror-editor-vue3";
import ArtSvgIcon from "@/components/Core/base/art-svg-icon/index.vue";
import { resolveIconForArtSvgIcon } from "@/utils/menuIcon/remix";
import { CopyDocument } from "@element-plus/icons-vue";
import { GENCODE_CM_KEY } from "../gencodeInjectionKeys";
import type { TreeNode } from "../types";

defineOptions({ name: "GenPreviewStep" });

const previewScope = defineModel<"all" | "frontend" | "backend">("previewScope", {
  required: true,
});
const previewTypes = defineModel<string[]>("previewTypes", { required: true });

const props = defineProps<{
  previewLoading: boolean;
  previewTypeOptions: string[];
  filteredTreeData: TreeNode[];
  cmOptions: EditorConfiguration;
}>();

const isTreeEmpty = computed(() => !props.filteredTreeData || props.filteredTreeData.length === 0);

const code = defineModel<string>("code", { required: true });

const emit = defineEmits<{
  "file-click": [data: TreeNode];
  "copy-code": [];
}>();

const cmRef = ref<CmComponentRef>();
const injected = inject(GENCODE_CM_KEY, undefined);

watch(
  cmRef,
  (v) => {
    if (injected) injected.value = v;
  },
  { immediate: true }
);

onUnmounted(() => {
  if (injected) injected.value = undefined;
});

function onTreeNodeClick(data: TreeNode) {
  emit("file-click", data);
}

function getFileTreeNodeIcon(label: string): string {
  if (label.endsWith(".py")) return "python";
  if (label.endsWith(".vue")) return "vue";
  if (label.endsWith(".ts")) return "typescript";
  return "file";
}
</script>

<style scoped lang="scss">
.gencode-preview-meta-tip {
  margin: 0 0 8px;
  font-size: 12px;
  line-height: 1.5;
  color: var(--el-text-color-secondary);
}

.gencode-preview-empty-tip {
  max-width: 420px;
  margin: 0 auto;
  font-size: 13px;
  line-height: 1.5;
  color: var(--el-text-color-secondary);
}
</style>
