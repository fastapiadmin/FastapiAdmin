<!-- 图片卡片 -->
<template>
  <div class="w-full cursor-pointer h-full" @click="handleClick">
    <div class="fa-card overflow-hidden h-full">
      <div class="relative w-full aspect-16/10 overflow-hidden">
        <ElImage
          :src="props.imageUrl"
          fit="cover"
          class="w-full h-full transition-transform duration-300 ease-in-out hover:scale-105"
        >
          <template #placeholder>
            <div class="flex items-center justify-center w-full h-full bg-(--el-fill-color-light)">
              <ElIcon><FaSvgIcon icon="ri:image-line" /></ElIcon>
            </div>
          </template>
          <template #error>
            <div
              class="flex flex-col items-center justify-center w-full h-full gap-1 bg-(--el-fill-color-light)"
            >
              <FaSvgIcon icon="ri:image-line" class="text-2xl text-g-400" />
              <span class="text-xs text-g-400">图片加载失败</span>
            </div>
          </template>
        </ElImage>
        <div
          class="absolute right-3.5 bottom-3.5 py-1 px-2 text-xs bg-g-200 rounded"
          v-if="props.readTime"
        >
          {{ props.readTime }} 阅读
        </div>
      </div>

      <div class="p-4">
        <div
          class="inline-block py-0.5 px-2 mb-2 text-xs bg-g-300/70 rounded"
          v-if="props.category"
        >
          {{ props.category }}
        </div>
        <p class="m-0 mb-3 text-base font-medium truncate" :title="props.title">{{ props.title }}</p>
        <div class="flex items-center gap-4 text-xs text-g-600">
          <span class="flex items-center gap-1" v-if="props.views">
            <ElIcon class="text-base"><FaSvgIcon icon="ri:eye-line" /></ElIcon>
            {{ props.views }}
          </span>
          <span class="flex items-center gap-1" v-if="props.comments">
            <ElIcon class="text-base"><FaSvgIcon icon="ri:chat-3-line" /></ElIcon>
            {{ props.comments }}
          </span>
          <span>{{ props.date }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "FaImageCard" });

interface Props {
  /** 图片地址 */
  imageUrl?: string;
  /** 标题 */
  title?: string;
  /** 分类 */
  category?: string;
  /** 阅读时间 */
  readTime?: string;
  /** 浏览量 */
  views?: number;
  /** 评论数 */
  comments?: number;
  /** 日期 */
  date?: string;
}

const props = withDefaults(defineProps<Props>(), {
  imageUrl: "",
  title: "",
  category: "",
  readTime: "",
  views: 0,
  comments: 0,
  date: "",
});

interface Emits {
  click: [card: Props];
}

const emit = defineEmits<Emits>();

const handleClick = () => {
  emit("click", props);
};
</script>
