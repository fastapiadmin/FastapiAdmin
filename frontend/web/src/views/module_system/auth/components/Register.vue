<template>
  <div>
    <h3 text-center m-0 mb-20px>{{ t("login.reg") }}</h3>
    <el-form ref="formRef" :model="model" :rules="rules" size="large" label-suffix=":">
      <!-- 账号 -->
      <el-form-item prop="username">
        <el-input v-model.trim="model.username" :placeholder="t('login.username')" clearable>
          <template #prefix>
            <el-icon><User /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <!-- 密码 -->
      <el-tooltip :visible="isCapsLock" :content="t('login.capsLock')" placement="right">
        <el-form-item prop="password">
          <el-input
            v-model.trim="model.password"
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

      <el-form-item>
        <div class="flex-y-center w-full gap-10px">
          <el-checkbox v-model="isRead">{{ t("login.agree") }}</el-checkbox>
          <el-link
            type="primary"
            underline="never"
            :href="configStore.configData.sys_web_clause.config_value"
            target="_blank"
          >
            {{ t("login.userAgreement") }}
          </el-link>
        </div>
      </el-form-item>

      <!-- 注册按钮 -->
      <el-form-item>
        <el-button :loading="loading" type="success" class="w-full" @click="submit">
          {{ t("login.register") }}
        </el-button>
      </el-form-item>
    </el-form>
    <div flex-center gap-10px>
      <el-text size="default">{{ t("login.haveAccount") }}</el-text>
      <el-link type="primary" underline="never" @click="toLogin">{{ t("login.login") }}</el-link>
    </div>
  </div>
</template>
<script setup lang="ts">
import type { FormInstance } from "element-plus";
import { Lock } from "@element-plus/icons-vue";
import UserAPI, { type RegisterForm } from "@/api/module_system/user";
import { useConfigStore } from "@/store";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

// 使用 defineModel 简化具名 v-model 绑定
const modelValue = defineModel<string>();
const presetUsername = defineModel<string>("presetUsername");
const presetPassword = defineModel<string>("presetPassword");
const toLogin = () => {
  modelValue.value = "login";
};

const configStore = useConfigStore();

const formRef = ref<FormInstance>();
const loading = ref(false); // 按钮 loading 状态
const isCapsLock = ref(false); // 是否大写锁定
const isRead = ref(false);

const model = ref<RegisterForm>({
  username: "",
  password: "",
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
          return value === model.value.password;
        },
        trigger: "blur",
        message: t("login.message.password.inconformity"),
      },
    ],
  };
});

// 检查输入大小写
function checkCapsLock(event: KeyboardEvent) {
  // 防止浏览器密码自动填充时报错
  if (event instanceof KeyboardEvent) {
    isCapsLock.value = event.getModifierState("CapsLock");
  }
}

const submit = async () => {
  try {
    // 0. 检查是否已勾选协议
    if (!isRead.value) {
      ElMessage.warning(t("login.message.agree.required"));
      return;
    }
    // 1. 表单验证
    const valid = await formRef.value?.validate();
    if (!valid) return;

    loading.value = true;

    await UserAPI.registerUser(model.value);
    // 注册成功后，双向绑定回写父容器的用户名和密码，并切回登录
    presetUsername.value = model.value.username;
    presetPassword.value = model.value.password;
    toLogin();
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {});
</script>
