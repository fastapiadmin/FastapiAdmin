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
# 回调异常时回跳的前端登录页(需与实际一致)
OAUTH_FRONTEND_FALLBACK=http://127.0.0.1:5173/login
```

## 3. 流程
登录页点击「飞书」→ 跳转飞书授权 → 授权后回调后端 → 自动注册/登录 → 带 token 跳回前端 `/login` → 进入系统。
首次登录自动创建用户名 `oauth_feishu_{union_id}`,分配 `OAUTH_DEFAULT_ROLE_IDS` 默认角色。
