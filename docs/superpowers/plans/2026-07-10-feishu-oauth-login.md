# 飞书授权登录 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 CodataAdmin 增加"飞书授权登录",作为现有 OAuth 框架的新 provider `feishu`,支持网页 OAuth2 授权码登录 + 首次登录自动注册。

**Architecture:** 复用项目已有的第三方 OAuth 框架(state 存 Redis、token 由 `LoginService.create_token` 签发、用户由 `ensure_oauth_user` 自动注册、前端整页跳转 + `/login` 回调消费 token)。后端在 `oauth_service.py` 增加飞书专属的两步换 token 流程(先取 `app_access_token`,再用 code 换 `user_access_token`),前端在登录页增加一个不受 `SHOW_SAAS_AUTH` 控制的独立飞书按钮。

**Tech Stack:** 后端 FastAPI + SQLAlchemy 2.0 + httpx + Redis;测试 pytest + pytest-asyncio(`asyncio_mode = "auto"`),用 monkeypatch mock httpx helper(不引入新依赖)。前端 Vue3 + TypeScript + Element Plus + vue-i18n。

## Global Constraints

- 飞书应用类型:**企业自建应用(国内版)**,API 域名默认 `https://open.feishu.cn`,做成配置项 `OAUTH_FEISHU_API_BASE`。
- provider 标识统一用字符串 `"feishu"`(前后端一致)。
- 不修改数据库表:用户自动注册复用现有 `_username_for_oauth`(`oauth_feishu_{union_id}`)。
- `unique_id` 用飞书 `union_id`(跨应用稳定);缺失时回退 `open_id`。
- 飞书 API 通用响应格式 `{"code": 0, "msg": "...", "data": {...}}`,`code != 0` 视为失败,抛 `CustomException(msg=...)`。
- 所有外部 HTTP 调用复用现有 `_http_json` helper。
- 凭证留空可运行(缺失时 `_require_credentials` 抛明确错误),不阻塞代码合入。
- 不做 JSSDK 工作台免登、不做已有账号绑定飞书界面、不改动其他 provider 行为。

---

### Task 1: 后端配置项 — 新增飞书 OAuth 配置

**Files:**
- Modify: `backend/app/config/setting.py`(OAuth 段,当前 :137-147)

**Interfaces:**
- Produces: `settings.OAUTH_FEISHU_APP_ID: str`、`settings.OAUTH_FEISHU_APP_SECRET: str`、`settings.OAUTH_FEISHU_API_BASE: str`(默认 `"https://open.feishu.cn"`)。供 Task 2 使用。

- [ ] **Step 1: 添加配置字段**

在 `backend/app/config/setting.py` 中,找到 OAuth 段现有的 QQ 配置行:

```python
    OAUTH_QQ_APP_ID: str = ""
    OAUTH_QQ_APP_SECRET: str = ""
```

在其后紧接着添加(仍在 OAuth 段内,`# 外部 HTTP` 注释之前):

```python
    # 飞书企业自建应用(国内版 open.feishu.cn);Lark 国际版把 API_BASE 改为 https://open.larksuite.com
    OAUTH_FEISHU_APP_ID: str = ""
    OAUTH_FEISHU_APP_SECRET: str = ""
    OAUTH_FEISHU_API_BASE: str = "https://open.feishu.cn"
```

- [ ] **Step 2: 验证配置可加载**

Run: `cd backend && python -c "from app.config.setting import settings; print(settings.OAUTH_FEISHU_APP_ID, '|', settings.OAUTH_FEISHU_API_BASE)"`
Expected: 输出 ` | https://open.feishu.cn`(app_id 为空字符串,api_base 为默认域名),无异常。

- [ ] **Step 3: Commit**

```bash
git add backend/app/config/setting.py
git commit -m "feat(oauth): 新增飞书 OAuth 配置项"
```

---

### Task 2: 后端 — 飞书 OAuth 服务逻辑(核心)

**Files:**
- Modify: `backend/app/api/v1/module_system/auth/oauth_service.py`
- Test: `backend/tests/test_feishu_oauth.py`(Create)

