# Baseline Evaluation - Comparison Table

## Aggregate Scores

| Project | Correctness | Completeness | Combined | Status |
|---------|-------------|--------------|----------|--------|
| fastapi  |      57.2% |       60.7% |   59.0% | ⚠️ |
| express  |      73.5% |       84.4% |   79.0% | ✅ |
| django   |      46.1% |      100.0% |   73.1% | ✅ |
| nextjs   |      50.0% |      100.0% |   75.0% | ✅ |
|---------|-------------|--------------|----------|--------|
| **Average** | **   56.7%** | **    86.3%** | **71.5%** | |

## Detailed Metrics

### fastapi

**Ground Truth:**
- Documentation: 51 files
- Architecture type: full-stack
- Patterns mentioned: Middleware, Strategy, ORM, Pydantic, REST

**Correctness:**
- Architecture detected: True
- Pattern detection (corrected F1): 75.00%
  - Corrected Precision: 100.00%
  - Corrected Recall: 60.00%
  - Conservative F1: 66.67% (GT-only)
  - Detected: 5 patterns
  - Supported (in GT): 5
- Component recall: 46.67% (9 detected)
- Dependencies detected: 5

**Completeness:**
- README section coverage: 21.43%
- Sections generated: 6 (GT: 28)
- Documentation lines: 179 (GT: 549)
- Components documented: 3

### express

**Ground Truth:**
- Documentation: 1 files
- Architecture type: not detected
- Patterns mentioned: Middleware, Repository, ORM

**Correctness:**
- Architecture detected: True
- Pattern detection (corrected F1): 70.59%
  - Corrected Precision: 75.00%
  - Corrected Recall: 66.67%
  - Conservative F1: 57.14% (GT-only)
  - Detected: 4 patterns
  - Supported (in GT): 2
  - Unsupported (unchecked): 2
- Component recall: 100.00% (7 detected)
- Dependencies detected: 44

**Completeness:**
- README section coverage: 68.75%
- Sections generated: 11 (GT: 16)
- Documentation lines: 179 (GT: 278)
- Components documented: 1

### django

**Ground Truth:**
- Documentation: 51 files
- Architecture type: mvc
- Patterns mentioned: Middleware, Strategy, ORM, Async, Model-View-Controller

**Correctness:**
- Architecture detected: True
- Pattern detection (corrected F1): 57.14%
  - Corrected Precision: 100.00%
  - Corrected Recall: 40.00%
  - Detected: 4 patterns
  - Supported (in GT): 4
- Component recall: 31.25% (8 detected)
- Dependencies detected: 9

**Completeness:**
- Sections generated: 6 (GT: 0)
- Documentation lines: 151 (GT: 84)
- Components documented: 3

### nextjs

**Ground Truth:**
- Documentation: 1 files
- Architecture type: full-stack
- Patterns mentioned: none

**Correctness:**
- Architecture detected: True
- Pattern detection (corrected F1): 0.00%
  - Corrected Precision: 50.00%
  - Corrected Recall: 0.00%
  - Detected: 2 patterns
- Component recall: 100.00% (8 detected)
- Dependencies detected: 194

**Completeness:**
- README section coverage: 100.00%
- Sections generated: 16 (GT: 6)
- Documentation lines: 196 (GT: 80)
- Components documented: 3
