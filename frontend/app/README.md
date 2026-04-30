<div align="center">
  <p align="center">
    <img src="https://gitee.com/fastapiadmin/FastDocs/raw/master/docs/public/logo.png" width="200" />
  </p>
  <h1 align="center">
    FastApp
    <sup style="background-color: #28a745; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.4em; vertical-align: super; margin-left: 5px;">
    v2.0.0
  </h1>
  <p align="center">
    ⚡️ FastApp 基于 uni-app + Vue 3 + TypeScript 的现代化移动端跨平台开发模板， ⭐️ 支持一下吧！
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Vue-3.5.22-green.svg" alt="Vue">
    <img src="https://img.shields.io/badge/TypeScript-5.9.2-blue.svg" alt="TypeScript">
    <img src="https://img.shields.io/badge/uni--app-3.0.0-orange.svg" alt="uni-app">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </p>
  <p align="center">
    <a href="https://service.fastapiadmin.com/app">📱 在线预览</a>
    <a href="https://service.fastapiadmin.com/">📖 在线文档</a>
  </p>
</div>

## 📖 项目介绍

FastApp 是 FastapiAdmin 项目的移动端应用，基于 uni-app 框架开发，支持一套代码多端运行。采用 Vue 3 + TypeScript + Vite 等现代化技术栈，集成了完善的代码规范和开发工具链，为开发者提供开箱即用的移动端开发解决方案。

## ⭐️ 核心特点

