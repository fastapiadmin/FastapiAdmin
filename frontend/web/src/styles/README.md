# src/styles/ 目录结构

全局样式按**职责**分目录组织：

```
styles/
├── index.scss              入口（薄）
│
├── core/                   全局基础
│   ├── _fa-tokens.scss     业务色 hex（partial，不单独编译）
│   ├── reset.scss          浏览器重置
│   ├── app.scss            项目级全局 app 样式
│   └── mixin.scss          SCSS mixin（vite additionalData 注入）
│
├── element-plus/           Element Plus 相关
│   ├── _theme.scss         主题色（@use with 注入 EP common/var）
│   ├── _overrides.scss     组件样式覆写（按钮 / 弹窗 / 表格 / 表单 ...）
│   └── _dark.scss          暗黑主题
│
└── animations/             全局动画
    ├── router-transition.scss
    ├── theme-change.scss
    └── theme-animation.scss
```

## 命名约定

- `_xxx.scss` Sass partial（下划线开头，不单独编译）
- `xxx.scss` 入口文件（被 `index.scss` `@use` 引入）

## 添加新样式的流程

1. 找准归属目录
   - 修改 EP 样式 → `element-plus/_overrides.scss`
   - 新增动画 → `animations/`
   - 业务页专属 → **就近放在该组件目录下**（不要放到 styles/）
2. 跑构建（`pnpm build`）确保 SCSS 编译通过
3. 全局变量（颜色、圆角、高度）放到 `core/_fa-tokens.scss` 或 `:root` 块

## 业务页样式就近原则（重要）

业务页 / 业务组件的样式 **不放到 styles/**，而是放到该组件同目录下：

- `src/components/layouts/_fa-layouts.scss` ← layouts/index.vue 用
- `src/components/views/fa-login/_fa-login.scss` ← fa-login 组件用

引用方式用相对路径（`@use "./fa-layouts"` 或 `@use "../fa-login"`），
避免 `@styles/...` 这种"全局别名"误导读代码的人以为它是全局样式。

## 历史

- 原 `element-plus-theme.scss`（位于 `styles/` 根）已迁移到 `element-plus/_theme.scss`
- 原 `core/el-ui.scss` → `element-plus/_overrides.scss`
- 原 `core/dark.scss` → `element-plus/_dark.scss`
- 原 `core/router-transition.scss` / `theme-change.scss` / `theme-animation.scss` → `animations/`
- 原 `core/highlight.scss` / `md.scss` → `vendors/`（已按需化到具体组件）
- 原 `core/variables.scss` 已废弃
- 原 `custom/fa-layouts.scss` → `components/layouts/_fa-layouts.scss`
- 原 `custom/fa-login.scss` → `components/views/fa-login/_fa-login.scss`
- 原 `core/tailwind.css` → 移到 `src/styles/tailwind.css`
