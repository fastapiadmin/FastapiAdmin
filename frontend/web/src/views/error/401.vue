<template>
  <el-result
    :title="t('error.noPermission')"
    sub-title="请确认您的权限是否满足操作要求，或者点击下方按钮返回首页。"
  >
    <template #icon>
      <!-- 此处必须img，如果是el-icon则无法识别 @ -->
      <img class="min-w-[23.4375rem] sm:w-120" src="@/assets/images/401.svg" alt="401" />
    </template>
    <template #extra>
      <el-button round type="primary" @click="back">{{ t("error.returnToHome") }}</el-button>
    </template>
  </el-result>
</template>

<script setup lang="ts">
defineOptions({ name: "Page401" });
const router = useRouter();
const back = () => router.push("/");
const t = useI18n().t;
</script>

<style lang="scss" scoped>
@mixin slide-up-animation($delay: 0s) {
  opacity: 0;
  animation-name: slideUp;
  animation-duration: 0.5s;
  animation-delay: $delay;
  animation-fill-mode: forwards;
}

@keyframes slideUp {
  0% {
    opacity: 0;
    transform: translateY(60px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.oops {
  color: var(--el-color-primary);
  @include slide-up-animation(0s);
}

.headline {
  @include slide-up-animation(0.1s);
}

.info {
  @include slide-up-animation(0.2s);
}

.btn {
  @include slide-up-animation(0.3s);
}
</style>
