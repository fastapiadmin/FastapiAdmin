<!-- 手机号登录（无后端接口，演示交互） -->
<template>
  <div>
    <div class="login-page-form login-mobile-flow">
      <div class="mb-[1.1rem]">
        <ElInput
          v-model.trim="mobileForm.phone"
          class="custom-height"
          maxlength="11"
          inputmode="numeric"
          clearable
          :placeholder="$t('login.mobilePhonePlaceholder')"
          @keyup.enter="submitMobileLogin"
        >
          <template #prefix>
            <ElIcon><Iphone /></ElIcon>
          </template>
        </ElInput>
      </div>

      <div class="login-mobile-code-row mb-[1.1rem] flex items-stretch gap-2 sm:gap-3">
        <div class="flex min-w-0 flex-1">
          <ElInputOtp
            v-model="otpCode"
            class="w-full"
            :length="6"
            size="large"
            inputmode="numeric"
            autofocus
            @finish="onOtpFilled"
          />
        </div>
        <ElButton
          class="login-mobile-sms-btn h-10 shrink-0 px-3 sm:px-4"
          plain
          :disabled="smsCountdown > 0"
          @click="sendSmsCodeMock"
        >
          {{ smsCountdown > 0 ? `${smsCountdown}s` : $t("login.getSmsCode") }}
        </ElButton>
      </div>

      <div class="login-mobile-actions flex w-full min-w-0 flex-col items-stretch gap-3">
        <ElButton
          type="primary"
          class="h-11 w-full min-w-0 rounded-lg! text-base font-medium"
          v-ripple
          @click="submitMobileLogin"
        >
          {{ $t("login.btnText") }}
        </ElButton>
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
import { Iphone } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

defineOptions({ name: "FaLoginMobilePanel" });

interface Emits {
  back: [];
  register: [];
}

defineEmits<Emits>();

const { t } = useI18n();

const mobileForm = reactive({
  phone: "",
});

const otpCode = ref("");

const smsCountdown = ref(0);
let smsTimerId: number | null = null;

function clearSmsTimer() {
  if (smsTimerId != null) {
    clearInterval(smsTimerId);
    smsTimerId = null;
  }
}

function resetMobileLoginUi() {
  mobileForm.phone = "";
  otpCode.value = "";
  smsCountdown.value = 0;
  clearSmsTimer();
}

defineExpose({ resetMobileLoginUi });

function sendSmsCodeMock() {
  const phone = mobileForm.phone.trim();
  if (!/^1\d{10}$/.test(phone)) {
    ElMessage.warning(t("login.message.mobile.invalid"));
    return;
  }
  if (smsCountdown.value > 0) return;
  ElMessage.success(t("login.smsCodeSentMock"));
  smsCountdown.value = 60;
  clearSmsTimer();
  smsTimerId = window.setInterval(() => {
    smsCountdown.value--;
    if (smsCountdown.value <= 0) {
      clearSmsTimer();
    }
  }, 1000);
}

function onOtpFilled(value: string) {
  otpCode.value = value;
}

function submitMobileLogin() {
  const phone = mobileForm.phone.trim();
  if (!/^1\d{10}$/.test(phone)) {
    ElMessage.warning(t("login.message.mobile.invalid"));
    return;
  }
  if (otpCode.value.length !== 6) {
    ElMessage.warning(t("login.smsCodeRequired"));
    return;
  }
  ElMessage.info(t("login.mobileLoginPending"));
}

onBeforeUnmount(() => {
  clearSmsTimer();
});
</script>
