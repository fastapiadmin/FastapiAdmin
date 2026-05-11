<!-- 系统 logo：优先使用接口 sys_web_logo，缺省用内置图 -->
<template>
  <div class="flex-cc">
    <img
      :style="logoStyle"
      :src="resolvedSrc"
      alt="logo"
      class="h-full w-full object-contain"
      @error="onImgError"
    />
  </div>
</template>

<script setup lang="ts">
import defaultLogoUrl from "@icons/vite.svg";

defineOptions({ name: "FaLogo" });

interface Props {
  /** logo 大小 */
  size?: number | string;
  /** 自定义地址（如配置接口 sys_web_logo）；不传则用默认资源 */
  src?: string;
}

const props = withDefaults(defineProps<Props>(), {
  size: 36,
  src: undefined,
});

const fallbackTriggered = ref(false);

const resolvedSrc = computed(() => {
  if (fallbackTriggered.value) return defaultLogoUrl;
  const custom = props.src?.trim();
  return custom || defaultLogoUrl;
});

function onImgError() {
  if (!fallbackTriggered.value) {
    fallbackTriggered.value = true;
  }
}

const logoStyle = computed(() => ({ width: `${props.size}px`, height: `${props.size}px` }));

watch(
  () => props.src,
  () => {
    fallbackTriggered.value = false;
  }
);
</script>
