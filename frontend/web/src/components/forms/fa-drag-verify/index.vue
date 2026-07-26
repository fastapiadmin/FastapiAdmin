<!-- 拖拽验证组件 -->
<template>
  <div
    ref="dragVerify"
    class="drag_verify"
    :style="dragVerifyStyle"
    @mousemove="dragMoving"
    @mouseup="dragFinish"
    @mouseleave="dragFinish"
    @touchmove="dragMoving"
    @touchend="dragFinish"
  >
    <!-- 进度条 -->
    <div class="dv_progress_bar" ref="progressBar" :style="progressBarStyle"></div>

    <!-- 提示文本 -->
    <div class="dv_text" :style="textStyle" ref="messageRef">
      <slot name="textBefore" v-if="$slots.textBefore"></slot>
      {{ message }}
      <slot name="textAfter" v-if="$slots.textAfter"></slot>
    </div>

    <!-- 滑块处理器 -->
    <div
      class="dv_handler dv_handler_bg"
      @mousedown="dragStart"
      @touchstart="dragStart"
      ref="handler"
      :style="handlerStyle"
    >
      <FaSvgIcon :icon="modelValue ? successIcon : handlerIcon" class="text-g-600"></FaSvgIcon>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useWindowSize } from "@vueuse/core";

defineOptions({ name: "FaDragVerify" });

// 事件定义
const emit = defineEmits(["handlerMove", "passCallback"]);

// 组件属性接口定义
interface Props {
  /** 组件宽度 */
  width?: number | string;
  /** 组件高度 */
  height?: number;
  /** 默认提示文本 */
  text?: string;
  /** 成功提示文本 */
  successText?: string;
  /** 背景色 */
  background?: string;
  /** 进度条背景色 */
  progressBarBg?: string;
  /** 完成状态背景色 */
  completedBg?: string;
  /** 是否圆角 */
  circle?: boolean;
  /** 圆角大小 */
  radius?: string;
  /** 滑块图标 */
  handlerIcon?: string;
  /** 成功图标 */
  successIcon?: string;
  /** 滑块背景色 */
  handlerBg?: string;
  /** 文本大小 */
  textSize?: string;
  /** 文本颜色 */
  textColor?: string;
}

// 属性默认值设置
const props = withDefaults(defineProps<Props>(), {
  width: "100%",
  height: 40,
  text: "按住滑块拖动",
  successText: "success",
  background: "#eee",
  progressBarBg: "#1385FF",
  completedBg: "#57D187",
  circle: false,
  radius: "calc(var(--custom-radius) / 3 + 2px)",
  handlerIcon: "solar:double-alt-arrow-right-linear",
  successIcon: "ri:check-fill",
  handlerBg: "#fff",
  textSize: "13px",
  textColor: "#333",
});

const { width: winWidth } = useWindowSize();
const effectiveHeight = computed(() =>
  props.height === 40 && winWidth.value < 768 ? 24 : props.height
);

// ----- 响应式状态（替换原来的 state 对象） -----
const modelValue = defineModel<boolean>("value", { default: false });
const sliderPosition = ref(0);
const isDragging = ref(false);
const startX = ref(0);
const currentX = ref(0);

// DOM 元素引用
const dragVerify = ref<HTMLElement>();
const messageRef = ref<HTMLElement>();
const handler = ref<HTMLElement>();
const progressBar = ref<HTMLElement>();

// 触摸事件变量 - 用于禁止页面滑动
let touchStartX = 0;
let touchStartY = 0;

/**
 * 触摸开始事件处理
 */
const onTouchStart = (e: TouchEvent) => {
  const touch = e.targetTouches[0];
  if (!touch) return;
  touchStartX = touch.pageX;
  touchStartY = touch.pageY;
};

/**
 * 触摸移动事件处理 - 判断是否为横向滑动，如果是则阻止默认行为
 */
const onTouchMove = (e: TouchEvent) => {
  const touch = e.targetTouches[0];
  if (!touch) return;
  const moveX = touch.pageX;
  const moveY = touch.pageY;
  if (Math.abs(moveX - touchStartX) > Math.abs(moveY - touchStartY)) {
    e.preventDefault();
  }
};

// 获取数值形式的宽度
const getNumericWidth = (): number => {
  if (typeof props.width === "string") {
    return dragVerify.value?.offsetWidth || 260;
  }
  return props.width;
};

// 获取样式字符串形式的宽度
const getStyleWidth = (): string => {
  if (typeof props.width === "string") {
    return props.width;
  }
  return props.width + "px";
};

// 组件挂载后的初始化
onMounted(() => {
  dragVerify.value?.style.setProperty("--textColor", props.textColor);
  nextTick(() => {
    const numericWidth = getNumericWidth();
    dragVerify.value?.style.setProperty("--width", Math.floor(numericWidth / 2) + "px");
    dragVerify.value?.style.setProperty("--pwidth", -Math.floor(numericWidth / 2) + "px");
  });
  document.addEventListener("touchstart", onTouchStart);
  document.addEventListener("touchmove", onTouchMove, { passive: false });
});

