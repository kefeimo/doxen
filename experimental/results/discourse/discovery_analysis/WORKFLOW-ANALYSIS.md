# Workflow Analysis

---
metadata:
  generated: 2026-03-27T17:01:54.542259
  doxen_version: 0.1.0
  analyzer: WorkflowMapper
---

**Generated:** 2026-03-27T17:01:54.542269

---

> **Note:** This is a high-level summary. Full endpoint catalog with metadata available in `WORKFLOW-ANALYSIS.json`

---

## API Endpoints

**Total endpoints:** 993

*Note: Some endpoints extracted via LLM from route definition files (not validated against controllers)*

### Endpoint Summary by Method

- **GET**: 578 endpoints
- **POST**: 169 endpoints
- **PUT**: 163 endpoints
- **PATCH**: 5 endpoints
- **DELETE**: 78 endpoints

### Sample Endpoints

*Full endpoint catalog available in `DISCOVERY-SUMMARY.json`*

#### GET Endpoints (showing 5 of 578)

- `GET /404` → `exceptions#not_found`
- `GET /404-body` → `exceptions#not_found_body`
- `GET /bootstrap/core-css-for-tests.css` → `bootstrap#core_css_for_tests`
- `GET /bootstrap/site-settings-for-tests.js` → `bootstrap#site_settings_for_tests`
- `GET /bootstrap/plugin-test-info` → `bootstrap#plugin_test_info`
- *... and 573 more*

#### POST Endpoints (showing 5 of 169)

- `POST /404` → `exceptions#not_found`
- `POST /webhooks/aws` → `webhooks#aws`
- `POST /webhooks/mailgun` → `webhooks#mailgun`
- `POST /webhooks/mailjet` → `webhooks#mailjet`
- `POST /webhooks/mailpace` → `webhooks#mailpace`
- *... and 164 more*

#### PUT Endpoints (showing 5 of 163)

- `PUT /finish-installation/resend-email` → `finish_installation#resend_email`
- `PUT /pub/by-topic/:topic_id` → `published_pages#upsert`
- `PUT /wizard/steps/:id` → `steps#update`
- `PUT /admin/site_settings/:id` → `admin/site_settings#update`
- `PUT /admin/site_settings/user_count` → `admin/site_settings#user_count`
- *... and 158 more*

#### PATCH Endpoints (showing 5 of 5)

- `PATCH /groups/:id` → `groups#update`
- `PATCH /g/:id` → `groups#update`
- `PATCH /invites/:id` → `invites#update`
- `PATCH /tag_groups/:id` → `tag_groups#update`
- `PATCH /sidebar_sections/:id` → `sidebar_sections#update`

#### DELETE Endpoints (showing 5 of 78)

- `DELETE /pub/by-topic/:topic_id` → `published_pages#destroy`
- `DELETE /admin/impersonate` → `admin/impersonate#destroy`
- `DELETE /admin/groups/:id/owners` → `admin/groups#remove_owner`
- `DELETE /admin/groups/:id` → `admin/groups#destroy`
- `DELETE /admin/users/:id` → `admin/users#destroy`
- *... and 73 more*

### Extraction Metadata

**Sources:**
- `routes.rb`: 993 endpoints

**Extraction Methods:**
- llm: 993 endpoints

**Validation Status:** 0 validated, 993 unvalidated

## User Workflows

### 404
- **Type:** creation
- **Resource:** `404`
- **Operations:** GET (1), POST (1)
- **Endpoints:** 2

### 404-Body
- **Type:** retrieval
- **Resource:** `404-body`
- **Operations:** GET (1)
- **Endpoints:** 1

### Bootstrap
- **Type:** retrieval
- **Resource:** `bootstrap`
- **Operations:** GET (3)
- **Endpoints:** 3

### Favicon.Ico
- **Type:** retrieval
- **Resource:** `favicon.ico`
- **Operations:** GET (1)
- **Endpoints:** 1

