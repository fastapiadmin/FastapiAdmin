<!-- 锁屏 -->
<template>
  <div class="layout-lock-screen">
    <!-- 开发者工具警告覆盖层 -->
    <div
      v-if="showDevToolsWarning"
      class="fixed top-0 left-0 z-[999999] flex-cc w-full h-full text-white bg-gradient-to-br from-[#1e1e1e] to-black animate-fade-in"
    >
      <div class="p-5 text-center select-none">
        <div class="mb-7.5 text-5xl">🔒</div>
        <h1 class="m-0 mb-5 text-3xl font-semibold text-danger">系统已锁定</h1>
        <p class="max-w-125 m-0 text-lg leading-relaxed text-white">
          检测到开发者工具已打开
          <br />
          为了系统安全，请关闭开发者工具后继续使用
        </p>
        <div class="mt-7.5 text-sm text-gray-400">Security Lock Activated</div>
      </div>
    </div>

    <!-- 设置锁屏密码弹窗（与旧版 LockDialog.vue 一致；锁密码仍写入 userStore + 加密） -->
    <div v-if="!isLock">
      <FaDialog
        v-model="visible"
        width="500px"
        max-height="170px"
        :title="t('lock.lockScreen')"
        class="v-lock-dialog"
        @opened="handleDialogOpen"
      >
        <div class="lock-dialog-content">
          <img v-if="userAvatar" :src="userAvatar" alt="" class="lock-dialog-avatar object-cover" />
          <img v-else class="lock-dialog-avatar" src="@imgs/user/avatar.webp" alt="" />
          <span class="lock-dialog-name">{{ displayName }}</span>
        </div>
        <ElForm ref="formRef" :model="formData" :rules="rules" @submit.prevent="handleLock">
          <ElFormItem :label="t('lockScreen.lockPassword')" prop="password">
            <ElInput
              ref="lockInputRef"
              v-model="formData.password"
              type="password"
              show-password
              clearable
              autocomplete="new-password"
              :placeholder="t('lock.placeholder')"
              @keydown.enter="handleLock"
            />
          </ElFormItem>
        </ElForm>
        <template #footer>
          <ElButton type="primary" @click="handleLock">{{ t("navbar.lock") }}</ElButton>
        </template>
      </FaDialog>
    </div>

    <!-- 解锁全屏（旧版 LockPage 样式） -->
    <div v-else class="lockpage" :style="lockPageBgStyle">
      <div v-show="showClock" class="unlock-container" @click="showUnlockForm">
        <ElIcon><Lock /></ElIcon>
        <span>{{ t("lock.unlock") }}</span>
      </div>

      <div class="time-container w-screen h-screen">
        <div class="hour-container mr-5 md:mr-20 w-2/5 h-2/5 md:h-4/5">
          <span>{{ hour }}</span>
          <span v-show="showClock" class="meridiem absolute left-5 top-5 text-md xl:text-xl">
            {{ meridiem }}
          </span>
        </div>
        <div class="minute-container w-2/5 h-2/5 md:h-4/5">
          <span>{{ minute }}</span>
        </div>
      </div>

      <transition name="fade-slide">
        <div v-show="!showClock" class="entry-wrapper">
          <div class="entry-content">
            <div class="avatar-container">
              <img v-if="userAvatar" :src="userAvatar" alt="" class="avatar object-cover" />
              <img v-else class="avatar" src="@imgs/user/avatar.webp" alt="" />
              <span class="username">{{ displayName }}</span>
            </div>
            <ElInput
              ref="passwordInputRef"
              v-model="unlockPwd"
              :placeholder="t('lock.placeholder')"
              class="password-input"
              show-password
              clearable
              @keydown.enter="submitUnlock"
            />
            <span v-if="unlockErrMsg" class="error-message">
              {{ t("lock.message") }}
            </span>
            <div class="button-group">
              <ElButton
                type="primary"
                size="small"
                class="back-button"
                link
                :disabled="unlockLoading"
                @click="showClockView"
              >
                {{ t("common.back") }}
              </ElButton>
              <ElButton
                type="primary"
                size="small"
                class="login-button"
                link
                :disabled="unlockLoading"
                @click="goLogin"
              >
                {{ t("lock.backToLogin") }}
              </ElButton>
              <ElButton
                type="primary"
                class="entry-button"
                size="small"
                link
                :disabled="unlockLoading"
                @click="submitUnlock"
              >
                {{ t("lock.entrySystem") }}
              </ElButton>
            </div>
          </div>
        </div>
      </transition>

      <div class="date-container">
        <div v-show="!showClock" class="time-display">
          {{ hour }}:{{ minute }}
          <span class="meridiem-display">{{ meridiem }}</span>
        </div>
        <div class="full-date">{{ year }}/{{ month }}/{{ day }} {{ week }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Lock } from "@element-plus/icons-vue";
