---
name: systematic-debugging
description: Four-phase debugging framework - root cause investigation, pattern analysis, hypothesis testing, implementation. No fixes without understanding.
---

# Systematic Debugging

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## The Four Phases

### Phase 1: Root Cause Investigation

1. **Read Error Messages** - Don't skip, they contain the solution
2. **Reproduce Consistently** - If not reproducible, gather more data
3. **Check Recent Changes** - Git diff, new dependencies
4. **Trace Data Flow** - Use root-cause-tracing skill

### Phase 2: Pattern Analysis

1. **Find Working Examples** - Similar code that works
2. **Compare Against References** - Read completely, don't skim
3. **Identify Differences** - List every difference

### Phase 3: Hypothesis Testing

1. **Form Single Hypothesis** - "X is root cause because Y"
2. **Test Minimally** - Smallest possible change
3. **One Variable at a Time** - Don't fix multiple things

### Phase 4: Implementation

1. **Create Failing Test** - Before fixing
2. **Implement Single Fix** - Root cause only
3. **Verify Fix** - Tests pass, issue resolved

## Red Flags - STOP

- "Quick fix for now"
- "Just try changing X"
- "I don't fully understand but..."
- Proposing solutions before tracing

**ALL mean: Return to Phase 1**

## If 3+ Fixes Failed

Question the architecture, not the symptoms.

## Quick Reference

| Phase | Success Criteria |
|-------|------------------|
| 1. Root Cause | Understand WHAT and WHY |
| 2. Pattern | Identify differences |
| 3. Hypothesis | Confirmed or rejected |
| 4. Implementation | Tests pass |
