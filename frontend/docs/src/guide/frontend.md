---
title: 前端开发指南
---
# FastApiAdmin 项目前端

## 📖 项目介绍

### 项目概述

**FastApiAdmin** 前端是一个基于 Vue3 + Vite + TypeScript + Element-Plus 构建的现代化后台管理系统前端模板。

+ 🎨 **现代化技术栈**：Vue 3 + TypeScript + Vite + Element Plus
+ 🚀 **高性能**：Vite 构建，快速热重载
+ 📱 **响应式设计**：适配桌面和移动端
+ 🌙 **主题切换**：支持明暗主题
+ 🌍 **国际化**：多语言支持
+ 🔧 **开箱即用**：完整的后台管理功能
+ 🎯 **TypeScript**：完整的类型支持
+ 📦 **组件化**：高度模块化的架构

### 核心特性

#### 🎨 界面功能

+ ✅ 暗色主题/亮色主题切换
+ ✅ 多种布局模式（左侧、顶部、混合）
+ ✅ 动态面包屑导航
+ ✅ 标签页导航（TagsView）
+ ✅ 快捷开始功能

#### 🔐 权限管理

+ ✅ 基于角色的权限控制
+ ✅ 动态路由生成
+ ✅ 菜单权限控制
+ ✅ 按钮级别的权限控制

#### 📊 数据管理

+ ✅ 统一的API接口管理
+ ✅ 状态管理（Pinia）
+ ✅ 本地存储管理
+ ✅ 请求拦截和响应处理

#### 🛠️ 开发体验

+ ✅ TypeScript 支持
+ ✅ 自动导入（Auto Import）
+ ✅ 组件自动注册
+ ✅ UnoCSS 原子化CSS
+ ✅ ESLint + Prettier 代码规范
+ ✅ Husky Git 提交规范

## 🏗️ 技术栈

### 核心框架

+ **Vue 3** - 渐进式前端框架
+ **TypeScript** - 类型安全的JavaScript
+ **Vite** - 下一代前端构建工具
+ **Element Plus** - Vue3 UI组件库

### 状态管理

+ **Pinia** - Vue3 官方状态管理库

### 构建工具

+ **Vite** - 快速的构建工具
+ **UnoCSS** - 原子化CSS引擎
+ **ESLint** - 代码检查工具
+ **Prettier** - 代码格式化工具

### HTTP 客户端

+ **Axios** - HTTP请求库

### 路由管理

+ **Vue Router 4** - Vue3 路由管理

### 国际化

+ **Vue I18n** - Vue 国际化插件

### 图表库

+ **ECharts** - 百度开源图表库

### 富文本编辑器

+ **WangEditor** - 轻量级富文本编辑器

## ⚙️ 环境配置

### 环境变量说明

项目支持多种环境配置：

#### 开发环境 (.env.development)

```bash
# 应用配置
VITE_APP_TITLE=FastApiAdmin
VITE_APP_ENV=development

# API 配置
VITE_APP_API_BASE_URL=http://localhost:8000
VITE_APP_API_TIMEOUT=10000

# 其他配置
VITE_APP_ROUTER_HISTORY=hash
VITE_APP_PUBLIC_PATH=/
```

#### 生产环境 (.env.production)

```bash
# 应用配置
VITE_APP_TITLE=FastApiAdmin
VITE_APP_ENV=production

# API 配置
VITE_APP_API_BASE_URL=https://api.yourdomain.com
VITE_APP_API_TIMEOUT=15000

# 其他配置
VITE_APP_ROUTER_HISTORY=history
VITE_APP_PUBLIC_PATH=/
```

#### 测试环境 (.env.test)

```bash
# 应用配置
VITE_APP_TITLE=FastApiAdmin Test
VITE_APP_ENV=test

# API 配置
VITE_APP_API_BASE_URL=https://test-api.yourdomain.com
VITE_APP_API_TIMEOUT=15000
```

### 环境变量使用

在代码中使用环境变量：

```typescript
// src/config/index.ts
export const config = {
  title: import.meta.env.VITE_APP_TITLE,
  env: import.meta.env.VITE_APP_ENV,
  api: {
    baseURL: import.meta.env.VITE_APP_API_BASE_URL,
    timeout: Number(import.meta.env.VITE_APP_API_TIMEOUT)
  }
}
```

## 📁 项目结构详解

### 完整目录结构

