<!-- 账号密码登录表单（含快捷账号、验证码、滑块） -->
<template>
  <div>
    <ElForm
      ref="formRef"
      :model="loginForm"
      :rules="rules"
      :key="formKey"
      class="login-page-form"
      :validate-on-rule-change="false"
      @keyup.enter="$emit('submit')"
    >
      <ElFormItem>
        <ElSelect
          :model-value="demoAccountKey"
          class="w-full"
          :placeholder="$t('login.quickSelectAccount')"
          @update:model-value="$emit('setupAccount', $event as AccountKey)"
        >
          <ElOption
            v-for="account in accounts"
            :key="account.key"
            :label="account.label"
            :value="account.key"
          >
            <span>{{ account.label }}</span>
          </ElOption>
        </ElSelect>
      </ElFormItem>

      <ElFormItem prop="username">
        <ElInput
          class="custom-height"
          v-model.trim="loginForm.username"
          clearable
          :placeholder="$t('login.placeholder.username')"
        >
          <template #prefix>
            <ElIcon><User /></ElIcon>
          </template>
        </ElInput>
      </ElFormItem>

      <ElTooltip :visible="isCapsLock" :content="$t('login.capsLock')" placement="right">
        <ElFormItem prop="password">
          <ElInput
            class="custom-height"
            v-model.trim="loginForm.password"
            type="password"
            autocomplete="off"
            show-password
            clearable
            :placeholder="$t('login.placeholder.password')"
            @keyup="checkCapsLock"
            @keyup.enter="$emit('submit')"
          >
            <template #prefix>
              <ElIcon><Lock /></ElIcon>
            </template>
          </ElInput>
        </ElFormItem>
      </ElTooltip>

      <ElFormItem v-if="captchaState.enable" prop="captcha" class="login-captcha-row">
        <div class="flex w-full items-center gap-2.5">
          <ElInput
            v-model.trim="loginForm.captcha"
            class="custom-height flex-1"
            clearable
            :placeholder="$t('login.captchaCode')"
            @keyup.enter="$emit('submit')"
          >
            <template #prefix>
              <FaSvgIcon
                icon="mdi:shield-lock-outline"
                class="size-[18px] text-[var(--el-text-color-secondary)]"
              />
            </template>
          </ElInput>
          <div
            class="login-captcha-img flex h-10 w-[100px] shrink-0 cursor-pointer items-center justify-center overflow-hidden rounded"
            role="button"
            :title="$t('login.captchaClickHint')"
            @click="$emit('getCaptcha')"
          >
            <ElIcon v-if="codeLoading" class="is-loading" :size="20">
              <Loading />
            </ElIcon>
            <ElImage
              v-else-if="captchaState.img_base"
              class="h-full w-full object-cover"
              fit="cover"
              :src="captchaState.img_base"
            />
            <ElText v-else type="info" size="small">
              {{ $t("login.captchaClickHint") }}
            </ElText>
          </div>
        </div>
      </ElFormItem>

      <div class="login-form-tail flex flex-col gap-[1.1rem]">
        <div class="relative pb-3">
          <div
            class="relative z-[2] overflow-hidden select-none rounded-lg border border-transparent tad-300"
            :class="{ '!border-[#FF4E4F]': !isPassing && isClickPass }"
          >
            <FaDragVerify
              ref="dragVerifyRef"
              v-model:value="isPassing"
              :text="$t('login.sliderText')"
              :text-color="dragVerifyTextColor"
              :success-text="$t('login.sliderSuccessText')"
              progress-bar-bg="var(--el-color-primary)"
              :background="isDark ? '#26272F' : '#F1F1F4'"
              handler-bg="var(--default-box-color)"
            />
          </div>
          <p
            class="absolute top-0 z-[1] mt-2 px-px text-xs text-[#f56c6c] tad-300"
            :class="{ 'translate-y-10': !isPassing && isClickPass }"
          >
            {{ $t("login.placeholder.slider") }}
          </p>
        </div>

        <div class="login-options-row flex-cb text-sm">
          <ElCheckbox v-model="loginForm.remember" class="login-remember">
            {{ $t("login.rememberPwd") }}
          </ElCheckbox>
          <ElLink
            type="primary"
            underline="never"
            class="inline-flex items-center text-sm !leading-[inherit]"
            @click="$emit('forget')"
          >
            {{ $t("login.forgetPwd") }}
          </ElLink>
        </div>

        <div>
          <ElButton
            class="h-11 w-full !rounded-lg text-base font-medium"
            type="primary"
            :loading="loading"
            v-ripple
            @click="$emit('submit')"
          >
            {{ $t("login.btnText") }}
          </ElButton>
        </div>

        <div class="login-secondary-actions grid grid-cols-2 gap-2">
          <ElButton class="login-secondary-btn" plain @click="$emit('openMobile')">
            {{ $t("login.mobileLogin") }}
          </ElButton>
          <ElButton class="login-secondary-btn" plain @click="$emit('openQr')">
            {{ $t("login.qrLogin") }}
          </ElButton>
        </div>
      </div>
    </ElForm>

    <LoginThirdPartySection @oauth="$emit('oauth', $event)" />

    <LoginAuthLinkRow
      :hint="$t('login.noAccount')"
      :link-text="$t('login.register')"
      @link="$emit('register')"
    />
  </div>
</template>

<script setup lang="ts">
import { Loading, Lock, User } from "@element-plus/icons-vue";
import type { CaptchaInfo, LoginFormData } from "@/api/module_system/auth";
import type { FormRules } from "element-plus";
import type { Account, AccountKey } from "../types";
import LoginAuthLinkRow from "./LoginAuthLinkRow.vue";
import LoginThirdPartySection from "./LoginThirdPartySection.vue";

defineProps<{
  loginForm: LoginFormData;
  rules: FormRules;
  captchaState: CaptchaInfo;
  codeLoading: boolean;
  demoAccountKey: AccountKey;
  accounts: Account[];
  formKey: number | string;
  isDark: boolean;
  dragVerifyTextColor: string;
  loading: boolean;
}>();

const isPassing = defineModel<boolean>("isPassing", { required: true });
const isClickPass = defineModel<boolean>("isClickPass", { required: true });

defineEmits<{
  submit: [];
  setupAccount: [key: AccountKey];
  getCaptcha: [];
  openMobile: [];
  openQr: [];
  forget: [];
  register: [];
  oauth: [provider: "wechat" | "qq" | "github" | "gitee"];
}>();

const formRef = ref();
const dragVerifyRef = ref<{ reset?: () => void } | null>(null);
const isCapsLock = ref(false);

function checkCapsLock(event: KeyboardEvent) {
  if (event instanceof KeyboardEvent) {
    isCapsLock.value = event.getModifierState("CapsLock");
  }
}

defineExpose({
  validate: () => formRef.value?.validate?.(),
  clearValidate: () => formRef.value?.clearValidate?.(),
  resetDragVerify: () => dragVerifyRef.value?.reset?.(),
});
</script>

<style scoped>
@import "../style.css";
</style>
