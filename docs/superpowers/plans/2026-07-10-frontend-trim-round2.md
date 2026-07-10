# 前端精简 第二轮(品牌图标 + 顶栏收敛)Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** 换 Codata 图标、收敛顶栏(去搜索/尺寸/全屏/artBot)、去锁屏、隐藏切换租户。

**Architecture:** 以配置开关 + 资源替换 + 摘引用为主,不删组件文件,可逆。

**Tech Stack:** Vue3 `<script setup>` + TS + Element Plus + Vite + pnpm。

## Global Constraints
- 不删任何 .vue / 组件文件(只隐藏 / 摘引用 / 关配置 / 换资源)。
- 品牌统一为 Codata。
- 图标源目录:`/Users/renyc/code/codata/frontend/public/`。
- 通知(notification)、设置(settings)保留在顶栏,不要关。
- 验证:`pnpm ts:check` 必须通过;前端无单测框架。所有 pnpm 命令在 `frontend/web/` 下执行。

---

## Task 1: Codata 图标 + 标题替换

**Files:**
- 覆盖: `frontend/web/src/assets/fa_imgs/logo.svg`(FaLogo 默认源)
- 覆盖: `frontend/web/public/logo.svg`
- 新增: `frontend/web/public/favicon.svg`
- Modify: `frontend/web/index.html`(favicon link)
- Modify: `frontend/web/.env.development`、`.env.production`、`.env.example`(VITE_APP_TITLE)

**Interfaces:** 无跨任务依赖。

- [ ] **Step 1: 拷贝图标资源**

```bash
cd /Users/renyc/code/CodataAdmin
cp /Users/renyc/code/codata/frontend/public/logo.svg frontend/web/src/assets/fa_imgs/logo.svg
cp /Users/renyc/code/codata/frontend/public/logo.svg frontend/web/public/logo.svg
cp /Users/renyc/code/codata/frontend/public/favicon.svg frontend/web/public/favicon.svg
```

- [ ] **Step 2: index.html favicon 指向 svg**

编辑 `frontend/web/index.html`,把:

```html
    <link rel="shortcut icon" type="image/x-icon" href="/favicon.ico" />
```

改为:

```html
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
```

- [ ] **Step 3: 浏览器标题改 Codata**

分别编辑三个 env 文件,把 `VITE_APP_TITLE` 的值 `FastapiAdmin` 改为 `Codata`:
- `frontend/web/.env.development:7` → `VITE_APP_TITLE = Codata`
- `frontend/web/.env.production:7` → `VITE_APP_TITLE = Codata`
- `frontend/web/.env.example:20` → `VITE_APP_TITLE=Codata`

- [ ] **Step 4: 类型检查**

Run: `cd frontend/web && pnpm ts:check`
Expected: PASS(资源替换不影响类型)。

- [ ] **Step 5: Commit**

```bash
cd /Users/renyc/code/CodataAdmin
git add frontend/web/src/assets/fa_imgs/logo.svg frontend/web/public/logo.svg frontend/web/public/favicon.svg frontend/web/index.html frontend/web/.env.development frontend/web/.env.production frontend/web/.env.example
git commit -m "feat(frontend): 品牌图标与标题替换为 Codata(顶栏/登录/favicon/title)"
```

---

## Task 2: 顶栏收敛 + 去锁屏 + 隐藏切换租户

**Files:**
- Modify: `frontend/web/src/config/modules/headerBar.ts`(关 globalSearch/sizeSelect/fullscreen/chat)
- Modify: `frontend/web/src/config/modules/component.ts`(关 screen-lock)
- Modify: `frontend/web/src/components/layouts/fa-header-bar/widgets/FaUserMenu.vue`(删锁屏项 + handler)
- Modify: `frontend/web/src/components/layouts/fa-header-bar/index.vue`(移除 FaTenantSwitcher)

**Interfaces:** 无跨任务依赖。

- [ ] **Step 1: 关闭顶栏四项**

编辑 `frontend/web/src/config/modules/headerBar.ts`,把这四个块的 `enabled` 改为 `false`(其余保持 true,尤其 notification / settings 不动):

```typescript
  fastEnter: {
    enabled: false,
    description: "快速入口功能，提供常用应用和链接的快速访问",
  },
  breadcrumb: {
    enabled: true,
    description: "面包屑导航，显示当前页面路径",
  },
  globalSearch: {
    enabled: false,
    description: "全局搜索功能，支持快捷键 Ctrl+K 或 Cmd+K",
  },
  fullscreen: {
    enabled: false,
    description: "全屏切换功能",
  },
```

