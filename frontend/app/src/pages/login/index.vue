<script lang="ts" setup>
import type { FormSchema } from '@wot-ui/ui/components/wd-form/types'
import type { CaptchaInfo, LoginFormData, OAuthProvider } from '@/api/module_system/auth'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { computed, nextTick, reactive, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import AuthAPI from '@/api/module_system/auth'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'
import { REMEMBER_ME_KEY } from '@/constants'
import { useConfigStore } from '@/store/configStore'
import { useUserStore } from '@/store/userStore'
import { Storage } from '@/utils/storage'

definePage({ name: 'login', style: { navigationBarTitleText: '登录', navigationBarTextStyle: 'white', navigationStyle: 'custom' } })
useI18nNavTitle('login.navTitle')

const { t } = useI18n()
const loginFormRef = ref()
const sliderCaptchaRef = ref<{ reset?: () => void }>()
const captchaVisible = ref(false)
const loading = ref(false)
const userStore = useUserStore()
const configStore = useConfigStore()
const redirect = ref('/pages/index/index')

/** 规范化 BASE_URL（保证以 / 结尾），用于拼接静态资源路径：H5 下避免 base '/app' 拼出 /appstatic/xxx */
const BASE_PATH = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : `${import.meta.env.BASE_URL}/`

/** 品牌区参数（来自后端系统参数，带默认值兜底；web 端消费方式：configData?.[key]?.config_value） */
// 官方默认 Logo 统一使用内置新品牌标识；管理员自定义上传的 Logo 仍优先
const OFFICIAL_LOGO_HOST = 'service.fastapiadmin.com'
const brandLogo = computed(() => {
  const custom = configStore.configData?.logo_url?.config_value?.trim()
  if (!custom || custom.includes(OFFICIAL_LOGO_HOST)) return `${BASE_PATH}static/logo.png`
  return custom
})
const brandTitle = computed(() => {
  const raw = configStore.configData?.sys_name?.config_value?.trim()
  if (!raw) return 'FastapiAdmin'
  return /^fastapiadmin\s*系统$/i.test(raw) ? 'FastapiAdmin' : raw
})
const brandSubtitle = computed(() => configStore.configData?.login_title?.config_value?.trim() || t('login.brandSubtitle'))

/** 表单验证 schema — 用户名/密码字段级错误提示（wot-ui 函数式校验） */
const loginSchema: FormSchema = {
  validate: (model) => {
    const errors: Array<{ path: Array<string | number>, message: string }> = []
    const username = String(model.username ?? '')
    const password = String(model.password ?? '')
    if (!username)
      errors.push({ path: ['username'], message: t('common.form.usernameRequired') })
    else if (username.length < 3 || username.length > 20)
      errors.push({ path: ['username'], message: t('login.usernameLength') })
    if (!password)
      errors.push({ path: ['password'], message: t('common.form.passwordRequired') })
    else if (password.length < 6 || password.length > 20)
      errors.push({ path: ['password'], message: t('login.passwordLength') })
    return errors
  },
}

const loginFormData = reactive<LoginFormData>({
  username: '',
  password: '',
  captcha: '',
  captcha_key: '',
  remember: true,
  login_type: '移动端',
})

const captchaState = reactive<CaptchaInfo>({
  enable: false,
  key: '',
  img_base: '',
  piece_base: '',
  piece_y: 0,
  piece_width: 55,
  piece_height: 48,
  bg_width: 320,
  bg_height: 160,
})

/** 滑块验证是否已通过（后端返回 verified=true 后置位） */
const sliderPassed = ref(false)

/** 从本地存储恢复记住的用户名（仅用户名，不存储密码） */
function restoreRememberedUser() {
  const remembered = Storage.get<{ username: string, remember: boolean }>(REMEMBER_ME_KEY)
  if (remembered) {
    loginFormData.username = remembered.username || ''
    loginFormData.remember = remembered.remember ?? true
  }
}

async function getLoginCaptcha() {
  try {
    const result = await AuthAPI.getCaptcha()
    if (result && typeof result === 'object') {
      captchaState.enable = Boolean(result.enable)
      captchaState.key = result.key || ''
      captchaState.img_base = result.img_base || ''
      captchaState.piece_base = result.piece_base || ''
      captchaState.piece_y = result.piece_y ?? 0
      captchaState.piece_width = result.piece_width ?? 55
      captchaState.piece_height = result.piece_height ?? 48
      captchaState.bg_width = result.bg_width ?? 320
      captchaState.bg_height = result.bg_height ?? 160
      sliderPassed.value = false
      if (captchaState.enable) {
        loginFormData.captcha_key = captchaState.key
        // 重置滑块到初始状态
        resetSliderCaptcha()
      }
    }
    else {
      captchaState.enable = false
    }
  }
  catch (e) {
    console.error('验证码获取失败', e)
    captchaState.enable = false
  }
}

/**
 * wd-slide-verify 拖动到终点触发 success — 调用后端 slider_complete 接口标记验证完成
 * 后端仅标记 captcha_key 状态为 verified，不校验 x 坐标
 */
async function handleSliderSuccess(position: number) {
  if (!captchaState.key) {
    uni.showToast({ title: t('login.captchaExpired'), icon: 'none' })
    sliderCaptchaRef.value?.reset?.()
    return
  }

  try {
    const result = await AuthAPI.completeSliderCaptcha({
      captcha_key: captchaState.key,
      position,
    })
    if (result?.verified) {
      sliderPassed.value = true
      loginFormData.captcha = 'verified' // 占位值，后端只校验 captcha_key 状态
      captchaVisible.value = false
      await doLogin()
    }
    else {
      uni.showToast({ title: t('login.sliderFailed'), icon: 'none' })
      sliderCaptchaRef.value?.reset?.()
    }
  }
  catch (e) {
    console.error('滑块验证失败', e)
    uni.showToast({ title: t('login.sliderFailed'), icon: 'none' })
    sliderCaptchaRef.value?.reset?.()
    void getLoginCaptcha()
  }
}

/** 重置滑块验证状态并清空占位验证值（验证码刷新 / 拖动未到终点触发 fail 时） */
function resetSliderCaptcha() {
  sliderPassed.value = false
  loginFormData.captcha = ''
  sliderCaptchaRef.value?.reset?.()
}

onLoad((options) => {
  const from = options?.redirect ? decodeURIComponent(options.redirect) : ''
  // 安全验证：仅允许本地页面路径，防止开放重定向攻击
  if (from && from !== '/pages/login/index' && from.startsWith('/pages/')) {
    redirect.value = from
  }
  restoreRememberedUser()
  getLoginCaptcha()
  // 拉取系统参数（品牌区 logo/标题/副标题），幂等 + 本地持久化缓存
  configStore.getConfig()
})

/**
 * 自定义导航栏由页面承接状态栏：根组件 onShow 会按浅色主题把状态栏前景写成黑色，
 * 这里在页面 onShow 再拉回白色，避免深色品牌区顶部出现黑字状态栏。
 */
onShow(() => {
  // #ifndef H5
  uni.setNavigationBarColor({ frontColor: '#ffffff', backgroundColor: '#3548C8' })
  // #endif
})

/** 登录提交 — 字段验证 → 需要时弹出安全验证 → 自动登录 */
async function handleSubmit() {
  if (loading.value)
    return

  const { valid } = await loginFormRef.value.validate()
  if (!valid)
    return

  if (captchaState.enable && !sliderPassed.value) {
    openCaptcha()
    return
  }

  await doLogin()
}

/** 打开安全验证：每次打开都取一张新验证码，避免 60 秒过期 */
async function openCaptcha() {
  captchaVisible.value = true
  await getLoginCaptcha()
}

/** 实际登录请求 */
async function doLogin() {
  loading.value = true
  try {
    await userStore.login(loginFormData)
    // 登录成功后处理记住密码：仅存储用户名，不存储密码
    if (loginFormData.remember) {
      Storage.set(REMEMBER_ME_KEY, { username: loginFormData.username, remember: true })
    }
    else {
      Storage.remove(REMEMBER_ME_KEY)
    }
    uni.reLaunch({ url: redirect.value })
  }
  catch {
    uni.showToast({ title: t('login.loginFailed'), icon: 'none', duration: 2500 })
    // 登录失败后自动刷新验证码并重置滑块
    if (captchaState.enable) {
      void getLoginCaptcha()
      captchaVisible.value = true
    }
  }
  finally {
    loading.value = false
  }
}

/** 跳转注册页 */
function goRegister() {
  uni.navigateTo({ url: '/pages/login/register/index' })
}

/** 跳转忘记密码页 */
function goForget() {
  uni.navigateTo({ url: '/pages/login/forget/index' })
}

/** 第三方 OAuth 登录 */
async function handleOAuth(provider: OAuthProvider) {
  try {
    const result = await AuthAPI.getOAuthLoginUrl(provider)
    if (result?.url) {
      // #ifdef H5
      window.location.href = result.url
      // #endif
      // #ifdef MP-WEIXIN
      uni.setClipboardData({
        data: result.url,
        success: () => {
          uni.showToast({ title: t('login.oauthCopyTip'), icon: 'none' })
        },
      })
      // #endif
    }
  }
  catch {
    uni.showToast({ title: t('login.oauthFailed'), icon: 'none' })
  }
}
</script>

<template>
  <view class="login-page">
    <!-- 品牌头部：从导航栏延续下来的满幅渐变，作为整页的构图起点 -->
    <view class="login-hero">
      <text class="login-hero__monogram" aria-hidden="true">F</text>
      <view class="login-hero__brand">
        <view class="brand-mark" aria-hidden="true">
          <image class="brand-mark__logo" :src="brandLogo" mode="aspectFit" />
        </view>
        <view class="brand-copy">
          <text class="brand-copy__name">{{ brandTitle }}</text>
          <text class="brand-copy__line">{{ brandSubtitle }}</text>
        </view>
      </view>
    </view>

    <!-- 表单面板：白色圆角上沿轻轻叠在品牌区上，成为页面下半部的“纸面” -->
    <view class="login-panel">
      <view class="login-panel__head">
        <text class="login-panel__title" aria-role="heading" aria-level="1">{{ t('login.cardTitle') }}</text>
        <text class="login-panel__subtitle">{{ t('login.cardSubtitle') }}</text>
      </view>

      <wd-form ref="loginFormRef" :model="loginFormData" :schema="loginSchema" class="login-form">
        <view class="form-field">
          <text class="form-field__label">{{ t('common.form.username') }}</text>
          <wd-form-item prop="username" title-width="0" custom-style="margin: 0; padding: 0;">
            <wd-input
              v-model="loginFormData.username"
              :aria-label="t('common.form.username')"
              :placeholder="t('common.form.usernamePlaceholder')"
              clearable
              confirm-type="next"
              :compact="false"
              prefix-icon="user"
              @confirm="handleSubmit"
            />
          </wd-form-item>
        </view>

        <view class="form-field form-field--last">
          <text class="form-field__label">{{ t('common.form.password') }}</text>
          <wd-form-item prop="password" title-width="0" custom-style="margin: 0; padding: 0;">
            <wd-input
              v-model="loginFormData.password"
              :aria-label="t('common.form.password')"
              :placeholder="t('common.form.passwordPlaceholder')"
              clearable
              show-password
              confirm-type="go"
              :compact="false"
              prefix-icon="lock"
              @confirm="handleSubmit"
            />
          </wd-form-item>
        </view>
      </wd-form>

      <!-- 记住密码 + 忘记密码 -->
      <view class="login-options">
        <wd-checkbox v-model="loginFormData.remember" size="18px">
          {{ t('login.remember') }}
        </wd-checkbox>
        <view
          class="tap-target login-forgot"
          aria-role="button"
          :aria-label="t('login.forgot')"
          tabindex="0"
          @click="goForget"
          @keyup.enter="goForget"
        >
          <text class="login-forgot__text">{{ t('login.forgot') }}</text>
        </view>
      </view>

      <!-- 唯一主 CTA -->
      <wd-button
        class="login-submit"
        type="primary"
        :loading="loading"
        block
        @click="handleSubmit"
      >
        <text class="login-submit__text" style="color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important;">{{ loading ? t('login.submitting') : t('login.submit') }}</text>
      </wd-button>

      <!-- 第三方登录：低饱和，不与主 CTA 抢层级 -->
      <view class="login-oauth">
        <view class="login-oauth__head">
          <view class="login-oauth__rule" />
          <text class="login-oauth__title">{{ t('login.thirdParty') }}</text>
          <view class="login-oauth__rule" />
        </view>
        <view class="login-oauth__row">
          <view
            class="oauth-item"
            hover-class="oauth-item--pressed"
            aria-role="button"
            :aria-label="t('login.wechat')"
            tabindex="0"
            @click="handleOAuth('wechat')"
            @keyup.enter="handleOAuth('wechat')"
          >
            <view class="oauth-item__icon" style="background-color: #07C160">
              <image class="oauth-item__img" src="/static/icons/wechat.svg" mode="aspectFit" />
            </view>
            <text class="oauth-item__label">{{ t('login.wechat') }}</text>
          </view>
          <view
            class="oauth-item"
            hover-class="oauth-item--pressed"
            aria-role="button"
            :aria-label="t('login.qq')"
            tabindex="0"
            @click="handleOAuth('qq')"
            @keyup.enter="handleOAuth('qq')"
          >
            <view class="oauth-item__icon" style="background-color: #12B7F5">
              <image class="oauth-item__img" src="/static/icons/qq.svg" mode="aspectFit" />
            </view>
            <text class="oauth-item__label">{{ t('login.qq') }}</text>
          </view>
          <view
            class="oauth-item"
            hover-class="oauth-item--pressed"
            aria-role="button"
            :aria-label="t('login.gitee')"
            tabindex="0"
            @click="handleOAuth('gitee')"
            @keyup.enter="handleOAuth('gitee')"
          >
            <view class="oauth-item__icon" style="background-color: #C71D23">
              <image class="oauth-item__img" src="/static/icons/gitee.svg" mode="aspectFit" />
            </view>
            <text class="oauth-item__label">{{ t('login.gitee') }}</text>
          </view>
          <view
            class="oauth-item"
            hover-class="oauth-item--pressed"
            aria-role="button"
            :aria-label="t('login.github')"
            tabindex="0"
            @click="handleOAuth('github')"
            @keyup.enter="handleOAuth('github')"
          >
            <view class="oauth-item__icon" style="background-color: #24292F">
              <image class="oauth-item__img" src="/static/icons/github.svg" mode="aspectFit" />
            </view>
            <text class="oauth-item__label">{{ t('login.github') }}</text>
          </view>
        </view>
      </view>

      <view class="login-footer">
        <text class="login-footer__text">{{ t('login.noAccount') }}</text>
        <view
          class="tap-target login-footer__link"
          aria-role="button"
          :aria-label="t('login.toRegister')"
          tabindex="0"
          @click="goRegister"
          @keyup.enter="goRegister"
        >
          <text class="login-footer__link-text">{{ t('login.toRegister') }}</text>
        </view>
      </view>
    </view>

    <!-- 安全验证弹层：点击登录后出现，验证码按需生成，避免长时间未操作过期 -->
    <wd-popup
      v-model="captchaVisible"
      position="bottom"
      :safe-area-inset-bottom="true"
      custom-style="border-radius: 28rpx 28rpx 0 0; padding: 28rpx 32rpx calc(28rpx + env(safe-area-inset-bottom)); background: var(--wot-bg-filled-content, #FFFFFF);"
    >
      <view class="captcha-popup">
        <view class="captcha-popup__grabber" aria-hidden="true" />
        <view class="captcha-popup__head">
          <view class="captcha-popup__titles">
            <text class="captcha-popup__title">{{ t('login.securityVerify') }}</text>
            <text class="captcha-popup__tip">{{ t('login.securityVerifyTip') }}</text>
          </view>
          <view
            class="tap-target captcha-popup__close"
            aria-role="button"
            :aria-label="t('common.close')"
            @click="captchaVisible = false"
          >
            <wd-icon name="close" size="20px" />
          </view>
        </view>
        <FaPuzzleCaptcha
          ref="sliderCaptchaRef"
          :bg-image="captchaState.img_base"
          :piece-image="captchaState.piece_base"
          :piece-y="captchaState.piece_y"
          :piece-width="captchaState.piece_width"
          :piece-height="captchaState.piece_height"
          :bg-width="captchaState.bg_width"
          :bg-height="captchaState.bg_height"
          :passed="sliderPassed"
          :loading="loading"
          :text="t('login.puzzleText')"
          :success-text="t('login.sliderSuccessText')"
          @verify="handleSliderSuccess"
          @refresh="getLoginCaptcha"
        />
      </view>
    </wd-popup>
  </view>
</template>

<style lang="scss" scoped>
/* ============================================================
   登录页构图：品牌渐变头部（与导航栏同色，满幅） + 上叠的白色表单面板
   所有高度预算按 390×844（自定义导航，整页 844px）校准，
   一屏不滚动；小屏用 max-height 断点收紧，极矮屏才允许滚动。
   ============================================================ */
.login-page {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  /* 自定义导航栏：页面从屏幕最顶部开始，品牌区直接承接状态栏氛围 */
  /* #ifdef H5 */
  height: 100vh;
  height: 100dvh;
  /* #endif */
  /* #ifndef H5 */
  height: 100vh;
  /* #endif */
  overflow-x: hidden;
  overflow-y: auto;
  background: #FFFFFF;
  box-sizing: border-box;
  -webkit-tap-highlight-color: transparent;

  &::-webkit-scrollbar {
    width: 0;
    height: 0;
  }
}

/* ===== Brand hero ===== */
.login-hero {
  position: relative;
  z-index: 1;
  flex: 0 0 276px;
  width: 100%;
  padding: 36px 24px 0;
  overflow: hidden;
  box-sizing: border-box;
  color: #FFFFFF;
  background-color: #3548C8;
  background-image:
    radial-gradient(70% 52% at 92% 88%, rgb(255 255 255 / 14%) 0%, rgb(255 255 255 / 0%) 66%),
    linear-gradient(180deg, #3548C8 0%, #4155DE 62%, #6D5BFF 100%);

  /* 品牌字母水印：只作为氛围，不承载信息 */
  &__monogram {
    position: absolute;
    top: -18px;
    right: -10px;
    z-index: 0;
    font-family: Inter, 'SF Pro Display', system-ui, sans-serif;
    font-size: 212px;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.08em;
    color: rgb(255 255 255 / 7%);
    pointer-events: none;
    user-select: none;
  }

  &__brand {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 14px;
    max-width: 100%;
    margin-top: 94px;
    animation: login-brand-in 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) both;
  }
}

.brand-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 58px;
  height: 58px;
  padding: 4px;
  flex-shrink: 0;
  box-sizing: border-box;
  background: #FFFFFF;
  border-radius: 18px;
  box-shadow: 0 12px 26px rgb(23 32 90 / 28%);

  &__logo {
    display: block;
    width: 50px;
    height: 50px;
    border-radius: 15px;
  }
}

