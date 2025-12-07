---
description: Add data quality checks to a table or model
---

# /data:quality

Add quality checks using data-quality skill.

## Input Required

1. **Table/Model** - What to validate?
2. **Critical columns** - What must not be null?
3. **Business rules** - Domain-specific validations?

## Output

- dbt tests (schema.yml)
- Custom SQL tests if needed
- Great Expectations suite (optional)