**Interfaces:**
- Consumes: `settings.OAUTH_FEISHU_APP_ID/APP_SECRET/API_BASE`(Task 1);现有 `_http_json`、`_require_credentials`、`build_authorize_url`、`complete_oauth_login`、`ensure_oauth_user`。
- Produces:
  - `OAuthProvider` 类型新增 `"feishu"`。
  - `async def fetch_feishu_app_access_token() -> str`
  - `async def exchange_feishu_token(code: str) -> str`(返回 user_access_token)
  - `async def fetch_feishu_profile(user_access_token: str) -> tuple[str, str]`(返回 `(unique_id, display_name)`,unique_id 优先 union_id 否则 open_id)
  - `complete_oauth_login` 支持 `provider == "feishu"` 分支。

- [ ] **Step 1: 写失败测试 — app_access_token 成功与失败**

创建 `backend/tests/test_feishu_oauth.py`:

```python
"""飞书 OAuth 服务单元测试。mock _http_json,不发真实请求。"""

import pytest

from app.api.v1.module_system.auth import oauth_service
from app.core.exceptions import CustomException


@pytest.fixture(autouse=True)
def _feishu_creds(monkeypatch):
    monkeypatch.setattr(oauth_service.settings, "OAUTH_FEISHU_APP_ID", "cli_test", raising=False)
    monkeypatch.setattr(oauth_service.settings, "OAUTH_FEISHU_APP_SECRET", "secret_test", raising=False)
    monkeypatch.setattr(oauth_service.settings, "OAUTH_FEISHU_API_BASE", "https://open.feishu.cn", raising=False)


def _mock_http_json(monkeypatch, responses):
    """responses: 按调用顺序返回的 dict 列表。"""
    calls = {"i": 0}

    async def fake(method, url, **kwargs):
        idx = calls["i"]
        calls["i"] += 1
        return responses[idx]

    monkeypatch.setattr(oauth_service, "_http_json", fake)
    return calls


async def test_fetch_app_access_token_success(monkeypatch):
    _mock_http_json(monkeypatch, [{"code": 0, "app_access_token": "a-at-123"}])
    token = await oauth_service.fetch_feishu_app_access_token()
    assert token == "a-at-123"


async def test_fetch_app_access_token_error_code(monkeypatch):
    _mock_http_json(monkeypatch, [{"code": 10003, "msg": "invalid app_secret"}])
    with pytest.raises(CustomException):
        await oauth_service.fetch_feishu_app_access_token()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd backend && pytest tests/test_feishu_oauth.py -v`
Expected: FAIL — `AttributeError: module ... has no attribute 'fetch_feishu_app_access_token'`

- [ ] **Step 3: 实现 — 类型 + 凭证 + app_access_token**

在 `oauth_service.py` 顶部,修改 `OAuthProvider`:

```python
OAuthProvider = Literal["wechat", "qq", "github", "gitee", "feishu"]
```

在 `_require_credentials` 函数的 `elif provider == "qq":` 分支之后、`else:` 之前,加飞书分支:

```python
    elif provider == "feishu":
        cid, sec = settings.OAUTH_FEISHU_APP_ID, settings.OAUTH_FEISHU_APP_SECRET
```

在文件末尾 `save_oauth_state` 之前(或 fetch_qq_profile 之后的任意合适位置)新增飞书专属函数:

```python
def _feishu_base() -> str:
    return str(settings.OAUTH_FEISHU_API_BASE).rstrip("/")


async def fetch_feishu_app_access_token() -> str:
    """企业自建应用:用 app_id + app_secret 换 app_access_token。"""
    app_id, app_secret = _require_credentials("feishu")
    data = await _http_json(
        "POST",
        f"{_feishu_base()}/open-apis/auth/v3/app_access_token/internal",
        headers={"Content-Type": "application/json; charset=utf-8"},
        json={"app_id": app_id, "app_secret": app_secret},
    )
    if not isinstance(data, dict) or data.get("code") not in (0, "0"):
        raise CustomException(msg=(isinstance(data, dict) and data.get("msg")) or "飞书获取 app_access_token 失败")
    token = data.get("app_access_token")
    if not token:
        raise CustomException(msg="飞书 app_access_token 为空")
    return str(token)
```

- [ ] **Step 4: 运行测试确认通过**

Run: `cd backend && pytest tests/test_feishu_oauth.py -v`
Expected: PASS(2 passed)

- [ ] **Step 5: 写失败测试 — exchange_feishu_token 与 fetch_feishu_profile**

在 `tests/test_feishu_oauth.py` 追加:

