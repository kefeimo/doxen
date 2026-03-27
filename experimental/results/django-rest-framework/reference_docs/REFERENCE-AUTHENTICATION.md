# authentication - API Reference

**Component Type:** python_module
**Language:** python
**Path:** `rest_framework/authentication.py`
**API Coverage:** 60.0%
---

## Overview

This component contains **6 classes**, **1 function**, and **13 methods**.

### Source Files

- [`authentication.py`](rest_framework/authentication.py) (entry point)

---

## API Reference

### Classes

#### `CSRFCheck`

*No description available.*

**Inherits from:** CsrfViewMiddleware

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L27)



##### Methods

<details>
<summary><code>_reject(request, reason)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L28)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `reason` | *any* | — | — |


</details>


---

#### `BaseAuthentication`

All authentication classes should extend BaseAuthentication.


**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L33)



##### Methods

<details>
<summary><code>authenticate(request)</code></summary>

Authenticate the request and return a two-tuple of (user, token).

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L38)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>authenticate_header(request)</code></summary>

Return a string to be used as the value of the `WWW-Authenticate`
header in a `401 Unauthenticated` response, or `None` if the
authentication scheme should return `403 Permission Denied` responses.

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L44)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>


---

#### `BasicAuthentication`

HTTP Basic authentication against username/password.

**Inherits from:** BaseAuthentication

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L53)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `www_authenticate_realm` | *any* | 57 |

##### Methods

<details>
<summary><code>authenticate(request)</code></summary>

Returns a `User` if a correct username and password have been supplied
using HTTP Basic authentication.  Otherwise returns `None`.

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L59)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>authenticate_credentials(userid, password, request)</code></summary>

Authenticate the userid and password against username and password
with optional request for context.

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L89)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `userid` | *any* | — | — |
| `password` | *any* | — | — |
| `request` | *any* | — | — |


</details>

<details>
<summary><code>authenticate_header(request)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L108)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>


---

#### `SessionAuthentication`

Use Django's session framework for authentication.

**Inherits from:** BaseAuthentication

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L112)



##### Methods

<details>
<summary><code>authenticate(request)</code></summary>

Returns a `User` if the request session currently has a logged in user.
Otherwise returns `None`.

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L117)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>enforce_csrf(request)</code></summary>

Enforce CSRF validation for session based authentication.

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L135)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>


---

#### `TokenAuthentication`

Simple token based authentication.

Clients should authenticate by passing the token key in the "Authorization"
HTTP header, prepended with the string "Token ".  For example:

    Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a

**Inherits from:** BaseAuthentication

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L151)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `keyword` | *any* | 161 |
| `model` | *any* | 162 |

##### Methods

<details>
<summary><code>get_model()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L164)



</details>

<details>
<summary><code>authenticate(request)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L177)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>authenticate_credentials(key)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L198)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `key` | *any* | — | — |


</details>

<details>
<summary><code>authenticate_header(request)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L210)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>


---

#### `RemoteUserAuthentication`

REMOTE_USER authentication.

To use this, set up your web server to perform authentication, which will
set the REMOTE_USER environment variable. You will need to have
'django.contrib.auth.backends.RemoteUserBackend in your
AUTHENTICATION_BACKENDS setting

**Inherits from:** BaseAuthentication

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L214)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `header` | *any* | 227 |

##### Methods

<details>
<summary><code>authenticate(request)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L229)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>


---


### Functions

#### `get_authorization_header(request)`

Return request's 'Authorization:' header, as a bytestring.

Hide some test client ickyness where the header can be unicode.

**Defined in:** [`rest_framework/authentication.py`](rest_framework/authentication.py#L14)


**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


---



## Usage Examples

```python
# Example usage of authentication

from rest_framework.authentication import CSRFCheck

# Create instance
obj = CSRFCheck()

# Use methods
# obj._reject(...)
```

---

## Related Components

**Category:** Unknown

*See also:*
- [Project Overview](../README.md)
- [Architecture](../ARCHITECTURE.md)

---

**Generated:** 2026-03-27 11:57:52
**Component:** authentication
**API Coverage:** 60.0%
**Total APIs:** 20