<!--
  图片裁剪组件 - 基于 vue-img-cutter 封装
  官方文档: https://gitee.com/GLUESTICK/vue-img-cutter

  封装策略：
  - 所有 ImgCutter 原生 prop 以对应名称透传（驼峰→短横线映射由 Vue 自动处理）
  - 包装层额外提供 title/showPreview/previewTitle/downloadable 等增强功能
  - 仅将 ImgCutter 原生 prop 通过 v-bind 传递，避免污染
-->
<template>
  <div class="cutter-container">
    <div class="cutter-component">
      <div v-if="title" class="title">{{ title }}</div>
      <ImgCutter
        ref="imgCutterModal"
        v-bind="imgCutterProps"
        @cut-down="onCutDown"
        @on-print-img="onPrintImg"
        @on-choose-img="onChooseImg"
        @on-clear-all="onClearAll"
        @on-image-load-complete="onImageLoadComplete"
        @on-image-load-error="onImageLoadError"
        @error="onError"
      >
        <template #choose>
          <ElButton type="primary" plain v-ripple>选择图片</ElButton>
        </template>
        <template #cancel>
          <ElButton type="danger" plain v-ripple>清除</ElButton>
        </template>
        <template #confirm>
          <div ref="confirmElRef" />
        </template>
      </ImgCutter>
    </div>

    <div v-if="showPreview" class="preview-container">
      <div v-if="previewTitle" class="title">{{ previewTitle }}</div>
      <div
        class="preview-box"
        :style="{
          width: `${cutWidth}px`,
          height: `${cutHeight}px`,
        }"
      >
        <img v-if="temImgPath" class="preview-img" :src="temImgPath" alt="预览图" />
      </div>
      <div class="preview-actions">
        <ElButton
          v-if="downloadable"
          class="download-btn"
          :disabled="!temImgPath"
          v-ripple
          @click="handleDownload"
        >
          下载图片
        </ElButton>
        <ElButton type="primary" :disabled="!temImgPath" v-ripple @click="triggerCrop">
          确定
        </ElButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import ImgCutter from "vue-img-cutter";
import "vue-img-cutter/vue-img-cutter.css";

defineOptions({ name: "FaCutterImg" });

/* ============================================================
 * Props
 * ============================================================ */

interface FaCutterImgProps {
  // ── 包装层增强 ──
  /** 裁剪区域标题 */
  title?: string;
  /** 是否显示预览区域 */
  showPreview?: boolean;
  /** 预览区域标题 */
  previewTitle?: string;
  /** 是否显示下载按钮 */
  downloadable?: boolean;
  /** 远程图片地址（支持 v-model） */
  imgUrl?: string;

  // ── ImgCutter 原生 prop ──
  isModal?: boolean;
  showChooseBtn?: boolean;
  lockScroll?: boolean;
  modalTitle?: string;
  boxWidth?: number;
  boxHeight?: number;
  cutWidth?: number;
  cutHeight?: number;
  tool?: boolean;
  toolBgc?: string;
  sizeChange?: boolean;
  moveAble?: boolean;
  imgMove?: boolean;
  originalGraph?: boolean;
  crossOrigin?: boolean;
  crossOriginHeader?: string;
  rate?: string;
  /** @deprecated 使用 watermarkText 代替 */
  WatermarkText?: string;
  /** 水印文字 */
  watermarkText?: string;
  /** 水印字体 (如 '12px Sans-serif') */
  watermarkTextFont?: string;
  /** 水印颜色 */
  watermarkTextColor?: string;
  /** 水印水平位置 (0-1) */
  watermarkTextX?: number;
  /** 水印垂直位置 (0-1) */
  watermarkTextY?: number;
  smallToUpload?: boolean;
  saveCutPosition?: boolean;
  scaleAble?: boolean;
  toolBoxOverflow?: boolean;
  index?: unknown;
  previewMode?: boolean;
  fileType?: "png" | "jpeg" | "webp";
  quality?: number;
  accept?: string;
  afterChooseImg?: () => Promise<boolean>;
}

