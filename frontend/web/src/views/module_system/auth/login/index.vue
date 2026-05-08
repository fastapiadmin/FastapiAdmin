<!-- 登录页：顶栏固定；仅插画列与表单区随布局切换 -->
<template>
  <div class="login-page-root flex h-screen w-full flex-col overflow-hidden">
    <LoginCenterBackdrop v-if="panelAlign === 'center'" viewport-fixed />
    <AuthTopBar v-model:panel-align="panelAlign" />

    <div
      class="login-auth-split relative z-[1] flex min-h-0 flex-1 overflow-hidden"
      :class="`login-auth-split--${panelAlign}`"
    >
      <div
        v-if="panelAlign !== 'center'"
        class="login-auth-split__col login-auth-split__col--illustration"
      >
        <LoginLeftView hide-top-branding />
      </div>

      <div
        class="login-auth-split__col login-auth-split__col--form login-page-panel relative flex min-h-0 min-w-0 flex-col"
        :class="panelAlign === 'center' ? 'bg-transparent' : 'bg-[var(--el-bg-color-page)]'"
      >
        <div
          class="login-page-panel__main relative z-[1] flex min-h-0 flex-1 flex-col overflow-hidden px-5 pb-2 pt-14 md:px-10 md:pt-[4.5rem]"
        >
          <div
            class="login-page-panel__scroll min-h-0 flex-1 overflow-y-auto overflow-x-hidden pb-6 [-webkit-overflow-scrolling:touch]"
            :class="panelAlign === 'center' && 'login-page-panel__scroll--centered'"
          >
            <div
              class="login-panel-align-row flex w-full items-center justify-center max-sm:min-h-0"
              :class="
                panelAlign === 'center'
                  ? 'min-h-0 flex-1 py-4'
                  : 'min-h-[min(720px,calc(100vh-13rem))]'
              "
            >
              <div class="auth-right-wrap">
                <div class="form">
                  <div class="form-intro">
                    <h3 class="title">{{ panelTitle }}</h3>
                    <p class="sub-title">{{ panelSubTitle }}</p>
                  </div>

                  <template v-if="authPanel === 'login'">
                    <template v-if="loginFlowMode === 'account'">
                      <LoginAccountForm
                        ref="accountFormRef"
                        v-model:is-passing="isPassing"
                        v-model:is-click-pass="isClickPass"
                        :login-form="loginForm"
                        :rules="rules"
                        :captcha-state="captchaState"
                        :code-loading="codeLoading"
                        :demo-account-key="demoAccountKey"
                        :accounts="accounts"
                        :form-key="formKey"
                        :is-dark="isDark"
                        :drag-verify-text-color="dragVerifyTextColor"
                        :loading="loading"
                        @submit="handleSubmit"
                        @setup-account="setupAccount"
                        @get-captcha="getCaptcha"
                        @open-mobile="openMobileLogin"
                        @open-qr="openQrLogin"
                        @forget="setAuthPanel('forget')"
                        @register="setAuthPanel('register')"
                        @oauth="handleOAuthLogin"
                      />
                    </template>

                    <LoginMobilePanel
                      v-else-if="loginFlowMode === 'mobile'"
                      @back="backToAccountLogin"
                      @register="setAuthPanel('register')"
                    />

                    <LoginQrPanel
                      v-else-if="loginFlowMode === 'qr'"
                      @back="backToAccountLogin"
                      @register="setAuthPanel('register')"
                    />
                  </template>

                  <LoginRegisterPanel
                    v-else-if="authPanel === 'register'"
                    ref="registerPanelRef"
                    v-model:register-agreement-read="registerAgreementRead"
                    :register-form="registerForm"
                    :register-rules="registerRules"
                    :form-key="formKey"
                    :register-loading="registerLoading"
                    :user-agreement-href="userAgreementHref"
                    @submit="submitRegister"
                    @to-login="setAuthPanel('login')"
                  />

                  <LoginForgetPanel
                    v-else
                    ref="forgetPanelRef"
                    :forget-form="forgetForm"
                    :forget-rules="forgetRules"
                    :form-key="formKey"
                    :forget-loading="forgetLoading"
                    @submit="submitForget"
                    @to-login="setAuthPanel('login')"
                  />
                </div>
              </div>
            </div>
          </div>

          <footer
            class="login-page-footer login-page-footer--pinned flex-shrink-0 pb-[max(0.75rem,env(safe-area-inset-bottom))] pt-3"
            :class="panelAlign === 'center' && 'login-page-footer--floating-layout'"
          >
            <div class="login-footer-text text-sm">
              <a
                :href="configStore.configData?.sys_git_code?.config_value || '#'"
                target="_blank"
                rel="noopener noreferrer"
                class="login-page-footer__link"
              >
                {{ configStore.configData?.sys_web_copyright?.config_value || "" }}
              </a>
              <span class="login-page-footer__sep">|</span>
              <a
                :href="configStore.configData?.sys_help_doc?.config_value || '#'"
                target="_blank"
                rel="noopener noreferrer"
                class="login-page-footer__link"
              >
                帮助
              </a>
              <span class="login-page-footer__sep">|</span>
              <a
                :href="configStore.configData?.sys_web_privacy?.config_value || '#'"
                target="_blank"
                rel="noopener noreferrer"
                class="login-page-footer__link"
              >
                隐私
              </a>
              <span class="login-page-footer__sep">|</span>
              <a
                :href="configStore.configData?.sys_web_clause?.config_value || '#'"
                target="_blank"
                rel="noopener noreferrer"
                class="login-page-footer__link"
              >
                条款
              </a>
              <span
                v-if="configStore.configData?.sys_keep_record?.config_value"
                class="login-page-footer__record"
              >
                {{ configStore.configData.sys_keep_record.config_value }}
              </span>
            </div>
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { LocationQuery, RouteLocationRaw } from "vue-router";
import AuthAPI, {
  type CaptchaInfo,
  type LoginFormData,
  type OAuthProvider,
} from "@/api/module_system/auth";
import UserAPI, { type ForgetPasswordForm, type RegisterForm } from "@/api/module_system/user";
import { useConfigStore } from "@stores/modules/config.store";
import { useAppStore } from "@stores/modules/app.store";
import { useSettingsStore } from "@stores/modules/setting.store";
import { useUserStore } from "@stores/modules/user.store";
import { Auth } from "@utils/auth";
import { HttpError } from "@utils/http";
import { startOAuthLogin } from "@utils/oauth";
import { ElMessage, ElNotification, type FormRules } from "element-plus";
import LoginAccountForm from "./components/LoginAccountForm.vue";
import LoginForgetPanel from "./components/LoginForgetPanel.vue";
import LoginMobilePanel from "./components/LoginMobilePanel.vue";
import LoginQrPanel from "./components/LoginQrPanel.vue";
import LoginRegisterPanel from "./components/LoginRegisterPanel.vue";
import type { Account, AccountKey } from "./types";
import { useLoginPanelAlign } from "../composables/useLoginPanelAlign";

