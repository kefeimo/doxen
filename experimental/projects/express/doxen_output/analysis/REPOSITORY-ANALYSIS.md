# Repository Analysis

---
metadata:
  generated: 2026-03-26T13:45:20.254891
  doxen_version: 0.1.0
  analyzer: RepositoryAnalyzer
  repository: repo
  path: /home/kefei/project/doxen/experimental/projects/express/repo
  git_branch: master
  git_commit: 6c4249fe
  git_commit_date: 2026-03-01T07:55:02
  git_author: Sam Tucker-Davis
  quality_score: 95%
---

**Repository:** repo
**Path:** `/home/kefei/project/doxen/experimental/projects/express/repo`
**Generated:** 2026-03-26T13:45:20.262968

---

## Detected Framework

**Framework:** Node.js Library/Package
**Primary Language:** Javascript
**Detection Method:** llm
**Route Definition:** `index.js or lib/`

**Framework Conventions:**
- Config Dir: `./`
- App Dir: `lib/`

---

## Languages Detected

- **Javascript**: 141 files

## Entry Points

*Entry points identified based on Node.js Library/Package conventions*

### index.js
- **Path:** `index.js`
- **Language:** javascript
- **Framework:** Node.js Library/Package
- **Detection:** framework_convention

## Components

### Tests
- **Path:** `test`
- **Type:** tests
- **Language:** javascript

## Dependencies

### Javascript

**Total packages:** 44

- `accepts`
- `body-parser`
- `content-disposition`
- `content-type`
- `cookie`
- `cookie-signature`
- `debug`
- `depd`
- `encodeurl`
- `escape-html`
- `etag`
- `finalhandler`
- `fresh`
- `http-errors`
- `merge-descriptors`
- `mime-types`
- `on-finished`
- `once`
- `parseurl`
- `proxy-addr`
- *... and 24 more*

## Configuration Files

- `.gitignore`

## Runtime Configuration

### Available Scripts

- **repo/lint**: `eslint .`
- **repo/lint:fix**: `eslint . --fix`
- **repo/test**: `mocha --require test/support/env --reporter spec --check-leaks test/ test/acceptance/`
- **repo/test-ci**: `nyc --exclude examples --exclude test --exclude benchmarks --reporter=lcovonly --reporter=text npm test`
- **repo/test-cov**: `nyc --exclude examples --exclude test --exclude benchmarks --reporter=html --reporter=text npm test`
- **repo/test-tap**: `mocha --require test/support/env --reporter tap --check-leaks test/ test/acceptance/`

## Directory Structure

```
repo/
  .editorconfig
  .eslintignore
  .eslintrc.yml
  .github/
    dependabot.yml
    workflows/
      ci.yml
      codeql.yml
      legacy.yml
      scorecard.yml
  .gitignore
  .npmrc
  History.md
  LICENSE
  Readme.md
  examples/
    README.md
    auth/
      index.js
      views/
    content-negotiation/
      db.js
      index.js
      users.js
    cookie-sessions/
      index.js
    cookies/
      index.js
    downloads/
      files/
      index.js
    ejs/
      index.js
      public/
      views/
    error/
      index.js
    error-pages/
      index.js
      views/
    hello-world/
      index.js
    markdown/
      index.js
      views/
    multi-router/
      controllers/
      index.js
    mvc/
      controllers/
      db.js
      index.js
      lib/
      public/
      views/
    online/
      index.js
    params/
      index.js
    resource/
      index.js
    route-map/
      index.js
    route-middleware/
      index.js
    route-separation/
      index.js
      post.js
      public/
      site.js
      user.js
      views/
    search/
      index.js
      public/
    ... (6 more items)
  index.js
  lib/
    application.js
    express.js
    request.js
    response.js
    utils.js
    view.js
  package.json
  test/
    Route.js
    Router.js
    acceptance/
      auth.js
      content-negotiation.js
      cookie-sessions.js
      cookies.js
      downloads.js
      ejs.js
      error-pages.js
      error.js
      hello-world.js
      markdown.js
      multi-router.js
      mvc.js
      params.js
      resource.js
      route-map.js
      route-separation.js
      vhost.js
      web-service.js
    app.all.js
    app.engine.js
    app.head.js
    app.js
    app.listen.js
    app.locals.js
    app.options.js
    app.param.js
    app.render.js
    app.request.js
    app.response.js
    app.route.js
    app.router.js
    app.routes.error.js
    app.use.js
    config.js
    exports.js
    ... (53 more items)
```
