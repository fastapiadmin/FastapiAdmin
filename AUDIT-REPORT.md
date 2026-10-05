# FastapiAdmin 全栈审计总报告

> 生成时间：2026-10-04
> 审计范围：后端（FastAPI）、Web 管理后台（Vue3）、移动端（uniapp）、部署编排（Docker/Nginx）、需求覆盖、测试与可验证性、交互与视觉一致性
> 参与：7 名审计成员并行执行 + 队长线上实测复核
> 方法：只读审查 + 真实命令执行（命令与退出码均记录在各分报告）；线上结论均由对生产环境的实测得出

---

## 0. 一句话结论

**这是一个功能可用、但安全与质量债较重的单租户 RBAC 中后台**：认证、权限、代码生成等核心能力具备，但存在多类可被直接利用的问题（公开密钥可伪造令牌、超管弱口令、代码生成即 RCE、部署面暴露），同时需求文档声称的 SaaS 多租户能力在代码中零实现——需求文档与实际产品是两件事。

---

## 1. 覆盖范围与缺口（必须先看）

| 维度 | 已覆盖 | 未覆盖 / 存疑 |
| --- | --- | --- |
| 后端代码 | 216 个 py 文件 / 28519 行静态审查；`ruff check` 全量通过 | 需真实 MySQL/PostgreSQL/Redis 的行为未验证（本机三端口均不可达） |
| 前端 Web | 101 个 `.vue`；`type-check` exit 0；`vitest` 10/10 通过 | 无浏览器实机验证；无真机性能数据 |
| 移动端 uniapp | 14 个页面；`type-check` exit 0 | 未跑 `uni build` 各平台产物；无真机验证；0 测试 |
| 部署编排 | compose 校验、镜像构建、容器运行时、端口、证书、资源实测 | 未做真实压测；未验证灾备恢复演练 |
| 需求覆盖 | 逐行读 REQUIREMENTS.md Part1 + §11–§19 + §20–§22 + §28–§30 | §23–§27、§38–§40 依「代码零实现」这一可穷举事实下结论，未逐行读正文表格 |
| 测试 | pytest 与 vitest 真实执行 | 迁移链路 0 覆盖；无 CI |

**审计成员明确声明的抽样边界与存疑项**，见各分报告末尾章节；本报告不把抽样结论伪装成全量结论。

---

## 2. 必须先止血的问题（可被直接利用）

### 2.1 [blocker] 生产使用源码公开的默认 SECRET_KEY

- 证据：`backend/app/config/setting.py:66` 默认值硬编码；`docker/docker-compose.yaml`、`docker/.env.example`、`backend/env/.env.prod` 三处均无该键（grep 验证 + 线上容器 env 实测）
- 后果：
  - `backend/app/core/security.py:114,139` 用该密钥签发/校验 JWT → 可离线伪造任意用户（含超管）令牌
  - `backend/app/core/crypto_util.py:47-56` 用同一密钥经 HKDF 派生 `DATA_ENCRYPTION_KEY` → 落库的加密字段（API Key、存储源口令）可被解密
  - 与 `/api/v1/monitor/online/list` 返回的 session_id 结合，可在不知道任何口令的情况下完成认证绕过
- 为什么严重：攻击者只需要拿到源码（或知道该默认字符串），不需要任何其他条件

### 2.2 [blocker] 种子超管账号使用公开弱口令

- 证据：安全审计经 PBKDF2 复算确认种子哈希对应 `123456`；`backend/app/scripts/initialize.py` 无环境判断，空库启动即写入；README 中公开该口令
- 受影响账号：`super`、`admin`（均为超管）
- 实测补充：种子账号的登录受滑块验证码保护，但安全审计判定该验证码**无实质人机校验**，不构成有效防线

### 2.3 [blocker] 代码生成模板导致权限即 RCE

- 证据：生成模板 `autoescape=False`，把 `function_name` / `column_comment` / `column_name` 原样写入 `.py`；输出目录为 `app/plugin/**`，而 `app/core/discover.py:52,74` 在启动时 import 该目录
- 后果：任何拥有代码生成权限的账号可通过构造字段注释写入任意 Python 代码，服务重启后执行
- 相关：`backend/app/modules/system/scheduler` 侧 `SCHEDULER_ALLOW_CODE_EXEC=True`（`setting.py:127`）+ `exec` 带完整 builtins（`ap_scheduler.py:562-563`）无需 gencode 权限同样构成 RCE 面