defineOptions({ name: "Login" });

type AuthPanel = "login" | "register" | "forget";

/** 登录区内：账号密码 ↔ 手机号 ↔ 扫码（扫码 / 手机号为演示交互） */
type LoginFlowMode = "account" | "mobile" | "qr";

const configStore = useConfigStore();
const settingStore = useSettingsStore();
const appStore = useAppStore();
const { isDark } = storeToRefs(settingStore);
const { t, locale } = useI18n();

const { panelAlign } = useLoginPanelAlign();

const authPanel = ref<AuthPanel>("login");
const loginFlowMode = ref<LoginFlowMode>("account");

const panelTitle = computed(() => {
  if (authPanel.value === "register") return t("login.reg");
  if (authPanel.value === "forget") return t("login.resetPassword");
  if (
    authPanel.value === "login" &&
    (loginFlowMode.value === "mobile" || loginFlowMode.value === "qr")
  ) {
    return t("login.qrLoginTitle");
  }
  return t("login.title");
});

const panelSubTitle = computed(() => {
  if (authPanel.value === "register") return t("register.subTitle");
  if (authPanel.value === "forget") return t("forgetPassword.subTitle");
  if (authPanel.value === "login" && loginFlowMode.value === "mobile") {
    return t("login.mobileLoginSubTitle");
  }
  if (authPanel.value === "login" && loginFlowMode.value === "qr") {
    return t("login.qrLoginSubTitle");
  }
  return t("login.subTitle");
});

