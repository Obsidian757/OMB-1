# Using System Instructions + GSD Together

## Real-World Examples for OMB-1

---

## Example 1: Small Enhancement (System Instructions Only)

### Scenario
Add agency abbreviation validation to quality checker.

### How System Instructions Help
```
Claude automatically:
✓ Loads only data_dictionary.yaml + quality_checker.py
✓ Breaks into 2 tasks (validation logic, report update)
✓ Uses atomic commits per task
✓ Tests with quality_checker.py before committing
✓ Stays under 50% context usage
```

### Your Request
```
"Add validation for agency abbreviations. Check that 3_abr field
matches known abbreviations from data dictionary."
```

### Claude's Response (Guided by Instructions)
```
I'll break this into 2 tasks:

Task 1: Add abbreviation validation logic
  Files: validation/quality_checker.py
  Action: Load valid abbreviations from data dict, validate in loop
  Verify: Run quality_checker.py, see new validation output

Task 2: Add abbreviation report to markdown
  Files: validation/quality_checker.py
  Action: Update generate_markdown_report() with abbreviation section
  Verify: Check QUALITY_REPORT.md has new section

[Executes Task 1]
[Commits: feat(validation): add agency abbreviation validation]
[Executes Task 2]
[Commits: feat(validation): report invalid abbreviations in output]

✓ Done. 2 commits, tested, quality score maintained.
```

**Git History:**
```
abc123 feat(validation): report invalid abbreviations in output
def456 feat(validation): add agency abbreviation validation
```

---

## Example 2: Medium Feature (System Instructions + Manual GSD Principles)

### Scenario
Add trend analysis comparing 2023 vs 2024 inventories.

### How to Use Both
```
System Instructions provide:
- Project structure (data/ validation/)
- Quality gates (>95% completeness)
- Atomic commit rules

You apply GSD principles manually:
- Break into 3 tasks
- Fresh context per task
- Structured requests
```

### Your Request
```
"Add trend analysis tool comparing 2023 and 2024 inventories.

Task 1: Create CSV comparison function
  Files: validation/trend_analyzer.py (new)
  Action: Load both CSVs, compare agency counts and use case totals
  Verify: python3 validation/trend_analyzer.py shows differences

Task 2: Calculate growth metrics
  Files: validation/trend_analyzer.py
  Action: Add percentage changes, new agencies, new use cases
  Verify: Metrics match manual calculation

Task 3: Generate trend report
  Files: validation/trend_analyzer.py
  Action: Create markdown report with year-over-year changes
  Verify: validation/TREND_REPORT.md is accurate and readable"
```

### Claude's Response
```
[Sees system instructions: minimal dependencies, markdown reports, atomic commits]

Task 1: Creating comparison function...
[Uses system instructions for file structure, coding standards]
[Commits: feat(validation): create CSV comparison function]

Task 2: Adding growth metrics...
[Applies type hints per instructions]
[Commits: feat(validation): add year-over-year growth metrics]

Task 3: Generating trend report...
[Follows markdown format from QUALITY_REPORT.md]
[Commits: feat(validation): generate trend analysis report]

✓ 3 atomic commits, all tests passed, report generated.
```

**Git History:**
```
ghi789 feat(validation): generate trend analysis report
abc456 feat(validation): add year-over-year growth metrics
def123 feat(validation): create CSV comparison function
```

---

## Example 3: Large Feature (Full GSD Workflow)

### Scenario
Build a compliance checker for EO 13960 requirements.

### Why Use Full GSD Here
```
- Multi-phase work (parsing, validation, reporting, testing)
- Complex requirements (multiple compliance criteria)
- Needs structured planning
- Benefits from git checkpoints
- May need research phase
```

### Installation
```bash
cd /home/user/OMB-1
npx get-shit-done-cc --local
```

### Full Workflow

