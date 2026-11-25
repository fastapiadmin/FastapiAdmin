<script setup lang="ts">
import type { FormSchema } from '@wot-ui/ui/components/wd-form/types'
import { onLoad } from '@dcloudio/uni-app'
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import AuthAPI from '@/api/module_system/auth'
import UserAPI from '@/api/module_system/user'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'
import { REMEMBER_ME_KEY } from '@/constants'
import { useConfigStore } from '@/store/configStore'
import { useUserStore } from '@/store/userStore'
import { Storage } from '@/utils/storage'

definePage({ name: 'register', style: { navigationBarTitleText: '注册' } })
useI18nNavTitle('register.navTitle')

const { t } = useI18n()
const toast = useToast()
const userStore = useUserStore()
const configStore = useConfigStore()

const submitting = ref(false)
const agreeRead = ref(false)
const registerFormRef = ref()
const registerForm = reactive({
  username: '',
  name: '',
  password: '',
  confirmPassword: '',
})

/** 与后端 UserRegisterSchema 一致：字母开头，3-32 位，仅允许字母、数字、_ . - */
const USERNAME_REG = /^[a-z][\w.-]{2,31}$/i

/** 表单验证 schema — 字段级错误提示（与登录页 wd-form 一致） */
const registerSchema: FormSchema = {
  validate: (model) => {
    const errors: Array<{ path: Array<string | number>, message: string }> = []
    const username = String(model.username ?? '').trim()
    const name = String(model.name ?? '').trim()
    const password = String(model.password ?? '')
    const confirmPassword = String(model.confirmPassword ?? '')
    if (!username)
      errors.push({ path: ['username'], message: t('common.form.usernameRequired') })
    else if (!USERNAME_REG.test(username))
      errors.push({ path: ['username'], message: t('common.form.usernameFormat') })
    if (!name)
      errors.push({ path: ['name'], message: t('common.form.nicknameRequired') })
    if (!password)
      errors.push({ path: ['password'], message: t('common.form.passwordRequired') })
    else if (password.length < 6)
      errors.push({ path: ['password'], message: t('common.form.passwordLength') })
    if (!confirmPassword)
      errors.push({ path: ['confirmPassword'], message: t('common.form.confirmRequired') })
    else if (confirmPassword !== password)
      errors.push({ path: ['confirmPassword'], message: t('common.form.mismatch') })
    return errors
  },
}

/** 打开用户协议：H5 新窗口，其他端复制链接（与设置页链接行为一致） */
function handleAgreementOpen() {
  const url = configStore.configData?.clause?.config_value?.trim() || ''
  if (!url) {
    toast.info(t('register.userAgreement'))
    return
  }
  // #ifdef H5
  window.open(url, '_blank')
  // #endif
  // #ifndef H5
  uni.setClipboardData({
    data: url,
    showToast: false,
    success: () => {
      uni.hideToast()
      toast.success({ msg: url })
    },
  })
  // #endif
}

/**
 * 注册成功后尝试自动登录：
 * - 系统未启用滑块验证码 → 直接登录进入首页
 * - 验证码启用 / 自动登录失败 → 记住用户名回登录页，由用户完成滑块后登录
 */
async function autoLoginAfterRegister(username: string, password: string) {
  try {
    const captcha = await AuthAPI.getCaptcha()
    if (captcha?.enable) {
      Storage.set(REMEMBER_ME_KEY, { username, remember: true })
      uni.reLaunch({ url: '/pages/login/index' })
      return
    }
    await userStore.login({ username, password, remember: true, login_type: '移动端' })
    uni.reLaunch({ url: '/pages/index/index' })
  }
  catch {
    Storage.set(REMEMBER_ME_KEY, { username, remember: true })
    uni.reLaunch({ url: '/pages/login/index' })
  }
}

async function handleSubmit() {
  if (submitting.value)
    return
  if (!agreeRead.value) {
    toast.warning(t('register.agreeRequired'))
    return
  }
  const { valid } = await registerFormRef.value.validate()
  if (!valid)
    return

  const username = registerForm.username.trim()
  const name = registerForm.name.trim()
  submitting.value = true
  try {
    await UserAPI.registerUser({ username, name, password: registerForm.password })
    toast.success(t('register.success'))
    await autoLoginAfterRegister(username, registerForm.password)
  }
  catch {
    // http 层已统一错误提示（如用户名已存在）
  }
  finally {
    submitting.value = false
  }
}

