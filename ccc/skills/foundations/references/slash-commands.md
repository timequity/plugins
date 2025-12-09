# Slash Commands

## What Are Slash Commands?

Shortcuts that trigger specific actions. Type `/` to see them.

## Built-in Commands

| Command | What it does |
|---------|--------------|
| `/help` | Show all available commands |
| `/clear` | Reset conversation, keep context |
| `/config` | View or change settings |
| `/cost` | Show token usage and cost |
| `/doctor` | Diagnose Claude Code issues |
| `/init` | Create CLAUDE.md interactively |
| `/memory` | Manage persistent memories |
| `/review` | Review recent changes |
| `/vim` | Toggle vim keybindings |

## Using Commands

Just type the command:

```
You: /help
Claude: [shows command list]

You: /clear
Claude: [conversation cleared]

You: /config
Claude: [shows current configuration]
```

## Commands with Arguments

Some commands take input:

```
/review                    # review all recent changes
/review src/auth.ts        # review specific file
/memory add "prefer tabs"  # add a memory
```

## Custom Commands

Create your own in `.claude/commands/`:

```
your-project/
└── .claude/
    └── commands/
        └── test.md       # becomes /test
```

### Example: /test command

File: `.claude/commands/test.md`
```markdown
Run the test suite and report results.

1. Run `npm test`
2. If tests fail, show which ones
3. Suggest fixes for failures
```

Now `/test` runs your custom workflow.

### Example: /deploy command

File: `.claude/commands/deploy.md`
```markdown
Deploy to production:

1. Run tests first: `npm test`
2. If tests pass, run: `npm run build`
3. Deploy with: `npm run deploy`
4. Report the deployment URL
```

## Command Arguments

Use `$ARGUMENTS` placeholder:

File: `.claude/commands/review-pr.md`
```markdown
Review pull request #$ARGUMENTS

1. Fetch PR details: `gh pr view $ARGUMENTS`
2. Check the diff: `gh pr diff $ARGUMENTS`
3. Provide code review feedback
```

Usage: `/review-pr 123`

## Finding Commands

```
/help              # see all commands
/                  # type slash, see autocomplete
```

## Try It

1. Type `/help` to see available commands
2. Try `/config` to see your settings
3. Try `/clear` to reset (your CLAUDE.md stays loaded)

### Create Your First Command

1. Create `.claude/commands/hello.md`:
   ```markdown
   Say hello and list 3 fun facts about the current project.
   ```

2. Use it: `/hello`