#### Step 1: Initialize Project
```
/gsd:new-project

GSD: "What do you want to build?"
You: "Add EO 13960 compliance checker to validate agency submissions"

GSD: "What makes a submission compliant?"
You: "Must have all required fields, impact assessment for rights-impacting
     cases, and documentation for high-risk AI systems"

GSD: "Any technical constraints?"
[GSD sees system instructions: Python 3.x, no dependencies]
You: "Use system instructions - Python stdlib only, minimal dependencies"

GSD: "What's explicitly NOT in v1?"
You: "No automated remediation, no email notifications, just validation
     and reporting"

GSD: "Ready to create PROJECT.md?"
You: "Yes"

[GSD creates .planning/PROJECT.md using system instructions as context]
```

#### Step 2: Create Roadmap
```
/gsd:create-roadmap

GSD analyzes system instructions + PROJECT.md
Creates roadmap:

Phase 1: EO Requirements Parser
  - Parse EO 13960 requirements
  - Map to data dictionary fields
  - Create compliance schema

Phase 2: Compliance Validator
  - Check required fields per use case type
  - Validate impact assessments
  - Check documentation requirements

Phase 3: Compliance Reporting
  - Generate per-agency compliance reports
  - Summary compliance dashboard
  - Remediation recommendations

[Respects system instructions: files in validation/, markdown reports]
```

#### Step 3: Execute Phases
```
/gsd:plan-phase 1

GSD creates atomic plan:
  Task 1: Parse EO requirements from reference docs
  Task 2: Map requirements to data dictionary fields
  Task 3: Create compliance schema YAML

[Each task has clear success criteria from system instructions]

/gsd:execute-plan

GSD spawns subagent:
- Uses system instructions for quality gates
- Atomic commits per task
- Tests with compliance_checker.py
- Generates SUMMARY.md

[Creates git checkpoints: gsd-checkpoint-01-01-pre/post]

Phase 1 Complete:
  3 commits created
  Checkpoint tagged
  Summary documented
```

**Git History After All Phases:**
```
abc123 docs(03-02): complete compliance reporting plan
def456 feat(validation): add remediation recommendations
ghi789 feat(validation): generate compliance dashboard
jkl012 feat(validation): create per-agency compliance reports

mno345 docs(02-03): complete compliance validator plan
pqr678 test(validation): add compliance validator tests
stu901 feat(validation): check documentation requirements
vwx234 feat(validation): validate impact assessments
yza567 feat(validation): check required fields by type

bcd890 docs(01-03): complete requirements parser plan
efg123 feat(validation): create compliance schema
hij456 feat(validation): map requirements to data dictionary
klm789 feat(validation): parse EO requirements
```

---

## Example 4: Emergency Rollback (GSD Safety Features)

### Scenario
Phase 2 of compliance checker broke the quality_checker.py

### Using GSD Rollback
```
/gsd:rollback last

GSD shows:
  "Rollback to: gsd-checkpoint-02-01-pre

  This will undo:
    • 4 commits
    • 3 files changed

  Commits to be undone:
    abc123 feat(validation): validate impact assessments
    def456 feat(validation): check required fields
    ghi789 test(validation): add validator tests
    jkl012 docs(02-01): complete validator plan"

You: "Yes, rollback"

GSD:
  ✓ Created backup: gsd-rollback-backup-20260118104500
  ✓ Reset to gsd-checkpoint-02-01-pre
  ✓ Updated STATE.md

  You're back to Phase 2 start.
  Fix the issue and re-run /gsd:execute-plan
```

### System Instructions Still Active
```
After rollback:
✓ Project rules still apply
✓ Quality gates still enforced
✓ Atomic commits still required
✓ Can manually fix or re-plan phase
```

---

## Example 5: Progressive Enhancement

### Scenario
Gradually improve quality_checker.py over multiple sessions.

### Session 1: Add Field Type Validation (Instructions Only)
```
You: "Add field type validation"

[2 tasks, 2 commits]
✓ feat(validation): add type parser
✓ feat(validation): validate field types
```

### Session 2: Add Enum Validation (Instructions Only)
```
You: "Add enum validation for topic_area field"

[2 tasks, 2 commits]
✓ feat(validation): extract enum constraints
✓ feat(validation): validate topic_area enums
```

