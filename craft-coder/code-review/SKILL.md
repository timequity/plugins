---
name: code-review
description: |
  Code review workflow and best practices.
  Use when: reviewing PRs, receiving feedback, or preparing code for review.
  Triggers: "code review", "review", "pr review", "pull request",
  "feedback", "review changes".
---

# Code Review

## Core Principle

**Technical correctness over social comfort.**

Don't say "Great point!" or "You're absolutely right!" — analyze the feedback technically and respond with substance.

## Review Checklist

```
□ Does it work? (logic, edge cases)
□ Is it secure? (injection, auth, secrets)
□ Is it tested? (coverage, edge cases)
□ Is it readable? (naming, structure)
□ Is it maintainable? (complexity, coupling)
□ Does it follow patterns? (consistency)
```

## Issue Severity

| Level | What | Action |
|-------|------|--------|
| **Critical** | Security holes, data loss, crashes | Must fix before merge |
| **Important** | Bugs, performance issues, bad patterns | Should fix |
| **Minor** | Style, naming, small improvements | Nice to have |
| **Nitpick** | Personal preference | Comment only, don't block |

## Giving Feedback

```markdown
# Good feedback format:

**Issue**: [What's wrong]
**Why**: [Why it matters]
**Suggestion**: [How to fix]

# Example:
**Issue**: SQL query uses string concatenation
**Why**: Vulnerable to SQL injection
**Suggestion**: Use parameterized queries:
`db.query('SELECT * FROM users WHERE id = $1', [userId])`
```

### Be Specific

```markdown
# BAD
"This code is confusing"

# GOOD
"The variable `data` doesn't describe what it contains.
Consider renaming to `userProfiles` to match its type."
```

### Praise Meaningfully

```markdown
# BAD
"LGTM!" (says nothing)

# GOOD
"Clean extraction of the validation logic into a separate function —
makes it much easier to test."
```

## Receiving Feedback

### Don't

- Take it personally
- Argue without investigating
- Dismiss without explanation
- Say "You're right!" without checking

### Do

- Investigate the concern technically
- Test the suggested approach
- Explain your reasoning if you disagree
- Ask clarifying questions

```markdown
# Good response to feedback:

"I tested this approach and [result].
The original implementation handles [edge case] because [reason].
However, your suggestion would work if we also [modification].
Should I make that change?"
```

## Verification Before Claiming Done

Before saying "done" or "fixed":

```bash
□ Run tests locally
□ Check the specific scenario mentioned
□ Verify the fix doesn't break related code
□ Test edge cases
```

## PR Description Template

```markdown
## What

[Brief description of changes]

## Why

[Motivation, link to issue]

## How

[Implementation approach]

## Testing

- [ ] Unit tests added/updated
- [ ] Manual testing done
- [ ] Edge cases covered

## Screenshots

[If UI changes]
```

## Quick Commands

```bash
# Prepare review (get diff stats)
git diff main...HEAD --stat
git log main..HEAD --oneline

# Review specific commits
git show <sha>
git diff <sha1>..<sha2>
```
