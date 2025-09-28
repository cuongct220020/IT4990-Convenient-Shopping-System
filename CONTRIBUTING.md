# Contributing Guidelines

---

## 1. Commit Message Convention

### Cú pháp:
```
<type>(<scope>): <short summary>
```

### Các `type` phổ biến
- `feat:` → thêm **tính năng mới**
- `fix:` → **sửa bug**
- `docs:` → thay đổi/tạo mới **tài liệu**
- `style:` → thay đổi **format/code style** (không ảnh hưởng logic)
- `refactor:` → **tái cấu trúc code**, không thêm tính năng hay sửa bug
- `test:` → thêm/sửa **test case**
- `chore:` → công việc phụ (config, build, tool…)
- `perf:` → cải thiện **hiệu năng**
- `ci:` → thay đổi **CI/CD config**

---

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

---

## 3. Pull Request (PR) Convention

### Title
- Ngắn gọn, rõ ràng, theo format giống commit message
- Ví dụ: `feat(auth): thêm đăng nhập Google`

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