# Contributing Guidelines

This contributing guideline applies to collaborators of this project only.  
External contributions are not accepted at this time. If you would like to contribute in the future, please contact the repository owner.

Only the repository owner (admin) has direct **push** and **merge** permissions on the `develop` and `main` branches.  
All other collaborators must create feature branches and submit pull requests for review.

---

## 📘 Introduction

This document defines the standard workflow and conventions that all collaborators must follow when contributing to this repository.  
It aims to ensure code consistency, maintain project stability, and make collaboration efficient and transparent.

By following these guidelines, you help:
- Keep the commit history clean and meaningful.
- Simplify the code review and deployment process.
- Maintain a professional, predictable workflow for all contributors.

Please read through these guidelines carefully before creating commits, branches, or pull requests.

---

## 📝 Commit Guidelines

To keep a clean and consistent Git history, please follow these conventions when writing commit messages.

### 1. Basic Syntax

```
git commit -m "<type>: <short description>"
```

Each commit message should clearly explain what and why a change was made. Before committing, ask yourself:
- Why have I made these changes?
- What effect have my changes made?
- Why was the change needed?
- What are the changes in reference to?

### 2. Conventional Commit Format
Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
standard:
```
<type>: <description>
```

#### The commit type can include the following:

| Type       | Meaning                                                 |
| ---------- | ------------------------------------------------------- |
| `feat`     | Introduces a new feature                                |
| `fix`      | Fixes a bug                                             |
| `docs`     | Documentation updates (e.g. README, CONTRIBUTING)       |
| `style`    | Code style or formatting changes (no code logic impact) |
| `refactor` | Code restructuring that doesn’t change functionality    |
| `test`     | Adds or updates tests                                   |
| `chore`    | Routine tasks, maintenance, or dependency updates       |
| `perf`     | Performance improvements                                |
| `ci`       | Continuous integration or build pipeline changes        |
| `build`    | Changes to the build system or external dependencies    |
| `revert`   | Reverts a previous commit                               |


### 3. Writing High-Quality Commit Messages

Follow these best practices:

- Use the imperative mood
  - ✅ "add dark mode toggle"
  - ❌ "added dark mode toggle” or “adds dark mode toggle"

- Capitalize the first word of type and description, but do not end with punctuation
  - ✅ "fix: resolve UI glitch on mobile"
  - ❌ "Fix: Resolve UI glitch on mobile."
- Template for commit message:
  - Keep it concise:
    - Subject line ≤ 50 characters
    - Body lines ≤ 72 characters 
  - Explain the context (if needed)
  - **Avoid filler words:**
    - Be direct, skip words like "maybe", "I think", or "kind of".
Add a body when the commit isn’t self-explanatory:

```
<short description>
feat: add caching layer for user data
<detail description>
- The new caching system reduces database load by ~30%.
- It uses Redis for fast in-memory lookups.
```






## 2. Branch Naming Convention

### Cú pháp:
```
<type>/<short-description>
```

### Các `type` phổ biến
- `feature/` → phát triển tính năng mới
- `bugfix/` → sửa bug
- `hotfix/` → sửa bug khẩn cấp trên production
- `release/` → chuẩn bị bản phát hành
- `chore/` → task phụ (CI/CD, config…)

### Ví dụ
```
feature/login-google
bugfix/cart-empty-error
hotfix/payment-crash
release/v1.2.0
chore/update-dependencies
feature/user-profile-management
bugfix/responsive-layout-mobile
```

# Commit message comparision
Good
- feat: improve performance with lazy load implementation for images
- chore: update npm dependency to latest version
- fix: fix bug preventing users from submitting the subscribe form
Update incorrect client phone number within footer body per client request
Bad
fixed bug on landing page
Changed style
oops
I think I fixed it this time?
empty commit messages



---

## 3. Pull Request (PR) Convention

### Title
- Ngắn gọn, rõ ràng, theo format giống commit message
- Ví dụ: `feat: thêm đăng nhập Google`

## 4. Workflow Recommendations

### Feature Development
1. Tạo branch từ `develop`: `git checkout -b feature/tên-tính-năng`
2. Develop và commit theo convention
3. Push và tạo PR vào `develop`
4. Request review từ team members
5. Merge sau khi được approve

### Hotfix Process
1. Tạo branch từ `main`: `git checkout -b hotfix/tên-bug`
2. Fix và test kỹ
3. Tạo PR vào cả `main` và `develop`
4. Deploy ngay sau khi merge vào `main`

### Release Process
1. Tạo `release/v1.x.x` từ `develop`
2. Final testing và bug fixes
3. Merge vào `main` và tag version
4. Merge ngược lại `develop`

---
