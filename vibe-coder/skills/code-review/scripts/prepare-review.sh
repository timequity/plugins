#!/bin/bash
# Prepare code review context
# Usage: ./prepare-review.sh [base-branch]

BASE=${1:-main}
HEAD=$(git rev-parse HEAD)
BASE_SHA=$(git merge-base $BASE HEAD)

echo "## Review Context"
echo ""
echo "**Base:** $BASE ($BASE_SHA)"
echo "**Head:** $HEAD"
echo ""

echo "## Changed Files"
echo "\`\`\`"
git diff $BASE_SHA..HEAD --stat
echo "\`\`\`"
echo ""

echo "## Commits"
echo "\`\`\`"
git log $BASE_SHA..HEAD --oneline
echo "\`\`\`"
echo ""

echo "## Diff Summary"
echo ""
echo "- Lines added: $(git diff $BASE_SHA..HEAD --shortstat | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+')"
echo "- Lines removed: $(git diff $BASE_SHA..HEAD --shortstat | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+')"
echo ""

echo "## Review Command"
echo "\`\`\`"
echo "git diff $BASE_SHA..$HEAD"
echo "\`\`\`"
