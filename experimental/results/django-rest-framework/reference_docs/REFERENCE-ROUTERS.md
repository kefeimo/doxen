# routers - API Reference

**Component Type:** python_module
**Language:** python
**Path:** `rest_framework/routers.py`
**API Coverage:** 60.9%
---

## Overview


This component contains **4 classes**, **2 functions**, and **17 methods**.

### Source Files

- [`routers.py`](rest_framework/routers.py) (entry point)

---

## API Reference

### Classes

#### `BaseRouter`

*No description available.*


**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L48)



##### Methods

<details>
<summary><code>__init__()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L49)



</details>

<details>
<summary><code>register(prefix, viewset, basename)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L52)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prefix` | *any* | — | — |
| `viewset` | *any* | — | — |
| `basename` | *any* | — | — |


</details>

<details>
<summary><code>is_already_registered(new_basename)</code></summary>

Check if `basename` is already registered

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L67)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `new_basename` | *any* | — | — |


</details>

<details>
<summary><code>get_default_basename(viewset)</code></summary>

If `basename` is not specified, attempt to automatically determine
it from the viewset.

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L73)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `viewset` | *any* | — | — |


</details>

<details>
<summary><code>get_urls()</code></summary>

Return a list of URL patterns, given the registered viewsets.

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L80)



</details>

<details>
<summary><code>urls()</code> [property]</summary>

*No description available.*

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L87)



</details>


---

#### `SimpleRouter`

*No description available.*

**Inherits from:** BaseRouter

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L93)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `routes` | *any* | 95 |

##### Methods

<details>
<summary><code>__init__(trailing_slash = True, use_regex_path = True)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L138)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `trailing_slash` | *any* | `True` | — |
| `use_regex_path` | *any* | `True` | — |


</details>

<details>
<summary><code>get_default_basename(viewset)</code></summary>

If `basename` is not specified, attempt to automatically determine
it from the viewset.

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L163)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `viewset` | *any* | — | — |


</details>

<details>
<summary><code>get_routes(viewset)</code></summary>

Augment `self.routes` with any dynamically generated routes.

Returns a list of the Route namedtuple.

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L176)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `viewset` | *any* | — | — |


</details>

<details>
<summary><code>_get_dynamic_route(route, action)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L212)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `route` | *any* | — | — |
| `action` | *any* | — | — |


</details>

<details>
<summary><code>get_method_map(viewset, method_map)</code></summary>

Given a viewset, and a mapping of http methods to actions,
return a new mapping which only includes any mappings that
are actually implemented by the viewset.

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L226)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `viewset` | *any* | — | — |
| `method_map` | *any* | — | — |


</details>

<details>
<summary><code>get_lookup_regex(viewset, lookup_prefix = )</code></summary>

Given a viewset, return the portion of URL regex that is used
to match against a single instance.

Note that lookup_prefix is not used directly inside REST rest_framework
itself, but is required in order to nicely support nested router
implementations, such as drf-nested-routers.

https://github.com/alanjds/drf-nested-routers

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L238)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `viewset` | *any* | — | — |
| `lookup_prefix` | *any* | `` | — |


</details>

<details>
<summary><code>get_urls()</code></summary>

Use the registered viewsets to generate a list of URL patterns.

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L266)



</details>


---

#### `APIRootView`

The default basic root view for DefaultRouter

**Inherits from:** views.APIView

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L314)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `_ignore_model_permissions` | *any* | 318 |
| `schema` | *any* | 319 |
| `api_root_dict` | *any* | 320 |

##### Methods

<details>
<summary><code>get(request)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L322)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |


</details>


---

#### `DefaultRouter`

The default router extends the SimpleRouter, but also adds in a default
API root view, and adds format suffix patterns to the URLs.

**Inherits from:** SimpleRouter

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L344)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `include_root_view` | *any* | 349 |
| `include_format_suffixes` | *any* | 350 |
| `root_view_name` | *any* | 351 |
| `default_schema_renderers` | *any* | 352 |
| `APIRootView` | *any* | 353 |
| `APISchemaView` | *any* | 354 |
| `SchemaGenerator` | *any* | 355 |

##### Methods

<details>
<summary><code>__init__()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L357)



</details>

<details>
<summary><code>get_api_root_view(api_urls)</code></summary>

Return a basic root view.

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L364)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_urls` | *any* | — | — |


</details>

<details>
<summary><code>get_urls()</code></summary>

Generate the list of URL patterns, including a default root view
for the API, and appending `.json` style format suffixes.

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L375)



</details>


---



### Functions

#### `escape_curly_brackets(url_path)`

Double brackets in regex of url_path for escape string formatting

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L34)


**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url_path` | *any* | — | — |


---

#### `flatten(list_of_lists)`

Takes an iterable of iterables, returns a single iterable containing all items

**Defined in:** [`rest_framework/routers.py`](rest_framework/routers.py#L41)


**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `list_of_lists` | *any* | — | — |


---



## Usage Examples

```python
# Example usage of routers

from rest_framework.routers import BaseRouter

# Create instance
obj = BaseRouter()

# Use methods
# obj.__init__(...)
```

---

## Related Components

**Category:** Api Endpoint

*See also:*
- [Project Overview](../README.md)
- [Architecture](../ARCHITECTURE.md)

---

**Generated:** 2026-04-01 09:03:24
**Component:** routers
**API Coverage:** 60.9%
**Total APIs:** 23