# views - API Reference

**Component Type:** python_module
**Language:** python
**Path:** `rest_framework/views.py`
**API Coverage:** 89.5%
---

## Overview

This component contains **1 class**, **4 functions**, and **33 methods**.

### Source Files

- [`views.py`](rest_framework/views.py) (entry point)

---

## API Reference

### Classes

#### `APIView`

*No description available.*

**Inherits from:** View

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L105)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `renderer_classes` | *any* | 108 |
| `parser_classes` | *any* | 109 |
| `authentication_classes` | *any* | 110 |
| `throttle_classes` | *any* | 111 |
| `permission_classes` | *any* | 112 |
| `content_negotiation_class` | *any* | 113 |
| `metadata_class` | *any* | 114 |
| `versioning_class` | *any* | 115 |
| `settings` | *any* | 118 |
| `schema` | *any* | 120 |

##### Methods

<details>
<summary><code>as_view()</code> [classmethod]</summary>

Store the original class on the view function.

This allows us to discover information about the view when we do URL
reverse lookups.  Used for breadcrumb generation.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L123)



</details>

<details>
<summary><code>allowed_methods()</code> [property]</summary>

Wrap Django's private `_allowed_methods` interface in a public property.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L153)



</details>

<details>
<summary><code>default_response_headers()</code> [property]</summary>

*No description available.*

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L160)



</details>

<details>
<summary><code>http_method_not_allowed(request)</code></summary>

If `request.method` does not correspond to a handler method,
determine what kind of exception to raise.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L168)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>permission_denied(request, message, code)</code></summary>

If request is not permitted, determine what kind of exception to raise.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L175)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `message` | *any* | — | — |
| `code` | *any* | — | — |


</details>

<details>
<summary><code>throttled(request, wait)</code></summary>

If request is throttled, determine what kind of exception to raise.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L183)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `wait` | *any* | — | — |


</details>

<details>
<summary><code>get_authenticate_header(request)</code></summary>

If a request is unauthenticated, determine the WWW-Authenticate
header to use for 401 responses, if any.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L189)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>get_parser_context(http_request)</code></summary>

Returns a dict that is passed through to Parser.parse(),
as the `parser_context` keyword argument.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L198)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `http_request` | *any* | — | — |


</details>

<details>
<summary><code>get_renderer_context()</code></summary>

Returns a dict that is passed through to Renderer.render(),
as the `renderer_context` keyword argument.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L211)



</details>

<details>
<summary><code>get_exception_handler_context()</code></summary>

Returns a dict that is passed through to EXCEPTION_HANDLER,
as the `context` argument.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L225)



</details>

<details>
<summary><code>get_view_name()</code></summary>

Return the view name, as used in OPTIONS responses and in the
browsable API.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L237)



</details>

<details>
<summary><code>get_view_description(html = False)</code></summary>

Return some descriptive text for the view, as used in OPTIONS responses
and in the browsable API.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L245)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `html` | *any* | `False` | — |


</details>

<details>
<summary><code>get_format_suffix()</code></summary>

Determine if the request includes a '.json' style format suffix

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L255)



</details>

<details>
<summary><code>get_renderers()</code></summary>

Instantiates and returns the list of renderers that this view can use.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L262)



</details>

<details>
<summary><code>get_parsers()</code></summary>

Instantiates and returns the list of parsers that this view can use.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L268)



</details>

<details>
<summary><code>get_authenticators()</code></summary>

Instantiates and returns the list of authenticators that this view can use.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L274)



</details>

<details>
<summary><code>get_permissions()</code></summary>

Instantiates and returns the list of permissions that this view requires.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L280)



</details>

<details>
<summary><code>get_throttles()</code></summary>

Instantiates and returns the list of throttles that this view uses.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L286)



</details>

<details>
<summary><code>get_content_negotiator()</code></summary>

Instantiate and return the content negotiation class to use.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L292)



</details>

<details>
<summary><code>get_exception_handler()</code></summary>

Returns the exception handler that this view uses.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L300)



</details>

<details>
<summary><code>perform_content_negotiation(request, force = False)</code></summary>

Determine which renderer and media type to use render the response.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L308)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `force` | *any* | `False` | — |


</details>

<details>
<summary><code>perform_authentication(request)</code></summary>

Perform authentication on the incoming request.

Note that if you override this and simply 'pass', then authentication
will instead be performed lazily, the first time either
`request.user` or `request.auth` is accessed.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L322)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>check_permissions(request)</code></summary>

Check if the request should be permitted.
Raises an appropriate exception if the request is not permitted.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L332)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>check_object_permissions(request, obj)</code></summary>

Check if the request should be permitted for a given object.
Raises an appropriate exception if the request is not permitted.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L345)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `obj` | *any* | — | — |


</details>

<details>
<summary><code>check_throttles(request)</code></summary>

Check if request should be throttled.
Raises an appropriate exception if the request is throttled.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L358)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>determine_version(request)</code></summary>

If versioning is being used, then determine any API version for the
incoming request. Returns a two-tuple of (version, versioning_scheme)

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L379)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>initialize_request(request)</code></summary>

Returns the initial request object.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L391)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>initial(request)</code></summary>

Runs anything that needs to occur prior to calling the method handler.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L405)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>finalize_response(request, response)</code></summary>

Returns the final response object.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L424)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `response` | *any* | — | — |


</details>

<details>
<summary><code>handle_exception(exc)</code></summary>

Handle any exception that occurs, by returning an appropriate response,
or re-raising the error.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L454)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `exc` | *any* | — | — |


</details>

<details>
<summary><code>raise_uncaught_exception(exc)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L480)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `exc` | *any* | — | — |


</details>

<details>
<summary><code>dispatch(request)</code></summary>

`.dispatch()` is pretty much the same as Django's regular dispatch,
but with extra hooks for startup, finalize, and exception handling.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L491)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>

<details>
<summary><code>options(request)</code></summary>

Handler method for HTTP 'OPTIONS' request.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L520)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>


---


### Functions

#### `get_view_name(view)`

Given a view instance, return a textual name to represent the view.
This name is used in the browsable API, and in OPTIONS responses.

This function is the default for the `VIEW_NAME_FUNCTION` setting.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L23)


**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `view` | *any* | — | — |


---

#### `get_view_description(view, html = False)`

Given a view instance, return a textual description to represent the view.
This name is used in the browsable API, and in OPTIONS responses.

This function is the default for the `VIEW_DESCRIPTION_FUNCTION` setting.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L48)


**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `view` | *any* | — | — |
| `html` | *any* | `False` | — |


---

#### `set_rollback()`

*No description available.*

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L66)




---

#### `exception_handler(exc, context)`

Returns the response that should be used for any given exception.

By default we handle the REST framework `APIException`, and also
Django's built-in `Http404` and `PermissionDenied` exceptions.

Any unhandled exceptions may return `None`, which will cause a 500 error
to be raised.

**Defined in:** [`rest_framework/views.py`](rest_framework/views.py#L72)


**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `exc` | *any* | — | — |
| `context` | *any* | — | — |


---



## Usage Examples

```python
# Example usage of views

from rest_framework.views import APIView

# Create instance
obj = APIView()

# Use methods
# obj.as_view(...)
```

---

## Related Components

**Category:** Api Endpoint

*See also:*
- [Project Overview](../README.md)
- [Architecture](../ARCHITECTURE.md)

---

**Generated:** 2026-03-27 11:57:52
**Component:** views
**API Coverage:** 89.5%
**Total APIs:** 38