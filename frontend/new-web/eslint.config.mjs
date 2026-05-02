// ESLint 配置文件
import fs from 'fs'
import path, { dirname } from 'path'
import { fileURLToPath } from 'url'

import pluginJs from '@eslint/js'
import eslintPluginPrettierRecommended from 'eslint-plugin-prettier/recommended'
import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'
import tseslint from 'typescript-eslint'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const autoImportConfig = JSON.parse(
  fs.readFileSync(path.resolve(__dirname, '.auto-import.json'), 'utf-8')
)

// Element Plus 组件全局配置
const elementPlusComponents = {
  ElInput: 'readonly',
  ElSelect: 'readonly',
  ElSwitch: 'readonly',
  ElCascader: 'readonly',
  ElInputNumber: 'readonly',
  ElTimePicker: 'readonly',
  ElTimeSelect: 'readonly',
  ElDatePicker: 'readonly',
  ElTreeSelect: 'readonly',
  ElText: 'readonly',
  ElRadioGroup: 'readonly',
  ElCheckboxGroup: 'readonly',
  ElOption: 'readonly',
  ElRadio: 'readonly',
  ElCheckbox: 'readonly',
  ElInputTag: 'readonly',
  ElForm: 'readonly',
  ElFormItem: 'readonly',
  ElTable: 'readonly',
  ElTableColumn: 'readonly',
  ElButton: 'readonly',
  ElDialog: 'readonly',
  ElPagination: 'readonly',
  ElMessage: 'readonly',
  ElMessageBox: 'readonly',
  ElNotification: 'readonly',
  ElTree: 'readonly',
  ElDropdown: 'readonly',
  ElDropdownMenu: 'readonly',
  ElDropdownItem: 'readonly',
  ElAvatar: 'readonly',
  ElBadge: 'readonly',
  ElCard: 'readonly',
  ElCol: 'readonly',
  ElRow: 'readonly',
  ElContainer: 'readonly',
  ElHeader: 'readonly',
  ElAside: 'readonly',
  ElMain: 'readonly',
  ElFooter: 'readonly',
  ElLink: 'readonly',
  ElDivider: 'readonly',
  ElImage: 'readonly',
  ElProgress: 'readonly',
  ElSkeleton: 'readonly',
  ElSlider: 'readonly',
  ElSwitch: 'readonly',
  ElTag: 'readonly',
  ElTooltip: 'readonly',
  ElPopover: 'readonly',
  ElPopconfirm: 'readonly',
  ElDrawer: 'readonly',
  ElAlert: 'readonly',
  ElLoading: 'readonly',
}

export default [
  // 忽略文件配置
  {
    ignores: [
      'node_modules',
      'dist',
      'public',
      '.vscode/**',
      'src/assets/**',
      'src/utils/console.ts',
      '**/*.min.*',
      '**/auto-imports.d.ts',
      '**/components.d.ts',
      '**/types/**/*.d.ts',
    ],
  },

  // 基础配置
  {
    files: ['**/*.{js,mjs,cjs,ts,tsx,vue}'],
  },
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2022,
      },
    },
  },
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
  ...pluginVue.configs['flat/essential'],

  // 全局配置
  {
    files: ['**/*.{js,mjs,cjs,ts,tsx,vue}'],

    languageOptions: {
      globals: {
        ...autoImportConfig.globals,
        Api: 'readonly',
        ...elementPlusComponents,
        // 全局类型定义
        PageQuery: 'readonly',
        PageResult: 'readonly',
        UserListItem: 'readonly',
        UserSearchParams: 'readonly',
        RoleListItem: 'readonly',
        RoleSearchParams: 'readonly',
        OptionType: 'readonly',
        ApiResponse: 'readonly',
        ExcelResult: 'readonly',
        CommonType: 'readonly',
        updatorType: 'readonly',
        creatorType: 'readonly',
        TagView: 'readonly',
        AppSettings: 'readonly',
        __APP_INFO__: 'readonly',
        UploadFilePath: 'readonly',
      },
    },
    rules: {
      // 代码风格
      quotes: ['error', 'single'],
      semi: ['error', 'never'],
      'no-var': 'error',
      'prefer-const': 'error',
      'object-shorthand': 'error',

      // 最佳实践
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'eqeqeq': 'off',
      'no-multi-spaces': 'error',
      'no-multiple-empty-lines': ['warn', { max: 1 }],
      'no-unexpected-multiline': 'error',

      // TypeScript 规则
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/ban-ts-comment': 'off',
      '@typescript-eslint/no-empty-function': 'off',
      '@typescript-eslint/no-empty-object-type': 'off',
      '@typescript-eslint/no-non-null-assertion': 'off',
      '@typescript-eslint/no-unused-vars': 'warn',

      // Vue 规则
      'vue/multi-word-component-names': 'off',
      'vue/no-v-html': 'off',
      'vue/require-default-prop': 'off',
      'vue/require-explicit-emits': 'error',
      'vue/no-unused-vars': 'error',
      'vue/no-mutating-props': 'off',
      'vue/valid-v-for': 'warn',
      'vue/no-template-shadow': 'warn',
      'vue/return-in-computed-property': 'warn',
      'vue/block-order': ['error', { order: ['template', 'script', 'style'] }],
      'vue/html-self-closing': [
        'error',
        {
          html: { void: 'always', normal: 'never', component: 'always' },
          svg: 'always',
          math: 'always',
        },
      ],
      'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    },
  },

  // Vue 文件特定配置
  {
    files: ['**/*.vue'],
    languageOptions: {
      parserOptions: { parser: tseslint.parser },
    },
  },

  // prettier 配置
  eslintPluginPrettierRecommended,
]
