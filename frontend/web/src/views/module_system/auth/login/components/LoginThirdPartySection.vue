<!-- 第三方 OAuth 登录（后端需配置各渠道 ClientId/Secret） -->
<template>
  <div class="third-party-login login-third-on-dark">
    <div class="divider-container">
      <div class="divider-line" />
      <span class="divider-text">{{ $t("login.otherLoginMethods") }}</span>
      <div class="divider-line" />
    </div>
    <div class="login-third-party-icons flex w-full items-center justify-center gap-x-3 sm:gap-x-4">
      <ElTooltip
        v-for="item in oauthItems"
        :key="item.provider"
        :content="item.tip"
        placement="top"
      >
        <button
          type="button"
          class="oauth-social-btn flex size-10 shrink-0 cursor-pointer items-center justify-center rounded-full border-0 bg-transparent transition-colors duration-200 outline-none"
          :aria-label="item.tip"
          @click="$emit('oauth', item.provider)"
        >
          <ArtSvgIcon :icon="item.icon" :class="item.iconClass" />
        </button>
      </ElTooltip>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { OAuthProvider } from "@/api/module_system/auth";

defineEmits<{ oauth: [provider: OAuthProvider] }>();

const { t } = useI18n();

const oauthItems = computed(() => [
  {
    provider: "wechat" as const,
    tip: t("login.oauthTooltip.wechat"),
    icon: "simple-icons:wechat",
    iconClass: "size-[22px] text-[#07c160]",
  },
  {
    provider: "qq" as const,
    tip: t("login.oauthTooltip.qq"),
    icon: "simple-icons:tencentqq",
    iconClass: "size-[22px] text-[#12b7f5]",
  },
  {
    provider: "github" as const,
    tip: t("login.oauthTooltip.github"),
    icon: "mdi:github",
    iconClass: "size-[22px] text-g-800 dark:text-white/85",
  },
  {
    provider: "gitee" as const,
    tip: t("login.oauthTooltip.gitee"),
    icon: "simple-icons:gitee",
    iconClass: "size-[22px] text-[#c71d23]",
  },
]);
</script>

<style scoped lang="scss">
.login-third-on-dark {
  margin-top: 1rem;

  .divider-container {
    display: flex;
    align-items: center;
    margin-bottom: 0.75rem;
  }

  .divider-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--el-border-color-lighter), transparent);
  }

  .divider-text {
    padding: 0 12px;
    font-size: 12px;
    color: var(--el-text-color-secondary);
    white-space: nowrap;
  }
}

html.dark .login-third-on-dark {
  .divider-line {
    background: linear-gradient(to right, transparent, rgb(255 255 255 / 15%), transparent);
  }

  .divider-text {
    color: rgb(255 255 255 / 38%);
  }
}

.oauth-social-btn:hover {
  background-color: var(--el-fill-color-light);
}

.oauth-social-btn:focus-visible {
  box-shadow: 0 0 0 2px var(--el-color-primary-light-7);
}

html.dark .oauth-social-btn:hover {
  background-color: rgb(255 255 255 / 10%);
}
</style>
