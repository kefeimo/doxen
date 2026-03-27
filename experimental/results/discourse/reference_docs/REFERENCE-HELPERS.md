# helpers - API Reference

**Component Type:** rails_helpers
**Language:** ruby
**Path:** `app/helpers`
**API Coverage:** 100.0%
---

## Overview


This component contains **0 classes**, **12 modules**, and **144 methods**.

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

##### Methods

<details>
<summary><code>sync_topic_user_bookmarked()</code></summary>

**Defined in:** [`app/helpers/topic_post_bookmarkable_helper.rb`](app/helpers/topic_post_bookmarkable_helper.rb#L7)


</details>


---

####`ClassMethods`

*Ruby module in TopicPostBookmarkableHelper*

**Defined in:** [`app/helpers/topic_post_bookmarkable_helper.rb`](app/helpers/topic_post_bookmarkable_helper.rb#L6)

##### Methods

<details>
<summary><code>sync_topic_user_bookmarked()</code></summary>

**Defined in:** [`app/helpers/topic_post_bookmarkable_helper.rb`](app/helpers/topic_post_bookmarkable_helper.rb#L7)


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
<summary><code>self.clear_canonical_cache!()</code></summary>

**Defined in:** [`app/helpers/posts_helper.rb`](app/helpers/posts_helper.rb#L8)


</details>

<details>
<summary><code>self.canonical_redis_key()</code></summary>

**Defined in:** [`app/helpers/posts_helper.rb`](app/helpers/posts_helper.rb#L13)


</details>

<details>
<summary><code>cached_post_url()</code></summary>

**Defined in:** [`app/helpers/posts_helper.rb`](app/helpers/posts_helper.rb#L17)


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
<summary><code>indent()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L6)


</details>

<details>
<summary><code>correct_top_margin()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L13)


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
<summary><code>email_excerpt()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L57)


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
<summary><code>format_for_email()</code></summary>

**Defined in:** [`app/helpers/user_notifications_helper.rb`](app/helpers/user_notifications_helper.rb#L79)


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

####`ApplicationHelper`

*Ruby module*

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L6)

##### Methods

<details>
<summary><code>self.extra_body_classes()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L12)


</details>

<details>
<summary><code>discourse_config_environment()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L19)


</details>

<details>
<summary><code>google_universal_analytics_json()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L54)


</details>

<details>
<summary><code>ga_universal_json()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L62)


</details>

<details>
<summary><code>google_tag_manager_json()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L66)


</details>

<details>
<summary><code>csp_nonce_placeholder()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L70)


</details>

<details>
<summary><code>shared_session_key()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L74)


</details>

<details>
<summary><code>is_brotli_req?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L85)


</details>

<details>
<summary><code>is_gzip_req?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L89)


</details>

<details>
<summary><code>generate_import_map()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L93)


</details>

<details>
<summary><code>script_asset_path()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L103)


</details>

<details>
<summary><code>preload_script()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L144)


</details>

<details>
<summary><code>preload_script_url()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L162)


</details>

<details>
<summary><code>add_resource_preload_list()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L177)


</details>

<details>
<summary><code>discourse_csrf_tags()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L184)


</details>

<details>
<summary><code>html_classes()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L191)


</details>

<details>
<summary><code>body_classes()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L203)


</details>

<details>
<summary><code>text_size_class()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L216)


</details>

<details>
<summary><code>escape_unicode()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L228)


</details>

<details>
<summary><code>format_topic_title()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L239)


</details>

<details>
<summary><code>with_format()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L243)


</details>

<details>
<summary><code>age_words()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L251)


</details>

<details>
<summary><code>short_date()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L255)


</details>

<details>
<summary><code>guardian()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L263)


</details>

<details>
<summary><code>admin?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L267)


</details>

<details>
<summary><code>moderator?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L271)


</details>

<details>
<summary><code>staff?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L275)


</details>

<details>
<summary><code>rtl?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L279)


</details>

<details>
<summary><code>html_lang()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L283)


</details>

<details>
<summary><code>title_content()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L287)


</details>

<details>
<summary><code>description_content()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L296)


</details>

<details>
<summary><code>is_crawler_homepage?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L305)


</details>

<details>
<summary><code>crawlable_meta_data()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L309)


</details>

<details>
<summary><code>render_sitelinks_search_tag()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L405)


</details>

<details>
<summary><code>discourse_track_view_session_tag()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L422)


</details>

<details>
<summary><code>gsub_emoji_to_unicode()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L429)


</details>

<details>
<summary><code>application_logo_url()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L433)


</details>

<details>
<summary><code>application_logo_dark_url()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L452)


</details>

<details>
<summary><code>waving_hand_url()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L465)


</details>

<details>
<summary><code>login_path()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L469)


</details>

<details>
<summary><code>mobile_view?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L473)


</details>

<details>
<summary><code>crawler_layout?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L477)


</details>

<details>
<summary><code>include_crawler_content?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L481)


