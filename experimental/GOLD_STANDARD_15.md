# Gold Standard 15 Projects - Reference Baseline

**Date:** 2026-03-27
**Status:** Active reference baseline for Doxen strategy validation
**Location:** `experimental/projects/` (15 projects)
**Archived:** `experimental/projects-archive/` (22 projects with minimal/external docs)

---

## The Gold Standard 15

These 15 projects represent the **best-in-class in-repo documentation** across diverse tech stacks and domains. All validation, testing, and strategy refinement should focus on these projects.

### Tier S: Massive Documentation (1000+ files)

1. **gitlabhq** (Ruby/Rails) - 2,617 doc files
   - DevOps platform with comprehensive enterprise documentation
   - Location: `/doc/`
   - Best for: Full Tier 1-5 hierarchy validation

2. **grafana** (Go+React) - 715 doc files
   - Monitoring/observability platform
   - Location: `/docs/`
   - Best for: Mixed stack (Go backend, React frontend), operational docs

---

### Tier A: Rich Documentation (200-400 files)

3. **wagtail** (Python/Django) - 372 doc files
   - CMS platform with well-structured docs
   - Location: `/docs/`
   - Best for: Django application patterns

4. **metabase** (Clojure+React) - 322 doc files
   - Business intelligence and analytics tool
   - Location: `/docs/`
   - Best for: Clojure/functional patterns, data visualization

5. **mui** (JavaScript/React) ⭐ NEW - 320 doc files
   - Material-UI component library
   - Location: `/docs/`
   - Best for: Tier 2 (component references), frontend patterns

6. **electron** (JavaScript) - 275 doc files
   - Desktop application framework
   - Location: `/docs/`
   - Best for: Complete tier coverage, tutorial-heavy docs

7. **pytest** (Python) - 258 doc files
   - Testing framework with gold-standard docs
   - Location: `/doc/`
   - Best for: How-to guides, plugin development

8. **celery** (Python) ⭐ NEW - 240 doc files
   - Distributed task queue
   - Location: `/docs/`
   - Best for: Tier 4 (operational), async patterns

9. **pandas** (Python) - 220 doc files
   - Data analysis library
   - Location: `/doc/`
   - Best for: API reference heavy, data science patterns

10. **scikit-learn** (Python) - 195 doc files
    - Machine learning library with exemplary docs
    - Location: `/doc/`
    - Best for: ML patterns, algorithm documentation

---

### Tier B: Moderate Documentation (50-200 files)

11. **sphinx** (Python) ⭐ NEW - 154 doc files
    - Documentation generation tool
    - Location: `/doc/`
    - Best for: Meta-documentation patterns, extension development

12. **discourse** (Ruby/Rails) - 112 doc files
    - Forum/community platform
    - Location: `/docs/`
    - Best for: Rails application patterns, developer guides

13. **django-rest-framework** (Python/Django) ⭐ NEW - 70 doc files
    - REST API framework for Django
    - Location: `/docs/`
    - Best for: API patterns, REST best practices

14. **superset** (Python/Flask+React) - 49 doc files
    - Data visualization and BI platform
    - Location: `/docs/`
    - Best for: Mixed Python/React stack, data visualization

15. **fastapi-users** (Python/FastAPI) - 36 doc files
    - Authentication library for FastAPI
    - Location: `/docs/`
    - Best for: FastAPI patterns, configuration-heavy docs

---

## Coverage Summary

### By Language
- **Python:** 8 projects (celery, pytest, pandas, scikit-learn, sphinx, django-rest-framework, superset, fastapi-users)
- **JavaScript/TypeScript:** 2 projects (electron, mui)
- **Ruby/Rails:** 2 projects (gitlabhq, discourse)
- **Go:** 1 project (grafana - backend)
- **Clojure:** 1 project (metabase - backend)

### By Domain
- **DevOps/Infrastructure:** 2 (gitlabhq, grafana)
- **Content/CMS:** 2 (wagtail, discourse)
- **Data/Analytics:** 3 (metabase, superset, pandas)
- **ML/Science:** 2 (scikit-learn, pytest)
- **Web Frameworks:** 3 (django-rest-framework, fastapi-users, celery)
- **UI/Frontend:** 1 (mui)
- **Desktop:** 1 (electron)
- **Documentation Tools:** 1 (sphinx)

