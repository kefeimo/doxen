# Testing & Validation - Detailed Reference

## Testing Philosophy

### Core Principles
- **Executable tests:** All examples must run successfully
- **No mocks in documentation:** Use real data, real projects, real APIs
- **Integration over unit:** Test component interactions, not isolated functions
- **Extraction accuracy:** Validate knowledge extraction quality, not just code coverage

## Test Structure

### Test Pyramid for Doxen

#### Unit Tests (Foundation)
```bash
# AST parsing correctness
./venv/bin/python -m pytest tests/test_ast_parser.py -v

# LLM prompt formatting  
./venv/bin/python -m pytest tests/test_llm_prompts.py -v

# File system utilities
./venv/bin/python -m pytest tests/test_file_utils.py -v
```

#### Integration Tests (Core)
```bash
# Agent pipeline integration
./venv/bin/python -m pytest tests/test_agent_pipeline.py -v

# Multi-language extraction
./venv/bin/python -m pytest tests/test_multi_language.py -v

# Documentation generation end-to-end
./venv/bin/python -m pytest tests/test_doc_generation.py -v
```

#### Validation Tests (Quality)
```bash
# Golden master comparison
./venv/bin/python -m pytest tests/test_golden_master.py -v

# Quality metrics assessment
./venv/bin/python -m pytest tests/test_quality_metrics.py -v

# Output structure validation
./venv/bin/python -m pytest tests/test_output_structure.py -v
```

## Test Data Management

### Real Project Test Cases
```
experimental/projects/
├── discourse/              # Ruby on Rails forum (993 API endpoints)
├── django-rest-framework/  # Python API toolkit (0 endpoints - framework)
├── electron/               # JavaScript desktop (50+ API modules)
├── pytest/                 # Python testing (extensive plugin system)
└── fastapi-users/          # Python auth (configuration-heavy)
```

### Golden Master Files
```
experimental/results/
├── discourse/
│   ├── README.md           # Expected project description
│   ├── INDEX.md            # Expected navigation structure
│   ├── ARCHITECTURE.md     # Expected system overview
│   └── REFERENCE-*.md      # Expected API references
└── validation/
    ├── discourse_metrics.json      # Quality scores
    ├── discourse_coverage.json     # API coverage stats
    └── discourse_validation.log    # Detailed validation results
```

## Quality Metrics

### Tier 1 Validation (Architecture)
```python
# README.md quality checks
def validate_readme(readme_path):
    content = read_file(readme_path)
    
    # Must have sections
    assert "## Features" in content or "## Overview" in content
    assert "## Quick Start" in content or "## Installation" in content
    
    # Length constraints
    lines = content.split('\n')
    assert 20 <= len(lines) <= 200, f"README too short/long: {len(lines)} lines"
    
    # Must mention project name and tech stack
    project_name = extract_project_name(readme_path)
    assert project_name.lower() in content.lower()
    
    return True
```

### Tier 2 Validation (References)
```python
# API coverage validation
def validate_api_coverage(project_path, reference_docs):
    # Extract all public APIs from source
    actual_apis = extract_public_apis(project_path)
    
    # Extract documented APIs from references
    documented_apis = []
    for doc_path in reference_docs:
        documented_apis.extend(extract_documented_apis(doc_path))
    
    # Calculate coverage
    coverage = len(documented_apis) / len(actual_apis)
    assert coverage >= 0.8, f"API coverage too low: {coverage:.1%}"
    
    return coverage
```

### Tier 3 Validation (Workflows)
```python
# Example executability validation
def validate_code_examples(guide_path):
    content = read_file(guide_path)
    code_blocks = extract_code_blocks(content)
    
    for i, code in enumerate(code_blocks):
        if code.language in ['python', 'javascript', 'ruby']:
            try:
                execute_code_safely(code.content, code.language)
            except Exception as e:
                raise ValidationError(f"Example {i+1} in {guide_path} failed: {e}")
    
    return len(code_blocks)
```

## Validation Pipeline

### Automated Quality Gates
```bash
#!/bin/bash
# scripts/validate_generation.sh

PROJECT=$1
RESULTS_DIR="experimental/results/$PROJECT"

echo "=== Validating $PROJECT ==="

# 1. Structure validation
python scripts/validate_structure.py $RESULTS_DIR
if [ $? -ne 0 ]; then
    echo "❌ Structure validation failed"
    exit 1
fi

# 2. Content quality validation  
python scripts/validate_content.py $RESULTS_DIR
if [ $? -ne 0 ]; then
    echo "❌ Content validation failed"
    exit 1
fi

# 3. Example executability
python scripts/validate_examples.py $RESULTS_DIR
if [ $? -ne 0 ]; then
    echo "❌ Example validation failed"
    exit 1
fi

echo "✅ All validations passed for $PROJECT"
```

