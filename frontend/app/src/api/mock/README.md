# API Mock 数据

本目录包含了项目中使用的 API 模拟数据，用于开发和测试环境。

## 目录结构

```
mock/
├── modules/                       # 按模块分类的模拟数据
│   ├── common.ts                 # 通用模拟处理
│   ├── loginInterface.ts         # 登录相关接口的模拟数据
│   ├── mdataInterface.ts         # 主数据相关接口的模拟数据
│   ├── vehsaleusesignInterface.ts # 车销使用签收相关接口的模拟数据
│   ├── vehsaleusesignarvInterface.ts # 车销使用签收到货相关接口的模拟数据
│   ├── user.ts                   # 用户相关的模拟数据
│   ├── university.ts             # 大学相关的模拟数据
│   └── feedback.ts               # 反馈相关的模拟数据
├── utils/                         # 工具目录
│   ├── index.ts                  # 工具导出文件
│   └── generators.ts             # 模拟数据生成工具
└── mockAdapter.ts                # 模拟适配器配置
```

## 使用方法

模拟数据已经通过 `@alova/mock` 和 `@alova/adapter-uniapp` 集成到项目中。在开发环境中，API 请求会自动使用模拟数据进行响应。

### 启用/禁用模拟

在 `mockAdapter.ts` 中，可以通过修改 `enable` 选项来启用或禁用模拟：

```typescript
const mockAdapter = createAlovaMockAdapter(allMocks, {
  // ...
  enable: true, // 设置为 false 可禁用模拟
  // ...
})
```

### 添加新的模拟数据

1. 在 `modules` 目录下创建新的模块文件或在现有文件中添加
2. 使用 `defineMock` 函数定义模拟数据
3. 在 `mockAdapter.ts` 中导入并添加到 `allMocks` 数组中

示例：

```typescript
// modules/example.ts
import { defineMock } from '@alova/mock'

// mockAdapter.ts
import exampleMocks from './modules/example'

export default defineMock({
  '[GET]/api/example': () => {
    return {
      code: 200,
      data: { /* 模拟数据 */ },
      message: 'success'
    }
  }
})

const allMocks = [
  // ...
  exampleMocks
]
```

## 模拟数据生成工具

在 `utils/generators.ts` 中提供了一系列用于生成模拟数据的工具函数，可以在各个模块中复用：

```typescript
import { generateMockData } from '../utils'

// 生成随机ID
const id = generateMockData.id()

// 生成随机名称
const name = generateMockData.name('前缀')

// 生成随机数组
const array = generateMockData.array(index => ({
  id: generateMockData.id(),
  name: generateMockData.name(`项目${index}`)
}), 10)

// 生成基础响应对象
const response = generateMockData.baseResponse(data)

// 生成列表响应对象
const listResponse = generateMockData.listResponse(items, total, more)

// 生成业务对象
const user = generateMockData.user()
const goods = generateMockData.goods(0)
const vehSaleEmp = generateMockData.vehSaleEmp(0)
```

## 注意事项

1. 模拟数据应尽量接近真实数据结构，以便于开发和测试
2. 对于需要保持一致性的数据（如ID引用），可以使用固定值而非随机生成
3. 可以使用请求参数来定制模拟响应，例如分页、筛选等
4. 模拟数据应包含各种场景，包括成功和失败的情况
