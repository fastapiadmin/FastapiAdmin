<template>
  <div>
    <h3 text-center m-0 mb-20px>{{ t("login.login") }}</h3>

    <el-tabs v-model="activeTab" class="login-tabs">
      <!-- 账号登录 -->
      <el-tab-pane label="账号登录" name="password">
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          size="large"
          :validate-on-rule-change="false"
        >
          <!-- 用户名 -->
          <el-form-item prop="username">
            <el-input
              v-model.trim="loginForm.username"
              :placeholder="t('login.username')"
              clearable
            >
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
      </el-tab-pane>

      <!-- 快速登录 -->
      <el-tab-pane v-if="autoLoginUsers.length > 0" label="快速登录" name="quick">
        <div class="quick-login-section">
          <div class="quick-login-tip">
            <el-text type="info">{{ t("login.quickLoginTip") }}</el-text>
          </div>
          <!-- 当用户数量大于4个时使用下拉选择，否则使用网格展示 -->
          <template v-if="autoLoginUsers.length > 3">
            <el-select
              v-model="selectedUserId"
              class="w-full"
              :placeholder="t('login.selectUser')"
              size="large"
              @change="handleAutoLogin"
            >
              <el-option
                v-for="user in autoLoginUsers"
                :key="user.id"
                :label="`${user.username}@${user.name}`"
                :value="user.id"
              />
            </el-select>
          </template>
          <template v-else>
            <div class="auto-login-users">
              <div
                v-for="user in autoLoginUsers"
                :key="user.id"
                class="auto-login-user-item"
                @click="handleAutoLogin(user.id)"
              >
                <el-avatar :size="60" :src="user.avatar || ''" class="user-avatar">
                  <el-icon size="24"><User /></el-icon>
                </el-avatar>
                <span class="user-name">{{ user.name }}</span>
                <span class="user-username">{{ user.username }}</span>
              </div>
            </div>
          </template>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 第三方登录 -->
    <div class="third-party-login">
      <div class="divider-container">
        <div class="divider-line"></div>
        <span class="divider-text">{{ t("login.otherLoginMethods") }}</span>
        <div class="divider-line"></div>
      </div>
      <div class="flex-center gap-x-5 w-full text-[var(--el-text-color-secondary)]">
        <CommonWrapper>
          <div text-20px class="i-svg:wechat" />
        </CommonWrapper>
        <CommonWrapper>
          <div text-20px cursor-pointer class="i-svg:qq" />
        </CommonWrapper>
        <CommonWrapper>
          <div text-20px cursor-pointer class="i-svg:github" />
        </CommonWrapper>
        <CommonWrapper>
          <div text-20px cursor-pointer class="i-svg:gitee" />
        </CommonWrapper>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import type { FormInstance } from "element-plus";
