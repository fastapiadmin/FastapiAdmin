<!-- 路由 / 侧栏菜单图标：与 IconSelect 存值规则一致 -->
<template>
  <template v-if="!trimmedIcon" />

  <ElIcon
    v-else-if="elementComponent"
    :class="iconClass"
    :style="mergedStyle"
    class="menu-route-icon"
  >
    <component :is="elementComponent" />
  </ElIcon>

  <ArtSvgIcon
    v-else-if="isInvalidElementPrefix"
    :icon="epFallback"
    :color="color"
    :class="iconClass"
    :style="mergedStyle"
  />

  <ArtSvgIcon
    v-else
    :icon="resolvedArtIcon"
    :color="color"
    :class="iconClass"
    :style="mergedStyle"
  />
</template>

<script setup lang="ts">
import { computed } from "vue";
import ArtSvgIcon from "@/components/Core/base/art-svg-icon/index.vue";
import {
  elementMenuIconToEpIconify,
  isElementPlusStoredIcon,
  resolveElementPlusIconComponent,
} from "@/utils/menuIcon";
import { resolveIconForArtSvgIcon } from "@/utils/menuIconRemix";

defineOptions({ name: "MenuRouteIcon", inheritAttrs: false });

const props = defineProps<{
  icon?: string;
  color?: string;
  /** 与 Vue `class` 一致（含条件 `false`） */
  class?: import("vue").ClassValue;
  style?: Record<string, unknown> | string;
}>();

const trimmedIcon = computed(() => props.icon?.trim() ?? "");

const elementComponent = computed(() => resolveElementPlusIconComponent(trimmedIcon.value));

/** 仅带 `el-icon-` 却解析不出 EP 组件时走 ep 兜底，裸名无效则仍按自定义 SVG 处理 */
const isInvalidElementPrefix = computed(
  () => !!trimmedIcon.value && isElementPlusStoredIcon(trimmedIcon.value) && !elementComponent.value
);

const epFallback = computed(() => elementMenuIconToEpIconify(trimmedIcon.value));

/** Iconify（含历史本地 SVG 文件名 → Remix `ri:`） */
const resolvedArtIcon = computed(() => resolveIconForArtSvgIcon(trimmedIcon.value));

const iconClass = computed(() =>
  props.class === false || props.class == null ? undefined : props.class
);
const mergedStyle = computed(() => {
  const base = typeof props.style === "object" && props.style !== null ? { ...props.style } : {};
  if (props.color) {
    (base as Record<string, string>).color = props.color;
  }
  return base as Record<string, string>;
});
</script>