.brand-copy {
  display: flex;
  flex-direction: column;
  min-width: 0;

  &__name {
    display: block;
    overflow: hidden;
    font-size: 23px;
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.015em;
    color: #FFFFFF;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__line {
    display: -webkit-box;
    overflow: hidden;
    max-width: 244px;
    margin-top: 5px;
    font-size: 12px;
    font-weight: 400;
    line-height: 1.45;
    color: rgb(255 255 255 / 92%);
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    word-break: break-word;
  }
}

/* ===== Form sheet ===== */
.login-panel {
  position: relative;
  z-index: 2;
  display: flex;
  flex: 1;
  flex-direction: column;
  width: 100%;
  min-height: 0;
  margin-top: -26px;
  padding: 26px 24px calc(14px + env(safe-area-inset-bottom));
  box-sizing: border-box;
  background: #FFFFFF;
  border-radius: 28px 28px 0 0;
  box-shadow: 0 -12px 34px rgb(24 34 92 / 16%);
  animation: login-panel-in 0.55s cubic-bezier(0.2, 0.8, 0.2, 1) both;

  &__head {
    flex-shrink: 0;
    margin-bottom: 22px;
  }

  &__title {
    display: block;
    font-size: 26px;
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.02em;
    color: #111827;
  }

  &__subtitle {
    display: block;
    margin-top: 6px;
    font-size: 13px;
    line-height: 1.45;
    color: #5B6472;
  }
}

