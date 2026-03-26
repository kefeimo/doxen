# Repository Analysis

---
metadata:
  generated: 2026-03-26T13:45:54.206904
  doxen_version: 0.1.0
  analyzer: RepositoryAnalyzer
  repository: repo
  path: /home/kefei/project/doxen/experimental/projects/django/repo
  git_branch: main
  git_commit: f6167b8b
  git_commit_date: 2026-03-25T11:20:58
  git_author: JaeHyuckSa
  quality_score: 95%
---

**Repository:** repo
**Path:** `/home/kefei/project/doxen/experimental/projects/django/repo`
**Generated:** 2026-03-26T13:45:54.219540

---

## Detected Framework

**Framework:** Django
**Primary Language:** Python
**Detection Method:** llm
**Route Definition:** `urls.py`

**Framework Conventions:**
- Config Dir: `django/conf/`
- App Dir: `django/`

---

## Languages Detected

- **Python**: 2894 files
- **Javascript**: 113 files

## Entry Points

*Entry points identified based on Django conventions*

### django/
- **Path:** `django`
- **Language:** unknown
- **Framework:** Django
- **Detection:** framework_convention

## Components

### Tests
- **Path:** `tests`
- **Type:** tests
- **Language:** python

### Docs
- **Path:** `docs`
- **Type:** docs
- **Language:** python

### Scripts
- **Path:** `scripts`
- **Type:** scripts
- **Language:** python

## Dependencies

### Python

**Total packages:** 3

- `asgiref`
- `sqlparse`
- `tzdata; sys_platform `

### Javascript

**Total packages:** 6

- `eslint`
- `puppeteer`
- `grunt`
- `grunt-cli`
- `grunt-contrib-qunit`
- `qunit`

## Configuration Files

- `.gitignore`

## Runtime Configuration

No runtime configuration extracted

## Directory Structure

