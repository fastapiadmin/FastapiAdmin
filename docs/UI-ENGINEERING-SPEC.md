# FastapiAdmin Web UI 工程规范

> 版本 v1.0 · 2026-11 · 适用 `frontend/web`（Vue 3 + Element Plus + Tailwind v4）
>
> 配套文档：[`DESIGN-SPEC.md`](./DESIGN-SPEC.md)（品牌与视觉）、[`design/tokens.json`](../design/tokens.json)（token 源）。
> 本文是**工程契约**：评审时以本文判断实现是否合格；视觉气质、Logo、品牌色以 `DESIGN-SPEC.md` 为准。两份文档冲突时，工程实现以本文为准，并回改 `DESIGN-SPEC.md`，不保留两套说法。

## 0. 适用范围与原则

适用于管理端所有页面、共享组件、弹窗/抽屉、列表、表单、空/错/加载状态与响应式布局。三条底线：

1. **一套 token**：颜色、字号、间距、圆角、阴影不在页面里另起一套。
2. **一个状态闭环**：加载、空、失败、重试、无权限都要有明确落点，不能静默失败。
3. **一个主操作**：每个区域只有一个主按钮；危险操作必须二次确认。

新增页面按本文从零实现；修改旧页面时，至少让**本次改动的区域**符合本文，不做无关的全页重写。

## 1. Token 与主题

### 1.1 单一来源

| 层 | 位置 | 规则 |
| --- | --- | --- |
| 设计源 | `design/tokens.json` | 品牌色、圆角、间距、字号、阴影、控件高度的唯一来源 |
| 生成产物 | `frontend/web/src/styles/core/_brand-tokens.generated.scss`、`frontend/app/...`、`frontend/docs/...` | **禁止手改**；改源后运行生成脚本 |
| Web 语义补充 | `frontend/web/src/styles/core/_tokens.scss` | 只放生成文件未覆盖的 surface/text/icon/terminal/empty 语义；不得重复定义 radius/space/font/shadow |
| 工具类映射 | `frontend/web/src/styles/tailwind.css` 的 `@theme` | 把字号、颜色映射成 `text-*` / `bg-*`；新增档位必须同时有设计值 |
| 组件变量 | Element Plus `--el-*` | 只通过主题变量覆盖，不在业务页写 EP 内部色值 |

生成命令（在仓库根目录）：

```bash
node scripts/design-tokens/generate.mjs
```

改完 token 必须检查生成 diff，三端（web/app/docs）应同步变化；只改 Web 生成文件属于违规。

### 1.2 使用层级

按优先级从高到低使用：

1. 语义 class：`text-g-700`、`bg-(--default-box-color)`、`border-(--default-border)`、`text-(--el-color-danger)`。
2. 语义变量：`var(--fa-text-1)`、`var(--fa-border)`、`var(--fa-radius-md)`。
3. Element Plus 变量：`var(--el-color-primary)`、`var(--el-text-color-secondary)`。
4. 原始色值：仅品牌 Logo、品牌插画、图表系列色允许；业务 UI 禁止。

主题色可切换（7 套），所以**禁止**把 `#409eff`、`#909399`、`#f56c6c`、`#e6a23c` 写进模板；需要语义时用 `--el-color-*`，需要中性色时用 `g-*`/`--fa-gray-*`。

### 1.3 字号、间距、圆角

| 类别 | 可用值 | 说明 |
| --- | --- | --- |
| 字号 | 11 / 12 / 13 / 14 / 15 / 18 / 22 / 28 | 正文 14（`text-md`）；紧凑表格/次要信息 13（`text-base`）；辅助 12（`text-sm`）；微型标签 11（`text-xs`） |
| 间距 | 4 / 8 / 12 / 16 / 20 / 24 | Tailwind `gap-1..6`、`p-*` 对应；禁止 5/7/9/10/14/18px 等随手值 |
| 圆角 | 6 / 8 / 12 / 16 / pill | 卡片 12；输入/按钮 8；小标签 6；胶囊用 pill |
| 阴影 | `--fa-shadow-card/pop/modal` | 卡片极轻；浮层用 pop；弹窗用 modal；不叠加自定义阴影 |

