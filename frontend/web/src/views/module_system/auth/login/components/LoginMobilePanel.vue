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
        <div
          ref="otpWrapRef"
          class="flex min-w-0 flex-1 gap-1.5 sm:gap-2"
          @paste.prevent="onOtpPaste"
        >
          <input
            v-for="idx in otpIndices"
            :key="idx"
            :value="otpDigits[idx]"
            type="text"
            inputmode="numeric"
            autocomplete="one-time-code"
            maxlength="1"
            class="login-mobile-otp-cell"
            @input="onOtpCellInput(idx, $event)"
            @keydown="onOtpCellKeydown(idx, $event)"
          />
        </div>
        <ElButton
          class="login-mobile-sms-btn h-10 shrink-0 self-center px-3 sm:px-4"
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
          class="h-11 w-full min-w-0 !rounded-lg text-base font-medium"
          v-ripple
          @click="submitMobileLogin"
        >
          {{ $t("login.btnText") }}
        </ElButton>
        <ElButton
          class="login-secondary-btn h-11 w-full min-w-0 !rounded-lg text-base font-medium"
          plain
          @click="$emit('back')"
        >
          {{ $t("login.backToAccountLogin") }}
        </ElButton>
      </div>
    </div>

    <LoginAuthLinkRow
      :hint="$t('login.noAccount')"
      :link-text="$t('login.register')"
      @link="$emit('register')"
    />
  </div>
</template>

<script setup lang="ts">
import { Iphone } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import LoginAuthLinkRow from "./LoginAuthLinkRow.vue";

defineEmits<{ back: []; register: [] }>();

const { t } = useI18n();

const mobileForm = reactive({
  phone: "",
});

const otpDigits = ref<string[]>(Array.from({ length: 6 }, () => ""));
const otpIndices = [0, 1, 2, 3, 4, 5];
const otpWrapRef = ref<HTMLElement | null>(null);
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
  otpDigits.value = Array.from({ length: 6 }, () => "");
  smsCountdown.value = 0;
  clearSmsTimer();
}

defineExpose({ resetMobileLoginUi });

function focusOtpCell(index: number) {
  nextTick(() => {
    const root = otpWrapRef.value;
    if (!root) return;
    const inputs = root.querySelectorAll<HTMLInputElement>(".login-mobile-otp-cell");
    inputs[index]?.focus();
  });
}

function onOtpCellInput(index: number, event: Event) {
  const target = event.target as HTMLInputElement;
  const digit = target.value.replace(/\D/g, "").slice(-1);
  otpDigits.value[index] = digit;
  target.value = digit;
  if (digit && index < 5) {
    focusOtpCell(index + 1);
  }
}

function onOtpCellKeydown(index: number, event: KeyboardEvent) {
  if (event.key === "Backspace" && !otpDigits.value[index] && index > 0) {
    event.preventDefault();
    otpDigits.value[index - 1] = "";
    focusOtpCell(index - 1);
    const root = otpWrapRef.value;
    const inputs = root?.querySelectorAll<HTMLInputElement>(".login-mobile-otp-cell");
    const prev = inputs?.[index - 1];
    if (prev) prev.value = "";
  }
}

function onOtpPaste(event: ClipboardEvent) {
  const text = event.clipboardData?.getData("text")?.replace(/\D/g, "").slice(0, 6) ?? "";
  if (!text) return;
  event.preventDefault();
  for (let i = 0; i < 6; i++) {
    otpDigits.value[i] = text[i] ?? "";
  }
  nextTick(() => {
    const root = otpWrapRef.value;
    if (!root) return;
    const inputs = root.querySelectorAll<HTMLInputElement>(".login-mobile-otp-cell");
    inputs.forEach((el, i) => {
      el.value = otpDigits.value[i] ?? "";
    });
    const nextIdx = Math.min(text.length, 5);
    focusOtpCell(nextIdx);
  });
}

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

function submitMobileLogin() {
  const phone = mobileForm.phone.trim();
  if (!/^1\d{10}$/.test(phone)) {
    ElMessage.warning(t("login.message.mobile.invalid"));
    return;
  }
  const code = otpDigits.value.join("");
  if (code.length !== 6) {
    ElMessage.warning(t("login.smsCodeRequired"));
    return;
  }
  ElMessage.info(t("login.mobileLoginPending"));
}

onBeforeUnmount(() => {
  clearSmsTimer();
});
</script>

<style scoped lang="scss">
@import "../style.css";

.login-mobile-flow {
  margin-top: 1rem;
}

.login-mobile-otp-cell {
  box-sizing: border-box;
  flex: 1;
  min-width: 0;
  max-width: 48px;
  height: 40px;
  padding: 0;
  font-size: 1rem;
  font-weight: 500;
  color: var(--el-text-color-primary);
  text-align: center;
  appearance: none;
  outline: none;
  background: var(--el-fill-color-blank);
  border: 1px solid var(--el-border-color);
  border-radius: 8px;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;

  &:focus {
    border-color: var(--el-color-primary);
    box-shadow: 0 0 0 1px var(--el-color-primary) inset;
  }
}

.login-mobile-sms-btn {
  border-radius: 8px;
}

html.dark {
  .login-mobile-otp-cell {
    background: rgb(255 255 255 / 6%);
    border-color: rgb(255 255 255 / 14%);

    &:focus {
      border-color: var(--el-color-primary);
    }
  }
}

/* EP 全局规则：相邻 .el-button { margin-left: 12px }，纵向叠放时仍会命中，导致第二颗按钮横向错位 */
.login-mobile-actions {
  ::v-deep(.el-button + .el-button) {
    margin-left: 0 !important;
  }

  ::v-deep(.el-button) {
    box-sizing: border-box;
    width: 100%;
    min-width: 0;
    max-width: 100%;
  }
}
</style>