### 2.4 [blocker] 仓库当前**无法构建**

- 证据：`docker/backend/Dockerfile` 仍只 `COPY requirements.txt`，而依赖已拆分为 `backend/requirements/`；该目录**未被 git 跟踪**（`git ls-files backend/requirements` = 0）
- 后果：新克隆的仓库按文档构建必然失败；`deploy-artifacts.sh` 因其自带 Dockerfile 生成逻辑而绕过该问题，但这掩盖了仓库本身的破损
- 状态：本轮已将仓库 Dockerfile 改写为与新依赖结构一致（见 §4）

### 2.5 [high] 部署面暴露与错误默认值

| 项 | 证据 | 状态 |
| --- | --- | --- |
| API 文档公网可访问 | `/api/v1/docs`、`/redoc`、`/openapi.json` 实测 200 | 已修（nginx 仅放行内网） |
| MySQL/Redis/Backend 端口对公网开放 | 外部实测 3306/6379/8001 均可达 | 已修（绑定 127.0.0.1） |
| 生产 CORS 回落为 `["*"]` 且 `ALLOW_CREDENTIALS=True` | `setting.py:243-248` | 待修 |
| `FORWARDED_ALLOW_IPS="*"` | `docker-compose.yaml:119`；叠加后端端口曾暴露 → 可伪造 XFF 绕过限流与登录 IP 记录 | 待修 |
| 登录失败返回 HTTP 500 | 实测：验证码过期走 `custom_exception_handler` → 500（业务异常被当服务器错误） | 待修 |

---

## 3. 逻辑与契约缺陷（影响数据正确性）

1. **通知状态枚举两端冲突**（已复核）：后端权威 `notice/model.py:16` = `0草稿/1已发布/2已归档`，移动端一致；Web 端 `views/module_system/notice/index.vue:116-117,189-190,254,403` 却是 `0启用/1停用` → 已归档公告在 Web 显示为灰色数字「2」，且筛选条件里不存在「已归档」。
2. **移动端刷新令牌格式不符**：app 发 `{refresh_token}` 对象，后端 `auth/controller.py:57` 为 `Body(str)` → 422；移动端 token 过期后必然强制登出。
3. **移动端文件上传路径错误**：app 调 `/file/upload`，真实路径为 `/api/v1/common/file/upload` → 404。
4. **移动端生产 WebSocket 指向 localhost**：`app/.env.production:23` = `ws://localhost:5180/ws` → 线上 AI 对话不可用。
5. **富文本默认上传地址畸形**：`web/src/components/forms/fa-wang-editor/index.vue:83` 拼出 `//file/upload`（协议相对 + 缺 `/common`）→ 公告/工单插图必失败。
6. **Web 生产构建开关恒 false**：`web/vite.config.ts:28` 判断 `mode === "prod"`，而脚本只传 `production/development` → minify、drop_console、gzip/brotli、剔除 vue-devtools 全部不生效。
7. **CRUDBase 权限注入不完整**：`base_crud.py:300-330` 仅读路径注入数据权限，`delete/clear/set`（`:225-251`）不注入；6 处 `set_available` 无完整性校验 → 普通管理员可改任意部门/字典/公告、可停用超管。
8. **部门/菜单成环导致权限查询 500**：`common_util.py:181-196` 的 `get_child_recursion` 无 visited 集合。

---

## 4. 本轮已落地的修复（部署侧，全部有验证证据）

