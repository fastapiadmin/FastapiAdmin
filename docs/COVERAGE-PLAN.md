# 覆盖率目标与基线（A：支持范围口径）

## 当前基线

| 口径 | 当前值 | 说明 |
|---|---:|---|
| 后端 pytest | **864 passed**（含真实集成） | 全量 pytest，覆盖 15,603 statements（已剔除无服务协议） |
| 后端行覆盖 | **80%**（3,188 missed） | `pytest --cov=app`，口径仅支持范围 |
| 前端 vitest | **94 passed** | 14 个测试文件 |
| 前端行覆盖 | 未启用 all-source | 不能当全站覆盖率，暂不作为验收口径 |
| 接口 | 250 个 | 还没有做到每个接口成功/校验/权限三路径 |
| Web 路由 | 31 个 | 已有只读巡检，写路径未全覆盖 |

## 100% 的定义

A（支持范围）包含四个独立目标：

1. **功能测试点 100%**：每条需求/字段/状态/权限组合都有用例并通过；
2. **接口/页面 100%**：250 个接口 × 成功/参数校验/未登录/无权限；31 个页面 × 关键交互；
3. **代码行/分支 100%**：后端 `pytest-cov`、前端 `vitest --coverage` 全源码；
4. **外部集成 100%**：仅 MinIO/S3、AI、SSH 使用真实测试环境；FTP/SFTP/OBS/OSS/COS 无服务，已从覆盖率分母剔除。

## 本轮新增（2026-11-05）

- `tests/test_string_util.py`：StringUtil 分支覆盖 100%；
- `tests/test_utils_coverage.py`：banner 100%、password 99%、excel 95%；
- `tests/test_common_util_coverage.py`：common_util 68%；
- 新增后相关测试 19 passed；
- `test_security_utils_coverage.py`：ai_factory 100%、lazy_sdk 100%、crypto 97%；
- `test_local_storage_adapter.py`：本地存储上传/下载/复制/删除/目录/路径穿越，local_adapter 72%、base 75%；
- `test_s3_adapter_paths.py`：S3 连接/列表/桶/复制/重命名/URL/关闭，s3_adapter 53%；
- `test_storage_browse_service.py`：路径校验/上传/下载/删除/列表/重命名/目录/分享，browse service 58%；
- `test_transfer_engine_helpers.py`：本地大小/文件树/目录准备/临时清理/目录判断/步骤正交，transfer engine 26%；
- `test_monitor_services.py`：缓存服务 100%、服务器监控 75%；
- `test_workflow_graph_service.py`：画布拆分、去重、源目标派生、非法连线，workflow service 39%；
- `test_online_service.py`：在线列表/搜索/清理/趋势，online service 81%；修复搜索参数把 str 当 tuple、趋势少算今天的问题；
- 监控服务补充本地 IP 成功/降级、Python 进程信息、汇总调用，server/cache service 均 100%；
- online service 补充 dashboard 统计、空 token/缺失会话处理，98%；
- transfer service 补充本地临时文件清理；
- transfer engine 补充单文件步骤成功/源缺失失败、后台无步骤失败、成功结束，63%；
- workflow service 补充明细保存、画布组装、流程执行/禁用/缺失路径、CRUD/分页，51%；
- transfer service 补充取消 pending/running、删除清理，43%；
- 监控控制器补充服务器信息/健康检查/SSE，health controller 96%、server controller 100%；
- base_crud 补充条件操作符/排序/预加载分支；
- 登录/验证码服务补充权限收集、限流、会话、验证码状态/来源校验，auth service 44%；
- 用户服务补充性别映射、导入模板、导出、空/损坏/缺列 Excel，user service 25%；
- 代码生成器补充类型映射/命名/长度拆分/表初始化/列推断/主键约束，gen_util 80%；
- 生成器静态规则补充路由首段/目录键/主子表校验/主键选择，gencode service 16%；
- 生成器预览补充不存在/正常模板渲染，gencode service 20%；
- 生成器同步补充差异计算/错误/正常预览；
- 生成写入补充表名/模块名/功能名前置校验；
- 生成器工具补充 HTML/查询类型推断，gen_util 89%；
- 上传工具补充文件名安全、类型检测、大小/时间戳/随机码、路径安全，upload_util 74%；
- IP/XSS 工具补充代理链、归属地降级、HTML 清洗，ip_local 87%、xss 100%；
- 模型扫描工具补充根目录/模型有效性/真实模型扫描，import_util 80%；
- 调度器补充可调度性/内置处理器注册/不可调度任务日志；
- 用户服务补充创建/更新重名/重手机/重邮箱、删除保护，user service 30%；
- 调度器补充 job id/触发类型/状态/事件分发，ap_scheduler 46%；
- AI 补充动作解析/导航建议/工具开关/模型配置，ai chat service 33%；
- 认证补充 token 创建/刷新轮换/重放撤销/登出，auth service 48%；
- 用户补充改密/重置/忘记密码/注册，user service 30%；
- 字典/菜单补充缓存回退、缓存刷新、父子类型/可见范围校验，dict service 28%、menu service 36%；
- 角色补充创建/更新/删除/批量状态/导出，role service 65%；
- AI 会话 CRUD 补充分页/标题搜索/创建/重命名/删除；顺带修复 order_by 解包 bug；
- OAuth 补充回调域名/前端重定向/凭证校验/四平台授权 URL，oauth service 31%；
- RedisCURD 补充基础读写/过期/扫描/清理/哈希，redis_crud 71%；
- 微信小程序补充凭证/错误映射/登录名/access_token 缓存，wx_mini 45%；
- 调度器补充任务包装/代码块开关/状态序列化，ap_scheduler 55%；
- 角色补充权限设置/角色加载/菜单部门关联，role service 91%；
- 菜单补充 CRUD/树/批量启停，menu service 77%；
- 字典类型补充创建/更新/级联/删除保护，dict service 39%；
- 字典数据补充创建/更新/删除，dict service 覆盖继续提升；
- 生成器补充业务表/物理表分页、字段读取、表导入，gencode service 26%；
- 健康检查补充 DB/Redis 成功/失败/空连接，health service 100%；
- 用户补充轻量当前信息、资料更新重手机、批量状态保护，user service 37%；
- 传输补充取消、软删除中止分支，transfer engine 68%。
- 存储基类补充端点规范化/密码加解密/高级配置/字段元数据；
- 存储工厂补充非法协议拒绝和本地适配器创建，factory 100%。