</details>

<details>
<summary><code>modern_mobile_device?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L491)


</details>

<details>
<summary><code>mobile_device?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L495)


</details>

<details>
<summary><code>customization_disabled?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L499)


</details>

<details>
<summary><code>include_ios_native_app_banner?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L503)


</details>

<details>
<summary><code>ios_app_argument()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L507)


</details>

<details>
<summary><code>include_splash_screen?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L516)


</details>

<details>
<summary><code>custom_splash_screen_enabled?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L521)


</details>

<details>
<summary><code>splash_screen_image_animated?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L529)


</details>

<details>
<summary><code>splash_screen_inline_svg()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L534)


</details>

<details>
<summary><code>splash_screen_image_data_uri()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L539)


</details>

<details>
<summary><code>build_splash_screen_image()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L561)


</details>

<details>
<summary><code>allow_plugins?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L582)


</details>

<details>
<summary><code>allow_third_party_plugins?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L586)


</details>

<details>
<summary><code>normalized_safe_mode()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L590)


</details>

<details>
<summary><code>loading_admin?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L600)


</details>

<details>
<summary><code>category_badge()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L607)


</details>

<details>
<summary><code>server_plugin_outlet()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L641)


</details>

<details>
<summary><code>topic_featured_link_domain()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L651)


</details>

<details>
<summary><code>theme_id()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L662)


</details>

<details>
<summary><code>stylesheet_manager()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L670)


</details>

<details>
<summary><code>user_scheme_id()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L675)


</details>

<details>
<summary><code>scheme_id()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L681)


</details>

<details>
<summary><code>user_dark_scheme_id()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L694)


</details>

<details>
<summary><code>dark_scheme_id()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L700)


</details>

<details>
<summary><code>theme_limits_color_schemes?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L713)


</details>

<details>
<summary><code>current_homepage()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L720)


</details>

<details>
<summary><code>build_plugin_html()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L724)


</details>

<details>
<summary><code>crawler_topic_container_schema()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L729)


</details>

<details>
<summary><code>crawler_topic_main_entity_schema()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L739)


</details>

<details>
<summary><code>crawler_post_schema()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L745)


</details>

<details>
<summary><code>replace_plugin_html()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L762)


</details>

<details>
<summary><code>theme_lookup()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L771)


</details>

<details>
<summary><code>theme_translations_lookup()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L781)


</details>

<details>
<summary><code>theme_js_lookup()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L791)


</details>

<details>
<summary><code>discourse_stylesheet_preload_tag()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L801)


</details>

<details>
<summary><code>discourse_stylesheet_link_tag()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L812)


</details>

<details>
<summary><code>discourse_preload_color_scheme_stylesheets()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L829)


</details>

<details>
<summary><code>discourse_color_scheme_stylesheets()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L847)


</details>

<details>
<summary><code>discourse_theme_color_meta_tags()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L883)


</details>

<details>
<summary><code>discourse_color_scheme_meta_tag()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L898)


</details>

<details>
<summary><code>dark_color_scheme?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L912)


</details>

<details>
<summary><code>forced_light_mode?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L917)


</details>

<details>
<summary><code>forced_dark_mode?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L926)


</details>

<details>
<summary><code>light_color_hex_for_name()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L935)


</details>

<details>
<summary><code>dark_color_hex_for_name()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L939)


</details>

<details>
<summary><code>dark_elements_media_query()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L943)


</details>

<details>
<summary><code>light_elements_media_query()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L953)


</details>

<details>
<summary><code>preloaded_json()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L963)


</details>

<details>
<summary><code>client_side_setup_data()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L972)


</details>

<details>
<summary><code>get_absolute_image_url()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L1028)


</details>

<details>
<summary><code>escape_noscript()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L1041)


</details>

<details>
<summary><code>manifest_url()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L1045)


</details>

<details>
<summary><code>can_sign_up?()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L1052)


</details>

<details>
<summary><code>rss_creator()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L1057)


</details>

<details>
<summary><code>anonymous_top_menu_items()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L1061)


</details>

<details>
<summary><code>authentication_data()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L1065)


</details>

<details>
<summary><code>color_scheme_stylesheet_link_tag()</code></summary>

**Defined in:** [`app/helpers/application_helper.rb`](app/helpers/application_helper.rb#L1076)


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
<summary><code>mailing_list_topic()</code></summary>

**Defined in:** [`app/helpers/email_helper.rb`](app/helpers/email_helper.rb#L6)


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
| `CACHE_URL_DURATION` | `<complex>` | 6 |
| `SERVER_PLUGIN_OUTLET_PLUGINS_PREFIXES` | `[]` | 611 |
| `SERVER_PLUGIN_OUTLET_CONNECTOR_TEMPLATES` | `<complex>` | 618 |

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

**Generated:** 2026-03-27 12:37:25
**Component:** helpers
**API Coverage:** 100.0%
**Total APIs:** 156