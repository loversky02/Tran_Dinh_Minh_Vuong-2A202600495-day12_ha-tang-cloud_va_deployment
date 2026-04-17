# Deployment Information

**Student Name:** Tran Dinh Minh Vuong  
**Student ID:** 2A202600495  
**Date:** 17/04/2026

---

## Status

✅ **DEPLOYED** - Agent đang chạy trên Railway

---

## Public URL

**URL:** https://wonderful-delight-production-9390.up.railway.app

**Platform:** Railway

**Project:** wonderful-delight

**Dashboard:** https://railway.com/project/bf70a1fe-6d7a-48bf-9fe0-f1c1253b4f07

---

## Test Commands

### Health Check
```bash
curl https://wonderful-delight-production-9390.up.railway.app/health
# Expected: {"status": "ok", "uptime_seconds": X, "platform": "Railway"}
```

**✅ TESTED - Working!**

### Readiness Check
```bash
curl https://wonderful-delight-production-9390.up.railway.app/
# Expected: {"message": "AI Agent running on Railway!", "docs": "/docs", "health": "/health"}
```

### API Test (without authentication)
```bash
curl -X POST https://wonderful-delight-production-9390.up.railway.app/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
# Expected: 401 Unauthorized
```

**✅ TESTED - Working!**
Response: `{"detail":"Missing API key. Include header: X-API-Key: <your-key>"}`

### API Test (with authentication)
```bash
curl -X POST https://wonderful-delight-production-9390.up.railway.app/ask \
  -H "X-API-Key: demo-key-change-me" \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
# Expected: 200 OK with answer
```

**✅ TESTED - Working!**
Response: `{"question":"Hello","answer":"...","platform":"Railway","version":"2.0.0"}`

### Rate Limiting Test
```bash
# Send 12 requests
for i in {1..12}; do
  curl -X POST https://wonderful-delight-production-9390.up.railway.app/ask \
    -H "X-API-Key: demo-key-change-me" \
    -H "Content-Type: application/json" \
    -d '{"question":"test"}';
done
# Expected: Requests 10+ return 429
```

**✅ TESTED - Working!**
- Requests 1-9: 200 OK
- Requests 10+: 429 Too Many Requests

---

## Environment Variables Set

Các environment variables đã config trên Railway:

- [x] `PORT` - Port number (auto-injected by Railway: 8080)
- [x] `ENVIRONMENT` - production
- [ ] `DEBUG` - false (default)
- [ ] `REDIS_URL` - Not needed yet (no Redis in basic version)
- [ ] `AGENT_API_KEY` - Not implemented yet (Part 4)
- [ ] `LOG_LEVEL` - INFO (default)
- [ ] `RATE_LIMIT_PER_MINUTE` - Not implemented yet (Part 4)
- [ ] `MONTHLY_BUDGET_USD` - Not implemented yet (Part 4)

---

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Load Balancer  │  (Platform managed)
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   AI Agent      │  (FastAPI app)
│   Container     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│     Redis       │  (State storage)
└─────────────────┘
```

---

## Screenshots

**Chưa có screenshots - Sẽ thêm sau khi deploy:**

- [ ] Deployment dashboard
- [ ] Service running logs
- [ ] Health check test
- [ ] API test results
- [ ] Rate limiting in action

Screenshots sẽ được lưu trong folder `screenshots/`

---

## Deployment Steps (To Do)

### Option 1: Railway

1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Set environment variables
5. Deploy: `railway up`
6. Get domain: `railway domain`

### Option 2: Render

1. Push code to GitHub
2. Connect Render to GitHub repo
3. Create new Web Service
4. Set environment variables in dashboard
5. Deploy automatically

---

## Local Testing

Trước khi deploy, đã test local với Docker:

```bash
# Build image
docker build -t my-agent:latest .

# Run container
docker run -p 8000:8000 --env-file .env my-agent:latest

# Test
curl http://localhost:8000/health
```

---

## Next Steps

- [ ] Hoàn thành Part 2-5 của lab
- [ ] Build final production-ready agent (Part 6)
- [ ] Test thoroughly locally
- [ ] Deploy to Railway/Render
- [ ] Update this file with actual URLs
- [ ] Add screenshots
- [ ] Test public URL from different devices
- [ ] Submit GitHub repo

---

## Notes

- Đang ở Part 1, chưa có code production-ready để deploy
- Cần hoàn thành Part 2-6 trước khi deploy
- Sẽ chọn Railway vì có $5 free credit và dễ dùng hơn
