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
  </ElDrawer>
</template>

<script setup lang="ts">
import { Close } from "@element-plus/icons-vue";
import type { DrawerProps } from "element-plus";
import { computed, useAttrs } from "vue";

defineOptions({ name: "ArtDrawer", inheritAttrs: false });

const props = withDefaults(
  defineProps<{
    modelValue: boolean;
    title?: string;
    size?: string | number;
    direction?: "rtl" | "ltr" | "ttb" | "btt";
    /** 透传到 el-drawer 的 class */
    drawerClass?: string;
  }>(),
  {
    direction: "rtl",
  }
);

const emit = defineEmits<{
  "update:modelValue": [v: boolean];
  close: [];
  opened: [];
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