const props = withDefaults(defineProps<FaCutterImgProps>(), {
  // ── 包装层 ──
  title: "",
  showPreview: true,
  previewTitle: "",
  downloadable: true,

  // ── ImgCutter 默认值（对齐官方） ──
  isModal: false,
  showChooseBtn: true,
  lockScroll: true,
  modalTitle: "图片裁剪",
  boxWidth: 800,
  boxHeight: 400,
  cutWidth: 200,
  cutHeight: 200,
  tool: true,
  toolBgc: "#fff",
  sizeChange: true,
  moveAble: true,
  imgMove: true,
  originalGraph: false,
  crossOrigin: false,
  crossOriginHeader: "",
  rate: undefined,
  watermarkText: "",
  watermarkTextFont: "12px Sans-serif",
  watermarkTextColor: "#ffffff",
  watermarkTextX: 0.95,
  watermarkTextY: 0.95,
  smallToUpload: false,
  saveCutPosition: false,
  scaleAble: true,
  toolBoxOverflow: true,
  index: undefined,
  previewMode: true,
  fileType: "png",
  quality: 1,
  accept: "image/gif, image/jpeg ,image/png",
});

/* ============================================================
 * Emits
 * ============================================================ */

interface FaCutterImgEmits {
  (e: "update:imgUrl", url: string): void;
  (e: "cut-down", result: CutterResult): void;
  (e: "error", error: Error): void;
  (e: "choose-img", result: unknown): void;
  (e: "print-img", result: { dataURL: string }): void;
  (e: "clear-all"): void;
  (e: "image-load-complete", result: unknown): void;
  (e: "image-load-error", error: Error): void;
}

const emit = defineEmits<FaCutterImgEmits>();

/* ============================================================
 * Types
 * ============================================================ */

interface CutterResult {
  fileName: string;
  file: File;
  blob: Blob;
  dataURL: string;
}

/* ============================================================
 * State
 * ============================================================ */

const temImgPath = ref("");
const imgCutterModal = ref();
const confirmElRef = ref<HTMLElement>();

/* ============================================================
 * Computed: pass only native ImgCutter props
 * ============================================================ */

const IMG_CUTTER_PROP_KEYS = new Set([
  "isModal",
  "showChooseBtn",
  "lockScroll",
  "modalTitle",
  "boxWidth",
  "boxHeight",
  "cutWidth",
  "cutHeight",
  "tool",
  "toolBgc",
  "sizeChange",
  "moveAble",
  "imgMove",
  "originalGraph",
  "crossOrigin",
  "crossOriginHeader",
  "rate",
  "WatermarkText",
  "WatermarkTextFont",
  "WatermarkTextColor",
  "WatermarkTextX",
  "WatermarkTextY",
  "smallToUpload",
  "saveCutPosition",
  "scaleAble",
  "toolBoxOverflow",
  "index",
  "previewMode",
  "fileType",
  "quality",
  "accept",
  "afterChooseImg",
]);

const imgCutterProps = computed(() => {
  const result: Record<string, unknown> = {};

  for (const key of IMG_CUTTER_PROP_KEYS) {
    const k = key as keyof FaCutterImgProps;
    if (props[k] != null) {
      result[key] = props[k];
    }
  }

  // 水印文字兼容 deprecated WatermarkText
  if (props.watermarkText) {
    result.WatermarkText = props.watermarkText;
  }
  // 水印字体映射
  if (props.watermarkTextFont) {
    result.WatermarkTextFont = props.watermarkTextFont;
  }
  // 水印颜色映射
  if (props.watermarkTextColor) {
    result.WatermarkTextColor = props.watermarkTextColor;
  }
  // 水印位置映射
  if (props.watermarkTextX != null) {
    result.WatermarkTextX = props.watermarkTextX;
  }
  if (props.watermarkTextY != null) {
    result.WatermarkTextY = props.watermarkTextY;
  }
  // 比例映射
  if (props.rate) {
    result.rate = props.rate;
  }

  return result;
});