```plain
FastapiAdmin/frontend/
├── 📁 .husky/                 # Git Hooks 配置
│   ├── pre-commit            # 提交前钩子
│   ├── commit-msg            # 提交信息钩子
│   └── ...                   # 其他 Git 钩子
├── 📁 node_modules/          # 依赖包目录
├── 📁 public/                # 静态资源目录
│   ├── background.svg        # 背景图片
│   ├── favicon.png           # 网站图标
│   └── logo.png              # 网站Logo
├── 📁 src/                   # 源代码目录
│   ├── 📁 api/               # API 接口层
│   │   ├── codegen.api.ts    # 代码生成接口
│   │   ├── 📁 demo/          # 示例接口
│   │   │   └── example.ts    # 示例 API
│   │   ├── 📁 monitor/       # 监控相关接口
│   │   │   ├── cache.ts      # 缓存监控
│   │   │   ├── job.ts        # 定时任务
│   │   │   ├── online.ts     # 在线用户
│   │   │   └── server.ts     # 服务器监控
│   │   └── 📁 system/        # 系统相关接口
│   │       ├── auth.ts       # 认证接口
│   │       ├── config.ts     # 系统配置
│   │       ├── dept.ts       # 部门管理
│   │       ├── dict.ts       # 字典管理
│   │       ├── log.ts        # 日志管理
│   │       ├── menu.ts       # 菜单管理
│   │       ├── notice.ts     # 通知公告
│   │       ├── position.ts   # 职位管理
│   │       ├── role.ts       # 角色管理
│   │       └── user.ts       # 用户管理
│   ├── 📁 assets/            # 静态资源
│   │   ├── 📁 icons/         # 图标资源
│   │   │   ├── api.svg       # API 图标
│   │   │   ├── user.svg      # 用户图标
│   │   │   ├── menu.svg      # 菜单图标
│   │   │   └── ...           # 其他图标 (70+ 个图标)
│   │   └── 📁 images/        # 图片资源
│   │       ├── 401.svg       # 401 错误图片
│   │       ├── 404.svg       # 404 错误图片
│   │       └── 500.svg       # 500 错误图片
│   ├── 📁 components/        # 全局组件库
│   │   ├── 📁 AppLink/       # 应用链接组件
│   │   ├── 📁 Breadcrumb/    # 面包屑导航
│   │   ├── 📁 CommonWrapper/ # 通用包装器
│   │   ├── 📁 CURD/          # CRUD 通用组件
│   │   │   ├── PageContent.vue  # 页面内容组件
│   │   │   ├── PageModal.vue    # 页面弹窗组件
│   │   │   ├── PageSearch.vue   # 页面搜索组件
│   │   │   ├── types.ts         # 类型定义
│   │   │   └── usePage.ts       # 页面逻辑组合
│   │   ├── 📁 DarkModeSwitch/   # 暗色模式切换
│   │   ├── 📁 DatePicker/       # 日期选择器
│   │   ├── 📁 ECharts/          # 图表组件
│   │   ├── 📁 Frame/            # 框架组件
│   │   ├── 📁 Fullscreen/       # 全屏组件
│   │   ├── 📁 GithubCorner/     # GitHub 角标
│   │   ├── 📁 Guide/            # 引导组件
│   │   ├── 📁 Hamburger/        # 汉堡菜单
│   │   ├── 📁 IconSelect/       # 图标选择器
│   │   ├── 📁 InputTag/         # 标签输入
│   │   ├── 📁 IntervalTab/      # 间隔标签页
│   │   ├── 📁 LangSelect/       # 语言选择器
│   │   ├── 📁 MenuSearch/       # 菜单搜索
│   │   ├── 📁 Notification/     # 通知组件
│   │   ├── 📁 OperationColumn/  # 操作列组件
│   │   ├── 📁 Pagination/       # 分页组件
│   │   ├── 📁 SizeSelect/       # 尺寸选择器
│   │   ├── 📁 TableSelect/      # 表格选择器
│   │   ├── 📁 TextScroll/       # 文字滚动
│   │   ├── 📁 Upload/           # 上传组件
│   │   │   ├── ImportModal.vue  # 导入弹窗
│   │   │   └── SingleImageUpload.vue # 单图上传
│   │   └── 📁 WangEditor/       # 富文本编辑器
│   ├── 📁 constants/           # 常量定义
│   │   ├── index.ts            # 常量导出
│   │   └── storage-keys.ts     # 存储键常量
│   ├── 📁 enums/              # 枚举定义
│   │   ├── index.ts            # 枚举导出
│   │   ├── 📁 api/             # API 相关枚举
│   │   │   └── result.enum.ts  # API 结果枚举
│   │   ├── 📁 codegen/         # 代码生成枚举
│   │   │   ├── form.enum.ts    # 表单枚举
│   │   │   └── query.enum.ts   # 查询枚举
│   │   ├── 📁 settings/        # 设置相关枚举
│   │   │   ├── device.enum.ts  # 设备枚举
│   │   │   ├── layout.enum.ts  # 布局枚举
│   │   │   ├── locale.enum.ts  # 语言枚举
│   │   │   └── theme.enum.ts   # 主题枚举
│   │   └── 📁 system/          # 系统相关枚举
│   │       └── menu.enum.ts    # 菜单枚举
│   ├── 📁 lang/               # 国际化配置
│   │   ├── index.ts            # 国际化入口
│   │   └── 📁 package/         # 语言包
│   │       ├── zh-cn.ts        # 中文语言包
│   │       └── en.ts           # 英文语言包
│   ├── 📁 layouts/            # 布局系统
│   │   ├── index.vue           # 主布局组件
│   │   ├── 📁 components/      # 布局子组件
│   │   │   ├── 📁 AppLogo/     # 应用Logo
│   │   │   ├── 📁 AppMain/     # 主内容区域
│   │   │   ├── 📁 Menu/        # 菜单组件 (4个文件)
│   │   │   ├── 📁 NavBar/      # 导航栏 (4个文件)
│   │   │   ├── 📁 Settings/    # 设置面板
│   │   │   └── 📁 TagsView/    # 标签页视图
│   │   ├── 📁 composables/     # 布局逻辑组合
│   │   │   ├── useLayout.ts           # 布局逻辑
│   │   │   ├── useLayoutMenu.ts       # 菜单逻辑
│   │   │   └── useLayoutResponsive.ts # 响应式逻辑
│   │   └── 📁 views/           # 布局视图
│   │       ├── BaseLayout.vue  # 基础布局
│   │       ├── LeftLayout.vue  # 左侧布局
│   │       ├── MixLayout.vue   # 混合布局
│   │       └── TopLayout.vue   # 顶部布局
│   ├── 📁 plugins/            # 插件配置
│   │   ├── icons.ts            # 图标插件
│   │   ├── index.ts            # 插件入口
│   │   └── permission.ts       # 权限插件
│   ├── 📁 router/             # 路由配置
│   │   └── index.ts            # 路由入口文件
│   ├── 📁 store/              # 状态管理
│   │   ├── index.ts            # 状态管理入口
│   │   └── 📁 modules/         # 状态模块
│   │       ├── app.store.ts       # 应用状态
│   │       ├── config.store.ts    # 配置状态
│   │       ├── dict.store.ts      # 字典状态
│   │       ├── lock.store.ts      # 锁屏状态
│   │       ├── notice.store.ts    # 通知状态
│   │       ├── permission.store.ts # 权限状态
│   │       ├── settings.store.ts  # 设置状态
│   │       ├── tags-view.store.ts # 标签页状态
│   │       └── user.store.ts      # 用户状态
│   ├── 📁 styles/             # 样式系统
│   │   ├── index.scss         # 全局样式入口
│   │   ├── reset.scss         # 样式重置
│   │   ├── variables.scss     # CSS 变量
│   │   ├── variables.module.scss # 模块化变量
│   │   ├── element-plus.scss  # Element Plus 样式覆盖
│   │   ├── vxe-table.scss     # VxeTable 样式
│   │   ├── vxe-table.css      # VxeTable 样式
│   │   ├── 📁 dark/           # 暗色主题
│   │   │   └── css-vars.css   # 暗色主题变量
│   ├── 📁 types/             # TypeScript 类型定义
│   │   ├── auto-imports.d.ts     # 自动导入类型
│   │   ├── components.d.ts       # 组件类型
│   │   ├── env.d.ts              # 环境类型
│   │   ├── global.d.ts           # 全局类型
│   │   ├── router.d.ts           # 路由类型
│   │   ├── shims-vue.d.ts        # Vue 声明文件
│   │   └── vue3-cron-plus.d.ts   # Cron 组件类型
│   ├── 📁 utils/              # 工具函数库
│   │   ├── index.ts            # 工具导出
│   │   ├── auth.ts             # 认证工具
│   │   ├── common.ts           # 通用工具
│   │   ├── dateUtil.ts         # 日期工具
│   │   ├── i18n.ts             # 国际化工具
│   │   ├── nprogress.ts        # 进度条工具
│   │   ├── quickStartManager.ts # 快速开始管理器
│   │   ├── request.ts          # HTTP 请求封装
│   │   ├── storage.ts          # 本地存储工具
│   │   └── theme.ts            # 主题工具
│   ├── 📁 views/              # 页面视图
│   │   ├── 📁 codegen/         # 代码生成页面
│   │   │   └── index.html      # 代码生成器页面
│   │   ├── 📁 common/          # 公共页面
│   │   │   ├── 📁 docs/        # 文档页面
│   │   │   └── 📁 redoc/       # ReDoc API 文档
│   │   ├── 📁 current/         # 当前用户页面
│   │   │   └── profile.vue     # 用户资料页
│   │   ├── 📁 dashboard/       # 仪表板页面
│   │   │   ├── analysis.vue       # 数据分析页
│   │   │   ├── workplace.vue      # 工作台页面
│   │   │   └── 📁 components/     # 仪表板组件
│   │   ├── 📁 demo/            # 示例页面
│   │   │   └── 📁 example/     # 示例页面
│   │   ├── 📁 error/           # 错误页面
│   │   │   ├── 401.vue         # 401 未授权
│   │   │   ├── 404.vue         # 404 未找到
│   │   │   └── 500.vue         # 500 服务器错误
│   │   ├── 📁 monitor/         # 监控页面
│   │   │   ├── 📁 cache/       # 缓存监控
│   │   │   ├── 📁 job/         # 定时任务
│   │   │   ├── 📁 online/      # 在线用户
│   │   │   └── 📁 server/      # 服务器监控
│   │   ├── 📁 redirect/        # 重定向页面
│   │   │   └── index.vue       # 重定向入口
│   │   └── 📁 system/          # 系统管理页面
│   │       ├── 📁 auth/        # 权限管理 (4个文件)
│   │       ├── 📁 config/      # 系统配置 (2个文件)
│   │       ├── 📁 dept/        # 部门管理 (1个文件)
│   │       ├── 📁 dict/        # 字典管理 (2个文件)
│   │       ├── 📁 log/         # 日志管理 (1个文件)
│   │       ├── 📁 menu/        # 菜单管理 (1个文件)
│   │       ├── 📁 notice/      # 通知公告 (1个文件)
│   │       ├── 📁 position/    # 职位管理 (1个文件)
│   │       ├── 📁 role/        # 角色管理 (2个文件)
│   │       └── 📁 user/        # 用户管理 (2个文件)
│   ├── App.vue                # Vue 根组件
│   ├── main.ts                # 应用入口文件
│   └── settings.ts            # 应用配置
├── 📄 .editorconfig          # 编辑器配置
├── 📄 .env.development       # 开发环境变量
├── 📄 .env.production        # 生产环境变量
├── 📄 .eslintignore          # ESLint 忽略配置
├── 📄 .eslintrc-auto-import.json # ESLint 自动导入配置
├── 📄 .gitignore             # Git 忽略文件
├── 📄 .prettierignore        # Prettier 忽略配置
├── 📄 .prettierrc.yaml       # Prettier 配置
├── 📄 .stylelintignore       # Stylelint 忽略配置
├── 📄 .stylelintrc.cjs       # Stylelint 配置
├── 📄 CHANGELOG.md           # 更新日志
├── 📄 commitlint.config.cjs  # Commitlint 配置
├── 📄 eslint.config.ts       # ESLint 配置
├── 📄 index.html             # HTML 入口文件
├── 📄 package.json           # 项目依赖配置
├── 📄 pnpm-lock.yaml         # pnpm 锁定文件
├── 📄 PROJECT_GUIDE.md       # 项目指南 (本文档)
├── 📄 README.md              # 项目说明
├── 📄 tsconfig.json          # TypeScript 配置
├── 📄 uno.config.ts          # UnoCSS 配置
└── 📄 vite.config.ts         # Vite 构建配置
```

### 核心文件说明

#### 🔧 构建配置

| 文件               | 说明                                            |
| ------------------ | ----------------------------------------------- |
| `vite.config.ts`   | Vite 构建工具主配置，包含插件、代理、构建优化等 |
| `tsconfig.json`    | TypeScript 编译配置，定义编译选项和路径映射     |
| `uno.config.ts`    | UnoCSS 原子化CSS配置，定义样式规则和主题        |
| `eslint.config.ts` | ESLint 代码检查配置，确保代码质量和规范         |
| `package.json`     | 项目依赖管理和脚本配置                          |


#### ⚡ 应用入口

| 文件              | 说明                                    |
| ----------------- | --------------------------------------- |
| `index.html`      | HTML 入口文件，包含基础的页面结构       |
| `src/main.ts`     | 应用入口文件，初始化 Vue 应用和各项配置 |
| `src/App.vue`     | Vue 根组件，应用的主要布局结构          |
| `src/settings.ts` | 应用基础配置，包含主题、语言等设置      |


#### 🗂️ 核心目录详解

##### 1. API 接口层 (`src/api/`)

负责前后端数据交互，采用分层架构：

