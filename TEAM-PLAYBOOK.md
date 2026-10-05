# 多智能体协作 Playbook（FastapiAdmin）

> 本文件只记录**官方插件给不了**的部分。通用协作策略由 DSH 实验性 Agent Teams 运行时自动注入
> （显式委派才建团队、共享 cwd、文件陈旧版本恢复、Bash/formatter/codegen 风险、task/write-scope 协调、
> steer 投递、mailbox 不重发、Lead 必须先等待），此处不重复。

## 1. 前置：先确认工具，再选档位

「智能体团队」组合包（插件页开关）开启时，团队工具会**取代同名的旧 subagent 控件**；关闭后恢复
`subagent` / `subagent_fork`。两者互斥，同一个开关同时控制工具与 Web 成员/任务板 UI。
因此开工第一步是**看当前会话实际有哪些委派工具**，再决定档位：

| 档位 | 适用 | 反例 |
| --- | --- | --- |
| 单会话直接做 | 单文件、≤20 行、需求明确 | 需要跨域并行探索 |
| `subagent` / `subagent_fork` | 独立小任务 / 需要本会话上下文 | 被团队组合包取代时不可用 |
| `workflow` | 几十个互不依赖的同类单元 | 需要人工逐步在环 |
| 团队（Agent Teams） | 多角色并行探索 + 质量门禁 + 可追溯 | 单文件；成员必然改同一批文件 |

判据：**任务能否切成互不重叠的单元**。能并行探索 → 用团队；只能串行改同一批文件 → 退回「1 实现 + 1 复核」。

## 2. 两种队形

### A. 审计波（只读，5–7 人）
角色覆盖端/域：后端架构、前端、测试、安全、运维、产品、UX/UI。

- 每个成员一个 `kind=work` 任务，产出「文件:行号 + 证据 + 优先级」报告
- 任务说明里写明：不得改代码、不得启动服务/装依赖、不得提交 git
- Lead 汇总总报告，并**修正成员的错误表述**——成员结论是材料，不是结论

### B. 交付波（3–4 人，带质量门禁）
`implementation`(+`repair`) → `review`(verdict=pass) → 必要时 `integration`。

- implementation 必须给全 `objective` / `acceptance` / `verify` / `inScope` / `outOfScope`；
  review 用 `reviewedTaskId` 指向被复核任务
- 失败 review 会自动加 repair + 下一轮 review，**不要手工重建循环**
- 跨端大改**分两波**：先审计波并归档，再起交付波

## 3. 本项目踩过的坑（版本相关，易复发）

1. **`inScope` 必须逐文件**：目录型条目在完成态校验里逐字匹配不上文件，成员将无法声明 `changedPaths`
2. **quality/review 任务必须显式 `assignee`**：否则调度器可能把「复核后端代码生成」派给前端工程师
3. **并行轨道按文件边界切**：两个任务碰同一文件 = 强制串行。官方不提供 confinement、也不支持独立工作目录
   （既不会拦重叠写，也不会做 worktree 隔离），所以这是唯一防线
4. **`verify` 命令先在本地跑通**；`acceptance` 不得引用不存在的基础（例：仓库里没有的「既有 401/403 用例」）
5. **review 通过 ≠ 已验证**：门禁之外保留独立验证（类型检查/测试/线上实测至少两项）；
   复核者要用对抗手段（绕过校验层构造脏数据、原始载荷重放）
6. **机械小改（≤20 行、单文件）自己动手**，不要开 implementation+review 两轮

## 4. 验证命令

```bash
# 后端
cd backend && UV_CACHE_DIR=/tmp/uv-cache-test uv run --no-sync pytest -q
cd backend && UV_CACHE_DIR=/tmp/uv-cache-test uv run --no-sync ruff check
# 前端
cd frontend/web && pnpm run type-check && pnpm run test
cd frontend/app && pnpm run type-check
```

注意：`frontend/web/src/types/*.d.ts` 由 unplugin-* 在 vite 运行时生成且**不入库**，
所以**类型检查前必须先构建**（`pnpm run build:prod`）——CI 里已按此顺序执行。

## 5. 不可逆动作（必须人确认）

部署、合并到 master、推送远端、轮换凭据、删除团队。

- 部署只走 `./deploy-artifacts.sh`（本机构建成品 → 服务器只收镜像与静态产物；服务器无源码、无构建）
- 推送只推 `origin`（GitHub）；gitee 由 GitHub 同步，不由本地推
- 凭据不进仓库（含文档与示例）；改口令用服务器上的 `/root/fa-set-password.sh`

## 6. 收尾

1. 必需任务全部终态、成员 idle；未完成工作不得丢弃（先问用户）
2. 逐条核对成员交接（`changedPaths` / `commandsRun` / `acceptanceResults`），关键命令自己复跑
3. 交付物落入仓库并提交（走 dev → master PR）
4. 归档团队，并向用户说明覆盖缺口与残余项

## 7. 审计波模板（可直接复制）

插件不提供预置队形，因此把审计波的 roster 与任务写成模板，省掉每次手工列角色：

```text
create({ approval: "required", description: "<本次目标>", plan: {
  members: [
    { name: "后端架构师",   role: "backend architect" },
    { name: "前端工程师",   role: "frontend engineer" },
    { name: "测试工程师",   role: "QA engineer" },
    { name: "安全审计员",   role: "security auditor" },
    { name: "运维工程师",   role: "devops / deployment" },
    { name: "产品经理",     role: "requirements coverage" },
    { name: "UX/UI 工程师", role: "UX + UI reviewer" }
  ],
  tasks: [ // 七个 kind=work 只读任务，各自写一份报告文件；均不可改代码/启服务/提交
    { id: "a1", subject: "后端架构与代码质量审计", assignee: "后端架构师",   description: "只读；产出 backend/audit-backend.md（文件:行号 + 证据 + 优先级）" },
    { id: "a2", subject: "前端与移动端审计",       assignee: "前端工程师",   description: "只读；产出 frontend/audit-frontend.md" },
    { id: "a3", subject: "测试与可验证性审计",     assignee: "测试工程师",   description: "只读；产出 backend/audit-testing.md（含实跑结果）" },
    { id: "a4", subject: "安全审计",               assignee: "安全审计员",   description: "只读；产出 backend/audit-security.md" },
    { id: "a5", subject: "Docker 与部署审计",      assignee: "运维工程师",   description: "只读；产出 docker/audit-deploy.md" },
    { id: "a6", subject: "需求覆盖审计",           assignee: "产品经理",     description: "只读；产出 backend/audit-requirements.md" },
    { id: "a7", subject: "UX/UI 审计",             assignee: "UX/UI 工程师", description: "只读；产出 frontend/audit-uxui.md" }
  ]
}})
```
要点：7 名成员 = 插件的 `maxMembers: 8` 上限内留 1 个余量；报告文件名先约定好，避免成员互相覆盖同一文件。
若要更多角色（如移动端、性能单列），需先把 profile 的 `cordis.patch.yml` 里 `maxMembers` 调大（改后需重载 GUI）。

## 8. 参考：官方文档在本地

```
…/app.asar.unpacked/node_modules/@deepseek-ai/
  dsh-experimental-agent-team/README.zh.md          # 领域服务：roster / mailbox / 任务板 / 持久性
  dsh-experimental-agent-team-profile/README.zh.md  # 组合包：插件页开关、限额（maxMembers=8 等）
  dsh-experimental-tool-agent-team/README.zh.md     # 9 个工具与内建共享策略
  dsh-experimental-client-ui-agent-team/README.zh.md# Web 成员列表 / 任务看板
```
