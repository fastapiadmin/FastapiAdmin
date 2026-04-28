<template>
  <el-drawer
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
      <div class="curd-drawer-header">
        <span class="curd-drawer-header__title">{{ title }}</span>
        <div class="curd-drawer-header__actions">
          <el-tooltip content="关闭" placement="top">
            <el-button text circle @click="visible = false">
              <el-icon><Close /></el-icon>
            </el-button>
          </el-tooltip>
        </div>
      </div>
    </template>
    <slot />
    <template v-if="$slots.footer" #footer>
      <slot name="footer" />
    </template>
  </el-drawer>
</template>

<script setup lang="ts">
  import { Close } from '@element-plus/icons-vue';
  import type { DrawerProps } from 'element-plus';
  import { computed, useAttrs } from 'vue';

  defineOptions({ inheritAttrs: false });

  const props = withDefaults(
    defineProps<{
      modelValue: boolean;
      title?: string;
      size?: string | number;
      direction?: 'rtl' | 'ltr' | 'ttb' | 'btt';
      /** 透传到 el-drawer 的 class */
      drawerClass?: string;
    }>(),
    {
      direction: 'rtl',
    }
  );

  const emit = defineEmits<{
    'update:modelValue': [v: boolean];
    close: [];
    opened: [];
  }>();

  const attrs = useAttrs();

  const visible = computed({
    get: () => props.modelValue,
    set: (v: boolean) => emit('update:modelValue', v),
  });

  const drawerClassMerged = computed(() => {
    const a = attrs.class;
    return [props.drawerClass, a].filter(Boolean);
  });

  const drawerAttrs = computed(() => {
    const a = { ...attrs } as Record<string, unknown>;
    delete a.class;
    return a as Partial<Omit<DrawerProps, 'modelValue'>>;
  });
</script>

<style scoped lang="scss">
  .curd-drawer-header {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding-right: 4px;
  }

  .curd-drawer-header__title {
    font-size: 16px;
    font-weight: 500;
    color: var(--el-text-color-primary);
  }

  .curd-drawer-header__actions {
    display: inline-flex;
    flex-shrink: 0;
    gap: 2px;
    align-items: center;
    margin-left: auto;
  }
</style>
