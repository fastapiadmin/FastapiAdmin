---
name: pinia-store-generator
description: 创建符合项目规范的 Pinia Store
---

# Pinia Store 生成器

快速创建符合 wot-starter 项目规范的 Pinia Store。

## 目录结构

```
src/store/
├── persist.ts           # 持久化配置
├── themeStore.ts        # 主题 store 示例
├── manualThemeStore.ts  # 手动主题 store 示例
└── {moduleName}Store.ts # 新建的 store
```

## Store 模板

### Options Store（推荐）

```typescript
// src/store/{moduleName}Store.ts
import type { {ModuleName}State } from '@/types/{moduleName}'
import { defineStore } from 'pinia'

/**
 * {moduleName} 状态管理
 * 描述这个 store 的用途
 */
export const use{ModuleName}Store = defineStore('{moduleName}', {
  state: (): {ModuleName}State => ({
    // 状态定义
    data: null,
    loading: false,
    error: null,
  }),

  getters: {
    // 计算属性
    isLoaded: (state) => state.data !== null,
    hasError: (state) => state.error !== null,
  },

  actions: {
    // 同步 action
    setData(data: any) {
      this.data = data
    },

    // 异步 action
    async fetchData() {
      this.loading = true
      this.error = null
      try {
        const { data } = await useRequest(Apis.xxx.getData())
        this.data = data.value
      } catch (err) {
        this.error = err as Error
      } finally {
        this.loading = false
      }
    },

    // 重置状态
    reset() {
      this.$reset()
    },
  },
})
```

### 带持久化的 Store

```typescript
// src/store/{moduleName}Store.ts
import { defineStore } from 'pinia'
import { createPersistedState } from '@/store/persist'

export const use{ModuleName}Store = defineStore('{moduleName}', {
  state: () => ({
    token: '',
    userInfo: null,
  }),

  actions: {
    setToken(token: string) {
      this.token = token
    },
  },

  // 启用持久化
  persist: createPersistedState({
    key: '{moduleName}-storage',
    paths: ['token', 'userInfo'],  // 只持久化指定字段
  }),
})
```

## 类型定义

```typescript
// src/types/{moduleName}.ts
export interface {ModuleName}State {
  data: {DataType} | null
  loading: boolean
  error: Error | null
}

export interface {DataType} {
  id: string
  name: string
  // ...其他字段
}
```

## 使用 Store

### 在组件中使用

```vue
<script setup lang="ts">
const {moduleName}Store = use{ModuleName}Store()

// 访问状态
const data = computed(() => {moduleName}Store.data)
const loading = computed(() => {moduleName}Store.loading)

// 调用 action
onMounted(() => {
  {moduleName}Store.fetchData()
})
</script>
```

### 在 composable 中使用

```typescript
// src/composables/use{ModuleName}.ts
export function use{ModuleName}() {
  const store = use{ModuleName}Store()

  // 封装逻辑
  const doSomething = async () => {
    await store.fetchData()
  }

  return {
    data: computed(() => store.data),
    loading: computed(() => store.loading),
    doSomething,
  }
}
```

## 持久化配置

```typescript
// src/store/persist.ts
export function createPersistedState(options: {
  key: string
  paths?: string[]
}) {
  return {
    key: options.key,
    paths: options.paths,
    storage: {
      getItem: (key: string) => uni.getStorageSync(key),
      setItem: (key: string, value: string) => uni.setStorageSync(key, value),
      removeItem: (key: string) => uni.removeStorageSync(key),
    },
  }
}
```

## 注意事项

- Store 文件名使用 `{moduleName}Store.ts` 格式
- 导出的函数使用 `use{ModuleName}Store` 命名
- 复杂逻辑建议封装到 composable 中
- 敏感数据不要持久化到本地存储
