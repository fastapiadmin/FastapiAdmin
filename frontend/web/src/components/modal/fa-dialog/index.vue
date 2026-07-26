<template>
  <ElDialog
    ref="elDialogRef"
    v-model="visible"
    :width="width"
    :draggable="draggable"
    :fullscreen="fullscreen"
    :show-close="false"
    :class="dialogClass"
    :modal-class="modalClass"
    :align-center="alignCenter"
    destroy-on-close
    v-bind="dialogAttrs"
    @close="emit('close')"
    @closed="emit('closed')"
    @opened="emit('opened')"
  >
    <template #header="{ titleId, titleClass, close }">
      <div class="core-overlay-dialog__header">
        <span :id="titleId" :class="titleClass">{{ title }}</span>
        <div class="core-overlay-dialog__actions">
          <ElTooltip :content="fullscreen ? '还原' : '全屏'" placement="top">
            <FaIconButton
              class="core-overlay-icon-btn"
              :icon="fullscreen ? 'ri:fullscreen-exit-line' : 'ri:fullscreen-fill'"
              @click="fullscreen = !fullscreen"
            />
          </ElTooltip>
          <ElTooltip content="关闭" placement="top">
            <FaIconButton class="core-overlay-icon-btn" icon="ri:close-line" @click="close" />
          </ElTooltip>
        </div>
      </div>
    </template>
    <slot />
    <template v-if="$slots.footer" #footer>
      <slot name="footer" />
    </template>
    <template v-else-if="formMode" #footer>
      <div class="fa-dialog-footer" :style="'padding-right: var(--el-dialog-padding-primary)'">
        <!-- detail 模式仅显示关闭按钮，emit close 以区分语义 -->
        <ElButton v-if="formMode === 'detail'" type="primary" @click="emit('close')">
          {{ confirmText || "关闭" }}
        </ElButton>
        <template v-else>
          <ElButton type="primary" plain @click="emit('cancel')">
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
  </ElDialog>
</template>

<script setup lang="ts">
import type { DialogProps } from "element-plus";
import { ElDialog } from "element-plus";
import { computed, ref, useAttrs, watch, onMounted, onUnmounted } from "vue";
import FaIconButton from "@/components/others/fa-icon-button/index.vue";

defineOptions({ name: "FaDialog", inheritAttrs: false });

interface Props {
  modelValue: boolean;
  title?: string;
  width?: string | number;
  /** 默认可拖拽；全屏时 Element Plus 会限制拖拽 */
  draggable?: boolean;
  /** 透传到 el-dialog 的 class */
  dialogClass?: string;
  /** 遮罩层自定义 class */
  modalClass?: string;
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
  /** 点击遮罩层是否关闭弹窗 */
  closeOnClickModal?: boolean;
  /** 按 Escape 键是否关闭弹窗 */
  closeOnPressEscape?: boolean;
  /** 是否居中显示弹窗 */
  alignCenter?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  draggable: true,
  confirmText: "确定",
  cancelText: "取消",
  showSubmitAndContinue: false,
  closeOnClickModal: true,
  closeOnPressEscape: true,
  alignCenter: true,
});

interface Emits {
  "update:modelValue": [v: boolean];
  close: [];
  closed: [];
  opened: [];
  "fullscreen-change": [isFullscreen: boolean];
  /** 点击取消按钮 */
  cancel: [];
  /** 点击确定按钮 */
  confirm: [];
  /** 点击提交并继续添加按钮 */
  submitAndContinue: [];
}

const emit = defineEmits<Emits>();

const attrs = useAttrs();
const fullscreen = ref(false);

watch(fullscreen, (newVal) => {
  emit("fullscreen-change", newVal);
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
  // 已通过 Props 显式声明的属性，避免与 v-bind 冲突
  delete a.alignCenter;
  delete a["align-center"];
  delete a.closeOnClickModal;
  delete a["close-on-click-modal"];
  delete a.closeOnPressEscape;
  delete a["close-on-press-escape"];
  return a as Partial<Omit<DialogProps, "modelValue" | "alignCenter">>;
});

/** ElDialog 实例引用，调用方可通过 ref 访问其方法（如 open、close 等） */
const elDialogRef = ref<InstanceType<typeof ElDialog>>();

defineExpose({
  elDialogRef,
});
</script>