以及 chat 与 sizeSelect 两块:

```typescript
  chat: {
    enabled: false,
    description: "聊天功能，提供实时沟通",
  },
```

```typescript
  sizeSelect: {
    enabled: false,
    description: "Element Plus 组件尺寸（默认/大/小）",
  },
```

> 注意:`fastEnter` 第一轮已是 false,保持不变。只需把 globalSearch / fullscreen / chat / sizeSelect 四项由 true 改 false。notification / settings / themeToggle / language / refreshButton / menuButton 保持 true。

- [ ] **Step 2: 关闭锁屏全局组件**

编辑 `frontend/web/src/config/modules/component.ts`,把 `screen-lock` 组件块的 `enabled` 改为 `false`:

```typescript
  {
    name: "锁屏",
    key: "screen-lock",
    component: defineAsyncComponent(() => import("@/components/layouts/fa-screen-lock/index.vue")),
    enabled: false,
  },
```

- [ ] **Step 3: 用户下拉删锁屏项**

编辑 `frontend/web/src/components/layouts/fa-header-bar/widgets/FaUserMenu.vue`,删除锁屏 `<li>`(约 73-79 行):

```html
            <li
              class="flex items-center p-2 mb-3 select-none rounded-md cursor-pointer last:mb-0 hover:bg-(--el-color-primary)/10"
              @click="lockScreen()"
            >
              <FaSvgIcon icon="ri:lock-line" class="mr-2 text-base" />
              <span class="text-sm">{{ $t("topBar.user.lockScreen") }}</span>
            </li>
```

删除 `lockScreen()` handler:

```typescript
function lockScreen(): void {
  mittBus.emit("openLockScreen");
}
```

删后 grep 确认 `mittBus` 在该文件是否还被用；若不再使用,则把 `import { mittBus } from "@utils";` 一行删除(按实际 grep 结果——第一轮已把 WEB_LINKS 移除,mittBus 是否仅锁屏用需确认)。

- [ ] **Step 4: 顶栏移除切换租户**

编辑 `frontend/web/src/components/layouts/fa-header-bar/index.vue`:

删除模板中的租户切换器(约 177-178 行):

```html
        <!-- 租户切换器（全局可见，1步切换） -->
        <FaTenantSwitcher />
```

删除其 import(约 205 行):

```typescript
import FaTenantSwitcher from "./widgets/FaTenantSwitcher.vue";
```

- [ ] **Step 5: 类型检查**

Run: `cd frontend/web && pnpm ts:check`
Expected: PASS。特别确认无 "FaTenantSwitcher declared but never read"、无 lockScreen/mittBus 相关 unused 报错。若报 mittBus unused,按 Step 3 删其 import。

- [ ] **Step 6: Commit**

```bash
cd /Users/renyc/code/CodataAdmin
git add frontend/web/src/config/modules/headerBar.ts frontend/web/src/config/modules/component.ts frontend/web/src/components/layouts/fa-header-bar/widgets/FaUserMenu.vue frontend/web/src/components/layouts/fa-header-bar/index.vue
git commit -m "feat(frontend): 顶栏收敛(去搜索/尺寸/全屏/artBot)+去锁屏+隐藏切换租户"
```

---

## Task 3: 构建验证

**Files:** 无改动。

- [ ] **Step 1: 全量构建**

Run: `cd frontend/web && pnpm build`
Expected: `vue-tsc --noEmit` 通过 + `vite build` 成功产出 dist/,无 error。

- [ ] **Step 2: 目视巡检**

`pnpm dev`,核对:
- Logo(顶栏+登录页)、favicon、浏览器标题为 Codata。
- 顶栏无:搜索框、组件尺寸、全屏、聊天(artBot)、切换租户。
- 顶栏仍有:菜单按钮、刷新、语言、通知、设置、主题切换、用户头像。
- 用户下拉无锁屏项。

- [ ] **Step 3: 无需 commit**

---

## Self-Review
- 图标/标题替换(顶栏+登录+favicon+title) → Task 1 ✅
- 顶栏去 搜索/尺寸/全屏/artBot → Task 2 Step 1 ✅
- 通知/设置保留 → Task 2 Step 1 明确不动 ✅
- 去锁屏(下拉项+handler+全局组件) → Task 2 Step 2/3 ✅
- 隐藏切换租户 → Task 2 Step 4 ✅
- 不删文件 → 全程遵守 ✅
- Placeholder 扫描:无 TBD;每步含确切文件/命令/代码。
- 一致性:headerBar 键名与源文件一致;screen-lock key 与 component.ts 一致。
