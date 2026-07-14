# 微信云开发规则

## 概述
本文档定义了使用微信云开发（CloudBase）为小程序提供后端服务的开发规范。
当 PRD 分析判定小程序需要后端服务且目标平台包含微信小程序时，在前端开发过程中同步生成云函数代码。部署操作在用户确认后通过 CloudBase MCP 工具完成。

## 适用条件
- 当小程序需要后端服务时启用（Taro 项目默认支持编译为微信小程序）
- `Taro.cloud` API 只在微信小程序（weapp）运行时可用，H5 预览时走 mock 数据
- 所有涉及 `Taro.cloud` 的代码必须用 `process.env.TARO_ENV === 'weapp'` 包裹

---

## 开发流程

### Phase A：后端需求分析

在 PRD 分析阶段（第一阶段）同步完成，识别需要云端支持的功能：

1. 需要用户身份识别 → 云函数 `login`（获取 openid）
2. 需要数据持久化 → 对应集合 + 云函数（CRUD）
3. 需要文件上传/下载 → 云存储 API

输出格式：
```
### 数据库集合设计
| 集合名 | 用途 | 核心字段 | 索引字段 |
|--------|------|----------|----------|
| users | 用户信息 | _openid, nickname, avatar, createTime | _openid |
| orders | 订单 | _openid, items, status, createTime | _openid, status |

### 云函数列表
| 函数名 | 用途 | 入参 | 返回 |
|--------|------|------|------|
| login | 获取用户openid | 无 | { openid } |
| getOrders | 查询订单 | { status? } | { orders: [] } |
```

### Phase B：生成云函数代码

在前端页面开发阶段（第六阶段）同步完成。每开发一个需要后端数据的页面时，同时生成对应的云函数代码，写入项目根目录的 `cloudfunctions/` 目录。每个云函数一个独立子目录。

### Phase C：前端调用层

前端统一使用 `src/services/cloud.ts`（模板已预置）封装调用：
- 微信平台（weapp）：走真实 `Taro.cloud.callFunction`
- 非微信平台（H5 预览、抖音、支付宝）：走 mock 数据

页面通过 service 层获取数据。涉及云函数的 mock 文件命名为 `src/data/<functionName>.ts`，`cloud.ts` 会在非微信环境下按函数名自动加载对应文件。

### Phase D：通过 MCP 部署（用户确认后执行）

用户确认部署后，使用 CloudBase MCP 工具完成部署（MCP 自动处理认证，无需主动管理登录状态）。

部署成功后，通过 MCP 的 `envQuery` 工具获取当前环境 ID，然后将 `app.tsx` 中 `Taro.cloud.init()` 的 `env` 参数设置为真实的环境 ID。如果 `envQuery` 无法获取，则询问用户提供环境 ID。

### Phase E：验证（部署后执行）

通过 MCP 调用云函数验证部署成功，输出结果摘要。

---

## 云函数代码规范

### 目录结构
```
cloudfunctions/
├── login/
│   ├── index.js
│   └── package.json
├── getUsers/
│   ├── index.js
│   └── package.json
└── createOrder/
    ├── index.js
    └── package.json
```

### 入口文件模板（index.js）
```javascript
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

exports.main = async (event, context) => {
  try {
    const wxContext = cloud.getWXContext()
    const openid = wxContext.OPENID

    // 业务逻辑...
    const result = null // 替换为实际逻辑

    return { code: 0, message: 'success', data: result }
  } catch (err) {
    console.error('[functionName] error:', err)
    return { code: -1, message: err.message || '服务异常', data: null }
  }
}
```

### package.json 模板
```json
{
  "name": "functionName",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "wx-server-sdk": "~2.6.3"
  }
}
```

### 编码规范
- 函数命名：camelCase，动词开头（getXxx, createXxx, updateXxx, deleteXxx）
- 必须调用 `cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })`
- 通过 `cloud.getWXContext().OPENID` 获取用户身份（免鉴权）
- 统一返回格式：`{ code: number, message: string, data: any }`
  - code=0 表示成功，code<0 表示失败
- 必须有 try-catch 错误处理
- 日志使用 `console.error('[函数名]', err)` 格式
- 云函数使用 CommonJS（`require` / `exports.main`），不使用 ESM

---

## 数据库规范

### 集合命名
- 小写字母 + 下划线：`users`, `user_profiles`, `order_items`
- 避免使用数据库保留字

### 文档结构约定
- 用户相关数据必须包含 `_openid` 字段用于权限控制
- 时间字段使用 `db.serverDate()` 写入
- 必须为高频查询字段建立索引

### 安全规则
- 默认规则："仅创建者可读写"（通过 _openid 匹配）
- 公开数据（如商品列表）：所有人可读，仅管理员可写

---

## 前端调用规范

### 初始化（app.tsx）

在 App 组件中初始化云开发，必须做平台判断：
```tsx
import { useEffect } from 'react'

function App(props) {
  useEffect(() => {
    if (process.env.TARO_ENV === 'weapp') {
      Taro.cloud.init({ env: 'your-env-id', traceUser: true })
    }
  }, [])
  return props.children
}
```