`text-md` 已在 `tailwind.css` 注册为 14px。页面正文优先 `text-md`，不要再用 `text-[14px]`；`text-[Npx]` 只允许在一次性图表/画布内使用并注明原因。

### 1.4 暗色模式

- 页面只能消费语义 token；`html.dark` 下由生成文件切换 `--fa-surface/border/text/shadow`。
- 不允许用 `dark:` 为同一个语义再写一套十六进制颜色；`dark:` 只用于布局/透明度等确有必要处。
- 新增颜色必须同时在浅色和深色下检查对比度；正文对比度 ≥ 4.5:1，大字号/图标 ≥ 3:1。
- 禁止 `opacity` 当禁用色、禁止纯黑 `#000` 大面积背景、禁止在深色下用浅色卡片阴影。

## 2. 页面框架

### 2.1 骨架

```vue
<div class="fa-full-height flex flex-col gap-4 p-4">
  <!-- 页面级工具栏：FaTableHeader 或业务标题栏 -->
  <!-- 内容卡片 -->
</div>
```

- 内容区统一内边距 16px；页面不重复画大标题，标题由面包屑/顶栏承担。
- 一级容器用 `fa-full-height`，保证表格/工作区能撑满并内部滚动。
- 页面区块间距 16；卡片内元素 8/12；表单项 16。
- 禁止卡片套卡片、双层边框、双层阴影；表格/列表直接放在卡片表面。

### 2.2 列表页标准结构

```text
FaTableHeader（左：新增/导入/导出/批删/更多；右：列设置/刷新/搜索）
FaTable（loading / error / data / pagination / 列配置）
FaDialog 或 FaDrawer（新建/编辑/详情）
```

- 工具栏和表格同宽；分页在卡片底部右侧。
- 新增是主按钮（solid primary）；导入/导出/批删/更多用 plain 或默认按钮。
- 搜索栏用 `FaSearchBar`，高级项默认收起；`Ctrl/Cmd + Enter` 触发搜索。
- 列表页必须把 `useTable()` 的 `error` 传给 `FaTable`，并提供 `@retry`。

### 2.3 主从工作区

统一使用 `FaWorkbench` + `FaSidePanel`：

```vue
<FaWorkbench :side-width="260">
  <template #side>...</template>
  ...
</FaWorkbench>
```

- 左右两张独立卡片，间距 **16px**；**固定宽度，不提供拖拽手柄/分割线/`col-resize`**。
- 左栏宽度按页面配置：字典 380、用户 260、参数 240、文件浏览 216。
- `≤1024px` 自动上下堆叠，上栏高度由 `side-height` 控制（默认 320）。
- 左栏自己滚动；右侧内容区 `min-width: 0`，禁止把页面撑出横向滚动。

> 该条与旧版 `DESIGN-SPEC.md` §2.3 的“12px 热区/可拖拽”冲突，已按当前实现统一为固定 16px；不要再按旧描述新增拖拽。

### 2.4 首页/仪表盘

- 主区 16 列、信息栏 8 列，`gutter=16`；同一行卡片等高。
- 首屏必须有加载骨架；接口失败要有错误条/重试，不允许把失败渲染成 0 或空图表。
- 统计数字用 `tabular-nums`，千分位；单位与口径写在标题/说明里。
- 快捷链接：固定 2 行 × 4 列，单项为正方形（宽度取 `min(100%, 80px)`，`aspect-ratio: 1`），最多展示 8 个，不出现横向或纵向滚动；超出部分在标题右侧显示“N 个未展示”提示。
- 快捷链接悬浮：使用 7% 主色混合背景 + 18% 边框，不用纯灰块；移除按钮 24px 命中区并二次确认，禁止 hover 即删除。

