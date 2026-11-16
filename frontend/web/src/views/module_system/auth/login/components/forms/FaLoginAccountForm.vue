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
          class="custom-height w-full"
          popper-class="login-account-dropdown"
          :placeholder="$t('login.quickSelectAccount')"
          :aria-label="$t('login.quickSelectAccount')"
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
          :aria-label="$t('login.placeholder.username')"
        >
          <template #prefix>
            <ElIcon><FaSvgIcon icon="ri:user-3-line" /></ElIcon>
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
            :aria-label="$t('login.placeholder.password')"
          >
            <template #prefix>
              <ElIcon><FaSvgIcon icon="ri:lock-2-line" /></ElIcon>
            </template>
          </ElInput>
        </ElFormItem>
      </ElTooltip>

      <div class="login-form-tail flex flex-col gap-[1.1rem]">
        <div class="relative pb-3">
          <div
            class="relative z-2 overflow-hidden select-none rounded-lg border border-transparent transition duration-300"
            :class="{ 'border-(--el-color-danger)!': !isPassing && isClickPass }"
          >
            <FaPuzzleCaptcha
              ref="puzzleRef"
              :bg-image="captchaState.img_base"
              :piece-image="captchaState.piece_base"
              :piece-y="captchaState.piece_y"
              :piece-width="captchaState.piece_width"
              :piece-height="captchaState.piece_height"
              :bg-width="captchaState.bg_width"
              :bg-height="captchaState.bg_height"
              :passed="isPassing"
              :loading="codeLoading"
              :text="$t('login.puzzleText')"
              :title-text="$t('login.puzzleTitle')"
              :success-text="$t('login.sliderSuccessText')"
              :close-text="$t('common.closeAction')"
              :entry-text="$t('login.puzzleEntry')"
              @verify="(pos) => emit('sliderPass', pos)"
              @request="emit('requestPuzzle')"
              @refresh="emit('getCaptcha')"
            />
          </div>
          <p
            class="absolute top-0 z-1 mt-2 px-px text-xs text-(--el-color-danger) transition duration-300"
            :class="{ 'opacity-0': !isClickPass, 'translate-y-10': !isPassing && isClickPass }"
          >
            {{ $t("login.placeholder.slider") }}
          </p>
        </div>

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

    <FaLoginThirdPartySection @oauth="$emit('oauth', $event)" />

    <FaLoginAuthLinkRow
      :hint="$t('login.noAccount')"
      :link-text="$t('login.register')"
      @link="$emit('register')"
    />
  </div>
</template>

<script setup lang="ts">
import type { CaptchaInfo, LoginFormData } from "@/api/module_system/auth";
import type { FormRules } from "element-plus";
import type { Account, AccountKey } from "@views/module_system/auth/login/types";

const loginForm = defineModel<LoginFormData>("loginForm", { required: true });

defineOptions({ name: "FaLoginAccountForm" });

interface Props {
  rules: FormRules;
  captchaState: CaptchaInfo;
  codeLoading: boolean;
  demoAccountKey: AccountKey;
  accounts: Account[];
  formKey: number | string;
  isDark: boolean;
  dragVerifyTextColor: string;
  loading: boolean;
}

withDefaults(defineProps<Props>(), {});

const isPassing = defineModel<boolean>("isPassing", { required: true });
const isClickPass = defineModel<boolean>("isClickPass", { required: true });

interface Emits {
  submit: [];
  setupAccount: [key: AccountKey];
  getCaptcha: [];
  openMobile: [];
  openQr: [];
  forget: [];
  register: [];
  oauth: [provider: "wechat" | "qq" | "github" | "gitee"];
  sliderPass: [position: number];
  requestPuzzle: [];
}

const emit = defineEmits<Emits>();

const formRef = ref();
const puzzleRef = ref<{ reset?: () => void; open?: () => void } | null>(null);
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
  resetDragVerify: () => puzzleRef.value?.reset?.(),
  openPuzzle: () => puzzleRef.value?.open?.(),
});
</script>
