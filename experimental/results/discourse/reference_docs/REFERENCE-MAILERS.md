# mailers - API Reference

**Component Type:** rails_mailers
**Language:** ruby
**Path:** `app/mailers`
**API Coverage:** 1.639344262295082%
---

## Overview


This component contains **9 classes**, **0 modules**, and **51 methods**.

### Source Files

- [`user_notifications.rb`](app/mailers/user_notifications.rb)
- [`subscription_mailer.rb`](app/mailers/subscription_mailer.rb)
- [`group_smtp_mailer.rb`](app/mailers/group_smtp_mailer.rb)
- [`rejection_mailer.rb`](app/mailers/rejection_mailer.rb)
- [`admin_confirmation_mailer.rb`](app/mailers/admin_confirmation_mailer.rb)
... and 4 more files

---

## API Reference

### Classes

#### `UserNotifications`

*No description available.*


**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L3)



##### Methods

<details>
<summary><code>signup(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L12)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>activation_reminder(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L16)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>signup_after_approval(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L24)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>post_approved(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L42)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>signup_after_reject(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L58)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>suspicious_login(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L69)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>notify_old_email(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L89)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>notify_old_email_add(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L99)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>confirm_old_email(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L109)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>confirm_old_email_add(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L117)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>confirm_new_email(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L125)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>forgot_password(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L139)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>email_login(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L147)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>admin_login(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L151)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>account_created(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L155)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>account_silenced(opts = nil)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L163)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `nil` | — |


</details>

<details>
<summary><code>account_deleted(reviewable)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L189)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `email` | *any* | — | — |
| `reviewable` | *any* | — | — |


</details>

<details>
<summary><code>account_suspended(opts = nil)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L206)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `nil` | — |


</details>

<details>
<summary><code>account_exists(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L232)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>account_second_factor_disabled(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L242)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>digest(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L252)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>

<details>
<summary><code>user_replied(opts)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L389)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | — | — |


</details>

<details>
<summary><code>user_quoted(opts)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L397)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | — | — |


</details>

<details>
<summary><code>user_linked(opts)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L405)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | — | — |


</details>

<details>
<summary><code>user_mentioned(opts)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L413)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | — | — |


</details>

<details>
<summary><code>group_mentioned(opts)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L422)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | — | — |


</details>

<details>
<summary><code>user_posted(opts)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L430)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | — | — |


</details>

<details>
<summary><code>user_private_message(opts)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L439)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | — | — |


</details>

<details>
<summary><code>user_invited_to_private_message(opts)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L453)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | — | — |


</details>

<details>
<summary><code>user_invited_to_topic(opts)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L459)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | — | — |


</details>

<details>
<summary><code>user_watching_first_post(opts)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L467)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | — | — |


</details>

<details>
<summary><code>mailing_list_notify(post)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L471)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `post` | *any* | — | — |


</details>

<details>
<summary><code>user_locale()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L490)



</details>

<details>
<summary><code>email_post_markdown(add_posted_by = false)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L494)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `post` | *any* | — | — |
| `add_posted_by` | *any* | `false` | — |


</details>

<details>
<summary><code>get_context_posts(topic_user, user)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L502)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `post` | *any* | — | — |
| `topic_user` | *any* | — | — |
| `user` | *any* | — | — |


</details>

<details>
<summary><code>notification_email(opts)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L530)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | — | — |


</details>

<details>
<summary><code>send_notification_email()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L598)



</details>

<details>
<summary><code>participants(recipient_user, reveal_staged_email: = false)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L817)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `post` | *any* | — | — |
| `recipient_user` | *any* | — | — |
| `reveal_staged_email:` | *any* | `false` | — |


</details>

<details>
<summary><code>build_user_email_token_by_template(user, email_token)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L874)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `template` | *any* | — | — |
| `user` | *any* | — | — |
| `email_token` | *any* | — | — |


</details>

<details>
<summary><code>build_summary_for()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L884)



</details>

<details>
<summary><code>summary_new_users_count()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L897)



</details>


---

#### `SubscriptionMailer`

*No description available.*


