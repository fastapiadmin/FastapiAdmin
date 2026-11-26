<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { formatMessage } from '@/locales/format'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'
import { useConfigStore } from '@/store/configStore'

const { t } = useI18n()

definePage({
  name: 'about',
  style: {
    navigationBarTitleText: '关于',
  },
})
useI18nNavTitle('about.navTitle')

const configStore = useConfigStore()
// 拉取系统参数（系统名称/版本/版权/链接），幂等 + 本地持久化缓存
configStore.getConfig()

/** 关于页参数（来自后端系统参数，带默认值兜底；web 端消费方式：configData?.[key]?.config_value） */
const sysName = computed(() => configStore.configData?.sys_name?.config_value?.trim() || 'FastapiAdmin')
const version = computed(() => configStore.configData?.version?.config_value?.trim() || '')
const loginSubtitle = computed(() => configStore.configData?.login_subtitle?.config_value?.trim() || '')
const copyright = computed(() => configStore.configData?.copyright?.config_value?.trim() || '')
const helpDoc = computed(() => configStore.configData?.help_doc?.config_value?.trim() || '')
const gitCode = computed(() => configStore.configData?.git_code?.config_value?.trim() || '')

// 链接导航处理（H5 新窗口打开，非 H5 复制到剪贴板）
function handleNavigate(url: string) {
  if (!url)
    return
  // #ifdef H5
  window.open(url, '_blank')
  // #endif
  // #ifndef H5
  uni.setClipboardData({
    data: url,
    showToast: false,
    success: () => {
      uni.hideToast()
      uni.showToast({ title: t('about.copied'), icon: 'none' })
    },
  })
  // #endif
}
</script>

<template>
  <view class="page-wraper box-border py-3">
    <!-- 头部介绍 -->
    <view class="mx-4 mb-6">
      <view class="wot-bg-filled-oppo rounded-3 px-5 py-8 text-center">
        <view class="mb-4 text-10">
          👋
        </view>
        <view class="wot-text-text-main mb-2 text-6 font-bold">
          {{ sysName }}
        </view>
        <view v-if="version" class="wot-text-text-secondary mb-2 text-3.5">
          {{ formatMessage(t, 'about.currentVersion', { version }) }}
        </view>
        <view v-if="loginSubtitle" class="wot-text-text-secondary text-3 leading-relaxed">
          {{ loginSubtitle }}
        </view>
      </view>
    </view>

    <!-- 更多信息 -->
    <view class="mx-4">
      <view class="wot-text-text-main mb-2 px-1 text-3.5 font-bold">
        {{ t('about.moreInfo') }}
      </view>
      <wd-cell-group border custom-class="rounded-3! overflow-hidden">
        <wd-cell :title="t('common.docs')" is-link @click="handleNavigate(helpDoc)" />
        <wd-cell :title="t('common.github')" is-link @click="handleNavigate(gitCode)" />
      </wd-cell-group>
    </view>

    <!-- 版权信息 -->
    <view v-if="copyright" class="mx-4 mt-8 text-center">
      <wd-text class="wot-text-text-auxiliary text-3" :text="copyright" />
    </view>

    <!-- 底部安全区（全面屏 Home 条避让） -->
    <wd-gap height="100rpx" safe-area-bottom />
  </view>
</template>
