# GlobalToast 全局提示组件

## 概述

GlobalToast 是基于 `wot-design-uni` 的 `wd-toast` 组件封装的全局提示组件，通过 Pinia 状态管理实现全局调用。

## 组件特性

- 基于 `wd-toast` 组件封装
- 支持多种提示类型：成功、错误、信息、警告
- 自动页面路径检测，确保在正确页面显示
- 支持自定义图标、位置、持续时间等
- 虚拟节点设计，不在 DOM 中创建额外层级

## 安装使用

### 1. 注册全局组件

在 `App.vue` 或根组件中注册：

```vue
<template>
  <div>
    <!-- 其他内容 -->
    <GlobalToast />
  </div>
</template>
```

### 2. 在组件中使用

```typescript
import { useGlobalToast } from '@/composables/useGlobalToast'

const toast = useGlobalToast()
```

## API 文档

### 基础用法

```typescript
// 普通提示
toast.show('这是一条提示信息')

// 自定义配置
toast.show({
  msg: '自定义提示',
  duration: 3000,
  position: 'top'
})
```

### 快捷方法

#### success(option)
成功提示，显示绿色成功图标

```typescript
toast.success('操作成功')
toast.success({
  msg: '保存成功',
  duration: 2000
})
```

**默认配置：**
- 图标：success
- 持续时间：1500ms

#### error(option)
错误提示，显示红色错误图标

```typescript
toast.error('操作失败')
toast.error({
  msg: '网络错误，请重试',
  duration: 3000
})
```

**默认配置：**
- 图标：error
- 方向：vertical（垂直布局）

#### info(option)
信息提示，显示蓝色信息图标

```typescript
toast.info('这是一条信息')
toast.info({
  msg: '请注意查看',
  position: 'top'
})
```

**默认配置：**
- 图标：info

#### warning(option)
警告提示，显示黄色警告图标

```typescript
toast.warning('警告信息')
toast.warning({
  msg: '请谨慎操作',
  iconName: 'warning'
})
```

**默认配置：**
- 图标：warning

#### close()
手动关闭提示

```typescript
toast.close()
```

## 参数说明

### ToastOptions

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| msg | string | - | 提示内容 |
| duration | number | 2000 | 持续时间(ms)，0表示不自动关闭 |
| position | string | 'middle' | 显示位置：'top' \| 'middle' \| 'bottom' |
| iconName | string | - | 图标名称 |
| direction | string | - | 布局方向：'horizontal' \| 'vertical' |
| cover | boolean | false | 是否显示遮罩 |
| show | boolean | - | 是否显示（内部使用） |

### 方法参数

所有方法都支持两种参数类型：

1. **字符串参数**：直接传入提示文本
2. **选项对象**：传入完整的 ToastOptions 配置

## 使用示例

### 基础示例

```typescript
export default {
  setup() {
    const toast = useGlobalToast()

    const handleSuccess = () => {
      toast.success('操作成功！')
    }

    const handleError = () => {
      toast.error('操作失败，请重试')
    }

    const handleCustom = () => {
      toast.show({
        msg: '自定义提示',
        duration: 5000,
        position: 'top',
        iconName: 'info'
      })
    }

    return {
      handleSuccess,
      handleError,
      handleCustom
    }
  }
}
```

### 异步操作示例

```typescript
async function handleSubmit() {
  const toast = useGlobalToast()

  try {
    // 提交数据
    await submitData()
    toast.success('提交成功')
  }
  catch (error) {
    toast.error(`提交失败：${error.message}`)
  }
}
```

### 长文本提示

```typescript
function showLongMessage() {
  toast.info({
    msg: '这是一条很长的提示信息，可能需要更长的显示时间',
    duration: 4000,
    position: 'top'
  })
}
```

## 实现原理

### 状态管理
- 使用 Pinia 管理全局状态
- 状态包含：`toastOptions`（提示配置）、`currentPage`（当前页面路径）

### 页面检测机制
- 调用提示方法时记录当前页面路径
- 组件监听状态变化时验证页面路径
- 确保提示信息在正确的页面显示

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

1. **选择合适的提示类型**
   - 成功操作使用 `success()`
   - 错误信息使用 `error()`
   - 一般信息使用 `info()`
   - 警告信息使用 `warning()`

2. **控制显示时长**
   - 简短消息：1500-2000ms
   - 长消息：3000-4000ms
   - 重要消息：可设置为0，用户手动关闭

3. **位置选择**
   - 一般提示：middle（默认）
   - 不遮挡内容：top 或 bottom
   - 重要提示：middle + cover

4. **避免频繁调用**
   ```typescript
   // ❌ 避免快速连续调用
   toast.success('第一条')
   toast.success('第二条') // 会覆盖第一条

   // ✅ 推荐做法
   toast.success('操作完成')
   ```

## 注意事项

1. 组件需要在应用根组件中注册才能正常使用
2. 提示会自动在对应页面显示，切换页面时会自动关闭
3. 同时只能显示一个提示，新的提示会覆盖旧的提示
4. 使用 `duration: 0` 时记得手动调用 `close()` 关闭
