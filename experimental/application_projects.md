# Reference Projects for Data-Driven Strategy

**Purpose:** Real-world applications + frameworks/libraries for data-driven STRATEGY.md refinement

**Total:** 23 new projects + 10 existing = 33 projects

---

## New Projects to Clone

### Part A: Application-Oriented Projects (15)

### FastAPI Applications (Python)
1. **Full Stack FastAPI PostgreSQL**
   - URL: https://github.com/tiangolo/full-stack-fastapi-template
   - Description: Full-stack template with FastAPI, PostgreSQL, Docker
   - Size: Medium

2. **FastAPI-Users**
   - URL: https://github.com/fastapi-users/fastapi-users
   - Description: User authentication and management for FastAPI
   - Size: Small-Medium

### Django Applications (Python)
3. **Saleor**
   - URL: https://github.com/saleor/saleor
   - Description: Headless e-commerce platform
   - Size: Large

4. **Wagtail**
   - URL: https://github.com/wagtail/wagtail
   - Description: Django-based CMS
   - Size: Large

5. **Sentry**
   - URL: https://github.com/getsentry/sentry
   - Description: Error tracking and monitoring (Django + React)
   - Size: Very Large

### React/Next.js Applications (JavaScript)
6. **Cal.com**
   - URL: https://github.com/calcom/cal.com
   - Description: Scheduling and calendar application (Next.js)
   - Size: Large

7. **Plane**
   - URL: https://github.com/makeplane/plane
   - Description: Project management tool (Next.js + React)
   - Size: Large

### Rails Applications (Ruby)
8. **Discourse**
   - URL: https://github.com/discourse/discourse
   - Description: Forum and community platform
   - Size: Very Large

9. **GitLab**
   - URL: https://github.com/gitlabhq/gitlabhq
   - Description: DevOps platform
   - Size: Very Large (may need shallow clone)

10. **Mastodon**
    - URL: https://github.com/mastodon/mastodon
    - Description: Decentralized social network
    - Size: Large

### Flask Applications (Python)
11. **Airflow**
    - URL: https://github.com/apache/airflow
    - Description: Workflow orchestration platform
    - Size: Very Large

12. **Superset**
    - URL: https://github.com/apache/superset
    - Description: Data visualization and BI platform (Flask + React)
    - Size: Large

### Node.js Applications
13. **Ghost**
    - URL: https://github.com/TryGhost/Ghost
    - Description: Publishing/blogging platform
    - Size: Large

### Go + React Applications
14. **Grafana**
    - URL: https://github.com/grafana/grafana
    - Description: Monitoring and observability dashboards
    - Size: Very Large

### Clojure + React Applications
15. **Metabase**
    - URL: https://github.com/metabase/metabase
    - Description: Business intelligence and analytics tool
    - Size: Large

---

### Part B: Framework/Library Projects (8)

**Note:** These are frameworks/libraries themselves (not applications), included for documentation quality and domain diversity.

#### Data Science/ML (Python)
16. **scikit-learn**
    - URL: https://github.com/scikit-learn/scikit-learn
    - Description: ML library with gold-standard documentation
    - Size: Large

17. **pandas**
    - URL: https://github.com/pandas-dev/pandas
    - Description: Data analysis library, comprehensive reference docs
    - Size: Large

#### Testing/Quality (Python)
18. **pytest**
    - URL: https://github.com/pytest-dev/pytest
    - Description: Testing framework with excellent doc structure
    - Size: Medium

#### Infrastructure/Database
19. **Redis**
    - URL: https://github.com/redis/redis
    - Description: In-memory database (C), clear operational docs
    - Size: Medium

20. **Kubernetes**
    - URL: https://github.com/kubernetes/kubernetes
    - Description: Container orchestration (Go), extensive docs
    - Size: Very Large (use shallow clone)

#### Build/Desktop Tools (JavaScript)
21. **Webpack**
    - URL: https://github.com/webpack/webpack
    - Description: Module bundler, complex configuration docs
    - Size: Large

