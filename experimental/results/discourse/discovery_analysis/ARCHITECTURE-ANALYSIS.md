# Architecture Analysis

**Generated:** 2026-03-27T17:01:54.555212

---

## Architectural Pattern

**Pattern:** Monolith

### Data Flow

**Primary Flow:** External APIs
**API Communication:** REST
**Data Persistence:** Database
**External Integrations:** 6 detected

## Components

### Frontend

- **Path:** `frontend`
- **Language:** javascript
- **Type:** frontend
- **Purpose:** Frontend UI providing user interface and interactions
- **Exports:** User interface, Client-side logic

### Database

- **Path:** `db`
- **Language:** ruby
- **Type:** database
- **Purpose:** Data persistence and storage layer
- **Exports:** Data storage, Database schema

### Tests

- **Path:** `test`
- **Language:** unknown
- **Type:** tests
- **Purpose:** Test suite for validation and quality assurance

### Docs

- **Path:** `docs`
- **Language:** ruby
- **Type:** docs
- **Purpose:** Project documentation

### Scripts

- **Path:** `bin`
- **Language:** unknown
- **Type:** scripts
- **Purpose:** Utility scripts for automation and maintenance
- **Entry Points:** `bin/rails`

### Config

- **Path:** `config`
- **Language:** ruby
- **Type:** config
- **Purpose:** Configuration and environment settings
- **Entry Points:** `config.ru`
- **API Endpoints:** 993

## Design Patterns

### RESTful API

**Description:** HTTP-based API following REST principles

**Evidence:** 993 endpoints using REST methods

## Technology Stack

**Framework:** Ruby on Rails
**Primary Language:** Ruby

### Languages

- **Ruby:** 9262 files
- **Javascript:** 2765 files
- **Typescript:** 2 files

### Key Dependencies

**Javascript:**
- @babel/plugin-proposal-decorators
- @discourse/lint-configs
- @discourse/moment-timezone-names-translations
- @fortawesome/fontawesome-free
- @glint/ember-tsc
- @glint/tsserver-plugin
- @rdil/parallel-prettier
- @swc/core
- chrome-launcher
- chrome-remote-interface

**Ruby:**
- bootsnap"
- actionmailer"
- actionpack"
- actionview"
- activemodel"
- activerecord"
- activesupport"
- railties"
- propshaft
- json

## Integration Points

- **Fetch:** 6 call(s)
  - Frontend makes 6 fetch call(s) to backend
