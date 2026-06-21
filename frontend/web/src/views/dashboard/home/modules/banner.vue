<template>
  <FaBasicBanner
    class="justify-center h-54! max-sm:pt-8! max-sm:h-48!"
    :title="bannerTitle"
    :subtitle="bannerSubtitle"
    boxStyle="bg-theme/10!"
    titleColor="var(--fa-gray-900)"
    subtitleColor="var(--fa-gray-500)"
    :decoration="false"
    :meteorConfig="{
      enabled: true,
      count: 10,
    }"
    :buttonConfig="{
      show: false,
      text: '开始探索',
      color: 'var(--fa-success)',
      textColor: '#fff',
      radius: '6px',
    }"
    :imageConfig="{
      src: bannerCover,
      width: '18rem',
      bottom: '-7.5rem',
    }"
    @click="handleBannerClick"
  >
    <div class="flex items-center gap-4 mt-2">
      <ElAvatar
        v-if="currentUser.avatar"
        :size="80"
        :src="currentUser.avatar"
        style="background-color: transparent"
      />
      <ElIcon v-else :size="56" class="text-g-500"><UserFilled /></ElIcon>
      <div>
        <div class="text-lg font-semibold text-g-800">{{ currentUser.name }}</div>
        <div class="text-sm text-g-600">
          {{ currentUser.dept_name }} · {{ currentUser.description }} · {{ currentUser.last_login }}
        </div>
      </div>
    </div>
  </FaBasicBanner>
</template>

<script setup lang="ts">
import { computed } from "vue";
import bannerCover from "@imgs/login/lf_icon2.webp";
import FaBasicBanner from "@/components/banners/fa-basic-banner/index.vue";
import { useUserStore } from "@stores";
import { greetings } from "@utils";
import { UserFilled } from "@element-plus/icons-vue";

const userStore = useUserStore();

const userInfo = computed(() => userStore.basicInfo);

const handleBannerClick = (): void => {
  // TODO: 接入真实跳转或路由
};

const timefix = greetings();
const welcome = "祝你开心每一天！";
const currentUser = {
  avatar: userStore.basicInfo.avatar || "",
  name: userInfo.value.name || "吴彦祖",
  username: userInfo.value.username || "账号信息",
  description: userInfo.value.description || "用户说明",
  dept_name: userInfo.value.dept_name || "软件专业部",
  last_login: userInfo.value.last_login || "2023-01-01 00:00:00",
};

const bannerTitle = `欢迎回来 ～ ${currentUser.name}（${currentUser.username}） ${timefix} ${welcome}`;

const bannerSubtitle = `基于 FastAPI + Vue3 + TypeScript 构建的企业级中后台解决方案，支持多端开发。`;
</script>

<style scoped lang="scss"></style>