### Webhooks
- **Type:** creation
- **Resource:** `webhooks`
- **Operations:** GET (1), POST (8)
- **Endpoints:** 9

### Sitemap
- **Type:** retrieval
- **Resource:** `sitemap`
- **Operations:** GET (1)
- **Endpoints:** 1

### Sitemap :Page
- **Type:** retrieval
- **Resource:** `sitemap_:page`
- **Operations:** GET (1)
- **Endpoints:** 1

### Sitemap Recent
- **Type:** retrieval
- **Resource:** `sitemap_recent`
- **Operations:** GET (1)
- **Endpoints:** 1

### News
- **Type:** retrieval
- **Resource:** `news`
- **Operations:** GET (1)
- **Endpoints:** 1

### About
- **Type:** retrieval
- **Resource:** `about`
- **Operations:** GET (2)
- **Endpoints:** 2

### Finish-Installation
- **Type:** creation
- **Resource:** `finish-installation`
- **Operations:** GET (4), POST (1), PUT (1)
- **Endpoints:** 6

### Pub
- **Type:** crud
- **Resource:** `pub`
- **Operations:** DELETE (1), GET (3), PUT (1)
- **Endpoints:** 5

### Directory Items
- **Type:** retrieval
- **Resource:** `directory_items`
- **Operations:** GET (1)
- **Endpoints:** 1

### Site
- **Type:** retrieval
- **Resource:** `site`
- **Operations:** GET (7)
- **Endpoints:** 7

### Srv
- **Type:** retrieval
- **Resource:** `srv`
- **Operations:** GET (1)
- **Endpoints:** 1

### Wizard
- **Type:** operation
- **Resource:** `wizard`
- **Operations:** GET (2), PUT (1)
- **Endpoints:** 3

### Admin
- **Type:** creation
- **Resource:** `admin`
- **Operations:** DELETE (26), GET (105), POST (34), PUT (42)
- **Endpoints:** 207

### Status
- **Type:** retrieval
- **Resource:** `status`
- **Operations:** GET (1)
- **Endpoints:** 1

### Cancel
- **Type:** operation
- **Resource:** `cancel`
- **Operations:** DELETE (1)
- **Endpoints:** 1

### Rollback
- **Type:** creation
- **Resource:** `rollback`
- **Operations:** POST (1)
- **Endpoints:** 1

### Readonly
- **Type:** operation
- **Resource:** `readonly`
- **Operations:** PUT (1)
- **Endpoints:** 1

### Upload
- **Type:** creation
- **Resource:** `upload`
- **Operations:** GET (1), POST (1)
- **Endpoints:** 2

### Upload Url
- **Type:** retrieval
- **Resource:** `upload_url`
- **Operations:** GET (1)
- **Endpoints:** 1

### Badges
- **Type:** creation
- **Resource:** `badges`
- **Operations:** DELETE (1), GET (8), POST (4), PUT (1)
- **Endpoints:** 14

### Groups
- **Type:** creation
- **Resource:** `groups`
- **Operations:** DELETE (1), GET (9), PATCH (1), POST (2), PUT (3)
- **Endpoints:** 16

### Search
- **Type:** creation
- **Resource:** `search`
- **Operations:** GET (3), POST (1)
- **Endpoints:** 4

### Config
- **Type:** creation
- **Resource:** `config`
- **Operations:** DELETE (4), GET (58), POST (5), PUT (10)
- **Endpoints:** 77

### Section
- **Type:** retrieval
- **Resource:** `section`
- **Operations:** GET (1)
- **Endpoints:** 1

### Admin Notices
- **Type:** operation
- **Resource:** `admin_notices`
- **Operations:** DELETE (1)
- **Endpoints:** 1

### Unknown Reviewables
- **Type:** operation
- **Resource:** `unknown_reviewables`
- **Operations:** DELETE (1)
- **Endpoints:** 1