### 2.5 监控看板

适用于服务器监控、缓存监控等实时性页面，结构固定为「状态条 → KPI → 资源详情 → 次要元数据」：

- 状态条：健康点 + 运行状态标签 + 节点/版本/端口摘要；右侧放「更新于 HH:mm:ss」、自动刷新开关、手动刷新。
- KPI：4 个当前最关键指标，指标值 + 单位 + 口径说明；百分比必须有真实上限，禁止用固定 `max=1000` 之类的假量程。
- 资源详情：CPU/内存用环形进度，磁盘按使用率降序表格；阈值统一为 `<60%` 正常、`60–80%` 警告、`>80%` 危险，颜色必须同时有文字标签。
- 缓存监控额外展示 Key 数、已用内存/上限、客户端连接、实时网络 I/O；未设置 `maxmemory` 时显示说明，不画无意义的内存仪表盘。
- 缓存管理主界面只保留「业务缓存」，按「缓存对象 → 键名 → 内容」三栏浏览；键空间是排障用的高级工具，从右上角「键空间」打开抽屉，不再和业务缓存平级、不占一级视图。抽屉内保留逻辑库、模式、SCAN/加载更多与只读脱敏提示，键详情复用同一套 JSON/TEXT 代码查看器。
- 缓存对象、键名这类主数据列表用轻量列表承载，不套表格：名称和备注单行省略、左对齐，删除操作固定在行尾；无数据时整块展示空状态，不保留表格底线或固定空白高度。
- 缓存内容按原始值自动识别格式：可解析为对象/数组时用只读 JSON 树（行号、折叠、长度），否则按纯文本展示；顶部显示 `JSON` / `TEXT` / `EMPTY` 格式标签、大小与行数，并提供复制。纯文本默认自动换行，允许切换为不换行横向滚动；不要在内容区使用看起来可编辑的 textarea。
- 自动刷新默认 30s，仅在页面可见且当前 Tab 激活时请求；静默刷新不弹 toast，失败要保留上次数据并显示错误条。
- 次要信息（节点信息、Python 环境、实例概览）放在页面底部，不与资源指标争夺首屏。

## 3. 表格契约

### 3.1 列

- 选择列宽 48，序号列 56；时间列 `YYYY-MM-DD` 120、`YYYY-MM-DD HH:mm` 150；带秒只用于详情/日志。
- 文本列必须 `showOverflowTooltip` 或 `minWidth`，不得撑破容器。
- 状态列统一走 `resolveStatusColumns` / `FaStatusTag`，同一状态全站同色同文案。
- 表格列配置集中在 `columnsFactory`，不在模板里堆 `ElTableColumn`。

### 3.2 操作列

- `prop="operation"`、`label="操作"`、`fixed="right"`、`align="center"`、`class-name="operation-column"`。
- 统一用 `renderTableOperationCell` 渲染；外层默认 `inline-flex items-center justify-center gap-1 whitespace-nowrap`。
- 默认宽度 180–200；只有 1 个图标按钮的紧凑页面可用 120–160，但同页必须统一。
- 超过 2 个次操作折叠为 `FaButtonMore`；删除永远单独可见且 `type="danger"`。
- 不允许操作列不固定、换行、右对齐漂移或在单元格里塞自定义下拉。

### 3.3 状态

`FaTable` 内部已处理：

| 状态 | 表现 |
| --- | --- |
| 首次加载 | 骨架屏（`loading && isEmpty`） |
| 刷新 | 保留旧数据 + 表格 loading，不闪空 |
| 空 | 统一空状态：图标 + 标题 + 一句说明 + 可选主操作；默认标题走 `common.noData`，领域空态可覆盖 |
| 失败 | `error && isEmpty` → 错误图标 + `common.loadFailed` + 后端 message + 重试按钮；`role="alert"` |

标准绑定：

