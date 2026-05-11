# GlobalLoading 全局加载组件

## 概述

GlobalLoading 是基于 `wot-design-uni` 的 `wd-toast` 组件封装的全局加载组件，可以结合`axios`、`alova`等请求库使用，显示加载状态，通过 Pinia 状态管理实现全局调用，用于显示数据加载、操作处理等场景的等待状态。

## 组件特性

- 基于 `wd-toast` 组件封装
- 显示加载动画，默认不自动关闭
- 支持遮罩层覆盖，防止用户操作
- 自动页面路径检测，确保在正确页面显示
- 虚拟节点设计，不在 DOM 中创建额外层级

## 安装使用

### 1. 注册全局组件

在 `App.vue` 或根组件中注册：

```vue
<template>
  <div>
    <!-- 其他内容 -->
    <GlobalLoading />
  </div>
</template>
```

### 2. 在组件中使用

```typescript
import { useGlobalLoading } from '@/composables/useGlobalLoading'

const loading = useGlobalLoading()
```

## API 文档

### 基础用法

```typescript
// 显示加载（字符串参数）
loading.loading('加载中...')

// 显示加载（配置对象）
loading.loading({
  msg: '数据加载中',
  cover: true
})

// 关闭加载
loading.close()
```

### 方法说明

#### loading(option)
显示加载状态

```typescript
// 简单文本
loading.loading('请稍候...')

// 自定义配置
loading.loading({
  msg: '数据处理中，请稍候',
  cover: false,
  position: 'middle'
})
```

**默认配置：**
- 图标：loading（旋转动画）
- 持续时间：0（不自动关闭）
- 遮罩：true
- 位置：middle
- 显示：true

#### close()
关闭加载状态

```typescript
loading.close()
```

## 参数说明

### ToastOptions

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| msg | string | - | 加载提示文本 |
| iconName | string | 'loading' | 图标名称（固定为loading） |
| duration | number | 0 | 持续时间(ms)，0表示不自动关闭 |
| cover | boolean | true | 是否显示遮罩层 |
| position | string | 'middle' | 显示位置：'top' \| 'middle' \| 'bottom' |
| show | boolean | - | 是否显示（内部使用） |

### 方法参数

支持两种参数类型：

1. **字符串参数**：直接传入加载提示文本
2. **选项对象**：传入完整的 ToastOptions 配置

## 使用示例

### 基础示例

```typescript
export default {
  setup() {
    const loading = useGlobalLoading()

    const handleLoad = async () => {
      loading.loading('加载中...')

      try {
        // 模拟异步操作
        await new Promise(resolve => setTimeout(resolve, 2000))
        console.log('加载完成')
      }
      finally {
        loading.close()
      }
    }

    return {
      handleLoad
    }
  }
}
```

### 网络请求示例

```typescript
async function fetchData() {
  const loading = useGlobalLoading()

  try {
    loading.loading('获取数据中...')
    const response = await api.getData()
    return response.data
  }
  catch (error) {
    console.error('获取数据失败:', error)
    throw error
  }
  finally {
    loading.close()
  }
}
```

### 表单提交示例

```typescript
async function handleSubmit(formData) {
  const loading = useGlobalLoading()
  const toast = useGlobalToast()

  try {
    loading.loading('提交中，请稍候...')
    await submitForm(formData)
    toast.success('提交成功')
  }
  catch (error) {
    toast.error(`提交失败：${error.message}`)
  }
  finally {
    loading.close()
  }
}
```

### 文件上传示例

```typescript
async function uploadFile(file) {
  const loading = useGlobalLoading()

  try {
    loading.loading({
      msg: '文件上传中...',
      cover: true // 防止用户重复操作
    })

    const result = await uploadToServer(file)
    return result
  }
  finally {
    loading.close()
  }
}
```

### 批量操作示例