/* 入场只做一次轻微上浮，避免登录页的第一帧是一次硬切换 */
@keyframes login-brand-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes login-panel-in {
  from {
    opacity: 0;
    transform: translateY(16px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ===== Form fields ===== */
.login-form {
  flex-shrink: 0;
}

.form-field {
  margin-bottom: 14px;

  &--last {
    margin-bottom: 0;
  }

  &__label {
    display: block;
    margin: 0 0 6px 2px;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.5;
    letter-spacing: 0.01em;
    color: #4B5563;
  }
}

/* 去掉 wd-form-item 的 cell 外壳，让输入框直接落在面板网格上 */
.login-form :deep(.wd-form-item) {
  margin: 0;
  padding: 0;
}

.login-form :deep(.wd-form-item .wd-cell) {
  --wot-cell-bg: transparent;

  padding: 0;
}

/* MP 端插槽静态判定会渲染空 left 列，隐藏后输入框才能满宽 */
.login-form :deep(.wd-form-item .wd-cell__left) {
  display: none;
}

.login-form :deep(.wd-form-item .wd-cell__right) {
  flex: 1;
  min-width: 0;
}

.login-form :deep(.wd-form-item .wd-cell__value) {
  width: 100%;
}

.login-form :deep(.wd-form-item__error-message) {
  margin: 5px 0 0 2px;
  font-size: 12px;
  line-height: 1.4;
  color: #D92D20;
}

/* 输入框：软色块 + 无边框，聚焦时出现品牌描边，触控高度 50px */
.login-form :deep(.wd-input) {
  --wot-input-bg: transparent;
  --wot-input-inner-height: 24px;
  --wot-input-inner-font-size: 15px;
  --wot-input-inner-color: #111827;
  --wot-input-inner-placeholder-color: #5B6472;
  --wot-input-icon-color: #6B7280;
  --wot-input-icon-font-size: 18px;
  --wot-input-icon-margin: 10px;

  height: 50px;
  padding: 0 14px;
  box-sizing: border-box;
  background: #F4F6FB;
  border: 1px solid transparent;
  border-radius: 14px;
  transition: background-color 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
}

.login-form :deep(.wd-input__prefix) {
  color: #4F6BFF;
}

.login-form :deep(.wd-input__prefix .wd-input__icon) {
  color: #4F6BFF;
}

.login-form :deep(.wd-input__inner) {
  caret-color: #4F6BFF;
}

/* 密码可见 / 清空图标：视觉保持 18px，点击热区扩到 44px；
   -8px 让图标视觉中心仍贴近输入框右侧，不因热区变大而显得内缩 */
.login-form :deep(.wd-input__suffix) {
  display: flex;
  align-items: center;
  height: 44px;
  min-height: 44px;
  margin-right: -8px;
}

.login-form :deep(.wd-input__suffix .wd-input__icon),
.login-form :deep(.wd-input__clear) {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  box-sizing: border-box;
}

/* #ifdef H5 */
.login-form :deep(.wd-input:focus-within) {
  background: #FFFFFF;
  border-color: #4F6BFF;
  box-shadow: 0 0 0 3px rgb(79 107 255 / 12%);
}
/* #endif */

/* ===== Remember / Forgot ===== */
.login-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 44px;
  margin: 2px 0 14px;
  flex-shrink: 0;

  :deep(.wd-checkbox) {
    --wot-checkbox-icon-size: 18px;
    --wot-checkbox-label-font-size: 13px;
    --wot-checkbox-label-color: #4B5563;
    --wot-checkbox-label-margin: 8px;
    --wot-checkbox-unchecked-color: #6B7280;

    min-height: 44px;
  }
}

.login-forgot {
  margin-right: -8px;

  &__text {
    font-size: 13px;
    font-weight: 600;
    color: #3D55E0;
  }
}

/* ===== Primary CTA ===== */
.login-submit {
  flex-shrink: 0;
  margin-bottom: 18px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 52px;
  padding: 0 20px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: #FFFFFF;
  background: linear-gradient(135deg, #4055E6 0%, #5A49E0 100%);
  border: none;
  border-radius: 14px;
  box-shadow: 0 10px 24px rgb(64 85 230 / 26%);
}

.login-submit__text {
  color: #FFFFFF;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.login-submit.wd-button {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 52px;
  padding: 0 20px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: #FFFFFF;
  background: linear-gradient(135deg, #4055E6 0%, #5A49E0 100%);
  border: none;
  border-radius: 14px;
  box-shadow: 0 10px 24px rgb(64 85 230 / 26%);
}

.login-submit:active {
  background: linear-gradient(135deg, #3448D0 0%, #4B3BC8 100%);
  box-shadow: 0 6px 16px rgb(64 85 230 / 22%);
}

/* H5 键盘焦点：登录页的辅助入口也要有可见焦点 */
/* #ifdef H5 */
.login-submit:focus-visible {
  outline: 2px solid #1B2559;
  outline-offset: 3px;
}

.tap-target:focus-visible,
.oauth-item:focus-visible {
  outline: 2px solid var(--fa-brand-blue, #4F6BFF);
  outline-offset: 2px;
}
/* #endif */

/* ===== Third-party ===== */
.login-oauth {
  flex-shrink: 0;
  margin-top: 14px;

  &__head {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  &__rule {
    flex: 1;
    height: 1px;
    background: #ECEEF3;
  }

  &__title {
    flex-shrink: 0;
    font-size: 12px;
    font-weight: 500;
    line-height: 16px;
    letter-spacing: 0.04em;
    color: #5B6472;
  }

  &__row {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: space-between;
    margin-top: 10px;
  }
}

.oauth-item {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-width: 44px;
  min-height: 44px;
  padding: 0 2px;
  box-sizing: border-box;
  border-radius: 12px;
  transition: opacity 0.15s ease;

  &--pressed {
    opacity: 0.62;
  }

  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }

  &__img {
    display: block;
    width: 22px;
    height: 22px;
  }

  &__label {
    margin-top: 6px;
    font-size: 12px;
    line-height: 16px;
    color: #5B6472;
  }
}

/* ===== Footer ===== */
.login-footer {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 2px;
  min-height: 44px;
  margin-top: auto;
  flex-shrink: 0;

  &__text {
    font-size: 13px;
    line-height: 1.4;
    color: #5B6472;
  }

  &__link {
    margin-right: -8px;

    &-text {
      font-size: 13px;
      font-weight: 600;
      line-height: 1.4;
      color: #3D55E0;
    }
  }
}

/* ===== Dark mode ===== */
.wot-theme-dark .login-page {
  background: #101216;
}

.wot-theme-dark .login-panel {
  background: #15181E;
  box-shadow: 0 -12px 34px rgb(0 0 0 / 42%);

  .login-panel__title {
    color: #F3F4F6;
  }

  .login-panel__subtitle {
    color: #A3AAB8;
  }
}

.wot-theme-dark .form-field__label {
  color: #A3AAB8;
}

.wot-theme-dark .login-form :deep(.wd-input) {
  --wot-input-inner-color: #F3F4F6;
  --wot-input-inner-placeholder-color: #8B93A1;

  background: #1D222B;
  border-color: #262B34;
}

/* #ifdef H5 */
.wot-theme-dark .login-form :deep(.wd-input:focus-within) {
  background: #1A2029;
  border-color: #6D8BFF;
  box-shadow: 0 0 0 3px rgb(109 139 255 / 16%);
}
/* #endif */

.wot-theme-dark .login-options :deep(.wd-checkbox) {
  --wot-checkbox-label-color: #A3AAB8;
  --wot-checkbox-unchecked-color: #8A94A6;
}

/* 暗色下默认错误红 #D92D20 在 #15181E 上只有 3.68:1，提到 AA */
.wot-theme-dark .login-form :deep(.wd-form-item__error-message) {
  color: #FF8A80;
}

.wot-theme-dark .login-forgot__text,
.wot-theme-dark .login-footer__link-text {
  color: #9BB0FF;
}

.wot-theme-dark .login-oauth__rule {
  background: #262B34;
}

.wot-theme-dark .login-oauth__title,
.wot-theme-dark .oauth-item__label,
.wot-theme-dark .login-footer__text {
  color: #A3AAB8;
}

/* GitHub 的深色圆在暗色面板上容易和背景融在一起，加一圈极淡的内描边 */
.wot-theme-dark .oauth-item__icon {
  box-shadow: inset 0 0 0 1px rgb(255 255 255 / 14%);
}

/* ===== 小屏收紧（高度断点，不改横向布局） ===== */
@media (max-width: 360px) {
  .brand-copy__line {
    max-width: 190px;
  }
}

@media (max-height: 820px) {
  .login-hero {
    flex-basis: 246px;
    padding-top: 28px;
  }

  .login-hero__brand {
    margin-top: 84px;
  }

  .login-hero__monogram {
    font-size: 188px;
  }

  .login-panel {
    margin-top: -22px;
    padding-top: 22px;
    border-radius: 24px 24px 0 0;
  }

  .login-panel__head {
    margin-bottom: 18px;
  }

  .login-panel__title {
    font-size: 24px;
  }

  .form-field {
    margin-bottom: 10px;
  }

  .login-form :deep(.wd-input) {
    height: 48px;
  }

  .login-options {
    margin-bottom: 10px;
  }

  .login-submit {
    margin-bottom: 14px;
  }

  .login-oauth__row {
    margin-top: 8px;
  }

  .oauth-item__icon {
    width: 36px;
    height: 36px;
  }
}

@media (max-height: 800px) {
  .login-hero {
    flex-basis: 208px;
    padding-top: 20px;
  }

  .login-hero__brand {
    margin-top: 60px;
  }

  .brand-mark {
    width: 50px;
    height: 50px;
    border-radius: 15px;
  }

  .brand-mark__logo {
    width: 42px;
    height: 42px;
    border-radius: 12px;
  }

  .brand-copy__name {
    font-size: 21px;
  }

  .login-panel {
    margin-top: -20px;
    padding-top: 20px;
    padding-bottom: calc(10px + env(safe-area-inset-bottom));
  }

  .login-panel__title {
    font-size: 23px;
  }

  .login-panel__head {
    margin-bottom: 12px;
  }

  .login-panel__subtitle {
    margin-top: 4px;
    font-size: 12px;
  }

  .login-form :deep(.wd-input) {
    height: 46px;
  }

  .login-options {
    margin-bottom: 8px;
  }

  .login-submit {
    margin-bottom: 12px;
  }

  .login-submit.wd-button {
    height: 50px;
  }

  .login-oauth__row {
    margin-top: 6px;
  }

  .login-oauth__head {
    gap: 10px;
  }

  .oauth-item__icon {
    width: 34px;
    height: 34px;
  }

  .oauth-item__label {
    margin-top: 4px;
  }
}

/* 极矮屏（<600px）不再硬挤：允许页面自然滚动，保证元素不被压扁 */
@media (max-height: 600px) {
  .login-page {
    height: auto;
    min-height: 100vh;
    overflow-y: auto;
  }

  .login-hero {
    flex: 0 0 198px;
  }
}

/* H5 桌面/平板：保留移动端构图，不把 390 的纸面拉成整屏表单 */
@media (min-width: 600px) {
  .login-page {
    width: 430px;
    height: 844px;
    max-height: 100vh;
    /* 用 top 位移而不是上下 margin：避免 margin 折叠把 body 整体顶下去，产生 28px 多余滚动 */
    margin: 0 auto;
    top: max(0px, calc((100vh - 844px) / 2));
    border-radius: 28px;
    box-shadow:
      0 0 0 1px rgb(17 24 39 / 6%),
      0 0 0 100vmax #EEF2FB;
  }

  .login-hero {
    border-radius: 28px 28px 0 0;
  }

  .wot-theme-dark .login-page {
    box-shadow:
      0 0 0 1px rgb(255 255 255 / 8%),
      0 0 0 100vmax #090B0F;
  }
}

/* 动效尊重系统偏好；关闭后页面仍以最终态直接出现 */
@media (prefers-reduced-motion: reduce) {
  .login-hero__brand,
  .login-panel {
    animation: none;
  }
}

/* 安全验证弹层 */
.captcha-popup {
  width: 100%;
  padding-top: 2px;

  &__grabber {
    width: 36px;
    height: 4px;
    margin: 0 auto 16px;
    background: #E6E8EC;
    border-radius: 999px;
  }

  &__head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 12px;
  }

  &__titles {
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
  }

  &__title {
    font-size: 19px;
    font-weight: 600;
    line-height: 1.35;
    color: #111827;
  }

  &__tip {
    font-size: 12px;
    line-height: 1.5;
    color: #5B6472;
  }

  &__close {
    margin: -10px -8px 0 0;
    color: #5B6472;
  }

  :deep(.fa-puzzle) {
    margin: 4px auto 0;
  }
}

.wot-theme-dark .captcha-popup {
  &__grabber {
    background: #2C313A;
  }

  &__title {
    color: #F3F4F6;
  }

  &__tip,
  &__close {
    color: #A3AAB8;
  }
}
</style>
