<template>
  <ElTag :type="type" :size="size" :effect="effect" :round="round" :closable="closable">
    {{ label }}
  </ElTag>
</template>

<script setup lang="ts">
import { ElTag } from "element-plus";

defineOptions({ name: "FaStatusTag" });

interface Props {
  /** 显示文本 */
  label?: string | number;
  /**
   * 标签类型（与 EP ElTag 一致）。
   * 不传时为 EP 默认样式（无 type 属性）。
   */
  type?: "primary" | "success" | "warning" | "danger" | "info";
  /** 尺寸 */
  size?: "large" | "default" | "small";
  /** 主题效果：light（默认）/ dark / plain */
  effect?: "light" | "dark" | "plain";
  /** 是否圆角 */
  round?: boolean;
  /** 是否可关闭 */
  closable?: boolean;
}

withDefaults(defineProps<Props>(), {
  label: "",
  type: undefined,
  size: undefined,
  effect: "light",
  round: false,
  closable: false,
});
</script>