### Manual Review Checklist

#### README.md Review
- [ ] Project purpose clear in first paragraph
- [ ] Installation instructions complete and tested
- [ ] Key features highlighted (3-7 bullet points)
- [ ] Quick start example works on fresh environment
- [ ] Links to INDEX.md and key documentation
- [ ] Appropriate length (50-150 lines typical)

#### INDEX.md Review  
- [ ] All generated docs listed and linked
- [ ] Tier structure clearly explained
- [ ] Multiple entry paths provided (new users vs integrators)
- [ ] Statistics accurate (file counts, word counts)
- [ ] Navigation logical and complete

#### REFERENCE-*.md Review
- [ ] Component purpose and scope clear
- [ ] All public APIs documented
- [ ] Usage examples provided and tested
- [ ] Configuration options explained
- [ ] Cross-references to related components
- [ ] Code examples executable

#### ARCHITECTURE.md Review
- [ ] High-level system design clear
- [ ] Component relationships explained
- [ ] Data flow diagrams accurate
- [ ] Technology choices justified
- [ ] Design patterns identified
- [ ] External dependencies noted

## Performance Testing

### Generation Speed Benchmarks
```python
# Benchmark generation performance
import time

def benchmark_generation(project_path):
    start = time.time()
    
    # Run full generation pipeline
    result = generate_documentation(project_path)
    
    end = time.time()
    duration = end - start
    
    # Performance targets
    file_count = count_source_files(project_path)
    if file_count < 100:
        assert duration < 120, f"Small project too slow: {duration}s"
    elif file_count < 1000:
        assert duration < 600, f"Medium project too slow: {duration}s"
    else:
        assert duration < 1800, f"Large project too slow: {duration}s"
    
    return {
        'duration': duration,
        'files_processed': file_count,
        'files_per_second': file_count / duration
    }
```

### Cost Tracking
```python
# Track LLM API costs during generation
class CostTracker:
    def __init__(self):
        self.total_tokens = 0
        self.total_cost = 0.0
        
    def track_request(self, prompt_tokens, completion_tokens, model):
        # AWS Bedrock Claude pricing (approximate)
        input_cost = prompt_tokens * 0.003 / 1000  # $3 per 1K input tokens
        output_cost = completion_tokens * 0.015 / 1000  # $15 per 1K output tokens
        
        self.total_tokens += prompt_tokens + completion_tokens
        self.total_cost += input_cost + output_cost
        
    def report(self):
        return {
            'total_tokens': self.total_tokens,
            'total_cost_usd': round(self.total_cost, 2),
            'cost_per_thousand_tokens': round(self.total_cost / self.total_tokens * 1000, 4)
        }
```

## Test Execution

### Running Test Suite
```bash
# Full test suite
./venv/bin/python -m pytest tests/ -v --tb=short

# Specific test categories
./venv/bin/python -m pytest tests/unit/ -v          # Fast unit tests
./venv/bin/python -m pytest tests/integration/ -v   # Slower integration tests  
./venv/bin/python -m pytest tests/validation/ -v    # Quality validation tests

# With coverage
./venv/bin/python -m pytest tests/ --cov=src --cov-report=html

# Parallel execution (faster)
./venv/bin/python -m pytest tests/ -n auto
```

### Continuous Integration
```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
          
      - name: Install dependencies
        run: |
          python -m venv venv
          ./venv/bin/pip install -e .
          
      - name: Run tests
        run: ./venv/bin/python -m pytest tests/ -v
        
      - name: Validate generation
        run: |
          ./venv/bin/python src/main.py --project experimental/projects/discourse
          bash scripts/validate_generation.sh discourse
```

## Debugging Failed Tests

### Common Test Failures

#### "ModuleNotFoundError"
```bash
# Check Python environment
./venv/bin/python -c "import sys; print(sys.path)"

# Reinstall in development mode
./venv/bin/pip install -e .
```

#### "LLM Connection Failed"
```bash
# Check AWS credentials
aws sts get-caller-identity

# Test Bedrock connectivity
./venv/bin/python -c "
from src.llm_analyzer import LLMAnalyzer
llm = LLMAnalyzer(use_bedrock=True)
print(llm.test_connection())
"
```

#### "Golden Master Mismatch"
```bash
# Regenerate golden master (when intentional changes)
./venv/bin/python scripts/regenerate_golden_master.py discourse

# Compare differences
diff -u experimental/results/discourse/README.md tests/golden_masters/discourse/README.md
```

#### "Example Execution Failed"
```bash
# Run example in isolation
cd /tmp
python -c "
# Paste the failing example code here
"

# Check for missing dependencies or environment issues
```