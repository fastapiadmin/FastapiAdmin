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
            <FaIconButton
              class="core-overlay-icon-btn"
              icon="ri:close-line"
              @click="visible = false"
            />
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
        <!-- detail 模式仅显示关闭按钮 -->
        <ElButton v-if="formMode === 'detail'" type="primary" @click="emit('confirm')">
          {{ confirmText || "关闭" }}
        </ElButton>
        <template v-else>
          <ElButton @click="emit('cancel')">
            {{ cancelText }}
          </ElButton>
          <!-- 创建模式支持"提交并继续添加" -->
          <ElButton
            v-if="showSubmitAndContinue && formMode === 'create'"
            type="primary"
            :loading="confirmLoading"
            @click="emit('submitAndContinue')"
          >
            提交并继续添加
          </ElButton>
          <ElButton type="primary" :loading="confirmLoading" @click="emit('confirm')">
            {{ confirmText }}
          </ElButton>
        </template>
      </div>
    </template>
  </ElDrawer>
</template>

<script setup lang="ts">
import type { DrawerProps } from "element-plus";
import { computed, useAttrs, onMounted, onUnmounted } from "vue";
import FaIconButton from "@/components/others/fa-icon-button/index.vue";

defineOptions({ name: "FaDrawer", inheritAttrs: false });

interface Props {
  modelValue: boolean;
  title?: string;
  size?: string | number;
  direction?: "rtl" | "ltr" | "ttb" | "btt";
  /** 透传到 el-drawer 的 class */
  drawerClass?: string;
  /** 表单模式：detail 仅显示关闭；create/update 显示取消+确定 */
  formMode?: "detail" | "create" | "update";
  /** 确定按钮 loading 状态 */
  confirmLoading?: boolean;
  /** 确定按钮文本 */
  confirmText?: string;
  /** 取消按钮文本 */
  cancelText?: string;
  /** 是否显示"提交并继续添加"按钮（仅 create 模式有效） */
  showSubmitAndContinue?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  direction: "rtl",
  confirmText: "确定",
  cancelText: "取消",
  showSubmitAndContinue: false,
});

interface Emits {
  "update:modelValue": [v: boolean];
  close: [];
  opened: [];
  /** 点击取消按钮 */
  cancel: [];
  /** 点击确定按钮 */
  confirm: [];
  /** 点击提交并继续添加按钮 */
  submitAndContinue: [];
}

const emit = defineEmits<Emits>();

const attrs = useAttrs();

const visible = computed({
  get: () => props.modelValue,
  set: (v: boolean) => emit("update:modelValue", v),
});

// Ctrl+Enter / Cmd+Enter 快捷键触发确认提交（非 detail 模式）
function onKeydown(e: KeyboardEvent) {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    if (props.modelValue && props.formMode && props.formMode !== "detail") {
      e.preventDefault();
      emit("confirm");
    }
  }
}

onMounted(() => window.addEventListener("keydown", onKeydown));
onUnmounted(() => window.removeEventListener("keydown", onKeydown));

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