### By Application Type
- **Applications:** 6 (gitlabhq, grafana, wagtail, metabase, discourse, superset)
- **Frameworks/Libraries:** 9 (mui, electron, pytest, celery, pandas, scikit-learn, sphinx, django-rest-framework, fastapi-users)

---

## Documentation Patterns

### /doc/ vs /docs/ (both common)
- **5 projects use `/doc/`** (singular): pytest, pandas, scikit-learn, sphinx, gitlabhq
- **10 projects use `/docs/`** (plural): grafana, wagtail, metabase, mui, electron, celery, discourse, django-rest-framework, superset, fastapi-users

**Insight:** Both are standard, slightly more projects use `/docs/` (plural)

### Documentation File Counts
- **Average:** 367 files per project
- **Median:** 220 files
- **Range:** 36-2,617 files
- **90th percentile:** 715+ files (gitlabhq, grafana)

### Tier Distribution (from these 15 projects)
Based on manual analysis of top projects:
- **Tier 2 (References):** Most prevalent in all 15 projects
- **Tier 1 (Overview):** Present in 13/15 projects
- **Tier 3 (Features):** Present in 10/15 projects
- **Tier 5 (Development):** Present in 11/15 projects
- **Tier 4 (Operational):** Present in 8/15 projects (celery, gitlabhq, grafana lead)

---

## Testing Strategy for Doxen

### Phase 3: Tier 2 (Component References) Testing
**Primary test projects:**
1. **mui** - Per-component API docs (Button.md, TextField.md)
2. **electron** - /api/ folder structure with module docs
3. **django-rest-framework** - /api-guide/ with serializers, views

**Expected patterns to validate:**
- Component grouping logic
- REFERENCE-{component}.md generation
- API extraction accuracy

### Phase 4: Tier 3 + Tier 5 Testing
**Tier 3 (Features/Workflows):**
- **electron** - /tutorial/ folder
- **pytest** - How-to guides
- **discourse** - Developer guides

**Tier 5 (Development/Contributing):**
- **pytest** - Testing guides, plugin development
- **sphinx** - Extension development, contributing
- **electron** - /development/ folder with internal docs

### Phase 5: Tier 4 (Operational) Testing
**Primary test projects:**
- **celery** - Monitoring, troubleshooting, production deployment
- **gitlabhq** - Administration, backup/restore, scaling
- **grafana** - Deployment, configuration, alerting

---

## Why These 15?

### Inclusion Criteria
✅ **36+ documentation files** in-repo (substantial)
✅ **Diverse tech stacks** (Python, JS, Ruby, Go, Clojure)
✅ **Diverse domains** (DevOps, Data, ML, Web, UI, Desktop)
✅ **Mix of applications and frameworks/libraries**
✅ **Well-maintained** (active, popular projects)
✅ **Code-driven documentation** (not external wikis)

### Exclusion Criteria (22 archived projects)
❌ Minimal doc folders (1-2 files only) - airflow, mastodon, cal.com, plane, ghost, kubernetes
❌ External documentation (hosted elsewhere) - django, rails, vue, nextjs, sentry, saleor, home-assistant
❌ Small libraries (root docs only) - click, flask, requests, redis, docker, express, fastapi, webpack

---

## Archived Projects (22)

**Location:** `experimental/projects-archive/`

**Still useful for:**
- Edge case testing (minimal docs)
- Root-level docs only pattern validation
- External docs integration (future feature)

**Primary focus remains:** The 15 gold standard projects

---

## Next Steps

### Immediate
✅ Gold standard 15 established
✅ 22 projects archived for clarity
✅ STRATEGY.md updated with new baseline

### Sprint 2-3 (Phase 3)
- Implement Tier 2 generation
- Test on: mui, electron, django-rest-framework
- Validate component grouping and REFERENCE-*.md generation

### Long-term
- Maintain 15-project test suite
- Add new gold standard projects as Doxen expands
- Use archived projects for specific edge cases

---

**Gold Standard 15 Status: Active ✅**
**Confidence Level: High**
**Ready for Phase 3 Implementation**
