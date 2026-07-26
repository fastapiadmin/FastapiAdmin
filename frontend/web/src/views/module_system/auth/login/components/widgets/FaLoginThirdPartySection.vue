<!-- 第三方 OAuth 登录（后端需配置各渠道 ClientId/Secret） -->
<template>
  <div class="third-party-login login-third-on-dark">
    <div class="divider-container">
      <div class="divider-line" />
      <span class="divider-text">{{ $t("login.otherLoginMethods") }}</span>
      <div class="divider-line" />
    </div>
    <div
      class="login-third-party-icons flex w-full items-center justify-center gap-x-3 sm:gap-x-4 max-sm:gap-x-2"
    >
      <ElTooltip
        v-for="item in oauthItems"
        :key="item.provider"
        :content="item.tip"
        placement="top"
      >
        <button
          type="button"
          class="oauth-social-btn flex size-10 max-sm:size-8 shrink-0 cursor-pointer items-center justify-center rounded-full border-0 bg-transparent transition-colors duration-200 outline-none"
          :aria-label="item.tip"
          @click="$emit('oauth', item.provider)"
        >
          <FaSvgIcon :icon="item.icon" :class="item.iconClass" />
        </button>
      </ElTooltip>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { OAuthProvider } from "@/api/module_system/auth";

defineOptions({ name: "FaLoginThirdPartySection" });

interface Emits {
  oauth: [provider: OAuthProvider];
}

defineEmits<Emits>();

const { t } = useI18n();

const oauthItems = computed(() => [
  {
    provider: "wechat" as const,
    tip: t("login.oauthTooltip.wechat"),
    icon: "simple-icons:wechat",
    iconClass: "size-[22px] max-sm:size-[18px] text-[#07c160]",
  },
  {
    provider: "qq" as const,
    tip: t("login.oauthTooltip.qq"),
    icon: "simple-icons:tencentqq",
    iconClass: "size-[22px] max-sm:size-[18px] text-[#12b7f5]",
  },
  {
    provider: "github" as const,
    tip: t("login.oauthTooltip.github"),
    icon: "mdi:github",
    iconClass: "size-[22px] max-sm:size-[18px] text-g-800 dark:text-white/85",
  },
  {
    provider: "gitee" as const,
    tip: t("login.oauthTooltip.gitee"),
    icon: "simple-icons:gitee",
    iconClass: "size-[22px] max-sm:size-[18px] text-[#c71d23]",
  },
]);
</script>