```python
async def test_exchange_feishu_token_success(monkeypatch):
    # 第 1 次调用:app_access_token;第 2 次:oidc/access_token
    _mock_http_json(monkeypatch, [
        {"code": 0, "app_access_token": "a-at-123"},
        {"code": 0, "data": {"access_token": "u-at-456"}},
    ])
    token = await oauth_service.exchange_feishu_token("the-code")
    assert token == "u-at-456"


async def test_exchange_feishu_token_error(monkeypatch):
    _mock_http_json(monkeypatch, [
        {"code": 0, "app_access_token": "a-at-123"},
        {"code": 20037, "msg": "code expired"},
    ])
    with pytest.raises(CustomException):
        await oauth_service.exchange_feishu_token("the-code")


async def test_fetch_feishu_profile_prefers_union_id(monkeypatch):
    _mock_http_json(monkeypatch, [
        {"code": 0, "data": {"union_id": "on_union_1", "open_id": "ou_open_1", "name": "张三"}},
    ])
    uid, name = await oauth_service.fetch_feishu_profile("u-at-456")
    assert uid == "on_union_1"
    assert name == "张三"


async def test_fetch_feishu_profile_fallback_open_id(monkeypatch):
    _mock_http_json(monkeypatch, [
        {"code": 0, "data": {"open_id": "ou_open_1", "name": "李四"}},
    ])
    uid, name = await oauth_service.fetch_feishu_profile("u-at-456")
    assert uid == "ou_open_1"
    assert name == "李四"


async def test_fetch_feishu_profile_error(monkeypatch):
    _mock_http_json(monkeypatch, [{"code": 99991663, "msg": "token invalid"}])
    with pytest.raises(CustomException):
        await oauth_service.fetch_feishu_profile("bad")
```

- [ ] **Step 6: 运行测试确认失败**

Run: `cd backend && pytest tests/test_feishu_oauth.py -v`
Expected: FAIL — `AttributeError: ... has no attribute 'exchange_feishu_token'`

- [ ] **Step 7: 实现 exchange_feishu_token 与 fetch_feishu_profile**

在 `fetch_feishu_app_access_token` 之后新增:

```python
async def exchange_feishu_token(code: str) -> str:
    """用 code 换 user_access_token(需先带上 app_access_token)。"""
    app_at = await fetch_feishu_app_access_token()
    data = await _http_json(
        "POST",
        f"{_feishu_base()}/open-apis/authen/v1/oidc/access_token",
        headers={
            "Authorization": f"Bearer {app_at}",
            "Content-Type": "application/json; charset=utf-8",
        },
        json={"grant_type": "authorization_code", "code": code},
    )
    if not isinstance(data, dict) or data.get("code") not in (0, "0"):
        raise CustomException(msg=(isinstance(data, dict) and data.get("msg")) or "飞书换取 user_access_token 失败")
    inner = data.get("data") or {}
    token = inner.get("access_token")
    if not token:
        raise CustomException(msg="飞书 user_access_token 为空")
    return str(token)


async def fetch_feishu_profile(user_access_token: str) -> tuple[str, str]:
    """取飞书用户信息,返回 (unique_id, display_name)。unique_id 优先 union_id。"""
    data = await _http_json(
        "GET",
        f"{_feishu_base()}/open-apis/authen/v1/user_info",
        headers={"Authorization": f"Bearer {user_access_token}"},
    )
    if not isinstance(data, dict) or data.get("code") not in (0, "0"):
        raise CustomException(msg=(isinstance(data, dict) and data.get("msg")) or "飞书获取用户信息失败")
    inner = data.get("data") or {}
    uid = inner.get("union_id") or inner.get("open_id")
    if not uid:
        raise CustomException(msg="飞书用户唯一标识缺失")
    name = str(inner.get("name") or "feishu")
    return str(uid), name
```

- [ ] **Step 8: 运行测试确认通过**

Run: `cd backend && pytest tests/test_feishu_oauth.py -v`
Expected: PASS(7 passed)

- [ ] **Step 9: 写失败测试 — build_authorize_url 支持飞书**

在 `tests/test_feishu_oauth.py` 追加:

```python
def test_build_authorize_url_feishu():
    url = oauth_service.build_authorize_url(
        provider="feishu",
        callback_url="https://x.com/api/v1/system/auth/oauth/feishu/callback",
        state="st-1",
    )
    assert url.startswith("https://open.feishu.cn/open-apis/authen/v1/authorize?")
    assert "app_id=cli_test" in url
    assert "state=st-1" in url
    assert "redirect_uri=" in url
```

- [ ] **Step 10: 运行测试确认失败**

