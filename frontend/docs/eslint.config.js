import tsParser from '@typescript-eslint/parser'
import tsPlugin from '@typescript-eslint/eslint-plugin'
import vueParser from 'vue-eslint-parser'
import vuePlugin from 'eslint-plugin-vue'
import prettierPlugin from 'eslint-plugin-prettier'
import prettierConfig from 'eslint-config-prettier'

export default [
  {
    ignores: [
      '**/node_modules/**',
      '**/.vitepress/cache/**',
      '**/dist/**',
      '**/build/**',
      '**/coverage/**',
      '**/*.log',
      '**/*.md'
    ]
  },
  {
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        browser: true,
        node: true
      }
    },
    rules: {
      'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'warn',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'warn',
      'no-unused-vars': 'warn',
      'no-empty-function': 'warn',
      'semi': ['error', 'always'],
      'quotes': ['error', 'single'],
      'indent': ['error', 2, { 'SwitchCase': 1 }]
    }
  },
  {
    files: ['**/*.ts'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        browser: true,
        node: true
      },
      parser: tsParser,
      parserOptions: {
        project: ['./tsconfig.json'],
        tsconfigRootDir: __dirname
      }
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
      'prettier': prettierPlugin
    },
    rules: {
      'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'warn',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'warn',
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unused-vars': 'error',
      '@typescript-eslint/no-empty-function': 'warn',
      '@typescript-eslint/semi': ['error', 'always'],
      '@typescript-eslint/quotes': ['error', 'single'],
      '@typescript-eslint/indent': ['error', 2, { 'SwitchCase': 1 }],
      'prettier/prettier': 'error'
    }
  },
  {
    files: ['**/*.vue'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        browser: true,
        node: true
      },
      parser: vueParser,
      parserOptions: {
        parser: '@typescript-eslint/parser',
        ecmaVersion: 'latest',
        sourceType: 'module'
      }
    },
    plugins: {
      'vue': vuePlugin,
      'prettier': prettierPlugin
    },
    rules: {
      ...vuePlugin.configs['recommended'].rules,
      'vue/script-setup-uses-vars': 'error',
      'vue/no-unused-components': 'warn',
      'vue/no-unused-vars': 'warn',
      'prettier/prettier': 'error'
    }
  },
  prettierConfig
]