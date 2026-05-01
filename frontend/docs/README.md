# FastDocs

FastDocs是FastapiAdmin 官网文档，该项目是一套完全开源的快速开发平台，提供免费使用。它结合了现代、高性能的技术栈，后端采用Fastapi + SQLAlchemy，前端采用基于 vue3 + typescript + vite + pinia + Element-Plus。旨在帮助开发者快速搭建高质量的中后台系统。

## 项目结构

```sh
FastapiAdmin/frontend/
├─ docs                 # 源代码
│  ├─ .vitepress           # VitePress配置
│  │  ├─ cache/          # 缓存目录
│  │  ├─ theme/          # 主题配置
│  │  │  ├─ index.ts     # 主题入口
│  │  │  └─ style.css    # 主题样式
│  │  └─ config.ts       # 主配置文件
│  ├─ src/               # 文档源文件
│  │  ├─ guide/          # 指南（所有文档）
│  │  │  ├─ overview.md          # 项目概述
│  │  │  ├─ start.md             # 快速开始
│  │  │  ├─ why.md               # 为什么选择FastapiAdmin
│  │  │  ├─ frontend.md          # 前端开发
│  │  │  ├─ backend.md           # 后端开发
│  │  │  ├─ miniprogram.md       # 移动端开发
│  │  │  ├─ guidelines.md        # 开发规范
│  │  │  ├─ examples.md          # 示例
│  │  │  ├─ custom-development.md # 自定义开发
│  │  │  ├─ deployment.md        # 部署指南
│  │  │  └─ api-docs.md          # API文档说明
│  │  ├─ about/          # 关于
│  │  │  ├─ about.md             # 关于我们
│  │  │  ├─ users.md             # 他们在使用
│  │  │  ├─ users-all.md         # 所有用户
│  │  │  ├─ sponsor.md           # 赞助
│  │  │  └─ contributing.md      # 贡献指南
│  │  ├─ en/             # 英文文档（结构同中文）
│  │  │  ├─ guide/
│  │  │  ├─ about/
│  │  │  └─ index.md     # 英文首页
│  │  ├─ public/         # 公共资源
│  │  │  ├─ favicon.png
│  │  │  ├─ group.jpg
│  │  │  ├─ help.png
│  │  │  ├─ logo.png
│  │  │  └─ wechatPay.jpg
│  │  └─ index.md        # 根首页
├─ .gitignore            # Git忽略文件
├─ LICENSE               # 许可证
├─ README.md             # 项目说明文档
├─ package.json          # 项目依赖文件
├─ pnpm-lock.yaml        # pnpm锁定文件
└─ tsconfig.json         # TypeScript配置

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
cd FastapiAdmin/frontend/docs
# 安装依赖
pnpm install
# 运行文档工程
pnpm run dev
# 构建文档工程
pnpm run build
```
