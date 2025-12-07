---
description: Write a blameless postmortem document for an incident
---

# /debug:postmortem

Create a root cause analysis document using postmortem-writing skill.

## Template

```markdown
# Postmortem: [Title]

**Date:** YYYY-MM-DD
**Severity:** P1/P2/P3

## Summary
[What happened and impact]

## Timeline
- HH:MM - Event
- HH:MM - Detection
- HH:MM - Resolution

## Root Cause
[Technical explanation using 5 Whys]

## Impact
- Users affected: X
- Duration: Y hours

## What Went Well
- [Positive observations]

## What Went Wrong
- [Areas for improvement]

## Action Items
| Action | Owner | Due |
|--------|-------|-----|
| Fix X | @name | date |
```

## Principles

- **Blameless** - Focus on systems, not people
- **Actionable** - Every finding has an action item
- **Honest** - Don't minimize or exaggerate
