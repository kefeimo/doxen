# Repository Analysis

---
metadata:
  generated: 2026-03-27T17:01:54.417772
  doxen_version: 0.1.0
  analyzer: RepositoryAnalyzer
  repository: discourse
  path: experimental/projects/discourse
  git_branch: main
  git_commit: e1a47e73
  git_commit_date: 2026-03-27T10:38:57
  git_author: Régis Hanol
  quality_score: 95%
---

**Repository:** discourse
**Path:** `experimental/projects/discourse`
**Generated:** 2026-03-27T17:01:54.492784

---

## Detected Framework

**Framework:** Ruby on Rails
**Primary Language:** Ruby
**Detection Method:** llm
**Route Definition:** `config/routes.rb`

**Framework Conventions:**
- Config Dir: `config/`
- App Dir: `app/`

---

## Languages Detected

- **Ruby**: 9262 files
- **Javascript**: 2765 files
- **Typescript**: 2 files

## Entry Points

*Entry points identified based on Ruby on Rails conventions*

### config.ru
- **Path:** `config.ru`
- **Language:** unknown
- **Framework:** Ruby on Rails
- **Detection:** framework_convention

### bin/rails
- **Path:** `bin/rails`
- **Language:** unknown
- **Framework:** Ruby on Rails
- **Detection:** framework_convention

## Components

### Frontend
- **Path:** `frontend`
- **Type:** frontend
- **Language:** javascript

### Database
- **Path:** `db`
- **Type:** database
- **Language:** ruby

### Tests
- **Path:** `test`
- **Type:** tests
- **Language:** unknown

### Docs
- **Path:** `docs`
- **Type:** docs
- **Language:** ruby

### Scripts
- **Path:** `bin`
- **Type:** scripts
- **Language:** unknown

### Config
- **Path:** `config`
- **Type:** config
- **Language:** ruby

## Dependencies

### Javascript

**Total packages:** 26

- `@babel/plugin-proposal-decorators`
- `@discourse/lint-configs`
- `@discourse/moment-timezone-names-translations`
- `@fortawesome/fontawesome-free`
- `@glint/ember-tsc`
- `@glint/tsserver-plugin`
- `@rdil/parallel-prettier`
- `@swc/core`
- `chrome-launcher`
- `chrome-remote-interface`
- `concurrently`
- `ember-template-lint`
- `esbuild`
- `eslint`
- `jsdoc`
- `lefthook`
- `licensee`
- `lint-to-the-future`
- `lint-to-the-future-ember-template`
- `lint-to-the-future-eslint`
- *... and 6 more*

### Ruby

**Total packages:** 172

- `bootsnap"`
- `actionmailer"`
- `actionpack"`
- `actionview"`
- `activemodel"`
- `activerecord"`
- `activesupport"`
- `railties"`
- `propshaft`
- `json`
- `actionview_precompiler"`
- `discourse-seed-fu`
- `mail`
- `mini_mime`
- `mini_suffix`
- `redis`
- `redis-namespace`
- `active_model_serializers"`
- `http_accept_language"`
- `discourse-fonts"`
- *... and 152 more*

## Configuration Files

- `.gitignore`
- `docs/developer-guides/.gitignore`
- `script/.gitignore`
- `script/benchmarks/markdown/.gitignore`
- `migrations/.gitignore`

## Runtime Configuration

### Available Scripts

- **rake/db:migrate**: `rake db:migrate`
- **rake/db:seed**: `rake db:seed`
- **rake/test**: `rake test`
- **rake/routes**: `rake routes`

## Directory Structure

```
discourse/
  .agents/
    skills/
      discourse-service-authoring/
      discourse-upcoming-changes/
      discourse-upcoming-changes-authoring/
  .annotaterb.yml
  .claude/
    skills/
      discourse-service-authoring/
      discourse-upcoming-changes/
      discourse-upcoming-changes-authoring/
  .cursor/
    rules/
      ai-agents-always.mdc
  .devcontainer/
    devcontainer.json
    scripts/
      chrome_wrapper
      start.rb
  .editorconfig
  .git-blame-ignore-revs
  .gitattributes
  .github/
    actions/
      setup-release-environment/
    dependabot.yml
    instructions/
      copilot.instructions.md
    labeler.yml
    workflows/
      backport.yml
      check-pr-body.yml
      dependabot-pnpm-dedupe.yml
      developer-docs-lint.yml
      developer-docs-publish.yml
      labeler.yml
      licenses.yml
      linting.yml
      migration-tests.yml
      publish-assets.yml
      publish-types.yml
      release-branch-handler.yml
      release-handler.yml
      release-notes.yml
      release-prepare-latest-bump.yml
      stale-pr-closer.yml
      tests.yml
  .gitignore
  .ignore
  .jsdoc
  .licensed.yml
  .licensee.json
  .npmrc
  .pnpmfile.cjs
  .prettierignore
  .prettierrc.cjs
  .rspec
  .rspec_parallel
  ... (51 more items)
```