+ **system/**: 系统管理相关接口（用户、角色、菜单、权限等）
+ **monitor/**: 系统监控相关接口（缓存、任务、服务器状态等）
+ **codegen/**: 代码生成相关接口
+ **demo/**: 示例接口（用于测试和演示）

每个接口模块都包含完整的 CRUD 操作和类型定义。

##### 2. 组件库 (`src/components/`)

高度复用的组件集合：

+ **CURD/**: 通用CRUD组件，支持列表、搜索、编辑、删除等操作
+ **Upload/**: 文件上传组件，支持单图、多图、批量导入
+ **布局相关**: 菜单、导航栏、面包屑等布局组件
+ **业务组件**: 针对具体业务场景的专用组件

##### 3. 状态管理 (`src/store/`)

基于 Pinia 的状态管理：

+ **modules/**: 按功能划分的状态模块
+ **持久化**: 支持状态持久化存储
+ **类型安全**: 完整的 TypeScript 类型支持

##### 4. 样式系统 (`src/styles/`)

统一的样式管理：

+ **主题系统**: 支持亮色/暗色主题切换
+ **变量管理**: CSS 变量集中管理
+ **组件样式**: 各组件的专用样式
+ **UnoCSS**: 原子化CSS框架，提升开发效率

##### 5. 工具函数 (`src/utils/`)

通用工具函数库：

+ **request.ts**: HTTP 请求封装，包含拦截器、错误处理
+ **auth.ts**: 认证相关工具
+ **storage.ts**: 本地存储封装
+ **dateUtil.ts**: 日期时间处理工具
+ **theme.ts**: 主题切换工具

##### 6. 页面视图 (`src/views/`)

具体的页面组件：

+ **system/**: 系统管理页面（用户、角色、菜单等）
+ **monitor/**: 系统监控页面
+ **dashboard/**: 数据仪表板
+ **error/**: 错误页面
+ **current/**: 当前用户相关页面

### 架构设计原则

1. **模块化**: 每个功能模块独立，便于维护和扩展
2. **类型安全**: 全面的 TypeScript 支持，减少运行时错误
3. **组件复用**: 抽象通用组件，提高开发效率
4. **配置化**: 通过配置而非硬编码实现功能
5. **规范化**: 统一的代码规范和开发流程

### 关键配置文件详解

#### 📄 package.json

项目依赖和脚本配置：

```json
{
  "name": "fastapi-vue3-admin",
  "version": "2.0.0",
  "scripts": {
    "dev": "vite",                    // 开发服务器
    "build": "vite build",            // 生产构建
    "build:pro": "vite build --mode pro", // 生产环境构建
    "build:dev": "vite build --mode dev",  // 开发环境构建
    "build:test": "vite build --mode test", // 测试环境构建
    "preview": "vite preview",        // 预览构建结果
    "lint": "eslint ...",             // 代码检查
    "type-check": "vue-tsc --noEmit"  // 类型检查
  },
  "dependencies": {
    "vue": "^3.5.17",                 // Vue 3 核心
    "element-plus": "^2.10.4",        // UI 组件库
    "pinia": "^3.0.3",               // 状态管理
    "vue-router": "^4.5.1",          // 路由管理
    "axios": "^1.10.0",              // HTTP 客户端
    "vue-i18n": "^11.1.10"           // 国际化
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.2.4",   // Vue 插件
    "typescript": "^5.8.3",           // TypeScript
    "unocss": "66.2.3",              // 原子化CSS
    "vite": "^6.3.5"                 // 构建工具
  }
}
```

#### ⚙️ vite.config.ts✨

Vite 构建配置：

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')  // 路径别名
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // 后端API地址
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        chunkFileNames: 'js/[name]-[hash].js',
        entryFileNames: 'js/[name]-[hash].js',
        assetFileNames: '[ext]/[name]-[hash].[ext]'
      }
    }
  }
})
```

#### 🔷 uno.config.ts

UnoCSS 原子化CSS配置：

```typescript
import { defineConfig } from 'unocss'
import { presetUno, presetAttributify } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),          // UnoCSS 预设
    presetAttributify()   // 属性化模式
  ],
  theme: {
    colors: {
      primary: 'var(--el-color-primary)',
      success: 'var(--el-color-success)',
      warning: 'var(--el-color-warning)',
      danger: 'var(--el-color-danger)'
    }
  },
  shortcuts: {
    'flex-center': 'flex items-center justify-center',
    'flex-between': 'flex items-center justify-between'
  }
})
```

#### 📝 tsconfig.json

TypeScript 配置：

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]  // 路径映射
    }
  },
  "include": [
    "src/**/*.ts",
    "src/**/*.d.ts",
    "src/**/*.tsx",
    "src/**/*.vue"
  ],
  "exclude": ["node_modules"]
}
```

### 核心模块功能详解

#### 🎯 应用入口 (`src/main.ts`)

应用初始化和配置：

```typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import router from './router'
import i18n from './lang'
import App from './App.vue'

// 创建应用实例
const app = createApp(App)

// 安装插件
app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.use(i18n)

// 挂载应用
app.mount('#app')
```

#### 🏗️ 应用配置 (`src/settings.ts`)

应用基础配置：

```typescript
export const settings = {
  // 应用信息
  title: 'FastApiAdmin',
  version: '2.0.0',

  // 显示配置
  showSettings: true,
  showTagsView: true,
  showSidebarLogo: true,

  // 功能开关
  enableErrorLog: true,
  enableWatermark: false,

  // 主题配置
  theme: 'light',
  primaryColor: '#409EFF',

  // 布局配置
  layout: 'left',
  fixedHeader: true,

  // 其他配置
  defaultLanguage: 'zh-cn',
  whiteList: ['/login', '/404', '/401']
}
```

#### 🧩 组件系统架构

##### CURD 通用组件

```typescript
// src/components/CURD/usePage.ts
export const usePage = (config: PageConfig) => {
  const loading = ref(false)
  const data = ref([])
  const pagination = ref({
    current: 1,
    size: 20,
    total: 0
  })

  // 分页查询
  const fetchData = async () => {
    loading.value = true
    try {
      const result = await config.api.list({
        page: pagination.value.current,
        size: pagination.value.size,
        ...config.queryParams
      })
      data.value = result.records
      pagination.value.total = result.total
    } finally {
      loading.value = false
    }
  }

  // 新增
  const handleCreate = () => {
    config.onCreate?.()
  }

  // 编辑
  const handleUpdate = (record: any) => {
    config.onUpdate?.(record)
  }

  // 删除
  const handleDelete = async (id: string) => {
    await config.api.delete(id)
    await fetchData()
  }

  return {
    loading,
    data,
    pagination,
    fetchData,
    handleCreate,
    handleUpdate,
    handleDelete
  }
}
```

#### 🔄 状态管理架构

##### 用户状态管理

```typescript
// src/store/modules/user.store.ts
export const useUserStore = defineStore('user', () => {
  // 状态
  const userInfo = ref<UserInfo | null>(null)
  const token = ref<string>('')
  const permissions = ref<string[]>([])
  const roles = ref<string[]>([])

  // 计算属性
  const isLogin = computed(() => !!token.value)
  const userId = computed(() => userInfo.value?.id)

  // 动作
  const login = async (loginForm: LoginForm) => {
    const { data } = await loginApi(loginForm)
    token.value = data.token
    await getUserInfo()
  }

  const getUserInfo = async () => {
    const { data } = await getUserInfoApi()
    userInfo.value = data.user
    permissions.value = data.permissions
    roles.value = data.roles
  }

  const logout = () => {
    userInfo.value = null
    token.value = ''
    permissions.value = []
    roles.value = []
  }

  return {
    userInfo,
    token,
    permissions,
    roles,
    isLogin,
    userId,
    login,
    getUserInfo,
    logout
  }
}, {
  persist: true  // 持久化存储
})
```

#### 🎨 样式系统架构

##### 主题系统

```sass
// src/styles/variables.scss
:root {
  // 亮色主题
  --primary-color: #409EFF;
  --success-color: #67C23A;
  --warning-color: #E6A23C;
  --danger-color: #F56C6C;

  // 布局变量
  --header-height: 60px;
  --sidebar-width: 260px;
  --sidebar-collapse-width: 64px;

  // 间距变量
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
}

// 暗色主题
.dark {
  --primary-color: #66D9EF;
  --success-color: #A6E22E;
  --warning-color: #FD971F;
  --danger-color: #F92672;

  --bg-color: #1E1E1E;
  --text-color: #D4D4D4;
  --border-color: #3E3E3E;
}
```

##### UnoCSS 工具类

```vue
<template>
  <!-- 使用 UnoCSS 工具类 -->
  <div class="container mx-auto px-4 py-8">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="item in items"
        :key="item.id"
        class="bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow p-6"
      >
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
          {{ item.title }}
        </h3>

        <p class="text-gray-600 dark:text-gray-300">
          {{ item.description }}
        </p>

      </div>

    </div>

  </div>

</template>

```

#### 🔧 工具函数库

##### HTTP 请求封装

```typescript
// src/utils/request.ts
import axios, { AxiosInstance, AxiosResponse } from 'axios'

class Request {
  private instance: AxiosInstance

