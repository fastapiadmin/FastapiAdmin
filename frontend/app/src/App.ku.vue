<script setup lang="ts">
const { themeVars, theme } = useManualTheme()
</script>

<template>
  <wd-config-provider :theme-vars="themeVars" :theme="theme" :custom-class="`page-wraper ${theme}`">
    <ku-root-view />
    <wd-notify />
    <wd-message-box />
    <wd-toast />
    <global-loading />
    <global-toast />
    <global-message />
    <!-- #ifdef MP-WEIXIN -->
    <privacy-popup />
    <!-- #endif -->

    <!-- 文字水印 -->
    <wd-watermark content="fastapp" :width="130" :height="130" />
  </wd-config-provider>
</template>
