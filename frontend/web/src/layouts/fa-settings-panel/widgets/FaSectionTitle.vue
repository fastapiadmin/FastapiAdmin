<template>
  <p
    class="relative mt-7.5 mb-5.5 text-sm text-center text-g-800 before:absolute before:top-2.5 before:left-0 before:w-12.5 before:m-auto before:content-[''] before:border-b before:border-(--fa-gray-300) after:absolute after:top-2.5 after:right-0 after:w-12.5 after:m-auto after:content-[''] after:border-b after:border-g-300"
    :style="style"
  >
    {{ title }}
  </p>
</template>

<script setup lang="ts">
defineOptions({ name: "FaSectionTitle" });

interface Props {
  title: string;
  style?: Record<string, any>;
}

withDefaults(defineProps<Props>(), {
  style: () => ({}),
});
</script>
