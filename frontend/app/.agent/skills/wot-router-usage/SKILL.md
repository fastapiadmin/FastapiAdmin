---
name: wot-router-usage
description: '@wot-ui/router 轻量级路由库使用指南'
---

# @wot-ui/router 使用指南

专为 uni-app 设计的轻量级路由库，提供类似 Vue Router 的 API。

## 核心特性

- 📝 编程式导航
- 🔄 参数传递（params + query）
- 🛡️ 导航守卫
- 📊 路由信息获取
- 🎯 TypeScript 支持

## 路由配置

```typescript
// src/router/index.ts
import { pages, subPackages } from 'virtual:uni-pages'

function generateRoutes() {
  const routes = pages.map((page) => ({
    ...page,
    path: `/${page.path}`,
  }))

  subPackages?.forEach((sub) => {
    sub.pages.forEach((page) => {
      routes.push({
        ...page,
        path: `/${sub.root}/${page.path}`,
      })
    })
  })

  return routes
}

const router = createRouter({
  routes: generateRoutes(),
})

export default router
```

## 基础导航

```typescript
const router = useRouter()
const route = useRoute()

// 字符串路径
router.push('/pages/detail/index')

// 对象形式
router.push({ path: '/pages/detail/index' })

// 命名路由
router.push({ name: 'detail' })

// 替换当前页面
router.replace({ name: 'login' })

// 返回上一页
router.back()

// 返回多级
router.go(-2)
```

## 参数传递

### Query 参数

```typescript
// 跳转
router.push({
  name: 'detail',
  query: { id: '123', type: 'product' },
})

// 获取
const route = useRoute()
const id = route.query.id
const type = route.query.type
```

### Params 参数

```typescript
// 跳转
router.push({
  name: 'detail',
  params: { id: '123' },
})

// 获取
const route = useRoute()
const id = route.params.id
```

## 导航守卫

### 全局前置守卫

```typescript
router.beforeEach((to, from, next) => {
  console.log(`导航: ${from.path} → ${to.path}`)

  // 权限检查
  if (to.meta?.requiresAuth && !isLoggedIn()) {
    next({ name: 'login' })
    return
  }

  // 异步守卫
  if (to.name === 'protected') {
    return new Promise((resolve) => {
      showConfirm({
        title: '确认访问',
        success: () => { next(); resolve() },
        fail: () => { next(false); resolve() },
      })
    })
  }

  next()
})
```

### 全局后置钩子

```typescript
router.afterEach((to, from) => {
  console.log(`页面切换完成: ${to.path}`)

  // 页面统计
  trackPageView(to.path)
})
```

## 路由信息

```typescript
const route = useRoute()

// 当前路径
route.path        // '/subPages/detail/index'

// 路由名称
route.name        // 'detail'

// 查询参数
route.query       // { id: '123' }

// 路径参数
route.params      // { id: '123' }

// 完整路径
route.fullPath    // '/subPages/detail/index?id=123'

// 路由元信息
route.meta        // { requiresAuth: true }
```

## 页面定义

```vue
<script setup lang="ts">
definePage({
  name: 'detail',           // 路由名称
  layout: 'default',        // 布局
  meta: {
    requiresAuth: true,     // 自定义元信息
  },
  style: {
    navigationBarTitleText: '详情',
  },
})
</script>
```

## TabBar 页面跳转

```typescript
// TabBar 页面使用 reLaunch
router.push({
  name: 'home',
  reLaunch: true,  // 或自动识别 tabBar 页面
})
```

## 注意事项

- uni-app 路由限制仍然存在（如页面栈限制）
- TabBar 页面需要特殊处理
- 导航守卫中的异步操作需要返回 Promise
- 参数过长时考虑使用全局状态传递
