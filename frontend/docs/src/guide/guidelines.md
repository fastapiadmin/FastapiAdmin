---
outline: "deep"
title: 开发规范
---
# 开发规范

## 📚规范概述

为了保证项目代码的一致性、可读性和可维护性，FastapiAdmin 项目制定了以下开发规范。所有参与项目开发的开发者都应该遵循这些规范。

## 🎨前端开发规范

### 1. 代码风格

#### 1.1 TypeScript 规范

- 使用 TypeScript 严格模式（`"strict": true`）
- 为所有变量、函数、接口添加类型注解
- 避免使用 `any` 类型，除非确实无法确定类型
- 使用接口定义对象类型，而不是类型别名
- 使用枚举定义常量集合
- 使用 `type` 定义联合类型和交叉类型
- 使用 `as const` 断言确保类型安全
- 使用 `readonly` 修饰符保护不可变数据
- 使用 `unknown` 类型处理不确定类型的数据

#### 1.2 Vue 规范

- 使用 Composition API
- 使用 `<script setup lang="ts">` 语法
- 组件命名使用 PascalCase
- 变量和函数命名使用 camelCase
- 常量命名使用 UPPER_SNAKE_CASE
- 使用 `ref()` 定义响应式变量
- 使用 `computed()` 定义计算属性
- 使用 `watch()` 或 `watchEffect()` 监听变化
- 使用 `onMounted()`、`onUnmounted()` 等生命周期钩子
- 组件 props 使用 `defineProps()` 定义并添加类型
- 组件事件使用 `defineEmits()` 定义并添加类型
- 组件暴露的属性和方法使用 `defineExpose()` 定义

#### 1.3 CSS 规范

- 使用 UnoCSS 原子化 CSS
- 避免使用内联样式
- 使用 BEM 命名规范（如果不使用 UnoCSS）
- 类名使用 kebab-case
- 避免使用 ID 选择器
- 使用 CSS 变量管理主题
- 避免使用 `!important` 修饰符
- 使用 flexbox 布局确保跨平台一致性
- 合理使用 CSS Grid 布局
- 优化 CSS 选择器优先级

### 2. 组件开发最佳实践

- **单一职责原则**：每个组件只负责一个功能
- **props 设计**：
  - 使用 `required` 和 `default` 明确 props 要求
  - 为复杂 props 添加验证
  - 使用 `withDefaults()` 为 props 设置默认值
- **事件设计**：
  - 使用 kebab-case 命名事件
  - 事件参数类型明确
  - 避免在事件中传递过多参数
- **插槽设计**：
  - 使用具名插槽提高可读性
  - 为插槽添加默认内容
  - 使用作用域插槽传递数据
- **样式设计**：
  - 使用 `scoped` 样式避免冲突
  - 合理使用 `:deep()` 选择器
  - 避免在组件中使用全局样式

### 3. 状态管理最佳实践

- **模块化设计**：按功能模块拆分 store
- **状态定义**：
  - 使用 `interface` 定义 state 类型
  - 初始化所有状态
  - 避免使用嵌套过深的状态结构
- **Actions 设计**：
  - 处理异步操作
  - 使用 try/catch 捕获错误
  - 提交多个 mutations 时使用事务
- **Getters 设计**：
  - 缓存计算结果
  - 避免在 getters 中修改状态
  - 合理使用参数化 getters

### 4. API 调用最佳实践

- **模块化管理**：按功能模块组织 API 接口
- **请求封装**：
  - 统一处理请求头
  - 统一处理错误
  - 统一处理 loading 状态
- **响应处理**：
  - 类型定义响应数据结构
  - 统一处理响应状态码
  - 合理处理空数据和边界情况
- **请求优化**：
  - 使用防抖和节流
  - 缓存频繁请求的结果
  - 合理使用并发请求

### 5. 性能优化建议

- **代码分割**：使用路由懒加载和组件懒加载
- **资源优化**：
  - 压缩图片和静态资源
  - 使用 WebP 格式图片
  - 合理使用 CDN
- **渲染优化**：
  - 使用 `v-memo` 缓存计算结果
  - 合理使用 `v-if` 和 `v-show`
  - 避免在模板中使用复杂表达式
- **网络优化**：
  - 使用 HTTP/2 或 HTTP/3
  - 启用 Gzip 或 Brotli 压缩
  - 合理设置缓存策略

### 6. 测试最佳实践