- ⚡️ [Vue 3](https://github.com/vuejs/core), [Vite](https://github.com/vitejs/vite), [pnpm](https://pnpm.io/), [esbuild](https://github.com/evanw/esbuild) - 就是快！

- 🐂 [Wot UI](https://github.com/Moonofweisheng/wot-design-uni) - 基于 Vue3 + TypeScript 的 uni-app 组件库，提供 70+ 高质量组件，支持国际化（内置多语言包）、暗黑模式与通过 CSS 变量进行主题定制

- 🚦 [@wot-ui/router](https://github.com/wot-ui/my-uni) - 适用于uni-app&vue3的轻量级路由库

- 🔄 [Uni Mini CI](https://github.com/Moonofweisheng/uni-mini-ci) - 一个小程序端持续集成的插件

- 🌐 [Alova](https://alova.js.org/zh-CN/) - 极致高效的请求工具集

- 🆒 [Uni Ku](https://uni-ku.js.org/) - 非常酷的 uni-app 插件库

- 📊 [Uni Echarts](https://uni-echarts.xiaohe.ink/) - 适用于 uni-app 的 Apache ECharts 组件

- 🎨 [UnoCSS](https://github.com/unocss/unocss) - 高性能且极具灵活性的即时原子化 CSS 引擎

- 📥 [API 自动加载](https://github.com/antfu/unplugin-auto-import) - 直接使用 Composition API 无需引入

- 🦾 [TypeScript](https://www.typescriptlang.org/) & [ESLint](https://eslint.org/) - 保证代码质量

## 🔗 源码仓库

| 平台       | 仓库地址                                                                                                                                                                                         |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **GitHub** | [FastapiAdmin主工程](https://github.com/fastapiadmin/FastapiAdmin.git) \| [FastDocs官网](https://github.com/fastapiadmin/FastDocs.git) \| [FastApp移动端](https://github.com/fastapiadmin/FastApp.git) |
| **Gitee**  | [FastapiAdmin主工程](https://gitee.com/fastapiadmin/FastapiAdmin.git) \| [FastDocs官网](https://gitee.com/fastapiadmin/FastDocs.git) \| [FastApp移动端](https://gitee.com/fastapiadmin/FastApp.git)          |

## 📁 项目结构

```bash
FastApp/
├── public/                       # 静态资源目录
├── src/
│   ├── api/                     # API 接口定义
│   ├── components/              # 公共组件
│   │   ├── DateQuery/           # 日期查询组件
│   │   └── Picker/              # 选择器组件
│   ├── composables/             # 组合式函数
│   ├── constants/               # 常量定义
│   ├── enums/                   # 枚举定义
│   ├── http/                    # HTTP 请求相关
│   │   ├── adapters/            # 请求适配器
│   │   ├── tools/               # 工具函数
│   │   └── types.ts             # 类型定义
│   ├── layouts/                 # 布局组件
│   ├── pages/                   # 页面目录
│   │   ├── index/               # 首页
│   │   ├── login/               # 登录页
│   │   ├── work/                # 工作台
│   │   └── mine/                # 个人中心
│   ├── router/                  # 路由配置
│   ├── store/                   # 状态管理
│   │   ├── modules/             # 模块
│   │   └── index.ts             # 入口文件
│   ├── styles/                  # 样式文件
│   ├── types/                   # TypeScript 类型定义
│   ├── utils/                   # 工具函数
│   ├── App.vue                  # 应用根组件
│   ├── main.ts                  # 应用入口文件
│   ├── manifest.json            # 应用配置文件
│   ├── pages.json               # 页面路由配置
│   └── theme.json               # 主题配置
├── dist/                        # 构建输出目录
├── eslint.config.mjs            # ESLint 配置
├── vite.config.ts               # Vite 配置
├── tsconfig.json                # TypeScript 配置
├── pages.config.ts              # 页面配置
├── unocss.config.ts             # UnoCSS 配置
└── package.json                 # 项目依赖配置
```

## 📸 项目截图

| 登录 <div style="width:60px"/> | 首页 <div style="width:60px"/> | 个人中心 <div style="width:60px"/> |
|----------|----------|----------|
| ![移动端登录](https://gitee.com/fastapiadmin/FastDocs/raw/master/docs/public/app_login.png) | ![移动端首页](https://gitee.com/fastapiadmin/FastDocs/raw/master/docs/public/app_home.png) | ![移动端个人中心](https://gitee.com/fastapiadmin/FastDocs/raw/master/docs/public/app_mine.png) |

## 🚀 快速开始

### 环境要求

- **Node.js** >= 22
- **pnpm** >= 9

### 安装依赖

```bash
# 安装项目依赖
pnpm install

# 启动 H5 开发服务器
pnpm run dev:h5

# 构建 H5 应用
pnpm run build:h5

# ESLint 检查并自动修复
pnpm run lint:eslint

# Prettier 格式化
pnpm run lint:prettier

# Stylelint 检查样式
pnpm run lint:stylelint

# TypeScript 类型检查
pnpm run type-check
```

---

## 🙏 鸣谢

- [uni-app](https://uniapp.dcloud.net.cn/) - 跨平台应用开发框架
- [Vue 3](https://cn.vuejs.org/) - 渐进式 JavaScript 框架（Composition API）
- [Vite](https://cn.vitejs.dev/) - 下一代前端构建工具
- [uni-helper](https://github.com/uni-helper) - 感谢 uni-helper 团队为 uni-app 开发体验优化做出的贡献。
- [vitesse-uni-app](https://github.com/uni-helper/vitesse-uni-app) - 感谢 vitesse-uni-app 提供的快速起手项目。
- [uni-ku](https://uni-ku.js.org/) - 感谢 uni-ku 团队为 uni-app 插件生态做出的贡献。

---

## 🌟 贡献者们

感谢以下所有给 FastApp 贡献过代码的 [开发者](https://github.com/FastapiAdmin/FastApp/graphs/contributors)。

<a href="https://github.com/FastapiAdmin/FastApp/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=FastapiAdmin/FastApp" />
</a>

---

## 🎨 社区交流

| 群组二维码 | 微信支付二维码 |
| --- | --- |
| ![群组二维码](https://gitee.com/fastapiadmin/FastDocs/raw/master/docs/public/group.jpg) | ![微信支付二维码](https://gitee.com/fastapiadmin/FastDocs/raw/master/docs/public/wechatPay.jpg) |

---

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证。

[![Star History Chart](https://api.star-history.com/svg?repos=FastapiAdmin/FastApp&type=Date)](https://star-history.com/#FastapiAdmin/FastApp&Date)

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐ Star**

Made with ❤️ by FastApp Team

</div>
