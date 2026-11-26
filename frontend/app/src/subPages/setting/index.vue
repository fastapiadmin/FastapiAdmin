<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { formatMessage } from '@/locales/format'
import { useGlobalDialog } from '@/composables/useGlobalDialog'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'
import {
  ACCESS_TOKEN_KEY,
  DICT_CACHE_KEY,
  LANG_KEY,
  REFRESH_TOKEN_KEY,
  REMEMBER_ME_KEY,
  WATERMARK_KEY,
} from '@/constants'
import { useConfigStore } from '@/store/configStore'
import { Storage } from '@/utils/storage'

definePage({
  name: 'setting',
  layout: 'default',
  style: {
    navigationBarTitleText: '设置',
  },
})
useI18nNavTitle('setting.navTitle')
const { success: showSuccess } = useGlobalToast()
const { t, locale } = useI18n()
const router = useRouter()
const globalDialog = useGlobalDialog()
const configStore = useConfigStore()
// 拉取系统参数（品牌介绍/相关链接/版本/水印开关），幂等 + 本地持久化缓存
configStore.getConfig()

/** 语言切换 */
const showLangSheet = ref(false)
const langOptions = [
  { labelKey: 'setting.langZh', value: 'zh-CN' },
  { labelKey: 'setting.langEn', value: 'en-US' },
]
/** 当前语言值（解包 vue-i18n 的 locale ref，供模板类型安全的比较） */
const currentLocale = computed(() => locale.value)
/** 当前语言 i18n key（仅数据查找，翻译交给模板的 t() 处理） */
const currentLangKey = computed(() => {
  const opt = langOptions.find(o => o.value === locale.value)
  return opt?.labelKey || langOptions[0].labelKey
})

function handleLangSelect(option: { labelKey: string, value: string }) {
  locale.value = option.value
  Storage.set(LANG_KEY, option.value)
  showLangSheet.value = false
}

/** 品牌区与相关链接参数（来自后端系统参数，带默认值兜底；web 端消费方式：configData?.[key]?.config_value） */
const brandTitle = computed(() => configStore.configData?.sys_name?.config_value?.trim() || 'FastapiAdmin')
const brandDesc = computed(() => configStore.configData?.login_subtitle?.config_value?.trim() || t('setting.brandDesc'))
const helpDoc = computed(() => configStore.configData?.help_doc?.config_value?.trim() || '')
const gitCode = computed(() => configStore.configData?.git_code?.config_value?.trim() || '')

/** 当前系统版本（后端 version 参数） */
const version = computed(() => configStore.configData?.version?.config_value?.trim() || '')

/** 本地水印偏好，默认开启，由本页开关控制（兼容历史脏对象 { value }，统一兜底为布尔） */
const storedWatermark = Storage.get<boolean | { value: boolean }>(WATERMARK_KEY)
const watermarkSwitch = ref(typeof storedWatermark === 'object' && storedWatermark ? Boolean(storedWatermark.value) : (storedWatermark ?? true))

/** wd-switch change 事件参数为 { value } 对象，取 value 落盘并同步 layout 水印 */
function handleWatermarkChange(e: { value: boolean }) {
  const on = e.value
  Storage.set(WATERMARK_KEY, on)
  // 同步常驻 layout 的水印显示状态（H5 / 小程序）
  uni.$emit('updateWatermarkSwitch', on)
}

// 跳转关于页
function navigateToAbout() {
  router.push({ name: 'about' })
}

/** 当前缓存占用大小，进入页面时刷新（清除后归零） */
const cacheSize = ref('')
onShow(() => {
  cacheSize.value = Storage.getSize()
})

/** 清除本地缓存：清认证与数据缓存（保留主题、水印偏好），清除后回到登录页 */
function clearLocalCache() {
  ;[ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY, REMEMBER_ME_KEY, DICT_CACHE_KEY, 'appUserInfo', 'appConfig']
    .forEach(key => Storage.remove(key))
  cacheSize.value = Storage.getSize()
  uni.reLaunch({ url: '/pages/login/index' })
}

function handleClearCache() {
  globalDialog.confirm({
    title: t('common.title'),
    msg: t('setting.clearCacheMsg'),
    confirmButtonText: t('setting.clearCacheConfirm'),
    success: (res) => {
      if (res.action === 'confirm')
        clearLocalCache()
    },
  })
}
const {
  theme,
  toggleTheme,
  currentThemeColor,
  followSystem,
  showThemeColorSheet,
  themeColorOptions,
  openThemeColorPicker,
  closeThemeColorPicker,
  selectThemeColor,
  setFollowSystem,
} = useTheme()

const isDark = computed({
  get() {
    return theme.value === 'dark'
  },
  set() {
    toggleTheme()
  },
})

/** 跟随系统：用开关展示当前状态，而不是一个没有选中态的普通按钮 */
function handleFollowSystemChange(e: { value: boolean }) {
  setFollowSystem(e.value)
}

// 当前主题色 i18n key（按 value 从预设中解析，兼容历史持久化数据缺失 labelKey 的情况；翻译交给模板的 t() 处理）
const currentThemeNameKey = computed(() => {
  const current = currentThemeColor.value
  const option = themeColorOptions.find(o => o.value === current.value) || themeColorOptions[0]
  return option.labelKey
})

