---
description: Start systematic debugging for any bug, test failure, or unexpected behavior
---

# /debug:investigate

Start the four-phase debugging process. Use the systematic-debugging skill.

## Process

1. **Phase 1: Root Cause Investigation**
   - Read error messages completely
   - Reproduce the issue consistently
   - Check recent changes (git diff)
   - Gather evidence at component boundaries

2. **Phase 2: Pattern Analysis**
   - Find similar working code
   - Compare differences
   - Understand dependencies

3. **Phase 3: Hypothesis Testing**
   - Form single hypothesis
   - Test minimally
   - One variable at a time

4. **Phase 4: Implementation**
   - Create failing test first
   - Implement fix
   - Verify resolution

## Important

- NO FIXES until Phase 1 complete
- If 3+ fixes fail, question architecture
- Use root-cause-tracing for deep errors
