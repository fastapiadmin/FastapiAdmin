<script lang="ts" setup>
import type { FormSchema } from '@wot-ui/ui/components/wd-form/types'
import type { CaptchaInfo, LoginFormData, OAuthProvider } from '@/api/module_system/auth'
import { onLoad } from '@dcloudio/uni-app'
import { computed, nextTick, reactive, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import AuthAPI from '@/api/module_system/auth'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'
import { REMEMBER_ME_KEY } from '@/constants'
import { useConfigStore } from '@/store/configStore'
import { useUserStore } from '@/store/userStore'
import { Storage } from '@/utils/storage'

definePage({ name: 'login', style: { navigationBarTitleText: '登录' } })
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
    <!-- Brand area -->
    <view class="login-brand">
      <image class="brand-logo" :src="brandLogo" mode="aspectFit" />
      <view class="login-brand__text">
        <text class="brand-title">
          {{ brandTitle }}
        </text>
        <wd-text class="brand-subtitle" :text="brandSubtitle" />
      </view>
    </view>

    <!-- Form card -->
    <view class="login-card">
      <text class="login-card__title">
        {{ t('login.cardTitle') }}
      </text>

      <wd-form ref="loginFormRef" :model="loginFormData" :schema="loginSchema">
        <!-- Username — wot 原生 wd-input，前缀图标走 prefix-icon 属性 -->
        <text class="form-field-label">{{ t('common.form.username') }}</text>
        <wd-form-item prop="username" title-width="0" custom-style="margin-bottom: 14rpx; padding-left: 0; padding-right: 0;">
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

        <!-- Password — show-password 自动启用密码可见性切换 -->
        <text class="form-field-label">{{ t('common.form.password') }}</text>
        <wd-form-item prop="password" title-width="0" custom-style="margin-bottom: 14rpx; padding-left: 0; padding-right: 0;">
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


        <!-- 记住密码 + 忘记密码 -->
        <view class="login-options">
          <wd-checkbox v-model="loginFormData.remember" size="18px">
            {{ t('login.remember') }}
          </wd-checkbox>
          <view
            class="tap-target"
            aria-role="button"
            :aria-label="t('login.forgot')"
            @click="goForget"
          >
            <wd-text class="forgot-link" :text="t('login.forgot')" type="primary" />
          </view>
        </view>

        <!-- Submit -->
        <wd-button
          class="login-submit"
          type="primary"
          :loading="loading"
          block
          @click="handleSubmit"
        >
          {{ loading ? t('login.submitting') : t('login.submit') }}
        </wd-button>
      </wd-form>
    </view>

    <!-- OAuth Login -->
    <view class="oauth-section">
      <wd-divider>{{ t('login.thirdParty') }}</wd-divider>
      <wd-grid :column="4" clickable :gutter="10">
        <!-- WeChat -->
        <wd-grid-item aria-role="button" :aria-label="t('login.wechat')" @click="handleOAuth('wechat')">
          <view class="oauth-btn__icon" style="background: #07C160">
            <image class="oauth-btn__iconify" src="/static/icons/wechat.svg" />
          </view>
          <wd-text class="oauth-btn__label" :text="t('login.wechat')" />
        </wd-grid-item>

        <!-- QQ -->
        <wd-grid-item aria-role="button" :aria-label="t('login.qq')" @click="handleOAuth('qq')">
          <view class="oauth-btn__icon" style="background: #12B7F5">
            <image class="oauth-btn__iconify" src="/static/icons/qq.svg" />
          </view>
          <wd-text class="oauth-btn__label" :text="t('login.qq')" />
        </wd-grid-item>

        <!-- Gitee -->
        <wd-grid-item aria-role="button" :aria-label="t('login.gitee')" @click="handleOAuth('gitee')">
          <view class="oauth-btn__icon" style="background: #C71D23">
            <image class="oauth-btn__iconify" src="/static/icons/gitee.svg" />
          </view>
          <wd-text class="oauth-btn__label" :text="t('login.gitee')" />
        </wd-grid-item>

        <!-- GitHub -->
        <wd-grid-item aria-role="button" :aria-label="t('login.github')" @click="handleOAuth('github')">
          <view class="oauth-btn__icon" style="background: #24292F">
            <image class="oauth-btn__iconify" src="/static/icons/github.svg" />
          </view>
          <wd-text class="oauth-btn__label" :text="t('login.github')" />
        </wd-grid-item>
      </wd-grid>
    </view>

    <!-- Footer -->
    <view class="login-footer">
      <wd-text class="login-footer__text" :text="t('login.noAccount')" />
      <view class="tap-target" aria-role="button" :aria-label="t('login.toRegister')" @click="goRegister">
        <wd-text class="login-footer__link" :text="t('login.toRegister')" type="primary" />
      </view>
    </view>

    <!-- 安全验证弹层：点击登录后出现，验证码按需生成，避免长时间未操作过期 -->
    <wd-popup
      v-model="captchaVisible"
      position="bottom"
      :safe-area-inset-bottom="true"
      custom-style="border-radius: 24rpx 24rpx 0 0; padding: 28rpx 32rpx calc(28rpx + env(safe-area-inset-bottom));"
    >
      <view class="captcha-popup">
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
.login-page {
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
  padding: 24rpx 64rpx 0;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
  /* 接入全局水滴渐变（--drop-bg 由 App.vue 按主题色定义，暗色回退纯色由下方规则接管） */
  background: var(--drop-bg, #F9F9F9);
  overflow-x: hidden;
  overflow-y: auto;
  box-sizing: border-box;
}

/* 暗黑模式下整页背景变深，消除白色断层（wot 根类为 wot-theme-dark） */
.wot-theme-dark .login-page {
  @apply wot-bg-filled-bottom;
}

/* ===== Brand ===== */
.login-brand {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  padding-top: 8rpx;
  padding-bottom: 16rpx;
  gap: 20rpx;
  flex-shrink: 0;

  &__text {
    display: flex;
    flex-direction: column;
    gap: 2rpx;
    min-width: 0;
  }

  .brand-logo {
    width: 80rpx;
    height: 80rpx;
    flex-shrink: 0;
  }

  .brand-title {
    font-size: var(--font-xl, 40rpx);
    line-height: 1.15;
    font-weight: 700;
    /* 亮色下使用主题色渐变文字，品牌识别度更高（background-clip 不生效时回退主题主色） */
    background: linear-gradient(135deg, var(--fa-brand-blue, #4F6BFF) 0%, var(--fa-brand-violet, #6D5BFF) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--wot-primary-6, #1C64FD);

    /* 暗黑模式下使用纯白，提升品牌标题醒目度 */
    .wot-theme-dark & {
      background: none;
      -webkit-background-clip: initial;
      background-clip: initial;
      -webkit-text-fill-color: initial;
      color: #FFFFFF;
    }
  }

  .brand-subtitle {
    font-size: var(--font-xs, 24rpx);
    line-height: 1.3;
    @apply wot-text-text-auxiliary;

    /* 暗黑下提亮到 --text-color-2，避免 #9CA3AF 在深底上偏暗 */
    .wot-theme-dark & {
      @apply wot-text-text-secondary;
    }
  }
}

/* ===== Card（不再是毛玻璃，使用纯色背景 + 与页面背景形成层级差） ===== */
.login-card {
  width: 100%;
  /* 亮色下默认带主题色最浅阶，避免一片纯白；--card-bg-color 可被外部覆盖 */
  background: var(--card-bg-color, var(--wot-primary-1, #F5F8FF));
  border-radius: var(--fa-radius-md, 24rpx);
  padding: 24rpx;
  /* 与 Web 卡片一致：中性描边，不跟随主题色 */
  border: 2rpx solid var(--fa-border, #E6E8EC);
  box-shadow: var(--shadow-md, 0 8rpx 32rpx rgba(15, 23, 42, 0.04));
  margin-bottom: 12rpx;
  flex-shrink: 0;

  /* 暗黑模式：卡片用深色 2 级，页面背景用深色 1 级，形成细微层级差 */
  .wot-theme-dark & {
    @apply wot-bg-filled-content;
    border-color: var(--border-color, #2C2C2E);
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.2);
  }

  &__title {
    display: block;
    font-size: var(--font-lg, 32rpx);
    font-weight: 600;
    @apply wot-text-text-main;
    margin-bottom: 10rpx;

    /* 暗黑模式下使用纯白，提升卡片标题醒目度 */
    .wot-theme-dark & {
      color: #FFFFFF;
    }
  }
}

.login-submit :deep(.wd-button) {
  border-radius: var(--fa-radius-sm, 16rpx);
  height: 88rpx;
  font-size: var(--font-md, 28rpx);
}

.login-submit {
  border-radius: var(--fa-radius-sm, 16rpx);
}

/* 输入框微调 — 圆角加大 + 主题色边框 + 轻阴影，从"方方正正"变"圆润悬浮" */
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

/* cell 容器回归透明：亮色下消除输入框外围的白色方形区域，暗色下消除纯黑块，
   让自带圆角+边框的输入框直接显示在卡片上 */
:deep(.wd-cell) {
  --wot-cell-bg: transparent;
}

/* 滑块验证 — 滑块按钮默认纯白（filled-oppo）在浅灰轨道上不明显；同时整个滑块行
   默认浅灰底在淡主题色卡片上也几乎隐形，只有拖动时才变色。
   统一改为与输入框一致的"白底 + 主题色边框 + 轻阴影"浮层语言，静态即可见 */
:deep(.wd-slide-verify) {
  /* 整行容器：白底替代浅灰轨道，静态可见 */
  --wot-slide-verify-bg: #FFFFFF;
  /* 滑块按钮：主题色描边 + 图标，白底保留 */
  --wot-slide-verify-button-bg: #FFFFFF;
  --wot-slide-verify-button-border-color: var(--wot-primary-6, #1C64FD);
  --wot-slide-verify-button-color: var(--wot-primary-6, #1C64FD);
  --wot-slide-verify-button-shadow: 0 4rpx 12rpx rgba(15, 23, 42, 0.12);
  /* 与输入框呼应的边框 + 浮层阴影 */
  overflow: hidden;
  border: 2rpx solid var(--wot-primary-2, var(--wot-border-main, #EAECF0));
  border-radius: var(--fa-radius-sm, 16rpx);
  box-shadow: 0 4rpx 16rpx rgba(15, 23, 42, 0.05);
}

/* 成功文案默认隐藏：Wot 初始轨道宽度不为 0 时会从滑块两侧漏出 */
:deep(.wd-slide-verify__track-text) {
  opacity: 0;
}

:deep(.wd-slide-verify.is-success .wd-slide-verify__track-text) {
  opacity: 1;
}

.wot-theme-dark .login-page :deep(.wd-input) {
  /* 比卡片背景（filled-content）亮一档，输入框在暗色卡片上凸起有层次 */
  --wot-input-bg: var(--wot-coolgrey-8, var(--wot-filled-content));
  border-color: var(--wot-border-main, #2C2C2E);
  box-shadow: none;
}

.wot-theme-dark .login-page :deep(.wd-slide-verify) {
  /* 滑块行与按钮：默认纯黑（filled-oppo）/纯黑轨道在暗色下均不可见，
     统一改亮一档底色 + 主题色描边/图标，与输入框的暗色浮层语言一致 */
  --wot-slide-verify-bg: var(--wot-coolgrey-8, var(--wot-filled-content));
  --wot-slide-verify-button-bg: var(--wot-coolgrey-8, var(--wot-filled-content));
  --wot-slide-verify-button-border-color: var(--wot-primary-5, #4480FF);
  --wot-slide-verify-button-color: var(--wot-primary-5, #4480FF);
  --wot-slide-verify-button-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.4);
  border-color: var(--wot-border-main, #2C2C2E);
  box-shadow: none;
}

:deep(.wd-form-item) {
  margin-bottom: 14rpx;
  /* 去掉 wd-cell 自带左右内边距，使输入框/滑块与登录按钮同宽 */
  padding-left: 0;
  padding-right: 0;
}

/* ===== 记住密码 + 忘记密码 ===== */
.login-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8rpx;
}

.forgot-link {
  font-size: var(--font-md, 28rpx);
}

/* ===== OAuth Section ===== */
.oauth-section {
  width: 100%;
  margin-top: 0;
  flex-shrink: 0;

  :deep(.wd-divider) {
    margin: 8rpx 0;
  }

  /* 去掉宫格项默认填充背景，仅保留图标/文字与轻量点击反馈 */
  :deep(.wd-grid-item) {
    --wot-grid-item-bg: transparent;
  }
}

/* ===== 微信一键登录区域 ===== */
.wx-login-section {
  margin-bottom: 16rpx;

  :deep(.wd-button) {
    height: 88rpx;
    font-size: 30rpx;
  }
}

.oauth-btn__icon {
  width: 60rpx;
  height: 60rpx;
  border-radius: 30rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.oauth-btn__iconify {
  width: 40rpx;
  height: 40rpx;
}

.oauth-btn__label {
  font-size: 22rpx;
  @apply wot-text-text-auxiliary;
}

/* ===== Footer ===== */
.login-footer {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
  padding: 4rpx 0 0;
  flex-shrink: 0;

  &__text {
    font-size: var(--font-xs, 24rpx);
    @apply wot-text-text-auxiliary;
  }

  &__link {
    font-size: var(--font-xs, 24rpx);
  }
}

/* MP 端兼容：wd-form-item 内部 wd-cell 因 uni-app 插槽静态声明（u-s）误判 label/title 插槽被使用，
   showLeft=true 渲染空 left 区域（flex:1 占半宽），H5 端运行时插槽判定无此问题。
   本页 form-item 无 title/label/prefix 内容，隐藏 left 安全，保证输入框与登录按钮同宽 */
.login-card :deep(.wd-form-item .wd-cell__left) {
  display: none;
}

/* 紧凑登录：表单行距与验证码高度收紧，保证 390×844 一屏放得下 */
.login-card :deep(.wd-form-item) {
  margin-bottom: 8rpx;
}

/* 安全验证弹层 */
.captcha-popup {
  width: 100%;
  padding-top: 4rpx;

  &__head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16rpx;
    margin-bottom: 12rpx;
  }

  &__titles {
    display: flex;
    flex-direction: column;
    gap: 4rpx;
    min-width: 0;
  }

  &__title {
    font-size: var(--font-lg, 32rpx);
    font-weight: 600;
    @apply wot-text-text-main;
  }

  &__tip {
    font-size: var(--font-xs, 24rpx);
    @apply wot-text-text-auxiliary;
  }

  &__close {
    margin: -8rpx -8rpx 0 0;
    color: var(--wot-text-auxiliary);
  }

  :deep(.fa-puzzle) {
    margin: 4rpx auto 0;
  }
}
</style>