  constructor() {
    this.instance = axios.create({
      baseURL: import.meta.env.VITE_APP_API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // 请求拦截器
    this.instance.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // 响应拦截器
    this.instance.interceptors.response.use(
      (response: AxiosResponse) => {
        const { data } = response
        if (data.code === 200) {
          return data
        }
        return Promise.reject(new Error(data.message))
      },
      (error) => {
        if (error.response?.status === 401) {
          // 处理未授权
          router.push('/login')
        }
        return Promise.reject(error)
      }
    )
  }

  public get<T = any>(url: string, config?: any): Promise<T> {
    return this.instance.get(url, config)
  }

  public post<T = any>(url: string, data?: any, config?: any): Promise<T> {
    return this.instance.post(url, data, config)
  }

  public put<T = any>(url: string, data?: any, config?: any): Promise<T> {
    return this.instance.put(url, data, config)
  }

  public delete<T = any>(url: string, config?: any): Promise<T> {
    return this.instance.delete(url, config)
  }
}

export const request = new Request()
export default request
```

##### 日期时间工具

```typescript
// src/utils/dateUtil.ts
import dayjs from 'dayjs'

export const formatDate = (date: string | Date, format = 'YYYY-MM-DD HH:mm:ss') => {
  return dayjs(date).format(format)
}

export const formatDateTime = (date: string | Date) => {
  return formatDate(date, 'YYYY-MM-DD HH:mm:ss')
}

export const formatDateOnly = (date: string | Date) => {
  return formatDate(date, 'YYYY-MM-DD')
}

export const formatTimeOnly = (date: string | Date) => {
  return formatDate(date, 'HH:mm:ss')
}

export const getRelativeTime = (date: string | Date) => {
  return dayjs(date).fromNow()
}

export const isToday = (date: string | Date) => {
  return dayjs(date).isSame(dayjs(), 'day')
}

export const isYesterday = (date: string | Date) => {
  return dayjs(date).isSame(dayjs().subtract(1, 'day'), 'day')
}

export const getDateRange = (days: number) => {
  const end = dayjs()
  const start = dayjs().subtract(days, 'day')
  return [start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD')]
}
```

### 技术栈依赖关系

```plain
Vue 3 (核心框架)
├── Vue Router 4 (路由管理)
├── Pinia (状态管理)
├── Element Plus (UI组件)
├── Vue I18n (国际化)
├── Axios (HTTP客户端)
└── UnoCSS (原子化CSS)

Vite (构建工具)
├── TypeScript (类型系统)
├── ESLint (代码检查)
├── Prettier (代码格式化)
└── PostCSS (CSS处理)
```

这个项目结构体现了现代前端项目的标准架构，具有良好的可维护性、可扩展性和开发体验。

## 🔗 API 接口管理

### 接口层架构

项目采用分层的API接口管理架构：

```plain
src/api/
├── 📁 system/         # 系统相关接口
│   ├── auth.ts        # 认证接口
│   ├── user.ts        # 用户管理接口
│   ├── menu.ts        # 菜单管理接口
│   └── config.ts      # 系统配置接口
├── 📁 monitor/        # 监控相关接口
│   ├── cache.ts       # 缓存监控
│   ├── job.ts         # 定时任务
│   ├── online.ts      # 在线用户
│   └── server.ts      # 服务器监控
└── 📁 codegen/        # 代码生成接口
```

### 请求封装

项目使用统一的HTTP请求封装：

```typescript
// src/utils/request.ts
import axios from 'axios'
import type { AxiosResponse } from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_APP_API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 添加认证token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    const { data } = response
    if (data.code === 200) {
      return data
    } else {
      ElMessage.error(data.message || '请求失败')
      return Promise.reject(new Error(data.message || '请求失败'))
    }
  },
  (error) => {
    if (error.response?.status === 401) {
      // 处理未授权
      router.push('/login')
    } else {
      ElMessage.error(error.message || '网络错误')
    }
    return Promise.reject(error)
  }
)

export default request
```

### 接口定义示例

```typescript
// src/api/system/user.ts
import request from '@/utils/request'

export interface UserInfo {
  id: number
  username: string
  email: string
  avatar?: string
  roles: string[]
  status: 'active' | 'inactive'
}

export interface UserQuery {
  page?: number
  size?: number
  username?: string
  status?: string
}

// 获取用户列表
export const getUserList = (params?: UserQuery) => {
  return request.get('/system/user/list', { params })
}

// 获取用户信息
export const getUserInfo = (id: number) => {
  return request.get(`/system/user/${id}`)
}

// 创建用户
export const createUser = (data: Omit<UserInfo, 'id'>) => {
  return request.post('/system/user', data)
}

// 更新用户
export const updateUser = (id: number, data: Partial<UserInfo>) => {
  return request.put(`/system/user/${id}`, data)
}

// 删除用户
export const deleteUser = (id: number) => {
  return request.delete(`/system/user/${id}`)
}

// 批量删除用户
export const batchDeleteUsers = (ids: number[]) => {
  return request.delete('/system/user/batch', { data: { ids } })
}
```

### 接口错误处理

```typescript
// src/hooks/useApi.ts
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

export const useApi = <T = any>(apiFn: (...args: any[]) => Promise<T>) => {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const data = ref<T | null>(null)

  const execute = async (...args: any[]) => {
    loading.value = true
    error.value = null

    try {
      const result = await apiFn(...args)
      data.value = result
      return result
    } catch (err: any) {
      error.value = err.message || '请求失败'
      ElMessage.error(error.value)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading: readonly(loading),
    error: readonly(error),
    data: readonly(data),
    execute
  }
}
```

### 接口使用示例

```vue
<script setup lang="ts">
import { useApi } from '@/hooks/useApi'
import { getUserList, type UserQuery } from '@/api/system/user'

const queryParams = ref<UserQuery>({
  page: 1,
  size: 20
})

const {
  loading,
  error,
  data: userList,
  execute: fetchUsers
} = useApi(getUserList)

// 页面加载时获取数据
onMounted(() => {
  fetchUsers(queryParams.value)
})

// 搜索用户
const handleSearch = () => {
  fetchUsers(queryParams.value)
}
</script>

```

## 🚀 快速开始

### 环境要求

+ **Node.js**: >= 20.0.0
+ **pnpm**: >= 8.0.0 (推荐)
+ **Git**: >= 2.0.0

### 安装依赖

```bash
# 进入项目目录
cd FastapiAdmin/frontend

# 安装依赖（推荐使用 pnpm）
pnpm install
```

### 开发环境

```bash
# 启动开发服务器
pnpm run dev

# 构建生产版本
pnpm run build

# 预览构建结果
pnpm run preview
```

### 其他命令

```bash
# 代码检查
pnpm run lint

# 类型检查
pnpm run type-check

# 格式化代码
pnpm run lint:format

# 清理缓存
pnpm run clean:cache
```

## 🎯 Vue 3 Composition API 最佳实践

### 1. 组合式函数设计

```typescript
// src/composables/useCounter.ts
export function useCounter(initialValue = 0) {
  const count = ref(initialValue)
  const doubleCount = computed(() => count.value * 2)
  
  const increment = () => count.value++
  const decrement = () => count.value--
  const reset = () => count.value = initialValue
  
  return {
    count,
    doubleCount,
    increment,
    decrement,
    reset
  }
}

// 使用示例
const { count, doubleCount, increment, decrement, reset } = useCounter(10)
```

### 2. 响应式数据管理

```typescript
// 推荐的响应式数据管理方式
const state = reactive({
  user: null,
  loading: false,
  error: null
})

// 对于复杂计算
const userDisplayName = computed(() => {
  if (!state.user) return 'Guest'
  return `${state.user.firstName} ${state.user.lastName}`
})

// 对于需要解构的响应式数据
import { toRefs } from 'vue'
const { user, loading, error } = toRefs(state)
```

### 3. 生命周期管理

```typescript
import { onMounted, onUnmounted, onBeforeUnmount, onUpdated, onErrorCaptured } from 'vue'

onMounted(() => {
  console.log('组件挂载完成')
  // 初始化数据、添加事件监听器等
})

onBeforeUnmount(() => {
  console.log('组件即将卸载')
  // 清理资源、移除事件监听器等
})

onUnmounted(() => {
  console.log('组件已卸载')
  // 最终清理工作
})

onUpdated(() => {
  console.log('组件已更新')
  // 响应更新后的逻辑
})

onErrorCaptured((error, instance, info) => {
  console.error('捕获到错误:', error, info)
  // 错误处理逻辑
  return true // 阻止错误继续传播
})
```

## 📝 TypeScript 使用技巧

### 1. 类型定义最佳实践

```typescript
// src/types/user.ts
export interface User {
  id: number
  username: string
  email: string
  avatar?: string
  roles: string[]
  status: 'active' | 'inactive'
  createdAt: string
  updatedAt: string
}

// 使用类型守卫
export function isUser(obj: any): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.id === 'number' &&
    typeof obj.username === 'string' &&
    typeof obj.email === 'string' &&
    Array.isArray(obj.roles)
  )
}
```

### 2. 泛型使用

```typescript
// src/utils/request.ts
export async function request<T = any>(
  url: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(url, options)
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  return response.json()
}

// 使用示例
interface UserListResponse {
  data: User[]
  total: number
  page: number
  size: number
}

const users = await request<UserListResponse>('/api/users')
```

### 3. 模块增强

```typescript
// src/types/vue-router.d.ts
import 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    icon?: string
    roles?: string[]
    keepAlive?: boolean
    hidden?: boolean
  }
}

// 使用增强的类型
const routes = [
  {
    path: '/user',
    component: UserPage,
    meta: {
      title: '用户管理',
      icon: 'User',
      roles: ['admin'],
      keepAlive: true
    }
  }
]
```

## ⚡ 性能优化

### 1. 组件优化

```vue
<template>
  <!-- 使用 v-memo 缓存渲染结果 -->
  <div v-memo="[item.id, item.name]">
    {{ item.name }}
  </div>
  
  <!-- 使用 v-once 只渲染一次 -->
  <div v-once>
    {{ staticContent }}
  </div>
  
  <!-- 使用 v-show 替代 v-if 用于频繁切换的元素 -->
  <div v-show="isVisible">
    {{ dynamicContent }}
  </div>
