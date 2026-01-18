# System Instructions + GSD Full Integration Guide

## What You Have Now

### 1. **System Instructions** (Always Active)
`.claude/settings.json` - Auto-loaded every Claude session
- Project rules, tech constraints, quality gates
- Auto-fix vs ask decision rules
- GSD-compatible atomic workflow
- OMB-1 specific context

### 2. **GSD Commands** (22 Slash Commands)
`.claude/commands/gsd/*.md` - Available on-demand
- `/gsd:new-project` - Initialize with deep questioning
- `/gsd:create-roadmap` - Generate phase breakdown
- `/gsd:plan-phase` - Create atomic task plans
- `/gsd:execute-phase` - Spawn subagent execution
- `/gsd:map-codebase` - Analyze existing code
- Plus 17 more workflow commands

### 3. **GSD System** (Workflow Engine)
`.claude/get-shit-done/` - Context engineering
- `workflows/` - Execution patterns
- `templates/` - Project/plan/summary templates
- `references/` - Principles, git integration, TDD

### 4. **Documentation** (Your Guides)
`.claude/*.md` - Reference materials
- `PROJECT_GUIDE.md` - Patterns & decision matrix
- `USAGE_EXAMPLES.md` - Real OMB-1 scenarios
- `QUICK_START.md` - Quick reference
- `INTEGRATION_GUIDE.md` - This file

---

## How They Work Together

```
┌─────────────────────────────────────────────────────────┐
│                    EVERY CLAUDE SESSION                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. System Instructions Load Automatically              │
│     ├─ OMB-1 project context                           │
│     ├─ Tech constraints (Python, no deps)              │
│     ├─ Quality gates (>95% completeness)               │
│     ├─ Atomic workflow rules                           │
│     └─ Auto-fix vs ask rules                           │
│                                                         │
│  2. GSD Commands Available                             │
│     ├─ /gsd:new-project                                │
│     ├─ /gsd:plan-phase                                 │
│     ├─ /gsd:execute-phase                              │
│     └─ 19 more commands                                │
│                                                         │
│  3. Both Use Same Principles                           │
│     ├─ Atomic commits (one per task)                   │
│     ├─ Context control (<50% usage)                    │
│     ├─ Quality gates enforcement                       │
│     └─ Test before commit                              │
│                                                         │
└─────────────────────────────────────────────────────────┘

           System Instructions = Autopilot
           GSD Commands = Flight Computer
           Both = Same Flight Plan
```

---

## Workflow Scenarios

### Scenario 1: Simple Task (Instructions Only)

**When:** 1-3 tasks, single file, quick change

**Example:**
```
You: "Add date format validation to quality_checker.py"

Claude (sees system instructions):
  ✓ Loads only: data_dictionary.yaml, quality_checker.py
  ✓ Breaks into 2 tasks (parse format, validate values)
  ✓ Commits after each task
  ✓ Tests with quality_checker.py
  ✓ Maintains >95% completeness

Result: 2 atomic commits, tested, done
```

**System Instructions Active:**
- Atomic workflow (2-3 tasks max)
- Type hints required
- Test before commit
- Validation/ directory structure

**GSD Commands:** Not needed

---

### Scenario 2: Medium Task (Instructions + GSD Principles)

**When:** 4-6 tasks, 2-3 files, needs structure

**Example:**
```
You: "Add CSV comparison tool for 2023 vs 2024 inventories

Task 1: Create comparison function
Task 2: Calculate growth metrics
Task 3: Generate trend report"

Claude (sees system instructions):
  ✓ Follows validation/ structure
  ✓ Python stdlib only (no pandas)
  ✓ Markdown report output
  ✓ Atomic commits per task
  ✓ Tests before each commit

Result: 3 commits, following GSD principles manually
```

**System Instructions Active:**
- All project rules
- Quality gates
- Code standards

**GSD Commands:** Not invoked, but principles applied

---

### Scenario 3: Large Feature (Full GSD Workflow)

**When:** 7+ tasks, multi-phase, needs planning

