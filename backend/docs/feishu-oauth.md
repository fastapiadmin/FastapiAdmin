# 飞书授权登录配置

## 1. 飞书开放平台创建企业自建应用
- 平台:https://open.feishu.cn → 开发者后台 → 创建企业自建应用
- 记录 App ID、App Secret
- 「安全设置 → 重定向 URL」添加后端回调地址:
  `https://<你的后端域名>/api/v1/system/auth/oauth/feishu/callback`
  (本地调试:`http://127.0.0.1:8001/api/v1/system/auth/oauth/feishu/callback`)
- 开通权限:获取用户 user_id / 通过 OAuth 获取用户身份(authen 相关)

## 2. 后端环境变量
在 `backend/env/.env.<环境>` 中填写(默认全空,不影响启动):

```
OAUTH_FEISHU_APP_ID=cli_xxxxxxxx
OAUTH_FEISHU_APP_SECRET=xxxxxxxxxxxx
# 国内版默认无需改;Lark 国际版改为 https://open.larksuite.com
OAUTH_FEISHU_API_BASE=https://open.feishu.cn
# 授权页域名(与 API 域名不同);Lark 国际版改为 https://accounts.larksuite.com
OAUTH_FEISHU_AUTH_BASE=https://accounts.feishu.cn
# 回调异常时回跳的前端登录页(需与实际一致)
OAUTH_FRONTEND_FALLBACK=http://127.0.0.1:5173/login
```

> 说明:授权页跳转域名为 `accounts.feishu.cn`(`OAUTH_FEISHU_AUTH_BASE`),而 token 换取 / app_access_token / user_info 等 API 调用域名为 `open.feishu.cn`(`OAUTH_FEISHU_API_BASE`),两者不同,请勿混用。

## 3. 流程
登录页点击「飞书」→ 跳转飞书授权 → 授权后回调后端 → 自动注册/登录 → 带 token 跳回前端 `/login` → 进入系统。
首次登录自动创建用户名 `oauth_feishu_{union_id}`,分配 `OAUTH_DEFAULT_ROLE_IDS` 默认角色。

> 技术说明:授权码换 `user_access_token` 走飞书标准 OAuth2 端点 `authen/v2/oauth/token`(单步,直接用 `client_id`+`client_secret`+`code`+`redirect_uri`,不再经 `app_access_token` 中转)。回调地址 `redirect_uri` 换 token 时会与授权时严格比对,必须与飞书后台配置的「重定向 URL」完全一致。