```typescript
async function batchProcess(items) {
  const loading = useGlobalLoading()

  try {
    loading.loading(`处理中 (0/${items.length})`)

    for (let i = 0; i < items.length; i++) {
      // 更新进度提示
      loading.loading(`处理中 (${i + 1}/${items.length})`)
      await processItem(items[i])
    }
  }
  finally {
    loading.close()
  }
}
```

### 自定义样式示例

```typescript
function showCustomLoading() {
  loading.loading({
    msg: '自定义加载样式',
    cover: false, // 不显示遮罩
    position: 'top' // 显示在顶部
  })
}
```

## 实现原理

### 状态管理
- 使用 Pinia 管理全局状态
- 状态包含：`loadingOptions`（加载配置）、`currentPage`（当前页面路径）

### 页面检测机制
- 调用加载方法时记录当前页面路径
- 组件监听状态变化时验证页面路径
- 确保加载状态在正确的页面显示

### 组件配置
```typescript
export default {
  options: {
    virtualHost: true, // 虚拟节点
    addGlobalClass: true, // 支持全局样式
    styleIsolation: 'shared' // 样式隔离共享
  }
}
```

## 最佳实践

1. **及时关闭**
   ```typescript
   // ✅ 推荐：使用 try-finally 确保关闭
   try {
     loading.loading('处理中...')
     await doSomething()
   }
   finally {
     loading.close()
   }

   // ❌ 避免：可能忘记关闭
   loading.loading('处理中...')
   await doSomething()
   loading.close() // 如果上面抛出异常，此行不会执行
   ```

2. **合理使用遮罩**
   ```typescript
   // 重要操作，防止用户干扰
   loading.loading({
     msg: '正在保存...',
     cover: true
   })

   // 轻量操作，允许用户其他操作
   loading.loading({
     msg: '加载中...',
     cover: false
   })
   ```

3. **提供清晰的提示文本**
   ```typescript
   // ✅ 清晰明确
   loading.loading('正在上传文件...')
   loading.loading('正在保存数据...')

   // ❌ 模糊不清
   loading.loading('请稍候...')
   loading.loading('处理中...')
   ```

4. **长时间操作显示进度**
   ```typescript
   // 对于耗时较长的操作，提供进度信息
   for (let i = 0; i < items.length; i++) {
     loading.loading(`处理进度：${i + 1}/${items.length}`)
     await processItem(items[i])
   }
   ```

5. **避免嵌套调用**
   ```typescript
   // ❌ 避免嵌套
   loading.loading('外层操作...')
   await outerOperation()
   loading.loading('内层操作...') // 会覆盖外层
   await innerOperation()
   loading.close() // 只关闭了内层

   // ✅ 推荐：合并操作或使用状态管理
   loading.loading('正在执行操作...')
   try {
     await outerOperation()
     await innerOperation()
   }
   finally {
     loading.close()
   }
   ```

## 使用场景

1. **数据加载**：页面初始化、列表刷新
2. **表单提交**：用户操作提交、数据保存
3. **文件操作**：上传、下载、删除文件
4. **网络请求**：API 调用、数据同步
5. **批量处理**：多个项目的批量操作
6. **页面跳转**：路由切换前的准备工作

## 注意事项

1. **必须手动关闭**：加载组件不会自动关闭，务必在操作完成后调用 `close()`
2. **防止内存泄漏**：在组件销毁前确保关闭加载状态
3. **单例模式**：同时只能显示一个加载状态，新的调用会覆盖旧的
4. **页面路径检测**：组件会自动在对应页面显示，切换页面时会自动关闭
5. **遮罩层影响**：开启遮罩时会阻止用户操作，谨慎使用

## 错误处理

```typescript
// 推荐的错误处理模式
async function safeOperation() {
  const loading = useGlobalLoading()
  const toast = useGlobalToast()

  try {
    loading.loading('处理中...')
    await riskyOperation()
    toast.success('操作成功')
  }
  catch (error) {
    console.error('操作失败:', error)
    toast.error('操作失败，请重试')
  }
  finally {
    // 无论成功或失败都要关闭加载
    loading.close()
  }
}
