---
name: performance-profiling
description: Identify performance bottlenecks systematically. Measure before optimizing.
---

# Performance Profiling

## Core Principle

**Measure first. Optimize second. Verify third.**

Never optimize based on intuition. Profile to find actual bottlenecks.

## The Process

### 1. Establish Baseline

```bash
# Node.js
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Browser
Performance tab → Record → Analyze
```

### 2. Identify Bottlenecks

Look for:
- Functions with high "self time"
- Unexpected call counts
- Memory allocations in hot paths
- N+1 queries

### 3. Form Hypothesis

"Function X is slow because Y"

### 4. Optimize Minimally

One change at a time:
- Caching
- Algorithm improvement
- Batch operations
- Lazy loading

### 5. Verify Improvement

Compare against baseline. Must be measurably better.

## Common Bottlenecks

| Symptom | Likely Cause |
|---------|--------------|
| Slow page load | Large bundle, blocking resources |
| Slow API | N+1 queries, missing indexes |
| Memory growth | Leaks, unbounded caches |
| CPU spikes | Inefficient loops, regex |

## Tools

**Node.js:**
- `--prof` flag
- `clinic.js`
- `0x` flame graphs

**Browser:**
- DevTools Performance
- Lighthouse
- WebPageTest

**Database:**
- EXPLAIN ANALYZE
- Query logs
- Connection pool stats

## Red Flags

- Optimizing without profiling
- "I think this is slow"
- Premature optimization
- Micro-optimizations in cold paths
