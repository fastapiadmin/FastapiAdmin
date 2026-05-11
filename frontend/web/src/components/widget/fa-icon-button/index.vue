<!-- 按钮组件 -->
<template>
  <div
    class="size-8.5 inline-flex flex-cc c-p text-g-600 dark:text-g-800 text-xl rounded tad-300 hover:bg-hover-color"
    :class="{ 'rounded-full': circle }"
  >
    <FaSvgIcon :icon="icon"></FaSvgIcon>
    <slot></slot>
  </div>
</template>

<script lang="ts" setup>
import FaSvgIcon from "@/components/base/fa-svg-icon/index.vue";

defineOptions({ name: "FaIconButton" });

interface Props {
  /** 图标名称 */
  icon: string;
  /** 圆角按钮 */
  circle?: boolean;
}

withDefaults(defineProps<Props>(), {});
</script>
