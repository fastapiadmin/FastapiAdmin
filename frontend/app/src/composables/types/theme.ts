/*
 * @Author: weisheng
 * @Date: 2025-09-02 09:42:36
 * @LastEditTime: 2026-04-10 11:01:37
 * @LastEditors: weisheng
 * @Description:
 * @FilePath: /wot-starter/src/composables/types/theme.ts
 * 记得注释
 */
import type { ConfigProviderThemeVars } from '@wot-ui/ui'

export type PrimaryShadeKey
  = | 'primary1'
    | 'primary2'
    | 'primary3'
    | 'primary4'
    | 'primary5'
    | 'primary6'
    | 'primary7'
    | 'primary8'
    | 'primary9'
    | 'primary10'

export type ThemePrimaryShades = Record<PrimaryShadeKey, string>

/**
 * 主题色选项接口
 */
export interface ThemeColorOption {
  /** i18n key（如 theme.colors.blue） */
  labelKey: string
  value: string
  // 主色 6，用于列表和当前主题色圆点展示
  primary: string
  // 完整主色阶，用于注入 ConfigProvider 主题变量
  primaryShades: ThemePrimaryShades
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
 * 预定义的主题色选项
 */
export const themeColorOptions: ThemeColorOption[] = [
  {
    labelKey: 'theme.colors.blue',
    value: 'blue',
    primary: '#4F6BFF',
    primaryShades: {
      primary1: '#EEF1FF',
      primary2: '#DCE2FF',
      primary3: '#C3CDFF',
      primary4: '#A5B3FF',
      primary5: '#4F6BFF',
      primary6: '#4F6BFF',
      primary7: '#3D55E0',
      primary8: '#2F43B8',
      primary9: '#24348F',
      primary10: '#1A2669',
    },
  },
  {
    labelKey: 'theme.colors.orange',
    value: 'orange',
    primary: '#FF7D00',
    primaryShades: {
      primary1: '#FFF7F0',
      primary2: '#FFEAD6',
      primary3: '#FFD0A8',
      primary4: '#FFB06E',
      primary5: '#FF9338',
      primary6: '#FF7D00',
      primary7: '#D96800',
      primary8: '#B35600',
      primary9: '#8A4200',
      primary10: '#5F2D00',
    },
  },
  {
    labelKey: 'theme.colors.green',
    value: 'green',
    primary: '#07C160',
    primaryShades: {
      primary1: '#F1FCF6',
      primary2: '#DCF7E8',
      primary3: '#B4EFD0',
      primary4: '#7FE2AF',
      primary5: '#42D28A',
      primary6: '#07C160',
      primary7: '#049F4F',
      primary8: '#028241',
      primary9: '#016532',
      primary10: '#014825',
    },
  },
  {
    labelKey: 'theme.colors.pink',
    value: 'pink',
    primary: '#FF69B4',
    primaryShades: {
      primary1: '#FFF2F9',
      primary2: '#FFE2F1',
      primary3: '#FFC2E3',
      primary4: '#FF99D1',
      primary5: '#FF7FC2',
      primary6: '#FF69B4',
      primary7: '#E84E9F',
      primary8: '#CC3F8A',
      primary9: '#A9336F',
      primary10: '#7A2450',
    },
  },
  {
    labelKey: 'theme.colors.purple',
    value: 'purple',
    primary: '#8A2BE2',
    primaryShades: {
      primary1: '#F7F2FF',
      primary2: '#EEE2FF',
      primary3: '#D9BDFF',
      primary4: '#BC8DFF',
      primary5: '#A05EFF',
      primary6: '#8A2BE2',
      primary7: '#7423BF',
      primary8: '#5E1D9C',
      primary9: '#491679',
      primary10: '#321056',
    },
  },
  {
    labelKey: 'theme.colors.red',
    value: 'red',
    primary: '#FF4757',
    primaryShades: {
      primary1: '#FFF3F4',
      primary2: '#FFE3E5',
      primary3: '#FFC0C6',
      primary4: '#FF909A',
      primary5: '#FF6672',
      primary6: '#FF4757',
      primary7: '#DB3445',
      primary8: '#B7293A',
      primary9: '#931E2E',
      primary10: '#6F1421',
    },
  },
]