</template>

<script setup lang="ts">
// 使用 defineAsyncComponent 懒加载组件
import { defineAsyncComponent } from 'vue'
const HeavyComponent = defineAsyncComponent(() => import('./HeavyComponent.vue'))

// 使用 shallowRef 处理大型对象
const largeObject = shallowRef({ /* 大型对象 */ })

// 使用 markRaw 处理不需要响应式的对象
const nonReactiveObject = markRaw({ /* 不需要响应式的对象 */ })
</script>
```

### 2. 路由优化

```typescript
// src/router/index.ts
// 路由懒加载
const Dashboard = () => import('@/views/dashboard/index.vue')
const UserManagement = () => import('@/views/system/user/index.vue')
const RoleManagement = () => import('@/views/system/role/index.vue')

// 路由分割
const routes = [
  {
    path: '/dashboard',
    component: Dashboard
  },
  {
    path: '/system',
    children: [
      {
        path: 'user',
        component: UserManagement
      },
      {
        path: 'role',
        component: RoleManagement
      }
    ]
  }
]
```

### 3. 网络优化

```typescript
// src/utils/request.ts
// 请求防抖
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout> | null = null
  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

// 批量请求
async function batchRequest<T>(requests: Array<Promise<T>>): Promise<T[]> {
  return Promise.all(requests)
}

// 缓存请求结果
const cache = new Map<string, any>()
async function cachedRequest<T>(url: string): Promise<T> {
  if (cache.has(url)) {
    return cache.get(url)
  }
  const result = await fetch(url).then(res => res.json())
  cache.set(url, result)
  return result
}
```

## 🧪 测试

### 1. 单元测试

```typescript
// src/utils/__tests__/dateUtil.test.ts
import { formatDate, getRelativeTime } from '../dateUtil'

describe('dateUtil', () => {
  test('formatDate should format date correctly', () => {
    const date = '2023-01-01T00:00:00Z'
    expect(formatDate(date)).toBe('2023-01-01 00:00:00')
    expect(formatDate(date, 'YYYY-MM-DD')).toBe('2023-01-01')
  })
  
  test('getRelativeTime should return relative time', () => {
    const date = new Date(Date.now() - 60000).toISOString() // 1 minute ago
    expect(getRelativeTime(date)).toBe('1 minute ago')
  })
})
```

### 2. 组件测试

```typescript
// src/components/__tests__/Button.test.ts
import { mount } from '@vue/test-utils'
import Button from '../Button/index.vue'

describe('Button', () => {
  test('should render correctly', () => {
    const wrapper = mount(Button, {
      props: {
        type: 'primary'
      },
      slots: {
        default: 'Click me'
      }
    })
    expect(wrapper.text()).toBe('Click me')
    expect(wrapper.classes()).toContain('el-button--primary')
  })
  
  test('should emit click event', async () => {
    const wrapper = mount(Button)
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })
})
```

## 🚀 CI/CD 配置

### 1. GitHub Actions 配置

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'pnpm'
      - name: Install dependencies
        run: pnpm install
      - name: Run lint
        run: pnpm run lint
      - name: Run type check
        run: pnpm run type-check
      - name: Run tests
        run: pnpm run test
  
  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'pnpm'
      - name: Install dependencies
        run: pnpm install
      - name: Build
        run: pnpm run build
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist
```

### 2. 部署配置

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'pnpm'
      - name: Install dependencies
        run: pnpm install
      - name: Build
        run: pnpm run build
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

## 📚 代码规范

### 1. ESLint 配置

```typescript
// eslint.config.ts
import { defineConfig } from 'eslint'
import vue from '@eslint/js'
import prettier from 'eslint-plugin-prettier'

export default defineConfig({
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
    'plugin:@typescript-eslint/recommended'
  ],
  plugins: {
    prettier
  },
  rules: {
    'prettier/prettier': 'error',
    'vue/multi-word-component-names': 'off',
    '@typescript-eslint/no-explicit-any': 'warn'
  }
})
```

### 2. Prettier 配置

```yaml
# .prettierrc.yaml
trailingComma: 'es5'
tabWidth: 2
semi: true
singleQuote: true
printWidth: 80
bracketSpacing: true
bracketSameLine: false
arrowParens: 'always'
```

## 🎨 设计系统

### 1. 主题配置

```typescript
// src/styles/theme/index.ts
export const lightTheme = {
  colors: {
    primary: '#409EFF',
    secondary: '#67C23A',
    success: '#67C23A',
    warning: '#E6A23C',
    danger: '#F56C6C',
    info: '#909399',
    background: '#F5F7FA',
    text: '#303133'
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px'
  },
  borderRadius: {
    sm: '2px',
    md: '4px',
    lg: '8px'
  }
}

export const darkTheme = {
  colors: {
    primary: '#66D9EF',
    secondary: '#A6E22E',
    success: '#A6E22E',
    warning: '#FD971F',
    danger: '#F92672',
    info: '#8884d8',
    background: '#1E1E1E',
    text: '#D4D4D4'
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px'
  },
  borderRadius: {
    sm: '2px',
    md: '4px',
    lg: '8px'
  }
}
```

### 2. 组件设计规范

```typescript
// src/components/Button/index.vue
<template>
  <button
    :class="[
      'btn',
      `btn--${type}`,
      `btn--${size}`,
      { 'btn--loading': loading }
    ]"
    :disabled="disabled || loading"
    @click="$emit('click')"
  >
    <span v-if="loading" class="btn__loading"></span>
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
defineOptions({
  name: 'AppButton' // 组件名称使用 PascalCase
})

interface Props {
  type?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger'
  size?: 'small' | 'medium' | 'large'
  disabled?: boolean
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'primary',
  size: 'medium',
  disabled: false,
  loading: false
})

defineEmits<{
  click: []
}>()
</script>

<style scoped lang="scss">
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &--primary {
    background-color: var(--primary-color);
    color: white;
  }
  
  &--small {
    padding: 4px 12px;
    font-size: 12px;
  }
  
  &--large {
    padding: 12px 24px;
    font-size: 16px;
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  &__loading {
    // 加载动画样式
  }
}
</style>
```

## 📝 项目配置管理

### 1. 环境变量管理

```typescript
// src/config/index.ts
import { loadEnv } from 'vite'

const env = loadEnv(import.meta.env.MODE, process.cwd())

export const config = {
  env: env.VITE_APP_ENV || 'development',
  api: {
    baseURL: env.VITE_APP_API_BASE_URL || 'http://localhost:8000',
    timeout: Number(env.VITE_APP_API_TIMEOUT) || 10000
  },
  app: {
    title: env.VITE_APP_TITLE || 'FastApiAdmin',
    version: env.VITE_APP_VERSION || '1.0.0'
  },
  features: {
    enableAnalytics: env.VITE_ENABLE_ANALYTICS === 'true',
    enableErrorTracking: env.VITE_ENABLE_ERROR_TRACKING === 'true'
  }
}
```

### 2. 全局配置

```typescript
// src/plugins/config.ts
import { App } from 'vue'
import { config } from '@/config'

export function setupConfig(app: App) {
  // 全局注入配置
  app.config.globalProperties.$config = config
  
  // 提供全局配置访问
  app.provide('config', config)
}

// 使用示例
import { inject } from 'vue'
const config = inject('config')
console.log('API Base URL:', config.api.baseURL)
```

## 🎯 开发工具推荐

### 1. VS Code 插件

- **Volar**: Vue 3 官方推荐的 VS Code 扩展
- **TypeScript Vue Plugin (Volar)**: 为 Vue 文件提供 TypeScript 支持
- **ESLint**: 代码质量检查
- **Prettier - Code formatter**: 代码格式化
- **UnoCSS**: UnoCSS 工具类支持
- **GitLens**: Git 增强工具
- **Error Lens**: 内联错误提示
- **Code Spell Checker**: 代码拼写检查

### 2. 浏览器扩展

- **Vue DevTools**: Vue 开发者工具
- **Redux DevTools**: 状态管理调试工具
- **JSON Viewer**: JSON 格式化工具
- **Postman**: API 测试工具
- **Lighthouse**: 性能分析工具

## 📚 学习资源

### 官方文档