const userAgreementHref = computed(
  () => configStore.configData?.sys_web_clause?.config_value || "#"
);

function setAuthPanel(panel: AuthPanel) {
  authPanel.value = panel;
  if (panel !== "login") {
    loginFlowMode.value = "account";
  }
  nextTick(() => {
    accountFormRef.value?.clearValidate?.();
    registerPanelRef.value?.clearValidate?.();
    forgetPanelRef.value?.clearValidate?.();
  });
}

function openMobileLogin() {
  loginFlowMode.value = "mobile";
}

function openQrLogin() {
  loginFlowMode.value = "qr";
}

function backToAccountLogin() {
  loginFlowMode.value = "account";
  nextTick(() => {
    getCaptcha();
    loginForm.captcha = "";
    accountFormRef.value?.resetDragVerify?.();
    isPassing.value = false;
    isClickPass.value = false;
  });
}

function handleOAuthLogin(provider: OAuthProvider) {
  startOAuthLogin(provider);
}

async function tryConsumeOAuthCallback() {
  const q = route.query;
  const oauthError = q.oauth_error as string | undefined;
  const access = q.access_token as string | undefined;
  const refresh = q.refresh_token as string | undefined;

  if (!oauthError && !(access && refresh)) return;

  const rest: Record<string, unknown> = { ...q };
  delete rest.oauth_error;
  delete rest.access_token;
  delete rest.refresh_token;
  delete rest.token_type;

  if (oauthError) {
    ElMessage.error(decodeURIComponent(oauthError));
    await router.replace({ path: route.path, query: rest as LocationQuery });
    return;
  }

  if (access && refresh) {
    try {
      Auth.setTokens(access, refresh, true);
      userStore.setToken(access, refresh);
      userStore.setLoginStatus(true);
      await userStore.getUserInfo();
      ElNotification({
        title: t("login.oauthNoticeTitle"),
        message: t("login.oauthLoginSuccess"),
        type: "success",
      });
      await router.replace(resolveRedirectTarget(rest as LocationQuery));
      if (settingStore.showGuide) {
        appStore.showGuide(true);
      }
    } catch (error) {
      console.error("[Login] OAuth callback:", error);
      ElMessage.error(t("login.oauthLoginFailed"));
      await router.replace({ path: route.path, query: rest as LocationQuery });
    }
  }
}

const dragVerifyTextColor = computed(() =>
  isDark.value ? "rgba(255, 255, 255, 0.45)" : "var(--art-gray-700)"
);
const formKey = ref(0);

watch(locale, () => {
  formKey.value++;
});

watch(authPanel, (panel) => {
  if (panel !== "login") return;
  if (loginFlowMode.value !== "account") return;
  getCaptcha();
  loginForm.captcha = "";
  accountFormRef.value?.resetDragVerify?.();
  isPassing.value = false;
  isClickPass.value = false;
});

const accounts = computed<Account[]>(() => [
  {
    key: "super",
    label: t("login.roles.super"),
    username: "super",
    password: "123456",
    roles: ["R_SUPER"],
  },
  {
    key: "admin",
    label: t("login.roles.admin"),
    username: "admin",
    password: "123456",
    roles: ["R_ADMIN"],
  },
  {
    key: "user",
    label: t("login.roles.user"),
    username: "user",
    password: "123456",
    roles: ["R_USER"],
  },
]);

