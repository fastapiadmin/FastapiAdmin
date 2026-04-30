---
outline: "deep"
title: Contributing Guide
---

# 🤝 Contributing Guide

Thank you for your interest in FastapiAdmin! We warmly welcome community contributions — whether it's fixing bugs, adding features, improving documentation, or sharing suggestions, every contribution is valuable to the project.

## 📋 Before You Start

Before contributing, please take a moment to:

- Read the [Development Guidelines](/en/guidelines/) to understand code style and commit conventions
- Search [GitHub Issues](https://github.com/fastapiadmin/FastapiAdmin/issues) to make sure your bug or feature request hasn't already been reported
- For significant changes, consider opening an Issue first to discuss your approach before writing code

## 🚀 Step-by-Step PR Workflow

### Step 1: Fork the Repository

Go to the project's GitHub page and click the **Fork** button in the top-right corner to fork the repository to your own account.

- GitHub: [fastapiadmin/FastapiAdmin](https://github.com/fastapiadmin/FastapiAdmin)
- Gitee: [fastapiadmin/FastapiAdmin](https://gitee.com/fastapiadmin/FastapiAdmin)

### Step 2: Clone Locally

Clone your forked repository to your local machine:

```bash
git clone https://github.com/<your-username>/FastapiAdmin.git
cd FastapiAdmin
```

Add the upstream remote to keep your fork in sync with the official repository:

```bash
git remote add upstream https://github.com/fastapiadmin/FastapiAdmin.git
```

### Step 3: Create a Feature Branch

**Never develop directly on `master` or `dev`.** Create a branch based on the type of change:

```bash
# New feature
git checkout -b feature/your-feature-name

# Bug fix
git checkout -b bugfix/your-bug-description

# Documentation update
git checkout -b docs/your-doc-description
```

### Step 4: Make Changes and Commit

After completing your changes, commit them following the project's [Git commit conventions](/en/guidelines/#git-commit-conventions):

```bash
git add .
git commit -m "feat(module): brief description of your change"
```

Commit message type reference:

| Type | Description |
| --- | --- |
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code formatting (no logic change) |
| `refactor` | Code refactoring |
| `chore` | Build tools or dependency updates |

### Step 5: Sync with Upstream

Before pushing, sync the latest changes from the official repository to avoid conflicts:

```bash
git fetch upstream
git rebase upstream/dev
```

If there are conflicts, resolve them and continue:

```bash
# After resolving conflicts
git add .
git rebase --continue
```

### Step 6: Push to Remote

Push your local branch to your forked remote repository:

```bash
git push origin feature/your-feature-name
```

### Step 7: Create a Pull Request

1. Open your forked repository on GitHub/Gitee — it will prompt you to create a PR automatically
2. Click **Compare & pull request** or **New Pull Request**
3. Make sure the target branch is **`dev`** (not `master`)
4. Fill in the PR details:

**PR Title** (concise, under 70 characters):
```
feat(system): add bulk user import feature
```

**PR Description Template**:
```markdown
## Summary

Briefly describe what this PR changes and why.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Other

## Related Issue

Closes #xxx

## Testing

Describe how you tested your changes.

## Screenshots (if applicable)
```

5. Submit the PR and wait for a maintainer to review it

### Step 8: Respond to Code Review

Maintainers may request changes. Please respond promptly:

```bash
# After making the requested changes
git add .
git commit -m "fix: address review feedback for xxx"
git push origin feature/your-feature-name
```

The PR page will update automatically — no need to create a new PR.

## ✅ Merge Criteria

Your PR needs to meet the following requirements before it can be merged:

- Code follows the project's [Development Guidelines](/en/guidelines/)
- All automated checks pass (lint, type check, etc.)
- At least one maintainer Approval
- No unresolved review comments
- Commit messages follow the convention

## 💡 Ways to Contribute

Not sure where to start? Here are some ideas:

- 🐛 **Fix Bugs**: Check [Issues](https://github.com/fastapiadmin/FastapiAdmin/issues) labeled `bug`
- ✨ **New Features**: Look for Issues labeled `enhancement` or `help wanted`
- 📖 **Improve Docs**: Fix typos, add explanations, or translate documentation
- 🌍 **Internationalization**: Help translate the UI or docs into other languages
- 🎨 **UI Improvements**: Enhance the user interface and interaction experience

## 📞 Need Help?

If you run into any issues during the contribution process, feel free to reach out:

- Comment on the relevant Issue
- Send an email to [948080782@qq.com](mailto:948080782@qq.com)
- Join the WeChat group (see [About Us](/en/about/))

Thank you again for contributing — we look forward to your PR! 🎉