Run: `cd backend && pytest tests/test_feishu_oauth.py::test_build_authorize_url_feishu -v`
Expected: FAIL — `CustomException: 不支持的 OAuth 渠道`(build_authorize_url 尾部抛出)

- [ ] **Step 11: 实现 build_authorize_url 飞书分支**

在 `build_authorize_url` 中,`if provider == "qq":` 分支之后、结尾 `raise CustomException(msg="不支持的 OAuth 渠道")` 之前,加:

```python
    if provider == "feishu":
        params = {
            "app_id": cid,
            "redirect_uri": callback_url,
            "state": state,
        }
        return f"{_feishu_base()}/open-apis/authen/v1/authorize?" + urlencode(params)
```

- [ ] **Step 12: 运行测试确认通过**

Run: `cd backend && pytest tests/test_feishu_oauth.py -v`
Expected: PASS(8 passed)

- [ ] **Step 13: 在 complete_oauth_login 加飞书分支**

在 `complete_oauth_login` 的 provider 分支链中,`elif provider == "qq":` 之后、`else:` 之前,加:

```python
    elif provider == "feishu":
        access = await exchange_feishu_token(code)
        uid, name = await fetch_feishu_profile(access)
```

(注意:`callback_url` 与 `cid`/`csec` 已在分支链前取好,飞书分支不需要它们——凭证在 `exchange_feishu_token` 内部经 `_require_credentials` 获取;这与现有分支不冲突。)

- [ ] **Step 14: 更新 __all__ 导出**

在文件末尾 `__all__` 列表中加入新函数(便于测试与外部引用):

```python
    "fetch_feishu_app_access_token",
    "exchange_feishu_token",
    "fetch_feishu_profile",
```

- [ ] **Step 15: 运行全部飞书测试**

Run: `cd backend && pytest tests/test_feishu_oauth.py -v`
Expected: PASS(8 passed)

- [ ] **Step 16: Commit**

```bash
git add backend/app/api/v1/module_system/auth/oauth_service.py backend/tests/test_feishu_oauth.py
git commit -m "feat(oauth): 飞书 OAuth 服务逻辑(两步换 token + user_info)"
```

---

### Task 3: 后端 — controller 放行 feishu provider

**Files:**
- Modify: `backend/app/api/v1/module_system/auth/controller.py`(:210, :216, :275)

**Interfaces:**
- Consumes: Task 2 的 `complete_oauth_login` feishu 分支、`build_authorize_url` feishu 分支。
- Produces: `GET /api/v1/system/auth/oauth/feishu/login` 与 `.../feishu/callback` 可用。

- [ ] **Step 1: login 控制器白名单加 feishu**

在 `controller.py`,`oauth_login_redirect_controller` 内:

将
```python
    allowed = {"wechat", "qq", "github", "gitee"}
```
改为
```python
    allowed = {"wechat", "qq", "github", "gitee", "feishu"}
```

同时把该函数 `provider` 参数的描述(:210)
```python
    provider: Annotated[str, Path(description="wechat | qq | github | gitee")],
```
改为
```python
    provider: Annotated[str, Path(description="wechat | qq | github | gitee | feishu")],
```

- [ ] **Step 2: callback 控制器白名单加 feishu**

在 `oauth_callback_controller` 内(:275):

将
```python
    if provider not in {"wechat", "qq", "github", "gitee"}:
```
改为
```python
    if provider not in {"wechat", "qq", "github", "gitee", "feishu"}:
```

- [ ] **Step 3: 验证路由注册且飞书 provider 被接受**

Run:
```bash
cd backend && python -c "
from fastapi.testclient import TestClient
from main import app
c = TestClient(app, follow_redirects=False)
r = c.get('/api/v1/system/auth/oauth/feishu/login', params={'redirect_uri': 'http://127.0.0.1:5173/login'})
print('status', r.status_code)
print('location', r.headers.get('location', '')[:120])
"
```
Expected: `status 302`;因凭证为空,`_require_credentials` 抛错,location 应为回到 `.../login?oauth_error=...`(URL 含 `oauth_error`,证明 provider 已被放行且进入了 build 流程)。若凭证已配置则 location 指向 `open.feishu.cn`。

> 注:若 `main.py` 导入路径在你的 shell 下不同,用 `cd backend` 后按项目 README 的启动方式运行等价检查即可。关键是确认返回 302 且不再是"不支持的 OAuth 渠道"。

- [ ] **Step 4: Commit**

