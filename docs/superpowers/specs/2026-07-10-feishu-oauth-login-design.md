# 飞书授权登录 — 设计文档

日期:2026-07-10
状态:已确认,待实现

## 背景

CodataAdmin(FastAPI + Vue3)已内置一套完整的第三方 OAuth 登录框架,支持 `wechat`/`qq`/`github`/`gitee` 四个 provider,前后端均已就绪。本功能新增飞书(`feishu`)作为一个新 provider 接入这套框架。

## 需求(已确认)

- **场景**:网页扫码/授权登录,标准 OAuth2 授权码流程(与现有微信/GitHub 一致),面向浏览器访问后台的用户。
- **账号关联**:首次飞书登录自动注册新系统用户,复用现有 username 编码策略(`oauth_feishu_{union_id}`),**无需修改数据库表**。
- **凭证**:暂无 app_id/app_secret,代码写完整且可配置,凭证留空由用户后续填入 env 即可用。
- **应用类型**:飞书企业自建应用(国内版),API 域名 `open.feishu.cn`(做成配置项,方便切换 Lark 国际版)。
- **前端展示**:目前第三方登录区被 `SHOW_SAAS_AUTH=false` 隐藏。为飞书做一个**独立入口,只露出飞书登录按钮**,不受该开关控制,其他第三方仍隐藏。

## OAuth2 授权码流程(时序)

```
用户点击"飞书登录"
  → 前端整页跳转到  GET /api/v1/system/auth/oauth/feishu/login
  → 后端生成 state 存 Redis(600s),302 跳转到飞书授权页
      https://open.feishu.cn/open-apis/authen/v1/authorize?app_id=...&redirect_uri=...&state=...
  → 用户在飞书扫码/确认授权
  → 飞书回调  GET /api/v1/system/auth/oauth/feishu/callback?code=...&state=...
  → 后端:
      1. 校验 state(Redis 取出并删除,防 CSRF / 过期)
      2. 用 app_id + app_secret 取 app_access_token
      3. 用 code + app_access_token 换 user_access_token
      4. 调 /authen/v1/user_info 取 union_id / open_id / name / avatar
      5. ensure_oauth_user(自动注册 oauth_feishu_{union_id},分配默认角色)
      6. LoginService.create_token 签发 access/refresh,写 Redis session
      7. 302 重定向回  {前端}/login?access_token=...&refresh_token=...&token_type=Bearer
  → 前端 login 页 onMounted 消费 token,写入 store,跳转首页
```

**关键差异点**:飞书是**两步换 token**(先 `app_access_token` 再 `user_access_token`),而现有 GitHub/微信是单步。这是本次唯一的结构性新增。

### 飞书 API 端点(国内版)

| 步骤 | 方法 | 端点 |
|------|------|------|
| 取 app_access_token | POST | `/open-apis/auth/v3/app_access_token/internal`(body: `app_id`, `app_secret`) |
| 授权页 | GET | `/open-apis/authen/v1/authorize`(query: `app_id`, `redirect_uri`, `state`) |
| code 换 user_access_token | POST | `/open-apis/authen/v1/oidc/access_token`(header: `Authorization: Bearer {app_access_token}`,body: `grant_type=authorization_code`, `code`) |
| 取用户信息 | GET | `/open-apis/authen/v1/user_info`(header: `Authorization: Bearer {user_access_token}`) |

## 改动清单

### 后端(核心工作量)

1. **`app/config/setting.py`** — 新增配置项:
   ```python
   OAUTH_FEISHU_APP_ID: str = ""
   OAUTH_FEISHU_APP_SECRET: str = ""
   OAUTH_FEISHU_API_BASE: str = "https://open.feishu.cn"  # 域名可配,方便切 Lark 国际版
   ```
   在 `env/.env.dev` 等 env 文件补空值占位。