```
repo/
  .editorconfig
  .flake8
  .git-blame-ignore-revs
  .gitattributes
  .github/
    CODE_OF_CONDUCT.md
    FUNDING.yml
    SECURITY.md
    copilot-instructions.md
    pull_request_template.md
    workflows/
      benchmark.yml
      check-migrations.yml
      check_commit_messages.yml
      coverage_comment.yml
      coverage_tests.yml
      data/
      docs.yml
      labels.yml
      linters.yml
      new_contributor_pr.yml
      postgis.yml
      python_matrix.yml
      schedule_tests.yml
      schedules.yml
      screenshots.yml
      selenium.yml
      tests.yml
  .gitignore
  .pre-commit-config.yaml
  .readthedocs.yml
  .tx/
    config
  AUTHORS
  CONTRIBUTING.rst
  Gruntfile.js
  INSTALL
  LICENSE
  LICENSE.python
  MANIFEST.in
  README.rst
  django/
    __init__.py
    __main__.py
    apps/
      __init__.py
      config.py
      registry.py
    conf/
      __init__.py
      app_template/
      global_settings.py
      locale/
        ... (88 more items)
      project_template/
      urls/
    contrib/
      __init__.py
      admin/
        ... (1 more items)
      admindocs/
      auth/
        ... (6 more items)
      contenttypes/
      flatpages/
      gis/
        ... (1 more items)
      humanize/
      messages/
      postgres/
      redirects/
      sessions/
      sitemaps/
      sites/
      staticfiles/
      syndication/
    core/
      __init__.py
      asgi.py
      cache/
      checks/
      exceptions.py
      files/
      handlers/
      mail/
      management/
      paginator.py
      serializers/
      servers/
      signals.py
      signing.py
      validators.py
      wsgi.py
    db/
      __init__.py
      backends/
      migrations/
      models/
      transaction.py
      utils.py
    dispatch/
      __init__.py
      dispatcher.py
      license.txt
    forms/
      __init__.py
      boundfield.py
      fields.py
      forms.py
      formsets.py
      jinja2/
      models.py
      renderers.py
      templates/
      utils.py
      widgets.py
    http/
      __init__.py
      cookie.py
      multipartparser.py
      request.py
      response.py
    middleware/
      __init__.py
      cache.py
      clickjacking.py
      common.py
      csp.py
      csrf.py
      gzip.py
      http.py
      locale.py
      security.py
    shortcuts.py
    tasks/
      __init__.py
      backends/
      base.py
      checks.py
      exceptions.py
      signals.py
    template/
      __init__.py
      autoreload.py
      backends/
      base.py
      context.py
      context_processors.py
      defaultfilters.py
      defaulttags.py
      engine.py
      exceptions.py
      library.py
      loader.py
      loader_tags.py
      loaders/
      response.py
      smartif.py
      utils.py
    templatetags/
      __init__.py
      cache.py
      i18n.py
      l10n.py
      static.py
      tz.py
    test/
      __init__.py
      client.py
      html.py
      runner.py
      selenium.py
      signals.py
      testcases.py
      utils.py
    urls/
      __init__.py
      base.py
      conf.py
      converters.py
      exceptions.py
      resolvers.py
      utils.py
    utils/
      __init__.py
      _os.py
      archive.py
      asyncio.py
      autoreload.py
      cache.py
      choices.py
      connection.py
      copy.py
      crypto.py
      csp.py
      datastructures.py
      dateformat.py
      dateparse.py
      dates.py
      deconstruct.py
      decorators.py
      deprecation.py
      duration.py
      encoding.py
      ... (23 more items)
    views/
      __init__.py
      csrf.py
      debug.py
      decorators/
      defaults.py
      generic/
      i18n.py
      static.py
      templates/
  docs/
    Makefile
    README.rst
    _ext/
      djangodocs.py
      github_links.py
    _theme/
      djangodocs/
      djangodocs-epub/
    conf.py
    contents.txt
    faq/
      admin.txt
      contributing.txt
      general.txt
      help.txt
      index.txt
      install.txt
      models.txt
      troubleshooting.txt
      usage.txt
    glossary.txt
    howto/
      _images/
      auth-remote-user.txt
      csp.txt
      csrf.txt
      custom-file-storage.txt
      custom-lookups.txt
      custom-management-commands.txt
      custom-model-fields.txt
      custom-shell.txt
      custom-template-backend.txt
      custom-template-tags.txt
      delete-app.txt
      deployment/
      error-reporting.txt
      index.txt
      initial-data.txt
      legacy-databases.txt
      logging.txt
      outputting-csv.txt
      outputting-pdf.txt
      ... (5 more items)
    index.txt
    internals/
      _images/
      contributing/
      deprecation.txt
      git.txt
      howto-release-django.txt
      index.txt
      mailing-lists.txt
      organization.txt
      release-process.txt
      security.txt
    intro/
      _images/
      contributing.txt
      index.txt
      install.txt
      overview.txt
      reusable-apps.txt
      tutorial01.txt
      tutorial02.txt
      tutorial03.txt
      tutorial04.txt
      tutorial05.txt
      tutorial06.txt
      tutorial07.txt
      tutorial08.txt
      whatsnext.txt
    lint.py
    make.bat
    man/
      django-admin.1
    misc/
      api-stability.txt
      design-philosophies.txt
      distributions.txt
      index.txt
    ref/
      applications.txt
      checks.txt
      class-based-views/
      clickjacking.txt
      contrib/
      csp.txt
      csrf.txt
      databases.txt
      django-admin.txt
      exceptions.txt
      files/
      forms/
      index.txt
      logging.txt
      middleware.txt
      migration-operations.txt
      models/
      paginator.txt
      request-response.txt
      schema-editor.txt
      ... (11 more items)
    releases/
      0.95.txt
      0.96.txt
      1.0-porting-guide.txt
      1.0.1.txt
      1.0.2.txt
      1.0.txt
      1.1.2.txt
      1.1.3.txt
      1.1.4.txt
      1.1.txt
      1.10.1.txt
      1.10.2.txt
      1.10.3.txt
      1.10.4.txt
      1.10.5.txt
      1.10.6.txt
      1.10.7.txt
      1.10.8.txt
      1.10.txt
      1.11.1.txt
      ... (361 more items)
    requirements.txt
    spelling_wordlist
    ... (1 more items)
  eslint-recommended.js
  ... (10 more items)
```
