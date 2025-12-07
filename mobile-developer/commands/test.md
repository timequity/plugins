---
description: Run mobile tests (unit, component, E2E)
---

# /mobile:test

Run mobile tests.

## Test Types

- **Unit** - Jest for logic
- **Component** - React Native Testing Library
- **E2E** - Detox or Maestro

## Commands

```bash
# Unit + Component
npm test

# E2E (Detox)
detox test --configuration ios.sim.debug

# E2E (Maestro)
maestro test flows/
```