### Email
- **Type:** creation
- **Resource:** `email`
- **Operations:** GET (2), POST (1)
- **Endpoints:** 3

### Extra-Locales
- **Type:** retrieval
- **Resource:** `extra-locales`
- **Operations:** GET (1)
- **Endpoints:** 1

### Session
- **Type:** creation
- **Resource:** `session`
- **Operations:** DELETE (1), GET (12), POST (7)
- **Endpoints:** 20

### Review
- **Type:** creation
- **Resource:** `review`
- **Operations:** DELETE (2), GET (7), POST (1), PUT (4)
- **Endpoints:** 14

### Reviewable Claimed Topics
- **Type:** creation
- **Resource:** `reviewable_claimed_topics`
- **Operations:** DELETE (1), POST (1)
- **Endpoints:** 2

### Composer
- **Type:** retrieval
- **Resource:** `composer`
- **Operations:** GET (1)
- **Endpoints:** 1

### Composer Messages
- **Type:** retrieval
- **Resource:** `composer_messages`
- **Operations:** GET (2)
- **Endpoints:** 2

### Login
- **Type:** creation
- **Resource:** `login`
- **Operations:** GET (1), POST (1)
- **Endpoints:** 2

### Login-Required
- **Type:** retrieval
- **Resource:** `login-required`
- **Operations:** GET (1)
- **Endpoints:** 1

### Login-Preferences
- **Type:** retrieval
- **Resource:** `login-preferences`
- **Operations:** GET (1)
- **Endpoints:** 1

### Signup
- **Type:** retrieval
- **Resource:** `signup`
- **Operations:** GET (1)
- **Endpoints:** 1

### Password-Reset
- **Type:** retrieval
- **Resource:** `password-reset`
- **Operations:** GET (1)
- **Endpoints:** 1

### Privacy
- **Type:** retrieval
- **Resource:** `privacy`
- **Operations:** GET (1)
- **Endpoints:** 1

### Tos
- **Type:** retrieval
- **Resource:** `tos`
- **Operations:** GET (1)
- **Endpoints:** 1

### Faq
- **Type:** retrieval
- **Resource:** `faq`
- **Operations:** GET (1)
- **Endpoints:** 1

### Guidelines
- **Type:** retrieval
- **Resource:** `guidelines`
- **Operations:** GET (1)
- **Endpoints:** 1

### Rules
- **Type:** retrieval
- **Resource:** `rules`
- **Operations:** GET (1)
- **Endpoints:** 1

### Conduct
- **Type:** retrieval
- **Resource:** `conduct`
- **Operations:** GET (1)
- **Endpoints:** 1

### My
- **Type:** retrieval
- **Resource:** `my`
- **Operations:** GET (1)
- **Endpoints:** 1

### .Well-Known
- **Type:** retrieval
- **Resource:** `.well-known`
- **Operations:** GET (4)
- **Endpoints:** 4

### User-Cards
- **Type:** retrieval
- **Resource:** `user-cards`
- **Operations:** GET (1)
- **Endpoints:** 1

### Directory-Columns
- **Type:** retrieval
- **Resource:** `directory-columns`
- **Operations:** GET (1)
- **Endpoints:** 1

### Edit-Directory-Columns
- **Type:** operation
- **Resource:** `edit-directory-columns`
- **Operations:** GET (1), PUT (1)
- **Endpoints:** 2

### Users
- **Type:** creation
- **Resource:** `users`
- **Operations:** DELETE (2), GET (28), POST (13), PUT (12)
- **Endpoints:** 55

### U
- **Type:** creation
- **Resource:** `u`
- **Operations:** DELETE (2), GET (28), POST (13), PUT (12)
- **Endpoints:** 55

### #{Root Path}
- **Type:** creation
- **Resource:** `#{root_path}`
- **Operations:** DELETE (3), GET (40), POST (4), PUT (10)
- **Endpoints:** 57

