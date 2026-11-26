<script lang="ts" setup>
import type { PasswordChangeForm } from '@/api/module_system/user'
import { useI18n } from 'vue-i18n'
import { formatMessage } from '@/locales/format'
import UserAPI from '@/api/module_system/user'
import { useGlobalDialog } from '@/composables/useGlobalDialog'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'
import { useShare } from '@/composables/useShare'
import { useTabbarActive } from '@/composables/useTabbarActive'
import { useTicketStats } from '@/composables/useTicketStats'
import { useUserStore } from '@/store/userStore'

const { t } = useI18n()

const userStore = useUserStore()
const userInfo = computed(() => userStore.userInfo)
const identityText = computed(() => {
  const username = userInfo.value?.username ? `@${userInfo.value.username}` : ''
  const role = userInfo.value?.roles?.map(item => item.name).filter(Boolean).join(', ')
  return [username, role].filter(Boolean).join(' · ') || t('mine.roleFallback')
})

useShare(() => ({
  title: formatMessage(t, 'mine.shareTitle', { name: userInfo.value?.name || t('common.admin') }),
  path: '/pages/index/index',
}))

definePage({
  name: 'mine',
  layout: 'tabbar',
  style: { navigationBarTitleText: '我的' },
})
useI18nNavTitle('mine.navTitle')

const router = useRouter()

function navigateTo(name: string) {
  router.push({ name })
}

const globalDialog = useGlobalDialog()

function handleLogout() {
  globalDialog.confirm({
    title: t('common.title'),
    msg: t('mine.logoutMsg'),
    confirmButtonText: t('mine.logoutConfirm'),
    success: (res) => {
      if (res.action === 'confirm')
        userStore.logout()
    },
  })
}

/** 工单统计（共享缓存，与 work 页面复用，30秒内不重复请求） */
const { pendingTickets, processingTickets, doneTickets, loadTicketStats } = useTicketStats()

useTabbarActive('pages/mine/index', 'mine', loadTicketStats)

const settingsList = [
  { titleKey: 'common.profile', name: 'profile' },
  { titleKey: 'mine.changePassword', name: 'account', dialog: true },
  { titleKey: 'common.aboutUs', name: 'about' },
]

const quickLinks = [
  { titleKey: 'common.nav.notices', name: 'work-notices', icon: 'notification', color: 'var(--fa-brand-blue)', soft: 'wot-bg-primary-1' },
  { titleKey: 'common.nav.tickets', name: 'work-tickets', icon: 'message', color: 'var(--fa-brand-violet)', soft: 'wot-bg-purple-1' },
  { titleKey: 'common.nav.aiChat', name: 'work-chat', icon: 'interaction', color: 'var(--fa-brand-blue)', soft: 'wot-bg-primary-1' },
  { titleKey: 'common.nav.aiModels', name: 'work-ai-models', icon: 'robot', color: 'var(--fa-brand-violet)', soft: 'wot-bg-purple-1' },
]

/** 修改密码弹窗（内嵌于「我的」页，免跳转） */
const toast = useToast()
const showPasswordDialog = ref(false)
const submitting = ref(false)
const passwordForm = reactive<PasswordChangeForm>({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

function openPasswordDialog() {
  passwordForm.old_password = ''
  passwordForm.new_password = ''
  passwordForm.confirm_password = ''
  showPasswordDialog.value = true
}

/** 提交修改密码：字段级校验 + 调用后端接口 */
async function handleSubmitPassword() {
  if (!passwordForm.old_password) {
    toast.warning(t('account.oldRequired'))
    return
  }
  if (!passwordForm.new_password) {
    toast.warning(t('common.form.newPasswordRequired'))
    return
  }
  if (passwordForm.new_password.length < 6) {
    toast.warning(t('account.newLength'))
    return
  }
  if (!passwordForm.confirm_password) {
    toast.warning(t('common.form.confirmNewRequired'))
    return
  }
  if (passwordForm.confirm_password !== passwordForm.new_password) {
    toast.warning(t('common.form.mismatch'))
    return
  }

  submitting.value = true
  try {
    await UserAPI.changeCurrentUserPassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password,
      confirm_password: passwordForm.confirm_password,
    })
    toast.success(t('account.success'))
    showPasswordDialog.value = false
  }
  catch {
    // http 层已统一错误提示
  }
  finally {
    submitting.value = false
  }
}
</script>