| 修复 | 证据 |
| --- | --- |
| 关闭公网数据面暴露：3306/6379/8001 仅绑 127.0.0.1 | 外部实测三端口均已关闭；四端 200 |
| API 文档对外封堵（仅内网可访问） | 外部 403，服务器本机 200，业务接口不受影响 |
| 容器改为非 root 运行（uid=1000 app） | 容器内 `id` = app；日志/上传/迁移目录均可写 |
| TLS 私钥与 `.env` 权限收紧到 600 | `stat` 实测；nginx 仍可读取 |
| 隐藏文件不再对外服务 | `.DS_Store` 由 200 变 403，并加 nginx deny 兜底 |
| 静态资源长缓存 | 哈希资源 `max-age=31536000, immutable`，图片 30 天，HTML 不缓存 |
| nginx 升级 1.25.5 → 1.27.5 | 配置校验通过；TLS1.2/1.3 正常；保留 `nginx:rollback-1.25` |
| 后端健康检查修复 | 由长期 unhealthy 变为 healthy（`ALLOWED_HOSTS` 放行 localhost） |
| 后端依赖拆分（核心 / 数据库驱动 / 存储） | MySQL 变体镜像 565MB → 521MB；PG 变体自检 asyncpg+psycopg 通过 |
| 部署脚本具备备份、回滚、轮转、变体构建 | `deploy-artifacts.sh` 各子命令均实测通过（含回滚哨兵测试） |
| SSH 加固 | 密码登录禁用、root 仅密钥、密码已轮换 |

---

## 5. 修复路线（按风险×成本排序）

| 优先级 | 动作 | 影响面 | 预估 |
| --- | --- | --- | --- |
| P0 | 注入强随机 `SECRET_KEY` + `DATA_ENCRYPTION_KEY`；轮换 super/admin 口令；若启用演示模式则关闭 | 会话作废需重新登录；落库密文保持可解 | 30 分钟 |
| P0 | 修仓库 Dockerfile 与依赖跟踪，使「克隆即可构建」 | 无运行时影响 | 20 分钟 |
| P1 | 前端 5 条 P0（生产开关、刷新令牌、上传路径、WS 地址、富文本上传） | 需重建并部署前端 | 1–2 小时 |
| P1 | 后端：日志级别、`SCHEDULER_ALLOW_CODE_EXEC=False`、模板 `autoescape=True`、CRUDBase 补权限注入、`get_child_recursion` 防环 | 需完整回归 | 1 天 |
| P1 | 生产 CORS 显式白名单；`FORWARDED_ALLOW_IPS` 收敛；业务异常返回 4xx | 需回归 | 半天 |
| P2 | 建立 CI（后端 pytest + ruff、web type-check + vitest）；修复测试夹具（fakeredis、assert_route、隔离） | 无运行时影响 | 1–2 天 |
| P2 | Web i18n 补齐（85/101 页面未接入）与通知枚举修正 | 需产品确认后端是否提供菜单 i18n 字段 | 2–3 天 |
| P2 | 证书自动续期（当前 2027-03-06 到期，无续期与告警；ACME 路径被 301） | 无运行时影响 | 半天 |
| P3 | 清理死代码、`any` 治理、键盘可达性（76 处 `@click` 无 tabindex/role） | 渐进 | 持续 |

---

## 6. 需要决策的事项

1. **线上数据库口令与 OPENAI_API_KEY**：两者均出现在 git 历史（旧库口令命中 10 个提交，已推送到 `master/dev`），且镜像内 `.env.prod` 曾包含真实值 → 建议按已泄露处理并重新签发。是否重写 git 历史取决于仓库可见性。
2. **多租户规格错位**：`REQUIREMENTS.md` v3.6.0 描述 SaaS 多租户（`grep -ril tenant` 在三端 0 命中），实为单租户后台；该文档是 CHANGELOG.md 重命名产生的纯文档提交。是「改文档」还是「立项实现」，只能由产品决定。
3. **`/user/register` 接口**：无鉴权/无验证码/无开关（当前被 `DEMO_ENABLE` 挡住返回 400）。是否保留该接口、以及演示模式在生产是否应关闭。
4. **后端是否提供菜单名 i18n 字段**：Web 侧边栏菜单名来自数据库，补齐前端 i18n 后菜单仍为中文。
5. **移动端范围**：无批量操作、无导入导出是否已在需求中登记为范围外。

---

## 7. 本次审计对既有结论的修正（避免误判）