### User-Badges
- **Type:** retrieval
- **Resource:** `user-badges`
- **Operations:** GET (2)
- **Endpoints:** 2

### User Avatar
- **Type:** creation
- **Resource:** `user_avatar`
- **Operations:** GET (1), POST (1)
- **Endpoints:** 2

### Letter Avatar
- **Type:** retrieval
- **Resource:** `letter_avatar`
- **Operations:** GET (1)
- **Endpoints:** 1

### Letter Avatar Proxy
- **Type:** retrieval
- **Resource:** `letter_avatar_proxy`
- **Operations:** GET (1)
- **Endpoints:** 1

### Svg-Sprite
- **Type:** retrieval
- **Resource:** `svg-sprite`
- **Operations:** GET (4)
- **Endpoints:** 4

### Highlight-Js
- **Type:** retrieval
- **Resource:** `highlight-js`
- **Operations:** GET (1)
- **Endpoints:** 1

### Stylesheets
- **Type:** retrieval
- **Resource:** `stylesheets`
- **Operations:** GET (2)
- **Endpoints:** 2

### Color-Scheme-Stylesheet
- **Type:** retrieval
- **Resource:** `color-scheme-stylesheet`
- **Operations:** GET (1)
- **Endpoints:** 1

### Theme-Javascripts
- **Type:** retrieval
- **Resource:** `theme-javascripts`
- **Operations:** GET (3)
- **Endpoints:** 3

### Uploads
- **Type:** creation
- **Resource:** `uploads`
- **Operations:** GET (5), POST (9)
- **Endpoints:** 14

### Secure-Media-Uploads
- **Type:** retrieval
- **Resource:** `secure-media-uploads`
- **Operations:** GET (1)
- **Endpoints:** 1

### Secure-Uploads
- **Type:** retrieval
- **Resource:** `secure-uploads`
- **Operations:** GET (1)
- **Endpoints:** 1

### Posts
- **Type:** creation
- **Resource:** `posts`
- **Operations:** DELETE (4), GET (15), POST (1), PUT (12)
- **Endpoints:** 32

### Private-Posts
- **Type:** retrieval
- **Resource:** `private-posts`
- **Operations:** GET (1)
- **Endpoints:** 1

### G
- **Type:** creation
- **Resource:** `g`
- **Operations:** DELETE (1), GET (7), PATCH (1), POST (2), PUT (2)
- **Endpoints:** 13

### Members
- **Type:** operation
- **Resource:** `members`
- **Operations:** DELETE (1), PUT (1)
- **Endpoints:** 2

### Leave
- **Type:** operation
- **Resource:** `leave`
- **Operations:** DELETE (1)
- **Endpoints:** 1

### Handle Membership Request
- **Type:** operation
- **Resource:** `handle_membership_request`
- **Operations:** PUT (1)
- **Endpoints:** 1

### By-Id
- **Type:** retrieval
- **Resource:** `by-id`
- **Operations:** GET (1)
- **Endpoints:** 1

### :Name
- **Type:** creation
- **Resource:** `:name`
- **Operations:** GET (25), POST (2)
- **Endpoints:** 27

### Associated Groups
- **Type:** retrieval
- **Resource:** `associated_groups`
- **Operations:** GET (1)
- **Endpoints:** 1

### Slugs
- **Type:** creation
- **Resource:** `slugs`
- **Operations:** POST (1)
- **Endpoints:** 1

### Bookmarks
- **Type:** creation
- **Resource:** `bookmarks`
- **Operations:** DELETE (1), POST (1), PUT (3)
- **Endpoints:** 5

### Post Localizations
- **Type:** creation
- **Resource:** `post_localizations`
- **Operations:** DELETE (1), GET (1), POST (1)
- **Endpoints:** 3

### Topic Localizations
- **Type:** creation
- **Resource:** `topic_localizations`
- **Operations:** DELETE (1), GET (1), POST (1)
- **Endpoints:** 3