**Example:**
```
You: /gsd:new-project

GSD: "What do you want to build?"
You: "Add EO 13960 compliance checker"

GSD (reads system instructions):
  ✓ Sees: validation/ directory structure
  ✓ Sees: Python stdlib preference
  ✓ Sees: >95% quality gate requirement
  ✓ Sees: Markdown report format
  ✓ Creates PROJECT.md respecting constraints

GSD: "What tech stack?"
[Already knows from system instructions: Python 3.x, no deps]

GSD: Creates roadmap:
  Phase 1: Requirements parser (validation/compliance_parser.py)
  Phase 2: Compliance validator (validation/compliance_checker.py)
  Phase 3: Compliance reporting (validation/COMPLIANCE_REPORT.md)

You: /gsd:plan-phase 1

GSD (uses system instructions):
  Task 1: Parse EO requirements
    Files: validation/compliance_parser.py (respects structure)
    Verify: python3 validation/compliance_parser.py (runnable script)
    Done: Returns dict with requirements

  Task 2: Map to data dictionary
    Files: validation/compliance_parser.py
    Test: Validates against data_dictionary.yaml (source of truth)

  Task 3: Create compliance schema
    Files: validation/compliance_schema.yaml
    Quality: Maintain >95% completeness

You: /gsd:execute-phase

GSD spawns subagent:
  ✓ Loads: validation/data_dictionary.yaml (from instructions)
  ✓ Creates: validation/compliance_parser.py
  ✓ Commits: feat(validation): parse EO requirements
  ✓ Tests: python3 validation/compliance_parser.py
  ✓ Commits: feat(validation): map requirements to data dict
  ✓ Tests again
  ✓ Commits: feat(validation): create compliance schema
  ✓ Creates: .planning/phases/01-requirements/01-01-SUMMARY.md
  ✓ Commits: docs(01-01): complete requirements parser plan
  ✓ Tags: gsd-checkpoint-01-01-pre/post

Result: 4 atomic commits, git checkpoint, tested, documented
```

**System Instructions Active:**
- All project rules enforced
- GSD reads and follows them
- Quality gates applied automatically

**GSD Commands:** Full workflow orchestration

---

## Integration Benefits

### 1. **System Instructions Guide GSD**

GSD commands see your system instructions and automatically:

```yaml
GSD sees: "validation/ - All quality checking code"
GSD creates: validation/compliance_checker.py (not src/validators/)

GSD sees: "Python stdlib preferred"
GSD avoids: import pandas, import requests

GSD sees: "Test before committing: python3 validation/script.py"
GSD runs: python3 validation/compliance_checker.py before commit

GSD sees: "Completeness score >95%"
GSD validates: Quality gate before marking task complete
```

### 2. **GSD Enhances Instructions**

System instructions say "atomic commits" → GSD provides:
- Git checkpoints before/after phases
- Rollback capability: `/gsd:rollback last`
- Recovery: `/gsd:recover` for interrupted work

System instructions say "test before commit" → GSD provides:
- Automated testing in subagent
- Verification criteria in plan format
- Quality validation before completion

### 3. **Consistent Behavior**

Whether you use:
- **Just ask** → Instructions guide the work
- **Structure request** → Instructions + GSD principles
- **GSD commands** → Instructions + GSD orchestration

**Result:** Same quality standards, same atomic commits, same testing

---

## Command Reference

### Available GSD Commands

#### Project Initialization
```bash
/gsd:new-project              # Deep context gathering (uses system instructions)
/gsd:map-codebase            # Analyze existing code (brownfield)
```

#### Planning
```bash
/gsd:create-roadmap          # Generate phase breakdown
/gsd:plan-phase N            # Create atomic task plans for phase
/gsd:discuss-phase N         # Gather context before planning
/gsd:list-phase-assumptions  # See what GSD thinks
```

#### Execution
```bash
/gsd:execute-phase           # Run plan via subagent (respects instructions)
/gsd:check-todos             # Track progress
```

#### Milestone Management
```bash
/gsd:complete-milestone      # Ship v1, prep v2
/gsd:new-milestone           # Start new version
/gsd:audit-milestone         # Review milestone quality
```

#### Phase Management
```bash
/gsd:add-phase              # Append phase to roadmap
/gsd:insert-phase N         # Insert urgent work
```

#### Safety & Recovery
```bash
/gsd:pause-work             # Create handoff file
/gsd:rollback last          # Undo last plan
/gsd:debug                  # Diagnose issues
```

#### Help
```bash
/gsd:help                   # Show all commands
```

---

## Real Example: Building Compliance Checker

Let's walk through a complete feature using both systems.

### Step 1: Initialize Project with GSD

```
/gsd:new-project

GSD: "What do you want to build?"
You: "EO 13960 compliance checker for federal AI use cases"

GSD: "What does it need to do?"
You: "Validate that agency submissions meet EO requirements:
      - Required fields present
      - Impact assessments for rights-impacting AI
      - Documentation for high-risk systems
      - Proper categorization"

GSD: "Any technical constraints?"
You: "See system instructions - Python stdlib only, validate against
     data_dictionary.yaml, output to validation/COMPLIANCE_REPORT.md"

GSD (reads .claude/settings.json):
  ✓ Sees: validation/ directory structure
  ✓ Sees: Python 3.x stdlib only
  ✓ Sees: data_dictionary.yaml is source of truth
  ✓ Sees: Markdown report format
  ✓ Sees: >95% quality requirement

GSD: "What's NOT in v1?"
You: "No automated remediation, no email alerts, just validation"

GSD: "Ready to create PROJECT.md?"
You: "Yes"

[Creates .planning/PROJECT.md]
```

