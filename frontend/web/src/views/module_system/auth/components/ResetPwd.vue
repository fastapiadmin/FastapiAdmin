<template>
  <div>
    <h3 text-center m-0 mb-20px>{{ t("login.resetPassword") }}</h3>
    <el-form ref="formRef" :model="model" :rules="rules" size="large" label-suffix=":">
      <!-- 用户名 -->
      <el-form-item prop="username">
        <el-input v-model.trim="model.username" :placeholder="t('login.username')" clearable>
          <template #prefix>
            <el-icon><User /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <!-- 新密码 -->
      <el-tooltip :visible="isCapsLock" :content="t('login.capsLock')" placement="right">
        <el-form-item prop="new_password">
          <el-input
            v-model.trim="model.new_password"
            :placeholder="t('login.password')"
            type="password"
            show-password
            clearable
            @keyup="checkCapsLock"
            @keyup.enter="submit"
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
      </el-tooltip>

      <!-- 确认密码 -->
      <el-tooltip :visible="isCapsLock" :content="t('login.capsLock')" placement="right">
        <el-form-item prop="confirmPassword">
          <el-input
            v-model.trim="model.confirmPassword"
            :placeholder="t('login.message.password.confirm')"
            type="password"
            show-password
            clearable
            @keyup="checkCapsLock"
            @keyup.enter="submit"
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
      </el-tooltip>

      <!-- 重置密码按钮 -->
      <el-form-item>
        <el-button type="warning" class="w-full" @click="submit">
          {{ t("login.resetPassword") }}
        </el-button>
      </el-form-item>
    </el-form>

    <div flex-center gap-10px>
      <el-text size="default">{{ t("login.thinkOfPasswd") }}</el-text>
      <el-link type="primary" underline="never" @click="toLogin">{{ t("login.login") }}</el-link>
    </div>
  </div>
</template>
<script setup lang="ts">
import { useI18n } from "vue-i18n";
import type { FormInstance } from "element-plus";
import UserAPI, { type ForgetPasswordForm } from "@/api/module_system/user";

const loading = ref(false); // 按钮 loading 状态
const isCapsLock = ref(false); // 是否大写锁定

const { t } = useI18n();

// 使用 defineModel 简化具名 v-model 绑定
const modelValue = defineModel<string>();
const presetUsername = defineModel<string>("presetUsername");
const presetPassword = defineModel<string>("presetPassword");
const toLogin = () => {
  modelValue.value = "login";
};

const model = ref<ForgetPasswordForm>({
  username: "",
  new_password: "",
  confirmPassword: "",
});

const rules = computed(() => {
  return {
    username: [
      {
        required: true,
        trigger: "blur",
        message: t("login.message.username.required"),
      },
    ],
    new_password: [
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
    confirmPassword: [
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
      {
        validator: (_: any, value: string) => {
          return value === model.value.new_password;
        },
        trigger: "blur",
        message: t("login.message.password.inconformity"),
      },
    ],
    mobile: [
      {
        required: true,
        trigger: "blur",
        message: t("login.message.captchaCode.required"),
      },
    ],
  };
});

const formRef = ref<FormInstance>();

const submit = async () => {
  try {
    // 1. 表单验证
    const valid = await formRef.value?.validate();
    if (!valid) return;

    loading.value = true;

    await UserAPI.forgetPassword(model.value);
    // 重置成功后，双向绑定回写父容器的用户名和新密码，并切回登录
    presetUsername.value = model.value.username;
    presetPassword.value = model.value.new_password;
    toLogin();
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

// 检查输入大小写
function checkCapsLock(event: KeyboardEvent) {
  // 防止浏览器密码自动填充时报错
  if (event instanceof KeyboardEvent) {
    isCapsLock.value = event.getModifierState("CapsLock");
  }
}
</script>
