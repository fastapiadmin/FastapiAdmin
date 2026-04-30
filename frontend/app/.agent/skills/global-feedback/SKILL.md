---
name: global-feedback
description: 全局反馈组件（Toast/Message/Loading）使用指南
---

# 全局反馈组件

wot-starter 提供了全局 Toast、Message、Loading 组件，支持跨页面调用。

## 组件列表

| 组件 | 用途 | Composable |
|------|------|------------|
| GlobalToast | 轻提示 | `useGlobalToast()` |
| GlobalMessage | 确认弹窗 | `useGlobalMessage()` |
| GlobalLoading | 加载状态 | `useGlobalLoading()` |

## useGlobalToast

### 基础用法

```typescript
const { show, success, error, info, warning, close } = useGlobalToast()

// 显示提示
show('这是一条提示')

// 成功提示
success('操作成功')

// 错误提示
error('操作失败')

// 信息提示
info('提示信息')

// 警告提示
warning('警告信息')
```

### 自定义配置

```typescript
show({
  msg: '自定义提示',
  duration: 3000,           // 持续时间
  iconName: 'success',      // 图标
  position: 'middle',       // 位置：'top' | 'middle' | 'bottom'
  direction: 'vertical',    // 方向：'horizontal' | 'vertical'
})
```

## useGlobalMessage

### 确认弹窗

```typescript
const { confirm } = useGlobalMessage()

confirm({
  title: '提示',
  msg: '确定要删除吗？',
  confirmButtonText: '确定',
  cancelButtonText: '取消',
  success() {
    console.log('用户点击确定')
  },
  fail() {
    console.log('用户点击取消')
  },
})
```

### 与 Promise 结合

```typescript
const handleDelete = async () => {
  return new Promise((resolve, reject) => {
    confirm({
      title: '确认删除',
      msg: '删除后无法恢复',
      success: resolve,
      fail: reject,
    })
  })
}

try {
  await handleDelete()
  // 用户确认，执行删除
} catch {
  // 用户取消
}
```

## useGlobalLoading

### 基础用法

```typescript
const { show, hide } = useGlobalLoading()

// 显示加载
show()
show('加载中...')

// 隐藏加载
hide()
```

### 包装异步操作

```typescript
const fetchData = async () => {
  const { show, hide } = useGlobalLoading()

  show('数据加载中...')
  try {
    const data = await api.getData()
    return data
  } finally {
    hide()
  }
}
```

## 在路由守卫中使用

```typescript
// src/router/index.ts
router.beforeEach((to, from, next) => {
  if (to.name === 'protected-page') {
    const { confirm } = useGlobalMessage()

    return new Promise((resolve, reject) => {
      confirm({
        title: '需要登录',
        msg: '是否前往登录？',
        success() {
          next({ name: 'login' })
          resolve()
        },
        fail() {
          next(false)
          reject()
        },
      })
    })
  }
  next()
})
```

## 组件配置

全局组件已在 `App.ku.vue` 中配置：

```vue
<!-- App.ku.vue -->
<template>
  <GlobalToast />
  <GlobalMessage />
  <GlobalLoading />
</template>
```

## 注意事项

- 这些 composable 基于 Pinia Store 实现
- 支持跨页面调用
- 自动导入，无需手动 import
- 同时只会显示一个实例
