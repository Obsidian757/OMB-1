# OMB-1 Project Guide

## Quick Reference for Claude Sessions

### What This Repository Is
Federal AI use case inventory tracker. Data collection from 41 agencies, publicly accessible transparency tool per Executive Order requirements.

### Current State (Jan 2026)
- ✓ Data collection infrastructure (CSV/XLS in data/)
- ✓ Data dictionary validation schema
- ✓ Quality checker tool (validation/quality_checker.py)
- ✓ Automated markdown reports
- ⚠ No web interface (data repository only)
- ⚠ No API (direct file access)

### Common Tasks

#### 1. Adding Validation Features
```bash
# Load context
- validation/data_dictionary.yaml (schema)
- validation/quality_checker.py (existing code)
- data/*.csv (first 10 rows only)

# Pattern
1. Extend DataQualityChecker class
2. Update validate_csv() or add new method
3. Test with: python3 validation/quality_checker.py
4. Commit: feat(validation): add {feature}
```

#### 2. Adding New Statistics
```bash
# Reference
- README.md (match table format)
- Current stats: agencies, use_cases, rights_impacting

# Pattern
1. Track in validate_csv() loop
2. Add to 'statistics' dict
3. Update generate_markdown_report()
4. Verify numbers make sense
5. Commit: feat(validation): add {statistic}
```

#### 3. Generating Reports
```bash
# Current report: validation/QUALITY_REPORT.md
# Generated automatically by quality_checker.py

# To add new report type
1. Create new method in DataQualityChecker
2. Follow markdown format (tables, headers)
3. Include: timestamp, summary, details, recommendations
4. Output to validation/REPORT_NAME.md
```

### File Ownership

**NEVER MODIFY:**
- data/*.csv (raw agency submissions)
- data/*.xls (source data)
- validation/data_dictionary.yaml (without approval)

**SAFE TO MODIFY:**
- validation/*.py (quality tools)
- validation/*.md (generated reports)
- .claude/* (project config)
- README.md (documentation)

**ASK FIRST:**
- Schema changes
- New data sources
- Breaking API changes

### Quality Standards

**Code Quality:**
- Python 3.x compatible
- Type hints on public methods
- Docstrings required
- Minimal dependencies (stdlib preferred)

**Data Quality:**
- Completeness score >95%
- All required fields validated
- Accurate statistics
- Clear error messages

**Git Quality:**
- Atomic commits (one task = one commit)
- Clear messages: `type(scope): description`
- Tested before commit
- Linear history preferred

### GSD Integration

When using GSD commands with this project:

**Greenfield (new features):**
```
/gsd:new-project
↓ Define: "Add CSV comparison tool"
↓ GSD asks questions
↓ Creates .planning/PROJECT.md
↓
/gsd:create-roadmap
↓ Phases: 1) Parser 2) Comparison 3) Report
↓
/gsd:plan-phase 1
/gsd:execute-plan
```

**Brownfield (enhancing existing):**
```
/gsd:map-codebase
↓ Analyzes validation/
↓ Creates .planning/codebase/
↓
/gsd:new-project
↓ Define: "Add trend analysis"
↓ GSD sees existing structure
↓
/gsd:create-roadmap (knows context)
```

**System Instructions + GSD:**
```
System Instructions:    GSD Commands:
├─ Project rules        ├─ Workflow orchestration
├─ Tech constraints     ├─ Phase planning
├─ Quality gates        ├─ Automated execution
├─ Auto-fix rules       ├─ Git checkpoints
└─ Domain knowledge     └─ Progress tracking

Both work together:
- GSD uses system instructions for context
- System instructions guide GSD execution
- Quality gates apply to both workflows
```

### Example Session Flow

**Using System Instructions Only:**
```
You: "Add field type validation to quality checker"

Claude (sees system instructions):
1. Loads: data_dictionary.yaml, quality_checker.py
2. Plans: 3 tasks (parser, validator, tests)
3. Executes each task
4. Commits after each: feat(validation): ...
5. Runs quality_checker.py to verify
```

**Using GSD Commands + Instructions:**
```
You: "/gsd:new-project"

GSD: "What do you want to build?"
You: "Add field type validation"

GSD (uses system instructions):
- Knows about data_dictionary.yaml
- Understands validation/ structure
- Respects "no dependencies" rule
- Applies quality gates
- Creates plan matching project standards

/gsd:execute-plan
- Respects atomic commit rules
- Uses type hints (per instructions)
- Tests with quality_checker.py
- Generates report
```

### Context Loading Strategy

**Minimal (progress checks):**
- .claude/settings.json only

**Standard (validation work):**
- data_dictionary.yaml (schema)
- quality_checker.py
- CSV headers only (not full file)

**Full (major changes):**
- Above + README.md
- Above + existing reports
- Above + full codebase scan

**Never Load:**
- Full CSV files (1757 rows)
- XLS files
- Git history
- Unrelated federal docs

### Decision Matrix

| Scenario | Auto-Fix | Ask First | Log for Later |
|----------|----------|-----------|---------------|
| Missing validation | ✓ | | |
| Data quality bug | ✓ | | |
| Report formatting | ✓ | | |
| Security issue | ✓ | | |
| Schema change | | ✓ | |
| New data source | | ✓ | |
| Architecture change | | ✓ | |
| Performance tweak | | | ✓ |
| Report enhancement | | | ✓ |
| Additional statistic | | | ✓ |

### Common Patterns

**Pattern 1: Extend Validation**
```python
# In DataQualityChecker.validate_csv()
# Track new metric in the loop
new_metric_count = 0
for row in reader:
    if condition:
        new_metric_count += 1

# Return in statistics
'statistics': {
    'new_metric': new_metric_count
}
```

**Pattern 2: Add Report Section**
```python
# In generate_markdown_report()
report += "## New Section\n\n"
report += "| Column | Value |\n"
report += "|--------|-------|\n"
report += f"| Metric | {value} |\n"
```

**Pattern 3: Atomic Commit**
```bash
git add validation/quality_checker.py
git commit -m "feat(validation): add field type validation

- Parse type from data_dictionary.yaml
- Validate string/number/date types
- Report type mismatches in quality report
- 15 type violations found in current data"
```

### Tips for Success

1. **Start Small**: 2-3 tasks maximum per session
2. **Load Smart**: Only files you'll actually modify
3. **Test Early**: Run quality_checker.py after each change
4. **Commit Often**: After each completed task
5. **Use GSD**: For multi-phase features (dashboard, API)
6. **Trust Instructions**: They prevent common mistakes

### Emergency Procedures

**If quality_checker.py breaks:**
```bash
git log validation/quality_checker.py  # Find last good commit
git diff HEAD~1 validation/quality_checker.py  # See what changed
git checkout HEAD~1 validation/quality_checker.py  # Revert if needed
```

**If GSD plan goes wrong:**
```bash
/gsd:rollback last  # Undo last plan execution
# or
/gsd:recover  # Diagnose and fix interrupted state
```

**If context gets too full:**
```
Stop, commit current work, start fresh session
Load only specific files needed for next task
```

---

*This guide works with both manual Claude sessions and GSD automated workflows*
