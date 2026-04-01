# Doxen Pipeline Documentation

**Complete guide to the Doxen documentation generation and validation pipeline.**

---

## Quick Start

```bash
# Generate documentation for a project
./scripts/doxen generate --project discourse --tiers 1,2,3

# Validate generated documentation  
./scripts/doxen validate --project discourse --full

# Analyze patterns across projects
./scripts/doxen analyze --patterns
```

---

## 🏗️ Pipeline Architecture

### Directory Structure

```
doxen/
├── scripts/                    # Unified CLI and organized scripts
│   ├── doxen                   # Main CLI entry point
│   ├── generation/             # Documentation generation (7 scripts)
│   ├── validation/             # Quality validation (3 scripts)
│   ├── analysis/               # Pattern analysis (9 scripts)
│   └── utilities/              # Setup and maintenance (6 scripts)
├── experimental/
│   ├── projects/               # Active projects with standardized structure
│   │   └── {project}/
│   │       ├── source/         # Original source code (git clone)
│   │       ├── ground_truth/   # Extracted original documentation  
│   │       └── doxen_output/   # Generated documentation ⭐
│   ├── gold_standard_15/       # High-quality projects for testing
│   ├── archive/                # Archived projects (gitignored)
│   └── analysis/               # Analysis results and reports
└── .doxen/
    ├── config.yaml             # Global configuration
    ├── cache/                  # Performance cache (gitignored)
    └── templates/              # Custom templates
```

### 3-Tier Documentation Structure

| Tier | Purpose | Files Generated | Priority |
|------|---------|----------------|----------|
| **Tier 1** | Architecture Overview | README.md, INDEX.md, ARCHITECTURE.md | ✅ Complete |
| **Tier 2** | Component References | REFERENCE-{component}.md | 🎯 Highest (27% of docs) |
| **Tier 3** | Integration Guides | GUIDE-*.md, TUTORIAL-*.md | ✅ Complete |

---

## 🚀 CLI Interface

### Main Commands

#### `generate` - Create Documentation

```bash
# Generate all tiers for a project
./scripts/doxen generate --project discourse --tiers 1,2,3

# Generate specific tier
./scripts/doxen generate --project pandas --tier 1

# Language-specific generation
./scripts/doxen generate --project discourse --tier 2 --language ruby

# Only regenerate README  
./scripts/doxen generate --project django-rest-framework --readme-only

# Batch generation
./scripts/doxen generate --all-projects --tier 1

# Budget control
./scripts/doxen generate --project pandas --tiers 1,2,3 --budget 5.00
```

**Options:**
- `--project PROJECT` - Target project name
- `--tier {1,2,3}` - Generate specific tier
- `--tiers TIERS` - Generate multiple tiers (e.g., "1,2,3")
- `--language {python,ruby,javascript}` - Language-specific processing
- `--all-projects` - Process all projects
- `--readme-only` - Only regenerate README.md
- `--budget BUDGET` - Maximum cost limit (USD)
- `--dry-run` - Show what would be generated

#### `validate` - Quality Assurance

```bash
# Full validation suite
./scripts/doxen validate --project discourse --full

# Tier-specific validation
./scripts/doxen validate --project django-rest-framework --tier 3

# Coverage analysis
./scripts/doxen validate --project pandas --coverage

# Custom threshold
./scripts/doxen validate --project pytest --full --threshold 0.8
```

**Options:**
- `--project PROJECT` - Target project name
- `--full` - Run comprehensive validation
- `--tier {3}` - Validate specific tier
- `--coverage` - Run API coverage analysis  
- `--threshold FLOAT` - Quality threshold (default: 0.7)

#### `analyze` - Pattern Discovery

```bash
# Documentation pattern analysis
./scripts/doxen analyze --patterns

# Component analysis for specific project
./scripts/doxen analyze --project pandas --components

# Performance benchmarking
./scripts/doxen analyze --benchmark

# Language-specific analysis  
./scripts/doxen analyze --project discourse --components --language ruby
```

**Options:**
- `--project PROJECT` - Target project name
- `--patterns` - Analyze documentation patterns across projects
- `--components` - Analyze project component structure
- `--benchmark` - Run performance benchmarks
- `--language {python,ruby,javascript}` - Language-specific processing

#### `setup` - Project Management

```bash
# Setup new project from git
./scripts/doxen setup --project pytest --git-url https://github.com/pytest-dev/pytest

# Setup from local directory
./scripts/doxen setup --project myproject --local-path /path/to/source
```

**Options:**
- `--project PROJECT` - Project name (required)
- `--git-url URL` - Git repository URL
- `--local-path PATH` - Local source directory

#### `cost` - Budget Management

```bash
# Estimate costs for generation
./scripts/doxen cost --project pandas --estimate

# View cost history
./scripts/doxen cost --project discourse --history
```

