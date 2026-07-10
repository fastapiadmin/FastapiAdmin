# 前端精简（单公司内部控制面）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把前端收敛为单公司内部控制面：隐藏 SaaS/营销/演示入口、登录仅留账号密码+忘记密码、品牌改 Codata——只隐藏不删文件。

**Architecture:** 改动集中在 4 处前端可控面（顶栏 fastEnter、登录页、用户下拉、品牌/外链常量）+ 静态路由摘挂载。隐藏用命名 `const` feature-flag 常量 gating（`v-if` 绑常量），保留组件 import / handler / emit 引用不动，确保 `vue-tsc` 类型检查通过且可一键 revert。

**Tech Stack:** Vue 3 `<script setup>` + TypeScript + Element Plus + Vite + pnpm。

## Global Constraints

- 只隐藏、不删任何 `.vue` 文件。
- 登录保留：用户名+密码+记住我+**忘记密码**；隐藏：注册 / 第三方 OAuth / 手机号 / 扫码 / 演示快捷账号下拉。
- 品牌：`FastapiAdmin` → `Codata`。
- `WEB_LINKS` 上游外链统一改为空串 `""`（保留键）。
- fastlink 路由保持挂载（URL-only）；`/fastlink/profile` 必留。
- 不动左侧栏菜单（DB 菜单表驱动，非前端文件范围）。
- 验证工具：`pnpm ts:check`（= `vue-tsc --noEmit --skipLibCheck`）必须通过；前端无单测框架，功能验证靠 `pnpm dev` 目视。
- 工作目录：所有 `pnpm` 命令在 `frontend/web/` 下执行。

---

## Task 1: 顶栏快速入口关闭 + 品牌 + 外链 + 用户下拉

**Files:**
- Modify: `frontend/web/src/config/modules/headerBar.ts`（`fastEnter.enabled`）
- Modify: `frontend/web/src/config/index.ts:41`（`systemInfo.name`）
- Modify: `frontend/web/src/utils/constants/definitions.ts:6-17`（`WEB_LINKS`）
- Modify: `frontend/web/src/components/layouts/fa-header-bar/widgets/FaUserMenu.vue`（去 GitHub/Gitee）

**Interfaces:**
- Consumes: 无（起始任务）
- Produces: `WEB_LINKS` 键集合不变（仅值清空），下游引用 `WEB_LINKS.GITHUB` 等编译仍有效。

- [ ] **Step 1: 关闭顶栏快速入口**

编辑 `frontend/web/src/config/modules/headerBar.ts`，把 `fastEnter` 块的 `enabled` 从 `true` 改为 `false`：

```typescript
  fastEnter: {
    enabled: false,
    description: "快速入口功能，提供常用应用和链接的快速访问",
  },
```

- [ ] **Step 2: 系统名改 Codata**

编辑 `frontend/web/src/config/index.ts:41`：

```typescript
  systemInfo: {
    name: "Codata", // 系统名称
  },
```

- [ ] **Step 3: 清空上游外链**

编辑 `frontend/web/src/utils/constants/definitions.ts`,把 `WEB_LINKS` 各上游外链值改为空串（保留键名，供下游编译引用）：

```typescript
export const WEB_LINKS = {
  GITHUB_HOME: "",
  GITHUB: "",
  GITEE: "",
  BLOG: "",
  DOCS: "",
  LiteVersion: "",
  OldVersion: "",
  COMMUNITY: "",
  BILIBILI: "",
  INTRODUCE: "",
};
```

- [ ] **Step 4: 用户下拉去掉 GitHub / Gitee 条目**

编辑 `frontend/web/src/components/layouts/fa-header-bar/widgets/FaUserMenu.vue`，删除模板中 GitHub 与 Gitee 两个 `<li>`（原 76-86 行区块）：

```html
            <li
              class="flex items-center p-2 mb-3 select-none rounded-md cursor-pointer last:mb-0 hover:bg-(--el-color-primary)/10"
              @click="toGithub()"
            >
              <FaSvgIcon icon="ri:github-line" class="mr-2 text-base" />
              <span class="text-sm">{{ $t("topBar.user.github") }}</span>
            </li>
            <li
              class="flex items-center p-2 mb-3 select-none rounded-md cursor-pointer last:mb-0 hover:bg-(--el-color-primary)/10"
              @click="toGitee"
            >
              <FaSvgIcon icon="ri:git-branch-line" class="mr-2 text-base" />
              <span class="text-sm">{{ $t("topBar.user.gitee") }}</span>
            </li>
```

