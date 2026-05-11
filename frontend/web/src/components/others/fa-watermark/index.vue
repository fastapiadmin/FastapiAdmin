<!-- 水印组件 -->
<template>
  <div
    v-if="watermarkVisible"
    class="fixed left-0 top-0 h-screen w-screen pointer-events-none"
    :style="{ zIndex: zIndex }"
  >
    <ElWatermark
      :content="content"
      :font="watermarkFont"
      :rotate="rotate"
      :gap="[gapX, gapY]"
      :offset="[offsetX, offsetY]"
    >
      <div style="height: 100vh"></div>
    </ElWatermark>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { storeToRefs } from "pinia";
import AppConfig from "@/config";
import { defaultSettings } from "@/config/setting";
import { ThemeMode } from "@/enums";
import { hexToRgba } from "@utils/ui";
import { useSettingsStore } from "@stores/modules/setting.store";

defineOptions({ name: "FaWatermark" });

interface WatermarkProps {
  /** 水印内容 */
  content?: string;
  /** 水印是否可见 */
  visible?: boolean;
  /** 水印字体大小 */
  fontSize?: number;
  /** 水印字体颜色（不传则跟随设置里的主题色） */
  fontColor?: string;
  /** 水印旋转角度 */
  rotate?: number;
  /** 水印间距X */
  gapX?: number;
  /** 水印间距Y */
  gapY?: number;
  /** 水印偏移X */
  offsetX?: number;
  /** 水印偏移Y */
  offsetY?: number;
  /** 水印层级 */
  zIndex?: number;
}

const props = withDefaults(defineProps<WatermarkProps>(), {
  content: AppConfig.systemInfo.name,
  visible: false,
  fontSize: 16,
  fontColor: undefined,
  rotate: -22,
  gapX: 100,
  gapY: 100,
  offsetX: 50,
  offsetY: 50,
  zIndex: 3100,
});

const settingStore = useSettingsStore();
const { watermarkVisible, themeColor, theme } = storeToRefs(settingStore);

/** 未指定 fontColor 时使用当前主题色半透明，与 App.vue 全局水印策略一致 */
const watermarkFont = computed(() => {
  let color: string;
  if (props.fontColor) {
    color = props.fontColor;
  } else {
    const hex = themeColor.value || defaultSettings.themeColor;
    const alpha = theme.value === ThemeMode.DARK ? 0.22 : 0.16;
    try {
      color = hexToRgba(hex, alpha).rgba;
    } catch {
      color = hexToRgba(defaultSettings.themeColor, alpha).rgba;
    }
  }
  return { fontSize: props.fontSize, color };
});
</script>
