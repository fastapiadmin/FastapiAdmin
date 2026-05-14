<template>
  <FaBasicBanner
    class="justify-center !h-53 max-sm:!pt-8 max-sm:!h-48"
    :title="`欢迎回来 ${userInfo?.username}`"
    boxStyle="!bg-theme/10"
    titleColor="var(--fa-gray-900)"
    :decoration="false"
    :meteorConfig="{
      enabled: true,
      count: 10,
    }"
    :buttonConfig="{
      show: false,
      text: '',
    }"
    :imageConfig="{
      src: bannerCover,
      width: '18rem',
      bottom: '-7.5rem',
    }"
    @click="handleBannerClick"
  >
    <div class="flex mt-6">
      <div class="mr-8 pr-8 border-r border-g-400 dark:border-g-300/60">
        <p class="text-3xl">
          <FaCountTo
            class="number box-title"
            :target="2340"
            :duration="1500"
            prefix="¥"
            separator=","
          />
          <FaSvgIcon icon="ri:arrow-right-up-line" class="text-xl text-success relative -top-2" />
        </p>
        <p class="mt-1 text-sm text-g-700">今日销售额</p>
      </div>
      <div class="mr-8">
        <p class="text-3xl">
          <FaCountTo class="number box-title" :target="35" :duration="1500" suffix="%" />
          <FaSvgIcon icon="ri:arrow-right-up-line" class="text-xl text-success relative -top-2" />
        </p>
        <p class="mt-1 text-sm text-g-700">较昨日</p>
      </div>
    </div>
  </FaBasicBanner>
</template>

<script setup lang="ts">
import bannerCover from "@imgs/login/lf_icon2.webp";
import { useUserStore } from "@stores/modules/user.store";

const userStore = useUserStore();

/**
 * 获取当前用户信息
 */
const userInfo = computed(() => userStore.basicInfo);

/**
 * 处理横幅点击事件
 */
const handleBannerClick = (): void => {
  // TODO: 添加横幅点击处理逻辑
};
</script>
