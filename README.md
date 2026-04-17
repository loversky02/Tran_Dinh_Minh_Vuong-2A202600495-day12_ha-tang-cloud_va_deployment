# Day 12 Lab - AI Agent Deployment

**Course:** AICB-P1 · VinUniversity 2026  
**Student:** Tran Dinh Minh Vuong  
**Student ID:** 2A202600495  
**Lab:** Deploy AI Agent to Production

---

## 📋 Project Overview

This repository contains my work for Day 12 Lab - learning how to deploy an AI agent from localhost to production cloud platforms.

**Learning Objectives:**
- Understand difference between development and production code
- Containerize AI agent with Docker
- Deploy to cloud platforms (Railway/Render)
- Implement API security (authentication, rate limiting, cost guard)
- Design scalable and reliable systems

---

## 🗂 Repository Structure

```
.
├── 01-localhost-vs-production/    # Part 1: Dev vs Prod comparison
│   ├── develop/                   # Basic version with anti-patterns
│   └── production/                # Production-ready version
├── 02-docker/                     # Part 2: Docker containerization
│   ├── develop/                   # Basic Dockerfile
│   └── production/                # Multi-stage build + compose
├── 03-cloud-deployment/           # Part 3: Cloud deployment configs
│   ├── railway/
│   ├── render/
│   └── production-cloud-run/
├── 04-api-gateway/                # Part 4: API security
│   ├── develop/                   # Basic auth
│   └── production/                # JWT + rate limit + cost guard
├── 05-scaling-reliability/        # Part 5: Scaling & reliability
│   ├── develop/                   # Basic health checks
│   └── production/                # Full stack with load balancer
├── 06-lab-complete/               # Part 6: Final production agent
│   └── [Will be completed]
├── utils/                         # Shared utilities
│   └── mock_llm.py               # Mock LLM for testing
├── MISSION_ANSWERS.md            # Answers to all exercises
├── DEPLOYMENT.md                 # Deployment information
├── CODE_LAB.md                   # Lab instructions
├── DAY12_DELIVERY_CHECKLIST.md   # Submission checklist
└── README.md                     # This file
```

---

## 🚀 Progress

- [x] **Part 1:** Localhost vs Production (COMPLETED ✅)
  - Identified 7 anti-patterns in develop code
  - Compared with production-ready version
  - Learned about env vars, health checks, graceful shutdown

- [ ] **Part 2:** Docker Containerization (TODO)
  - Basic Dockerfile
  - Multi-stage builds
  - Docker Compose orchestration

- [ ] **Part 3:** Cloud Deployment (TODO)
  - Deploy to Railway/Render
  - Configure environment variables
  - Test public URL

- [ ] **Part 4:** API Security (TODO)
  - API key authentication
  - JWT tokens
  - Rate limiting
  - Cost guard

- [ ] **Part 5:** Scaling & Reliability (TODO)
  - Health checks
  - Graceful shutdown
  - Stateless design
  - Load balancing

- [ ] **Part 6:** Final Project (TODO)
  - Build production-ready agent from scratch
  - Deploy to cloud
  - Full testing

---

## 🛠 Setup Instructions

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- (Optional) Railway CLI or Render account

### Local Development

1. **Clone repository:**
```bash
git clone https://github.com/your-username/day12-agent-deployment.git
cd day12-agent-deployment
```

2. **Part 1 - Test develop version:**
```bash
cd 01-localhost-vs-production/develop
pip install -r requirements.txt
python app.py

# Test
curl "http://localhost:8000/ask?question=Hello" -X POST
```

3. **Part 1 - Test production version:**
```bash
cd ../production
cp .env.example .env
pip install -r requirements.txt
python app.py

# Test health check
curl http://localhost:8000/health

# Test readiness
curl http://localhost:8000/ready

# Test API
curl http://localhost:8000/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello from production"}'
```

---

## 📝 Key Learnings

### Part 1: Development vs Production

**Anti-patterns found in develop code:**
1. Hardcoded secrets (API keys in code)
2. No config management
3. Print() instead of proper logging
4. No health check endpoints
5. Fixed port number
6. Localhost-only binding
7. Debug mode always on

**Production best practices:**
- ✅ Environment variables for config
- ✅ Structured JSON logging
- ✅ Health check endpoints (`/health`, `/ready`)
- ✅ Graceful shutdown (SIGTERM handler)
- ✅ 0.0.0.0 binding for containers
- ✅ Dynamic port from env vars
- ✅ CORS configuration
- ✅ No secrets in code/logs

---

## 🧪 Testing

### Part 1 Tests

**Develop version:**
```bash
curl "http://localhost:8000/ask?question=Hello" -X POST
# Expected: {"answer": "Mock response..."}
```

**Production version:**
```bash
# Health check
curl http://localhost:8000/health
# Expected: {"status": "ok", "uptime_seconds": X, ...}

# Readiness check
curl http://localhost:8000/ready
# Expected: {"ready": true}

# API call
curl http://localhost:8000/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "Test"}'
# Expected: {"question": "Test", "answer": "...", "model": "gpt-4o-mini"}
```

---

## 🌐 Deployment

**Status:** 🚧 Not yet deployed

**Target Platform:** Railway (free $5 credit)

**Planned URL:** `https://vuong-ai-agent.railway.app`

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment information.

---

## 📚 Resources

- [Lab Instructions](CODE_LAB.md)
- [Mission Answers](MISSION_ANSWERS.md)
- [Deployment Info](DEPLOYMENT.md)
- [Submission Checklist](DAY12_DELIVERY_CHECKLIST.md)
- [12-Factor App](https://12factor.net/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 📧 Contact

**Student:** Tran Dinh Minh Vuong  
**Student ID:** 2A202600495  
**Course:** AICB-P1 · VinUniversity 2026

---

## 📄 License

This is a student project for educational purposes.

---

**Last Updated:** 17/04/2026  
**Status:** Part 1 Completed ✅ | Parts 2-6 In Progress 🚧
