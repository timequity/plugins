---
name: debugging-mastery
description: Systematic debugging framework for senior developers. Stop random fix attempts, start finding root causes.
---

# Debugging Mastery

Transform chaotic debugging into systematic problem-solving.

## Philosophy

**Random fixes waste time and create new bugs.**

This plugin provides a structured approach:
1. Find root cause BEFORE attempting fixes
2. Trace problems to their source
3. Make bugs structurally impossible
4. Document for future prevention

## Skills

| Skill | When to Use |
|-------|-------------|
| **systematic-debugging** | Any bug, test failure, unexpected behavior |
| **root-cause-tracing** | Error deep in call stack |
| **defense-in-depth** | After fixing, prevent recurrence |
| **condition-based-waiting** | Flaky tests with timing issues |
| **testing-anti-patterns** | Writing or reviewing tests |
| **performance-profiling** | Slow code, bottlenecks |
| **postmortem-writing** | Document RCA for team |

## Commands

| Command | Purpose |
|---------|---------|
| `/debug:investigate` | Start systematic debugging process |
| `/debug:trace` | Trace error to root cause |
| `/debug:flaky` | Fix flaky test |
| `/debug:postmortem` | Write RCA document |

## The Four Phases

### Phase 1: Root Cause Investigation
- Read error messages carefully
- Reproduce consistently
- Check recent changes
- Trace data flow

### Phase 2: Pattern Analysis
- Find working examples
- Compare against references
- Identify differences

### Phase 3: Hypothesis Testing
- Form single hypothesis
- Test minimally
- Verify before continuing

### Phase 4: Implementation
- Create failing test
- Implement single fix
- Verify fix works

## Impact

- Systematic approach: 15-30 minutes to fix
- Random fixes: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common
