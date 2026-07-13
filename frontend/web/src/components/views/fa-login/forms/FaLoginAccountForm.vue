<!-- 账号密码登录表单（含快捷账号） -->
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
      <ElFormItem v-if="SHOW_SAAS_AUTH">
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
            @keyup="onPasswordKeyup"
          >
            <template #prefix>
              <ElIcon><Lock /></ElIcon>
            </template>
          </ElInput>
        </ElFormItem>
      </ElTooltip>

      <div class="login-form-tail flex flex-col gap-[1.1rem]">
        <div class="login-options-row flex items-center justify-between text-sm">
          <ElCheckbox v-model="loginForm.remember" class="login-remember">
            {{ $t("login.rememberPwd") }}
          </ElCheckbox>
          <ElLink
            type="primary"
            underline="never"
            class="inline-flex items-center text-sm leading-[inherit]!"
            @click="$emit('forget')"
          >
            {{ $t("login.forgetPwd") }}
          </ElLink>
        </div>

        <div>
          <ElButton
            class="h-11 w-full rounded-lg! text-base font-medium"
            type="primary"
            :loading="loading"
            v-ripple
            @click="$emit('submit')"
          >
            {{ $t("login.btnText") }}
          </ElButton>
        </div>

        <div class="login-feishu-entry mt-2">
          <ElButton
            class="login-feishu-btn w-full"
            plain
            @click="$emit('oauth', 'feishu')"
          >
            <FaSvgIcon icon="simple-icons:feishu" class="mr-1 size-[16px] text-[#00d6b9]" />
            {{ $t("login.oauthTooltip.feishu") }}
          </ElButton>
        </div>

        <div v-if="SHOW_SAAS_AUTH" class="login-secondary-actions grid grid-cols-2 gap-2">
          <ElButton class="login-secondary-btn" plain @click="$emit('openMobile')">
            {{ $t("login.mobileLogin") }}
          </ElButton>
          <ElButton class="login-secondary-btn" plain @click="$emit('openQr')">
            {{ $t("login.qrLogin") }}
          </ElButton>
        </div>
      </div>
    </ElForm>

    <FaLoginThirdPartySection v-if="SHOW_SAAS_AUTH" @oauth="$emit('oauth', $event)" />

    <FaLoginAuthLinkRow
      v-if="SHOW_SAAS_AUTH"
      :hint="$t('login.noAccount')"
      :link-text="$t('login.register')"
      @link="$emit('register')"
    />
  </div>
</template>

<script setup lang="ts">
import { Lock, User } from "@element-plus/icons-vue";
import type { LoginFormData } from "@/api/module_system/auth";
import type { FormRules } from "element-plus";
import type { Account, AccountKey } from "@views/module_system/auth/login/types";

const loginForm = defineModel<LoginFormData>("loginForm", { required: true });

defineOptions({ name: "FaLoginAccountForm" });

interface Props {
  rules: FormRules;
  demoAccountKey: AccountKey;
  accounts: Account[];
  formKey: number | string;
  loading: boolean;
}

withDefaults(defineProps<Props>(), {});

interface Emits {
  submit: [];
  setupAccount: [key: AccountKey];
  openMobile: [];
  openQr: [];
  forget: [];
  register: [];
  oauth: [provider: "wechat" | "qq" | "github" | "gitee" | "feishu"];
}

const emit = defineEmits<Emits>();

/** 内部控制面：隐藏注册/第三方/手机扫码/演示账号等 SaaS 登录入口，仅留账号密码 */
const SHOW_SAAS_AUTH = false;

const formRef = ref();
const isCapsLock = ref(false);

function onPasswordKeyup(event: KeyboardEvent) {
  if (event instanceof KeyboardEvent) {
    isCapsLock.value = event.getModifierState("CapsLock");
    if (event.key === "Enter") {
      emit("submit");
    }
  }
}

defineExpose({
  validate: () => formRef.value?.validate?.(),
  clearValidate: () => formRef.value?.clearValidate?.(),
});
</script>

<style scoped lang="scss">
@use "../fa-login";
</style>
