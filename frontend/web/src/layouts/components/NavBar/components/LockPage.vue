<template>
  <div class="lockpage">
    <div v-show="showDate" class="unlock-container" @click="handleShowForm(false)">
      <el-icon><Lock /></el-icon>
      <span>{{ t('lock.unlock') }}</span>
    </div>

    <div class="time-container w-screen h-screen">
      <div class="hour-container mr-5 md:mr-20 w-2/5 h-2/5 md:h-4/5">
        <span>{{ hour }}</span>
        <span v-show="showDate" class="meridiem absolute left-5 top-5 text-md xl:text-xl">
          {{ meridiem }}
        </span>
      </div>
      <div class="minute-container w-2/5 h-2/5 md:h-4/5">
        <span>{{ minute }}</span>
      </div>
    </div>

    <transition name="fade-slide">
      <div v-show="!showDate" class="entry-wrapper">
        <div class="entry-content">
          <div class="avatar-container">
            <img :src="userStore.basicInfo.avatar" alt="" class="avatar" />
            <span class="username">{{ userStore.basicInfo.name }}</span>
          </div>
          <ElInput
            ref="passwordInputRef"
            v-model="password"
            :placeholder="t('lock.placeholder')"
            class="password-input"
            show-password
            clearable
            @keydown.enter="unLock"
          />
          <span v-if="errMsg" class="error-message">
            {{ t('lock.message') }}
          </span>
          <div class="button-group">
            <el-button
              type="primary"
              size="small"
              class="back-button"
              link
              :disabled="loading"
              @click="handleShowForm(true)"
            >
              {{ t('common.back') }}
            </el-button>
            <el-button
              type="primary"
              size="small"
              class="login-button"
              link
              :disabled="loading"
              @click="goLogin"
            >
              {{ t('lock.backToLogin') }}
            </el-button>
            <el-button
              type="primary"
              class="entry-button"
              size="small"
              link
              :disabled="loading"
              @click="unLock()"
            >
              {{ t('lock.entrySystem') }}
            </el-button>
          </div>
        </div>
      </div>
    </transition>

    <div class="date-container">
      <div v-show="!showDate" class="time-display">
        {{ hour }}:{{ minute }}
        <span class="meridiem-display">{{ meridiem }}</span>
      </div>
      <div class="full-date">{{ year }}/{{ month }}/{{ day }} {{ week }}</div>
    </div>
  </div>
</template>

<script lang="ts" setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useUserStore, useLockStore } from '@/store';
  import { ElInput } from 'element-plus';
  import { useNow } from '@/utils/dateUtil';

  const route = useRoute();
  const router = useRouter();
  const userStore = useUserStore();

  const password = ref('');
  const loading = ref(false);
  const errMsg = ref(false);
  const showDate = ref(true);

  const lockStore = useLockStore();

  const { hour, month, minute, meridiem, year, day, week } = useNow(true);

  const { t } = useI18n();

  // 解锁
  async function unLock() {
    if (!password.value) {
      return;
    }
    const pwd = password.value;
    try {
      loading.value = true;
      const res = await lockStore.unLock(pwd);
      errMsg.value = !res;
    } finally {
      loading.value = false;
    }
  }

  // 返回登录（logout 成功会 resetAllState；失败时再清一次本地，避免仍带 token）
  async function goLogin() {
    await userStore.logout().catch(() => {});
    await userStore.resetAllState();
    lockStore.resetLockInfo();
    await router.replace(`/login?redirect=${encodeURIComponent(route.fullPath)}`);
  }

  const passwordInputRef = ref<InstanceType<typeof ElInput>>();

  function handleShowForm(show = false) {
    showDate.value = show;
    if (!show) {
      requestAnimationFrame(() => {
        passwordInputRef.value?.focus();
      });
    }
  }
</script>

<style lang="scss" scoped>
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
    background-color: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(8px);

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

      @media (min-width: 640px) {
        font-size: 0.875rem;
      }

      @media (min-width: 1280px) {
        font-size: 1.25rem;
      }
    }

    .time-container {
      display: flex;
      align-items: center;
      justify-content: center;

      .hour-container {
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
      justify-content: space-between; // 左右对齐
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

      @media (min-width: 1280px) {
        font-size: 1.25rem;
      }

      @media (min-width: 1536px) {
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
</style>
