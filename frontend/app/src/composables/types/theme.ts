import type { ConfigProviderThemeVars } from 'wot-design-uni'

/**
 * 主题色选项接口
 */
export interface ThemeColorOption {
  name: string
  value: string
  primary: string
}

/**
 * 主题类型
 */
export type ThemeMode = 'light' | 'dark'

/**
 * 主题状态接口
 */
export interface ThemeState {
  theme: ThemeMode
  followSystem: boolean
  hasUserSet: boolean
  currentThemeColor: ThemeColorOption
  themeVars: ConfigProviderThemeVars
}

/**
 * 系统主题状态接口（简化版）
 */
export interface SystemThemeState {
  theme: ThemeMode
  themeVars: ConfigProviderThemeVars
}

/**
 * 预定义的主题色选项
 */
export const themeColorOptions: ThemeColorOption[] = [
  { name: '默认蓝', value: 'blue', primary: '#4D7FFF' },
  { name: '活力橙', value: 'orange', primary: '#FF7D00' },
  { name: '薄荷绿', value: 'green', primary: '#07C160' },
  { name: '樱花粉', value: 'pink', primary: '#FF69B4' },
  { name: '紫罗兰', value: 'purple', primary: '#8A2BE2' },
  { name: '朱砂红', value: 'red', primary: '#FF4757' },
]