22. **Electron**
    - URL: https://github.com/electron/electron
    - Description: Desktop application framework, cross-platform docs
    - Size: Very Large

#### IoT/Home Automation (Python)
23. **Home Assistant**
    - URL: https://github.com/home-assistant/core
    - Description: Home automation platform, community-driven docs
    - Size: Very Large

---

## Coverage Summary (33 Total Projects)

### Existing Projects (10)
- FastAPI, Express, Django, Next.js (pilot projects)
- Flask, Rails, Vue, Click, Requests, Docker (expansion projects)

### New Projects (23)

#### By Category
**Applications (15):**
- FastAPI apps: 2 (Full Stack Template, FastAPI-Users)
- Django apps: 3 (Saleor, Wagtail, Sentry)
- React/Next.js apps: 2 (Cal.com, Plane)
- Rails apps: 3 (Discourse, GitLab, Mastodon)
- Flask apps: 2 (Airflow, Superset)
- Node.js apps: 1 (Ghost)
- Go + React: 1 (Grafana)
- Clojure + React: 1 (Metabase)

**Frameworks/Libraries (8):**
- Data Science/ML: 2 (scikit-learn, pandas)
- Testing: 1 (pytest)
- Infrastructure: 2 (Redis, Kubernetes)
- Build/Desktop: 2 (Webpack, Electron)
- IoT: 1 (Home Assistant)

#### By Application Type (Applications only)
- **SaaS/Business:** 5 (Saleor, Cal.com, Plane, Ghost, Wagtail)
- **Developer Tools:** 3 (Sentry, GitLab, Grafana)
- **Social/Community:** 2 (Discourse, Mastodon)
- **Data/Analytics:** 3 (Airflow, Superset, Metabase)
- **Auth/Infrastructure:** 1 (FastAPI-Users)
- **Templates:** 1 (Full Stack FastAPI)

#### By Language
- **Python:** 11 (Saleor, Wagtail, Sentry, Airflow, Superset, FastAPI-Users, Full Stack, scikit-learn, pandas, pytest, Home Assistant)
- **JavaScript/TypeScript:** 7 (Cal.com, Plane, Ghost, Webpack, Electron, + existing: Express, Vue, Next.js)
- **Ruby:** 3 (Discourse, GitLab, Mastodon)
- **Go:** 2 (Grafana, Kubernetes)
- **Clojure:** 1 (Metabase)
- **C:** 1 (Redis)

#### By Size
- **Small-Medium:** 2
- **Medium:** 2
- **Large:** 11
- **Very Large:** 8

---

## Cloning Strategy

### Full Clone (Small-Medium projects)
- fastapi-users
- full-stack-fastapi-template
- pytest
- redis

### Shallow Clone (All others - 19 projects)
```bash
git clone --depth 1 <url>
```
- All Large and Very Large projects

### Estimated Disk Space
- ~8-15 GB total (with shallow clones for large projects)

### Note on Potential Issues
Some very large repos (GitLab, Kubernetes, Electron, Home Assistant) may:
- Take longer to clone
- Require more disk space even with shallow clone
- Have complex submodule dependencies

**Strategy:** Start cloning, skip or note issues for projects that are problematic

---

## Documentation Extraction Plan

For each project, extract:
1. `/docs/` folder structure
2. Root-level docs (README.md, CONTRIBUTING.md, etc.)
3. Doc types and organization
4. Common patterns and sections

---

## Next Steps

1. Clone all 23 projects to `experimental/projects/`
   - Note: May skip/flag problematic very large projects
2. Run documentation inventory extraction on all 33 projects
3. Analyze documentation patterns across all projects
4. Calculate metrics (% of projects with each doc type)
5. Map patterns to Tier 1-5 hierarchy and validate/adjust
6. Update STRATEGY.md with data-driven insights and real examples
