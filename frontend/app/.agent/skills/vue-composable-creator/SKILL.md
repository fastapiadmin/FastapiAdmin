---
name: vue-composable-creator
description: 快速创建 Vue 3 组合式函数
---

# Vue Composable 创建器

快速创建符合 wot-starter 项目规范的 Vue 3 组合式函数。

## 目录结构

```
src/composables/
├── types/               # 类型定义目录
│   └── theme.ts
├── useGlobalToast.ts    # 全局 Toast
├── useGlobalMessage.ts  # 全局 Message
├── useGlobalLoading.ts  # 全局 Loading
├── useTheme.ts          # 主题管理
├── useManualTheme.ts    # 手动主题管理
├── useTabbar.ts         # TabBar 控制
└── use{Name}.ts         # 新建的 composable
```

## Composable 模板

### 基础模板

```typescript
// src/composables/use{Name}.ts
import { ref, computed, onMounted, onUnmounted } from 'vue'

/**
 * {描述这个 composable 的用途}
 * @returns {返回值描述}
 */
export function use{Name}() {
  // 响应式状态
  const state = ref<StateType>(initialValue)
  const loading = ref(false)

  // 计算属性
  const computedValue = computed(() => {
    return state.value
  })

  // 方法
  function doSomething() {
    // 业务逻辑
  }

  async function asyncAction() {
    loading.value = true
    try {
      // 异步操作
    } finally {
      loading.value = false
    }
  }

  // 生命周期
  onMounted(() => {
    // 初始化
  })

  onUnmounted(() => {
    // 清理
  })

  return {
    state,
    loading,
    computedValue,
    doSomething,
    asyncAction,
  }
}
```

### 结合 Pinia Store

```typescript
// src/composables/use{Name}.ts
import { computed } from 'vue'
import { storeToRefs } from 'pinia'

export function use{Name}() {
  const store = use{Name}Store()

  // 使用 storeToRefs 保持响应性
  const { data, loading } = storeToRefs(store)

  // 封装 action
  async function refresh() {
    await store.fetchData()
  }

  return {
    data,
    loading,
    refresh,
  }
}
```

### 带参数的 Composable

```typescript
// src/composables/use{Name}.ts
interface Use{Name}Options {
  immediate?: boolean
  onSuccess?: (data: any) => void
  onError?: (error: Error) => void
}

export function use{Name}(options: Use{Name}Options = {}) {
  const { immediate = true, onSuccess, onError } = options

  const data = ref<DataType | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  async function execute() {
    loading.value = true
    error.value = null
    try {
      const result = await fetchData()
      data.value = result
      onSuccess?.(result)
    } catch (err) {
      error.value = err as Error
      onError?.(err as Error)
    } finally {
      loading.value = false
    }
  }

  if (immediate) {
    execute()
  }

  return {
    data,
    loading,
    error,
    execute,
  }
}
```

## 项目示例参考

### useGlobalToast

```typescript
// 全局 Toast 提示
export const useGlobalToast = defineStore('global-toast', {
  actions: {
    show(option: ToastOptions | string) { /* ... */ },
    success(option: ToastOptions | string) { /* ... */ },
    error(option: ToastOptions | string) { /* ... */ },
    info(option: ToastOptions | string) { /* ... */ },
    warning(option: ToastOptions | string) { /* ... */ },
    close() { /* ... */ },
  },
})
```

### useTheme

```typescript
// 主题管理
export function useTheme() {
  const store = useThemeStore()

  return {
    theme: computed(() => store.theme),
    isDark: computed(() => store.isDark),
    themeVars: computed(() => store.themeVars),
  }
}
```

## 使用方式

```vue
<script setup lang="ts">
// 自动导入，无需手动 import
const { data, loading, execute } = use{Name}({
  immediate: false,
  onSuccess: (data) => {
    console.log('成功:', data)
  },
})

// 手动执行
const handleClick = () => {
  execute()
}
</script>
```

## 注意事项

- 文件名使用 `use{Name}.ts` 格式
- 导出函数使用 `use{Name}` 命名
- 类型定义放在 `types/` 目录或文件顶部
- 自动导入已配置，无需手动 import
- 复用 Pinia Store 时使用 `storeToRefs` 保持响应性
