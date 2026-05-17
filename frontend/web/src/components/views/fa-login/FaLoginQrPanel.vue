<!-- 扫码登录（无后端会话，演示二维码与交互） -->
<template>
  <div>
    <div class="login-page-form login-qr-flow flex w-full min-w-0 flex-col items-center">
      <div
        class="login-qr-card flex w-full max-w-[280px] flex-col items-center rounded-2xl bg-white p-6 shadow-[0_8px_24px_rgb(0_0_0_/12%)] dark:shadow-[0_8px_28px_rgb(0_0_0_/45%)]"
      >
        <QrcodeVue class="block" :value="qrPayload" v-bind="qrCodeRenderOptions" />
      </div>

      <p
        class="login-qr-hint mt-4 max-w-[280px] text-center text-sm leading-relaxed text-(--el-text-color-secondary)"
      >
        {{ $t("login.qrLoginHint") }}
      </p>

      <div class="login-mobile-actions mt-8 w-full min-w-0">
        <ElButton
          class="login-secondary-btn h-11 w-full min-w-0 rounded-lg! text-base font-medium"
          plain
          @click="$emit('back')"
        >
          {{ $t("login.backToAccountLogin") }}
        </ElButton>
      </div>
    </div>

    <FaLoginAuthLinkRow
      :hint="$t('login.noAccount')"
      :link-text="$t('login.register')"
      @link="$emit('register')"
    />
  </div>
</template>

<script setup lang="ts">
import QrcodeVue from "qrcode.vue";
import type { Level, RenderAs } from "qrcode.vue";

defineEmits<{ back: []; register: [] }>();

/** 集中配置 + H 级纠错 + SVG（矢量清晰、易对齐容器） */
const qrCodeRenderOptions: {
  size: number;
  level: Level;
  renderAs: RenderAs;
  margin: number;
  background: string;
  foreground: string;
} = {
  size: 220,
  level: "H",
  renderAs: "svg",
  margin: 0,
  background: "#ffffff",
  foreground: "#000000",
};

/** 演示用载荷；接入后端后替换为会话 URL / ticket */
const qrPayload = computed(() => {
  if (typeof window === "undefined") return "https://example.com/login";
  const { origin, pathname } = window.location;
  return `${origin}${pathname}?qrLogin=demo`;
});
</script>

<style scoped lang="scss">
@import "@styles/fa-login.css";

.login-qr-flow {
  margin-top: 1rem;
}

.login-qr-card {
  box-sizing: border-box;
}

/* EP：相邻按钮横向间距；单列返回按钮无需处理 */
.login-mobile-actions {
  :deep(.el-button) {
    box-sizing: border-box;
    width: 100%;
    min-width: 0;
    max-width: 100%;
  }
}
</style>
