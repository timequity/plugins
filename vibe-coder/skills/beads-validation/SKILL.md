---
name: beads-validation
description: |
  Validates beads issues after creation. Checks dependencies, PRD mapping, order.
  Use when: after creating issues in project-init, before TDD loop.
  Triggers: "validate beads", "check issues", "verify tasks".
---

# Beads Validation Skill

Validates that beads issues are correctly created and ready for TDD.

## When to Use

1. **After creating issues** (in rust-project-init):
   - Check all PRD features have corresponding issues
   - Check priorities are valid
   - Check issue IDs exist before adding dependencies

2. **Before TDD loop** (in /ship Phase 2.5):
   - Check for circular dependencies
   - Check `bd ready` returns expected first task
   - Check no issues are incorrectly blocked

## Validation Checks

### 1. PRD → Issues Mapping
```bash
# Count features in PRD
grep -c "^###\|^-" docs/PRD.md | head -1

# Count issues created
bd list --status=open | wc -l

# Each MVP feature should have an issue
```

### 2. Dependency Validity
```bash
# List all dependencies
bd list --status=open --json | jq '.[] | .dependencies'

# Check each dependency ID exists
bd show {dep_id}  # Should not error
```

### 3. Circular Dependency Check
```bash
# bd doctor checks for cycles
bd doctor
```

### 4. Ready State Check
```bash
# Should have at least one ready issue
bd ready --limit=1

# If empty, something is blocked incorrectly
```

### 5. Priority Validation
```bash
# All priorities should be 1, 2, or 3
bd list --json | jq '.[] | .priority' | sort -u
```

## Script Usage

```bash
# After creating issues
python3 scripts/validate_beads.py --check-created --prd docs/PRD.md

# Before TDD
python3 scripts/validate_beads.py --check-deps --check-ready
```

**Output:**
```
## Beads Validation

[PASS] PRD features: 4, Issues created: 4
[PASS] All dependency IDs exist
[PASS] No circular dependencies
[PASS] Ready queue has 1 issue (notes-abc)
[PASS] All priorities valid (1-3)

Result: 5/5 checks passed
```

## Common Issues

### No Ready Issues
```
[FAIL] No issues ready to work on
```
**Cause:** All issues blocked by dependencies
**Fix:** Check dependency chain, ensure at least one issue has no blockers

### Missing Features
```
[WARN] PRD has 5 features, only 3 issues created
```
**Fix:** Create missing issues with `bd create`

### Invalid Dependency
```
[FAIL] Dependency notes-xyz does not exist
```
**Fix:** Check issue ID before `bd dep add`

### Circular Dependency
```
[FAIL] Circular dependency: A → B → C → A
```
**Fix:** Remove one dependency to break cycle

## Integration

Called automatically in:
- `rust-project-init.md` → After creating issues
- `ship.md` → Phase 2.5: Before TDD loop
