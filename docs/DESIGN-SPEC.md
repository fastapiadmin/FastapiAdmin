# FastapiAdmin 设计规范（品牌 + 界面）

> 本文件合并原 `docs/BRAND-SPEC.md` 与 `docs/UI-SPEC.md`，作为品牌与界面的唯一规范来源。

## 品牌规范

> 版本 v2.0 · 2026-10
> 适用范围：产品界面、官网/文档、演示材料、应用图标。
> 配套：[界面规范](#界面规范)· 资源目录：[docs/brand](./brand)

## 1. 品牌核心

| 项 | 内容 |
| --- | --- |
| 品牌名 | **FastapiAdmin**（中文语境可简称「FA 后台」） |
| 写法 | 固定为 `FastapiAdmin`；不写 `FastAPIAdmin`、`Fastapi Admin`、`FAadmin` |
| 定位 | 面向开发者的现代化 FastAPI 管理后台：开箱即用，也经得起长期维护 |
| 品牌关键词 | 快速 · 秩序 · 克制 · 可靠 · 现代 |
| 品牌主张 | **Fast APIs. Clear control.**（让接口，安静地跑起来） |
| 品牌承诺 | 一屏一件事；默认就好用；复杂功能也有清晰路径 |

### 品牌人格

- **工程师的克制**：不喧哗、不炫技，信息优先级清楚。
- **速度感**：动作路径短，反馈即时，视觉上有向前的动势。
- **秩序感**：网格、对齐、统一的间距与圆角。
- **可靠**：状态可预期，危险操作有确认，错误有下一步。

## 2. Logo

### 2.1 构成与含义

Logo 由三部分组成：

1. **圆角方形底**：代表「后台 / 应用 / 容器」，圆角 23% 接近现代应用图标语言。
2. **字母 F**：FastapiAdmin 的首字母，结构取自「面板 + 列表 + 详情」的三段式后台布局。
3. **燕尾缺口（核心识别点）**：F 的两条横臂末端各有一个向内收的 45° 燕尾缺口，形成两个尖角，像旗尾、也像请求的往返流向。这是本标识**可注册、可防御**的图形母题，必须保留，不能简化成普通 F。
4. **双色渐变**：`#4F6BFF → #6D5BFF`，只在数字场景使用；单色场景使用 `logo-mark-mono.svg` / `logo-mark-mono-inverse.svg`。

### 2.2 版本

| 版本 | 文件 | 用途 |
| --- | --- | --- |
| 主图标（彩色） | `brand/logo-mark.svg` | 应用图标、顶栏、登录页、头像 |
| 横版（浅底） | `brand/logo-horizontal-light.svg` | 官网、文档、浅色封面 |
| 横版（深底） | `brand/logo-horizontal-dark.svg` | 深色封面、演示、深色 UI |
| 单色标识（深） | `brand/logo-mark-mono.svg` | 单色印刷、浅底、压印 |
| 单色标识（浅） | `brand/logo-mark-mono-inverse.svg` | 深底单色、反白、压印 |
| 应用图标 | `brand/favicon.svg` | 16–32px 简化版 |
| 品牌板 | `brand/preview.png` | 对外展示 / 规范预览 |

### 2.3 尺寸与安全区

- 图标最小尺寸：数字 **24px**，印刷 **12mm**；favicon 使用简化版。
- 横版组合最小宽度：**120px**（图标不小于 28px）。
- 安全区：图标四周留白 ≥ 图标宽度的 **1/4**；横版文字右侧留白 ≥ 字高。
- 图标与文字间距：图标宽度的 **1/5**（横版已内置）。

### 2.4 使用规则

**可以：**

- 放在白色、浅灰 `#F5F6F8`、深色 `#161618` 背景上；
- 在深色背景使用横版深底或单色浅字标；
- 按比例整体缩放。

**禁止：**

- 拉伸、压扁、旋转、倾斜；
- 改渐变方向/颜色，或抹掉燕尾缺口；
- 把缺口改成圆角/斜切，破坏“双尖角”特征；
- 给图标加投影、描边、外发光；
- 把图标放在高饱和或复杂照片背景上（需加安全底板）；
- 只保留 tile 去掉 F，或只保留 F 去掉 tile 用于应用图标；
- 在单色场景把渐变 tile 直接转灰度（应改用 glyph 单色版）。

## 3. 色彩

### 3.1 品牌色

| 名称 | 值 | 用法 |
| --- | --- | --- |
| Brand Blue | `#4F6BFF` | 主色、渐变起点、链接、强调 |
| Brand Violet | `#6D5BFF` | 渐变终点、AI/智能相关 |
| Brand Gradient | 135° `#4F6BFF → #6D5BFF` | 仅用于 Logo、主 CTA、少量强调 |

### 3.2 中性色

| 名称 | 浅色 | 深色 |
| --- | --- | --- |
| Ink | `#141824` | `#F5F7FA` |
| Text secondary | `#5B6472` | `#AEB6C6` |
| Border | `#E6E8EC` | `#262B34` |
| Surface | `#FFFFFF` | `#1D1F24` |
| Canvas | `#F5F6F8` | `#161618` |

### 3.3 比例

- **60% 中性**：背景、卡片、文字；
- **30% 品牌**：主按钮、选中态、Logo；
- **10% 语义**：成功/警告/危险（见 UI-SPEC 3.2）。

> 品牌渐变**不做大面积背景**，只做点缀；一整屏渐变会失去「克制」。

### 3.4 主题色适配（重要）

平台支持 7 个主题主色 + 浅/深模式。**Logo 不跟随主题变色**，只按背景选择三种形态：

| 背景 | 用哪种 | 说明 |
| --- | --- | --- |
| 白色 / `#F5F6F8` 卡片、顶栏 | **彩色标** `logo-mark.svg` | 默认 |
| 深色 `#161618` | **彩色标** | 渐变 tile 与深底对比足够 |
| 主题色 / 饱和色背景（Indigo `#3F5CE8`、Purple `#B48DF3`、Blue `#1D84FF`、Green `#60C041`、Cyan `#38C0FC`、Orange `#F9901F`、Pink `#FF80C8`） | **反白标** `logo-mark-inverse.svg` 或 **白色单色** `logo-mark-mono-inverse.svg` | 彩色 tile 与蓝/紫主题会“融”在一起 |
| 灰度模式 / 单色印刷 | **单色标** `logo-mark-mono.svg` | 不依赖渐变 |
| 纯白底 | 禁止使用反白标 | 白 tile 在白底会消失 |

规则：

1. **不把 F 改成主题色**。主题色只影响按钮、选中态、图表，不影响品牌标识。
2. 彩色标与背景的对比度 ≥ 3:1；放置在同色系背景时切换为反白/白色单色。
3. 一张页面里 Logo 只出现一种形态，不要头部彩色、侧栏反白。
4. 若菜单/顶栏使用主题色填充，Logo 区使用反白标，并保证四周 ≥ 12px 留白。

> 参考：`brand/logo-on-themes.png`（7 个主题色 + 深/浅的实际效果）。

## 4. 字体

| 用途 | 字体 |
| --- | --- |
| 拉丁 / 数字 | Inter（回退 SF Pro Display / Segoe UI） |
| 中文 | PingFang SC（回退 思源黑体 / Microsoft YaHei） |
| 代码 / 终端 | JetBrains Mono（回退 SFMono-Regular / Consolas） |

- 品牌标题：700，字距 `-0.02em`；
- 正文：400/500，14px；
- 辅助：12px，`#5B6472`；
- 数字统一 `tabular-nums`。

## 5. 图形语言

- **圆角**：应用图标 23%，卡片 12px，按钮 8px，标签 pill。
- **线条**：1px `#E6E8EC`；不使用粗描边。
- **阴影**：仅卡片极轻投影，禁止彩色阴影。
- **渐变**：仅 Logo、主 CTA、进度条；同一屏不超过 2 处。
- **图标**：线性 1.5px、圆角端点；与文字间距 8px。

## 6. 语气与文案

- 动词开头，短句；一个句子只表达一件事。
- 不用感叹号堆情绪；不用「亲」「哦」等口语化语气。
- 错误文案 = 发生了什么 + 下一步怎么做。
- 空状态 = 当前状态 + 为什么 + 主操作。
- 按钮文案 = 动作（「保存」「生成」），不是「确定」。

## 7. 应用示例

### 顶栏

- 图标 32px + 品牌名 16px/600，间距 8px；
- 图标与页面内容左边缘对齐；
- 深色下使用同一彩色图标，文字转白。

### 登录页

- 图标 46px，与品牌名同排或上下排；
- 背景保持干净，不额外加渐变块。

### 浏览器图标

- 16/32px 使用简化 F（`favicon.svg`）；
- 不使用横版组合做 favicon。

### 文档 / PPT 封面

- 左上角 tile + 品牌名；
- 渐变面积 ≤ 页面 20%；
- 标题用 Ink，正文用 secondary。

## 8. 资源与落地

| 资源 | 路径 |
| --- | --- |
| 品牌资源 | `docs/brand/` |
| 前端内置 Logo | `frontend/web/src/assets/fa_imgs/logo.svg` |
| 站点图标 | `frontend/web/public/logo.svg`、`public/favicon.ico` |
| 后端静态 Logo | `backend/static/image/logo.svg`、`favicon.ico` |

自定义 Logo 仍走「参数管理 → Logo」，管理员上传的 Logo 优先；官方默认 Logo 已替换为新品牌标识。

## 9. 商业化准备

- **商标检索**：优先检索第 9 类（软件）、第 42 类（SaaS/开发服务），关键词用「图形 + FastapiAdmin」组合。
- **注册策略**：以「燕尾 F 图形」+「FastapiAdmin 文字」组合申请；纯字母 F 单独注册保护力度弱。
- **近似规避**：不要去掉缺口、不要改成常规 F；缺口就是与同类 F 标识拉开距离的关键。
- **落地测试**：新标识需通过四项测试后再对外发布：
  1. 16px favicon 可辨认；
  2. 单色黑/白仍能认出缺口；
  3. 深色底反白不糊；
  4. 压印/刺绣（无渐变）仍成立。
- **资产授权**：对外提供 `logo-mark.svg`、`logo-horizontal-light/dark.svg`、`logo-mark-mono*.svg` 四个文件，不提供渐变 PNG 以外的变体。

## 10. 变更记录

| 版本 | 日期 | 变更 |
| --- | --- | --- |
| v1.0 | 2026-10 | 首版标识：F + 斜切角 + 蓝紫渐变 |
| v2.0 | 2026-10 | 商业化增强：燕尾缺口成为独占母题；双色渐变；新增单色/反白版本与商标建议 |

---

## 界面规范

> 适用于 `frontend/web` 的管理端界面。跨端 token 生成见本文「设计 Token 生成」一节。目标是「现代、统一、可预期」：同一类信息用同一种布局与同一种视觉语言表达。
> 改 UI 前先读本规范；与本规范冲突的旧实现按本规范收敛。

## 1. 设计原则

1. **一屏一件事**：一页只解决一组任务，不堆重复入口、不叠页头。
2. **主次分明**：主操作在内容区左上；危险操作靠右并用红色；辅助信息降级为次要文字色。
3. **对齐优先**：同一行的卡片上下边对齐，左边缘统一，间距只使用 4 的倍数。
4. **少即是多**：默认无多余描边、无“卡中卡”、无第二层标题栏。
5. **深浅一致**：浅色与深色共用同一套语义 token，不允许在页面里写死颜色。

## 2. 布局

### 2.1 页面骨架

- 内容区统一内边距 **16px**（上下左右），不额外加页头。
- 页面标题由顶栏面包屑承担；页面内不再重复大标题。
- 一级容器使用 `fa-full-height`（`display:flex; flex-direction:column`）。

### 2.2 卡片

- 圆角 **12px**（`--fa-radius-md`），1px 边框 `--fa-border`（浅色 `#e6e8ec`，深色 `#262b34`），阴影极轻。
- 卡片内边距：常规 **16px**，紧凑列表 **12px**。
- 禁止卡片套卡片：内容区的表格/列表直接用卡片表面，不再加一层 `el-card` 外观。
- 同一行卡片高度一致（`align-items: stretch`，子卡片 `height: 100%`）。

### 2.3 工作区（左列表 + 右内容）

主从页面（字典、用户、SQL、文件浏览、参数、SSH 等）统一使用 `FaWorkbench` + `FaSidePanel`：

- 左右两张独立卡片，中间 **12px 热区**；
- 热区正中画 **1px 分割线**（`--fa-border`），悬停不变色；
- 热区可拖拽，左栏最小 **160px**、最大 **640px**；宽度随页面配置（字典 380 / 用户 260 / SQL 280 / 浏览 216 / 参数 240 / SSH 280）；
- ≤1280px 自动上下堆叠，分割线转横向；
- 左栏本身承载列表/树/分组，右侧承载表格/表单/终端。

> 背景：EP 原生的 `__dragger::before/::after` 会画两条 2px 线叠成粗线，必须隐藏后由自己画 1px。

### 2.4 首页信息架构

- 左主区 16 列、右信息栏 8 列（`el-row :gutter="16"`）。
- 行内所有卡片**间距 16**，顶底对齐；右栏卡片与左栏对应行对齐。
- 首页不要放重复卡片；健康、待办、快速入口按「常用 → 详情 → 辅助」排序。

### 2.5 间距

只允许以下间距：`4 / 8 / 12 / 16 / 20 / 24`。

- 卡片之间：16
- 卡片内元素：8 / 12
- 表单项之间：16
- 页面区块之间：16

## 3. 色彩

### 3.1 Token

| 用途 | 浅色 | 深色 |
| --- | --- | --- |
| 页面背景 | `#f5f6f8` | `#161618` |
| 卡片表面 | `#ffffff` | `#1d1f24` |
| 边框 | `#e6e8ec` | `#262b34` |
| 主色 | `--theme-color` | 同左 |
| 次要文字 | `--el-text-color-secondary` | 同左 |
| 占位文字 | `--el-text-color-placeholder` | 同左 |
| 滚动条 | `#c9ced8` | `#3a3f4a` |

### 3.2 主题色与品牌色

- 界面主色可在设置面板切换（7 个预设：#3F5CE8 / #B48DF3 / #1D84FF / #60C041 / #38C0FC / #F9901F / #FF80C8）。
- **Logo 不跟随主题色**：主题色只影响按钮、选中态、图表；品牌标识始终使用品牌渐变或单色版。
- 主题色背景上放 Logo 时，使用反白标/白色单色，避免同色系相融；规则见 [品牌规范 3.4](#品牌规范)。

### 3.3 语义色（U19）

- **状态/结果**才用语义色：启用/成功 `success`、停用/失败 `danger`、警告 `warning`、处理中 `primary`、中性信息 `info`。
- **非状态字段**（性别、类型、分类等）统一 `info`，不赋予红绿含义。
- 不允许用颜色作为唯一信息载体，必须同时有文字或图标。

## 4. 字体与数字

- 字号：正文 14，次要 13，辅助 12，页面标题 20–24。
- 行高 1.5；标题 1.3。
- 数字统一 `font-variant-numeric: tabular-nums`，统计数字千分位（`toLocaleString("zh-CN")`）。
- 日期规则：
  - 列表/表格：`YYYY-MM-DD` 或 `YYYY-MM-DD HH:mm`；
  - 详情/日志：需要精确到秒时才用 `YYYY-MM-DD HH:mm:ss`；
  - 禁止在 168px 列宽里塞带秒时间导致截断。

## 5. 组件规范

### 5.1 按钮

- 一个区域只允许一个主按钮（`type="primary"`）。
- 主操作放工具栏最左；删除用 `danger`，且二次确认。
- 图标按钮必须有 `aria-label`/`title`。
- 禁用态保留语义色但降低透明度，不改成灰色以外的颜色。

### 5.2 表单

- 标签在左、控件在右；搜索栏使用 `FaSearchBar`，默认收起高级项。
- 输入框不得只靠 placeholder 表达字段含义；无可见 label 时必须 `aria-label`。
- 校验信息统一红色 12px，紧贴控件下方。

### 5.3 表格

- 操作列 `fixed="right"`，宽度 180–200px；选择列 48，序号列 56。
- **1600px 下不出现横向滚动**为首要目标；列宽收敛顺序：操作 → 时间 → 描述 → 备注。
- 时间列宽：`YYYY-MM-DD` 用 120，`YYYY-MM-DD HH:mm` 用 150。
- 文本列 `showOverflowTooltip`，禁止撑破列宽。
- 空数据必须用统一空状态（图标 + 标题 + 一句说明 + 主操作），不要留白表格。
- 分页在卡片底部右侧，与表格同宽。

### 5.4 标签

- 使用 `FaStatusTag`，圆角 pill；同一状态全站同色。
- 标签数量超过 3 个时折叠为 `+N`。

### 5.5 弹窗 / 抽屉

- 表单型用抽屉（右侧 480–560px），确认型用对话框。
- 标题只写动作，不写“操作成功”之类结果文案。
- 提交按钮在右下，取消在左。

### 5.6 空状态 / 加载 / 错误

- 空状态三级：图标、标题、说明（+ 可选主操作）。
- 骨架屏用于首屏卡片；局部加载用 `v-loading`，不要整页白屏。
- 错误提示统一 `ElMessage.error`，网络错误给出可重试动作。

## 6. 响应式

| 断点 | 行为 |
| --- | --- |
| `> 1280` | 左右主从布局，右栏正常显示 |
| `≤ 1280` | 主从上下堆叠；首页保持左右栏；Banner 隐藏插画（≤1440） |
| `≤ 800` | 侧边栏变抽屉（220px + 遮罩）；卡片全宽；表格分页精简 |

- 移动端断点唯一来源：`MOBILE_BREAKPOINT = 800`。
- 不允许出现横向滚动；表格可横向滚动时必须保证操作列固定。

## 7. 交互与可访问性

- 所有图标按钮、纯图标链接有可读名称。
- 键盘焦点可见（`focus-visible` 环），不使用 `outline: none`。
- 首屏提供 skip link（跳到主内容）。
- 拖拽分割线提供 cursor 提示（`col-resize` / `row-resize`）。
- 收藏入口：顶部标签左侧星标（默认透明度 0.62，选中实心）；首页「快速链接」为空时显示引导文案。
- 滚动条统一点性灰，不使用品牌色。

## 8. 反模式（禁止）

- 页面内再画一层页头/标题栏。
- 卡片套卡片、双层边框、双层阴影。
- 表格里塞带秒时间导致省略号。
- 操作列不固定，滚出视口。
- 用 opacity 隐藏分割线（要移除元素或显式画 1px）。
- 写死颜色/间距/字号，绕过 token。
- 同一状态在不同页面用不同颜色。

## 9. 提交前检查清单

- [ ] 无页面级横向滚动；表格 1600px 下无横向滚动（或操作列固定）
- [ ] 时间列完整显示，日期/时间格式符合第 4 节
- [ ] 同一行卡片顶底对齐，间距为 16
- [ ] 深浅色都检查过
- [ ] 1280 / 768 检查过，无溢出
- [ ] 图标按钮有 aria-label
- [ ] `pnpm ts:check`、SFC 扫描、eslint、stylelint 通过

## 10. 参考实现

- 工作区：`src/components/containers/fa-workbench/index.vue`、`fa-side-panel/index.vue`
- 首页：`src/views/dashboard/home/index.vue`
- 表格示例：用户、角色、菜单、公告、日志、代码生成
- 全局样式：`src/styles/core/_app.scss`、`_reset.scss`、`tailwind.css`

## 11. 分栏规范

- 左右工作区统一使用两张卡片 + 16px 间距；
- 不提供拖拽手柄、分割线或 `col-resize`；
- 左栏宽度由页面 `side-width` 固定（如 216 / 240 / 260 / 380）；
- 窄屏 ≤1280 自动上下排列，AI 助手侧栏 ≤800 自动收起。

## 12. 图标规范

- **统一图标集**：Remix Icon 线性图标（`ri:*-line`），通过 `FaSvgIcon` 渲染。
- **尺寸**：常规 16px、操作按钮 18px、强调 20px；不混用 14/22 等自定尺寸。
- **颜色**：跟随 `currentColor`，由按钮/菜单状态控制，不在图标上写死颜色。
- **Element Plus 图标**：只允许出现在组件内部（下拉箭头、分页、加载、密码可见性），业务按钮不使用。
- **第三方品牌图标**：保持官方 Logo（微信、GitHub、Gitee 等），不做线性化处理。
- **Emoji**：只用于欢迎语等装饰场景，不用于操作按钮。

## 13. 三端验收（Web / 官网 / 小程序）

验收图：

- 三端浅色 / 深色：[`brand/acceptance.png`](./brand/acceptance.png)
- 三端暗色：[`brand/dark-consistency.png`](./brand/dark-consistency.png)

### 检查清单

- [ ] 三端颜色、圆角、间距、字号全部来自 `design/tokens.json`
- [ ] Logo 使用 v2 燕尾 F，品牌名统一 `FastapiAdmin`
- [ ] 主色阶一致（Web 主题色 / 官网渐变 / 小程序 wot-primary）
- [ ] 浅色表面 `#FFF` / `#F5F6F8`，深色表面 `#15181E` / `#191D24`
- [ ] 深色边框 `#262B34`，文字 `#E5E7EB / #A3AAB8 / #8B93A1`
- [ ] 输入框、弹窗、浮层、遮罩使用组件表面 token
- [ ] 表格表头浅色 `#F9FAFB`、深色 `#1B1E24`
- [ ] 1200 / 800 断点下无横向溢出
- [ ] 三端 favicon / 小程序头像为新标识

### 结果

- Web：主表、仪表盘、工作区无横向溢出；深色组件验证通过。
- 官网：VitePress 构建通过，深浅色首页正常。
- 小程序：H5 编译通过，登录页深浅色与新品牌色一致。


---

## 设计 Token 生成

一份源，三端消费：**官网（VitePress）/ Web（Vue3 + Element Plus）/ 小程序（uni-app）**。

## 唯一来源

`design/tokens.json` 是颜色、圆角、间距、字号、断点的唯一来源。**不要直接改生成文件。**

## 生成

```bash
node scripts/design-tokens/generate.mjs
```

生成结果：

| 端 | 文件 | 形式 |
| --- | --- | --- |
| Web | `frontend/web/src/styles/core/_brand-tokens.generated.scss` | CSS 变量 `--fa-*` |
| 官网 | `frontend/docs/.vitepress/theme/styles/brand-tokens.generated.css` | CSS 变量 `--fa-*` / `--vp-brand-gradient` |
| 小程序 | `frontend/app/src/styles/brand-tokens.generated.scss` | SCSS 变量 `$fa-*` |

## 当前 Token

| 组 | 值 |
| --- | --- |
| brand.blue | `#4F6BFF` |
| brand.violet | `#6D5BFF` |
| brand.gradient | `135deg #4F6BFF → #6D5BFF` |
| neutral.ink | `#141824` |
| neutral.border | `#E6E8EC` |
| neutral.canvas | `#F5F6F8` / 深色 `#15181E` |
| radius | `6 / 8 / 12 / 16 / pill` |
| space | `4 / 8 / 12 / 16 / 20 / 24` |
| font | `12 / 13 / 14 / 16 / 20 / 24` |
| breakpoint | `800 / 992 / 1280` |
| control | `24 / 32 / 40`（sm/md/lg 控件高） |
| table | 行高 40 / 表头 44 |
| layout | 页面内边距 16 / 顶栏 56 |
| shadow | card / pop / modal（含深色版本） |
| fontFamily | Inter / PingFang SC / 等宽栈 |
| table.headerBg | 浅色 #F9FAFB / 深色 #1B1E24 |
| component.input / dialog / popover | 浅色 #FFFFFF，深色 #1B1E24 / #23262E |
| component.overlay | 浅色 rgba(0,0,0,.5)，深色 rgba(0,0,0,.65) |
| dark | surface `#15181E` / `#191D24`，border `#262B34`，text `#E5E7EB / #A3AAB8 / #8B93A1` |

## 规则

1. 新增颜色/圆角/间距，先改 `tokens.json`，再运行生成脚本。
2. 页面与组件不写十六进制颜色，不写魔法圆角/间距。
3. Web 的 `--fa-*` 继续作为全站变量名；官网映射到 `--vp-brand-gradient`；小程序使用 `$fa-*`。
4. 生成文件顶部有「请勿手改」注释；提交前跑一次生成，保证三端一致。
5. Brand 专属资产（Logo、单色版）仍以 `docs/brand/` 与 `docs/DESIGN-SPEC.md` 为准。

## 暗色模式现状

| 端 | 选择器 | 状态 |
| --- | --- | --- |
| Web | `html.dark` | 已映射 surface / border / text / shadow |
| 官网 | `.dark` | 已映射 `--vp-c-bg*`、divider、text |
| 小程序 | `.wot-theme-dark` | 已映射 wot 背景/文字/边框/主色 |

## 验收材料

- 三端浅色/深色对比：[`docs/brand/three-platform.png`](../docs/brand/three-platform.png)
- 三端暗色对比：[`docs/brand/dark-consistency.png`](../docs/brand/dark-consistency.png)
- 三端浅/深验收：[`docs/brand/acceptance.png`](../docs/brand/acceptance.png)

## 与规范的关系

- 界面规范：[`docs/DESIGN-SPEC.md`](../docs/DESIGN-SPEC.md)
- 品牌规范：[`docs/DESIGN-SPEC.md`](../docs/DESIGN-SPEC.md)

---

## UI 规范（强制）

所有 Web UI 新增与修改必须遵守 [DESIGN-SPEC.md](../docs/DESIGN-SPEC.md)：布局、间距、断点、表格、移动卡片、弹窗、颜色语义、i18n、提交检查清单。

---

## 品牌素材（单一来源）

- Logo / favicon 统一放在 `design/assets/`。
- 同步到官网、Web、小程序、后端验证码：

```bash
node scripts/sync-brand-assets.mjs
```

不要在 `frontend/*/public`、`frontend/app/src/static` 等目录单独修改 Logo；改 `design/assets/` 后执行同步脚本。

## 一致性检查

```bash
node scripts/check-brand-consistency.mjs
```

检查三端 Logo 哈希、旧品牌色、旧间距/圆角类；CI 或提交前执行。