- **测试分层**：单元测试、集成测试、端到端测试
- **测试覆盖率**：
  - 核心功能 100% 覆盖
  - 复杂逻辑 80% 以上覆盖
  - 简单功能 50% 以上覆盖
- **测试工具**：
  - 使用 Vitest 进行单元测试
  - 使用 Playwright 进行端到端测试
  - 使用 Vue Test Utils 进行组件测试

### 7. 代码审查要点

- **类型安全**：检查 TypeScript 类型定义是否正确
- **代码质量**：检查代码是否简洁、清晰
- **性能问题**：检查是否存在性能瓶颈
- **安全问题**：检查是否存在安全漏洞
- **规范遵循**：检查是否遵循项目开发规范

## 🐍后端开发规范

### 1. 代码风格

#### 1.1 Python 规范

- 遵循 PEP 8 代码风格
- 使用 4 个空格缩进
- 行长度不超过 100 字符
- 函数和类之间空两行
- 方法之间空一行
- 导入语句按标准库、第三方库、本地库分组

#### 1.2 FastAPI 规范

- 使用 FastAPI 装饰器定义路由
- 使用 Pydantic 模型定义请求和响应数据
- 使用依赖注入处理认证和权限
- 使用路径参数和查询参数
- 使用 HTTPException 处理错误
- 使用 Depends 注入依赖

### 2. 目录结构

```
backend/app/
├── api/             # API 接口
├── common/          # 公共代码
├── config/          # 配置管理
├── core/            # 核心功能
├── plugin/          # 插件系统
├── scripts/         # 脚本工具
└── utils/           # 工具函数
```

### 3. 插件开发规范

- 插件目录应该以 `module_` 开头
- 插件应该包含 `controller.py`、`model.py`、`schema.py`、`service.py`、`crud.py` 等文件
- 控制器应该使用 `APIRouter` 定义路由
- 路由前缀应该与模块名对应（module_xxx -> /xxx）
- 控制器应该使用 `OperationLogRoute` 记录操作日志
- 接口应该使用 `AuthPermission` 进行权限控制

### 4. 数据库规范

- 使用 SQLAlchemy 2.0 ORM
- 使用 Alembic 进行数据库迁移
- 模型类应该继承自 `Base`
- 模型类应该定义 `__tablename__` 属性
- 字段命名应该使用 snake_case
- 表名应该使用 snake_case 复数形式
- 外键应该使用 `ForeignKey` 定义
- 关系应该使用 `relationship` 定义

### 5. 认证和权限规范

- 使用 JWT 进行身份认证
- 使用 RBAC 模型进行权限管理
- 接口应该添加权限控制装饰器
- 权限字符串格式：`module:controller:action`
- 权限应该在角色管理中配置

### 6. 错误处理规范

- 使用 `HTTPException` 处理 HTTP 错误
- 使用自定义异常处理全局错误
- 错误响应应该有统一的格式
- 错误应该记录到日志

### 7. 日志规范

- 使用 Python 标准库 `logging` 模块
- 日志级别：DEBUG、INFO、WARNING、ERROR、CRITICAL
- 日志应该包含时间、级别、模块、消息等信息
- 关键操作应该记录日志
- 错误应该记录详细信息

## 📦FastApp 移动端开发规范

### 1. 代码风格

- 遵循前端开发规范
- 使用 TypeScript 严格模式
- 使用 Vue 3 Composition API
- 使用 `<script setup lang="ts">` 语法
- 组件命名使用 PascalCase
- 变量和函数命名使用 camelCase

### 2. 目录结构

```
FastApp/src/
├── api/             # API 接口
├── components/      # 组件
├── composables/     # 组合式函数
├── constants/       # 常量定义
├── enums/           # 枚举定义
├── layouts/         # 布局组件
├── pages/           # 页面文件
├── router/          # 路由配置
├── static/          # 静态资源
├── store/           # 状态管理
├── styles/          # 样式文件
├── types/           # TypeScript 类型定义
├── utils/           # 工具函数
├── App.vue          # 应用根组件
└── main.ts          # 应用入口文件
```

### 3. 页面开发规范

- 页面组件应该放在 `pages` 目录下
- 页面目录应该使用 kebab-case
- 页面组件应该包含 `index.vue` 文件
- 页面组件可以包含 `data.ts`、`types.ts` 等辅助文件
- 页面组件应该使用 `onLoad()`、`onShow()` 等生命周期钩子
- 页面跳转应该使用 `uni.navigateTo()`、`uni.switchTab()` 等 API

### 4. API 调用规范