### Step 2: Create Roadmap

```
/gsd:create-roadmap

GSD (uses system instructions):
  Creates roadmap respecting project structure:

  Phase 1: EO Requirements Parser
    Goal: Parse EO 13960 requirements
    Files: validation/compliance_parser.py
    Output: compliance_requirements.yaml

  Phase 2: Compliance Validator
    Goal: Validate submissions against requirements
    Files: validation/compliance_checker.py
    Validates: Against data_dictionary.yaml (per instructions)
    Quality: Maintain >95% completeness

  Phase 3: Compliance Reporting
    Goal: Generate compliance reports
    Files: validation/COMPLIANCE_REPORT.md
    Format: Markdown (per instructions)
    Style: Match QUALITY_REPORT.md structure

[Creates .planning/ROADMAP.md, .planning/STATE.md]
```

### Step 3: Plan Phase 1

```
/gsd:plan-phase 1

GSD creates plan (respecting system instructions):

.planning/phases/01-requirements/01-01-PLAN.md:

<plan>
  <phase>1</phase>
  <name>EO Requirements Parser</name>
  <goal>Parse EO 13960 compliance requirements</goal>

  <context>
    @validation/data_dictionary.yaml   # From instructions
    @.claude/settings.json             # System instructions
  </context>

  <tasks>
    <task type="auto">
      <name>Parse EO 13960 requirements</name>
      <files>validation/compliance_parser.py</files>
      <action>
        - Extract required fields from EO text
        - Map to data_dictionary.yaml fields
        - Use Python stdlib only (per instructions)
        - Type hints required (per instructions)
      </action>
      <verify>
        python3 validation/compliance_parser.py --help
        # Per instructions: scripts must be runnable
      </verify>
      <done>
        Returns dict with EO requirements mapped to data fields
      </done>
    </task>

    <task type="auto">
      <name>Create compliance schema</name>
      <files>validation/compliance_schema.yaml</files>
      <action>
        - Define compliance rules in YAML format
        - Reference data_dictionary.yaml (source of truth)
        - Include field requirements per use case type
      </action>
      <verify>
        python -c "import yaml; yaml.safe_load(open('validation/compliance_schema.yaml'))"
      </verify>
      <done>
        Valid YAML schema defining compliance rules
      </done>
    </task>

    <task type="auto">
      <name>Add compliance check function</name>
      <files>validation/compliance_parser.py</files>
      <action>
        - Add check_compliance() method
        - Type hints: Dict[str, Any] (per instructions)
        - Validate against schema
      </action>
      <verify>
        python3 validation/compliance_parser.py --test
        # Quality gate: >95% pass rate
      </verify>
      <done>
        Function validates use case against compliance rules
      </done>
    </task>
  </tasks>

  <success_criteria>
    - All tasks executable (per instructions)
    - Type hints present (per instructions)
    - Tests pass before commits (per instructions)
    - Files in validation/ directory (per instructions)
    - Quality score maintained >95% (per instructions)
  </success_criteria>
</plan>
```

### Step 4: Execute Plan

```
/gsd:execute-phase

GSD spawns subagent with system instructions:

[Creates checkpoint: gsd-checkpoint-01-01-pre]

Subagent (sees system instructions):
  ✓ Loads: validation/data_dictionary.yaml
  ✓ Creates: validation/compliance_parser.py
  ✓ Uses: Type hints (Dict[str, Any])
  ✓ Tests: python3 validation/compliance_parser.py --help
  ✓ Commits: feat(validation): parse EO 13960 requirements

  ✓ Creates: validation/compliance_schema.yaml
  ✓ Validates: YAML syntax
  ✓ References: data_dictionary.yaml
  ✓ Commits: feat(validation): create compliance schema

  ✓ Adds: check_compliance() method
  ✓ Type hints: Dict[str, Any] → bool
  ✓ Tests: python3 validation/compliance_parser.py --test
  ✓ Quality: 97.2% compliance rate (>95% ✓)
  ✓ Commits: feat(validation): add compliance check function

  ✓ Creates: .planning/phases/01-requirements/01-01-SUMMARY.md
  ✓ Commits: docs(01-01): complete requirements parser plan

[Creates checkpoint: gsd-checkpoint-01-01-post]

Result:
  4 atomic commits
  All files in validation/ (per instructions)
  All scripts runnable (per instructions)
  Quality gate met (>95%)
  Git checkpoints created
  Can rollback if needed
```

### Git History

```bash
$ git log --oneline

abc1234 docs(01-01): complete requirements parser plan
def5678 feat(validation): add compliance check function
ghi9012 feat(validation): create compliance schema
jkl3456 feat(validation): parse EO 13960 requirements
```