- [Vue 3 官方文档](https://v3.vuejs.org/)
- [TypeScript 官方文档](https://www.typescriptlang.org/docs/)
- [Vite 官方文档](https://vitejs.dev/)
- [Element Plus 官方文档](https://element-plus.org/)
- [Pinia 官方文档](https://pinia.vuejs.org/)
- [Vue Router 官方文档](https://router.vuejs.org/)

### 推荐教程

- [Vue Mastery](https://www.vuemastery.com/)
- [Vue School](https://vueschool.io/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [Frontend Masters](https://frontendmasters.com/)

### 社区资源

- [Vue Land](https://vue.land/): Vue 社区资源聚合
- [Vue Use](https://vueuse.org/): Vue Composition API 实用工具集
- [Awesome Vue](https://github.com/vuejs/awesome-vue): Vue 生态系统精选资源
- [TypeScript Playground](https://www.typescriptlang.org/playground): TypeScript 在线编辑器

通过本文档的指导，相信你已经掌握了 FastApiAdmin 前端项目的核心技术和最佳实践。在实际开发中，你可以根据具体需求灵活运用这些知识，构建高质量的前端应用。

### 项目启动步骤

1. **克隆项目**
   ```bash
   git clone https://gitee.com/fastapiadmin/FastapiAdmin.git
   ```

2. **进入前端目录**
   ```bash
   cd FastapiAdmin/frontend
   ```

3. **安装依赖**
   ```bash
   pnpm install
   ```

4. **启动开发服务器**
   ```bash
   pnpm run dev
   ```

5. **访问应用**
   打开浏览器访问 [前端页面](http://localhost:5173) <!-- 本地开发链接 -->

> 默认账号：admin / 123456

## 🔧 二次开发指南

## 🎯 动态菜单系统介绍

### 系统特性

**FastApiAdmin** 采用 **动态路由 + 动态菜单** 的设计模式，具有以下优势：

#### ✅ 优势特点

+ **运行时动态配置**：无需重新编译前端代码
+ **权限控制灵活**：基于角色的菜单权限管理
+ **组件动态加载**：按需加载页面组件
+ **菜单结构自由**：支持多级菜单、目录、按钮、外链
+ **热更新生效**：添加菜单后立即生效

### 动态路由流程详解

1. **后端数据结构**：

```typescript
interface MenuTable {
  id: number
  name: string              // 菜单名称（显示在菜单栏）
  title: string            // 菜单标题（显示在标签页）
  route_path: string       // 路由路径
  route_name: string       // 路由名称
  component_path: string   // 组件路径
  icon: string            // 菜单图标
  type: 'CATALOG' | 'MENU' | 'BUTTON' | 'EXTLINK'
  parent_id?: number       // 父级菜单ID
  order: number           // 排序
  keep_alive: boolean     // 是否缓存
  hidden: boolean         // 是否隐藏
  always_show: boolean    // 只有一个子路由时是否始终显示
  params: Array<{key: string, value: string}> // 路由参数
  status: boolean         // 状态
}
```

2. **前端转换逻辑**：

```typescript
// src/store/modules/permission.store.ts
const generator = (routers: MenuTable[]): RouteVO[] => {
  return routers.map((item) => {
    const currentRouter: RouteVO = {
      path: item.route_path,
      name: item.route_name,
      component: item.component_path,  // 动态组件路径
      meta: {
        title: item.title,
        icon: item.icon,
        keepAlive: item.keep_alive,
        hidden: item.hidden,
      }
    };
    // 递归处理子菜单
    if (item.children) {
      currentRouter.children = generator(item.children);
    }
    return currentRouter;
  });
};
```

3. **组件动态解析**：

```typescript
// 动态导入组件
const modules = import.meta.glob("../../views/**/**.vue");


normalizedRoute.component =
  !normalizedRoute.component
    ? Layout  // 目录使用Layout组件
    : modules[`../../views/${normalizedRoute.component}.vue`] || // 动态导入页面组件
      modules["../../views/error/404.vue"]; // 404页面兜底
```

## 🚀 运行时动态添加页面

### 方法一：通过菜单管理界面添加

#### 步骤1：访问菜单管理

1. 登录系统后，进入 **系统管理 → 菜单管理**
2. 点击 **新增** 按钮

#### 步骤2：创建目录菜单

如果需要先创建父级目录：

```json
{
  "菜单名称": "示例模块",
  "菜单标题": "示例模块",
  "菜单类型": "目录",
  "路由路径": "/example",
  "路由名称": "Example",
  "图标": "Document",
  "排序": 10,
  "状态": "启用"
}
```

#### 步骤3：创建页面菜单

```json
{
  "父级菜单": "示例模块",
  "菜单名称": "用户列表",
  "菜单标题": "用户管理",
  "菜单类型": "菜单",
  "路由路径": "/example/user",
  "路由名称": "ExampleUser",
  "组件路径": "example/user/index",
  "图标": "User",
  "是否缓存": true,
  "排序": 1,
  "状态": "启用"
}
```

#### 步骤4：创建页面组件

在 `src/views/example/user/index.vue` 创建组件：

```vue
<template>
  <div class="app-container">
    <h1>用户列表</h1>

    <div class="content">
      <!-- 页面内容 -->
      <el-table :data="userList" stripe>
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="status" label="状态" />
      </el-table>

    </div>

  </div>

</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义页面name，用于keep-alive缓存
defineOptions({
  name: 'ExampleUserList'
})

const userList = ref([
  { username: 'admin', email: 'admin@example.com', status: '启用' }
])
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

.content {
  margin-top: 20px;
}
</style>

```

#### 步骤5：刷新页面

添加菜单后：

1. 刷新浏览器页面
2. 系统会重新加载用户权限和菜单数据
3. 新菜单立即出现在侧边栏
4. 点击新菜单可访问新页面

## 📝 菜单配置字段详解

### 核心字段说明

| 字段名           | 类型    | 必填     | 说明                                  |
| ---------------- | ------- | -------- | ------------------------------------- |
| `name`           | string  | ✅        | 菜单显示名称                          |
| `title`          | string  | ✅        | 页面标题（标签页显示）                |
| `type`           | enum    | ✅        | 菜单类型：CATALOG/MENU/BUTTON/EXTLINK |
| `route_path`     | string  | ✅        | 路由路径，如 `/system/user`           |
| `route_name`     | string  | ✅        | 路由名称，用于keep-alive缓存          |
| `component_path` | string  | 菜单必填 | 组件路径，相对于 `src/views/`         |
| `parent_id`      | number  | ❌        | 父级菜单ID                            |
| `icon`           | string  | ❌        | 菜单图标，支持 SVG与Element Plus 图标 |
| `order`          | number  | ❌        | 排序号，越小越靠前                    |
| `keep_alive`     | boolean | ❌        | 是否开启页面缓存                      |
| `hidden`         | boolean | ❌        | 是否在菜单中隐藏                      |
| `always_show`    | boolean | ❌        | 只有一个子路由时是否始终显示          |
| `params`         | array   | ❌        | 路由参数数组                          |
| `status`         | boolean | ❌        | 菜单状态：true-启用，false-禁用       |


### 菜单类型详解

#### 1. 目录 (CATALOG)

```json
{
  "type": "CATALOG",
  "route_path": "/system",
  "route_name": "System",
  "component_path": null,
  "children": [...] // 子菜单数组
}
```

#### 2. 菜单 (MENU)

```json
{
  "type": "MENU",
  "route_path": "/system/user",
  "route_name": "SystemUser",
  "component_path": "system/user/index",
  "keep_alive": true
}
```

#### 3. 按钮 (BUTTON)

```json
{
  "type": "BUTTON",
  "name": "用户新增",
  "route_path": null,
  "route_name": null,
  "component_path": null
}
```

#### 4. 外链 (EXTLINK)

```json
{
  "type": "EXTLINK",
  "route_path": "https://example.com",
  "route_name": "ExternalLink"
}
```

### 图标配置

支持的图标格式：

+ Element Plus 图标：`el-icon-User`、`el-icon-Setting`
+ 自定义SVG图标：`icon-user`、`icon-setting`
+ 空值：不显示图标

## 🔄 动态更新的机制

### 路由热更新

当菜单数据发生变化时，系统会：

1. **检测变化**：监听用户权限和菜单数据变化
2. **重新生成路由**：调用 `generateRoutes()` 方法
3. **更新路由表**：动态注册新的路由到 Vue Router
4. **刷新菜单**：更新侧边栏菜单显示
5. **清理缓存**：移除旧的路由缓存

```typescript
// src/store/modules/permission.store.ts
async function generateRoutes() {
  const userStore = useUserStore();
  if (!userStore.hasGetRoute) {
    await userStore.getUserInfo();
  }

  const routersTree = listToTree(userStore.routeList);
  const routerMap = generator(routersTree);
  const dynamicRoutes = parseDynamicRoutes(routerMap);

  routes.value = [...constantRoutes, ...dynamicRoutes];
  routesLoaded.value = true;

  return dynamicRoutes;
}
```

### 组件动态加载

系统使用 Vite 的 `import.meta.glob` 实现组件动态加载：

```typescript
// 预加载所有页面组件
const modules = import.meta.glob("../../views/**/**.vue");

// 动态解析组件
normalizedRoute.component =
  !normalizedRoute.component
    ? Layout  // 目录使用Layout组件
    : modules[`../../views/${normalizedRoute.component}.vue`] ||
      modules["../../views/error/404.vue"]; // 404兜底
```

## 🎯 最佳实践

### 1. 菜单规划

#### 合理的菜单层级

```plain
📁 系统管理 (CATALOG)
├── 👤 用户管理 (MENU)
├── 🔐 角色管理 (MENU)
├── 📋 菜单管理 (MENU)
└── 📝 操作日志 (MENU)
```

### 2. 路由设计

#### 路由路径规范

```typescript
// ✅ 推荐格式
/system/user          // 用户管理
/system/role          // 角色管理
/content/article      // 文章管理
/statistics/dashboard // 数据统计

// ❌ 避免格式
/user-management      // 太长
/usr-mgmt            // 缩写不易懂
```

#### 组件路径规范

```typescript
// ✅ 推荐格式
"system/user/index"           // 用户管理主页面
"system/user/detail"          // 用户详情页面
"content/article/editor"      // 文章编辑器

// ❌ 避免格式
"UserManagement"             // PascalCase
"system/UserList.vue"        // 包含扩展名
```

### 3. 权限控制

#### 菜单权限

```typescript
// 后端控制菜单显示
{
  "name": "用户管理",
  "roles": ["admin", "user_manager"],
  "status": true
}
```

#### 页面权限

```vue
<script setup lang="ts">
// 页面级别权限控制
import { usePermission } from '@/hooks/usePermission'

const { hasPermission } = usePermission()

// 检查权限
if (!hasPermission('user:create')) {
  // 无权限处理
}
</script>

```

### 4. 缓存策略

#### 页面缓存配置

```vue
<script setup lang="ts">
// 启用页面缓存
defineOptions({
  name: 'UserList'  // 与路由名称保持一致
})
</script>

```

#### 缓存控制

```json
{
  "keep_alive": true,      // 启用缓存
  "route_name": "UserList" // 必须与组件name一致
}
```

## 🔧 开发方式（代码层面）

### 1. 添加新页面

#### 步骤1：创建页面组件

在 `src/views/` 下创建新的页面组件：

```vue
<!-- src/views/example/new-page.vue -->
<template>
  <div class="new-page">
    <h1>{{ t('example.newPage') }}</h1>

    <div class="content">
      <!-- 页面内容 -->
    </div>

  </div>

</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style lang="scss" scoped>
.new-page {
  padding: 20px;

  .content {
    // 页面样式
  }
}
</style>

```

#### 步骤2：添加路由配置

在 `src/router/index.ts` 中添加路由：

```typescript
import NewPage from '@/views/example/new-page.vue'

const routes: RouteRecordRaw[] = [
  // ... 其他路由
  {
    path: '/example/new-page',
    name: 'NewPage',
    component: NewPage,
    meta: {
      title: '新页面',
      icon: 'Document',
      keepAlive: true,
      roles: ['admin']
    }
  }
]
```

#### 步骤3：添加菜单配置

如果需要菜单显示，需要在后端菜单配置中添加对应的菜单项。

#### 步骤4：添加国际化

在语言包中添加翻译：

```typescript
// src/lang/package/zh-cn.ts
export default {
  example: {
    newPage: '新页面'
  }
}

// src/lang/package/en.ts
export default {
  example: {
    newPage: 'New Page'
  }
}
```

### 2. 添加新组件

#### 创建全局组件

```vue
<!-- src/components/CustomButton/index.vue -->
<template>
  <el-button
    :type="type"
    :size="size"
    :loading="loading"
    @click="handleClick"
  >
    <slot />
  </el-button>

</template>

<script setup lang="ts">
import { ElButton } from 'element-plus'

interface Props {
  type?: 'primary' | 'success' | 'warning' | 'danger'
  size?: 'large' | 'default' | 'small'
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'primary',
  size: 'default',
  loading: false
})

const emit = defineEmits<{
  click: []
}>()

const handleClick = () => {
  emit('click')
}
</script>

```

#### 导出组件

在 `src/components/index.ts` 中导出：

```typescript
export { default as CustomButton } from './CustomButton/index.vue'
```

### 3. 添加API接口

#### 创建API模块

```typescript
// src/api/example.ts
import request from '@/utils/request'

export interface ExampleData {
  id: number
  name: string
  status: string
}

export const getExampleList = (params?: any) => {
  return request.get('/example/list', { params })
}

export const createExample = (data: Omit<ExampleData, 'id'>) => {
  return request.post('/example', data)
}

export const updateExample = (id: number, data: Partial<ExampleData>) => {
  return request.put(`/example/${id}`, data)
}

export const deleteExample = (id: number) => {
  return request.delete(`/example/${id}`)
}
```

### 4. 添加状态管理

#### 创建Store模块

```typescript
// src/store/modules/example.store.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ExampleData } from '@/api/example'

export const useExampleStore = defineStore('example', () => {
  // 状态
  const exampleList = ref<ExampleData[]>([])
  const loading = ref(false)

  // 计算属性
  const activeExamples = computed(() =>
    exampleList.value.filter(item => item.status === 'active')
  )

  // 动作
  const fetchExampleList = async () => {
    loading.value = true
    try {
      const { data } = await getExampleList()
      exampleList.value = data
    } catch (error) {
      console.error('获取示例列表失败:', error)
    } finally {
      loading.value = false
    }
  }

  const addExample = async (data: Omit<ExampleData, 'id'>) => {
    await createExample(data)
    await fetchExampleList()
  }

  const updateExample = async (id: number, data: Partial<ExampleData>) => {
    await updateExample(id, data)
    await fetchExampleList()
  }

  const removeExample = async (id: number) => {
    await deleteExample(id)
    await fetchExampleList()
  }

  return {
    // 状态
    exampleList,
    loading,

    // 计算属性
    activeExamples,

    // 动作
    fetchExampleList,
    addExample,
    updateExample,
    removeExample
  }
})
```

### 5. 添加工具函数

```typescript
// src/utils/example.ts
/**
 * 格式化示例数据
 */
export const formatExampleData = (data: any): ExampleData => {
  return {
    id: data.id,
    name: data.name || '',
    status: data.status || 'inactive'
  }
}

/**
 * 验证示例数据
 */
export const validateExampleData = (data: Partial<ExampleData>): string[] => {
  const errors: string[] = []

  if (!data.name?.trim()) {
    errors.push('名称不能为空')
  }

  if (!data.status) {
    errors.push('状态不能为空')
  }

  return errors
}
```

### 6. 添加类型定义

```typescript
// src/types/example.d.ts
export interface ExampleData {
  id: number
  name: string
  status: 'active' | 'inactive'
  createdAt: string
  updatedAt: string
}

export interface ExampleForm {
  name: string
  status: 'active' | 'inactive'
}

export interface ExampleQuery {
  page?: number
  size?: number
  name?: string
  status?: 'active' | 'inactive'
}
```

### 7. 添加常量和枚举

```typescript
// src/constants/example.ts
export const EXAMPLE_STATUS = {
  ACTIVE: 'active',
  INACTIVE: 'inactive'
} as const

export const EXAMPLE_STATUS_TEXT = {
  [EXAMPLE_STATUS.ACTIVE]: '启用',
  [EXAMPLE_STATUS.INACTIVE]: '禁用'
} as const

export const EXAMPLE_PAGE_SIZE = 20
```

### 8. 使用 UnoCSS

项目使用 UnoCSS 进行原子化CSS开发：

```vue
<template>
  <div class="example">
    <!-- 使用 UnoCSS 类名 -->
    <div class="flex items-center justify-between p-4 bg-white rounded-lg shadow-md">
      <h1 class="text-xl font-bold text-gray-800">标题</h1>

      <el-button type="primary" class="ml-4">按钮</el-button>

    </div>

  </div>

</template>

```

常用 UnoCSS 类名：

+ **布局**: `flex`, `grid`, `block`, `inline-block`
+ **定位**: `relative`, `absolute`, `fixed`
+ **间距**: `p-4`, `m-2`, `mt-4`, `mb-4`, `ml-4`, `mr-4`
+ **颜色**: `text-red-500`, `bg-blue-500`, `border-gray-300`
+ **尺寸**: `w-4`, `h-8`, `min-w-20`, `max-h-100`
+ **边框**: `border`, `border-t`, `border-solid`, `rounded`, `rounded-lg`
+ **阴影**: `shadow`, `shadow-lg`, `shadow-xl`
+ **文字**: `text-sm`, `text-lg`, `font-bold`, `text-center`

## 🎨 主题和样式

### 主题配置

项目支持明暗主题切换，主题变量定义在：

```sass
// src/styles/variables.scss
:root {
  // 亮色主题
  --el-color-primary: #409eff;
  --el-color-success: #67c23a;
  --el-color-warning: #e6a23c;
  --el-color-danger: #f56c6c;
  --el-color-info: #909399;
}

// 暗色主题
.dark {
  --el-color-primary: #66d9ef;
  --el-color-success: #a6e22e;
  --el-color-warning: #fd971f;
  --el-color-danger: #f92672;
  --el-color-info: #75715e;
}
```

### 自定义样式

#### 全局样式

在 `src/styles/index.scss` 中添加全局样式：

```sass
// 自定义全局样式
.custom-class {
  // 自定义样式
}
```

#### 组件样式

使用 scoped 样式：

```vue
<style lang="scss" scoped>
.my-component {
  .title {
    @apply text-xl font-bold text-gray-800 mb-4;
  }

  .content {
    @apply p-4 bg-white rounded-lg shadow-md;
  }
}
</style>

```

## 🔧 开发规范

### 代码规范

项目使用 ESLint + Prettier 进行代码规范检查：

```bash
# 检查代码
pnpm run lint

# 修复代码
pnpm run lint:fix
```

### Git 提交规范

项目使用 Husky + commitizen 进行 Git 提交规范：

```bash
# 交互式提交
pnpm run commit

# 或直接提交
git commit -m "feat: 添加新功能"
```

提交类型：

+ `feat`: 新功能
+ `fix`: 修复bug
+ `docs`: 文档更新
+ `style`: 代码格式调整
+ `refactor`: 代码重构
+ `test`: 测试相关
+ `chore`: 构建过程或工具配置更新

## 🚀 部署指南

### 构建生产版本

```bash
# 构建生产版本
pnpm run build

# 构建特定环境
pnpm run build:pro    # 生产环境
pnpm run build:dev    # 开发环境
pnpm run build:test   # 测试环境
```

### Nginx 配置

```nginx
# 前端代理 - /web访问前端
location /web {
    alias /usr/share/nginx/html/frontend/dist;
    try_files $uri $uri/ /web/index.html; #解决页面刷新404问题
}
```

## 🌍 国际化配置

### 国际化架构

项目使用 Vue I18n 进行国际化管理：

```plain
src/lang/
├── 📁 package/         # 语言包
│   ├── zh-cn.ts       # 中文语言包
│   └── en.ts          # 英文语言包
└── index.ts           # 国际化配置
```

### 语言包配置

```typescript
// src/lang/package/zh-cn.ts
export default {
  common: {
    confirm: '确定',
    cancel: '取消',
    save: '保存',
    delete: '删除',
    edit: '编辑',
    add: '新增',
    search: '搜索',
    reset: '重置',
    export: '导出',
    import: '导入'
  },
  menu: {
    dashboard: '仪表板',
    system: '系统管理',
    user: '用户管理',
    role: '角色管理',
    menu: '菜单管理'
  },
  message: {
    success: '操作成功',
    error: '操作失败',
    confirmDelete: '确定要删除这条记录吗？',
    noPermission: '没有权限访问'
  }
}
```

### 在组件中使用

```vue
<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div>
    <h1>{{ t('menu.dashboard') }}</h1>

    <el-button>{{ t('common.save') }}</el-button>

  </div>

</template>

```

## 🛡️ 错误处理机制

### 全局错误处理

```typescript
// src/utils/errorHandler.ts
import { ElMessage } from 'element-plus'

export const setupErrorHandler = (app: App) => {
  // Vue 错误处理
  app.config.errorHandler = (err: Error, instance, info) => {
    console.error('Vue Error:', err, info)
    handleError(err)
  }

  // 全局错误处理函数
  const handleError = (error: any) => {
    if (error.code === 'NETWORK_ERROR') {
      ElMessage.error('网络连接失败')
    } else if (error.code === 401) {
      ElMessage.error('登录已过期，请重新登录')
      router.push('/login')
    } else if (error.code === 403) {
      ElMessage.error('没有权限访问')
    } else {
      ElMessage.error(error.message || '发生未知错误')
    }
  }
}
```

### 错误边界组件

```vue
<!-- src/components/ErrorBoundary.vue -->
<script setup lang="ts">
import { onErrorCaptured } from 'vue'

const error = ref<Error | null>(null)

onErrorCaptured((err) => {
  error.value = err
  return false
})

const handleRetry = () => {
  error.value = null
  window.location.reload()
}
</script>

<template>
  <div v-if="error" class="error-boundary">
    <div class="error-content">
      <h2>出错了！</h2>

      <p>{{ error.message }}</p>

      <el-button @click="handleRetry">重试</el-button>

    </div>

  </div>

  <slot v-else />
</template>

```

## ❓ 常见问题解答

### 项目配置问题

**Q: 如何修改项目的标题和Logo？**

A: 在 `src/settings.ts` 中修改应用配置：

```typescript
export const settings = {
  title: '你的应用名称',
  logo: '/path/to/your/logo.png'
}
```

**Q: 如何修改主题色？**

A: 在 `src/styles/variables.scss` 中修改CSS变量：

```sass
:root {
  --el-color-primary: #your-color;
}
```

**Q: 如何添加新的环境变量？**

A: 在对应的 `.env` 文件中添加变量，然后在代码中使用：

```bash
# .env.development
VITE_APP_NEW_VAR=value
```

```typescript
// 在代码中使用
const newVar = import.meta.env.VITE_APP_NEW_VAR
```

### 开发问题汇总

**Q: 组件样式不生效怎么办？**

A: 检查以下几点：

1. 是否使用了 `scoped` 样式
2. CSS 类名是否正确
3. 是否使用了正确的 UnoCSS 类名
4. 样式优先级是否正确

**Q: API请求失败怎么办？**

A: 检查以下几点：

1. 后端服务是否启动
2. API地址是否正确
3. 请求头是否包含认证信息
4. 网络连接是否正常

**Q: 路由跳转失败怎么办？**

A: 检查以下几点：

1. 路由路径是否正确
2. 路由组件是否存在
3. 路由权限是否正确
4. 路由参数是否正确传递

### 性能问题

**Q: 页面加载慢怎么办？**

A: 尝试以下优化：

1. 启用代码分割和懒加载
2. 优化图片资源
3. 启用压缩和缓存
4. 使用CDN加速

### 部署问题

**Q: 部署后页面空白怎么办？**

A: 检查以下几点：

1. 构建是否成功
2. 静态资源路径是否正确
3. 服务器配置是否正确
4. 路由模式是否匹配服务器配置

**Q: API请求跨域怎么办？**

A: 配置代理或修改服务器CORS设置：

```typescript
// vite.config.ts
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

## 📚 常用资源

### 官方文档

+ [Vue 3](https://cn.vuejs.org/)
+ [TypeScript](https://www.typescriptlang.org/)
+ [Vite](https://cn.vitejs.dev/)
+ [Element Plus](https://element-plus.org/)
+ [Pinia](https://pinia.vuejs.org/)
+ [UnoCSS](https://unocss.dev/)

### 📚 学习路径

1. **新手入门** - 阅读快速开始和项目结构
2. **功能开发** - 学习动态菜单系统和API接口管理
3. **高级特性** - 掌握性能优化和安全性配置（后续更新）
4. **生产部署** - 完成项目上线

## 🧩 代码生成模块

代码生成模块是本项目的核心功能之一，可以帮助开发者快速生成完整的 CRUD 代码。该模块基于 Vue3 和 Element Plus 构建，提供了直观的用户界面来配置和生成代码。

### 前端组件结构

代码生成模块的前端组件位于 `src/views/gencode/backcode/index.vue`，采用了多步骤向导式界面：

1. **基础配置步骤**：配置表的基本信息和生成参数
2. **字段配置步骤**：配置每个字段的属性和行为
3. **代码预览步骤**：预览将要生成的代码内容
4. **代码生成步骤**：配置生成选项并执行代码生成

### 核心功能

1. **表管理**：
   - 创建新表（通过SQL语句）
   - 导入现有数据库表
   - 编辑表结构和字段配置
   - 删除代码生成配置

2. **字段配置**：
   - 配置字段的显示类型（文本框、下拉框、日期控件等）
   - 设置字段的查询方式和查询条件
   - 配置字段的验证规则和默认值
   - 设置字段的字典类型用于下拉选项

3. **代码预览**：
   - 实时预览生成的后端代码（Python）
   - 实时预览生成的前端代码（Vue/TypeScript）
   - 实时预览生成的数据库脚本（SQL）
   - 支持按类型筛选预览内容

4. **代码生成**：
   - 生成并下载ZIP压缩包
   - 直接写入到项目目录中

### API 接口

代码生成相关的API接口定义在 `src/api/generator/gencode.ts` 文件中，主要包括：

- `listTable`：查询代码生成业务表列表
- `listDbTable`：查询数据库表列表
- `importTable`：导入表结构
- `getGenTableDetail`：获取业务表详细信息
- `createTable`：创建表
- `updateTable`：编辑业务表信息
- `deleteTable`：删除业务表信息
- `batchGenCode`：批量生成代码
- `genCodeToPath`：生成代码到指定路径
- `previewTable`：预览代码
- `syncDb`：同步数据库

### 使用流程

1. **准备工作**：
   - 在数据库中创建业务表
   - 确保后端服务正常运行

2. **导入表结构**：
   - 进入代码生成页面
   - 点击"导入"按钮
   - 选择要导入的数据库表

3. **配置生成参数**：
   - 在基础配置步骤中填写：
     - 生成包路径（package_name）
     - 生成模块名（module_name）
     - 生成业务名（business_name）
     - 生成功能名（function_name）
     - 选择上级菜单

4. **配置字段属性**：
   - 在字段配置步骤中设置每个字段的：
     - 是否为主键、是否必填
     - 是否为插入字段、编辑字段、列表字段、查询字段
     - 显示类型和查询方式
     - 字典类型（用于下拉选项）

5. **预览代码**：
   - 进入代码预览步骤
   - 查看生成的后端、前端、数据库代码
   - 确认代码内容无误

6. **生成代码**：
   - 进入代码生成步骤
   - 选择生成方式（下载ZIP包或写入本地）
   - 点击相应按钮执行代码生成

7. **集成使用**：
   - 如果选择了下载方式，解压ZIP包并按项目结构复制到对应目录
   - 如果选择了写入本地方式，代码已直接写入项目目录
   - 重启服务，新功能模块即可使用

## 🎯 总结

**FastApiAdmin** 前端项目提供了一套完整的企业级后台管理系统解决方案，具有以下优势：

1. **现代化技术栈**：基于 Vue3、Vite、TypeScript 等前沿技术构建
2. **高度模块化**：清晰的项目结构，便于维护和扩展
3. **开箱即用**：丰富的功能模块，减少重复开发工作
4. **易于定制**：灵活的配置选项，适应不同业务需求
5. **良好文档**：详细的开发指南，降低学习成本

通过本指南，您应该能够快速上手并开发出功能完善的后台管理系统。在开发过程中，建议遵循项目规范，合理利用现有组件和工具，以提高开发效率和代码质量。

---

**祝您开发愉快！使用这个模板构建出色的后台管理系统**