const demoAccountKey = ref<AccountKey>("super");
const userStore = useUserStore();
const router = useRouter();
const route = useRoute();
const isPassing = ref(false);
const isClickPass = ref(false);

const accountFormRef = ref<InstanceType<typeof LoginAccountForm> | null>(null);
const registerPanelRef = ref<InstanceType<typeof LoginRegisterPanel> | null>(null);
const forgetPanelRef = ref<InstanceType<typeof LoginForgetPanel> | null>(null);

const loading = ref(false);
const registerLoading = ref(false);
const forgetLoading = ref(false);
const codeLoading = ref(false);

const registerAgreementRead = ref(false);

const registerForm = reactive<RegisterForm>({
  username: "",
  password: "",
  confirmPassword: "",
});

const forgetForm = reactive<ForgetPasswordForm>({
  username: "",
  new_password: "",
  confirmPassword: "",
});

const validateRegisterPassword = (_rule: unknown, value: string, callback: (e?: Error) => void) => {
  if (!value) {
    callback(new Error(t("login.message.password.required")));
    return;
  }
  if (registerForm.confirmPassword) {
    registerPanelRef.value?.validateField?.("confirmPassword");
  }
  callback();
};

const validateRegisterConfirm = (_rule: unknown, value: string, callback: (e?: Error) => void) => {
  if (!value) {
    callback(new Error(t("login.message.password.required")));
    return;
  }
  if (value !== registerForm.password) {
    callback(new Error(t("login.message.password.inconformity")));
    return;
  }
  callback();
};

const registerRules = computed<FormRules<RegisterForm>>(() => ({
  username: [{ required: true, message: t("login.message.username.required"), trigger: "blur" }],
  password: [
    { required: true, validator: validateRegisterPassword, trigger: "blur" },
    { min: 6, message: t("login.message.password.min"), trigger: "blur" },
  ],
  confirmPassword: [
    { required: true, message: t("login.message.password.required"), trigger: "blur" },
    { min: 6, message: t("login.message.password.min"), trigger: "blur" },
    { validator: validateRegisterConfirm, trigger: "blur" },
  ],
}));

const validateForgetConfirm = (_rule: unknown, value: string, callback: (e?: Error) => void) => {
  if (!value) {
    callback(new Error(t("login.message.password.required")));
    return;
  }
  if (value !== forgetForm.new_password) {
    callback(new Error(t("login.message.password.inconformity")));
    return;
  }
  callback();
};

const forgetRules = computed<FormRules<ForgetPasswordForm>>(() => ({
  username: [{ required: true, message: t("login.message.username.required"), trigger: "blur" }],
  new_password: [
    { required: true, message: t("login.message.password.required"), trigger: "blur" },
    { min: 6, message: t("login.message.password.min"), trigger: "blur" },
  ],
  confirmPassword: [
    { required: true, message: t("login.message.password.required"), trigger: "blur" },
    { min: 6, message: t("login.message.password.min"), trigger: "blur" },
    { validator: validateForgetConfirm, trigger: "blur" },
  ],
}));

const loginForm = reactive<LoginFormData>({
  username: "",
  password: "",
  captcha: "",
  captcha_key: "",
  remember: true,
  login_type: "PC端",
});

const captchaState = reactive<CaptchaInfo>({
  enable: false,
  key: "",
  img_base: "",
});

const rules = computed<FormRules>(() => {
  const base: FormRules = {
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
    base.captcha = [
      {
        required: true,
        trigger: "blur",
        message: t("login.message.captchaCode.required"),
      },
    ];
  }
  return base;
});

function setupAccount(key: AccountKey) {
  const selected = accounts.value.find((a: Account) => a.key === key);
  demoAccountKey.value = key;
  loginForm.username = selected?.username ?? "";
  loginForm.password = selected?.password ?? "";
}