```vue
<FaTable
  :loading="loading"
  :error="error"
  :data="data"
  :columns="columns"
  :pagination="pagination"
  @retry="getData"
/>
```

- `ElTable` 没有 `loading` prop；不要写 `:loading` 到 `ElTable`/`ElCard`。用 `FaTable` 的 `loading` 或 `v-loading`。
- 自定义移动端卡片列表必须自己补错误态和重试，不能只依赖桌面表格。
- 失败时如果已有旧数据，保留旧数据并 toast；不要清空成“暂无数据”。

### 3.4 移动端卡片

- `≤800px` 优先使用 `FaTable` 的 `mobile-cards`；标题列 + 操作列 + 2 列字段摘要。
- 长文本字段（时间、路径、描述）跨 2 列；操作按钮在卡片底部，不换行溢出。
- 分页精简为上一页/页码/下一页；保留总数。

## 4. 表单契约

### 4.1 布局

- 统一用 `FaForm`，24 栅格；默认 `span=6`（4 列），业务表单按信息密度显式设置。
- 桌面表单推荐 **2 列**：`span=12`；长文本、编辑器、路径、描述用 `span=24`。
- 标签默认右对齐、宽 96px；窄屏 `md` 以下自动单列。
- 输入框不得只靠 placeholder 表达含义；没有可见 label 时必须 `aria-label`。
- 校验信息 12px、紧贴控件；提交失败聚焦第一个错误字段。

### 4.2 对话框 / 抽屉

| 场景 | 组件 | 尺寸 |
| --- | --- | --- |
| 确认、轻量提示 | `ElMessageBox` / `FaDialog size="sm"` | 480 |
| 3–8 个字段的 CRUD | `FaDialog size="lg"` | 720，2 列 |
| 字段多、需要对照页面 | `FaDialog size="xl"` | 900，2–4 列 |
| 上下文编辑、长表单 | `FaDrawer` | 480–560，单列 |

- 表单型弹窗底部固定：取消在左、提交在右；`formMode` 驱动按钮，不手写两套 footer。
- 详情弹窗只读，底部只保留关闭；长内容用内部 `ElScrollbar` 固定最大高度（公告 280、版本 260、工单内容/回复 140、评论 180、会话消息 300、传输步骤 300、流程来源/目标 140、任务结果/错误 160）。
- **弹窗自身不出现 body 滚动条**；内容区滚动，标题/底部固定。
- 关闭前有未保存修改时二次确认；提交中禁用关闭/重复提交。

### 4.3 操作与反馈

- 一个区域一个主按钮；删除用 danger + `ElMessageBox.confirm` 或 `ElPopconfirm`。
- 提交成功 toast + 关闭 + 刷新列表；失败保留弹窗、展示后端 message。
- 批量和行内操作都要 loading，防重复点击。
- 状态变更必须发明确动作（发布/转草稿/归档），不要用“启用/停用”模糊文案套在公告等有业务语义的状态上。

## 5. 反馈状态

每个异步区域至少覆盖：

1. **loading**：首屏骨架；局部 `v-loading`；按钮 loading。
2. **empty**：`FaEmptyState`，标题说明“为什么空/下一步做什么”，不要只写“暂无数据”。
3. **error**：持久错误态 + 原因 + 重试；toast 只做瞬时补充。
4. **success**：toast 或状态标签，不弹阻塞对话框。
5. **permission**：无权限时隐藏入口或展示无权限说明，不静默 403。

禁止：`catch {}` 后不提示、失败后显示 0/“-”/“不存在”、失败后仍渲染空状态、用 `console.error` 代替用户反馈。

## 6. 可访问性（A11y）