// 组件卸载前清理事件监听器
onBeforeUnmount(() => {
  document.removeEventListener("touchstart", onTouchStart);
  document.removeEventListener("touchmove", onTouchMove);
});

// ----- 样式计算 -----
const handlerStyle = computed(() => ({
  left: sliderPosition.value + "px",
  width: effectiveHeight.value + "px",
  height: effectiveHeight.value + "px",
  background: props.handlerBg,
  transition: isDragging.value ? "none" : "left 0.3s",
}));

const dragVerifyStyle = computed(() => ({
  width: getStyleWidth(),
  height: effectiveHeight.value + "px",
  lineHeight: effectiveHeight.value + "px",
  background: props.background,
  borderRadius: props.circle ? effectiveHeight.value / 2 + "px" : props.radius,
}));

const progressBarStyle = computed(() => ({
  width: sliderPosition.value + effectiveHeight.value / 2 + "px",
  background: modelValue.value ? props.completedBg : props.progressBarBg,
  height: effectiveHeight.value + "px",
  borderRadius: props.circle
    ? effectiveHeight.value / 2 + "px 0 0 " + effectiveHeight.value / 2 + "px"
    : props.radius,
  transition: isDragging.value ? "none" : "width 0.3s",
}));

// 文本样式计算
const textStyle = computed(() => ({
  fontSize: props.textSize,
}));

// 显示消息计算属性
const message = computed(() => {
  return modelValue.value ? props.successText : props.text;
});

// ----- 拖拽逻辑 -----
const dragStart = (e: MouseEvent | TouchEvent) => {
  if (modelValue.value) return;
  isDragging.value = true;

  const pageX = "touches" in e ? (e.touches[0]?.pageX ?? 0) : (e as MouseEvent).pageX;
  if (typeof pageX !== "number") return;
  startX.value = pageX;
  currentX.value = sliderPosition.value;

  emit("handlerMove");
};

const dragMoving = (e: MouseEvent | TouchEvent) => {
  if (!isDragging.value || modelValue.value) return;

  const pageX = "touches" in e ? (e.touches[0]?.pageX ?? 0) : (e as MouseEvent).pageX;
  const numericWidth = getNumericWidth();
  const maxPosition = numericWidth - effectiveHeight.value;

  const newPosition = Math.max(0, Math.min(maxPosition, currentX.value + (pageX - startX.value)));

  if (newPosition >= maxPosition) {
    // 拖拽到末端，验证成功
    sliderPosition.value = maxPosition;
    modelValue.value = true;
    isDragging.value = false;
    emit("passCallback");
  } else {
    sliderPosition.value = newPosition;
  }
};

const dragFinish = () => {
  if (!isDragging.value) return;
  isDragging.value = false;

  const numericWidth = getNumericWidth();
  const maxPosition = numericWidth - effectiveHeight.value;

  if (sliderPosition.value < maxPosition) {
    // 未到末端，复位
    sliderPosition.value = 0;
  } else {
    // 到末端，验证成功
    sliderPosition.value = maxPosition;
    modelValue.value = true;
    emit("passCallback");
  }
};

/**
 * 重置验证状态
 */
const reset = () => {
  sliderPosition.value = 0;
  modelValue.value = false;
};

// 当外部将 modelValue 设为 false 时（如 getCaptcha 重置），同步复位滑块位置
watch(modelValue, (val) => {
  if (!val && sliderPosition.value > 0) {
    sliderPosition.value = 0;
  }
});

// 暴露重置方法给父组件
defineExpose({
  reset,
});
</script>

<style lang="scss" scoped>
.drag_verify {
  position: relative;
  box-sizing: border-box;
  overflow: hidden;
  text-align: center;
  border: 1px solid var(--default-border-dashed);

  .dv_handler {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 9;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: move;

    i {
      padding-left: 0;
      font-size: 14px;
      color: #999;
    }

    .el-icon-circle-check {
      margin-top: 9px;
      color: #6c6;
    }
  }

  .dv_progress_bar {
    position: absolute;
    height: 34px;
  }

  .dv_text {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: transparent;
    user-select: none;
    background: linear-gradient(
      to right,
      var(--textColor) 0%,
      var(--textColor) 40%,
      #fff 50%,
      var(--textColor) 60%,
      var(--textColor) 100%
    );
    -webkit-background-clip: text;
    background-clip: text;
    animation: slidetounlock 2s cubic-bezier(0, 0.2, 1, 1) infinite;
    -webkit-text-fill-color: transparent;
    text-size-adjust: none;

    * {
      -webkit-text-fill-color: var(--textColor);
    }
  }
}
</style>

<style lang="scss">
@keyframes slidetounlock {
  0% {
    background-position: var(--pwidth) 0;
  }

  100% {
    background-position: var(--width) 0;
  }
}

@keyframes slidetounlock2 {
  0% {
    background-position: var(--pwidth) 0;
  }

  100% {
    background-position: var(--pwidth) 0;
  }
}
</style>