async function getCaptcha() {
  try {
    codeLoading.value = true;
    const response = await AuthAPI.getCaptcha();
    const data = response.data.data;
    loginForm.captcha_key = data.key;
    captchaState.img_base = data.img_base;
    captchaState.enable = data.enable;
  } catch {
    captchaState.enable = false;
    loginForm.captcha = "";
    loginForm.captcha_key = "";
  } finally {
    codeLoading.value = false;
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

let notificationInstance: ReturnType<typeof ElNotification> | null = null;

const showVoteNotification = () => {
  notificationInstance = ElNotification({
    title: "⭐ FastapiAdmin 完全开源 · 期待您的 Star 支持 🙏",
    message: `项目持续迭代中，若对您有所帮助，欢迎点亮 Star 支持！
    <br/><a href="https://github.com/fastapiadmin/FastapiAdmin" target="_blank" style="color: var(--el-color-primary); text-decoration: none; font-weight: 500;">Github仓库 →</a>
    <br/><a href="https://gitee.com/fastapiadmin/FastapiAdmin" target="_blank" style="color: var(--el-color-warning); text-decoration: none; font-weight: 500;">Gitee仓库 →</a>`,
    type: "success",
    position: "bottom-left",
    duration: 0,
    dangerouslyUseHTMLString: true,
  });
};

onMounted(async () => {
  setupAccount("super");
  await configStore.getConfig(true);
  await tryConsumeOAuthCallback();
  getCaptcha();
  setTimeout(showVoteNotification, 500);
});

onActivated(() => {
  if (authPanel.value !== "login" || loginFlowMode.value !== "account") return;
  getCaptcha();
  loginForm.captcha = "";
});

onBeforeUnmount(() => {
  notificationInstance?.close();
  notificationInstance = null;
});

watch(
  () => route.fullPath,
  () => {
    if (authPanel.value !== "login" || loginFlowMode.value !== "account") return;
    getCaptcha();
    loginForm.captcha = "";
  }
);

const handleSubmit = async () => {
  if (!accountFormRef.value) return;

  try {
    const valid = await accountFormRef.value.validate?.();
    if (!valid) return;

    if (!isPassing.value) {
      isClickPass.value = true;
      return;
    }

    loading.value = true;

    await userStore.login(loginForm);

    await router.replace(resolveRedirectTarget(route.query));

    if (settingStore.showGuide) {
      appStore.showGuide(true);
    }
  } catch (error) {
    await getCaptcha();
    if (!(error instanceof HttpError)) {
      console.error("[Login] Unexpected error:", error);
      ElNotification({
        title: "提示",
        message: error instanceof Error ? error.message : String(error),
        type: "error",
      });
    }
  } finally {
    loading.value = false;
    accountFormRef.value?.resetDragVerify?.();
  }
};

async function submitRegister() {
  if (!registerAgreementRead.value) {
    ElMessage.warning(t("login.message.agree.required"));
    return;
  }
  if (!registerPanelRef.value) return;
  try {
    await registerPanelRef.value.validate?.();
    registerLoading.value = true;
    await UserAPI.registerUser(registerForm);
    loginForm.username = registerForm.username;
    loginForm.password = registerForm.password;
    registerForm.username = "";
    registerForm.password = "";
    registerForm.confirmPassword = "";
    registerAgreementRead.value = false;
    setAuthPanel("login");
  } catch (error) {
    console.error("[Login] register:", error);
  } finally {
    registerLoading.value = false;
  }
}

async function submitForget() {
  if (!forgetPanelRef.value) return;
  try {
    await forgetPanelRef.value.validate?.();
    forgetLoading.value = true;
    await UserAPI.forgetPassword(forgetForm);
    loginForm.username = forgetForm.username;
    loginForm.password = forgetForm.new_password;
    forgetForm.username = "";
    forgetForm.new_password = "";
    forgetForm.confirmPassword = "";
    setAuthPanel("login");
  } catch (error) {
    console.error("[Login] forget password:", error);
  } finally {
    forgetLoading.value = false;
  }
}
</script>

<style scoped>
@import "./style.css";
</style>

<style lang="scss" scoped>
.login-page-panel {
  :deep(.btn) {
    border-radius: 8px;
  }
}

html.dark .login-page-panel {
  :deep(.text-g-800) {
    color: rgb(255 255 255 / 78%) !important;
  }
}

/* 副标题与表单块间距（login-page-form 在子组件内，须 :deep） */
:deep(.login-page-form) {
  margin-top: 1rem;
}

:deep(.login-page-form .el-form-item) {
  margin-bottom: 1.1rem;
}

:deep(.el-select__wrapper) {
  min-height: 42px !important;
}

/* 仅账号登录底部「手机号 / 扫码」双列按钮需要 42px；手机号登录页的返回钮与主按钮同为 h-11，勿全局压高度 */
:deep(.login-secondary-actions .login-secondary-btn) {
  height: 42px;
  border-radius: 8px;
}

html.dark {
  :deep(.login-page-form .el-input__wrapper) {
    background-color: rgb(255 255 255 / 6%) !important;
    box-shadow: 0 0 0 1px rgb(255 255 255 / 10%) inset !important;
  }

  :deep(.login-page-form .el-input__inner) {
    color: rgb(255 255 255 / 92%);
  }

  :deep(.login-page-form .el-input__inner::placeholder) {
    color: rgb(255 255 255 / 35%);
  }

  :deep(.login-page-form .el-select .el-select__wrapper) {
    background-color: rgb(255 255 255 / 6%) !important;
    box-shadow: 0 0 0 1px rgb(255 255 255 / 10%) inset !important;
  }

  :deep(.login-page-form .el-select__placeholder) {
    color: rgb(255 255 255 / 40%);
  }

  :deep(.login-page-form .el-select__selected-item) {
    color: rgb(255 255 255 / 92%);
  }

  :deep(.login-remember .el-checkbox__label) {
    color: rgb(255 255 255 / 65%);
  }

  :deep(.login-secondary-btn) {
    color: rgb(255 255 255 / 85%) !important;
    background: transparent !important;
    border-color: rgb(255 255 255 / 22%) !important;
    border-radius: 8px;

    &:hover {
      color: var(--el-color-primary) !important;
      background: var(--el-color-primary-light-9) !important;
      border-color: var(--el-color-primary) !important;
    }
  }

  :deep(.login-secondary-actions .login-secondary-btn) {
    height: 42px;
  }
}

.login-page-footer {
  margin-top: 0;
  text-align: center;
  border-top: 1px solid var(--el-border-color-lighter);

  .login-footer-text {
    line-height: 1.65;
    color: var(--el-text-color-secondary) !important;
  }

  .login-page-footer__link {
    color: var(--el-text-color-regular);
    text-decoration: none;
    transition: color 0.2s ease;

    &:hover {
      color: var(--el-color-primary);
    }
  }

  .login-page-footer__sep {
    margin: 0 0.35rem;
    color: var(--el-border-color);
  }

  .login-page-footer__record {
    display: inline-block;
    margin-left: 0.35rem;
    color: var(--el-text-color-placeholder);
  }
}

html.dark .login-page-footer {
  border-top-color: rgb(255 255 255 / 8%);

  .login-footer-text {
    color: rgb(255 255 255 / 42%) !important;
  }

  .login-page-footer__link {
    color: rgb(255 255 255 / 48%);

    &:hover {
      color: var(--el-color-primary);
    }
  }

  .login-page-footer__sep {
    color: rgb(255 255 255 / 25%);
  }

  .login-page-footer__record {
    color: rgb(255 255 255 / 35%);
  }
}
</style>