注意：`process.env.TARO_ENV` 在编译时被替换为常量，非微信平台的 cloud 代码会被 tree shaking 移除。

### Service 层封装（src/services/cloud.ts）

项目模板中已预置 `src/services/cloud.ts`，提供统一的云调用封装：
- 微信平台：走真实云函数调用
- 非微信平台（H5 预览、抖音、支付宝）：走 mock 数据

开发云函数时，只需修改此文件中的 mock fallback 逻辑为真实云调用即可。

### 页面中使用
```typescript
import { callFunction } from '@/services/cloud'

const [orders, setOrders] = useState<Order[]>([])

useEffect(() => {
  callFunction<Order[]>('getOrders', { status: 'pending' })
    .then(setOrders)
    .catch(err => console.error('[OrderPage]', err))
}, [])
```

---

## MCP 部署操作

### 配置 MCP

部署前需确认用户 IDE 已配置 CloudBase MCP。如果 MCP 工具不可用，通过以下方式帮助用户配置：

**方式一（推荐）：自动触发安装**

使用终端工具执行以下命令（根据操作系统选择），系统会自动打开 Trae 的 MCP 配置确认窗口：

- macOS: `open "trae-cn://trae.ai-ide/mcp-import?type=stdio&name=cloudbase&config=eyJjb21tYW5kIjoibnB4IiwiYXJncyI6WyIteSIsIkBjbG91ZGJhc2UvY2xvdWRiYXNlLW1jcEBsYXRlc3QiXX0%3D"`
- Windows: `start "" "trae-cn://trae.ai-ide/mcp-import?type=stdio&name=cloudbase&config=eyJjb21tYW5kIjoibnB4IiwiYXJncyI6WyIteSIsIkBjbG91ZGJhc2UvY2xvdWRiYXNlLW1jcEBsYXRlc3QiXX0%3D"`

执行后告知用户：
1. 在弹出的确认窗口中点击「确认」（添加 CloudBase MCP 服务）
2. 在弹出的 MCP 管理面板中，点击「+ 添加」按钮左侧的 🔄 按钮刷新，等待 cloudbase 下的工具列表加载成功
3. 回复「已配置」继续部署

**重要**：MCP 工具只有在用户发起新一轮对话后才能被检测到，因此必须等待用户回复后再继续部署流程，不要尝试在当前轮次中轮询检测。

**方式二：手动配置（仅当方式一失败时使用）**

1. 打开「设置」→「MCP」
2. 点击「+ 添加」→「手动配置」
3. 将以下 JSON 粘贴到输入框中并点击确认：

```json
{
  "mcpServers": {
    "cloudbase": {
      "command": "npx",
      "args": [
        "-y",
        "@cloudbase/cloudbase-mcp@latest"
      ]
    }
  }
}
```

用户确认配置完成后，可直接调用以下 MCP 工具。

### 部署顺序
1. 创建所有数据库集合
2. 为集合创建索引
3. 部署所有云函数
4. 调用 login 函数验证部署成功

### 创建数据库集合
- 工具：`writeNoSqlDatabaseStructure`
- 参数：`action: "createCollection"`, `collectionName: "xxx"`

### 创建索引
- 工具：`writeNoSqlDatabaseStructure`
- 参数：`action: "updateCollection"`, `collectionName: "xxx"`, 包含 CreateIndexes 配置

### 部署云函数
- 工具：`manageFunctions`
- 参数：`action: "createFunction"`, `functionName: "xxx"`, `functionRootPath: "<项目路径>/cloudfunctions"`

### 验证部署
- 工具：`manageFunctions`
- 参数：`action: "invoke"`, `functionName: "login"`, `params: {}`

### 输出部署结果
部署完成后，向用户输出摘要（环境 ID 从部署阶段 `envQuery` 获取的真实值动态替换）：
```
✅ 后端部署完成：
- 已部署云函数：login, getUsers, createOrder（共 3 个）
- 已创建数据库集合：users, orders（共 2 个）
- 验证结果：login 函数调用成功

🔗 云开发管理控制台：https://tcb.cloud.tencent.com/dev?envId=<环境ID>#/scf
   您可以点击上方链接，在腾讯云控制台中查看和管理云函数、数据库等资源。
```

---

## 约束

- **禁止执行任何 CLI 命令**（tcb、cloudbase、npm 等），所有云端操作通过 MCP 工具完成
- **H5 预览模式下使用 mock 数据**，不调用真实云端
- **env-id 在部署阶段确定**：生成代码时 `Taro.cloud.init({ env: '' })` 可留空或用任意占位，部署阶段通过 MCP `envQuery` 获取真实环境 ID 后修改 `app.tsx`
- **云函数使用 CommonJS**：`require` / `exports.main`，不使用 ESM
- **平台判断是强制的**：所有涉及 `Taro.cloud` 的代码必须用 `process.env.TARO_ENV === 'weapp'` 包裹
- **MCP 认证由 MCP 内部自动处理**：Skill 不需要主动调用 auth 工具或管理登录状态
