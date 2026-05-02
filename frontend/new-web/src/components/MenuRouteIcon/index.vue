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

  <!-- 本地 SVG：用 Vite URL，避免动态 `i-svg:*` 未被 Tailwind 扫描导致空白 -->
  <img
    v-else-if="isLocalSvgIcon && localSvgAssetUrl"
    :src="localSvgAssetUrl"
    alt=""
    :class="['menu-route-icon', 'menu-route-icon__local-img', iconClass]"
    :style="mergedStyle"
    draggable="false"
  />

  <div
    v-else-if="isLocalSvgIcon"
    :class="['menu-route-icon', localSvgClass, iconClass]"
    :style="mergedStyle"
  />

  <ArtSvgIcon v-else :icon="trimmedIcon" :color="color" :class="iconClass" :style="mergedStyle" />
</template>

<script setup lang="ts">
import { computed } from "vue";
import ArtSvgIcon from "@/components/core/base/art-svg-icon/index.vue";
import {
  elementMenuIconToEpIconify,
  isElementPlusStoredIcon,
  isIconifyStoredIcon,
  resolveElementPlusIconComponent,
} from "@/utils/menuIcon";
import { resolveMenuLocalSvgUrl } from "@/utils/menuLocalSvg";

defineOptions({ name: "MenuRouteIcon", inheritAttrs: false });

const props = defineProps<{
  icon?: string;
  color?: string;
  class?: string;
  style?: Record<string, unknown> | string;
}>();

const trimmedIcon = computed(() => props.icon?.trim() ?? "");

const elementComponent = computed(() => resolveElementPlusIconComponent(trimmedIcon.value));

/** 仅带 `el-icon-` 却解析不出 EP 组件时走 ep 兜底，裸名无效则仍按自定义 SVG 处理 */
const isInvalidElementPrefix = computed(
  () => !!trimmedIcon.value && isElementPlusStoredIcon(trimmedIcon.value) && !elementComponent.value
);

const epFallback = computed(() => elementMenuIconToEpIconify(trimmedIcon.value));

/** 非 Iconify、且不能映射为 EP 组件时，按 IconSelect「SVG」视为本地 `i-svg:` */
const isLocalSvgIcon = computed(() => {
  const ic = trimmedIcon.value;
  if (!ic || isIconifyStoredIcon(ic)) return false;
  if (resolveElementPlusIconComponent(ic)) return false;
  if (isElementPlusStoredIcon(ic)) return false;
  return true;
});

const localSvgAssetUrl = computed(() => {
  if (!isLocalSvgIcon.value) return undefined;
  return resolveMenuLocalSvgUrl(trimmedIcon.value);
});

const localSvgClass = computed(() => (trimmedIcon.value ? `i-svg:${trimmedIcon.value}` : ""));

const iconClass = computed(() => props.class ?? "");
const mergedStyle = computed(() => {
  const base = typeof props.style === "object" && props.style !== null ? { ...props.style } : {};
  if (props.color) {
    (base as Record<string, string>).color = props.color;
  }
  return base as Record<string, string>;
});
</script>

<style scoped lang="scss">
.menu-route-icon__local-img {
  flex-shrink: 0;
  width: 1em;
  height: 1em;
  vertical-align: -0.15em;
  object-fit: contain;
}
</style>
