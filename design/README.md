# 跨端设计 Token

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
