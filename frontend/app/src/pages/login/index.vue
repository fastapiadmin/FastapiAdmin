<script lang="ts" setup>
import type { CaptchaInfo, LoginFormData } from '@/api/auth'
import { onLoad } from '@dcloudio/uni-app'
import { onMounted, reactive, ref } from 'vue'
import { useToast } from 'wot-design-uni'
import AuthAPI from '@/api/auth'
import { useUserStore } from '@/store/userStore'

definePage({
  name: 'login',
  style: {
    navigationBarTitleText: '登录',
  },
})

// 主题相关
const loginFormRef = ref()
const toast = useToast()
const loading = ref(false)
const userStore = useUserStore()

// 登录表单数据
const loginFormData = reactive<LoginFormData>({
  username: 'admin',
  password: '123456',
  captcha: '',
  captcha_key: '',
  remember: true,
  login_type: '移动端',
})

// 验证码状态
const captchaState = reactive<CaptchaInfo>({
  enable: false,
  key: '',
  img_base: '',
})

// 防重复请求标志
const isCaptchaLoading = ref(false)

// 获取验证码
async function getLoginCaptcha() {
  if (isCaptchaLoading.value) {
    return
  }

  isCaptchaLoading.value = true
  try {
    const result = await AuthAPI.getCaptcha()

    if (result && typeof result === 'object') {
      captchaState.enable = Boolean(result.enable)
      captchaState.key = result.key || ''
      captchaState.img_base = result.img_base || result.img || ''
      if (captchaState.enable) {
        loginFormData.captcha = ''
        loginFormData.captcha_key = captchaState.key
      }
    }
    else {
      captchaState.enable = false
    }
  }
  catch (error: any) {
    console.error('获取验证码失败:', error)
    toast.error(error?.message || '验证码获取失败')
    captchaState.img_base = ''
    captchaState.enable = false
  }
  finally {
    isCaptchaLoading.value = false
  }
}

// 仅使用 query 作为重定向来源
const redirect = ref('/pages/index/index')

// 页面加载时初始化
onLoad((options) => {
  uni.setNavigationBarTitle({ title: '登录' })

  // 处理重定向逻辑
  const fromQuery
    = options && options.redirect ? decodeURIComponent(options.redirect) : ''
  if (fromQuery && fromQuery !== '/pages/login/index') {
    redirect.value = fromQuery
  }

  // 获取验证码
  getLoginCaptcha()
})

// 页面挂载时确保验证码正确显示
onMounted(() => {
  // 如果验证码未启用或未获取到，重新获取
  setTimeout(() => {
    if (!captchaState.enable || !captchaState.img_base) {
      getLoginCaptcha()
    }
    // 强制清除输入框背景色，优化视觉效果
    const inputs = document.querySelectorAll('input')
    inputs.forEach((input) => {
      input.style.backgroundColor = 'transparent'
      input.style.boxShadow = 'none'
    })
  }, 100)
})

// 账号密码登录
async function handleSubmit() {
  try {
    const { valid, errors } = await loginFormRef.value.validate()
    if (!valid)
      return toast.error(errors[0].message)

    loading.value = true
    await userStore.login(loginFormData)
    toast.success('登录成功')

    // 登录成功后跳转到指定页面
    setTimeout(() => {
      uni.reLaunch({
        url: redirect.value,
        success: () => toast.success('跳转成功'),
        fail: err => toast.error(`跳转失败: ${err.errMsg}`),
      })
    }, 500)
  }
  catch (error: any) {
    toast.error(error?.message || '登录失败')
    getLoginCaptcha() // 刷新验证码
  }
  finally {
    loading.value = false
  }
}

// 忘记密码
async function handleForgotPassword() {
  toast.error('忘记密码功能开发中...')
}

// 注册账号
async function handleRegister() {
  toast.error('注册账号功能开发中...')
}
</script>