- 所有图标按钮必须有 `aria-label` 或可见文字；纯图标链接同理。
- 表单控件有 `<label>`；没有可见 label 时 `aria-label` 必填。
- 可点击的 `div/span/li/td` 必须 `role="button"`、`tabindex="0"`、`@keydown.enter`、`@keydown.space.prevent`；能用 `button` 就不用 div。
- 焦点可见：使用 `:focus-visible` 环，禁止全局 `outline: none` 无替代。
- 弹窗打开后焦点进入弹窗，关闭后回到触发元素（Element Plus 默认行为不要破坏）。
- 状态不能只靠颜色；必须同时有文字/图标。
- 图片有 `alt`；装饰图 `alt=""`。
- 动画尊重 `prefers-reduced-motion`；加载动画不阻塞读屏。

## 7. 响应式

| 断点 | 规则 |
| --- | --- |
| `>1024` | 主从左右布局；表格完整列 |
| `≤1024` | 工作区上下堆叠；首页保持 16/8 栏；Banner 隐藏插画 |
| `≤800` | 侧边栏抽屉；表格转移动卡片；弹窗全宽或接近全宽；分页精简 |

- 唯一移动断点：`MOBILE_BREAKPOINT = 800`（`@utils/constants/definitions`）。
- 任何页面不得出现页面级横向滚动；表格横向滚动时操作列必须固定。
- 1280 / 800 两档必须实际检查，不只看 CSS。

## 8. 文案与 i18n

- 新增/修改的界面文案必须走 `$t()`，同时补 `zh.json` 与 `en.json`，键保持一致；禁止只补一端。
- 状态文案集中映射（如公告 0 草稿 / 1 已发布 / 2 已归档），页面、移动端、详情、筛选共用同一语义。
- 日期、数字、文件大小用共享格式化函数；不在模板里手拼。
- 空态、错误、确认文案要说明对象和后果，例如“确定将选中的 3 条公告转为草稿吗？”，不用“确定吗？”。

## 9. 评审清单（PR 必过）

- [ ] 颜色/字号/间距/圆角来自 token 或语义 class，无新增裸十六进制/`text-[Npx]`
- [ ] 列表有 loading / empty / error+retry；`error` 已从 `useTable` 接到 `FaTable`
- [ ] 操作列 `operation/fixed=right/center/nowrap`，使用共享操作单元格
- [ ] 表单 2 列或明确全宽；无 placeholder-only 字段；无 label 时有 `aria-label`
- [ ] 弹窗无 body 滚动条；长内容内部滚动；底部按钮固定
- [ ] 危险操作二次确认；批量操作有 loading 和结果反馈
- [ ] 图标按钮有可访问名；可点击 div 有键盘支持
- [ ] 1280 / 800、浅色/深色实际检查；无页面横向滚动
- [ ] 新文案同时补 zh/en；状态语义与后端一致
- [ ] `pnpm type-check`、`pnpm test`、`pnpm build` 通过

## 10. 验收命令

```bash
cd frontend/web
pnpm type-check
pnpm test
pnpm build
```

改了 token 时，先在仓库根目录执行：

```bash
node scripts/design-tokens/generate.mjs
```

`pnpm build` 已包含 `vue-tsc --noEmit`，但评审仍要求单独跑 `type-check`，便于定位。`pnpm lint` 会写文件，提交前按需执行，不要把它当作唯一验证。

## 11. 已知历史债务（不在本次改动中伪装完成）

以下问题已确认存在，属于后续专项，不应在评审时声称“已规范”：

- Web 仍有大量页面模板硬编码中文，i18n 迁移未完成；本次只保证新增/修改文案遵守第 8 节。
- 部分旧列表页尚未接 `error`/`retry`；`FaTable` 已具备能力，逐页迁移。
- 仍有绕过 token 的硬编码色、`text-[Npx]`、可点击 `div`、无 label 表单和无可访问名图标按钮；新增代码不得扩大这些数量。
- 监控/缓存、参数、工单评论等页面已确认存在静默失败或无效 loading 的历史实现，修复时按第 3、5 节落地并补测试。
- `DESIGN-SPEC.md` 旧版 §2.3 与 §11 对工作区描述冲突，本文按“固定 16px、不可拖拽”统一；旧文档应同步修改，不再引用旧描述。
