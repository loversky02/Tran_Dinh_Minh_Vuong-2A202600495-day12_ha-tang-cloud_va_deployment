# Screenshots

## Required Screenshots for Submission

Please add the following screenshots to this folder:

### 1. Railway Dashboard
**Filename:** `railway-dashboard.png`
- Show your Railway project dashboard
- Display: Project name, deployment status, URL

### 2. Service Running
**Filename:** `service-running.png`
- Show Railway deployment logs
- Display: "Deploy complete", health check success

### 3. Health Check Test
**Filename:** `health-check.png`
- Terminal screenshot showing:
```bash
curl https://wonderful-delight-production-9390.up.railway.app/health
```
- Response showing status "ok"

### 4. Authentication Test
**Filename:** `auth-test.png`
- Terminal screenshot showing:
  - Request without API key → 401
  - Request with API key → 200

### 5. Rate Limiting Test
**Filename:** `rate-limit-test.png`
- Terminal screenshot showing:
  - Multiple requests
  - 429 error after limit exceeded

### 6. API Response
**Filename:** `api-response.png`
- Postman or terminal showing successful API call
- Display full request and response

---

## How to Take Screenshots

### Windows
- Press `Win + Shift + S` to capture screen
- Or use Snipping Tool

### Mac
- Press `Cmd + Shift + 4` to capture area
- Or press `Cmd + Shift + 3` for full screen

### Linux
- Press `PrtScn` or use Screenshot tool

---

## Current Status

- [ ] railway-dashboard.png
- [ ] service-running.png
- [ ] health-check.png
- [ ] auth-test.png
- [ ] rate-limit-test.png
- [ ] api-response.png

**Note:** Add actual screenshots before final submission!
