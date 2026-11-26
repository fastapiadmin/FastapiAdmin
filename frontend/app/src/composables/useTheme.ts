import type { ThemeColorOption, ThemeMode } from '@/composables/types/theme'
import { themeColorOptions } from '@/composables/types/theme'
import { initializeThemeOnce, subscribeSystemThemeChange } from '@/utils/systemTheme'

/**
 * 主题管理组合式API（统一入口）
 *
 * 功能特性：
 * - 支持手动切换暗黑模式
 * - 支持主题色选择
 * - 支持跟随系统主题
 * - 自动同步导航栏颜色
 * - 持久化用户设置
 *
 * @example
 * ```vue
 * <script setup>
 * const {
 *   theme,
 *   isDark,
 *   toggleTheme,
 *   openThemeColorPicker,
 *   currentThemeColor,
 *   themeVars
 * } = useTheme()
 * </script>
 *
 * <template>
 *   <wd-config-provider :theme="theme" :theme-vars="themeVars">
 *     <view :class="{ 'dark-mode': isDark }">
 *       <wd-button @click="toggleTheme">切换主题</wd-button>
 *       <wd-button @click="openThemeColorPicker">选择主题色</wd-button>
 *     </view>
 *   </wd-config-provider>
 * </template>
 * ```
 */
export function useTheme() {
  const store = useThemeStore()
  const showThemeColorSheet = ref(false)
  let stopThemeChangeListener: (() => void) | undefined

  /**
   * 切换暗黑模式
   * @param mode 指定主题模式，不传则自动切换
   * @param isFollowSystem 是否跟随系统
   */
  function toggleTheme(mode?: ThemeMode, isFollowSystem: boolean = false) {
    store.toggleTheme(mode, isFollowSystem)
  }

  /**
   * 打开主题色选择器
   */
  function openThemeColorPicker() {
    showThemeColorSheet.value = true
  }

  /**
   * 关闭主题色选择器
   */
  function closeThemeColorPicker() {
    showThemeColorSheet.value = false
  }

  /**
   * 选择主题色
   * @param option 主题色选项
   */
  function selectThemeColor(option: ThemeColorOption) {
    store.setCurrentThemeColor(option)
    closeThemeColorPicker()
  }

  /**
   * 初始化主题
   */
  function initTheme() {
    store.initTheme()
  }

  // 组件挂载前初始化主题
  onBeforeMount(() => {
    initializeThemeOnce(store, initTheme)
    stopThemeChangeListener = subscribeSystemThemeChange(store, (res) => {
      if (store.followSystem) {
        store.toggleTheme(res.theme, true)
      }
    })
  })

  // 页面显示时更新导航栏颜色，确保每次切换页面时导航栏颜色都是正确的
  onShow(() => {
    store.setNavigationBarColor()
  })

  // 组件卸载时清理监听
  onUnmounted(() => {
    stopThemeChangeListener?.()
    stopThemeChangeListener = undefined
  })

  return {
    // 状态
    theme: computed(() => store.theme),
    isDark: computed(() => store.isDark),
    followSystem: computed(() => store.followSystem),
    hasUserSet: computed(() => store.hasUserSet),
    currentThemeColor: computed(() => store.currentThemeColor),
    themeVars: computed(() => ({ ...store.currentThemeColor.primaryShades })),
    showThemeColorSheet,

    // 常量
    themeColorOptions,

    // 方法
    initTheme,
    toggleTheme,
    setFollowSystem: store.setFollowSystem,
    openThemeColorPicker,
    closeThemeColorPicker,
    selectThemeColor,
  }
}

// 导出类型和常量供外部使用
export type { ThemeColorOption, ThemeMode }
export { themeColorOptions }
