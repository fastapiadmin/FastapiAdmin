<!-- 居中布局：与左侧栏一致的浅色底 + 中部淡化插画（不参与交互） -->
<template>
  <div
    class="login-center-backdrop"
    :class="{ 'login-center-backdrop--viewport-fixed': viewportFixed }"
    aria-hidden="true"
  >
    <div class="login-center-backdrop__bg" />
    <div class="login-center-backdrop__hero-wrap">
      <ThemeSvg :src="loginIcon" size="100%" class="login-center-backdrop__hero" />
    </div>
  </div>
</template>

<script setup lang="ts">
import loginIcon from "@imgs/svg/login_icon.svg";

defineOptions({ name: "LoginCenterBackdrop" });

withDefaults(
  defineProps<{
    /** 铺满视口并置于底层（与固定顶栏配合） */
    viewportFixed?: boolean;
  }>(),
  { viewportFixed: false }
);
</script>

<style scoped lang="scss">
.login-center-backdrop {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.login-center-backdrop--viewport-fixed {
  position: fixed;
  inset: 0;
  z-index: 0;
}

.login-center-backdrop__bg {
  position: absolute;
  inset: 0;
  background-color: color-mix(
    in srgb,
    var(--el-color-primary-light-9) 100%,
    var(--default-box-color)
  );
}

.login-center-backdrop__hero-wrap {
  position: absolute;
  top: 12%;
  left: 50%;
  width: min(420px, 52vw);
  height: min(340px, 38vh);
  opacity: 0.22;
  transform: translateX(-50%);
}

.login-center-backdrop__hero {
  width: 100%;
  height: 100%;
}

html.dark .login-center-backdrop__bg {
  background-color: color-mix(in srgb, var(--el-color-primary-light-9) 60%, #070707);
}

html.dark .login-center-backdrop__hero-wrap {
  opacity: 0.14;
}

@media only screen and (width <= 1180px) {
  .login-center-backdrop__hero-wrap {
    top: 10%;
    width: min(320px, 72vw);
    height: min(240px, 28vh);
  }
}
</style>
