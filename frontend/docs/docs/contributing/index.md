---
outline: "deep"
title: 贡献指南
---

# 🤝 贡献指南

感谢你对 FastapiAdmin 的关注！我们非常欢迎社区贡献，无论是修复 Bug、新增功能、完善文档还是提出建议，都是对项目的宝贵支持。

## 📋 贡献前须知

在开始贡献之前，请先阅读以下内容：

- 查阅 [开发规范](/guidelines/)，了解代码风格和提交规范
- 在 [GitHub Issues](https://github.com/fastapiadmin/FastapiAdmin/issues) 或 [Gitee Issues](https://gitee.com/fastapiadmin/FastapiAdmin/issues) 中搜索，确认你的问题或功能需求尚未被提出
- 对于较大的功能改动，建议先开 Issue 讨论方案，再动手开发

## 🚀 提交 PR 完整流程

### 第一步：Fork 仓库

前往 GitHub 或 Gitee 项目主页，点击右上角的 **Fork** 按钮，将仓库 Fork 到你自己的账号下。

- GitHub：[fastapiadmin/FastapiAdmin](https://github.com/fastapiadmin/FastapiAdmin)
- Gitee：[fastapiadmin/FastapiAdmin](https://gitee.com/fastapiadmin/FastapiAdmin)

### 第二步：克隆到本地

将你 Fork 后的仓库克隆到本地：

```bash
git clone https://github.com/<你的用户名>/FastapiAdmin.git
cd FastapiAdmin
```

添加上游仓库，方便后续同步官方最新代码：

```bash
git remote add upstream https://github.com/fastapiadmin/FastapiAdmin.git
```

### 第三步：创建功能分支

**不要直接在 `master` 或 `dev` 分支上开发**，请根据改动类型创建对应分支：

```bash
# 新功能
git checkout -b feature/your-feature-name

# Bug 修复
git checkout -b bugfix/your-bug-description

# 文档更新
git checkout -b docs/your-doc-description
```

### 第四步：开发与提交

完成代码修改后，按照项目的 [Git 提交规范](/guidelines/#git-提交规范) 提交代码：

```bash
git add .
git commit -m "feat(module): 简短描述你的改动"
```

提交信息格式参考：

| 类型 | 说明 |
| --- | --- |
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档修改 |
| `style` | 代码格式调整（不影响逻辑） |
| `refactor` | 代码重构 |
| `chore` | 构建工具或依赖变更 |

### 第五步：同步上游代码

在推送之前，先同步官方仓库的最新代码，避免冲突：

```bash
git fetch upstream
git rebase upstream/dev
```

如果有冲突，解决冲突后继续：

```bash
# 解决冲突后
git add .
git rebase --continue
```

### 第六步：推送到远程

将本地分支推送到你 Fork 的远程仓库：

```bash
git push origin feature/your-feature-name
```

### 第七步：创建 Pull Request

1. 打开你 Fork 的仓库页面，GitHub/Gitee 会自动提示你创建 PR
2. 点击 **Compare & pull request** 或 **新建 Pull Request**
3. 确认目标分支为 **`dev`**（不是 `master`）
4. 填写 PR 信息：

**PR 标题**（简洁清晰，不超过 70 字符）：
```
feat(system): 添加用户批量导入功能
```

**PR 描述模板**：
```markdown
## 改动说明

简要描述本次 PR 的改动内容和目的。

## 改动类型

- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 其他

## 关联 Issue

Closes #xxx

## 测试说明

描述你是如何测试这些改动的。

## 截图（如适用）
```

5. 提交 PR 后，等待维护者审核

### 第八步：响应 Code Review

维护者可能会对你的 PR 提出修改意见，请及时响应：

```bash
# 根据反馈修改代码后，追加提交
git add .
git commit -m "fix: 根据 review 意见修改 xxx"
git push origin feature/your-feature-name
```

PR 页面会自动更新，无需重新创建。

## ✅ PR 合并标准

你的 PR 需要满足以下条件才会被合并：

- 代码符合项目 [开发规范](/guidelines/)
- 通过所有自动化检查（lint、type check 等）
- 至少获得一位维护者的 Approve
- 没有未解决的 Review 意见
- 提交信息符合规范

## 💡 贡献方向

如果你不知道从哪里开始，可以参考以下方向：

- 🐛 **修复 Bug**：查看 [Issues](https://github.com/fastapiadmin/FastapiAdmin/issues) 中标记为 `bug` 的问题
- ✨ **新功能**：查看标记为 `enhancement` 或 `help wanted` 的 Issue
- 📖 **完善文档**：修正错别字、补充说明、翻译文档
- 🌍 **国际化**：帮助翻译界面或文档到其他语言
- 🎨 **UI 优化**：改善用户界面和交互体验

## 📞 遇到问题？

如果在贡献过程中遇到任何问题，欢迎通过以下方式寻求帮助：

- 在相关 Issue 下留言
- 发送邮件至 [948080782@qq.com](mailto:948080782@qq.com)
- 加入微信交流群（见 [关于我们](/about/)）

再次感谢你的贡献，期待你的 PR！🎉