| 原表述 | 修正 |
| --- | --- |
| 任务背景称「Web 端使用 uno.config.ts」 | 不成立：Web 端为 Tailwind v4（`@tailwindcss/vite` + `tailwindcss@^4.3.0`），UnoCSS 仅存在于 app 端；两端令牌体系独立 |
| 安全报告称 `/user/register` 无鉴权可注册 | 接口确实无鉴权，但当前被演示模式拦截（实测 400）；风险取决于 `DEMO_ENABLE` |
| 队长初判 nginx `ssl_protocols` 缺 TLS1.3 | 误判：`nginx -T` 显示 `ssl_protocols TLSv1.2 TLSv1.3;`，实测 TLS1.3 可用 |
| 队长初判 `.DS_Store` 清理后仍可访问 | 实为清理成功，后续 200 来自 SPA 回退（`try_files` → index.html），已用 deny 规则彻底封堵 |

---

## 8. 分报告索引

| 报告 | 覆盖 |
| --- | --- |
| `backend/audit-backend.md` | 后端架构与代码质量（22 条） |
| `frontend/audit-frontend.md` | 前端与移动端工程（32 条） |
| `backend/audit-testing.md` | 测试与可验证性 |
| `backend/audit-security.md` | 认证/授权/敏感信息（23 条） |
| `backend/audit-requirements.md` | 需求覆盖对照 |
| `frontend/audit-uxui.md` | 交互与视觉一致性（590 行） |
| `docker/audit-deploy.md` | 容器化与部署链路（799 行） |

每份报告均包含：问题清单（级别 + 文件:行号 + 现象 + 影响 + 建议）、按优先级的修复清单、未验证/存疑项。

---

## 9. 修复进展（2026-10-04 更新）

### 9.1 已修复并验证（上线）