#### `clean` - Maintenance

```bash
# Clean all outputs for a project
./scripts/doxen clean --project discourse

# Clean cache only
./scripts/doxen clean --project pandas --cache-only

# Clean all projects  
./scripts/doxen clean --all-projects
```

---

## 📋 Standard Workflows

### 1. New Project Setup

```bash
# 1. Clone project
./scripts/doxen setup --project pandas --git-url https://github.com/pandas-dev/pandas

# 2. Generate Tier 1 (quick overview)
./scripts/doxen generate --project pandas --tier 1

# 3. Validate quality
./scripts/doxen validate --project pandas --coverage

# 4. Generate full documentation
./scripts/doxen generate --project pandas --tiers 1,2,3 --budget 10.00
```

### 2. Quality Validation Pipeline

```bash
# 1. Generate documentation
./scripts/doxen generate --project discourse --tiers 1,2,3

# 2. Run full validation
./scripts/doxen validate --project discourse --full --threshold 0.7

# 3. Check coverage
./scripts/doxen validate --project discourse --coverage

# 4. Analyze patterns (optional)
./scripts/doxen analyze --project discourse --components
```

### 3. Batch Processing

```bash
# Generate Tier 1 for all projects
./scripts/doxen generate --all-projects --tier 1

# Validate all generated docs
for project in discourse django-rest-framework pandas; do
    ./scripts/doxen validate --project $project --full
done
```

### 4. Development & Testing

```bash
# Quick README update during development
./scripts/doxen generate --project myproject --readme-only

# Performance benchmarking
./scripts/doxen analyze --benchmark

# Pattern analysis across codebase
./scripts/doxen analyze --patterns
```

---

## 🔧 Script Organization

### Generation Scripts (`scripts/generation/`)

| Script | Purpose | CLI Command |
|--------|---------|-------------|
| `generate_architecture.py` | Tier 1 generation | `generate --tier 1` |
| `regenerate_readme.py` | README-only updates | `generate --readme-only` |
| `generate_dual_guides.py` | Tier 3 single project | `generate --tier 3` |
| `generate_all_dual_guides.py` | Tier 3 batch | `generate --all-projects --tier 3` |
| `test_reference_generation.py` | Tier 2 Python | `generate --tier 2 --language python` |
| `test_ruby_reference_generation.py` | Tier 2 Ruby | `generate --tier 2 --language ruby` |
| `test_tier3_guide_generation.py` | Tier 3 testing | Internal testing |

### Validation Scripts (`scripts/validation/`)

| Script | Purpose | CLI Command |
|--------|---------|-------------|
| `evaluate_baseline.py` | Full quality validation | `validate --full` |
| `validate_tier3_guides.py` | Tier 3 validation | `validate --tier 3` |
| `test_coverage_analysis.py` | API coverage analysis | `validate --coverage` |

### Analysis Scripts (`scripts/analysis/`)

| Script | Purpose | CLI Command |
|--------|---------|-------------|
| `analyze_doc_patterns.py` | Pattern analysis | `analyze --patterns` |
| `test_component_grouping.py` | Component analysis | `analyze --components` |
| `run_baseline.py` | Performance benchmarks | `analyze --benchmark` |
| `compare_pattern_detection.py` | Pattern comparison | Internal analysis |
| `test_ruby_component_grouping.py` | Ruby components | `analyze --components --language ruby` |

### Utility Scripts (`scripts/utilities/`)

| Script | Purpose | CLI Command |
|--------|---------|-------------|
| `extract_ground_truth.py` | Documentation extraction | `setup` (internal) |
| `calculate_characteristics.py` | Project analysis | `setup` (internal) |
| `clone_projects.sh` | Git repository cloning | `setup --git-url` |
| `extract_doc_inventory.py` | Documentation inventory | `analyze --patterns` (internal) |

---

## ⚙️ Configuration

### Global Configuration (`.doxen/config.yaml`)

```yaml
# Default settings
defaults:
  llm_model: "claude-3-5-sonnet-20241022"
  bedrock_region: "us-west-2"
  validation_threshold: 0.7
  max_cost_per_project: 5.00

# Directory structure
directories:
  projects_dir: "experimental/projects"
  analysis_dir: "experimental/analysis"
  
# Quality thresholds
validation:
  minimum_completeness: 0.6
  api_coverage_target: 0.8
```

### Per-Project Configuration

Projects can override global settings by creating `.doxen.yaml` in their source directory:

```yaml
# Project-specific overrides
language_priority: ["python", "javascript"]  
tier_focus: [1, 2]  # Skip Tier 3 for this project
custom_components: 
  - "core"
  - "plugins"
  - "extensions"
```

---

## 📊 Quality Metrics

### Validation Criteria