<template>
  <view class="app-container">
    <!-- 背景图 -->
    <wd-img
      src="/static/images/login-bg.svg"
      mode="aspectFill"
      class="login-bg"
    />

    <view class="login-card">
      <!-- Logo和标题区域 -->
      <view class="header">
        <wd-img src="/static/logo.png" class="logo" mode="aspectFit" />
        <text class="title theme-text-inverse">
          FastApp管理系统
        </text>
        <text class="subtitle theme-text-inverse">
          欢迎使用移动端管理平台
        </text>
      </view>

      <!-- 登录表单区域 -->
      <wd-form
        ref="loginFormRef"
        :model="loginFormData"
        class="login-form"
      >
        <wd-cell-group border class="form-group">
          <wd-input
            v-model="loginFormData.username"
            label="账号"
            label-width="100px"
            prefix-icon="user"
            type="text"
            prop="username"
            placeholder="请输入账号"
            clearable
            center
            clear-trigger="focus"
            :rules="[{ required: true, message: '请输入账号' }]"
          />
          <wd-input
            v-model="loginFormData.password"
            label="密码"
            label-width="100px"
            prefix-icon="lock-on"
            type="text"
            prop="password"
            show-password
            placeholder="请输入密码"
            clear-trigger="focus"
            clearable
            center
            :rules="[{ required: true, message: '请输入密码' }]"
          />
          <!-- 验证码输入框 -->
          <view v-if="captchaState.enable" class="captcha">
            <wd-input
              v-model="loginFormData.captcha"
              label="验证码"
              label-width="100px"
              prefix-icon="lock-on"
              class="captcha-input"
              type="text"
              prop="captcha"
              placeholder="请输入验证码"
              clear-trigger="focus"
              clearable
              center
              :rules="[{ required: true, message: '请输入验证码' }]"
            />
            <wd-img
              :src="captchaState.img_base"
              class="captcha-image"
              mode="aspectFit"
              @click="getLoginCaptcha"
            />
            <view
              v-if="!captchaState.img_base && captchaState.enable"
              @click="getLoginCaptcha"
            >
              <text>点击加载</text>
            </view>
          </view>

          <wd-divider />
          <!-- 忘记密码和注册账号 -->
          <view class="auth-links">
            <!-- 记住我 -->
            <view class="remember-me">
              <wd-checkbox v-model="loginFormData.remember">
                <wd-text size="24rpx" text="记住我" />
              </wd-checkbox>
            </view>

            <view class="forgot-password">
              <wd-text
                type="primary"
                text="忘记密码？"
                size="24rpx"
                @click="handleForgotPassword"
              />
            </view>
          </view>

          <!-- 登录按钮 -->
          <view class="footer">
            <wd-button
              type="primary"
              size="large"
              block
              class="login-button"
              :loading="loading"
              loading-size="24"
              @click="handleSubmit"
            >
              {{ loading ? "登录中..." : "账号登录" }}
            </wd-button>
          </view>

          <view class="register-link">
            <wd-text size="24rpx" text="您没有账号?" />
            <wd-text
              type="primary"
              text="注册账号"
              size="24rpx"
              @click="handleRegister"
            />
          </view>

          <!-- 版权信息 -->
          <view class="copyright">
            <wd-text
              text="Copyright © 2025-2026 service.fastapiadmin.com 版权所有 陕ICP备2025069493号-1"
              size="20rpx"
            />
          </view>
        </wd-cell-group>
      </wd-form>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.app-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;

  .login-bg {
    position: absolute;
    width: 100%;
    height: 100%;
  }

  .login-card {
    z-index: 2;
    margin-top: 40rpx;
    width: 92%;

    .header {
      z-index: 2;
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-top: 30rpx;

      .logo {
        width: 250rpx;
        height: 250rpx;
      }

      .title {
        margin-bottom: 20rpx;
        font-size: 48rpx;
        font-weight: bold;
        color: #ffffff;
      }

      .subtitle {
        font-size: 28rpx;
        color: #ffffff;
        text-align: center;
      }
    }

    .login-form {
      margin-top: 40rpx;
      padding: 24rpx;

      .form-group {
        padding: 24rpx;
      }

      .captcha {
        display: flex;
        align-items: center;
        margin-bottom: 40rpx;
      }

      .captcha-input {
        flex: 1;
        min-width: 0;
      }

      .captcha-image {
        width: 160rpx;
        height: 60rpx;
      }

      .footer {
        margin-top: 32rpx;
      }

      .auth-links {
        display: flex;
        justify-content: space-between;
        margin-top: 32rpx;
      }

      .register-link {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 32rpx;
      }

      .copyright {
        margin-top: 32rpx;
        text-align: center;
      }

    }
  }
}
</style>