### Tag Localizations
- **Type:** creation
- **Resource:** `tag_localizations`
- **Operations:** DELETE (1), GET (1), POST (1)
- **Endpoints:** 3

### Notifications
- **Type:** creation
- **Resource:** `notifications`
- **Operations:** DELETE (1), GET (2), POST (1), PUT (3)
- **Endpoints:** 7

### Auth
- **Type:** creation
- **Resource:** `auth`
- **Operations:** GET (3), POST (3)
- **Endpoints:** 6

### Associate
- **Type:** creation
- **Resource:** `associate`
- **Operations:** GET (1), POST (1)
- **Endpoints:** 2

### Clicks
- **Type:** creation
- **Resource:** `clicks`
- **Operations:** POST (1)
- **Endpoints:** 1

### Post Action Users
- **Type:** retrieval
- **Resource:** `post_action_users`
- **Operations:** GET (1)
- **Endpoints:** 1

### Post Readers
- **Type:** retrieval
- **Resource:** `post_readers`
- **Operations:** GET (1)
- **Endpoints:** 1

### Post Actions
- **Type:** creation
- **Resource:** `post_actions`
- **Operations:** DELETE (1), POST (1)
- **Endpoints:** 2

### User Actions
- **Type:** retrieval
- **Resource:** `user_actions`
- **Operations:** GET (2)
- **Endpoints:** 2

### User Badges
- **Type:** creation
- **Resource:** `user_badges`
- **Operations:** DELETE (1), GET (1), POST (1), PUT (1)
- **Endpoints:** 4

### Categories
- **Type:** creation
- **Resource:** `categories`
- **Operations:** DELETE (1), GET (5), POST (3), PUT (1)
- **Endpoints:** 10

### Category
- **Type:** creation
- **Resource:** `category`
- **Operations:** GET (1), POST (2), PUT (1)
- **Endpoints:** 4

### Categories And Latest
- **Type:** retrieval
- **Resource:** `categories_and_latest`
- **Operations:** GET (1)
- **Endpoints:** 1

### Categories And Top
- **Type:** retrieval
- **Resource:** `categories_and_top`
- **Operations:** GET (1)
- **Endpoints:** 1

### Categories And Hot
- **Type:** retrieval
- **Resource:** `categories_and_hot`
- **Operations:** GET (1)
- **Endpoints:** 1

### C
- **Type:** retrieval
- **Resource:** `c`
- **Operations:** GET (10)
- **Endpoints:** 10

### New-Category
- **Type:** retrieval
- **Resource:** `new-category`
- **Operations:** GET (3)
- **Endpoints:** 3

### Hashtags
- **Type:** retrieval
- **Resource:** `hashtags`
- **Operations:** GET (3)
- **Endpoints:** 3

### Latest.Rss
- **Type:** retrieval
- **Resource:** `latest.rss`
- **Operations:** GET (1)
- **Endpoints:** 1

### Top.Rss
- **Type:** retrieval
- **Resource:** `top.rss`
- **Operations:** GET (1)
- **Endpoints:** 1

### Hot.Rss
- **Type:** retrieval
- **Resource:** `hot.rss`
- **Operations:** GET (1)
- **Endpoints:** 1

### Filter
- **Type:** retrieval
- **Resource:** `filter`
- **Operations:** GET (1)
- **Endpoints:** 1

### T
- **Type:** creation
- **Resource:** `t`
- **Operations:** DELETE (2), GET (18), POST (8), PUT (25)
- **Endpoints:** 53

### Topics
- **Type:** creation
- **Resource:** `topics`
- **Operations:** GET (15), POST (1), PUT (3)
- **Endpoints:** 19

### Similar Topics
- **Type:** retrieval
- **Resource:** `similar_topics`
- **Operations:** GET (1)
- **Endpoints:** 1

### Embed
- **Type:** retrieval
- **Resource:** `embed`
- **Operations:** GET (4)
- **Endpoints:** 4