onLoad(() => {
  // 拉取系统参数（用户协议链接 clause），幂等 + 本地持久化缓存
  configStore.getConfig()
})

function goLogin() {
  uni.reLaunch({ url: '/pages/login/index' })
}
</script>

<template>
  <view class="register-page">
    <view class="register-card">
      <text class="register-card__title">
        {{ t('register.title') }}
      </text>

      <view class="register-form">
        <wd-form ref="registerFormRef" :model="registerForm" :schema="registerSchema">
          <text class="form-field-label">{{ t('common.form.username') }}</text>
          <wd-form-item prop="username" custom-style="margin-bottom: 14rpx; padding-left: 0; padding-right: 0;">
            <wd-input
              v-model="registerForm.username"
              :aria-label="t('common.form.username')"
              :placeholder="t('common.form.usernamePlaceholder')"
              clearable
              :compact="false"
              prefix-icon="user"
            />
          </wd-form-item>
          <text class="form-field-label">{{ t('common.form.nickname') }}</text>
          <wd-form-item prop="name" custom-style="margin-bottom: 14rpx; padding-left: 0; padding-right: 0;">
            <wd-input
              v-model="registerForm.name"
              :aria-label="t('common.form.nickname')"
              :placeholder="t('common.form.nicknamePlaceholder')"
              clearable
              :compact="false"
              prefix-icon="user"
            />
          </wd-form-item>
          <text class="form-field-label">{{ t('common.form.password') }}</text>
          <wd-form-item prop="password" custom-style="margin-bottom: 14rpx; padding-left: 0; padding-right: 0;">
            <wd-input
              v-model="registerForm.password"
              :aria-label="t('common.form.password')"
              :placeholder="t('common.form.passwordPlaceholder')"
              show-password
              clearable
              :compact="false"
              prefix-icon="lock"
            />
          </wd-form-item>
          <text class="form-field-label">{{ t('common.form.confirmPassword') }}</text>
          <wd-form-item prop="confirmPassword" custom-style="margin-bottom: 14rpx; padding-left: 0; padding-right: 0;">
            <wd-input
              v-model="registerForm.confirmPassword"
              :aria-label="t('common.form.confirmPassword')"
              :placeholder="t('common.form.confirmPlaceholder')"
              show-password
              clearable
              :compact="false"
              prefix-icon="lock"
            />
          </wd-form-item>
        </wd-form>

        <!-- 用户协议勾选（与 web 端一致，注册前必须同意） -->
        <view class="register-agreement">
          <wd-checkbox v-model="agreeRead" size="18px">
            {{ t('register.agree') }}
          </wd-checkbox>
          <view class="tap-target" aria-role="button" :aria-label="t('register.userAgreement')" @click="handleAgreementOpen">
            <wd-text class="register-agreement__link" :text="t('register.userAgreement')" type="primary" />
          </view>
        </view>

        <wd-button type="primary" round block :loading="submitting" @click="handleSubmit">
          {{ submitting ? t('register.submitting') : t('register.submit') }}
        </wd-button>
      </view>

      <view class="register-footer">
        <wd-text class="register-footer__text" :text="t('register.hasAccount')" />
        <view class="tap-target" aria-role="button" :aria-label="t('register.toLogin')" @click="goLogin">
          <wd-text class="register-footer__link" :text="t('register.toLogin')" type="primary" />
        </view>
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.register-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  /* H5 下 100vh 包含导航栏，使用uni-app的可用视口高度变量避免溢出 */
  /* #ifdef H5 */
  height: calc(100vh - 44px);
  /* #endif */
  /* #ifndef H5 */
  height: 100vh;
  /* #endif */
  padding: 0 64rpx;
  padding-bottom: calc(48rpx + env(safe-area-inset-bottom));
  /* 接入全局水滴渐变（--drop-bg 由 App.vue 按主题色定义，暗色回退纯色由下方规则接管） */
  background: var(--drop-bg, #F9F9F9);
  overflow-x: hidden;
  overflow-y: auto;
  box-sizing: border-box;
}

