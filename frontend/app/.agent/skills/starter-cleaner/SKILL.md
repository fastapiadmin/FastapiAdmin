---
name: starter-cleaner
description: 清理 wot-starter 模板，移除示例页面、文档和 monorepo 配置，创建一个最简基础模板。
---

# Starter Cleaner Skill

该技能用于将 `wot-starter` 模板精简至最小状态，适合用于启动不包含示例代码的新项目。

## 功能说明

1.  **目录清理**:
    *   移除 `docs/`: 文档目录。
    *   移除 `src/subPages/`: 示例分包页面。
    *   移除 `src/subEcharts/`: Echarts 示例。
    *   移除 `src/subAsyncEcharts/`: 异步 Echarts 示例。
    *   移除 `src/pages.json`: 项目页面配置文件（由 `pages.config.ts` 生成）。
    *   移除 `pnpm-workspace.yaml`: Monorepo 配置文件。

2.  **配置清理**:
    *   **vite.config.ts**:
        *   移除 `UniHelperPages` 相关分包配置 (`subEcharts`, `subAsyncEcharts` 等)。
        *   **注意**：保留 `uni-echarts` 相关配置。
    *   **package.json**:
        *   移除 `docs:` 相关脚本 (`docs:dev`, `docs:build`, `docs:preview`)。
        *   **注意**：保留 `uni-echarts` 和 `echarts` 依赖。

## 使用方法

要执行清理过程，请使用 `run_command` 工具运行提供的 node 脚本。

```zsh
node .agent/skills/starter-cleaner/scripts/clean.js
```

> [!WARNING]
> 该技能执行**破坏性**操作。它将永久删除文件和目录。运行前请确保相关工作已提交。
