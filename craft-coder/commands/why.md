---
description: Explain the last decision or any architectural choice
---

# /why - Decision Explanation

Explains the reasoning behind decisions made during project development.

## Usage

```
/why                    # Explain last decision
/why stack              # Explain stack choice
/why architecture       # Explain project structure
/why {specific}         # Explain specific decision
```

## Process

### 1. Identify What to Explain

If no argument provided:
- Check docs/DECISIONS.md for most recent ADR
- If no ADR exists, explain last significant action in conversation

If argument provided:
- Match against known decision categories
- Search docs/DECISIONS.md for related ADR

### 2. Decision Categories

#### Stack (`/why stack`)
```markdown
## Why {stack_name}?

**Your Requirements:**
- {requirement_1}
- {requirement_2}

**How {stack_name} Fits:**
- {fit_1}
- {fit_2}

**Alternatives Considered:**

| Option | Why Not? |
|--------|----------|
| {alt_1} | {reason} |
| {alt_2} | {reason} |

**Trade-offs Accepted:**
- {tradeoff_1}
- {tradeoff_2}

**Learn More:**
- [Official Docs]({url})
- [When to use {stack}]({article_url})
```

#### Architecture (`/why architecture`)
```markdown
## Why This Structure?

```
src/
├── lib.rs        # {explanation}
├── main.rs       # {explanation}
├── handlers/     # {explanation}
└── models/       # {explanation}
```

**Pattern Used:** {pattern_name}

**Why This Pattern?**
- {reason_1}
- {reason_2}

**Alternatives:**

| Pattern | When to Use Instead |
|---------|-------------------|
| {alt_1} | {scenario} |
| {alt_2} | {scenario} |

**YAGNI Applied:**
Things we intentionally skipped:
- {skipped_1}: Will add when {condition}
- {skipped_2}: Will add when {condition}
```

#### Database (`/why database`)
```markdown
## Why {database}?

**Your Data Characteristics:**
- {char_1}
- {char_2}

**{database} Strengths for This:**
- {strength_1}
- {strength_2}

**What We're NOT Using:**

| Database | Why Not? |
|----------|----------|
| {alt_1} | {reason} (overkill for {your_scale}) |
| {alt_2} | {reason} (doesn't support {feature}) |

**Migration Path:**
If you outgrow {database}:
1. {step_1}
2. {step_2}
```

#### Specific Library (`/why {library}`)
```markdown
## Why {library}?

**Problem Solved:** {problem}

**Comparison:**

| Library | Pros | Cons |
|---------|------|------|
| {library} (chosen) | {pros} | {cons} |
| {alt_1} | {pros} | {cons} |
| {alt_2} | {pros} | {cons} |

**Key Decision Factors:**
1. {factor_1}
2. {factor_2}

**Usage Example:**
```rust
// How we use {library}
{code_example}
```

**Resources:**
- [Docs]({url})
- [Best Practices]({url})
```

### 3. Read from DECISIONS.md

If docs/DECISIONS.md exists, parse ADRs:
```markdown
# Architecture Decision Records

## ADR-001: {title}
**Date:** {date}
**Status:** Accepted

**Context:** {context}

**Decision:** {decision}

**Consequences:**
- {consequence_1}
- {consequence_2}
```

Format for display:
```markdown
## ADR-001: {title}

**Context:** {context}

**We Decided:** {decision}

**Why?**
{extracted_rationale}

**What This Means:**
- {consequence_1}
- {consequence_2}

**Related:** ADR-002, ADR-003
```

### 4. If No Decision Found

```markdown
## No Recent Decisions

I don't have a specific decision to explain.

**Available topics:**
- `/why stack` — Technology choice
- `/why architecture` — Project structure
- `/why {file}` — Why a specific file exists

**Or ask specifically:**
- "Why did you use sqlx instead of diesel?"
- "Why is there no models/ directory?"
```

## Integration with /craft

During `/craft`, each decision is logged to docs/DECISIONS.md.
`/why` reads from this log to provide context.

## Output Format

Always include:
1. **The Decision** — What was chosen
2. **The Reasoning** — Why it was chosen
3. **Alternatives** — What else was considered
4. **Trade-offs** — What we gave up
5. **Resources** — Where to learn more

Keep explanations concise but complete.