**Every commit follows system instructions:**
- ✓ format: `type(validation): description`
- ✓ Atomic (one task per commit)
- ✓ Tested before committing
- ✓ Files in validation/

---

## Customization

### Adding Project-Specific Rules

Edit `.claude/settings.json`:

```json
{
  "systemInstructions": "# OMB-1 ...

  ## New Rule: Compliance Checks
  - All new validators must include compliance checking
  - Reference validation/compliance_schema.yaml
  - Report compliance percentage in output

  ## New Auto-Fix Rule
  Auto-fix:
  - Compliance validation bugs (add to existing list)

  ..."
}
```

**Effect:** GSD commands now automatically:
- Include compliance checks in plans
- Reference compliance_schema.yaml
- Add compliance percentage to reports

### Adding GSD Templates

Create project-specific templates:

```bash
.claude/get-shit-done/templates/omb-validation-plan.md
```

GSD will use these templates when creating plans for validation work.

---

## Troubleshooting

### "GSD doesn't follow my instructions"

**Problem:** GSD plans don't respect project structure

**Solution:** Be explicit in /gsd:new-project responses:
```
GSD: "What tech stack?"
You: "See .claude/settings.json - Python 3.x stdlib only,
     validation/ directory, no external dependencies"
```

GSD will read and apply instructions.

### "Too many commits"

**Problem:** GSD creates commit per task + metadata commit

**Solution:** This is correct! System instructions require atomic commits.
```
Task commits: feat/fix (working code)
Metadata commit: docs (SUMMARY + STATE)
```

This is GSD + System Instructions working together correctly.

### "Instructions and GSD conflict"

**Problem:** System instructions say one thing, GSD does another

**Solution:** Instructions take precedence. Update GSD plan:
```
/gsd:plan-phase 1

[Review plan]

If plan violates instructions, regenerate:
"This plan violates system instructions (no external deps).
Please revise to use Python stdlib only."
```

### "Context too full"

**Problem:** GSD loading too much context

**Solution:** System instructions specify what to load:
```
When working on validation:
- Load: validation/data_dictionary.yaml
- Reference: First 10 rows of CSV
- Skip: Full CSV (1757 rows)
```

GSD should respect this. If not, remind it in planning phase.

---

## Best Practices

### 1. **Let Instructions Guide GSD**

Don't repeat yourself:
```
❌ Bad:
/gsd:new-project
GSD: "What tech stack?"
You: "Python 3.x, no dependencies, use validation/ directory,
     type hints required, test before commit..."

✅ Good:
/gsd:new-project
GSD: "What tech stack?"
You: "See system instructions in .claude/settings.json"
```

### 2. **Use GSD for Multi-Phase Work**

Simple tasks → Just ask (instructions handle it)
Complex features → GSD commands (orchestration needed)

### 3. **Trust the Atomic Workflow**

Both systems create lots of commits. This is correct!
- Easy debugging (git bisect)
- Clear history
- Independent reversion
- Better for AI-assisted development

### 4. **Review Plans Before Execution**

```
/gsd:plan-phase 1
[Review plan in .planning/phases/01-*/01-01-PLAN.md]
[Verify it follows system instructions]
/gsd:execute-phase  # Only after review
```

### 5. **Use Checkpoints for Experiments**

```
/gsd:execute-phase  # Creates checkpoint
[Experiment with new approach]
Works? Keep it
Breaks? /gsd:rollback last
```

---

## Summary

**What You Have:**
```
System Instructions:
├─ Always active
├─ Project rules
├─ Quality gates
└─ Auto-fix decisions

GSD Commands:
├─ On-demand workflow
├─ Multi-phase orchestration
├─ Git checkpoints
└─ Progress tracking

Together:
├─ GSD reads instructions
├─ Instructions guide GSD
├─ Same principles
└─ Consistent quality
```

**When to Use What:**
```
1-3 tasks, 1 file     → System instructions only
4-6 tasks, 2-3 files  → Instructions + manual structure
7+ tasks, multi-phase → Full GSD workflow
```

**Key Insight:**
> System instructions = Rules of the road
> GSD commands = GPS navigation
> Both get you there faster and safer

---

## Next Steps

1. **Try GSD Commands:**
   ```
   /gsd:help
   /gsd:new-project  # For next major feature
   ```

2. **Read Documentation:**
   - `.claude/PROJECT_GUIDE.md` - Patterns
   - `.claude/USAGE_EXAMPLES.md` - Scenarios
   - `.claude/QUICK_START.md` - Quick ref

3. **Customize as Needed:**
   - Edit system instructions
   - Add project patterns
   - Refine quality gates

---

**You're all set! System instructions + GSD = Powerful, consistent development workflow.**
