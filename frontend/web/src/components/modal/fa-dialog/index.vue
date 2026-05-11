<template>
  <ElDialog
    v-model="visible"
    :width="width"
    :draggable="draggable"
    :fullscreen="fullscreen"
    :show-close="false"
    :class="dialogClass"
    :modal-class="modalClass"
    align-center
    destroy-on-close
    v-bind="dialogAttrs"
    @close="emit('close')"
    @opened="emit('opened')"
  >
    <template #header="{ titleId, titleClass, close }">
      <div class="core-overlay-dialog__header">
        <span :id="titleId" :class="titleClass">{{ title }}</span>
        <div class="core-overlay-dialog__actions">
          <ElTooltip :content="fullscreen ? '还原' : '全屏'" placement="top">
            <ElButton
              class="core-overlay-icon-btn"
              text
              type="primary"
              @click="fullscreen = !fullscreen"
            >
              <ElIcon>
                <Fold v-if="fullscreen" />
                <FullScreen v-else />
              </ElIcon>
            </ElButton>
          </ElTooltip>
          <ElTooltip content="关闭" placement="top">
            <ElButton class="core-overlay-icon-btn" text @click="close">
              <ElIcon><Close /></ElIcon>
            </ElButton>
          </ElTooltip>
        </div>
      </div>
    </template>
    <slot />
    <template v-if="$slots.footer" #footer>
      <slot name="footer" />
    </template>
  </ElDialog>
</template>

<script setup lang="ts">
import { Close, Fold, FullScreen } from "@element-plus/icons-vue";
import type { DialogProps } from "element-plus";
import { computed, ref, useAttrs, watch } from "vue";

defineOptions({ name: "FaDialog", inheritAttrs: false });

const props = withDefaults(
  defineProps<{
    modelValue: boolean;
    title?: string;
    width?: string | number;
    /** 默认可拖拽；全屏时 Element Plus 会限制拖拽 */
    draggable?: boolean;
    /** 透传到 el-dialog 的 class */
    dialogClass?: string;
    /** 遮罩层自定义 class */
    modalClass?: string;
  }>(),
  {
    draggable: true,
  }
);

const emit = defineEmits<{
  "update:modelValue": [v: boolean];
  close: [];
  opened: [];
  "fullscreen-change": [isFullscreen: boolean];
}>();

const attrs = useAttrs();
const fullscreen = ref(false);

watch(fullscreen, (newVal) => {
  emit("fullscreen-change", newVal);
});

const dialogClass = computed(() => {
  const a = attrs.class;
  return [props.dialogClass, a].filter(Boolean);
});

const visible = computed({
  get: () => props.modelValue,
  set: (v: boolean) => emit("update:modelValue", v),
});

/** 透传除 modelValue 外的 el-dialog 属性（如 top、modal-class、append-to-body 等） */
const dialogAttrs = computed(() => {
  const a = { ...attrs } as Record<string, unknown>;
  delete a.class;
  return a as Partial<Omit<DialogProps, "modelValue">>;
});
</script>

<style scoped lang="scss">
.core-overlay-dialog__header {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding-right: 4px;
}

.core-overlay-dialog__actions {
  display: inline-flex;
  flex-shrink: 0;
  gap: 4px;
  align-items: center;
  margin-left: auto;

  ::deep(.core-overlay-icon-btn.el-button) {
    min-width: 32px;
    padding: 6px;
    border-radius: var(--el-border-radius-base);

    &.is-text:not(.is-disabled):hover {
      border-radius: var(--el-border-radius-base);
    }
  }
}
</style>