- 遵循前端 API 调用规范
- 使用封装的 `request.ts` 工具
- API 接口应该按模块分类
- API 调用应该处理错误情况
- API 调用应该显示加载状态

### 5. 跨平台适配规范

- 使用条件编译处理平台差异
- 使用 `#ifdef`、`#ifndef`、`#endif` 指令
- 平台特有 API 应该添加条件编译
- 样式应该考虑不同平台的差异
- 布局应该使用 flexbox 确保跨平台一致性

## 🎯Git 提交规范

### 1. 分支管理

- `master`：主分支，用于发布生产版本
- `dev`：开发分支，用于集成开发
- `feature/xxx`：功能分支，用于开发新功能
- `bugfix/xxx`：修复分支，用于修复 bug
- `hotfix/xxx`：热修复分支，用于紧急修复生产环境问题

### 2. 提交信息规范

提交信息应该遵循以下格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 2.1 Type

- `feat`：新功能
- `fix`：修复 bug
- `docs`：文档修改
- `style`：代码风格修改
- `refactor`：代码重构
- `test`：测试代码修改
- `chore`：构建工具或依赖修改
- `revert`：回滚提交

#### 2.2 Scope

- 可选，用于指定修改的范围
- 例如：`api`、`component`、`page`、`store` 等

#### 2.3 Subject

- 简短的提交信息，不超过 50 个字符
- 使用祈使句，动词开头
- 首字母小写
- 不需要句号结尾

#### 2.4 Body

- 可选，详细的提交信息
- 每行不超过 72 个字符
- 解释为什么修改，而不是如何修改

#### 2.5 Footer

- 可选，用于引用 issue 或 BUG
- 例如：`Closes #123`、`Fixes #456`

### 3. 提交示例

```
feat(api): 添加用户登录接口

- 实现用户登录功能
- 添加 JWT 认证
- 处理登录错误情况

Closes #123
```

```
fix(frontend): 修复首页轮播图显示问题

- 修复轮播图高度计算错误
- 优化轮播图切换动画

Fixes #456
```

```
docs: 更新开发文档

- 添加 API 文档说明
- 完善部署指南
```

### 4. Pull Request 规范

- Pull Request 应该从功能分支合并到 dev 分支
- Pull Request 标题应该清晰、语义化
- Pull Request 描述应该详细说明修改内容
- Pull Request 应该包含相关的 issue 链接
- Pull Request 应该通过所有测试
- Pull Request 应该由至少一个 reviewer 审核

## 🔧工具链规范

### 1. 前端工具链

- 使用 Vite 作为构建工具
- 使用 ESLint 进行代码检查
- 使用 Prettier 进行代码格式化
- 使用 Stylelint 进行样式检查
- 使用 Husky 进行 Git 钩子管理
- 使用 Commitlint 进行提交信息检查

### 2. 后端工具链

- 使用 Poetry 或 pip 管理依赖
- 使用 Pylint 或 Flake8 进行代码检查
- 使用 Black 进行代码格式化
- 使用 MyPy 进行类型检查
- 使用 pytest 进行测试

## 💡开发流程规范

### 1. 需求分析

- 明确功能需求
- 分析业务逻辑
- 确定技术方案

### 2. 设计阶段

- 设计数据库表结构
- 设计 API 接口
- 设计前端页面
- 设计组件结构

### 3. 开发阶段

- 创建分支
- 实现功能
- 编写测试
- 运行测试

### 4. 测试阶段

- 单元测试
- 集成测试
- 端到端测试
- 性能测试

### 5. 部署阶段

- 构建生产版本
- 部署到测试环境
- 进行回归测试
- 部署到生产环境

### 6. 维护阶段

- 监控系统运行状态
- 处理 bug 和问题
- 进行性能优化
- 进行功能迭代

## 📚参考资料

- [TypeScript 官方文档](https://www.typescriptlang.org/docs/)
- [Vue 官方文档](https://vuejs.org/docs/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/)
- [PEP 8 代码风格指南](https://peps.python.org/pep-0008/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [ESLint 官方文档](https://eslint.org/docs/)
- [Prettier 官方文档](https://prettier.io/docs/en/)

## 🤝贡献指南

如果您对开发规范有任何建议或改进意见，欢迎提交 Issue 或 Pull Request。我们会认真考虑每一个建议，不断完善开发规范。

## 📄许可协议

本开发规范文档采用 MIT 许可协议，与 FastapiAdmin 项目保持一致。

