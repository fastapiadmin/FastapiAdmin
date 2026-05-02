<template>
  <!-- 菜单图标 -->
  <template v-if="icon">
    <el-icon v-if="isElIcon" class="menu-icon">
      <component :is="iconComponent" />
    </el-icon>
    <img
      v-else-if="localSvgAssetUrl"
      :src="localSvgAssetUrl"
      alt=""
      class="menu-icon menu-icon--asset"
      draggable="false"
    />
    <div v-else :class="`i-svg:${icon}`" class="menu-icon" />
  </template>
  <template v-else>
    <img
      v-if="defaultMenuSvgUrl"
      :src="defaultMenuSvgUrl"
      alt=""
      class="menu-icon menu-icon--asset"
      draggable="false"
    />
    <div v-else class="i-svg:menu menu-icon" />
  </template>
  <!-- 菜单标题 -->
  <span v-if="title" class="menu-title ml-1">{{ translateRouteTitle(title) }}</span>
</template>

<script setup lang="ts">
import { translateRouteTitle } from "@/utils/i18n";
import { computed } from "vue";
import { resolveMenuLocalSvgUrl } from "@/utils/menuLocalSvg";

const props = defineProps<{
  icon?: string;
  title?: string;
}>();

const isElIcon = computed(() => props.icon?.startsWith("el-icon"));
const iconComponent = computed(() => props.icon?.replace("el-icon-", ""));

/** 动态 `i-svg:*` 可能未被 Tailwind 打出样式，优先用 assets 直链 */
const localSvgAssetUrl = computed(() => {
  const ic = props.icon?.trim();
  if (!ic || ic.startsWith("el-icon") || ic.includes(":")) return undefined;
  return resolveMenuLocalSvgUrl(ic);
});

const defaultMenuSvgUrl = computed(() => resolveMenuLocalSvgUrl("menu"));
</script>

<style lang="scss" scoped>
.menu-icon {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  margin-right: 5px;
  font-size: 18px;
  color: currentcolor;
}

.menu-icon--asset {
  object-fit: contain;
}
</style>