## 真实 DB/Redis 集成测试（2026-11-09）

- 本机 PostgreSQL `localhost:5432`、Redis `localhost:6379` 已启动；
- 测试库：`fastapiadmin_test`（不写生产库）；
- 文件：`backend/tests/test_integration_pg_redis.py`；
- 默认套件跳过，需显式开启：

```bash
cd backend
RUN_INTEGRATION=1 TEST_DB_TYPE=postgres TEST_DB_USER=root \
TEST_DB_PASSWORD=*** TEST_DB_NAME=fastapiadmin_test \
uv run pytest -q tests/test_integration_pg_redis.py
```

- 当前覆盖：`SELECT 1`、用户 CRUD 往返、显式 NULL 更新、分页、唯一约束回滚、Redis set/get/ttl/delete；
- 服务层：角色创建/更新/分页/删除、角色重名、用户创建/详情/更新/分页/删除、用户重名；
- RedisCURD：set/get/delete、expire/ttl、lock/unlock、compare_and_set、scan/mget、hash；
- 当前真实集成 **94 passed**（PG 基础 6、RedisCURD 6、服务与角色关联 6、认证会话 4、账号密码登录 4、gencode 5、调度器自愈 3、字典 3、菜单 4、AI 配置 5、存储源 3、文件浏览 3、AI 会话 5、Excel 导入 3、传输端到端 4、工单 4、数据库控制台 4、AI 接口 4、数据权限 4、部门 4、示例插件接口 3、公告 2、系统参数 4）；
- 后续把调度器、认证会话、gencode 同步迁到真实 DB/Redis 验证。

## 范围口径 A（2026-11-09 确认）