| 类别 | 修复内容 | 验证证据 |
| --- | --- | --- |
| 部署面 | MySQL/Redis/backend 端口收敛到 127.0.0.1 | 宿主机 socket 实测：公网监听数 0；服务器自连公网 IP 返回 ConnectionRefused |
| 部署面 | API 文档仅内网可访问 | 公网 403 / 内网 200 |
| 部署面 | 容器非 root（uid=1000）运行 | 容器内 `id` = app；日志/上传/迁移目录可写 |
| 部署面 | TLS 私钥与 .env 权限 600；隐藏文件 403 | stat 与 curl 实测 |
| 部署面 | 静态资源长缓存；nginx 升级 1.27.5；ACME 校验路径放行 | 响应头 `max-age=31536000, immutable`；证书 153 天 |
| 部署面 | 每日健康巡检（容器/接口/证书/磁盘/swap） | systemd timer active，日志全绿 |
| 部署面 | CI（backend: uv+ruff+pytest；frontend: type-check+vitest） | workflow 语法与引用脚本已校验 |
| 密钥 | SECRET_KEY 与 DATA_ENCRYPTION_KEY 轮换并注入；旧密钥保留于 OLD_KEYS | 旧密钥加密样本仍可解密；用旧公开默认密钥伪造的令牌被拒（InvalidSignatureError） |
| 口令 | 种子账号 super/admin/user 口令轮换 | 新口令与库内哈希匹配、旧口令 123456 被拒 |
| 策略 | 生产 CORS 不再回落通配；FORWARDED_ALLOW_IPS 收敛为应用网段；DEMO_ENABLE 显式化 | 恶意 Origin 无许可头；容器内环境变量实测 |
| 前端 | 5 条 P0（生产构建开关、令牌刷新、上传路径、WS/开发地址） | type-check×2、build:prod、build:h5 均 exit 0；产物第一方 console 0 命中；H5 内 localhost:5180 0 命中 |
| 后端 | 业务异常按语义返回（客户端 4xx / 内部故障 500）；调度器 exec 默认关闭；代码生成按上下文转义 | ruff 全过、pytest 47 passed；AST 级对抗载荷无法注入；线上验证码过期由 500 变 400 |
| 后端（复核未通过 → t14 pass） | 代码生成注入面曾**未真正关闭**：`column_type` 未安全化即进入代码位置 `mapped_column({{ sqlalchemy_type }})` | 独立复核 t12 = needs_revision；队长复现载荷原样拼入 → t13 整改（类型白名单 + 结构闸门）、t14 复审 **pass** |
| 后端（错误码收敛） | 单一事实来源：删除全部显式 `status_code`（含构造器参数），HTTP 语义只由 `RET.code → fastapi.status` 映射决定；`_DEFAULT_BUSINESS_STATUS` 降为未登记码安全网 | 业务代码中 `CustomException` 带 status_code = 0；AST 护栏（注入违规即失败）；语义探针 400/401/403/404/500 全对 |
| 后端（异常写法统一） | 删除 `CustomException.internal` 与 132 处包装：意外异常交全局处理器（5xx + 通用文案 + 日志），需运维上下文处 `logger.exception(...) + raise`；6 处 4xx→5xx 反转点补 `except CustomException: raise` | `grep CustomException.internal` = 0；构造器传 status_code 抛 TypeError；AST 审计残留 0；97 用例通过；线上验证码过期仍 400 且保留业务文案 |
| 后端（全局兜底修正） | SQLAlchemyError 非完整性错误由 400 改为 503（连接）/500（其它），文案不再拼 `exc_type` | 读码 + 探针实测 409/503/503/500/500 |
| 前端（错误文案） | 错误提示改为「后端 msg 优先 → 业务码兜底 → 状态码兜底 → 通用」，去掉按 code 白名单取文案的耦合（含 Blob 下载分支；401 排除在解析外以不影响静默续期） | type-check exit 0；vitest 41 用例（含 500+4500 与 404+404 文案断言）；成功下载分支零改动 |
| 存储适配器（类型检查暴露的运行时缺陷） | ① OSS：`Client.uploader` 是**方法**，原写法 `self.client.uploader.upload_file(...)` 在绑定方法上取属性 → 运行时 AttributeError（OSS 上传必失败）；② SFTP/FTP：`config.host` 可空却直接传给要求 `str` 的 `connect(hostname/host)` | ① 改为 `self.client.uploader().upload_file(...)`（已按 SDK 签名核对 part_size/parallel_num）；② 补主机校验，缺主机时返回 400 业务异常；basedpyright 这三个文件由 4 error → 0；运行时探针：缺主机拦截、配主机放行 |
| 类型检查校准（新增 `backend/pyrightconfig.json`） | 仓库此前无 pyright 配置，basedpyright 走自身默认：`app/` 下 247 errors / 3799 warnings，143 条是 `reportMissingTypeArgument` 泛型注解类噪音，掩盖真缺陷 | `typeCheckingMode: basic` + 显式保留能抓 bug 的规则为 error + tests/ 用 `executionEnvironments` 单独放宽 → **0 errors**；做了红绿验证：合成 `str | None` 传参、`MethodType` 属性误用、Optional 成员访问三类仍全部报 error |
| 类型检查暴露的两处真缺陷（我们上一轮引入） | ① `template_safety._SQLALCHEMY_TYPE_WHITELIST` 对全大写常量二次赋值；② 同文件 `normalize_column_type` 假定 `_TYPE_BASE_RE` 必命中（用 `# type: ignore` 盖住，None 时 `.group()` 会崩）；③ `node/service.py` 两处 `CustomException(msg=reason)` 中 `reason` 为 `str | None` → 客户端可能收到空文案 | ① 一次成型；② 改 None 安全并去掉 type-ignore；③ 新增 `SchedulerUtil.require_schedulable()` 收敛「判定 + 抛异常 + 兜底文案」，两个调用点改为一行 |

### 9.2 仍未处理（需后续立项或产品决策）

