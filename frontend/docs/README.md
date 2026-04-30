# FastDocs

FastDocs是FastapiAdmin 官网文档，该项目是一套完全开源的快速开发平台，提供免费使用。它结合了现代、高性能的技术栈，后端采用Fastapi + SQLAlchemy，前端采用基于 vue3 + typescript + vite + pinia + Element-Plus。旨在帮助开发者快速搭建高质量的中后台系统。

## 项目结构

```sh
FastDocs/
├─ docs                 # 源代码
│  ├─ .vitepress           # VitePress配置
│  │  ├─ cache/          # 缓存目录
│  │  ├─ theme/          # 主题配置
│  │  │  ├─ index.ts     # 主题入口
│  │  │  └─ style.css    # 主题样式
│  │  └─ config.ts       # 主配置文件
│  ├─ en/                # 英文文档
│  │  ├─ about/          # 关于
│  │  │  └─ index.md     # 内容
│  │  ├─ api-docs/       # API文档
│  │  │  └─ index.md     # 内容
│  │  ├─ backend/        # 后端文档
│  │  │  └─ index.md     # 内容
│  │  ├─ custom-development/  # 自定义开发
│  │  │  └─ index.md     # 内容
│  │  ├─ deployment/     # 部署文档
│  │  │  └─ index.md     # 内容
│  │  ├─ examples/       # 示例
│  │  │  └─ index.md     # 内容
│  │  ├─ frontend/       # 前端文档
│  │  │  └─ index.md     # 内容
│  │  ├─ guidelines/     # 指南
│  │  │  └─ index.md     # 内容
│  │  ├─ miniprogram/    # 小程序文档
│  │  │  └─ index.md     # 内容
│  │  ├─ overview/       # 概览
│  │  │  └─ index.md     # 内容
│  │  ├─ start/          # 快速开始
│  │  │  └─ index.md     # 内容
│  │  ├─ why/            # 为什么选择
│  │  │  └─ index.md     # 内容
│  │  └─ index.md        # 英文首页             # 中文文档
│  ├─ about/          # 关于
│  │  └─ index.md     # 内容
│  ├─ api-docs/       # API文档
│  │  └─ index.md     # 内容
│  ├─ backend/        # 后端文档
│  │  └─ index.md     # 内容
│  ├─ custom-development/  # 自定义开发
│  │  └─ index.md     # 内容
│  ├─ deployment/     # 部署文档
│  │  └─ index.md     # 内容
│  ├─ examples/       # 示例
│  │  └─ index.md     # 内容
│  ├─ frontend/       # 前端文档
│  │  └─ index.md     # 内容
│  ├─ guidelines/     # 指南
│  │  └─ index.md     # 内容
│  ├─ miniprogram/    # 小程序文档
│  │  └─ index.md     # 内容
│  ├─ overview/       # 概览
│  │  └─ index.md     # 内容
│  ├─ start/          # 快速开始
│  │  └─ index.md     # 内容
│  ├─ why/            # 为什么选择
│  │  └─ index.md     # 内容
│  ├─ public/            # 公共资源
│  │  ├─ favicon.png
│  │  ├─ group.jpg
│  │  ├─ help.png
│  │  ├─ logo.png
│  │  └─ wechatPay.jpg
│  └─ index.md           # 根首页
├─ .gitignore            # Git忽略文件
├─ .prettierrc.js        # Prettier配置
├─ LICENSE               # 许可证
├─ README.md             # 项目说明文档
├─ eslint.config.js      # ESLint配置
├─ package.json          # 项目依赖文件
├─ pnpm-lock.yaml        # pnpm锁定文件
├─ tsconfig.json         # TypeScript配置
└─ vite.config.ts        # Vite配置

```

## 🔗 源码仓库

| 平台 | 仓库地址 |
|------|----------|
| GitHub | [FastapiAdmin主工程](https://github.com/fastapiadmin/FastapiAdmin.git) \| [FastDocs官网](https://github.com/fastapiadmin/FastDocs.git) \| [FastApp移动端](https://github.com/fastapiadmin/FastApp.git) |
| Gitee  | [FastapiAdmin主工程](https://gitee.com/fastapiadmin/FastapiAdmin.git) \| [FastDocs官网](https://gitee.com/fastapiadmin/FastDocs.git) \| [FastApp移动端](https://gitee.com/fastapiadmin/FastApp.git) |

## 官网展示

![在线文档](/docs/public/help.png)

## 快速开始

```sh
# 进入项目目录
cd FastDocs
# 安装依赖
pnpm install
# 运行文档工程
pnpm run dev
# 构建文档工程
pnpm run build
```
