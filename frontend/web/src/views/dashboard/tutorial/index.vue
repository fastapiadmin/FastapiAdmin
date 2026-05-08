<!-- 操作教程：内置视频演示（可改为自有 CDN / 资源地址） -->
<template>
  <div class="page-content tutorial-page">
    <div class="max-w-200 mx-auto">
      <h1 class="text-2xl font-medium text-g-900 dark:text-g-50 mb-2">操作教程</h1>
      <p class="text-sm text-g-600 mb-6">
        以下为系统常用操作演示视频，可随时暂停、调速与全屏观看。正式环境请将视频地址替换为自有素材。
      </p>

      <div class="art-card-sm p-5">
        <h2 class="text-lg font-semibold mb-4">快速上手</h2>
        <div class="max-w-full tutorial-page__player">
          <ArtVideoPlayer
            player-id="dashboard-tutorial-player"
            :video-url="videoUrl"
            :poster-url="posterUrl"
            :autoplay="false"
            :volume="1"
            :playback-rates="[0.5, 1, 1.5, 2]"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import lockImg from "@imgs/lock/bg_dark.webp";

defineOptions({ name: "DashboardTutorial" });

/** 演示用在线 MP4，上线后建议改为自有 OSS / 静态资源地址 */
const DEFAULT_VIDEO =
  "//lf3-static.bytednsdoc.com/obj/eden-cn/nupenuvpxnuvo/xgplayer_doc/xgplayer-demo.mp4";

const videoUrl = ref(DEFAULT_VIDEO);
const posterUrl = ref(lockImg);
</script>

<style scoped lang="scss">
.tutorial-page__player {
  width: 100%;
}
</style>