<template>
  <view class="tabbar-wraper py-3">
    <!-- 用户信息卡（品牌渐变 + 极光装饰圆环，与工作台一致） -->
    <view class="user-info-card mx-4 mb-6 flex items-center gap-4 rounded-3 px-5 py-6">
      <wd-avatar
        size="64px"
        round
        :src="userInfo?.avatar || ''"
        icon="user"
      />
      <view class="min-w-0 flex-1">
        <view class="text-4 text-white font-bold">
          {{ userInfo?.name || t('common.admin') }}
        </view>
        <view class="mt-1 truncate text-3" style="color: rgba(255, 255, 255, 0.9);">
          {{ identityText }}
        </view>
      </view>
      <!-- 设置入口（纯 icon，打开设置页：内含主题设置） -->
      <view
        class="relative z-10 h-11 w-11 flex shrink-0 items-center justify-center rounded-full active:opacity-70"
        hover-class="none"
        aria-role="button"
        :aria-label="t('common.settings')"
        @click="navigateTo('setting')"
      >
        <wd-icon name="settings" size="20px" color="rgba(255, 255, 255, 0.9)" />
      </view>
    </view>

    <!-- 工单统计 -->
    <view class="mx-4 mb-6">
      <wd-row :gutter="12">
        <wd-col :span="8">
          <view class="wot-bg-filled-oppo rounded-3 p-4 text-center active:opacity-70" aria-role="button" :aria-label="t('mine.pendingTickets')" @click="navigateTo('work-tickets')">
            <view class="wot-text-warning-main text-5 font-bold">
              {{ pendingTickets ?? '-' }}
            </view>
            <view class="wot-text-text-secondary mt-1 text-3">
              {{ t('mine.pendingTickets') }}
            </view>
          </view>
        </wd-col>
        <wd-col :span="8">
          <view class="wot-bg-filled-oppo rounded-3 p-4 text-center active:opacity-70" aria-role="button" :aria-label="t('mine.processingTickets')" @click="navigateTo('work-tickets')">
            <view class="wot-text-primary-6 text-5 font-bold">
              {{ processingTickets ?? '-' }}
            </view>
            <view class="wot-text-text-secondary mt-1 text-3">
              {{ t('mine.processingTickets') }}
            </view>
          </view>
        </wd-col>
        <wd-col :span="8">
          <view class="wot-bg-filled-oppo rounded-3 p-4 text-center active:opacity-70" aria-role="button" :aria-label="t('mine.doneTickets')" @click="navigateTo('work-tickets')">
            <view class="wot-text-success-main text-5 font-bold">
              {{ doneTickets ?? '-' }}
            </view>
            <view class="wot-text-text-secondary mt-1 text-3">
              {{ t('mine.doneTickets') }}
            </view>
          </view>
        </wd-col>
      </wd-row>
    </view>

    <!-- 快捷入口 -->
    <view class="wot-bg-filled-oppo mx-4 mb-6 rounded-3 p-3">
      <wd-grid :column="4" :border="false" clickable>
        <wd-grid-item
          v-for="item in quickLinks"
          :key="item.name"
          @click="navigateTo(item.name)"
        >
          <view
            class="h-11 w-11 flex items-center justify-center rounded-xl"
            :class="item.soft"
          >
            <wd-icon :name="item.icon" size="20px" :color="item.color" />
          </view>
          <view class="wot-text-text-secondary mt-1 text-3">
            {{ t(item.titleKey) }}
          </view>
        </wd-grid-item>
      </wd-grid>
    </view>

    <!-- 设置列表 -->
    <view class="mx-4 mb-6">
      <view class="mb-2 mt-1 flex items-center gap-2 px-3">
        <view class="wot-bg-primary-6 h-3.5 w-1 rounded-full" />
        <wd-text class="wot-text-text-main text-3.5" :text="t('common.settings')" bold />
      </view>
      <wd-cell-group border custom-class="rounded-3! overflow-hidden">
        <wd-cell
          v-for="item in settingsList"
          :key="item.name"
          :title="t(item.titleKey)"
          is-link
          @click="item.dialog ? openPasswordDialog() : navigateTo(item.name)"
        />
      </wd-cell-group>
    </view>

    <!-- 退出登录 -->
    <view class="mx-4">
      <wd-button class="logout-btn" type="danger" plain block @click="handleLogout">
        {{ t('mine.logout') }}
      </wd-button>
    </view>

    <!-- 修改密码弹窗 -->
    <wd-popup
      v-model="showPasswordDialog"
      position="bottom"
      round
      :z-index="1100"
      custom-style="padding-bottom: env(safe-area-inset-bottom);"
    >
      <view class="px-4 pb-4 pt-4">
        <view class="wot-text-text-main mb-4 text-center text-4 font-bold">
          {{ t('account.password') }}
        </view>
        <wd-input
          v-model="passwordForm.old_password"
          :label="t('account.oldPassword')"
          show-password
          clearable
          :placeholder="t('account.oldPlaceholder')"
        />
        <view class="h-3" />
        <wd-input
          v-model="passwordForm.new_password"
          :label="t('account.newPassword')"
          show-password
          clearable
          :placeholder="t('common.form.newPasswordPlaceholder')"
        />
        <view class="h-3" />
        <wd-input
          v-model="passwordForm.confirm_password"
          :label="t('account.confirmPassword')"
          show-password
          clearable
          :placeholder="t('common.form.confirmNewPlaceholder')"
        />
        <view class="mt-5">
          <wd-button type="primary" round block :loading="submitting" @click="handleSubmitPassword">
            {{ t('account.submit') }}
          </wd-button>
        </view>
      </view>
      <wd-gap :height="20" />
    </wd-popup>
  </view>
</template>

<style lang="scss">
/* global logout：uni-button 自定义标签不受 scoped 样式作用域约束 */
.wd-button.logout-btn {
  color: var(--wot-danger-main) !important;
  background: transparent !important;
  border: 2rpx solid var(--wot-danger-main) !important;
  border-radius: var(--fa-radius-sm, 16rpx) !important;
}
</style>
