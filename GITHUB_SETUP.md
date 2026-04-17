# GitHub Setup Guide

## Bước 1: Tạo Repository trên GitHub

1. Vào https://github.com
2. Click "New repository"
3. Repository name: `day12-agent-deployment`
4. Description: "Day 12 Lab - Deploy AI Agent to Production"
5. **Public** (để instructor có thể access)
6. **KHÔNG** check "Initialize with README" (vì đã có rồi)
7. Click "Create repository"

## Bước 2: Initialize Git Local

Mở terminal trong folder project và chạy:

```bash
# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Day 12 Lab - Production AI Agent

- Completed all 6 parts of the lab
- Deployed to Railway
- All features working (auth, rate limiting, health checks)
- Public URL: https://wonderful-delight-production-9390.up.railway.app"
```

## Bước 3: Connect to GitHub

```bash
# Add remote (thay YOUR_USERNAME bằng GitHub username của bạn)
git remote add origin https://github.com/YOUR_USERNAME/day12-agent-deployment.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Bước 4: Verify

1. Refresh GitHub repository page
2. Kiểm tra tất cả files đã được push
3. Kiểm tra `.env` KHÔNG có trong repo (chỉ có `.env.example`)

## Bước 5: Add Screenshots

1. Chụp screenshots theo hướng dẫn trong `screenshots/README.md`
2. Add screenshots vào folder `screenshots/`
3. Commit và push:

```bash
git add screenshots/
git commit -m "Add deployment screenshots"
git push
```

## Bước 6: Submit

Copy GitHub repository URL và submit:

```
https://github.com/YOUR_USERNAME/day12-agent-deployment
```

---

## Troubleshooting

### Lỗi: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/day12-agent-deployment.git
```

### Lỗi: "failed to push"
```bash
git pull origin main --rebase
git push -u origin main
```

### Kiểm tra .env không bị commit
```bash
git status
# Không thấy .env trong list → OK!
```

---

## Security Checklist

- [ ] `.env` file KHÔNG có trong repo
- [ ] `.env.example` có trong repo (không có secrets thật)
- [ ] `AGENT_API_KEY` trong code là placeholder
- [ ] Không có hardcoded secrets
- [ ] `.gitignore` đã config đúng

---

## Final Checklist

- [ ] Repository created on GitHub
- [ ] All files pushed
- [ ] Screenshots added
- [ ] No secrets committed
- [ ] README.md displays correctly
- [ ] Public URL in DEPLOYMENT.md works
- [ ] Repository is public
- [ ] Submit GitHub URL

---

**Good luck! 🚀**
