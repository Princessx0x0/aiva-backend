# Architecture Decision Records (ADRs)

## ADR-001: Use Gemini API Free Tier
**Date:** January 2026  
**Status:** Accepted  
**Context:** Need AI capabilities for AIVA insights without upfront costs  
**Decision:** Use Gemini API free tier (20 req/min limit)  
**Consequences:**
- No costs during development
- Easy to upgrade later
- Rate limits require client-side protection
- Not suitable for high-traffic production

---

## ADR-002: Deploy to Cloud Run (Serverless)
**Date:** January 2026  
**Status:** Accepted  
**Context:** Need production-grade infrastructure without managing servers  
**Decision:** Use Google Cloud Run for serverless container hosting  
**Consequences:**
- Auto-scaling (0-10 instances)
- Pay-per-use pricing
- Managed SSL certificates
- 99.95% SLA
- 60-second request timeout limit
- Requires container expertise

---

## ADR-003: Separate Health Endpoints
**Date:** January 2026  
**Status:** Accepted  
**Context:** Need to distinguish between service health and dependency health  
**Decision:** Implement two health endpoints:
- `/health` - Fast, no external deps (for Cloud Run)
- `/health/ai` - Includes external dependency checks (for monitoring)  
**Consequences:**
- Cloud Run health checks always fast
- Can monitor AI service separately
- Service stays "healthy" even if AI is down

---

## ADR-004: Reduce Container Concurrency to 5
**Date:** January 27, 2026  
**Status:** Accepted  
**Context:** Load test revealed queue buildup with default 80 concurrency  
**Decision:** Reduce concurrency to 5 requests per container  
**Consequences:**
- Faster horizontal scaling under load
- Less queue buildup
- More predictable behavior
- More containers needed (higher cost at scale)
- More cold starts

---

## ADR-005: Implement Circuit Breaker for Gemini API
**Date:** January 27, 2026  
**Status:** Proposed  
**Context:** Cascading failure when Gemini API rate limits are hit  
**Decision:** Add circuit breaker that fast-fails during Gemini cooldown periods  
**Consequences:**
- Prevents resource exhaustion
- Faster failure response
- Service stays responsive when AI is unavailable
- Adds code complexity
- Requires global state management