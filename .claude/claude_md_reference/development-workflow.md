# Development Workflow - Detailed Reference

## Before Starting Work

### Context Gathering
1. **Check current status:** `docs/PROGRESS.md`
   - Review active tasks and priorities
   - Check for blockers or dependencies
   - Understand current sprint goals

2. **Review technical context:** `docs/DEVELOPMENT.md`
   - Read relevant architectural decisions
   - Understand why previous choices were made
   - Check for related patterns or constraints

3. **Check session history:** `docs/.progress/`
   - Review recent investigation results
   - Check for relevant findings or gotchas
   - Avoid repeating previous work

### Environment Verification
```bash
# Python environment
./venv/bin/python -c "import doxen; print('Python OK')"

# Ruby environment (if needed)
ruby --version  # Should show 3.4.1
bundle check || bundle install

# Git status
git status  # Clean working directory preferred
git pull    # Sync with remote
```

## During Development

### Progress Tracking
1. **Update PROGRESS.md frequently:**
   - Mark tasks in progress
   - Note blockers immediately
   - Update estimated completion

2. **Session notes in .progress/:**
   - Create `session-YYYY-MM-DD.md` for detailed work
   - Document investigation findings
   - Record decision rationale
   - Note useful commands or discoveries

### Code Development Patterns
```bash
# Feature branch workflow
git checkout -b feature/component-analysis
# ... make changes ...
git add . && git commit -m "feat: add component grouping logic"

# Test as you go
./venv/bin/python -m pytest tests/
./venv/bin/python src/main.py --test-project discourse

# Incremental commits
git add specific_file.py
git commit -m "refactor: extract component analyzer class"
```

### Documentation Updates
- Update relevant docs as you code (don't batch at end)
- Add examples to reference files when you create new features
- Update STRATEGY.md if you change generation approach

## After Major Milestones

### Distill Learnings
1. **Update DEVELOPMENT.md:**
   - Add entry with date header: `## 2026-04-01 - Component Analysis Enhancement`
   - Document: Context → Decision → Rationale → Consequences
   - Include alternative approaches considered

2. **Clean up PROGRESS.md:**
   - Archive completed tasks
   - Add new tasks discovered during work
   - Update priorities based on learnings

3. **Organize session notes:**
   - Review `.progress/session-*.md` files
   - Extract important findings to DEVELOPMENT.md
   - Archive detailed notes (rarely delete, just organize)

### Knowledge Transfer
```markdown
## 2026-04-01 - Component Grouping Strategy

**Context:** Individual file analysis was too granular, needed to group related files into logical components for better documentation structure.

**Decision:** Implement semantic file grouping based on:
- Directory structure patterns
- Import dependency analysis  
- Functional cohesion scoring

**Alternatives Considered:**
- Manual configuration files (too maintenance-heavy)
- Pure directory-based grouping (missed cross-cutting concerns)
- LLM-only analysis (too expensive, inconsistent)

**Implementation:** 
- `ComponentAnalyzer` class with configurable grouping rules
- Fallback to directory-based grouping for edge cases
- Validation against hand-labeled test cases

**Results:**
- 85% accuracy on test projects
- 40% reduction in generated reference docs
- Better logical cohesion in REFERENCE-*.md files

**Next Steps:** 
- Test on larger codebases (1000+ files)
- Add user feedback mechanism for grouping corrections
```

## Before Committing

### Pre-commit Checklist
```bash
# 1. Tests pass
./venv/bin/python -m pytest tests/ -v

# 2. Code quality
./venv/bin/python -m flake8 src/
./venv/bin/python -m mypy src/

# 3. Integration test
./venv/bin/python src/main.py --project experimental/projects/discourse --output /tmp/test-output

# 4. Documentation current
git diff --name-only | grep -E "(docs/|README)" && echo "Review doc updates"

# 5. Commit message follows convention
git log --oneline -5  # Check recent message style
```

### Commit Message Quality
- **Good:** `feat: add component grouping with semantic analysis`
- **Bad:** `fix stuff`, `wip`, `update code`

**Structure:**
```
<type>: <brief description (50 chars max)>

[Optional detailed explanation]
- Why this change was needed
- How it solves the problem
- Any trade-offs or limitations

[Optional breaking changes]
BREAKING: Component.analyze() now returns GroupedComponents instead of FileList

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>
```

### Types Reference
- `feat`: New functionality
- `fix`: Bug fixes
- `refactor`: Code restructuring without functional changes
- `test`: Adding or updating tests
- `docs`: Documentation updates
- `chore`: Maintenance tasks (deps, build, etc.)

## Testing Strategy

### Test Pyramid
1. **Unit tests:** Individual functions, classes
2. **Integration tests:** Component interactions
3. **End-to-end tests:** Full generation pipeline
4. **Validation tests:** Output quality assessment

### Test Data Management
```bash
# Use real projects for integration tests
experimental/projects/
├── discourse/          # Ruby web framework
├── django-rest-framework/  # Python API framework  
├── electron/           # JavaScript desktop framework
└── pytest/             # Python testing framework

# Golden master testing
experimental/results/
├── discourse/
│   ├── README.md       # Expected output
│   ├── INDEX.md
│   └── REFERENCE-*.md
└── validation/
    └── discourse_validation.json  # Quality metrics
```

### Quality Gates
- **Tier 1 Generation:** README/ARCHITECTURE must be informative and accurate
- **Tier 2 Generation:** 80%+ API coverage, examples executable
- **Tier 3 Generation:** User workflows complete and testable
- **Performance:** <30 seconds for medium repos (1000 files)
- **Cost:** <$1 per complete project documentation

## Troubleshooting Common Issues

### Environment Problems
```bash
# "Command not found" errors
which python  # Should be ./venv/bin/python or activated venv
echo $PATH | grep venv  # Should include venv/bin

# Ruby version issues  
rbenv version  # Should show 3.4.1
rbenv which ruby  # Should point to rbenv-managed Ruby

# Permission issues
ls -la venv/bin/python  # Should be executable
chmod +x venv/bin/*     # Fix if needed
```

### Generation Problems
```bash
# Debug generation pipeline
./venv/bin/python src/main.py --debug --project discourse

# Check intermediate outputs
ls -la experimental/results/discourse/discovery_analysis/
cat experimental/results/discourse/discovery_analysis/repository_data.json | jq .

# Validate LLM connectivity
./venv/bin/python -c "from src.llm_analyzer import LLMAnalyzer; print(LLMAnalyzer(use_bedrock=True).test_connection())"
```

### Git Issues
```bash
# Merge conflicts in generated files
git checkout --theirs experimental/results/  # Usually take generated version
git add . && git commit -m "resolve: accept regenerated documentation"

# Large file issues
git lfs track "*.json"  # For large analysis results
git add .gitattributes
```