/* 暗黑模式下整页背景变深，消除白色断层（wot 根类为 wot-theme-dark） */
.wot-theme-dark .register-page {
  @apply wot-bg-filled-bottom;
}

.register-card {
  width: 100%;
  margin-top: 120rpx;
  /* 亮色下默认带主题色最浅阶，避免一片纯白；--card-bg-color 可被外部覆盖 */
  background: var(--card-bg-color, var(--wot-primary-1, #FFFFFF));
  border-radius: var(--fa-radius-md, 24rpx);
  padding: 40rpx 36rpx;
  /* 边框跟随主题色浅阶，替代中性灰，让卡片更有主题感 */
  border: 2rpx solid var(--fa-border, #E6E8EC);
  box-shadow: var(--shadow-md, 0 8rpx 32rpx rgba(15, 23, 42, 0.04));

  .wot-theme-dark & {
    @apply wot-bg-filled-content;
    border-color: var(--border-color, #2C2C2E);
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.2);
  }

  &__title {
    display: block;
    font-size: var(--font-xl, 36rpx);
    font-weight: 600;
    @apply wot-text-text-main;
    margin-bottom: 28rpx;

    /* 暗黑模式下使用纯白，提升卡片标题醒目度 */
    .wot-theme-dark & {
      color: #FFFFFF;
    }
  }
}

.register-form {
  :deep(.wd-input) {
    border-radius: var(--fa-radius-sm, 16rpx);
    /* 亮色下主题色浅阶边框与卡片边框呼应，白色底在淡色卡片上形成浮层 */
    border: 2rpx solid var(--wot-primary-2, var(--wot-border-main, #EAECF0));
    box-shadow: 0 4rpx 16rpx rgba(15, 23, 42, 0.05);
  }

  /* H5 聚焦态：主题色描边 + 淡色光晕（MP 端不支持 :focus-within，跳过） */
  /* #ifdef H5 */
  :deep(.wd-input:focus-within) {
    border-color: var(--wot-primary-6, #1C64FD);
    box-shadow: 0 0 0 4rpx var(--wot-primary-1, #F5F8FF);
  }
  /* #endif */

  /* 去掉 wd-cell 自带左右内边距，使输入框与登录按钮同宽（与登录页一致） */
  :deep(.wd-form-item) {
    margin-bottom: 14rpx;
    padding-left: 0;
    padding-right: 0;
  }
}

/* cell 容器回归透明：亮色下消除输入框外围的白色方形区域，暗色下消除纯黑块，
   让自带圆角+边框的输入框直接显示在卡片上 */
:deep(.wd-cell) {
  --wot-cell-bg: transparent;
}

.wot-theme-dark .register-page :deep(.wd-input) {
  /* 比卡片背景（filled-content）亮一档，输入框在暗色卡片上凸起有层次 */
  --wot-input-bg: var(--wot-coolgrey-8, var(--wot-filled-content));
  border-color: var(--wot-border-main, #2C2C2E);
  box-shadow: none;
}

.register-agreement {
  display: flex;
  align-items: center;
  margin-bottom: 24rpx;

  :deep(.wd-checkbox__label) {
    font-size: var(--font-md, 28rpx);
    @apply wot-text-text-auxiliary;
  }

  &__link {
    font-size: var(--font-md, 28rpx);
  }
}

.register-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8rpx;
  margin-top: 32rpx;

  &__text {
    font-size: var(--font-md, 28rpx);
    @apply wot-text-text-auxiliary;
  }

  &__link {
    font-size: var(--font-md, 28rpx);
  }
}

/* MP 端兼容：wd-form-item 内部 wd-cell 因 uni-app 插槽静态声明（u-s）误判 label/title 插槽被使用，
   showLeft=true 渲染空 left 区域（flex:1 占半宽），H5 端运行时插槽判定无此问题。
   本页 form-item 无 title/label/prefix 内容，隐藏 left 安全，保证输入框与登录按钮同宽 */
.register-card .wd-form-item .wd-cell__left {
  display: none;
}
</style>
