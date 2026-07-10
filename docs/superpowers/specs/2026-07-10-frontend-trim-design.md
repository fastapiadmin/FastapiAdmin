# 前端精简（单公司内部控制面）设计

日期：2026-07-10
分支基线：`feat/single-tenant-slim`
关联：`2026-07-09-single-tenant-slim-design.md`（后端第一阶段：禁用商业化 + 单租户化）

## 目标

后端第一阶段已禁用商业化 API 并单租户化。本轮把**前端**收敛为「单公司多部门内部控制面」的形态：移除 SaaS / 营销 / 演示类入口，去掉自助注册与第三方登录，完成 FastapiAdmin → Codata 品牌替换。

## 约束与既定决策（用户确认）

1. **只隐藏、不删文件**：所有 `.vue` 视图文件保留。改动集中在配置项与模板 gating，全部可逆。
2. **登录仅保留账号密码 + 忘记密码**：移除注册、第三方 OAuth、手机号/扫码演示、演示快捷账号下拉。**保留**忘记密码流程。
3. **品牌改为 Codata**。
4. **fastlink 路由保持挂载**（仅 URL 可达，不在任何 UI 出现）。`/fastlink/profile` 被用户菜单「个人中心」使用，必须保留。

## 关键背景（探明的现状）

- 菜单模式 = `mixed`（`VITE_ACCESS_MODE=mixed`）：左侧栏由**后端菜单表(DB)** + 静态 home/dashboard 壳层合并而成。`builtinFrontendRoutes` 为空数组。
  → **左侧栏内容不由前端文件控制**，本轮不动侧栏；侧栏精简属后端菜单表工作，另行处理。
- 前端可控的「冗余入口」集中在四处：顶栏快速入口(fastEnter)、登录页、用户下拉、品牌/外链常量。
- `module_platform/{order,invoice,package,tenant,self_service}` 等视图对应的后端 API 已禁用；文件按决策(1)保留，但需摘除仍指向被禁用功能的**静态路由挂载**。

## 变更清单（按文件）

### 1. 顶栏快速入口 — 一键关闭
- `src/config/modules/headerBar.ts`：`fastEnter.enabled` → `false`。
  - 关闭整个快速入口面板（当前 8 个应用 + 6 个 quicklink 全是营销/演示：定价、文章、聊天、更新日志、注册、留言等）。
  - `fastEnter.ts` 配置文件本身保留不动（决策 1）；仅通过 headerBar 开关隐藏。

### 2. 登录页 — 账号密码 + 忘记密码
gating 方式：模板块加 `v-if="false"` 或直接移除模板块（保留组件 import 与 handler 定义，不删组件文件）。

`src/components/views/fa-login/forms/FaLoginAccountForm.vue`：
- 隐藏顶部**演示快捷账号下拉**（`ElSelect` + `accounts`）——避免在 UI 暴露 super/admin/test 种子账号。
- 隐藏 `login-secondary-actions`（手机号登录 / 扫码登录两个按钮）。
- 隐藏 `<FaLoginThirdPartySection>`（第三方 OAuth）。
- 隐藏 `<FaLoginAuthLinkRow>`（去注册链接行）。
- **保留** `@forget`（忘记密码链接）。

`src/views/module_system/auth/login/index.vue`：
- 隐藏 `authPanel === 'register'` 分支（`<FaLoginRegisterPanel>`）。
- 隐藏 `loginFlowMode === 'mobile'` / `'qr'` 分支（`<FaLoginMobilePanel>` / `<FaLoginQrPanel>`）。
- **保留** `authPanel === 'forget'` 分支（`<FaLoginForgetPanel>`）。
- OAuth 回调消费逻辑（`tryConsumeOAuthCallback`）保留不动——无入口即不会触发，删之增加风险。

### 3. 用户下拉 + 品牌
- `src/components/layouts/fa-header-bar/widgets/FaUserMenu.vue`：移除 **GitHub**、**Gitee** 两个 `<li>`（上游 FastapiAdmin 仓库链接）及其 `toGithub`/`toGitee` handler。保留 个人中心 / 参数配置 / 锁屏 / 退出。
- `src/config/index.ts`：`systemInfo.name` `"FastapiAdmin"` → `"Codata"`。
- `src/utils/constants/definitions.ts` `WEB_LINKS`：把 fastapiadmin.com / gitee / github / csdn / bilibili 等上游外链**统一改为空串 `""`**（保留键，值清空），消除悬挂外链。选空串而非占位域名：官方 Codata 域名尚未确定（与另一仓库「仅剩官方域名占位」状态一致），空串使任何残余 `window.open` 为无害空跳。因引用这些常量的 fastEnter / 用户菜单条目已隐藏，改值无 UI 副作用。

### 4. 静态路由 — 摘除指向已禁用功能的挂载
`src/router/staticRoutes.ts`：
- 移除 `payment/:orderId`（order 模块子页，后端订单 API 已禁用）。
- 移除 `workspace`（复用 self_service 页面，后端自助服务 API 已禁用）。
- **保留** 整个 `fastlink` 父级及其子路由（决策 4，URL-only）；`/fastlink/profile` 必留。
- 其余静态路由（redirect/login/401/403/404/500/dashboard/home/outside/catch-all）不动。

## 不做（明确排除）

- 不删任何 `.vue` 文件。
- 不改左侧栏菜单（DB 菜单表驱动，超出前端文件范围）。
- 不删 OAuth / 注册 / 订单等后端逻辑与前端组件文件——仅摘入口。
- 不做 i18n 文案清理（隐藏后文案不再出现，低价值）。

## 验证

- `pnpm build`（或 `pnpm tsc`）通过：确保移除模板块/handler 后无未用变量报错、无类型错误。
- `pnpm dev` 起 http://localhost:5180/web：
  - 登录页只剩账号密码 + 记住我 + 忘记密码；无注册/第三方/手机/扫码/演示账号下拉。
  - 顶栏无快速入口图标。
  - 用户下拉无 GitHub/Gitee。
  - 页面标题/系统名显示 Codata。
- 手动访问 `/payment/x`、`/workspace` → 落到 404（挂载已摘）。
- `/fastlink/profile` 仍可从用户菜单「个人中心」打开。

## 回滚

全部为配置/模板 gating，`git revert` 单个提交即可恢复;组件文件与后端逻辑未动。
