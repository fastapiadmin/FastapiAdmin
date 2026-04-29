<!-- 接口文档 -->
<template>
  <div class="app-container">
    <Frame :src="url" />
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "Redoc",
  inheritAttrs: false,
});

const url = ref(import.meta.env.VITE_APP_BASE_API + "/redoc");

onBeforeUnmount(() => {
  window.onresize = null;
});
</script>

<style lang="scss" scoped></style>
