<template>
  <ElDrawer
    v-model="visible"
    :size="size"
    :direction="direction"
    :show-close="false"
    :class="drawerClassMerged"
    destroy-on-close
    v-bind="drawerAttrs"
    @close="emit('close')"
    @opened="emit('opened')"
  >
    <template #header>
      <div class="core-overlay-drawer__header">
        <span class="core-overlay-drawer__title">{{ title }}</span>
        <div class="core-overlay-drawer__actions">
          <ElTooltip content="关闭" placement="top">
            <ElButton class="core-overlay-icon-btn" text @click="visible = false">
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
    <template v-else-if="formMode" #footer>
      <div class="fa-drawer-footer" :style="'padding-right: var(--el-drawer-padding-primary)'">
        <ElButton v-if="formMode !== 'detail'" @click="emit('cancel')">
          {{ cancelText }}
        </ElButton>
        <ElButton type="primary" :loading="confirmLoading" @click="emit('confirm')">
          {{ confirmText }}
        </ElButton>
      </div>
    </template>
  </ElDrawer>
</template>

<script setup lang="ts">
import { Close } from "@element-plus/icons-vue";
import type { DrawerProps } from "element-plus";
import { computed, useAttrs } from "vue";

defineOptions({ name: "FaDrawer", inheritAttrs: false });

const props = withDefaults(
  defineProps<{
    modelValue: boolean;
    title?: string;
    size?: string | number;
    direction?: "rtl" | "ltr" | "ttb" | "btt";
    /** 透传到 el-drawer 的 class */
    drawerClass?: string;
    /** 表单模式：detail 仅显示确定；create/update 显示取消+确定 */
    formMode?: "detail" | "create" | "update";
    /** 确定按钮 loading 状态 */
    confirmLoading?: boolean;
    /** 确定按钮文本 */
    confirmText?: string;
    /** 取消按钮文本 */
    cancelText?: string;
  }>(),
  {
    direction: "rtl",
    confirmText: "确定",
    cancelText: "取消",
  }
);

const emit = defineEmits<{
  "update:modelValue": [v: boolean];
  close: [];
  opened: [];
  /** 点击取消按钮 */
  cancel: [];
  /** 点击确定按钮 */
  confirm: [];
}>();

const attrs = useAttrs();

const visible = computed({
  get: () => props.modelValue,
  set: (v: boolean) => emit("update:modelValue", v),
});

const drawerClassMerged = computed(() => {
  const a = attrs.class;
  return [props.drawerClass, a].filter(Boolean);
});

const drawerAttrs = computed(() => {
  const a = { ...attrs } as Record<string, unknown>;
  delete a.class;
  return a as Partial<Omit<DrawerProps, "modelValue">>;
});
</script>

<style scoped lang="scss">
.core-overlay-drawer__header {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding-right: 4px;
}

.core-overlay-drawer__title {
  font-size: 16px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.fa-drawer-footer {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  padding-top: 4px;
}

.core-overlay-drawer__actions {
  display: inline-flex;
  flex-shrink: 0;
  gap: 4px;
  align-items: center;
  margin-left: auto;

  :deep(.core-overlay-icon-btn.el-button) {
    min-width: 32px;
    padding: 6px;
    border-radius: var(--el-border-radius-base);

    &.is-text:not(.is-disabled):hover {
      border-radius: var(--el-border-radius-base);
    }
  }
}
</style>
