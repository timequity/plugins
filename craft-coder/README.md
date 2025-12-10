# Craft Coder

Pair programming with a senior dev: guided project creation, decision explanations, TDD workflow.

## Features

**50+ skills for serious developers:**

- **Backend**: Python, Node.js, Rust, core patterns
- **Frontend**: React, design systems, theme factory
- **Testing**: TDD, pytest, anti-patterns, debugging
- **DevOps**: CI/CD, monitoring, infrastructure
- **Data**: Pipelines, dbt, Airflow, Spark
- **Mobile**: React Native, Expo, offline-first
- **Infrastructure**: Terraform, Kubernetes, security

## Commands

| Command | Description |
|---------|-------------|
| `/craft-coder:craft` | Start guided project creation |
| `/craft-coder:why` | Explain a decision or pattern |

## Agents

- **code-reviewer** — Review code changes
- **tdd-test-writer** — Write tests first
- **rust-developer** — Rust-specific development
- **rust-code-reviewer** — Rust code review
- **rust-project-init** — Initialize Rust projects

## Installation

### Option 1: Download ZIP (Recommended)

1. Go to [Releases](../../releases)
2. Download the latest `craft-coder.zip`
3. Extract to `~/.claude/plugins/craft-coder/`

```bash
mkdir -p ~/.claude/plugins
cd ~/.claude/plugins
unzip ~/Downloads/craft-coder.zip -d craft-coder
```

### Option 2: Git Clone

```bash
cd ~/.claude/plugins
git clone https://github.com/timequity/craft-coder
```

### Verify Installation

Restart Claude Code and type `/craft-coder:craft`

## Requirements

- Claude Code CLI installed

## License

MIT

## Author

[timequity](https://github.com/timequity)
