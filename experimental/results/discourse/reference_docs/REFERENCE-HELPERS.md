# helpers - API Reference

**Component Type:** rails_helpers
**Language:** ruby
**Path:** `app/helpers`

---

## Overview


This component contains **0 classes**, **11 modules**, and **43 methods**.

### Source Files

- [`qunit_helper.rb`](app/helpers/qunit_helper.rb)
- [`topic_post_bookmarkable_helper.rb`](app/helpers/topic_post_bookmarkable_helper.rb)
- [`embed_helper.rb`](app/helpers/embed_helper.rb)
- [`posts_helper.rb`](app/helpers/posts_helper.rb)
- [`topics_helper.rb`](app/helpers/topics_helper.rb)
... and 6 more files

---

## API Reference


### Modules

####`QunitHelper`

*Ruby module*

**Defined in:** [`app/helpers/qunit_helper.rb`](app/helpers/qunit_helper.rb#L3)

##### Methods

<details>
<summary><code>theme_tests()</code></summary>

**Defined in:** [`app/helpers/qunit_helper.rb`](app/helpers/qunit_helper.rb#L4)


</details>


---

####`TopicPostBookmarkableHelper`

*Ruby module*

**Defined in:** [`app/helpers/topic_post_bookmarkable_helper.rb`](app/helpers/topic_post_bookmarkable_helper.rb#L3)


---

####`ClassMethods`

*Ruby module in TopicPostBookmarkableHelper*

**Defined in:** [`app/helpers/topic_post_bookmarkable_helper.rb`](app/helpers/topic_post_bookmarkable_helper.rb#L6)

##### Methods

<details>
<summary><code>sync_topic_user_bookmarked(topic, opts)</code></summary>

**Defined in:** [`app/helpers/topic_post_bookmarkable_helper.rb`](app/helpers/topic_post_bookmarkable_helper.rb#L7)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | None | — | — |
| `topic` | None | — | — |
| `opts` | None | — | — |

</details>


---

####`EmbedHelper`

*Ruby module*

**Defined in:** [`app/helpers/embed_helper.rb`](app/helpers/embed_helper.rb#L3)

##### Methods

<details>
<summary><code>embed_post_date_title()</code></summary>

**Defined in:** [`app/helpers/embed_helper.rb`](app/helpers/embed_helper.rb#L4)


</details>

<details>
<summary><code>embed_post_date()</code></summary>

**Defined in:** [`app/helpers/embed_helper.rb`](app/helpers/embed_helper.rb#L8)


</details>

<details>
<summary><code>get_html()</code></summary>

**Defined in:** [`app/helpers/embed_helper.rb`](app/helpers/embed_helper.rb#L22)


</details>


---

####`PostsHelper`

*Ruby module*

**Defined in:** [`app/helpers/posts_helper.rb`](app/helpers/posts_helper.rb#L3)

##### Methods

<details>
<summary><code>clear_canonical_cache!()</code></summary>

**Defined in:** [`app/helpers/posts_helper.rb`](app/helpers/posts_helper.rb#L8)


</details>

<details>
<summary><code>canonical_redis_key()</code></summary>

**Defined in:** [`app/helpers/posts_helper.rb`](app/helpers/posts_helper.rb#L13)


</details>

<details>
<summary><code>cached_post_url(use_canonical:)</code></summary>

**Defined in:** [`app/helpers/posts_helper.rb`](app/helpers/posts_helper.rb#L17)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `post` | None | — | — |
| `use_canonical:` | None | — | — |

</details>


---

####`TopicsHelper`

*Ruby module*

**Defined in:** [`app/helpers/topics_helper.rb`](app/helpers/topics_helper.rb#L3)

##### Methods

<details>
<summary><code>render_topic_title()</code></summary>

**Defined in:** [`app/helpers/topics_helper.rb`](app/helpers/topics_helper.rb#L6)


</details>

<details>
<summary><code>categories_breadcrumb()</code></summary>

**Defined in:** [`app/helpers/topics_helper.rb`](app/helpers/topics_helper.rb#L10)


</details>

<details>
<summary><code>localize_topic_view_content()</code></summary>

**Defined in:** [`app/helpers/topics_helper.rb`](app/helpers/topics_helper.rb#L24)


</details>


---

####`ListHelper`

*Ruby module*

**Defined in:** [`app/helpers/list_helper.rb`](app/helpers/list_helper.rb#L3)

##### Methods

<details>
<summary><code>page_links()</code></summary>

**Defined in:** [`app/helpers/list_helper.rb`](app/helpers/list_helper.rb#L4)


</details>


---

####`UserNotificationsHelper`

*Ruby module*

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L3)

##### Methods

<details>
<summary><code>indent(by)</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L6)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | None | — | — |
| `by` | None | yes | — |

</details>

<details>
<summary><code>correct_top_margin(desired)</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L13)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `html` | None | — | — |
| `desired` | None | — | — |

</details>

<details>
<summary><code>logo_url()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L21)


</details>

<details>
<summary><code>html_site_link()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L28)


</details>

<details>
<summary><code>first_paragraphs_from()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L32)


</details>

<details>
<summary><code>email_excerpt(post)</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L57)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `html_arg` | None | — | — |
| `post` | None | yes | — |

</details>

<details>
<summary><code>normalize_name()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L62)


</details>

<details>
<summary><code>show_username_on_post()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L66)


</details>

<details>
<summary><code>show_name_on_post()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L74)


</details>

<details>
<summary><code>format_for_email(use_excerpt)</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L79)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `post` | None | — | — |
| `use_excerpt` | None | — | — |

</details>

<details>
<summary><code>digest_custom_html()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L84)


</details>

<details>
<summary><code>digest_custom_text()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L88)


</details>

<details>
<summary><code>digest_custom()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L92)


</details>

<details>
<summary><code>show_image_with_url()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L96)


</details>

<details>
<summary><code>email_image_url()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L100)


</details>

<details>
<summary><code>url_for_email()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L104)


</details>

<details>
<summary><code>render_digest_header()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L110)


</details>


---

####`CommonHelper`

*Ruby module*

**Defined in:** [`app/helpers/common_helper.rb`](app/helpers/common_helper.rb#L3)

##### Methods

<details>
<summary><code>render_google_universal_analytics_code()</code></summary>

**Defined in:** [`app/helpers/common_helper.rb`](app/helpers/common_helper.rb#L4)


</details>

<details>
<summary><code>render_google_tag_manager_head_code()</code></summary>

**Defined in:** [`app/helpers/common_helper.rb`](app/helpers/common_helper.rb#L10)


</details>

<details>
<summary><code>render_google_tag_manager_body_code()</code></summary>

**Defined in:** [`app/helpers/common_helper.rb`](app/helpers/common_helper.rb#L14)


</details>

<details>
<summary><code>render_adobe_analytics_tags_code()</code></summary>

**Defined in:** [`app/helpers/common_helper.rb`](app/helpers/common_helper.rb#L18)


</details>


---

####`EmojiHelper`

*Ruby module*

**Defined in:** [`app/helpers/emoji_helper.rb`](app/helpers/emoji_helper.rb#L3)

##### Methods

<details>
<summary><code>emoji_codes_to_img()</code></summary>

**Defined in:** [`app/helpers/emoji_helper.rb`](app/helpers/emoji_helper.rb#L4)


</details>


---

####`EmailHelper`

*Ruby module*

**Defined in:** [`app/helpers/email_helper.rb`](app/helpers/email_helper.rb#L5)

##### Methods

<details>
<summary><code>mailing_list_topic(post_count)</code></summary>

**Defined in:** [`app/helpers/email_helper.rb`](app/helpers/email_helper.rb#L6)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `topic` | None | — | — |
| `post_count` | None | — | — |

</details>

<details>
<summary><code>mailing_list_topic_text()</code></summary>

**Defined in:** [`app/helpers/email_helper.rb`](app/helpers/email_helper.rb#L16)


</details>

<details>
<summary><code>private_topic_title()</code></summary>

**Defined in:** [`app/helpers/email_helper.rb`](app/helpers/email_helper.rb#L21)


</details>

<details>
<summary><code>email_topic_link()</code></summary>

**Defined in:** [`app/helpers/email_helper.rb`](app/helpers/email_helper.rb#L25)


</details>

<details>
<summary><code>email_html_template()</code></summary>

**Defined in:** [`app/helpers/email_helper.rb`](app/helpers/email_helper.rb#L30)


</details>

<details>
<summary><code>dark_mode_meta_tags()</code></summary>

**Defined in:** [`app/helpers/email_helper.rb`](app/helpers/email_helper.rb#L46)


</details>

<details>
<summary><code>dark_mode_styles()</code></summary>

**Defined in:** [`app/helpers/email_helper.rb`](app/helpers/email_helper.rb#L53)


</details>

<details>
<summary><code>extract_details()</code></summary>

**Defined in:** [`app/helpers/email_helper.rb`](app/helpers/email_helper.rb#L119)


</details>

<details>
<summary><code>partial_for()</code></summary>

**Defined in:** [`app/helpers/email_helper.rb`](app/helpers/email_helper.rb#L127)


</details>


---



## Constants

| Name | Value | Line |
|------|-------|------|
| `CACHE_URL_DURATION` | `12.hours.to_i` | 6 |

---

## Usage Examples

*Example usage coming soon.*

---

## Related Components

**Category:** Utility

*See also:*
- [Project Overview](../README.md)
- [Architecture](../ARCHITECTURE.md)

---

**Generated:** 2026-03-27 12:51:24
**Component:** helpers
**API Coverage:** 0.0%
**Total APIs:** 54