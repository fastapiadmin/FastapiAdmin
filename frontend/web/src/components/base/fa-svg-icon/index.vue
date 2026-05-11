<!-- 图标组件 -->
<template>
  <Icon v-if="icon" :icon="icon" v-bind="bindAttrs" class="fa-svg-icon inline" />
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

defineOptions({ name: "FaSvgIcon", inheritAttrs: false });

interface Props {
  /** Iconify icon name */
  icon?: string;
}

defineProps<Props>();

const attrs = useAttrs();

const bindAttrs = computed<{ class: string; style: string }>(() => ({
  class: (attrs.class as string) || "",
  style: (attrs.style as string) || "",
}));
</script>

<!-- <template>
  <div class="space-y-5 mb-5">
    <div class="text-2xl font-medium mt-5 max-sm:text-2xl max-sm:mt-3">图标</div>
    <div class="text-g-800">
      v.3.0 版本图标库升级为 iconify，可在
      <a href="https://icones.js.org/" target="_blank" class="text-theme hover:underline">
        Iconify
      </a>
      中查找，支持多种图标库，如 Remix Icon, Solar, Tabler Icons 等。
    </div>
    <div class="text-g-800">
      为确保系统图标风格统一，项目全部采用 Remix Icon 图标库，可在
      <a
        href="https://icones.js.org/collection/ri"
        target="_blank"
        class="text-theme hover:underline"
      >
        Iconify
      </a>
      或
      <a href="https://remixicon.com/" target="_blank" class="text-theme hover:underline">
        Remix Icon 官网
      </a>
      搜索使用。
    </div> -->

<!-- Iconify 图标 -->
<!-- <div class="fa-card-sm p-5">
      <div class="text-lg font-semibold mb-4">Iconify</div>
      <div class="flex items-center gap-6">
        <FaSvgIcon icon="ri:github-fill" class="text-2xl" />
        <FaSvgIcon icon="ri:copilot-line" class="text-2xl text-theme" />
        <FaSvgIcon icon="ri:edge-line" class="text-2xl text-secondary" />
        <FaSvgIcon icon="ri:planet-line" class="text-2xl text-warning" />
        <FaSvgIcon icon="ri:windows-line" class="text-2xl text-info" />
        <FaSvgIcon icon="ri:thumb-up-line" class="text-2xl text-danger" />
        <FaSvgIcon icon="ri:gift-2-line" class="text-2xl text-success" />
        <FaSvgIcon icon="ri:apple-line" class="text-2xl text-secondary" />
      </div>
    </div> -->

<!-- Svg Icons -->
<!-- <div class="fa-card-sm p-5">
      <div class="text-lg font-semibold mb-4">Svg Icons</div>
      <div class="flex items-center gap-6">
        <FaSvgIcon icon="svg-spinners:3-dots-fade" class="text-2xl text-red-400" />
        <FaSvgIcon icon="svg-spinners:3-dots-bounce" class="text-2xl text-blue-400" />
        <FaSvgIcon icon="svg-spinners:3-dots-move" class="text-2xl text-orange-400" />
        <FaSvgIcon icon="svg-spinners:3-dots-rotate" class="text-2xl text-purple-400" />
        <FaSvgIcon icon="svg-spinners:blocks-shuffle-2" class="text-2xl text-pink-300" />
        <FaSvgIcon icon="svg-spinners:clock" class="text-2xl text-yellow-500" />
        <FaSvgIcon icon="svg-spinners:tadpole" class="text-2xl text-orange-500" />
        <FaSvgIcon icon="svg-spinners:blocks-wave" class="text-2xl text-blue-500" />
      </div>
    </div> -->

<!-- Svg Icons -->
<!-- <div class="fa-card-sm p-5">
      <div class="text-lg font-semibold mb-4">Material Line Icons</div>
      <div class="flex items-center gap-6">
        <FaSvgIcon icon="line-md:phone-call-twotone-loop" class="text-2xl text-blue-500" />

        <FaSvgIcon icon="line-md:switch-off" class="text-2xl text-green-500" />
        <FaSvgIcon icon="line-md:sun-rising-filled-loop" class="text-2xl text-yellow-400" />
        <FaSvgIcon icon="line-md:volume-high-filled" class="text-2xl text-purple-500" />
        <FaSvgIcon icon="line-md:github-twotone" class="text-2xl text-gray-700" />
        <FaSvgIcon icon="line-md:telegram" class="text-2xl text-sky-500" />
        <FaSvgIcon icon="line-md:reddit-loop" class="text-2xl text-orange-400" />
        <FaSvgIcon
          icon="line-md:coffee-half-empty-filled-loop"
          class="text-2xl text-emerald-500"
        />
      </div>
    </div> -->

<!-- 使用示例 -->
<!-- <div class="fa-card-sm p-5">
      <div class="text-lg font-semibold mb-4">使用示例</div>
      <div class="space-y-4">
        <div>
          <div class="text-sm text-g-600 mb-2">基础使用</div>
          <div class="bg-g-200 dark:bg-g-300/30 p-4 rounded font-mono text-sm text-g-800">
            &lt;FaSvgIcon icon="ri:home-line" /&gt;
          </div>
        </div>
        <div>
          <div class="text-sm text-g-600 mb-2">自定义大小</div>
          <div class="bg-g-200 dark:bg-g-300/30 p-4 rounded font-mono text-sm text-g-800">
            &lt;FaSvgIcon icon="ri:user-line" class="text-2xl" /&gt;
          </div>
        </div>
        <div>
          <div class="text-sm text-g-600 mb-2">自定义颜色</div>
          <div class="bg-g-200 dark:bg-g-300/30 p-4 rounded font-mono text-sm text-g-800">
            &lt;FaSvgIcon icon="ri:hefa-fill" class="text-red-500" /&gt;
          </div>
        </div>
        <div>
          <div class="text-sm text-g-600 mb-2">组合使用</div>
          <div class="bg-g-200 dark:bg-g-300/30 p-4 rounded font-mono text-sm text-g-800">
            &lt;FaSvgIcon icon="ri:star-fill" class="text-4xl text-yellow-500" /&gt;
          </div>
        </div>
      </div>
    </div>
  </div>
</template> -->

<!-- <script setup lang="ts">
import FaSvgIcon from "@/components/base/fa-svg-icon/index.vue";

defineOptions({ name: "IconPage" });
</script> -->