```bash
git add backend/app/api/v1/module_system/auth/controller.py
git commit -m "feat(oauth): controller 放行 feishu provider"
```

---

### Task 4: 前端 — provider 类型与 i18n 文案

**Files:**
- Modify: `frontend/web/src/api/module_system/auth.ts:6`
- Modify: `frontend/web/src/components/views/fa-login/widgets/FaLoginThirdPartySection.vue`(内联类型 :32 依赖导入,和 oauthItems :44)
- Modify: `frontend/web/src/components/views/fa-login/forms/FaLoginAccountForm.vue:206`(内联联合类型)
- Modify: `frontend/web/src/locales/langs/zh.json`(:434 oauthTooltip)
- Modify: `frontend/web/src/locales/langs/en.json`(:434 oauthTooltip)

**Interfaces:**
- Produces: `OAuthProvider` 前端类型含 `"feishu"`;i18n key `login.oauthTooltip.feishu`。供 Task 5 使用。

- [ ] **Step 1: 扩展 OAuthProvider 类型**

`frontend/web/src/api/module_system/auth.ts:6`:

```typescript
export type OAuthProvider = "wechat" | "qq" | "github" | "gitee" | "feishu";
```

- [ ] **Step 2: 同步 AccountForm 内联联合类型**

`frontend/web/src/components/views/fa-login/forms/FaLoginAccountForm.vue:206`:

```typescript
  oauth: [provider: "wechat" | "qq" | "github" | "gitee" | "feishu"];
```

- [ ] **Step 3: 添加 i18n 文案(中文)**

`frontend/web/src/locales/langs/zh.json` 中 `oauthTooltip` 对象:

```json
    "oauthTooltip": {
      "wechat": "微信",
      "qq": "QQ",
      "github": "GitHub",
      "gitee": "Gitee",
      "feishu": "飞书"
    },
```

- [ ] **Step 4: 添加 i18n 文案(英文)**

`frontend/web/src/locales/langs/en.json` 中 `oauthTooltip` 对象:

```json
    "oauthTooltip": {
      "wechat": "WeChat",
      "qq": "QQ",
      "github": "GitHub",
      "gitee": "Gitee",
      "feishu": "Feishu"
    },
```

- [ ] **Step 5: (可选)第三方图标区加飞书项**

在 `FaLoginThirdPartySection.vue` 的 `oauthItems` computed 数组末尾(gitee 项之后)追加(该组件仅在 `SHOW_SAAS_AUTH=true` 时显示,加上以保持完整):

```typescript
  {
    provider: "feishu" as const,
    tip: t("login.oauthTooltip.feishu"),
    icon: "simple-icons:feishu",
    iconClass: "size-[22px] max-sm:size-[18px] text-[#00d6b9]",
  },
```

- [ ] **Step 6: 类型检查**

Run: `cd frontend/web && npx vue-tsc --noEmit 2>&1 | grep -iE "feishu|oauth|auth.ts|AccountForm" || echo "no feishu/oauth type errors"`
Expected: `no feishu/oauth type errors`(与飞书/OAuth 相关无新增类型错误)。

- [ ] **Step 7: Commit**

```bash
git add frontend/web/src/api/module_system/auth.ts frontend/web/src/components/views/fa-login/forms/FaLoginAccountForm.vue frontend/web/src/components/views/fa-login/widgets/FaLoginThirdPartySection.vue frontend/web/src/locales/langs/zh.json frontend/web/src/locales/langs/en.json
git commit -m "feat(oauth): 前端 feishu provider 类型与文案"
```

---

### Task 5: 前端 — 独立飞书登录按钮(不受 SHOW_SAAS_AUTH 控制)

**Files:**
- Modify: `frontend/web/src/components/views/fa-login/forms/FaLoginAccountForm.vue`(模板 :147-157 区域;script :171-209)

**Interfaces:**
- Consumes: `OAuthProvider` 含 feishu(Task 4)、i18n `login.oauthTooltip.feishu`(Task 4)、父级已绑定的 `@oauth="handleOAuthLogin"`(index.vue:68)、`startOAuthLogin('feishu')`(现有 `@utils`)。
- Produces: 登录页出现"飞书登录"按钮,点击触发整页跳转到后端飞书 OAuth 入口。

- [ ] **Step 1: 在账号表单登录按钮下方加独立飞书按钮**