import { LocationQuery, RouteLocationRaw, useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { onActivated, onMounted, watch } from "vue";
import AuthAPI, {
  type AutoLoginUser,
  type LoginFormData,
  type CaptchaInfo,
} from "@/api/module_system/auth";
import { useAppStore, useUserStore, useSettingsStore } from "@/store";
import CommonWrapper from "@/components/CommonWrapper/index.vue";
import { User, Loading, Lock } from "@element-plus/icons-vue";
import { Auth } from "@/utils/auth";

const { t } = useI18n();
const userStore = useUserStore();
const appStore = useAppStore();
const settingsStore = useSettingsStore();

// 激活的标签页
const activeTab = ref("password");

// 选择的用户ID（用于下拉选择）
const selectedUserId = ref<number | null>(null);

// 来自父容器的预填用户名和密码
const props = defineProps<{ presetUsername?: string; presetPassword?: string }>();

const route = useRoute();
const router = useRouter();

// 组件挂载时获取验证码和免登录用户列表
onMounted(() => {
  getCaptcha();
  getAutoLoginUsers();
});

// 组件激活时获取验证码（适用于KeepAlive缓存的情况）
onActivated(() => {
  getCaptcha();
  // 重置登录表单
  loginForm.captcha = "";
});

// 监听路由变化，确保每次进入登录页面都有最新验证码
watch(
  () => route.fullPath,
  () => {
    getCaptcha();
    loginForm.captcha = "";
  }
);

const loginFormRef = ref<FormInstance>();
const loading = ref(false);
// 是否大写锁定
const isCapsLock = ref(false);

const loginForm = reactive<LoginFormData>({
  username: "",
  password: "",
  captcha: "",
  captcha_key: "",
  remember: true,
  login_type: "PC端",
});

// 监听父组件传入的预填信息，立即填充到登录表单
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

// 免登录用户列表
const autoLoginUsers = ref<AutoLoginUser[]>([]);
const autoLoginLoading = ref(false);

// 获取免登录用户列表
async function getAutoLoginUsers() {
  try {
    const response = await AuthAPI.getAutoLoginUsers();
    autoLoginUsers.value = response.data.data || [];
  } catch (error) {
    console.error("获取免登录用户列表失败:", error);
  }
}

// 免登录
async function handleAutoLogin(userId: number) {
  if (autoLoginLoading.value) return;

  try {
    autoLoginLoading.value = true;

    // 1. 获取免登录Token
    const tokenResponse = await AuthAPI.getAutoLoginToken(userId);
    const { token } = tokenResponse.data.data;

    // 2. 使用Token登录
    const loginResponse = await AuthAPI.autoLogin(token);
    const loginData = loginResponse.data.data;

    // 3. 设置登录状态
    userStore.rememberMe = true;
    Auth.setTokens(loginData.access_token, loginData.refresh_token, true);

    // 4. 获取用户信息
    await userStore.getUserInfo();

    // 5. 跳转
    const redirect = resolveRedirectTarget(route.query);
    await router.replace(redirect);

    // 6. 显示引导
    if (settingsStore.showGuide) {
      appStore.showGuide(true);
    }

    ElMessage.success("登录成功");
  } catch (error: any) {
    console.error("免登录失败:", error);
    ElMessage.error(error?.response?.data?.msg || "登录失败");
  } finally {
    autoLoginLoading.value = false;
  }
}

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

  // 只有在验证码开启时才添加验证码验证规则
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

// 获取验证码
const codeLoading = ref(false);
async function getCaptcha() {
  try {
    codeLoading.value = true;
    const response = await AuthAPI.getCaptcha();
    loginForm.captcha_key = response.data.data.key;
    captchaState.img_base = response.data.data.img_base;
    captchaState.enable = response.data.data.enable;
  } catch (error: any) {
    // 验证码获取失败时，默认关闭验证码功能
    console.error("获取验证码失败:", error);
    captchaState.enable = false;
    // 清空验证码相关字段，避免影响登录
    loginForm.captcha = "";
    loginForm.captcha_key = "";
  } finally {
    codeLoading.value = false;
  }
}

/**
 * 登录提交
 */
async function handleLoginSubmit() {
  try {
    // 1. 表单验证
    const valid = await loginFormRef.value?.validate();
    if (!valid) return;

    loading.value = true;

    // 2. 执行登录
    await userStore.login(loginForm);

    // 4. 登录成功，让路由守卫处理跳转逻辑
    // 解析目标地址，但不直接跳转
    const redirect = resolveRedirectTarget(route.query);

    // 通过替换当前路由触发路由守卫，让守卫处理后续的路由生成和跳转
    await router.replace(redirect);

    // 5. 记住我功能已实现，根据用户选择决定token的存储方式:
    // - 选中"记住我": token存储在localStorage中，浏览器关闭后仍然有效
    // - 未选中"记住我": token存储在sessionStorage中，浏览器关闭后失效

    // 登录成功后自动开启项目引导
    if (settingsStore.showGuide) {
      appStore.showGuide(true);
    }
  } catch (error: any) {
    if (error) {
      getCaptcha(); // 刷新验证码
    }
  } finally {
    loading.value = false;
  }
}

/**
 * 解析重定向目标
 *
 * @param query 路由查询参数
 * @returns 标准化后的路由地址
 */
function resolveRedirectTarget(query: LocationQuery): RouteLocationRaw {
  // 默认跳转路径
  const defaultPath = "/";

  // 获取原始重定向路径
  const rawRedirect = (query.redirect as string) || defaultPath;

  try {
    // 6. 使用Vue Router解析路径
    const resolved = router.resolve(rawRedirect);
    return {
      path: resolved.path,
      query: resolved.query,
    };
  } catch {
    // 7. 异常处理：返回安全路径
    return { path: defaultPath };
  }
}

// 检查输入大小写
function checkCapsLock(event: KeyboardEvent) {
  // 防止浏览器密码自动填充时报错
  if (event instanceof KeyboardEvent) {
    isCapsLock.value = event.getModifierState("CapsLock");
  }
}

const emit = defineEmits(["update:modelValue"]);
function toOtherForm(type: "register" | "resetPwd") {
  emit("update:modelValue", type);
}
</script>

<style lang="scss" scoped>
.login-tabs {
  margin-bottom: 20px;

  :deep(.el-tabs__content) {
    min-height: 300px;
    overflow: visible;
  }

  :deep(.el-tab-pane) {
    position: relative;
    overflow: visible;
  }
}

.quick-login-section {
  position: relative;
  min-height: 200px;
  padding: 20px 0;

  .quick-login-tip {
    margin-bottom: 20px;
    font-size: 14px;
    text-align: center;
  }

  // 下拉菜单样式
  .user-dropdown {
    .user-dropdown-btn {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      height: 48px;
      padding: 0 16px;

      .btn-text {
        font-size: 14px;
        color: var(--el-text-color-regular);
      }
    }
  }

  :deep(.user-dropdown-menu) {
    max-height: 320px;
    overflow-y: auto;

    .el-dropdown-menu__item {
      display: flex !important;
      gap: 20px !important;
      align-items: center !important;
      padding: 14px 24px !important;
    }
  }

  .user-option {
    display: flex;
    gap: 16px;
    align-items: center;
    padding: 10px 0;

    .user-info {
      display: flex;
      flex: 1;
      flex-direction: column;
      gap: 4px;
      min-width: 0;

      .user-option-name {
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 14px;
        font-weight: 600;
        white-space: nowrap;
      }

      .user-option-username {
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 12px;
        font-weight: 500;
        white-space: nowrap;
      }
    }
  }

  .user-option-avatar {
    flex-shrink: 0;
    border: 2px solid var(--el-border-color-light);
    transition: all 0.3s ease;

    &:hover {
      border-color: var(--el-color-primary);
    }
  }

  .auto-login-users {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    padding: 10px 0;

    .auto-login-user-item {
      display: flex;
      flex-direction: column;
      gap: 8px;
      align-items: center;
      justify-content: center;
      width: 120px;
      padding: 12px;
      cursor: pointer;
      background-color: var(--el-fill-color-lighter);
      border: 2px solid var(--el-border-color-light);
      border-radius: 12px;
      box-shadow: var(--el-box-shadow-light);
      transition: all 0.3s ease;

      &:hover {
        background-color: var(--el-color-primary-light-9);
        border-color: var(--el-color-primary);
        box-shadow: var(--el-box-shadow);
        transform: translateY(-2px);
      }

      .user-avatar {
        border: 2px solid var(--el-border-color);
        transition: all 0.3s ease;

        &:hover {
          border-color: var(--el-color-primary);
        }
      }

      .user-name {
        max-width: 80px;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 14px;
        font-weight: 500;
        text-align: center;
        white-space: nowrap;
      }

      .user-username {
        max-width: 80px;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 12px;
        text-align: center;
        white-space: nowrap;
      }
    }
  }
}

.third-party-login {
  .divider-container {
    display: flex;
    align-items: center;
    margin: 20px 0;

    .divider-line {
      flex: 1;
      height: 1px;
      background: linear-gradient(to right, transparent, var(--el-border-color-light), transparent);
    }

    .divider-text {
      padding: 0 16px;
      font-size: 12px;
      color: var(--el-text-color-regular);
      white-space: nowrap;
    }
  }
}
</style>
