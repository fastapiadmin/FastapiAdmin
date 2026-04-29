<!-- 自定义 iframe 组件 -->
<template>
  <div v-loading="loading" :style="'height:' + height">
    <iframe :src="url" frameborder="0" width="100%" height="100%" scrolling="auto" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const props = defineProps({
  src: {
    type: String,
    required: true,
  },
});

const height = ref(document.documentElement.clientHeight - 94.5 + "px;");
const loading = ref(true);
const url = computed(() => props.src);

onMounted(() => {
  setTimeout(() => {
    loading.value = false;
  }, 300);
});
</script>

<style lang="scss" scoped>
/** 关闭tag标签  */
.app-container {
  /* 50px = navbar = 50px */
  height: calc(100vh - 50px);
}

/** 开启tag标签  */
.hasTagsView {
  .app-container {
    /* 84px = navbar + tags-view = 50px + 34px */
    height: calc(100vh - 84px);
  }
}
</style>