**Defined in:** [`app/mailers/subscription_mailer.rb`](app/mailers/subscription_mailer.rb#L3)



##### Methods

<details>
<summary><code>confirm_unsubscribe(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/subscription_mailer.rb`](app/mailers/subscription_mailer.rb#L6)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>


---

#### `GroupSmtpMailer`

*No description available.*


**Defined in:** [`app/mailers/group_smtp_mailer.rb`](app/mailers/group_smtp_mailer.rb#L3)



##### Methods

<details>
<summary><code>send_mail(to_address, post, cc_addresses: = nil, bcc_addresses: = nil)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/group_smtp_mailer.rb`](app/mailers/group_smtp_mailer.rb#L6)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `from_group` | *any* | — | — |
| `to_address` | *any* | — | — |
| `post` | *any* | — | — |
| `cc_addresses:` | *any* | `nil` | — |
| `bcc_addresses:` | *any* | `nil` | — |


</details>

<details>
<summary><code>html_override()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/group_smtp_mailer.rb`](app/mailers/group_smtp_mailer.rb#L61)



</details>


---

#### `RejectionMailer`

*No description available.*


**Defined in:** [`app/mailers/rejection_mailer.rb`](app/mailers/rejection_mailer.rb#L5)



##### Methods

<details>
<summary><code>send_rejection(message_from, template_args)</code></summary>

Send an email rejection message.

template - i18n key under system_messages
message_from - Who to send the rejection message to
template_args - arguments to pass to i18n for interpolation into the message
    Certain keys are disallowed in template_args to avoid confusing the
    BuildEmailHelper. You can see the list in DISALLOWED_TEMPLATE_ARGS.

**Defined in:** [`app/mailers/rejection_mailer.rb`](app/mailers/rejection_mailer.rb#L35)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `template` | *any* | — | — |
| `message_from` | *any* | — | — |
| `template_args` | *any* | — | — |


</details>


---

#### `AdminConfirmationMailer`

*No description available.*


**Defined in:** [`app/mailers/admin_confirmation_mailer.rb`](app/mailers/admin_confirmation_mailer.rb#L3)



##### Methods

<details>
<summary><code>send_email(target_email, target_username, token)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/admin_confirmation_mailer.rb`](app/mailers/admin_confirmation_mailer.rb#L6)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `to_address` | *any* | — | — |
| `target_email` | *any* | — | — |
| `target_username` | *any* | — | — |
| `token` | *any* | — | — |


</details>


---

#### `InviteMailer`

*No description available.*


**Defined in:** [`app/mailers/invite_mailer.rb`](app/mailers/invite_mailer.rb#L3)



##### Methods

<details>
<summary><code>send_invite(invite_to_topic: = false)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/invite_mailer.rb`](app/mailers/invite_mailer.rb#L8)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `invite` | *any* | — | — |
| `invite_to_topic:` | *any* | `false` | — |


</details>

<details>
<summary><code>send_password_instructions()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/invite_mailer.rb`](app/mailers/invite_mailer.rb#L71)



</details>


---

#### `VersionMailer`

*No description available.*


**Defined in:** [`app/mailers/version_mailer.rb`](app/mailers/version_mailer.rb#L3)



##### Methods

<details>
<summary><code>send_notice()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/version_mailer.rb`](app/mailers/version_mailer.rb#L6)



</details>


---

#### `DownloadBackupMailer`

*No description available.*


**Defined in:** [`app/mailers/download_backup_mailer.rb`](app/mailers/download_backup_mailer.rb#L3)



##### Methods

<details>
<summary><code>send_email(backup_file_path)</code></summary>

*No description available.*

**Defined in:** [`app/mailers/download_backup_mailer.rb`](app/mailers/download_backup_mailer.rb#L6)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `to_address` | *any* | — | — |
| `backup_file_path` | *any* | — | — |


</details>


---

#### `TestMailer`

*No description available.*


**Defined in:** [`app/mailers/test_mailer.rb`](app/mailers/test_mailer.rb#L3)



##### Methods

<details>
<summary><code>send_test(opts = {})</code></summary>

*No description available.*

**Defined in:** [`app/mailers/test_mailer.rb`](app/mailers/test_mailer.rb#L6)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `to_address` | *any* | — | — |
| `opts` | *any* | `{}` | — |


</details>


---




## Constants

| Name | Value | Line |
|------|-------|------|
| `DISALLOWED_TEMPLATE_ARGS` | `%i[
  to
  from
  base_url
  user_preferences_url
  include_respond_instructions
  html_override
  add_unsubscribe_link
  respond_instructions
  style
  body
  post_id
  topic_id
  subject
  template
  allow_reply_by_email
  private_reply
  from_alias
]` | 8 |

---

## Usage Examples

```ruby
# Example usage of mailers

```

---

## Related Components

**Category:** Unknown

*See also:*
- [Project Overview](../README.md)
- [Architecture](../ARCHITECTURE.md)

---

**Generated:** 2026-03-27 12:51:24
**Component:** mailers
**API Coverage:** 1.639344262295082%
**Total APIs:** 60