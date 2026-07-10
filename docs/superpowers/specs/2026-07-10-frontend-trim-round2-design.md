# 前端精简 第二轮(品牌图标 + 顶栏收敛)设计

日期：2026-07-10
分支：`feat/single-tenant-slim`(接第一轮 commit 7f739752 之后)
关联：`2026-07-10-frontend-trim-design.md`

## 目标

在第一轮基础上继续收敛顶栏、替换品牌图标为 Codata,并隐藏单租户下无意义的切换租户入口。

## 用户确认的四项

1. **换 Codata 图标**：图标源 = `/Users/renyc/code/codata/frontend/public/`(logo.svg 29KB=内嵌 128×128 PNG、favicon.svg 2.9KB=内嵌 32×32 PNG、logo-512.png)。**全部替换**:顶栏 Logo + 登录页 Logo + favicon + 浏览器标题。
2. **顶栏收敛**:去掉 搜索、组件尺寸(sizeSelect)、全屏、artBot 聊天(chat)四个入口；**通知和设置保留在顶栏**(二者面板本就从右侧弹出,符合"统一放右侧"诉求)。
3. **去掉锁定屏幕**操作。
4. **隐藏切换租户**(默认单租户)。

## 变更清单(按文件)

### 1. Codata 图标替换
- 拷贝 `codata/frontend/public/logo.svg` → 覆盖 `frontend/web/src/assets/fa_imgs/logo.svg`(FaLogo 默认源,顶栏+登录页共用)与 `frontend/web/public/logo.svg`。
- 拷贝 `codata/frontend/public/favicon.svg` → `frontend/web/public/favicon.svg`;`index.html` 的 `<link rel="shortcut icon">` 改指向 `/favicon.svg`(type=`image/svg+xml`)。保留旧 `favicon.ico` 不删(向后兼容,不引用即可)。
- 浏览器标题:`.env.development` / `.env.production` / `.env.example` 的 `VITE_APP_TITLE` `FastapiAdmin` → `Codata`。

### 2. 顶栏收敛(`config/modules/headerBar.ts`)
用配置开关关闭四项(优先改配置而非删模板,可逆、集中):
- `globalSearch.enabled` → `false`
- `sizeSelect.enabled` → `false`
- `fullscreen.enabled` → `false`
- `chat.enabled` → `false`(artBot)
保留 `notification` / `settings` / `themeToggle` / `language` / `refreshButton` / `menuButton` 不变。
> `useHeaderBar` 的 `shouldShowGlobalSearch/Fullscreen/SizeSelect` 均为 `isFeatureEnabled(x) && showXxx`,`shouldShowChat = isFeatureEnabled("chat")`——配置置 false 即全部隐藏,顶栏模板无需改。

### 3. 去掉锁屏
- `FaUserMenu.vue`:删除锁屏 `<li>`(`@click="lockScreen()"` 那条)及 `lockScreen()` handler；若删后 `mittBus` 在该文件不再被引用则收窄其 import。
- `config/modules/component.ts`:全局组件 `screen-lock` 的 `enabled` → `false`(不再挂载锁屏组件,无触发源即无入口)。文件保留不删。

### 4. 隐藏切换租户(`fa-header-bar/index.vue`)
- 移除模板中 `<FaTenantSwitcher />` 使用及其 `import FaTenantSwitcher from "./widgets/FaTenantSwitcher.vue"`。组件文件 `FaTenantSwitcher.vue` 保留不删(它本就 `v-if="tenantList.length > 1"` 自隐,但显式移除更彻底,契合单租户定位)。

## 不做
- 不删任何 .vue / 组件文件(只隐藏/摘引用/关配置)。
- 不动左侧栏菜单。
- 不动第一轮已完成项。

## 验证
- `pnpm ts:check` 通过(尤其确认移除 FaTenantSwitcher import / lockScreen handler 后无 unused import / declared-but-never-read)。
- `pnpm build` 成功。
- `pnpm dev` 目视:顶栏只剩 菜单/刷新/语言/通知/设置/主题/用户头像;无搜索框、无尺寸、无全屏、无聊天、无租户切换;用户下拉无锁屏;Logo/favicon/标题为 Codata。

## 回滚
全部为配置/资源替换/摘引用,`git revert` 即恢复;组件文件与后端未动。