- 验收目标改为“支持范围内 100%”，不再要求全仓 100%；
- `pyproject.toml` 的 `[tool.coverage.run] omit` 已剔除：
  - `ftp_ftps_adapter.py`
  - `sftp_adapter.py`
  - `obs_adapter.py`
  - `oss_adapter.py`
  - `cos_adapter.py`
- 剔除后分母 15,579 行，当前覆盖 74%（4,063 未覆盖）；
- 工厂、懒加载、安全校验等与协议无关的逻辑仍在统计内；
- 将来提供这些协议的真实服务后，再移除 omit 并补集成测试。

## 外部协议范围（2026-11-05 确认）

- 当前只有 **MinIO S3** 可用；
- FTP/FTPS、SFTP、OBS、OSS、COS 没有可用测试服务，**不纳入本轮集成 100%**；
- 对应适配器不做真实协议验证，只保留现有懒加载/工厂/安全单测；
- 覆盖率统计若包含这些适配器，必须标记为“环境不可用”，不能伪装成真实通过；
- 将来提供对应测试服务后，再补真实连接、上传/下载/删除、异常和分片测试。

## 测试过程中发现并已修复的问题

| 问题 | 修复 |
|---|---|
| 在线用户搜索把 `str` 当 tuple 使用 | 兼容 `str` 与旧 tuple 写法 |
| 7 天登录趋势实际少算今天 | 起点改为 6 天前 |
| AI 会话 `order_by` 对字典错误解包 | 改为 `next(iter(order_by[0].items()))` |
| 用户导入异常缺少 `except CustomException: raise` 守卫 | 补守卫，避免业务异常被二次包装 |
| 前端 `node_modules` 被 npm 临时安装污染，出现 60 个假类型错误 | 按 `pnpm-lock.yaml` 冻结重装，`vue-tsc` 恢复 0 错误 |
| 部署脚本重复（deploy.sh / deploy-artifacts.sh） | 合并为统一 `deploy.sh`，文档同步 |
| 代码生成新增字段重复传 `table_id`，新增列必然 TypeError | 字段 dump 排除 `table_id`，由外层统一传 |
| 目录复制目标带尾斜杠时生成 `dst//sub` 双斜杠 key | `_sync_copy_dir` 对 dst 去尾斜杠 |
| JWT 无唯一标识，同一秒内登录/刷新会生成完全相同的 access/refresh token，刷新轮换与重放检测失效 | `JWTPayloadSchema` 增加 `jti`，登录与刷新均写入 `uuid4` |
| gencode 重复同步时既有字段未取到，重复插入字段（2 列同步两次变 4 条） | 预加载为空时按 `table_id` 兜底查询现有字段，再做匹配更新 |
| 字典类型编码重复时直接撞数据库唯一约束，返回 500 而非业务错误 | 创建前增加 `dict_type` 查重，返回“字典编码已存在” |
| 更新用户时传 `role_ids=[]` / `position_ids=[]` 实际不清空关联 | 更新路径新增 `clear_when_empty=True`，显式清空；创建/导入路径保持 no-op |

## 现实约束

- 后端当前还有 4,063 行未被测试覆盖，包含 gencode、调度器、传输引擎、工作流、监控、初始化、工具函数等；
- 前端若开启 `coverage.all`，大量 views/components/hooks 会进入统计；
- FTP/SFTP/OBS/OSS/COS 适配器已从 coverage 分母剔除，只保留工厂/懒加载逻辑测试；提供真实服务后再恢复统计。
- 100% 代码覆盖不能替代功能验收，反之亦然。

## 执行顺序

1. 固定功能清单与接口/页面 traceability matrix；
2. 后端按模块补测试：权限/认证 → 存储/传输 → 调度 → SQL/SSH → 生成器/AI → 监控/工具；
3. 前端按页面补交互与异常分支；
4. 接入覆盖率门禁：先记录基线，逐模块提高，达到目标后再设为 100%；
5. 外部集成仅 MinIO/S3 进入验收；无服务协议在矩阵中标记为排除，不进入覆盖率分母。

## 命令

```bash
cd backend && uv run pytest -q --cov=app --cov-report=term-missing
cd frontend/web && pnpm exec vitest run --coverage
```