| Metric | Target | Description |
|--------|--------|-------------|
| **Completeness** | ≥60% | Percentage of intended documentation generated |
| **API Coverage** | ≥80% | Percentage of public APIs documented |
| **Quality Score** | ≥70% | Combined correctness and completeness |
| **Pattern Detection** | ≥75% | Accuracy of architectural pattern identification |

### Cost Guidelines

| Project Size | Tier 1 Cost | Tier 2 Cost | Tier 3 Cost | Total |
|-------------|-------------|-------------|-------------|-------|
| Small (<100 files) | $0.10-0.30 | $0.50-1.00 | $0.30-0.60 | ~$1-2 |
| Medium (<1000 files) | $0.20-0.50 | $1.00-2.50 | $0.50-1.50 | ~$2-5 |
| Large (>1000 files) | $0.30-1.00 | $2.00-5.00 | $1.00-3.00 | ~$3-10 |

---

## 🚨 Troubleshooting

### Common Issues

#### "Project directory not found"
```bash
# Ensure project exists in correct location
ls experimental/projects/myproject/

# If missing, set up project first
./scripts/doxen setup --project myproject --git-url <url>
```

#### "Discovery data not found" 
```bash
# Generate discovery data first
./scripts/doxen analyze --project myproject --components

# Or regenerate Tier 1
./scripts/doxen generate --project myproject --tier 1
```

#### "LLM connection failed"
```bash
# Check AWS credentials
aws sts get-caller-identity

# Or set Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

#### "Validation threshold not met"
```bash
# Lower threshold temporarily
./scripts/doxen validate --project myproject --threshold 0.5

# Or regenerate with higher quality
./scripts/doxen generate --project myproject --tiers 1,2,3
```

### Performance Issues

#### Slow generation
- Use `--tier 1` for quick overview
- Enable caching in `.doxen/config.yaml`
- Use `--dry-run` to estimate before running

#### High costs
- Set `--budget` limits
- Focus on specific tiers: `--tier 1`
- Use smaller test projects first

### Path Issues

All scripts now use standardized paths:
- **Generated docs:** `experimental/projects/{project}/doxen_output/`
- **Analysis results:** `experimental/analysis/`
- **Source code:** `experimental/projects/{project}/source/`

If you encounter path errors, ensure you're running from project root:
```bash
cd /path/to/doxen
./scripts/doxen <command>
```

---

## 🔄 Development Workflow

### Contributing to Pipeline

1. **Script Organization:**
   - Generation scripts → `scripts/generation/`
   - Validation scripts → `scripts/validation/`
   - Analysis scripts → `scripts/analysis/`
   - Utilities → `scripts/utilities/`

2. **CLI Integration:**
   - Add command routing in `scripts/doxen`
   - Update help text and examples
   - Test via CLI before committing

3. **Path Standards:**
   - Use `experimental/projects/{name}/doxen_output/` for generated docs
   - Use `experimental/analysis/` for analysis results
   - Never hardcode paths - use config system

4. **Testing:**
   ```bash
   # Test new generation feature
   ./scripts/doxen generate --project discourse --tier 2 --dry-run
   
   # Test validation
   ./scripts/doxen validate --project discourse --coverage
   
   # Test CLI help
   ./scripts/doxen <command> --help
   ```

### Adding New Projects

```bash
# 1. Setup project structure
./scripts/doxen setup --project newproject --git-url <url>

# 2. Test Tier 1 generation
./scripts/doxen generate --project newproject --tier 1

# 3. Validate quality
./scripts/doxen validate --project newproject --coverage

# 4. Add to test suite (if high quality)
mv experimental/projects/newproject experimental/gold_standard_15/
```

---

## 📈 Roadmap

### Current Status (Phase 2 Complete)
- ✅ Unified CLI interface
- ✅ Script organization by function  
- ✅ Standardized directory structure
- ✅ Path migration complete
- ✅ Quality validation pipeline

### Phase 3: End-to-End Validation
- [ ] pandas documentation generation
- [ ] Full workflow testing
- [ ] Performance benchmarking
- [ ] Cost validation

### Future Enhancements
- [ ] Web interface for CLI
- [ ] Automated quality gates
- [ ] Multi-language expansion
- [ ] Integration with CI/CD
- [ ] Custom template system

---

## 🆘 Getting Help

### Documentation
- **Pipeline Overview:** This document
- **Project Strategy:** `docs/STRATEGY.md`
- **Development Guide:** `CLAUDE.md`
- **Project Status:** `docs/PROGRESS.md`

### CLI Help
```bash
# General help
./scripts/doxen --help

# Command-specific help
./scripts/doxen generate --help
./scripts/doxen validate --help
./scripts/doxen analyze --help
```

### Support
- **Issues:** Report problems via project issue tracker
- **Questions:** Check existing documentation first
- **Features:** Propose in project discussions

---

*This pipeline documentation is maintained alongside the codebase. Last updated: 2026-04-01*