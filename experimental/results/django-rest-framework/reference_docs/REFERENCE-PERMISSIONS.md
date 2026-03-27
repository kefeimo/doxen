# permissions - API Reference

**Component Type:** python_module
**Language:** python
**Path:** `rest_framework/permissions.py`
**API Coverage:** 23.9%
---

## Overview

This component contains **15 classes**, **0 functions**, and **31 methods**.

### Source Files

- [`permissions.py`](rest_framework/permissions.py) (entry point)

---

## API Reference

### Classes

#### `OperationHolderMixin`

*No description available.*


**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L11)



##### Methods

<details>
<summary><code>__and__(other)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L12)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `other` | *any* | — | — |


</details>

<details>
<summary><code>__or__(other)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L15)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `other` | *any* | — | — |


</details>

<details>
<summary><code>__rand__(other)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L18)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `other` | *any* | — | — |


</details>

<details>
<summary><code>__ror__(other)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L21)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `other` | *any* | — | — |


</details>

<details>
<summary><code>__invert__()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L24)



</details>


---

#### `SingleOperandHolder`

*No description available.*

**Inherits from:** OperationHolderMixin

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L28)



##### Methods

<details>
<summary><code>__init__(operator_class, op1_class)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L29)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `operator_class` | *any* | — | — |
| `op1_class` | *any* | — | — |


</details>

<details>
<summary><code>__call__()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L33)



</details>


---

#### `OperandHolder`

*No description available.*

**Inherits from:** OperationHolderMixin

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L38)



##### Methods

<details>
<summary><code>__init__(operator_class, op1_class, op2_class)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L39)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `operator_class` | *any* | — | — |
| `op1_class` | *any* | — | — |
| `op2_class` | *any* | — | — |


</details>

<details>
<summary><code>__call__()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L44)



</details>

<details>
<summary><code>__eq__(other)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L49)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `other` | *any* | — | — |


</details>

<details>
<summary><code>__hash__()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L57)



</details>


---

#### `AND`

*No description available.*


**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L61)



##### Methods

<details>
<summary><code>__init__(op1, op2)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L62)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `op1` | *any* | — | — |
| `op2` | *any* | — | — |


</details>

<details>
<summary><code>has_permission(request, view)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L66)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |


</details>

<details>
<summary><code>has_object_permission(request, view, obj)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L72)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |
| `obj` | *any* | — | — |


</details>


---

#### `OR`

*No description available.*


**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L79)



##### Methods

<details>
<summary><code>__init__(op1, op2)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L80)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `op1` | *any* | — | — |
| `op2` | *any* | — | — |


</details>

<details>
<summary><code>has_permission(request, view)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L84)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |


</details>

<details>
<summary><code>has_object_permission(request, view, obj)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L90)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |
| `obj` | *any* | — | — |


</details>


---

#### `NOT`

*No description available.*


**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L100)



##### Methods

<details>
<summary><code>__init__(op1)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L101)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `op1` | *any* | — | — |


</details>

<details>
<summary><code>has_permission(request, view)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L104)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |


</details>

<details>
<summary><code>has_object_permission(request, view, obj)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L107)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |
| `obj` | *any* | — | — |


</details>


---

#### `BasePermissionMetaclass`

*No description available.*

**Inherits from:** OperationHolderMixin, type

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L111)




---

#### `BasePermission`

A base class from which all permission classes should inherit.


**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L115)



##### Methods

<details>
<summary><code>has_permission(request, view)</code></summary>

Return `True` if permission is granted, `False` otherwise.

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L120)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |


</details>

<details>
<summary><code>has_object_permission(request, view, obj)</code></summary>

Return `True` if permission is granted, `False` otherwise.

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L126)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |
| `obj` | *any* | — | — |


</details>


---

#### `AllowAny`

Allow any access.
This isn't strictly required, since you could use an empty
permission_classes list, but it's useful because it makes the intention
more explicit.

**Inherits from:** BasePermission

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L133)



##### Methods

<details>
<summary><code>has_permission(request, view)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L141)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |


</details>


---

#### `IsAuthenticated`

Allows access only to authenticated users.

**Inherits from:** BasePermission

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L145)



##### Methods

<details>
<summary><code>has_permission(request, view)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L150)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |


</details>


---

#### `IsAdminUser`

Allows access only to admin users.

**Inherits from:** BasePermission

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L154)



##### Methods

<details>
<summary><code>has_permission(request, view)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L159)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |


</details>


---

#### `IsAuthenticatedOrReadOnly`

The request is authenticated as a user, or is a read-only request.

**Inherits from:** BasePermission

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L163)



##### Methods

<details>
<summary><code>has_permission(request, view)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L168)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |


</details>


---

#### `DjangoModelPermissions`

The request is authenticated using `django.contrib.auth` permissions.
See: https://docs.djangoproject.com/en/dev/topics/auth/#permissions

It ensures that the user is authenticated, and has the appropriate
`add`/`change`/`delete` permissions on the model.

This permission can only be applied against view classes that
provide a `.queryset` attribute.

**Inherits from:** BasePermission

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L176)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `perms_map` | *any* | 191 |
| `authenticated_users_only` | *any* | 201 |

##### Methods

<details>
<summary><code>get_required_permissions(method, model_cls)</code></summary>

Given a model and an HTTP method, return the list of permission
codes that the user is required to have.

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L203)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `method` | *any* | — | — |
| `model_cls` | *any* | — | — |


</details>

<details>
<summary><code>_queryset(view)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L218)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `view` | *any* | — | — |


</details>

<details>
<summary><code>has_permission(request, view)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L233)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |


</details>


---

#### `DjangoModelPermissionsOrAnonReadOnly`

Similar to DjangoModelPermissions, except that anonymous users are
allowed read-only access.

**Inherits from:** DjangoModelPermissions

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L249)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `authenticated_users_only` | *any* | 254 |


---

#### `DjangoObjectPermissions`

The request is authenticated using Django's object-level permissions.
It requires an object-permissions-enabled backend, such as Django Guardian.

It ensures that the user is authenticated, and has the appropriate
`add`/`change`/`delete` permissions on the object using .has_perms.

This permission can only be applied against view classes that
provide a `.queryset` attribute.

**Inherits from:** DjangoModelPermissions

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L257)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `perms_map` | *any* | 268 |

##### Methods

<details>
<summary><code>get_required_object_permissions(method, model_cls)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L278)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `method` | *any* | — | — |
| `model_cls` | *any* | — | — |


</details>

<details>
<summary><code>has_object_permission(request, view, obj)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/permissions.py`](rest_framework/permissions.py#L289)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | *any* | — | — |
| `view` | *any* | — | — |
| `obj` | *any* | — | — |


</details>


---



## Constants

| Name | Value | Line |
|------|-------|------|
| `SAFE_METHODS` | `('GET', 'HEAD', 'OPTIONS')` | 8 |

---

## Usage Examples

```python
# Example usage of permissions

from rest_framework.permissions import OperationHolderMixin

# Create instance
obj = OperationHolderMixin()

# Use methods
# obj.__and__(...)
```

---

## Related Components

**Category:** Unknown

*See also:*
- [Project Overview](../README.md)
- [Architecture](../ARCHITECTURE.md)

---

**Generated:** 2026-03-27 11:57:52
**Component:** permissions
**API Coverage:** 23.9%
**Total APIs:** 46