同时删除 `<script setup>` 中不再使用的两个 handler（原 150-156 行）：

```typescript
function toGithub(): void {
  window.open(WEB_LINKS.GITHUB);
}

function toGitee(): void {
  window.open(WEB_LINKS.GITEE);
}
```

删除后检查 `WEB_LINKS` 若在该文件不再被引用，则一并删除其 import（第 115 行 `import { WEB_LINKS, mittBus } from "@utils";` → 改为 `import { mittBus } from "@utils";`）。`mittBus` 仍被 `lockScreen` 使用，必须保留。

- [ ] **Step 5: 类型检查**

Run: `cd frontend/web && pnpm ts:check`
Expected: PASS（无 error；尤其确认无 “toGithub/toGitee is declared but never read” 或 “WEB_LINKS unused import”）

- [ ] **Step 6: 目视验证**

Run: `cd frontend/web && pnpm dev`（若未在跑）
打开 http://localhost:5180/web 登录后确认：顶栏无快速入口图标；右上角用户下拉无 GitHub/Gitee，仅剩 个人中心/参数配置/锁屏/退出；浏览器标签/系统名显示 Codata。

- [ ] **Step 7: Commit**

```bash
cd /Users/renyc/code/CodataAdmin
git add frontend/web/src/config/modules/headerBar.ts frontend/web/src/config/index.ts frontend/web/src/utils/constants/definitions.ts frontend/web/src/components/layouts/fa-header-bar/widgets/FaUserMenu.vue
git commit -m "feat(frontend): 关闭顶栏快速入口 + Codata品牌 + 清空上游外链 + 用户下拉去GitHub/Gitee"
```

---

## Task 2: 登录页收敛为账号密码 + 忘记密码

**Files:**
- Modify: `frontend/web/src/components/views/fa-login/forms/FaLoginAccountForm.vue`（隐藏演示账号下拉 / 手机扫码按钮 / 第三方 / 去注册行）
- Modify: `frontend/web/src/views/module_system/auth/login/index.vue`（隐藏 register / mobile / qr 分支）

**Interfaces:**
- Consumes: 无跨任务依赖。
- Produces: 无（终端 UI 改动）。

**gating 约定:** 在各自 `<script setup>` 顶部加 `const SHOW_SAAS_AUTH = false;`,模板块用 `v-if="SHOW_SAAS_AUTH"` 包裹。这样 handler / emit / 组件 import 仍被模板引用,`vue-tsc` 不报未用；开关翻 `true` 即完全恢复。

- [ ] **Step 1: 账号表单加 feature flag**

编辑 `frontend/web/src/components/views/fa-login/forms/FaLoginAccountForm.vue`,在 `<script setup>` 内(defineProps/defineEmits 之后合适位置)新增常量：

```typescript
/** 内部控制面：隐藏注册/第三方/手机扫码/演示账号等 SaaS 登录入口，仅留账号密码 */
const SHOW_SAAS_AUTH = false;
```

- [ ] **Step 2: 隐藏演示快捷账号下拉**

同文件模板,给顶部演示账号 `ElFormItem`(含 `ElSelect` + `accounts`,原 13-29 行)最外层 `ElFormItem` 加 `v-if="SHOW_SAAS_AUTH"`：

```html
      <ElFormItem v-if="SHOW_SAAS_AUTH">
        <ElSelect
          :model-value="demoAccountKey"
          class="w-full"
          :placeholder="$t('login.quickSelectAccount')"
          @update:model-value="$emit('setupAccount', $event as AccountKey)"
        >
          <ElOption
            v-for="account in accounts"
            :key="account.key"
            :label="account.label"
            :value="account.key"
          >
            <span>{{ account.label }}</span>
          </ElOption>
        </ElSelect>
      </ElFormItem>
```

- [ ] **Step 3: 隐藏手机/扫码按钮、第三方、去注册行**

