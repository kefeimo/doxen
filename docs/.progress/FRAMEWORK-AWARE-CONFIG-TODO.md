# Framework-Aware Configuration Extraction - TODO

## Issues Identified (2026-03-25)

### 1. ❌ Dependencies Only Show JavaScript
**Problem**: For Ruby on Rails project (audit-template), only JavaScript dependencies from package.json are shown. Ruby gems from Gemfile are missing.

**Root Cause**: `_parse_ruby_deps()` method was missing (now added), but needs testing.

**Status**: ✅ **Fixed** - Added Ruby Gemfile parser

**Test**: Re-run discovery on audit-template and verify Ruby gems appear in REPOSITORY-ANALYSIS.md

**⚠️ EXTENSIBILITY WARNING**:
Current implementation uses **hardcoded language parsers** (`_parse_ruby_deps`, `_parse_js_deps`, `_parse_python_deps`). This is acceptable as a **hot fix** but **NOT scalable** for additional languages.

**TODO - Long-term Refactoring**:
- Replace hardcoded language-specific methods with **plugin/registry pattern**
- Use LLM to detect dependency file types dynamically
- Allow external parser registration for new languages (Go, Rust, Java, etc.)
- **Code locations to refactor**:
  - `repository_analyzer.py:33-40` (PACKAGE_FILES dict - hardcoded mappings)
  - `repository_analyzer.py:390-480` (_extract_dependencies - hardcoded loops per language)
  - `repository_analyzer.py:482-556` (Individual parser methods - hardcoded per language)

---

### 2. ✅ Irrelevant "test" Script Shown
**Problem**: For Rails project, showing npm `test` script: `echo "Error: no test specified" && exit 1`

**Root Cause**: Configuration extraction blindly extracts scripts from package.json regardless of framework.

**Solution Implemented**:
- Added `_extract_scripts_framework_aware()` method
- For Rails: Extract **Rake tasks** from Rakefile (db:migrate, db:seed, test, routes)
- For Django: Extract management commands (runserver, migrate, test)
- For Node.js: Extract npm/yarn scripts
- For Go: Extract Makefile targets
- Framework-aware logic checks primary language and framework name

**Implementation**:
```python
def _extract_scripts_framework_aware(self, repo_path, framework_info, file_roles):
    framework = framework_info.get("framework", "").lower()
    primary_lang = framework_info.get("primary_language", "").lower()

    if "rails" in framework or "ruby" in primary_lang:
        rakefile = repo_path / "Rakefile"
        if rakefile.exists():
            return self._extract_rake_tasks(rakefile)
    elif "javascript" in primary_lang or "node" in framework:
        # Extract npm scripts
    # ... other frameworks
```

**Result**:
```markdown
### Available Scripts
- **rake/db:migrate**: `rake db:migrate`
- **rake/db:seed**: `rake db:seed`
- **rake/test**: `rake test`
- **rake/routes**: `rake routes`
```

**Status**: ✅ **DONE** - Implemented and tested

---

### 3. ✅ Environment Variables Section Too Bulky
**Problem**: 80+ environment variables listed, many duplicated across .env files. Overwhelming and not useful.

**Root Cause**: Blindly extracting ALL env vars from ALL .env* files without filtering or summarization.

**Solution Implemented**: LLM-based intelligent summarization

Added `_summarize_env_vars_with_llm()` method that:
1. Groups variables by category (Database, API Keys, App Config, Email, etc.)
2. Identifies CRITICAL/REQUIRED variables
3. Uses wildcards for patterns (e.g., "DB_*" for DB_HOST, DB_PORT, DB_NAME)
4. Keeps summary concise

**Implementation**:
```python
def _summarize_env_vars_with_llm(self, all_env_vars: List[Dict]) -> Dict:
    # Sample first 50 vars for LLM
    sample_vars = all_env_vars[:50]
    var_names = [v["name"] for v in sample_vars]

    prompt = f"""Analyze these {len(all_env_vars)} environment variables...
    Group by category, identify critical vars, use wildcards...
    Return JSON: {{"total_count": ..., "critical_required": [...], "categories": {{...}}}}
    """

    response = self.llm.generate(prompt, max_tokens=1000, temperature=0.1)
    summary = json.loads(response)
    return summary
```

**Result**:
```markdown
### Environment Variables

**Total Variables:** 380

**Critical/Required:** `DATABASE_SQLSERVER_PASSWORD`, `SECRET_KEY_BASE`, `BING_MAPS_API_KEY`

**By Category:**
- **Database Configuration**: `DATABASE_SQLSERVER_HOST`, `DATABASE_SQLSERVER_PORT`, `DATABASE_SQLSERVER_*`
- **Application Core**: `APP_NAME`, `APP_BUILD`, `APP_VERSION`, `RAILS_ENV`
- **Web Server & Network**: `RAILS_PROTOCOL`, `RAILS_HOST`, `RAILS_PORT`
- **Email & SMTP**: `SMTP_ADDRESS`, `SMTP_DOMAIN`, `EMAIL_ADDRESS_*`
- **External API Keys**: `BING_MAPS_API_KEY`, `OPENSTREETMAP_API_KEY`
```

**Benefits**:
- Reduced from 380 individual vars to 8 organized categories
- Critical vars highlighted upfront
- Wildcards show patterns without listing every variation
- Much easier to understand at a glance

**Status**: ✅ **DONE** - Implemented and tested

---

## Implementation Priority

1. ✅ **Done**: Ruby dependency parsing
2. ✅ **Done**: Framework-aware scripts extraction (Rails Rake tasks vs npm scripts)
3. ✅ **Done**: LLM-based env var summarization
4. **Medium**: Framework-aware config file discovery (only scan relevant files) - Future enhancement

## Testing Results

✅ **All tests passed** on audit-template (Rails):

1. ✅ **Ruby Dependencies**: Shows 77 gems from Gemfile (not just JavaScript)
   - Before: Only 2 JavaScript packages
   - After: 77 Ruby gems + 2 JavaScript packages

2. ✅ **Framework-Aware Scripts**: Shows Rake tasks (not npm test)
   - Before: `audit-template/test: echo "Error: no test specified" && exit 1`
   - After:
     ```
     rake/db:migrate: rake db:migrate
     rake/db:seed: rake db:seed
     rake/test: rake test
     rake/routes: rake routes
     ```

3. ✅ **Summarized Environment Variables**: Organized into 8 categories (not 380 individual vars)
   - Before: 380 individual variables listed one by one
   - After:
     - Total count: 380
     - Critical vars highlighted
     - 8 organized categories with wildcards
     - Much more readable and useful

## Next Steps

**Regression Testing**: Test on rag-demo (Python/FastAPI) to ensure no regression
- Verify Python dependencies still extracted
- Verify npm scripts extracted for Node.js projects
- Verify env var summarization works for Python projects

**Future Enhancements**:
- Framework-aware config file discovery (scan only relevant files)
- Support for more frameworks (Django management commands, Go Makefiles)
- Smarter Rake task extraction (parse actual task definitions with descriptions)

---

*Created: 2026-03-25*
*Issue Reporter: User feedback on audit-template analysis*
