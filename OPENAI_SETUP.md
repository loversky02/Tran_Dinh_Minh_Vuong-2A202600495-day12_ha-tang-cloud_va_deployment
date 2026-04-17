# OpenAI Integration Guide

## Overview

Agent now supports **real OpenAI LLM** with automatic fallback to mock!

**Smart Fallback:**
- ✅ Has `OPENAI_API_KEY` → Uses OpenAI GPT-4o-mini
- ✅ No API key → Uses mock LLM (free, for testing)

**Zero breaking changes!** Agent works with or without OpenAI.

---

## Setup OpenAI (Optional)

### Step 1: Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-...`)

### Step 2: Add to Environment

**Local (.env file):**
```bash
OPENAI_API_KEY=sk-your-key-here
LLM_MODEL=gpt-4o-mini
MAX_TOKENS=500
```

**Railway (Dashboard):**
1. Go to your Railway project
2. Click "Variables" tab
3. Add:
   - `OPENAI_API_KEY` = `sk-your-key-here`
   - `LLM_MODEL` = `gpt-4o-mini` (optional)
   - `MAX_TOKENS` = `500` (optional)
4. Redeploy

### Step 3: Verify

```bash
# Check metrics endpoint
curl https://wonderful-delight-production-9390.up.railway.app/metrics

# Should show:
{
  "llm": {
    "type": "openai",
    "model": "gpt-4o-mini",
    "status": "active"
  }
}
```

---

## Test with OpenAI

```bash
curl -X POST https://wonderful-delight-production-9390.up.railway.app/ask \
  -H "X-API-Key: demo-key-change-me" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Docker?"}'
```

**Response (with OpenAI):**
```json
{
  "question": "What is Docker?",
  "answer": "Docker is a platform that enables developers to package applications into containers—standardized executable components combining application source code with the operating system libraries and dependencies required to run that code in any environment...",
  "platform": "Railway",
  "version": "2.0.0"
}
```

---

## Cost Estimation

**Model:** gpt-4o-mini  
**Pricing:**
- Input: $0.150 / 1M tokens
- Output: $0.600 / 1M tokens

**Example:**
- 1000 requests/day
- ~100 tokens input, ~200 tokens output per request
- Cost: ~$0.18/day = ~$5.40/month

**Free tier:** $5 credit for new accounts

---

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | None | OpenAI API key (required for real LLM) |
| `LLM_MODEL` | `gpt-4o-mini` | OpenAI model to use |
| `MAX_TOKENS` | `500` | Maximum tokens in response |

### Supported Models

- `gpt-4o-mini` (recommended) - Fast, cheap, good quality
- `gpt-4o` - Best quality, more expensive
- `gpt-3.5-turbo` - Cheaper, older

---

## Implementation Details

### Code Structure

**New file:** `utils/llm.py`
```python
from utils.llm import ask, get_llm_info

# Automatically uses OpenAI if available
answer = ask(question)

# Check current LLM type
info = get_llm_info()
# {"type": "openai", "model": "gpt-4o-mini", ...}
```

**Fallback logic:**
```python
if OPENAI_API_KEY:
    try:
        return openai_call(question)
    except Exception:
        return mock_llm(question)  # Fallback on error
else:
    return mock_llm(question)  # No API key
```

### Error Handling

- ✅ API key invalid → Falls back to mock
- ✅ Rate limit exceeded → Falls back to mock
- ✅ Network error → Falls back to mock
- ✅ No API key → Uses mock (no error)

---

## Monitoring

### Check LLM Status

```bash
curl https://wonderful-delight-production-9390.up.railway.app/metrics
```

### Logs (Railway)

```json
{"level":"INFO","msg":"OpenAI initialized with model: gpt-4o-mini"}
{"level":"INFO","msg":"OpenAI tokens: input=25, output=150, total=175"}
```

### Fallback Logs

```json
{"level":"WARNING","msg":"OpenAI call failed: Rate limit exceeded. Falling back to mock."}
{"level":"DEBUG","msg":"Using mock LLM (no OpenAI API key)"}
```

---

## FAQ

**Q: Do I need OpenAI for submission?**  
A: No! Mock LLM is perfectly fine for this lab.

**Q: Will it break if I don't add API key?**  
A: No! It automatically uses mock LLM.

**Q: Can I switch between OpenAI and mock?**  
A: Yes! Just add/remove `OPENAI_API_KEY` and restart.

**Q: What if I run out of credits?**  
A: Agent automatically falls back to mock LLM.

**Q: How to test locally with OpenAI?**  
A: Add `OPENAI_API_KEY` to `.env` file.

---

## Benefits of OpenAI Integration

✅ **Real AI responses** - Actual intelligent answers  
✅ **Production-ready** - Enterprise-grade LLM  
✅ **Automatic fallback** - Never breaks  
✅ **Cost-effective** - gpt-4o-mini is cheap  
✅ **Easy to enable** - Just add API key  
✅ **Zero code changes** - Same API interface  

---

## Submission

**For Day 12 Lab submission:**
- ✅ Mock LLM is acceptable (and recommended)
- ✅ OpenAI is optional bonus
- ✅ Both work perfectly

**Current status:**
- Agent deployed: ✅
- Mock LLM working: ✅
- OpenAI ready: ✅ (just add API key)

---

**Last Updated:** 17/04/2026  
**Version:** 2.1.0 with OpenAI support
