import type { ThemeColorOption, ThemeMode, ThemeState } from '@/composables/types/theme'
import { defineStore } from 'pinia'
import { themeColorOptions } from '@/composables/types/theme'
import { getSystemTheme } from '@/utils/systemTheme'

function buildThemeVars(color: ThemeColorOption) {
  return {
    ...color.primaryShades,
  }
}

/** 主题色 → 原生导航栏背景色（与水滴渐变顶部色 --drop-base-a 一致，消除导航栏与页面背景的白色断层） */
const THEME_NAV_BG: Record<string, string> = {
  blue: '#EEF1FF',
  orange: '#FFF4E7',
  green: '#EAF9F1',
  pink: '#FFF0F7',
  purple: '#F3EEFF',
  red: '#FFF0F1',
}

/**
 * 主题状态管理
 * 支持手动切换主题、主题色选择、跟随系统主题等完整功能
 */
export const useThemeStore = defineStore('theme', {
  state: (): ThemeState => ({
    theme: 'light',
    followSystem: true, // 是否跟随系统主题
    hasUserSet: false, // 用户是否手动设置过主题
    currentThemeColor: themeColorOptions[0],
    themeVars: buildThemeVars(themeColorOptions[0]),
  }),

  getters: {
    isDark: state => state.theme === 'dark',
  },

  actions: {
    /**
     * 手动切换主题
     * @param mode 指定主题模式，不传则自动切换
     * @param isFollowSystem 是否是跟随系统
     */
    toggleTheme(mode?: ThemeMode, isFollowSystem: boolean = false) {
      this.theme = mode || (this.theme === 'light' ? 'dark' : 'light')
      if (!isFollowSystem) {
        // 如果不是跟随系统，是手动切换
        this.hasUserSet = true // 标记用户已手动设置
        this.followSystem = false // 不再跟随系统
      }
      this.setNavigationBarColor()
    },

    /**
     * 设置是否跟随系统主题
     * @param follow 是否跟随系统
     */
    setFollowSystem(follow: boolean) {
      this.followSystem = follow
      if (follow) {
        this.hasUserSet = false
        this.initTheme() // 重新获取系统主题
      }
      else {
        this.hasUserSet = true
        this.setNavigationBarColor()
      }
    },

    /**
     * 设置导航栏颜色：亮色跟随主题色渐变顶部色；暗色用 --wot-filled-content 对应色（coolgrey-9 #272B3B），
     * 与暗色页面背景一致，避免纯黑与深灰蓝断层
     */
    setNavigationBarColor() {
      const bg = this.theme === 'light' ? (THEME_NAV_BG[this.currentThemeColor.value] ?? '#E3F1FF') : '#272B3B'
      uni.setNavigationBarColor({
        frontColor: this.theme === 'light' ? '#000000' : '#ffffff',
        backgroundColor: bg,
      })
    },

    /**
     * 设置主题色
     * @param color 主题色选项
     */
    setCurrentThemeColor(color: ThemeColorOption) {
      this.currentThemeColor = color
      this.themeVars = {
        ...this.themeVars,
        ...buildThemeVars(color),
      }
      // 切换主题色后同步刷新导航栏背景，避免停留在旧主题色
      this.setNavigationBarColor()
    },

    /**
     * 获取系统主题
     * @returns 系统主题模式
     */
    getSystemTheme(): ThemeMode {
      return getSystemTheme()
    },

    /**
     * 初始化主题
     */
    initTheme() {
      // 迁移旧版持久化的主题色阶：按 value 重新取当前预设，避免历史缓存把主色留在旧蓝色
      const freshColor = themeColorOptions.find(item => item.value === this.currentThemeColor?.value)
      if (freshColor) {
        this.currentThemeColor = freshColor
        this.themeVars = buildThemeVars(freshColor)
      }

      // 如果用户已手动设置且不跟随系统，保持当前主题
      if (this.hasUserSet && !this.followSystem) {
        this.setNavigationBarColor()
        return
      }

      // 获取系统主题
      const systemTheme = this.getSystemTheme()

      // 如果是首次启动或跟随系统，使用系统主题
      if (!this.hasUserSet || this.followSystem) {
        this.theme = systemTheme
        if (!this.hasUserSet)
          this.followSystem = true
      }

      this.setNavigationBarColor()
    },
  },
})
