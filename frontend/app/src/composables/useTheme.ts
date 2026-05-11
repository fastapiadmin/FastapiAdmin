import type { ThemeMode } from '@/composables/types/theme'

/**
 * 简化版系统主题管理组合式API
 *
 * 功能特性：
 * - 仅跟随系统主题变化
 * - 自动响应系统主题切换
 * - 导航栏颜色通过 theme.json 自动处理
 * - 轻量级，无额外功能
 *
 * 适用场景：
 * - 只需要系统主题适应的简单应用
 * - 不需要用户手动控制主题的应用
 * - 追求轻量级主题管理的应用
 *
 * 注意事项：
 * - 不支持手动切换主题
 * - 不支持主题色自定义
 * - 导航栏颜色依赖 theme.json 配置
 *
 * @example
 * ```vue
 * <script setup>
 * import { useTheme } from '@/composables/useTheme'
 *
 * const { theme, isDark, themeVars } = useTheme()
 * </script>
 *
 * <template>
 *   <wd-config-provider :theme-vars="themeVars">
 *     <view :class="{ 'dark-mode': isDark }">
 *       <text>当前主题: {{ theme }}</text>
 *     </view>
 *   </wd-config-provider>
 * </template>
 * ```
 */
export function useTheme() {
  const store = useThemeStore()

  // 组件挂载前初始化系统主题
  onBeforeMount(() => {
    store.initSystemTheme()
    // 监听系统主题变化
    if (typeof uni !== 'undefined' && uni.onThemeChange) {
      uni.onThemeChange((res) => {
        // 系统主题变化时自动更新，导航栏颜色由 theme.json 自动处理
        store.setTheme(res.theme as ThemeMode)
        console.log('系统主题已切换至:', res.theme)
      })
    }
  })

  // 组件卸载时清理监听
  onUnmounted(() => {
    if (typeof uni !== 'undefined' && uni.offThemeChange) {
      uni.offThemeChange((res) => {
        store.setTheme(res.theme as ThemeMode)
      })
    }
  })

  return {
    // 状态（只读）
    theme: computed(() => store.theme),
    isDark: computed(() => store.isDark),
    themeVars: computed(() => store.themeVars),
  }
}
