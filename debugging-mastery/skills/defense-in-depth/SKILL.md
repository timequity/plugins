---
name: defense-in-depth
description: Validate at every layer to make bugs structurally impossible. Single validation isn't enough.
---

# Defense-in-Depth

## Core Principle

Single validation: "We fixed the bug"
Multiple layers: "We made the bug impossible"

## The Four Layers

### Layer 1: Entry Point
```typescript
function createProject(dir: string) {
  if (!dir) throw new Error('dir required');
  if (!existsSync(dir)) throw new Error('dir not found');
}
```

### Layer 2: Business Logic
```typescript
function initWorkspace(projectDir: string) {
  if (!projectDir) throw new Error('projectDir required');
}
```

### Layer 3: Environment Guards
```typescript
if (process.env.NODE_ENV === 'test') {
  if (!dir.startsWith(tmpdir())) {
    throw new Error('Refusing dangerous operation in tests');
  }
}
```

### Layer 4: Debug Instrumentation
```typescript
logger.debug('About to git init', {
  directory,
  cwd: process.cwd(),
  stack: new Error().stack,
});
```

## Application

1. Trace data flow
2. Map all checkpoints
3. Add validation at each layer
4. Test each layer independently

All four layers are necessary. Each catches what others miss.
