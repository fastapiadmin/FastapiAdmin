<template>
  <div>
    <h3 text-center m-0 mb-20px>{{ t("login.login") }}</h3>

    <el-form
      ref="loginFormRef"
      :model="loginForm"
      :rules="loginRules"
      size="large"
      :validate-on-rule-change="false"
    >
      <!-- 用户名 -->
      <el-form-item prop="username">
        <el-input v-model.trim="loginForm.username" :placeholder="t('login.username')" clearable>
          <template #prefix>
            <el-icon><User /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <!-- 密码 -->
      <el-tooltip :visible="isCapsLock" :content="t('login.capsLock')" placement="right">
        <el-form-item prop="password">
          <el-input
            v-model.trim="loginForm.password"
            :placeholder="t('login.password')"
            type="password"
            show-password
            clearable
            @keyup="checkCapsLock"
            @keyup.enter="handleLoginSubmit"
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
      </el-tooltip>

      <!-- 验证码 -->
      <el-form-item v-if="captchaState.enable" prop="captcha">
        <div flex items-center gap-10px class="flex-1">
          <el-input
            v-model.trim="loginForm.captcha"
            :placeholder="t('login.captchaCode')"
            clearable
            class="flex-1"
            @keyup.enter="handleLoginSubmit"
          >
            <template #prefix>
              <div class="i-svg:captcha" />
            </template>
          </el-input>
          <div cursor-pointer flex-center h-40px w-100px>
            <el-icon v-if="codeLoading" class="is-loading" size="20">
              <Loading />
            </el-icon>
            <el-image
              v-else-if="captchaState.img_base"
              border-rd-4px
              object-cover
              shadow="[0_0_0_1px_var(--el-border-color)_inset]"
              :src="captchaState.img_base"
              class="w-full h-full"
              @click="getCaptcha"
            />
            <el-text v-else type="info" size="small">点击获取验证码</el-text>
          </div>
        </div>
      </el-form-item>

      <div class="flex-x-between w-full">
        <el-checkbox v-model="loginForm.remember">{{ t("login.rememberMe") }}</el-checkbox>
        <el-link type="primary" underline="never" @click="toOtherForm('resetPwd')">
          {{ t("login.forgetPassword") }}
        </el-link>
      </div>

      <!-- 登录按钮 -->
      <el-form-item>
        <el-button :loading="loading" type="primary" class="w-full" @click="handleLoginSubmit">
          {{ t("login.login") }}
        </el-button>
      </el-form-item>
    </el-form>

    <div flex-center gap-10px>
      <el-text size="default">{{ t("login.noAccount") }}</el-text>
      <el-link type="primary" underline="never" @click="toOtherForm('register')">
        {{ t("login.reg") }}
      </el-link>
    </div>
  </div>
</template>
<script setup lang="ts">
import type { FormInstance } from "element-plus";
import { LocationQuery, RouteLocationRaw, useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { onActivated, watch } from "vue";
import AuthAPI, { type LoginFormData, type CaptchaInfo } from "@/api/module_system/auth";
import { useAppStore, useUserStore, useSettingsStore } from "@/store";
import { User, Loading, Lock } from "@element-plus/icons-vue";
import { Auth } from "@/utils/auth";

const { t } = useI18n();
const userStore = useUserStore();
const appStore = useAppStore();
const settingsStore = useSettingsStore();

// 来自父容器的预填用户名和密码
const props = defineProps<{ presetUsername?: string; presetPassword?: string }>();

const route = useRoute();
const router = useRouter();

onActivated(() => {
  getCaptcha();
  loginForm.captcha = "";
});

watch(
  () => route.fullPath,
  () => {
    getCaptcha();
    loginForm.captcha = "";
  }
);

const loginFormRef = ref<FormInstance>();
const loading = ref(false);
const isCapsLock = ref(false);

const loginForm = reactive<LoginFormData>({
  username: "",
  password: "",
  captcha: "",
  captcha_key: "",
  remember: true,
  login_type: "PC端",
});

watch(
  () => [props.presetUsername, props.presetPassword],
  ([presetUsername, presetPassword]) => {
    if (typeof presetUsername === "string") {
      loginForm.username = presetUsername;
    }
    if (typeof presetPassword === "string") {
      loginForm.password = presetPassword;
    }
  },
  { immediate: true }
);

const captchaState = reactive<CaptchaInfo>({
  enable: true,
  key: "",
  img_base: "",
});

const loginRules = computed(() => {
  const rules: any = {
    username: [
      {
        required: true,
        trigger: "blur",
        message: t("login.message.username.required"),
      },
    ],
    password: [
      {
        required: true,
        trigger: "blur",
        message: t("login.message.password.required"),
      },
      {
        min: 6,
        message: t("login.message.password.min"),
        trigger: "blur",
      },
    ],
  };

  if (captchaState.enable) {
    rules.captcha = [
      {
        required: true,
        trigger: "blur",
        message: t("login.message.captchaCode.required"),
      },
    ];
  }

  return rules;
});

const codeLoading = ref(false);
async function getCaptcha() {
  try {
    codeLoading.value = true;
    const response = await AuthAPI.getCaptcha();
    loginForm.captcha_key = response.data.data.key;
    captchaState.img_base = response.data.data.img_base;
    captchaState.enable = response.data.data.enable;
  } catch (error: any) {
    console.error("获取验证码失败:", error);
    captchaState.enable = false;
    loginForm.captcha = "";
    loginForm.captcha_key = "";
  } finally {
    codeLoading.value = false;
  }
}

getCaptcha();

async function handleLoginSubmit() {
  try {
    const valid = await loginFormRef.value?.validate();
    if (!valid) return;

    loading.value = true;
    await userStore.login(loginForm);

    const redirect = resolveRedirectTarget(route.query);
    await router.replace(redirect);

    if (settingsStore.showGuide) {
      appStore.showGuide(true);
    }
  } catch (error: any) {
    if (error) {
      getCaptcha();
    }
  } finally {
    loading.value = false;
  }
}

function resolveRedirectTarget(query: LocationQuery): RouteLocationRaw {
  const defaultPath = "/";
  const rawRedirect = (query.redirect as string) || defaultPath;

  try {
    const resolved = router.resolve(rawRedirect);
    return {
      path: resolved.path,
      query: resolved.query,
    };
  } catch {
    return { path: defaultPath };
  }
}

function checkCapsLock(event: KeyboardEvent) {
  if (event instanceof KeyboardEvent) {
    isCapsLock.value = event.getModifierState("CapsLock");
  }
}

const emit = defineEmits(["update:modelValue"]);
function toOtherForm(type: "register" | "resetPwd") {
  emit("update:modelValue", type);
}
</script>
