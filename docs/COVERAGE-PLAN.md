# 覆盖率目标与基线（D：全部口径）

## 当前基线

| 口径 | 当前值 | 说明 |
|---|---:|---|
| 后端 pytest | 351 passed | 全量 pytest，覆盖 16,661 statements |
| 后端行覆盖 | **50%**（8,327 missed） | `pytest --cov=app` |
| 前端 vitest | 41 passed | 现有 3 个测试文件 |
| 前端行覆盖 | **61.73%**（仅被 import 的文件） | 尚未启用 all-source 统计，不能当全站覆盖率 |
| 接口 | 250 个 | 还没有做到每个接口成功/校验/权限三路径 |
| Web 路由 | 31 个 | 已有只读巡检，写路径未全覆盖 |

## 100% 的定义

D 包含四个独立目标：

1. **功能测试点 100%**：每条需求/字段/状态/权限组合都有用例并通过；
2. **接口/页面 100%**：250 个接口 × 成功/参数校验/未登录/无权限；31 个页面 × 关键交互；
3. **代码行/分支 100%**：后端 `pytest-cov`、前端 `vitest --coverage` 全源码；
4. **外部集成 100%**：FTP/SFTP/OBS/OSS/COS、AI、SSH 使用真实测试环境。

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
- transfer service 补充本地临时文件清理。

## 外部协议范围（2026-11-05 确认）

- 当前只有 **MinIO S3** 可用；
- FTP/FTPS、SFTP、OBS、OSS、COS 没有可用测试服务，**不纳入本轮集成 100%**；
- 对应适配器不做真实协议验证，只保留现有懒加载/工厂/安全单测；
- 覆盖率统计若包含这些适配器，必须标记为“环境不可用”，不能伪装成真实通过；
- 将来提供对应测试服务后，再补真实连接、上传/下载/删除、异常和分片测试。

## 现实约束

- 后端当前还有约 8,300 行未被测试覆盖，包含存储 FTP/SFTP、传输引擎、工作流、监控、初始化、工具函数等；
- 前端若开启 `coverage.all`，大量 views/components/hooks 会进入统计；
- 外部协议和第三方服务没有测试环境时，mock 只能算逻辑覆盖，不能算集成 100%；
- 100% 代码覆盖不能替代功能验收，反之亦然。

## 执行顺序

1. 固定功能清单与接口/页面 traceability matrix；
2. 后端按模块补测试：权限/认证 → 存储/传输 → 调度 → SQL/SSH → 生成器/AI → 监控/工具；
3. 前端按页面补交互与异常分支；
4. 接入覆盖率门禁：先记录基线，逐模块提高，达到目标后再设为 100%；
5. 外部集成接入真实测试环境；无环境的项必须在矩阵中标记为 mock，不算 100%。

## 命令

```bash
cd backend && uv run pytest -q --cov=app --cov-report=term-missing
cd frontend/web && pnpm exec vitest run --coverage
```