同文件模板,给三处加 `v-if="SHOW_SAAS_AUTH"`：

手机/扫码按钮容器(原 149-156 行 `login-secondary-actions`)：

```html
        <div v-if="SHOW_SAAS_AUTH" class="login-secondary-actions grid grid-cols-2 gap-2">
          <ElButton class="login-secondary-btn" plain @click="$emit('openMobile')">
            {{ $t("login.mobileLogin") }}
          </ElButton>
          <ElButton class="login-secondary-btn" plain @click="$emit('openQr')">
            {{ $t("login.qrLogin") }}
          </ElButton>
        </div>
```

第三方区块(原 160 行)：

```html
    <FaLoginThirdPartySection v-if="SHOW_SAAS_AUTH" @oauth="$emit('oauth', $event)" />
```

去注册行(原 162-166 行)：

```html
    <FaLoginAuthLinkRow
      v-if="SHOW_SAAS_AUTH"
      :hint="$t('login.noAccount')"
      :link-text="$t('login.register')"
      @link="$emit('register')"
    />
```

- [ ] **Step 4: 登录页 index 加 feature flag**

编辑 `frontend/web/src/views/module_system/auth/login/index.vue`,在 `<script setup>` 内新增常量：

```typescript
/** 内部控制面：隐藏注册/手机/扫码面板,仅留账号密码 + 忘记密码 */
const SHOW_SAAS_AUTH = false;
```

- [ ] **Step 5: 隐藏 mobile / qr / register 分支**

同文件模板：给 `<FaLoginMobilePanel>`(原 72-76 行)与 `<FaLoginQrPanel>`(原 78-82 行)各自的 `v-else-if` 追加 flag 守卫；register 分支同理。

mobile：

```html
                      <FaLoginMobilePanel
                        v-else-if="SHOW_SAAS_AUTH && loginFlowMode === 'mobile'"
                        @back="backToAccountLogin"
                        @register="setAuthPanel('register')"
                      />
```

qr：

```html
                      <FaLoginQrPanel
                        v-else-if="SHOW_SAAS_AUTH && loginFlowMode === 'qr'"
                        @back="backToAccountLogin"
                        @register="setAuthPanel('register')"
                      />
```

register 面板(原 85-97 行)：

```html
                    <FaLoginRegisterPanel
                      v-else-if="SHOW_SAAS_AUTH && authPanel === 'register'"
                      ref="registerPanelRef"
                      v-model:register-agreement-read="registerAgreementRead"
                      v-model:register-form="registerForm"
                      :register-rules="registerRules"
                      :form-key="formKey"
                      :register-loading="registerLoading"
                      :show-email="true"
                      :user-agreement-href="userAgreementHref"
                      @submit="submitRegister"
                      @to-login="setAuthPanel('login')"
                    />
```

保留 `<FaLoginForgetPanel>`(忘记密码,原 99-108 行)不动——它是最终 `v-else` 分支,当 `authPanel==='forget'` 时命中,不受 flag 影响。

- [ ] **Step 6: 类型检查**

Run: `cd frontend/web && pnpm ts:check`
Expected: PASS。若报某 handler/组件 “declared but never read”,说明该引用只存在于被 `v-if` 关闭的块之外——回查该 handler 是否仍在模板中出现(应仍出现,因 flag 是运行时值,模板静态引用保留);确保未误删任何 `@event` 绑定。

- [ ] **Step 7: 目视验证**

http://localhost:5180/web/login 确认：只有 用户名+密码+验证码/滑块+记住我+登录按钮+忘记密码链接；无演示账号下拉、无手机/扫码按钮、无第三方图标、无“去注册”。点击“忘记密码”仍能进入重置面板并返回。

- [ ] **Step 8: Commit**

```bash
cd /Users/renyc/code/CodataAdmin
git add frontend/web/src/components/views/fa-login/forms/FaLoginAccountForm.vue frontend/web/src/views/module_system/auth/login/index.vue
git commit -m "feat(frontend): 登录页收敛为账号密码+忘记密码,隐藏注册/OAuth/手机/扫码/演示账号"
```

---

## Task 3: 摘除指向已禁用功能的静态路由

