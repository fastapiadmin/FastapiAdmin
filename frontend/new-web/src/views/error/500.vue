<template>
  <el-result
    :title="t('error.networkError')"
    sub-title="请确认您的网络是否正常，或者点击下方按钮返回首页。"
  >
    <template #icon>
      <!-- 此处必须img，如果是el-icon则无法识别 @ -->
      <img class="min-w-[23.4375rem] sm:w-120" src="@/assets/images/500.svg" alt="500" />
    </template>
    <template #extra>
      <el-button round type="primary" @click="back">{{ t("error.returnToHome") }}</el-button>
    </template>
  </el-result>
</template>

<script setup lang="ts">
defineOptions({ name: "Page500" });
const router = useRouter();
const back = () => router.push("/");
const t = useI18n().t;
</script>

<style lang="scss" scoped></style>