| 项 | 说明 |
| --- | --- |
| 会话失效机制 | 停用/删除/改密/撤权后旧会话仍有效（最长 7 天）——需应用侧改造 |
| 数据权限注入 | `CRUDBase` 的删除/清空/改状态路径未注入数据权限 |
| 需求规格错位 | 文档声称的 SaaS 多租户在代码中零实现 |
| Web i18n 与通知枚举 | 85/101 页面未接入 i18n；通知状态枚举与后端语义冲突 |
| 测试覆盖与夹具 | 夹具掩盖缺陷、迁移链路 0 覆盖（CI 已建立，但用例仍需补） |
| 移动端其它缺陷 | `alova.ts:115-119` 请求头写成 `ContentType`（缺连字符），修正需回归上传/表单/JSON 三类请求 |
| 凭据轮换与镜像卫生 | ① 生产口令整体轮换：MySQL 应用用户 / MySQL root / Redis（旧值实测被拒：`ERROR 1045`、`WRONGPASS`）；② 镜像不再携带任何口令：`deploy-artifacts.sh` 构建时剔除 `DATABASE_PASSWORD / REDIS_PASSWORD / SECRET_KEY / DATA_ENCRYPTION_KEY` 等键（审计 B3 根治），重建后镜像内口令行命中 0 条，应用改由 compose 注入口令且 `db_status/redis_status=1`；③ 本地 `backend/env/.env.prod` 中泄露值清空并改 600 权限 | 旧口令拒绝测试、新口令容器内连接测试、镜像内容扫描、四端 200、容器全 healthy |
| 公开仓库历史暴露（需用户侧吊销） | 仓库为 **public**，历史中真实出现过：**OpenAI API Key（35 字符 `sk-…`）**、旧 MySQL/Redis/root 口令、旧 `SECRET_KEY`、旧自签名 TLS 私钥；其余 `PAYMENT_* / EMAIL_PASSWORD / DINGDING_SECRET / MONGO_DB_PASSWORD / POSTGRESQL_PASSWORD` 等仅出现在 `.example` 占位文件 | 已消除：DB/Redis/root 口令与 `SECRET_KEY`/`DATA_ENCRYPTION_KEY` 本轮轮换（历史值即失效）；线上证书与历史私钥**不同**（指纹比对）。**待用户处理：到 OpenAI 控制台吊销该 Key**（第三方无法代办）；是否用 `git-filter-repo` 清洗历史见 §9.2 |
| 对外口径（异常统一后的取舍） | 存储「测试连接」密钥环损坏、上传/下载失败、OAuth 渠道未配置、Redis 同步失败等已由具体原因变为通用 5xx 文案（细节只在日志）。若希望管理员在界面看到可操作原因，正确做法是为这些场景定义**业务码**，而不是回到「包装意外异常」 |
| 仍可能外泄的出口 | `ValueError` 全局处理器返回 `msg=str(exc)`；建议改为通用文案 + 日志，或让我们的校验统一抛 `CustomException` |
| 静默吞异常（既有） | 48 处「记录日志但不 raise」的 best-effort 处理器（redis_crud、ap_scheduler、middlewares、discover 等），属审计「静默吞异常」主线，建议单独排一轮 |
| 仓库密钥防回归（已落地） | 新增 `.github/workflows/secrets.yml`：gitleaks **8.30.1**（固定版本 + sha256 校验）只扫描**本次变更范围**（push 用 `before..sha`，PR 用 base..head，新分支退化为 `-1`），拦住**新增**密钥；`.gitignore` 增加数据库导出规则 `backend/*.sql`、`backend/sql/**/*.sql`、`*.dump` | 本地红绿验证：干净提交 `no leaks found`（exit 0）；临时插入 `ghp_` 令牌 → 命中 `github-pat`（exit 1）；`before` 全 0 的退化分支同样正常；YAML 解析通过 |
| 历史密钥清单（gitleaks 全历史扫描） | 命中 **138 处 / 15 个提交**：`jwt` 97、`generic-api-key` 38、`private-key` 2、`curl-auth-header` 1；集中在本轮之前就已从 HEAD 删除的 `backend/sql/**/*.sql`(76+7+36) 与 `fastapi_vue3_admin.json`、旧 `backend/env/.env.dev/.env.prod`、旧 `docker/nginx/ssl/server.key` | **当前 HEAD 无真实密钥**：这些文件均已不在 HEAD（仅存在于历史）。`backend/audit-security.md:242` 的命中经核实为**误报**（长标识符，非密钥）。因历史未清洗，CI 不做全历史扫描（否则必然红） |

### 9.3 本轮产生的回滚资产

- 镜像：`backend:prev`（上一版）、`nginx:rollback-1.25`
- 配置备份：`docker-compose.yaml.bak-*`、`nginx.conf.bak-*`、`.env.bak-*`
- 静态成品备份：`backups/{web,app-h5}-<时间戳>`（每类保留 5 份）
- 种子账号新口令：服务器 `/root/.fa-seed-passwords`（600，登录后请修改并删除）

