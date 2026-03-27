# mailers - API Reference

**Component Type:** rails_mailers
**Language:** ruby
**Path:** `app/mailers`
**API Coverage:** 100.0%
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
<summary><code>signup()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L12)



</details>

<details>
<summary><code>activation_reminder()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L16)



</details>

<details>
<summary><code>signup_after_approval()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L24)



</details>

<details>
<summary><code>post_approved()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L42)



</details>

<details>
<summary><code>signup_after_reject()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L58)



</details>

<details>
<summary><code>suspicious_login()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L69)



</details>

<details>
<summary><code>notify_old_email()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L89)



</details>

<details>
<summary><code>notify_old_email_add()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L99)



</details>

<details>
<summary><code>confirm_old_email()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L109)



</details>

<details>
<summary><code>confirm_old_email_add()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L117)



</details>

<details>
<summary><code>confirm_new_email()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L125)



</details>

<details>
<summary><code>forgot_password()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L139)



</details>

<details>
<summary><code>email_login()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L147)



</details>

<details>
<summary><code>admin_login()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L151)



</details>

<details>
<summary><code>account_created()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L155)



</details>

<details>
<summary><code>account_silenced()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L163)



</details>

<details>
<summary><code>account_deleted()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L189)



</details>

<details>
<summary><code>account_suspended()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L206)



</details>

<details>
<summary><code>account_exists()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L232)



</details>

<details>
<summary><code>account_second_factor_disabled()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L242)



</details>

<details>
<summary><code>digest()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L252)



</details>

<details>
<summary><code>user_replied()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L389)



</details>

<details>
<summary><code>user_quoted()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L397)



</details>

<details>
<summary><code>user_linked()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L405)



</details>

<details>
<summary><code>user_mentioned()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L413)



</details>

<details>
<summary><code>group_mentioned()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L422)



</details>

<details>
<summary><code>user_posted()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L430)



</details>

<details>
<summary><code>user_private_message()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L439)



</details>

<details>
<summary><code>user_invited_to_private_message()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L453)



</details>

<details>
<summary><code>user_invited_to_topic()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L459)



</details>

<details>
<summary><code>user_watching_first_post()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L467)



</details>

<details>
<summary><code>mailing_list_notify()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L471)



</details>

<details>
<summary><code>user_locale()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L490)



</details>

<details>
<summary><code>email_post_markdown()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L494)



</details>

<details>
<summary><code>self.get_context_posts()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L502)



</details>

<details>
<summary><code>notification_email()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L530)



</details>

<details>
<summary><code>send_notification_email()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L598)



</details>

<details>
<summary><code>self.participants()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L817)



</details>

<details>
<summary><code>build_user_email_token_by_template()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/user_notifications.rb`](app/mailers/user_notifications.rb#L874)



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
<summary><code>confirm_unsubscribe()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/subscription_mailer.rb`](app/mailers/subscription_mailer.rb#L6)



</details>


---

#### `GroupSmtpMailer`

*No description available.*


**Defined in:** [`app/mailers/group_smtp_mailer.rb`](app/mailers/group_smtp_mailer.rb#L3)



##### Methods

<details>
<summary><code>send_mail()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/group_smtp_mailer.rb`](app/mailers/group_smtp_mailer.rb#L6)



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
<summary><code>send_rejection()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/rejection_mailer.rb`](app/mailers/rejection_mailer.rb#L35)



</details>


---

#### `AdminConfirmationMailer`

*No description available.*


**Defined in:** [`app/mailers/admin_confirmation_mailer.rb`](app/mailers/admin_confirmation_mailer.rb#L3)



##### Methods

<details>
<summary><code>send_email()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/admin_confirmation_mailer.rb`](app/mailers/admin_confirmation_mailer.rb#L6)



</details>


---

#### `InviteMailer`

*No description available.*


**Defined in:** [`app/mailers/invite_mailer.rb`](app/mailers/invite_mailer.rb#L3)



##### Methods

<details>
<summary><code>send_invite()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/invite_mailer.rb`](app/mailers/invite_mailer.rb#L8)



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
<summary><code>send_email()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/download_backup_mailer.rb`](app/mailers/download_backup_mailer.rb#L6)



</details>


---

#### `TestMailer`

*No description available.*


**Defined in:** [`app/mailers/test_mailer.rb`](app/mailers/test_mailer.rb#L3)



##### Methods

<details>
<summary><code>send_test()</code></summary>

*No description available.*

**Defined in:** [`app/mailers/test_mailer.rb`](app/mailers/test_mailer.rb#L6)



</details>


---




## Constants

| Name | Value | Line |
|------|-------|------|
| `DISALLOWED_TEMPLATE_ARGS` | `[]` | 8 |

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

**Generated:** 2026-03-27 12:37:25
**Component:** mailers
**API Coverage:** 100.0%
**Total APIs:** 60