`FaLoginAccountForm.vue` 模板中,找到登录按钮所在 `</div>`(:147,即 `{{ $t("login.btnText") }}` 的 ElButton 收尾那一段之后),在紧邻的 `<div v-if="SHOW_SAAS_AUTH" class="login-secondary-actions ...">`(:149)**之前**插入(即放在主登录按钮下、SaaS 次要操作区之上):

```vue
        <div class="login-feishu-entry mt-2">
          <ElButton
            class="login-feishu-btn w-full"
            plain
            @click="$emit('oauth', 'feishu')"
          >
            <FaSvgIcon icon="simple-icons:feishu" class="mr-1 size-[16px] text-[#00d6b9]" />
            {{ $t("login.oauthTooltip.feishu") }}
          </ElButton>
        </div>
```

> `FaSvgIcon` 在本项目为全局组件(现有第三方区已直接使用,无需 import);若类型检查提示未注册,则在 `<script setup>` 顶部加 `import FaSvgIcon from "@/components/core/....";` —— 先按全局组件用,报错再补 import。

- [ ] **Step 2: 前端启动,人工确认按钮出现且可点击**

Run: `cd frontend/web && npm run dev`
打开浏览器登录页,确认:
1. 账号密码表单下方出现"飞书"按钮(中文环境)。
2. 点击后浏览器整页跳转到 `/api/v1/system/auth/oauth/feishu/login?redirect_uri=...`(凭证未配置时会 302 回 `/login?oauth_error=...` 并弹出错误提示——这是预期,证明链路打通)。

Expected: 按钮渲染正常;点击触发跳转;因凭证空,回到登录页并提示飞书未配置类错误。

- [ ] **Step 3: 类型检查**

Run: `cd frontend/web && npx vue-tsc --noEmit 2>&1 | grep -iE "AccountForm|feishu" || echo "no new type errors"`
Expected: `no new type errors`

- [ ] **Step 4: Commit**

```bash
git add frontend/web/src/components/views/fa-login/forms/FaLoginAccountForm.vue
git commit -m "feat(oauth): 登录页新增独立飞书登录按钮"
```

---

### Task 6: 文档 — 配置与联调说明

**Files:**
- Create: `backend/env/.env.example` 追加飞书配置说明,或 Modify 项目现有 OAuth 文档(若 `docs/` 下有 OAuth 说明则改之;否则在 spec 同目录留一份简短 README)。

**Interfaces:**
- Produces: 用户拿到 app_id/app_secret 后填哪里、飞书后台回调域怎么配的说明。

- [ ] **Step 1: 写配置说明**

创建 `backend/docs/feishu-oauth.md`(若 `backend/docs/` 不存在则创建目录):

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add backend/docs/feishu-oauth.md
git commit -m "docs(oauth): 飞书授权登录配置与联调说明"
```

---

## Self-Review

**Spec coverage:**
- 配置项 3 个 → Task 1 ✅
- 两步换 token(app_access_token → user_access_token)→ Task 2 Step 3/7 ✅
- user_info 取 union_id/open_id/name → Task 2 Step 7 ✅
- OAuthProvider 加 feishu(后端)→ Task 2 Step 3 ✅;(前端)→ Task 4 ✅
- build_authorize_url 飞书分支 → Task 2 Step 11 ✅
- complete_oauth_login 飞书分支(unique_id=union_id)→ Task 2 Step 13 ✅
- controller 两处白名单 → Task 3 ✅
- 前端独立飞书入口(不受 SHOW_SAAS_AUTH)→ Task 5 ✅
- i18n 中英 → Task 4 ✅
- 错误处理(code!=0 抛 CustomException,回调走 oauth_error)→ Task 2 各函数 + 复用现有 controller 错误重定向 ✅
- 测试(mock httpx helper,覆盖成功+失败)→ Task 2 ✅
- 配置/联调文档 → Task 6 ✅
- 不改表、不做 JSSDK、不做绑定界面 → 计划未涉及,符合 YAGNI ✅

**Placeholder scan:** 无 TBD/TODO;每个代码步骤均给出完整代码。

**Type consistency:** `fetch_feishu_app_access_token`/`exchange_feishu_token`/`fetch_feishu_profile` 三个函数名在 Task 2 定义、__all__ 导出、complete_oauth_login 调用处一致;前端 `"feishu"` 字面量在 auth.ts、AccountForm 内联类型、按钮 emit 三处一致;i18n key `login.oauthTooltip.feishu` 在 Task 4 定义、Task 5 使用一致。