### New-Topic
- **Type:** retrieval
- **Resource:** `new-topic`
- **Operations:** GET (1)
- **Endpoints:** 1

### New-Message
- **Type:** retrieval
- **Resource:** `new-message`
- **Operations:** GET (1)
- **Endpoints:** 1

### New-Invite
- **Type:** retrieval
- **Resource:** `new-invite`
- **Operations:** GET (1)
- **Endpoints:** 1

### P
- **Type:** retrieval
- **Resource:** `p`
- **Operations:** GET (1)
- **Endpoints:** 1

### Raw
- **Type:** retrieval
- **Resource:** `raw`
- **Operations:** GET (1)
- **Endpoints:** 1

### Invites
- **Type:** creation
- **Resource:** `invites`
- **Operations:** DELETE (2), GET (2), PATCH (1), POST (6), PUT (2)
- **Endpoints:** 13

### Export Csv
- **Type:** creation
- **Resource:** `export_csv`
- **Operations:** GET (1), POST (1)
- **Endpoints:** 2

### Onebox
- **Type:** retrieval
- **Resource:** `onebox`
- **Operations:** GET (1)
- **Endpoints:** 1

### Inline-Onebox
- **Type:** retrieval
- **Resource:** `inline-onebox`
- **Operations:** GET (1)
- **Endpoints:** 1

### Exception
- **Type:** retrieval
- **Resource:** `exception`
- **Operations:** GET (1)
- **Endpoints:** 1

### Message-Bus
- **Type:** retrieval
- **Resource:** `message-bus`
- **Operations:** GET (1)
- **Endpoints:** 1

### Drafts
- **Type:** creation
- **Resource:** `drafts`
- **Operations:** DELETE (2), GET (2), POST (1)
- **Endpoints:** 5

### Service-Worker.Js
- **Type:** retrieval
- **Resource:** `service-worker.js`
- **Operations:** GET (1)
- **Endpoints:** 1

### Cdn Asset
- **Type:** retrieval
- **Resource:** `cdn_asset`
- **Operations:** GET (1)
- **Endpoints:** 1

### Favicon
- **Type:** retrieval
- **Resource:** `favicon`
- **Operations:** GET (1)
- **Endpoints:** 1

### Robots.Txt
- **Type:** retrieval
- **Resource:** `robots.txt`
- **Operations:** GET (1)
- **Endpoints:** 1

### Robots-Builder.Json
- **Type:** retrieval
- **Resource:** `robots-builder.json`
- **Operations:** GET (1)
- **Endpoints:** 1

### Llms.Txt
- **Type:** retrieval
- **Resource:** `llms.txt`
- **Operations:** GET (1)
- **Endpoints:** 1

### Offline.Html
- **Type:** retrieval
- **Resource:** `offline.html`
- **Operations:** GET (1)
- **Endpoints:** 1

### Manifest.Webmanifest
- **Type:** retrieval
- **Resource:** `manifest.webmanifest`
- **Operations:** GET (1)
- **Endpoints:** 1

### Manifest.Json
- **Type:** retrieval
- **Resource:** `manifest.json`
- **Operations:** GET (1)
- **Endpoints:** 1

### Apple-App-Site-Association
- **Type:** retrieval
- **Resource:** `apple-app-site-association`
- **Operations:** GET (1)
- **Endpoints:** 1

### Opensearch
- **Type:** retrieval
- **Resource:** `opensearch`
- **Operations:** GET (1)
- **Endpoints:** 1

### Tag
- **Type:** creation
- **Resource:** `tag`
- **Operations:** DELETE (4), GET (12), POST (2), PUT (5)
- **Endpoints:** 23

### Tags
- **Type:** creation
- **Resource:** `tags`
- **Operations:** DELETE (1), GET (7), POST (2)
- **Endpoints:** 10

### Tag Groups
- **Type:** creation
- **Resource:** `tag_groups`
- **Operations:** DELETE (1), GET (3), PATCH (1), POST (2), PUT (1)
- **Endpoints:** 8