### Session 3: Build Validation Suite (Start Using GSD)
```
You: "/gsd:new-project"
    "Build comprehensive validation suite with all checks"

/gsd:map-codebase
[GSD scans validation/ directory]
[Sees existing validation work]

/gsd:create-roadmap
Phase 1: Consolidate existing validators
Phase 2: Add missing validators (date format, PII detection)
Phase 3: Create validation CLI
Phase 4: Add automated testing

[GSD builds on existing work, respects system instructions]
```

**Result:**
```
Early work: Manual with system instructions (fast, simple)
Later work: GSD orchestration (complex, multi-phase)
Both: Follow same quality standards, atomic commits, testing
```

---

## Decision Matrix: When to Use What

| Task Complexity | Use System Instructions | Use GSD Commands | Why |
|----------------|------------------------|------------------|-----|
| **1-3 tasks, single file** | ✓ | | Fast, no overhead |
| **4-6 tasks, 2-3 files** | ✓ + GSD principles | | Structured but manual |
| **7+ tasks, multi-phase** | Context | ✓ Full workflow | Orchestration needed |
| **Research needed** | Context | ✓ /gsd:research-phase | GSD has research tools |
| **Experimental work** | ✓ | ✓ /gsd:rollback | Checkpoints for safety |
| **Maintenance/fixes** | ✓ | | Simple, direct |
| **Greenfield features** | Context | ✓ Full workflow | Planning + execution |
| **Brownfield enhancements** | Context | ✓ /gsd:map-codebase | Understand existing code |

---

## Best Practices

### 1. Start with Instructions, Escalate to GSD
```
Small task → System instructions only
Growing complexity → Add GSD principles manually
Large feature → Full GSD workflow
```

### 2. Let System Instructions Guide GSD
```
GSD asks: "What tech stack?"
GSD reads: .claude/settings.json
GSD applies: Python 3.x, no deps, validation/ structure
```

### 3. Use GSD Checkpoints for Experiments
```
Trying new approach?
→ /gsd:execute-plan (creates checkpoint)
→ Experiment
→ Works? Keep it
→ Breaks? /gsd:rollback last
```

### 4. Keep Instructions Focused
```
System instructions:
✓ Project-specific rules
✓ Tech constraints
✓ Quality gates
✗ Not workflow steps (GSD handles that)
✗ Not documentation (separate files)
```

### 5. Update Instructions as Project Evolves
```
New pattern emerges?
→ Add to system instructions

New quality gate needed?
→ Update .claude/settings.json

New tool added?
→ Document in PROJECT_GUIDE.md
```

---

## Troubleshooting

### "Claude ignores my system instructions"
```
Problem: Instructions too generic
Fix: Be specific with file paths, commands, criteria

Bad: "Use good code quality"
Good: "Type hints required on public methods. Test with: python3 validation/script.py"
```

### "GSD plans don't match my project"
```
Problem: GSD doesn't see system instructions
Fix: Reference instructions in your /gsd:new-project responses

GSD: "What tech stack?"
You: "See .claude/settings.json - Python 3.x stdlib only"
```

### "Too many commits"
```
Problem: Task scope too small
Fix: Combine related changes into one task

Bad: 3 tasks for 3 lines of code
Good: 1 task for complete feature unit
```

### "Context keeps filling up"
```
Problem: Loading too much
Fix: Follow PROJECT_GUIDE.md context loading strategy

Don't load: Full CSVs, git history
Do load: Specific files you'll modify
```

---

## Summary

**System Instructions:**
- Always active
- Project-specific rules
- Quality standards
- Guides every response

**GSD Commands:**
- On-demand workflow
- Multi-phase orchestration
- Git checkpoints
- Progress tracking

**Together:**
```
System Instructions = The rules of the road
GSD Commands = GPS navigation system

Both help you reach destination faster and safer.
```

**Golden Rule:**
> Start simple (instructions only), scale up to GSD as complexity grows.

---

*Examples based on actual OMB-1 development patterns*
