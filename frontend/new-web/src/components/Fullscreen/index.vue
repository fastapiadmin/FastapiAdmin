<!-- 全屏切换按钮 -->
<template>
  <div @click="toggle">
    <ArtSvgIcon :icon="resolveIconForArtSvgIcon(isFullscreen ? 'fullscreen-exit' : 'fullscreen')" />
  </div>
</template>

<script setup lang="ts">
import ArtSvgIcon from "@/components/Core/base/art-svg-icon/index.vue";
import { resolveIconForArtSvgIcon } from "@/utils/menuIconRemix";

const { isFullscreen, toggle } = useFullscreen();
</script>

<style lang="scss" scoped></style>