### User-Api-Key
- **Type:** creation
- **Resource:** `user-api-key`
- **Operations:** GET (2), POST (4)
- **Endpoints:** 6

### User-Api-Key-Client
- **Type:** creation
- **Resource:** `user-api-key-client`
- **Operations:** GET (1), POST (1)
- **Endpoints:** 2

### Calendar-Subscriptions
- **Type:** creation
- **Resource:** `calendar-subscriptions`
- **Operations:** DELETE (1), GET (1), POST (1)
- **Endpoints:** 3

### Safe-Mode
- **Type:** creation
- **Resource:** `safe-mode`
- **Operations:** GET (1), POST (1)
- **Endpoints:** 2

### Dev-Mode
- **Type:** creation
- **Resource:** `dev-mode`
- **Operations:** GET (1), POST (1)
- **Endpoints:** 2

### Theme-Qunit
- **Type:** retrieval
- **Resource:** `theme-qunit`
- **Operations:** GET (1)
- **Endpoints:** 1

### Testem-Theme-Qunit
- **Type:** retrieval
- **Resource:** `testem-theme-qunit`
- **Operations:** GET (1)
- **Endpoints:** 1

### Push Notifications
- **Type:** creation
- **Resource:** `push_notifications`
- **Operations:** POST (2)
- **Endpoints:** 2

### Permalink-Check
- **Type:** retrieval
- **Resource:** `permalink-check`
- **Operations:** GET (1)
- **Endpoints:** 1

### Do-Not-Disturb
- **Type:** creation
- **Resource:** `do-not-disturb`
- **Operations:** DELETE (1), POST (1)
- **Endpoints:** 2

### Presence
- **Type:** creation
- **Resource:** `presence`
- **Operations:** GET (1), POST (1)
- **Endpoints:** 2

### User-Status
- **Type:** crud
- **Resource:** `user-status`
- **Operations:** DELETE (1), GET (1), PUT (1)
- **Endpoints:** 3

### Sidebar Sections
- **Type:** creation
- **Resource:** `sidebar_sections`
- **Operations:** DELETE (1), GET (1), PATCH (1), POST (1), PUT (2)
- **Endpoints:** 6

### Pageview
- **Type:** creation
- **Resource:** `pageview`
- **Operations:** POST (1)
- **Endpoints:** 1

### Form-Templates
- **Type:** retrieval
- **Resource:** `form-templates`
- **Operations:** GET (2)
- **Endpoints:** 2

### Emojis
- **Type:** retrieval
- **Resource:** `emojis`
- **Operations:** GET (2)
- **Endpoints:** 2

### Test Net Http Timeouts
- **Type:** retrieval
- **Resource:** `test_net_http_timeouts`
- **Operations:** GET (1)
- **Endpoints:** 1

### Test Net Http Headers
- **Type:** retrieval
- **Resource:** `test_net_http_headers`
- **Operations:** GET (1)
- **Endpoints:** 1

### *Url
- **Type:** retrieval
- **Resource:** `*url`
- **Operations:** GET (1)
- **Endpoints:** 1

## Frontend-Backend Integrations

**Total API calls:** 6

### `{var}/about.json`
- **Calls:** 2
- **Type:** fetch
- **Used in:**
  - `frontend/discourse/testem.js`
  - `frontend/discourse/testem.js`

### `{var}/pageview`
- **Calls:** 2
- **Type:** fetch
- **Used in:**
  - `frontend/discourse/scripts/pageview.js`
  - `frontend/discourse/scripts/pageview.js`

### `{var}bootstrap/plugin-test-info.json?target={var}`
- **Calls:** 2
- **Type:** fetch
- **Used in:**
  - `frontend/discourse/public/assets/scripts/discourse-test-load-dynamic-js.js`
  - `frontend/discourse/public/assets/scripts/discourse-test-load-dynamic-js.js`