## 10. 收尾状态

**代码与部署**

- 本轮共 12 个提交（`ce940119` … 本报告提交），已推送 GitHub `master/dev` 与 gitee `gitee/dev`。
- 线上版本：后端含 t10/t11/t13/t15/t16/t19 全部修复；Web 含 t17/t18 错误文案修复；App 为 t9 修复版。
- 部署方式：本机构建成品 → 服务器只接收镜像与静态产物（服务器无源码、无构建），细节见 `DEPLOYMENT.md`。

**最终验证（部署后新跑）**

| 项 | 结果 |
| --- | --- |
| 容器 | backend / nginx / redis / mysql 全部 healthy；健康检查 exit 0 |
| 四端（公网） | `/`、`/web/`、`/app/`、`/api/v1/monitor/health/check` 均 200 |
| 接口文档 | 公网 403；仅内网白名单可访问（本机 200） |
| Host 校验 | 正确域名 200；`localhost` 400；伪造域名 400（`ALLOW_LOCALHOST_HOSTS=false`） |
| 数据面暴露 | 3306/6379/8001 无公网监听（宿主 `ss` + 服务器自连双向确认） |
| 业务语义 | 验证码过期 → 400 且保留业务文案；无令牌 → 401；内部故障 → 5xx + 通用文案（细节仅日志） |
| 密钥 | 旧公开默认密钥伪造令牌被拒；`SECRET_KEY`/`DATA_ENCRYPTION_KEY` 已注入并轮换 |
| 类型检查 | basedpyright 全量 0 errors（`backend/pyrightconfig.json`）；ruff 全绿 |
| 测试 | 后端 pytest 97 passed；Web vitest 41 passed |
| 巡检 | `fa-health-check.timer` active，日志无 ALERT |

**团队**

审计团队（7 名成员，t1–t19）已归档；本报告与 7 份分报告为全部交付物，残余项见 §9.2。
多智能体协作的**项目专属纪律**（先探测工具再选档位、审计波/交付波两种队形、审计波可复制模板、本项目踩过的版本坑、验证命令、不可逆动作规则）见 [TEAM-PLAYBOOK.md](TEAM-PLAYBOOK.md)——通用协作策略由 DSH 运行时注入，不在此重复。

**收尾后仍需人工处理（不阻塞上线）**

1. **吊销旧 OpenAI API Key**：仓库是 public，`sk-…`（35 字符）确实出现在 `backend/env/.env.prod` 的历史提交中。线上环境从未使用它（容器 env 与该键均为空、新镜像已不含任何密钥），所以风险只在于该 Key 在 OpenAI 侧可能仍有效。请到 <https://platform.openai.com/api-keys> 吊销；如需 AI 功能再签发新 Key 并只写入服务器 `.env`。
2. **曾存入存储源/接口密钥配置的第三方凭据**：历史里的数据库导出文件含 38 处 `generic-api-key` 形态命中，而旧主密钥（`DATA_ENCRYPTION_OLD_KEYS`）同样在历史的 `.env.prod` 中——若这些导出里含加密态的第三方凭据，持有历史的第三方可解密。建议按「已暴露」处理并轮换真实凭据；同时可在数据库层面清空 `DATA_ENCRYPTION_OLD_KEYS`（确认无历史密文依赖后）。
3. **是否清洗 git 历史**：`git-filter-repo` 可把历史中的 `.env*`、`.sql` 导出与旧证书整体抹除，但会重写所有 SHA（需 force-push `dev` 与 `master`，影响既有克隆与 PR 引用，且 gitee 镜像需同步）。由于相关口令已轮换、Key 将吊销，**建议以「吊销 + 轮换」为准，清洗作为可选项**；若仓库要转为对外开源，则建议执行清洗（清洗后还可把 `secrets` 工作流从「仅扫描变更范围」升级为全历史扫描）。
4. §9.2 中的产品/架构决策项（会话失效、数据权限注入、多租户规格、i18n、移动端 `ContentType`）。