**Files:**
- Modify: `frontend/web/src/router/staticRoutes.ts`（移除 `payment/:orderId` 与 `workspace` 两个子路由）

**Interfaces:**
- Consumes: 无。
- Produces: 无。

- [ ] **Step 1: 移除 payment 路由**

编辑 `frontend/web/src/router/staticRoutes.ts`,删除 RootLayout `children` 内的 `payment/:orderId` 路由块(原 452-462 行)：

```typescript
      /** 支付页面（订单模块子组件） */
      {
        path: "payment/:orderId",
        name: "Payment",
        component: () => import("@views/module_platform/order/components/PaymentPage.vue"),
        meta: {
          title: "订单支付",
          hidden: true,
          keepAlive: false,
        },
      },
```

- [ ] **Step 2: 移除 workspace 路由**

同文件,删除 `workspace` 路由块(原 463-473 行)：

```typescript
      /** 租户工作台概览 — 复用自助服务页面 */
      {
        path: "workspace",
        name: "TenantWorkspace",
        component: () => import("@views/module_platform/self_service/index.vue"),
        meta: {
          title: "工作台",
          hidden: true,
          keepAlive: false,
        },
      },
```

保留同区块内的 `fastlink` 父级及其全部子路由不动(决策：URL-only)。

- [ ] **Step 3: 类型检查**

Run: `cd frontend/web && pnpm ts:check`
Expected: PASS（确认无对 `Payment` / `TenantWorkspace` 路由 name 的悬挂引用——如有,grep 定位并处理）。

补充确认:

Run: `cd frontend/web && grep -rn '"Payment"\|TenantWorkspace\|payment/' src/ | grep -v staticRoutes.ts`
Expected: 无输出（或仅注释/无关命中）。

- [ ] **Step 4: 目视验证**

浏览器访问 `http://localhost:5180/web/payment/1` 与 `http://localhost:5180/web/workspace` → 均落到 404 页。访问 `http://localhost:5180/web/fastlink/profile` → 从用户菜单“个人中心”仍可正常打开。

- [ ] **Step 5: Commit**

```bash
cd /Users/renyc/code/CodataAdmin
git add frontend/web/src/router/staticRoutes.ts
git commit -m "feat(frontend): 摘除指向已禁用功能的静态路由(payment/workspace)"
```

---

## Task 4: 整体构建验证

**Files:**
- 无改动（纯验证任务）

**Interfaces:**
- Consumes: Task 1-3 的全部改动。
- Produces: 无。

- [ ] **Step 1: 全量构建**

Run: `cd frontend/web && pnpm build`
Expected: `vue-tsc --noEmit` 通过 + `vite build` 成功产出 `dist/`,无 error。（若因环境依赖/内存导致 build 失败但 `pnpm ts:check` 通过,记录失败原因交用户,不算本计划回归。）

- [ ] **Step 2: 最终目视巡检**

`pnpm dev`,逐项核对：
- 登录页：仅账号密码 + 忘记密码。
- 顶栏：无快速入口。
- 用户下拉：无 GitHub/Gitee。
- 系统名：Codata。
- `/payment/x`、`/workspace` → 404。

- [ ] **Step 3: 无需 commit**（无文件改动）

---

## Self-Review

**Spec 覆盖核对：**
- fastEnter 关闭 → Task 1 Step 1 ✅
- 登录 gating(注册/OAuth/手机/扫码/演示账号,留忘记密码) → Task 2 ✅
- 用户下拉去 GitHub/Gitee → Task 1 Step 4 ✅
- 品牌 Codata → Task 1 Step 2 ✅
- WEB_LINKS 清空 → Task 1 Step 3 ✅
- 静态路由 payment/workspace 摘除、fastlink 保留 → Task 3 ✅
- 不删文件 / 不动侧栏 → Global Constraints,各 Task 均遵守 ✅

**Placeholder 扫描：** 无 TBD/TODO；每步含具体文件路径、可运行命令、完整代码块或明确删除目标。

**类型/命名一致性：** feature-flag 常量统一命名 `SHOW_SAAS_AUTH`(两文件各自局部声明,非跨文件 import,命名一致即可读);`WEB_LINKS` 键集合保持不变,下游引用不断。