2. **`app/api/v1/module_system/auth/oauth_service.py`**:
   - `OAuthProvider` 联合类型加 `"feishu"`
   - `_require_credentials` 加 feishu 分支(读上面 3 个配置,缺失则抛明确错误)
   - `build_authorize_url` 加飞书分支 → `{API_BASE}/open-apis/authen/v1/authorize`
   - 新增 `_fetch_feishu_app_access_token()` — POST `/open-apis/auth/v3/app_access_token/internal`,拿 `app_access_token`
   - 新增 `exchange_feishu_token(code)` — POST `/open-apis/authen/v1/oidc/access_token`(先取 app_access_token 作 header),拿 `user_access_token`
   - 新增 `fetch_feishu_profile(user_access_token)` — GET `/open-apis/authen/v1/user_info`,拿 `union_id`/`open_id`/`name`/`avatar_url`
   - `complete_oauth_login` 的 if/elif 链加 feishu 分支,`unique_id` 用 `union_id`(跨应用稳定)

3. **`app/api/v1/module_system/auth/controller.py`** — 两处 provider 白名单集合(`login` 和 `callback`,约 :216、:275)加 `"feishu"`,更新参数描述。

### 前端(极小)

4. **`src/api/module_system/auth.ts`** — `OAuthProvider` 类型加 `"feishu"`。
5. **`src/components/views/fa-login/widgets/FaLoginThirdPartySection.vue`** — `oauthItems` 加飞书项(iconify 图标如 `simple-icons:feishu` + tooltip),同步该文件内联的 provider 联合类型。
6. **i18n** — `src/locales/langs/`(中英)加飞书 tooltip 文案。
7. **独立飞书入口** — 在登录页做一个**不受 `SHOW_SAAS_AUTH` 控制**的飞书登录入口,只露出飞书按钮;其他第三方仍由 `SHOW_SAAS_AUTH` 控制(保持隐藏)。复用现有 `startOAuthLogin('feishu')`。

## 错误处理

- **state 校验失败**(CSRF/过期):回调重定向到 `{前端}/login?oauth_error=<urlencoded msg>`,前端已有逻辑弹出错误提示。
- **飞书 API 调用失败**(换 token/取 profile 报错、飞书返回非 0 错误码):捕获后同样走 `oauth_error` 重定向,不抛 500。
- **凭证未配置**:`_require_credentials` 抛明确错误("飞书登录未配置")。
- 复用现有 `oauth_service_error_redirect` helper,行为与现有 OAuth 一致。

## 复用的现有基础设施(无需新建)

- **token 签发**:`LoginService.create_token`
- **state 存储**:`save_oauth_state`(Redis,`oauth_state:` 前缀,TTL 600s)
- **用户自动注册**:`ensure_oauth_user` + `_username_for_oauth`
- **HTTP 调用**:`_http_json` / `_http_text`(封装好的 httpx helper)
- **前端回调消费**:登录页 `tryConsumeOAuthCallback`(onMounted 自动解析 URL query 中的 token),`/login` 已在免登录白名单
- **前端跳转封装**:`startOAuthLogin(provider)`(整页跳转到后端 OAuth 入口)

## 测试策略

- **后端单测**:mock httpx(respx 或等价手段),覆盖:
  - `_fetch_feishu_app_access_token` 成功 / 飞书返回错误码
  - `exchange_feishu_token` 成功 / 失败
  - `fetch_feishu_profile` 成功 / 失败
- **后端集成测**:`complete_oauth_login` 的 feishu 分支——mock 外部调用,验证 state 校验、用户自动注册、token 签发。
- **手动验证**:凭证填入后走完整浏览器流程截图确认(等用户提供 app_id/secret)。

## 不做的事(YAGNI)

- 不加 User 表字段 / alembic 迁移(复用 username 编码策略)
- 不做飞书客户端内免登(JSSDK 工作台免登)
- 不做已有账号绑定飞书的管理界面
- 不改动其他 OAuth provider 的现有行为

## 关键文件路径

- 路由/控制器:`backend/app/api/v1/module_system/auth/controller.py`
- OAuth 服务(核心):`backend/app/api/v1/module_system/auth/oauth_service.py`
- 登录服务/token 签发:`backend/app/api/v1/module_system/auth/service.py`
- 配置:`backend/app/config/setting.py`(env 目录 `backend/env/`)
- User 模型:`backend/app/api/v1/module_system/user/model.py`
- 前端登录 API:`frontend/web/src/api/module_system/auth.ts`
- 前端第三方按钮:`frontend/web/src/components/views/fa-login/widgets/FaLoginThirdPartySection.vue`
- 前端 OAuth 跳转:`frontend/web/src/utils/oauth/index.ts`
- 前端登录页:`frontend/web/src/views/module_system/auth/login/index.vue`
