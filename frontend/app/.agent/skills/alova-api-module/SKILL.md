---
name: alova-api-module
description: 快速创建 Alova 请求模块和 Mock 数据
---

# Alova API 模块生成器

基于 Alova 请求库创建 API 模块和 Mock 数据。

## 目录结构

```
src/api/
├── core/
│   └── instance.ts      # Alova 实例配置
├── mock/
│   ├── modules/         # Mock 模块目录
│   │   ├── user.ts      # 用户相关 Mock
│   │   └── product.ts   # 商品相关 Mock
│   ├── mockAdapter.ts   # Mock 适配器
│   └── utils/           # Mock 工具函数
├── apiDefinitions.ts    # API 定义（自动生成）
├── createApis.ts        # API 创建函数
└── index.ts             # API 导出入口
```

## 创建 Mock 模块

### 模块模板

```typescript
// src/api/mock/modules/{moduleName}.ts
import { defineMock } from '@alova/mock'

export default defineMock({
  // GET 请求
  '/api/{moduleName}/list': () => {
    return {
      code: 200,
      message: 'success',
      data: {
        list: [],
        total: 0,
      },
    }
  },

  // POST 请求
  '[POST]/api/{moduleName}/create': ({ data }) => {
    return {
      code: 200,
      message: '创建成功',
      data: { id: Date.now(), ...data },
    }
  },

  // 带路径参数
  '/api/{moduleName}/{id}': ({ params }) => {
    return {
      code: 200,
      message: 'success',
      data: { id: params.id },
    }
  },
})
```

### 注册 Mock 模块

```typescript
// src/api/mock/mockAdapter.ts
import userMock from './modules/user'
import productMock from './modules/product'
// 导入新模块
import newModuleMock from './modules/{moduleName}'

export default createAlovaMockAdapter([
  userMock,
  productMock,
  newModuleMock,  // 注册新模块
], {
  enable: import.meta.env.DEV,
  delay: 300,
})
```

## 使用 API

### useRequest Hook

```typescript
// 基础请求
const { data, loading, error, send } = useRequest(
  Apis.user.getUserInfo({ id: '123' }),
  { immediate: true }
)

// 手动触发
const { send: fetchData } = useRequest(
  (id: string) => Apis.user.getUserInfo({ id }),
  { immediate: false }
)
await fetchData('123')
```

### usePagination Hook

```typescript
const {
  data: list,
  page,
  pageSize,
  total,
  loading,
  isLastPage,
  refresh,
  reload,
} = usePagination(
  (page, pageSize) => Apis.product.getList({ page, pageSize }),
  {
    initialPage: 1,
    initialPageSize: 10,
    total: (res) => res.total,
    data: (res) => res.list,
  }
)
```

## 响应数据类型

```typescript
// src/api/types/{moduleName}.ts
export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export interface PaginatedData<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}

export interface UserInfo {
  id: string
  name: string
  avatar: string
}
```

## 配置文件

```typescript
// alova.config.ts
export default {
  input: 'https://api.example.com/openapi.json',
  output: 'src/api',
  // OpenAPI 自动生成配置
}
```