import type { FormInstance, FormRules } from "element-plus";
import { ElInput } from "element-plus";
import FaDialog from "@/components/modal/fa-dialog/index.vue";
import { useI18n } from "vue-i18n";
import { useRoute, useRouter } from "vue-router";
import CryptoJS from "crypto-js";
import { useUserStore } from "@stores/modules/user.store";
import { useSettingsStore } from "@stores/modules/setting.store";
import { mittBus } from "@utils/sys";
import { useNow } from "@utils/common";
import bgDark from "@imgs/lock/bg_dark.webp";
import bgLight from "@imgs/lock/bg_light.webp";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const ENCRYPT_KEY = import.meta.env.VITE_LOCK_ENCRYPT_KEY;

const userStore = useUserStore();
const settingsStore = useSettingsStore();
const { info: userInfo, lockPassword, isLock } = storeToRefs(userStore);
const { isDark } = storeToRefs(settingsStore);

/** 锁屏全屏背景：随明暗主题切换壁纸，叠加半透明罩层保证时钟/文案可读 */
const lockPageBgStyle = computed(() => {
  const url = isDark.value ? bgDark : bgLight;
  return {
    backgroundImage: `linear-gradient(rgb(0 0 0 / 46%), rgb(0 0 0 / 46%)), url(${url})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundRepeat: "no-repeat",
  };
});

const { hour, month, minute, meridiem, year, day, week } = useNow(true);

const displayName = computed(
  () =>
    (userInfo.value as { name?: string; username?: string })?.name ||
    (userInfo.value as { username?: string })?.username ||
    "—"
);

const userAvatar = computed(() => {
  const a = (userInfo.value as { avatar?: string })?.avatar?.trim();
  return a || "";
});

const visible = ref<boolean>(false);
const lockInputRef = ref<any>(null);
const passwordInputRef = ref<InstanceType<typeof ElInput>>();
const showDevToolsWarning = ref<boolean>(false);

/** true：大号时钟；false：密码表单（与旧版 LockPage showDate 一致） */
const showClock = ref(true);
const unlockPwd = ref("");
const unlockErrMsg = ref(false);
const unlockLoading = ref(false);

const formRef = ref<FormInstance>();

const formData = ref({
  password: "",
});

const rules = computed<FormRules>(() => ({
  password: [{ required: true, message: t("lock.required"), trigger: "blur" }],
}));

const isMobile = () => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
};

const disableDevTools = () => {
  const handleContextMenu = (e: Event) => {
    if (isLock.value) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }
  };
  document.addEventListener("contextmenu", handleContextMenu, true);

  const handleKeyDown = (e: KeyboardEvent) => {
    if (!isLock.value) return;

    if (e.key === "F12") {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    if (e.ctrlKey && e.shiftKey) {
      const key = e.key.toLowerCase();
      if (["i", "j", "c", "k"].includes(key)) {
        e.preventDefault();
        e.stopPropagation();
        return false;
      }
    }

    if (e.ctrlKey && e.key.toLowerCase() === "u") {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    if (e.ctrlKey && e.key.toLowerCase() === "s") {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    if (e.ctrlKey && e.key.toLowerCase() === "a") {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    if (e.ctrlKey && e.key.toLowerCase() === "p") {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    if (e.ctrlKey && e.key.toLowerCase() === "f") {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    if (e.altKey && e.key === "Tab") {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    if (e.ctrlKey && e.key === "Tab") {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    if (e.ctrlKey && e.key.toLowerCase() === "w") {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    if ((e.ctrlKey && e.key.toLowerCase() === "r") || e.key === "F5") {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "r") {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }
  };
  document.addEventListener("keydown", handleKeyDown, true);

  const handleSelectStart = (e: Event) => {
    if (isLock.value) {
      e.preventDefault();
      return false;
    }
  };
  document.addEventListener("selectstart", handleSelectStart, true);

  const handleDragStart = (e: Event) => {
    if (isLock.value) {
      e.preventDefault();
      return false;
    }
  };
  document.addEventListener("dragstart", handleDragStart, true);

  const devtools = { open: false };
  const threshold = 160;
  let devToolsInterval: ReturnType<typeof setInterval> | null = null;

  const checkDevTools = () => {
    if (!isLock.value || isMobile()) return;

    const isDevToolsOpen =
      window.outerHeight - window.innerHeight > threshold ||
      window.outerWidth - window.innerWidth > threshold;

    if (isDevToolsOpen && !devtools.open) {
      devtools.open = true;
      showDevToolsWarning.value = true;
    } else if (!isDevToolsOpen && devtools.open) {
      devtools.open = false;
      showDevToolsWarning.value = false;
    }
  };

  if (!isMobile()) {
    devToolsInterval = setInterval(checkDevTools, 500);
  }

  return () => {
    document.removeEventListener("contextmenu", handleContextMenu, true);
    document.removeEventListener("keydown", handleKeyDown, true);
    document.removeEventListener("selectstart", handleSelectStart, true);
    document.removeEventListener("dragstart", handleDragStart, true);
    if (devToolsInterval) {
      clearInterval(devToolsInterval);
    }
  };
};

const verifyPassword = (inputPassword: string, storedPassword: string): boolean => {
  try {
    const decryptedPassword = CryptoJS.AES.decrypt(storedPassword, ENCRYPT_KEY).toString(
      CryptoJS.enc.Utf8
    );
    return inputPassword === decryptedPassword;
  } catch (error) {
    console.error("密码解密失败:", error);
    return false;
  }
};

const handleKeydown = (event: KeyboardEvent) => {
  if (event.altKey && event.key.toLowerCase() === "¬") {
    event.preventDefault();
    if (!isLock.value) {
      visible.value = true;
    }
  }
};

const handleDialogOpen = () => {
  setTimeout(() => {
    lockInputRef.value?.input?.focus();
  }, 100);
};

const handleLock = async () => {
  if (!formRef.value) return;

  await formRef.value.validate((valid, fields) => {
    if (valid) {
      const encryptedPassword = CryptoJS.AES.encrypt(
        formData.value.password,
        ENCRYPT_KEY
      ).toString();
      userStore.setLockStatus(true);
      userStore.setLockPassword(encryptedPassword);
      visible.value = false;
      formData.value.password = "";
      showClock.value = true;
      unlockPwd.value = "";
      unlockErrMsg.value = false;
    } else {
      console.error("表单验证失败:", fields);
    }
  });
};

function showUnlockForm() {
  showClock.value = false;
  unlockErrMsg.value = false;
  requestAnimationFrame(() => {
    passwordInputRef.value?.focus?.();
  });
}

function showClockView() {
  showClock.value = true;
  unlockPwd.value = "";
  unlockErrMsg.value = false;
}

async function submitUnlock() {
  if (!unlockPwd.value) {
    return;
  }
  unlockLoading.value = true;
  try {
    const isValid = verifyPassword(unlockPwd.value, lockPassword.value);
    if (isValid) {
      userStore.setLockStatus(false);
      userStore.setLockPassword("");
      unlockPwd.value = "";
      unlockErrMsg.value = false;
      visible.value = false;
      showDevToolsWarning.value = false;
      showClock.value = true;
    } else {
      unlockErrMsg.value = true;
      ElMessage.error(t("lockScreen.pwdError"));
      const root = passwordInputRef.value?.$el as HTMLElement | undefined;
      const inputWrap = root?.querySelector?.(".el-input__wrapper") as HTMLElement | undefined;
      const shakeTarget = inputWrap ?? root;
      if (shakeTarget) {
        shakeTarget.classList.add("shake-animation");
        setTimeout(() => {
          shakeTarget.classList.remove("shake-animation");
        }, 300);
      }
      unlockPwd.value = "";
    }
  } finally {
    unlockLoading.value = false;
  }
}

async function goLogin() {
  await userStore.logout({ navigate: false }).catch(() => {});
  const redirect = route.path !== "/login" && route.name !== "Login" ? route.fullPath : undefined;
  await router.replace({
    name: "Login",
    ...(redirect ? { query: { redirect } } : {}),
  });
}

const openLockScreen = () => {
  if (!isLock.value) {
    visible.value = true;
  }
};

watch(isLock, (newValue) => {
  if (newValue) {
    document.body.style.overflow = "hidden";
    showClock.value = true;
    unlockPwd.value = "";
    unlockErrMsg.value = false;
  } else {
    document.body.style.overflow = "auto";
    showDevToolsWarning.value = false;
  }
});

let cleanupDevTools: (() => void) | null = null;

onMounted(() => {
  mittBus.on("openLockScreen", openLockScreen);
  document.addEventListener("keydown", handleKeydown);

  if (isLock.value) {
    document.body.style.overflow = "hidden";
  }

  cleanupDevTools = disableDevTools();
});

onUnmounted(() => {
  mittBus.off("openLockScreen", openLockScreen);
  document.removeEventListener("keydown", handleKeydown);
  document.body.style.overflow = "auto";
  if (cleanupDevTools) {
    cleanupDevTools();
    cleanupDevTools = null;
  }
});
</script>

<style lang="scss" scoped>
.v-lock-dialog {
  @media (width <=767px) {
    max-width: calc(100vw - 16px);
  }

  .lock-dialog {
    &-content {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    &-avatar {
      width: 70px;
      height: 70px;
      border-radius: 50%;
    }

    &-name {
      margin: 10px 0;
      font-size: 14px;
      color: var(--top-header-text-color);
    }
  }
}

.lockpage {
  position: fixed;
  inset: 0;
  top: 0;
  left: 0;
  z-index: 3000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: var(--el-color-white);

  .unlock-container {
    position: absolute;
    top: 0.5rem;
    left: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 4rem;
    padding: 0.5rem 1rem;
    padding-top: 1.25rem;
    color: inherit;
    cursor: pointer;
    border-radius: 12px;
    transform: translateX(-50%);

    @media (width >= 640px) {
      font-size: 0.875rem;
    }

    @media (width >= 1280px) {
      font-size: 1.25rem;
    }
  }

  .time-container {
    display: flex;
    align-items: center;
    justify-content: center;

    .hour-container {
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1rem;
      margin-bottom: 2rem;
      font-size: 220px;
      font-weight: 700;
      color: var(--el-text-color-primary);
      background-color: var(--el-bg-color-overlay);
      border-radius: 16px;
      backdrop-filter: blur(8px);
    }

    .minute-container {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1rem;
      margin-bottom: 2rem;
      font-size: 220px;
      font-weight: 700;
      color: var(--el-text-color-primary);
      background-color: var(--el-bg-color-overlay);
      border-radius: 16px;
      backdrop-filter: blur(8px);
    }
  }

  .meridiem {
    position: absolute;
    top: 1.25rem;
    left: 1.25rem;
    font-size: 1.25rem;
  }

  .entry-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    background-color: rgb(0 0 0 / 50%);
    backdrop-filter: blur(8px);
  }

  .entry-content {
    width: 260px;
    color: var(--el-text-color-regular);
    text-align: center;
  }

  .avatar-container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .avatar {
    width: 70px;
    height: 70px;
    border-radius: 50%;
  }

  .username {
    margin: 0.625rem 0;
    font-size: 0.875rem;
    color: var(--el-text-color-primary);
  }

  .password-input {
    margin-top: 1rem;
  }

  .error-message {
    display: inline-block;
    margin-top: 0.625rem;
    font-size: 0.875rem;
    color: var(--el-color-danger);
  }

  .button-group {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 0.5rem;

    .back-button,
    .login-button,
    .entry-button {
      min-width: auto;
      padding: 0;
    }

    .login-button {
      flex: 1;
      text-align: center;
    }
  }

  .date-container {
    position: absolute;
    bottom: 1.25rem;
    width: 100%;
    color: inherit;
    text-align: center;

    @media (width >= 1280px) {
      font-size: 1.25rem;
    }

    @media (width >= 1536px) {
      font-size: 1.875rem;
    }
  }

  .time-display {
    margin-bottom: 1rem;
    font-size: 3rem;

    .meridiem-display {
      font-size: 1.875rem;
    }
  }

  .full-date {
    font-size: 1.5rem;
  }
}

.fade-slide-leave-active,
.fade-slide-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(-60px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(60px);
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: scale(0.9);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-in-out;
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }

  10%,
  30%,
  50%,
  70%,
  90% {
    transform: translateX(-10px);
  }

  20%,
  40%,
  60%,
  80% {
    transform: translateX(10px);
  }
}

.shake-animation {
  animation: shake 0.5s ease-in-out;
}
</style>