// 处理主题色选择
function handleThemeColorSelect(option: any) {
  selectThemeColor(option)
}

// 链接导航处理
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
      showSuccess({ msg: formatMessage(t, 'setting.copied', { url }) })
    },
  })
  // #endif
}
</script>

<template>
  <view class="page-wraper box-border pb-6 pt-3">
    <view class="wot-bg-filled-oppo mx-4 box-border rounded-4 px-5 py-5">
      <text class="wot-text-text-main mb-2 block text-5 font-bold">
        {{ brandTitle }}
      </text>
      <wd-text class="wot-text-text-secondary block" size="14px" line-height="1.6" :text="brandDesc" />
    </view>

    <view class="mx-4">
      <view class="section-head section-head--flush">
        <view class="section-head__bar" />
        <text class="section-head__title">{{ t('setting.basic') }}</text>
      </view>
      <wd-cell-group border custom-class="rounded-4! overflow-hidden">
        <wd-cell :title="t('setting.darkMode')">
          <wd-switch v-model="isDark" size="20px" />
        </wd-cell>
        <wd-cell :title="t('setting.followSystem')">
          <wd-switch :model-value="followSystem" size="20px" @change="handleFollowSystemChange" />
        </wd-cell>
        <wd-cell :title="t('setting.themeColor')" is-link @click="openThemeColorPicker">
          <view class="flex items-center justify-end gap-2">
            <view
              class="h-4 w-4 rounded-full"
              :style="{ backgroundColor: currentThemeColor.primary }"
            />
            <wd-text :text="t(currentThemeNameKey)" />
          </view>
        </wd-cell>
        <wd-cell :title="t('setting.language')" is-link @click="showLangSheet = true">
          <wd-text class="wot-text-text-secondary text-3" :text="t(currentLangKey)" />
        </wd-cell>
        <wd-cell :title="t('setting.watermark')" :is-link="false">
          <wd-switch
            v-model="watermarkSwitch"
            size="20px"
            @change="handleWatermarkChange"
          />
        </wd-cell>
      </wd-cell-group>
    </view>

    <view class="mx-4">
      <view class="section-head section-head--flush">
        <view class="section-head__bar" />
        <text class="section-head__title">{{ t('setting.links') }}</text>
      </view>
      <wd-cell-group border custom-class="rounded-4! overflow-hidden">
        <wd-cell :title="t('common.docs')" is-link @click="handleNavigate(helpDoc)" />
        <wd-cell :title="t('common.github')" is-link @click="handleNavigate(gitCode)" />
      </wd-cell-group>
    </view>

    <view class="mx-4">
      <view class="section-head section-head--flush">
        <view class="section-head__bar" />
        <text class="section-head__title">{{ t('setting.general') }}</text>
      </view>
      <wd-cell-group border custom-class="rounded-4! overflow-hidden">
        <wd-cell :title="t('setting.version')" :is-link="false">
          <wd-text class="wot-text-text-secondary text-3" :text="`v${version || '--'}`" />
        </wd-cell>
        <wd-cell :title="t('common.aboutUs')" is-link @click="navigateToAbout" />
        <wd-cell :title="t('setting.clearCache')" is-link :value="cacheSize" @click="handleClearCache" />
      </wd-cell-group>
    </view>

    <!-- 底部安全区（全面屏 Home 条避让） -->
    <wd-gap height="100rpx" safe-area-bottom />

    <!-- 主题色选择 ActionSheet -->
    <wd-action-sheet
      v-model="showThemeColorSheet"
      :title="t('setting.themeColor')"
      :close-on-click-action="true"
      @cancel="closeThemeColorPicker"
    >
      <view class="px-4 pb-4">
        <view
          v-for="option in themeColorOptions"
          :key="option.value"
          class="wot-border-border-main flex min-h-11 items-center justify-between border-b py-3 last:border-b-0"
          @click="handleThemeColorSelect(option)"
        >
          <view class="flex items-center gap-3">
            <view
              class="wot-border-border-main h-6 w-6 border-2 rounded-full"
              :style="{ backgroundColor: option.primary }"
            />
            <wd-text class="wot-text-text-main text-4" :text="t(option.labelKey)" />
          </view>
          <wd-icon
            v-if="currentThemeColor.value === option.value"
            name="check"
            :color="option.primary"
            size="20px"
          />
        </view>
      </view>
      <wd-gap :height="50" />
    </wd-action-sheet>

    <!-- 语言选择 ActionSheet -->
    <wd-action-sheet
      v-model="showLangSheet"
      :title="t('setting.language')"
      :close-on-click-action="true"
      @cancel="showLangSheet = false"
    >
      <view class="px-4 pb-4">
        <view
          v-for="option in langOptions"
          :key="option.value"
          class="wot-border-border-main flex min-h-11 items-center justify-between border-b py-3 last:border-b-0"
          @click="handleLangSelect(option)"
        >
          <wd-text :text="t(option.labelKey)" class="wot-text-text-main text-4" />
          <wd-icon
            v-if="currentLocale === option.value"
            name="check"
            color="var(--wot-primary-6)"
            size="20px"
          />
        </view>
      </view>
      <wd-gap :height="50" />
    </wd-action-sheet>
  </view>
</template>