/* ============================================================
 * Methods: ImgCutter 事件处理 → emit camelCase 事件
 * ============================================================ */

function onCutDown(result: CutterResult) {
  emit("update:imgUrl", result.dataURL);
  emit("cut-down", result);
}

function onPrintImg(result: { dataURL: string }) {
  temImgPath.value = result.dataURL;
  emit("print-img", result);
}

function onChooseImg(result: unknown) {
  emit("choose-img", result);
}

function onClearAll() {
  temImgPath.value = "";
  emit("clear-all");
}

function onImageLoadComplete(result: unknown) {
  emit("image-load-complete", result);
}

function onImageLoadError(error: Error) {
  emit("error", error);
  emit("image-load-error", error);
}

function onError(error: Error) {
  emit("error", error);
}

/* ============================================================
 * Methods: 图片预加载
 * ============================================================ */

function preloadImage(url: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => resolve();
    img.onerror = reject;
    img.src = url;
  });
}

async function initImgCutter() {
  if (props.imgUrl) {
    try {
      await preloadImage(props.imgUrl);
      imgCutterModal.value?.handleOpen({
        name: "封面图片",
        src: props.imgUrl,
      });
    } catch (error) {
      emit("error", error as Error);
      console.error("图片加载失败:", error);
    }
  }
}

/* ============================================================
 * Watch: imgUrl 变化
 * ============================================================ */

watch(
  () => props.imgUrl,
  (newVal) => {
    if (newVal) {
      temImgPath.value = newVal;
      initImgCutter();
    }
  }
);

onMounted(() => {
  if (props.imgUrl) {
    temImgPath.value = props.imgUrl;
    initImgCutter();
  }
});

/* ============================================================
 * Methods: 下载
 * ============================================================ */

function handleDownload() {
  const a = document.createElement("a");
  a.href = temImgPath.value;
  a.download = "image.png";
  a.click();
}

function triggerCrop() {
  confirmElRef.value?.dispatchEvent(new MouseEvent("click", { bubbles: true }));
}
</script>

<style lang="scss" scoped>
.cutter-container {
  display: flex;
  flex-flow: row nowrap;

  .title {
    padding-bottom: 10px;
    font-size: 18px;
    font-weight: 500;
  }

  .cutter-component {
    margin-right: 30px;
  }

  .preview-container {
    flex-shrink: 0;

    .preview-box {
      background-color: var(--art-active-color) !important;

      .preview-img {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
    }

    .preview-actions {
      display: flex;
      gap: 12px;
      justify-content: center;
      margin-top: 20px;
    }
  }

  :deep(.toolBoxControl) {
    z-index: 100;
  }

  :deep(.dockMain) {
    right: 0;
    bottom: -40px;
    left: 0;
    z-index: 10;
    padding: 0;
    background-color: transparent !important;
    opacity: 1;
  }

  :deep(.copyright) {
    display: none !important;
  }

  :deep(.i-dialog-footer) {
    margin-top: 60px !important;
  }

  :deep(.dockBtn) {
    height: 26px;
    padding: 0 10px;
    font-size: 12px;
    line-height: 26px;
    color: var(--el-color-primary) !important;
    background-color: var(--el-color-primary-light-9) !important;
    border: 1px solid var(--el-color-primary-light-4) !important;
  }

  :deep(.dockBtnScrollBar) {
    margin: 0 10px 0 6px;
    background-color: var(--el-color-primary-light-1);
  }

  :deep(.scrollBarControl) {
    border-color: var(--el-color-primary);
  }

  :deep(.closeIcon) {
    line-height: 15px !important;
  }
}

.dark {
  .cutter-container {
    :deep(.toolBox) {
      border: transparent;
    }

    :deep(.dialogMain) {
      background-color: transparent !important;
    }

    :deep(.i-dialog-footer) {
      .btn {
        background-color: var(--el-color-primary) !important;
        border: transparent;
      }
    }
  }
}
</style>
