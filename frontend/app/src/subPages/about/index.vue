<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { formatMessage } from '@/locales/format'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'
import { useConfigStore } from '@/store/configStore'
import { VersionAPI, type VersionItem } from '@/api/module_system/version'

const { t } = useI18n()

definePage({
  name: 'about',
  style: {
    navigationBarTitleText: '关于',
  },
})
useI18nNavTitle('about.navTitle')

const configStore = useConfigStore()
const versions = ref<VersionItem[]>([])

onMounted(async () => {
  try {
    versions.value = (await VersionAPI.getPublished()).slice().sort((a, b) => (b.date || '').localeCompare(a.date || '') || b.id - a.id)
  }
  catch {
    versions.value = []
  }
})
// 拉取系统参数（系统名称/版本/版权/链接），幂等 + 本地持久化缓存
configStore.getConfig()

/** 关于页参数（来自后端系统参数，带默认值兜底；web 端消费方式：configData?.[key]?.config_value） */
const sysName = computed(() => configStore.configData?.sys_name?.config_value?.trim() || 'FastapiAdmin')
const version = computed(() => configStore.configData?.version?.config_value?.trim() || '')
const loginSubtitle = computed(() => configStore.configData?.login_subtitle?.config_value?.trim() || '')
const copyright = computed(() => configStore.configData?.copyright?.config_value?.trim() || '')
const helpDoc = computed(() => configStore.configData?.help_doc?.config_value?.trim() || '')
const gitCode = computed(() => configStore.configData?.git_code?.config_value?.trim() || '')

/** 与登录页一致的品牌标识：优先后端自定义 Logo，否则内置新品牌标识 */
const BASE_PATH = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : `${import.meta.env.BASE_URL}/`
const OFFICIAL_LOGO_HOST = 'service.fastapiadmin.com'
const brandLogo = computed(() => {
  const custom = configStore.configData?.logo_url?.config_value?.trim()
  if (!custom || custom.includes(OFFICIAL_LOGO_HOST)) return `${BASE_PATH}static/logo.png`
  return custom
})

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
      <view class="wot-bg-filled-oppo rounded-4 px-5 py-6 text-center">
        <view class="about-logo">
          <image class="about-logo__img" :src="brandLogo" mode="aspectFit" />
        </view>
        <view class="wot-text-text-main mb-1 text-6 font-bold">
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
      <view class="section-head section-head--flush">
        <view class="section-head__bar" />
        <text class="section-head__title">{{ t('about.moreInfo') }}</text>
      </view>
      <wd-cell-group border custom-class="rounded-4! overflow-hidden">
        <wd-cell :title="t('common.docs')" is-link @click="handleNavigate(helpDoc)" />
        <wd-cell :title="t('common.github')" is-link @click="handleNavigate(gitCode)" />
      </wd-cell-group>
    </view>

    <!-- 更新日志 -->
    <view v-if="versions.length" class="mx-4 mt-6">
      <view class="section-head section-head--flush">
        <view class="section-head__bar" />
        <text class="section-head__title">{{ t('about.changelog') }}</text>
      </view>
      <view class="changelog-list">
        <view v-for="item in versions" :key="item.id" class="changelog-item">
          <view class="changelog-item__head">
            <text class="changelog-item__version">{{ item.version.startsWith('v') ? item.version : `v${item.version}` }}</text>
            <text class="changelog-item__date">{{ item.date }}</text>
          </view>
          <view class="changelog-item__title">{{ item.title }}</view>
          <rich-text v-if="item.content" class="changelog-item__content" :nodes="item.content" />
        </view>
      </view>
    </view>

    <!-- 版权信息 -->
    <view v-if="copyright" class="mx-4 mt-6 text-center">
      <wd-text class="wot-text-text-auxiliary text-3" :text="copyright" />
    </view>

    <!-- 底部安全区（全面屏 Home 条避让） -->
    <wd-gap height="100rpx" safe-area-bottom />
  </view>
</template>

<style lang="scss" scoped>
/* 品牌标识：与登录页同一枚 Logo，替代原来的 emoji 主视觉 */
.about-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  margin: 0 auto 16px;
  overflow: hidden;
  border-radius: 18px;
  box-shadow: 0 8px 20px rgba(79, 107, 255, 0.18);

  &__img {
    display: block;
    width: 72px;
    height: 72px;
  }
}
.changelog-list {
  overflow: hidden;
  background: var(--wot-bg-filled-oppo, #fff);
  border-radius: 16px;
}

.changelog-item {
  padding: 16px;

  & + & {
    border-top: 1px solid var(--wot-border-main, #eef0f4);
  }

  &__head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
  }

  &__version {
    color: var(--wot-primary-main, #4f6bff);
    font-size: 15px;
    font-weight: 600;
  }

  &__date {
    color: var(--wot-text-auxiliary, #8a94a6);
    font-size: 12px;
  }

  &__title {
    color: var(--wot-text-main, #1f2d3d);
    font-size: 14px;
    line-height: 1.6;
  }

  &__content {
    display: block;
    margin-top: 6px;
    color: var(--wot-text-secondary, #5b6472);
    font-size: 13px;
    line-height: 1.7;
  }
}
</style>
