# Publishing Plugins

## The Journey

```
Idea → Build → Test → Package → Publish → Market
```

## Before You Publish

### Checklist

- [ ] Plugin solves a real problem
- [ ] All skills have clear descriptions
- [ ] Commands work correctly
- [ ] Help skill documents everything
- [ ] README explains value proposition
- [ ] Tested in real projects

## Plugin Quality

### Must Have
- Clear, specific purpose
- Working skills/commands
- No bugs in core functionality
- Helpful documentation

### Nice to Have
- Examples and tutorials
- Reference documentation
- Multiple use cases covered
- Quick start guide

## Packaging

### Directory structure
```
my-plugin/
├── .claude-plugin/
│   └── marketplace.json
├── SKILL.md              # Entry point
├── README.md             # For marketplace
├── skills/
│   ├── main-skill/
│   └── helper-skill/
├── commands/
│   └── main-command.md
├── agents/
│   └── worker-agent.md
└── help/
    └── SKILL.md
```

### marketplace.json

```json
{
  "name": "my-awesome-plugin",
  "version": "1.0.0",
  "description": "One compelling sentence about what this does.",
  "author": "your-name",
  "price": 5,
  "category": "development",
  "tags": ["specific", "relevant", "tags"],
  "skills": [
    "./skills/main-skill",
    "./skills/helper-skill",
    "./help"
  ],
  "agents": [
    "./agents/worker-agent.md"
  ]
}
```

### Writing descriptions

**Bad:**
> A plugin for developers.

**Good:**
> Debug React apps 10x faster. Systematic approach finds root causes, not symptoms. Includes component tree analyzer and state inspector.

**Formula:**
> [Benefit] + [How] + [What's included]

## Pricing Strategy

### Free ($0)
- Building audience
- Open source ethos
- Lead generation
- Community contribution

### Low ($1-5)
- Impulse buy
- High volume potential
- Lower expectations
- Good for niche tools

### Medium ($10-20)
- Professional tools
- Higher quality expected
- Support expected
- Regular updates

### Premium ($50+)
- Enterprise features
- Guaranteed support
- Regular updates
- Comprehensive solution

## Marketplace Submission

### Step 1: Prepare
```bash
# Verify structure
ls -la my-plugin/
cat my-plugin/.claude-plugin/marketplace.json
```

### Step 2: Test locally
Install your own plugin and test everything works.

### Step 3: Submit
Follow marketplace submission process (varies by platform).

### Step 4: Respond to feedback
Marketplace may request changes.

## Marketing Your Plugin

### Description optimization
- Lead with benefit, not feature
- Use specific numbers when possible
- Include social proof if available
- Clear call to action

### README structure
```markdown
# Plugin Name

One sentence: what problem this solves.

## Quick Start
How to get value in 60 seconds.

## Features
- Feature 1: benefit
- Feature 2: benefit
- Feature 3: benefit

## Examples
Real usage scenarios.

## FAQ
Common questions answered.
```

### Where to promote
- Twitter/X (dev community)
- Reddit (r/programming, niche subreddits)
- Hacker News (if genuinely useful)
- Dev.to / Hashnode articles
- YouTube tutorials
- Discord communities

## Updates and Maintenance

### Versioning
```
1.0.0 → 1.0.1  # Bug fix
1.0.0 → 1.1.0  # New feature
1.0.0 → 2.0.0  # Breaking change
```

### Changelog
```markdown
## [1.1.0] - 2024-01-15

### Added
- New skill for X
- Command /do-thing

### Fixed
- Bug in Y skill

### Changed
- Improved Z performance
```

### User feedback
- Respond to issues promptly
- Consider feature requests
- Thank users for feedback
- Update based on real usage

## Exercise: Prepare for Publishing

### Step 1: Audit your plugin
Check against the checklist above.

### Step 2: Write compelling description
Follow the formula: Benefit + How + What's included

### Step 3: Create README
Use the structure template.

### Step 4: Set your price
Consider your goals and audience.

### Step 5: Plan marketing
Pick 2-3 channels to focus on.

## Common Mistakes

### Don't
- Publish without testing
- Use vague descriptions
- Skip documentation
- Ignore user feedback
- Abandon after publishing

### Do
- Test thoroughly
- Write compelling copy
- Document everything
- Engage with users
- Update regularly

## Success Metrics

Track these after publishing:
- Install count
- User feedback (positive/negative)
- Support requests
- Feature requests
- Revenue (if paid)

Iterate based on data, not assumptions.
