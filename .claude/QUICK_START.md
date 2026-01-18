# Quick Start: System Instructions + GSD

## 30-Second Setup

### What You Have Now
✓ **System Instructions** (`.claude/settings.json`)
  - Project rules, tech constraints, quality gates
  - Active in EVERY Claude session automatically

✓ **Project Guide** (`.claude/PROJECT_GUIDE.md`)
  - Context, patterns, decision matrix
  - Reference when needed

✓ **Usage Examples** (`.claude/USAGE_EXAMPLES.md`)
  - Real scenarios for OMB-1
  - When to use what

### Install GSD (Optional, for Large Features)
```bash
npx get-shit-done-cc --local
# Adds .claude/commands/gsd/*.md
# Enables /gsd:* slash commands
```

---

## Quick Reference

### Simple Task (1-3 tasks, one file)
```
Just describe what you want:
"Add field X validation to quality checker"

Claude uses system instructions automatically:
→ Loads only needed files
→ Breaks into 2-3 tasks
→ Atomic commits
→ Tests before committing
```

### Medium Task (4-6 tasks, multiple files)
```
Structure your request:
"Add trend analysis

Task 1: Create comparison function
Task 2: Calculate growth metrics
Task 3: Generate report"

Claude follows GSD principles from instructions
```

### Large Feature (7+ tasks, multi-phase)
```
Use GSD commands:
/gsd:new-project
/gsd:create-roadmap
/gsd:plan-phase 1
/gsd:execute-plan

GSD uses system instructions for context
```

---

## Commands You'll Use

### Without GSD Installation
```
You type:     "Add validation for X"
Claude sees:  System instructions
Claude does:  Atomic workflow automatically
```

### With GSD Installation
```
You type:     /gsd:new-project
GSD asks:     Questions about feature
GSD reads:    System instructions for context
GSD creates:  Structured plan + roadmap
You type:     /gsd:execute-plan
GSD spawns:   Subagent following instructions
```

---

## Decision Tree

```
Need to add something to OMB-1?
│
├─ Is it 1-3 tasks in one file?
│  └─ YES → Use system instructions only
│           "Add X to quality_checker.py"
│
├─ Is it 4-6 tasks across 2-3 files?
│  └─ YES → Structure request with GSD principles
│           "Task 1: ... Task 2: ... Task 3: ..."
│
└─ Is it 7+ tasks, multi-phase, or needs research?
   └─ YES → Install GSD, use /gsd:* commands
            /gsd:new-project → /gsd:create-roadmap → execute
```

---

## What System Instructions Do For You

### Automatic Behavior
```
✓ Loads only relevant files (not entire codebase)
✓ Breaks work into 2-3 tasks max
✓ Uses atomic commits (one per task)
✓ Tests before committing (quality_checker.py)
✓ Follows project structure (validation/ directory)
✓ Respects constraints (Python stdlib, no deps)
✓ Applies quality gates (>95% completeness)
```

### Auto-Fix vs Ask
```
Auto-fixes:
✓ Data validation bugs
✓ Report formatting
✓ Missing field checks
✓ Security issues

Asks first:
⚠ Schema changes
⚠ New data sources
⚠ Breaking changes
⚠ Architecture decisions
```

---

## File Guide

| File | Purpose | When to Read |
|------|---------|--------------|
| `.claude/settings.json` | System instructions | Auto-loaded every session |
| `.claude/PROJECT_GUIDE.md` | Patterns & context | Reference when stuck |
| `.claude/USAGE_EXAMPLES.md` | Real scenarios | Learning how to use both |
| `.claude/QUICK_START.md` | This file | Quick reference |

---

## Common Workflows

### Workflow 1: Add Validation Rule
```bash
1. You: "Add validation for agency abbreviations"
2. Claude loads: data_dictionary.yaml, quality_checker.py
3. Claude creates: validation logic
4. Claude commits: feat(validation): add abbreviation validation
5. Claude tests: python3 validation/quality_checker.py
6. Claude reports: ✓ Done, 1 commit
```

### Workflow 2: Generate New Report Type
```bash
1. You: "Create agency compliance report"
2. Claude structures: 3 tasks (data collection, scoring, report)
3. Claude executes each task
4. Claude commits after each: feat(validation): ...
5. Claude generates: validation/COMPLIANCE_REPORT.md
6. Claude verifies: Report is accurate and readable
```

### Workflow 3: Build Multi-Phase Feature (with GSD)
```bash
1. You: /gsd:new-project
2. GSD: [Questions about feature]
3. GSD: Creates .planning/PROJECT.md
4. You: /gsd:create-roadmap
5. GSD: Creates phases (uses system instructions for structure)
6. You: /gsd:plan-phase 1
7. GSD: Creates atomic task plan
8. You: /gsd:execute-plan
9. GSD: Spawns subagent, executes, commits, creates checkpoint
10. Repeat for phases 2, 3, etc.
```

---

## Tips for Success

### Do This ✓
```
✓ Start with simple requests, let instructions guide
✓ Add task structure when complexity grows
✓ Install GSD for multi-phase features
✓ Read PROJECT_GUIDE.md when patterns unclear
✓ Check USAGE_EXAMPLES.md for similar scenarios
```

### Don't Do This ✗
```
✗ Override system instructions without reason
✗ Load entire CSV files (1757 rows) unnecessarily
✗ Modify data/ directory files directly
✗ Skip testing before commits
✗ Use GSD for simple 1-task changes
```

---

## Emergency Procedures

### If Something Breaks
```bash
# See what changed
git diff HEAD~1

# Revert last commit
git reset --hard HEAD~1

# Or use GSD rollback (if installed)
/gsd:rollback last
```

### If Context Gets Full
```
1. Commit current work
2. Start fresh session
3. Load only specific files needed
4. Continue with next task
```

### If Quality Score Drops
```bash
# Run quality checker
python3 validation/quality_checker.py

# See what failed
cat validation/QUALITY_REPORT.md

# Fix issues
# Commit: fix(validation): restore quality score to >95%
```

---

## Next Steps

### Just Starting?
```
1. Try a simple task: "Add field validation for X"
2. Watch how system instructions guide the work
3. Check git log to see atomic commits
4. Read USAGE_EXAMPLES.md for more patterns
```

### Ready for GSD?
```
1. Install: npx get-shit-done-cc --local
2. Try: /gsd:new-project with simple feature
3. See how it uses system instructions
4. Scale up to multi-phase work
```

### Want to Customize?
```
1. Edit .claude/settings.json (system instructions)
2. Add project-specific patterns
3. Update quality gates
4. Refine auto-fix vs ask rules
```

---

## Support

### Questions?
- Read: `.claude/PROJECT_GUIDE.md`
- Examples: `.claude/USAGE_EXAMPLES.md`
- GSD Docs: https://github.com/itsjwill/GSD-2.0-Get-Shit-Done-Cost-saver-

### Issues?
- Check git log for clean commits
- Verify quality_checker.py runs
- Review system instructions in settings.json
- Use /gsd:rollback if GSD installed

---

**Remember:**
> System instructions = Always active, automatic guidance
> GSD commands = On-demand workflow orchestration
> Together = Maximum productivity and quality

**Start simple. Scale up as needed. Let the tools guide you.**

---

*Quick reference for OMB-1 development with Claude*
