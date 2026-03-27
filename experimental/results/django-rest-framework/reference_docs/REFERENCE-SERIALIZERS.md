# serializers - API Reference

**Component Type:** python_module
**Language:** python
**Path:** `rest_framework/serializers.py`
**API Coverage:** 51.2%
---

## Overview

This component contains **10 classes**, **2 functions**, and **72 methods**.

### Source Files

- [`serializers.py`](rest_framework/serializers.py) (entry point)

---

## API Reference

### Classes

#### `BaseSerializer`

The BaseSerializer class provides a minimal class which may be used
for writing custom serializer implementations.

Note that we strongly restrict the ordering of operations/properties
that may be used on the serializer in order to enforce correct usage.

In particular, if a `data=` argument is passed then:

.is_valid() - Available.
.initial_data - Available.
.validated_data - Only available after calling `is_valid()`
.errors - Only available after calling `is_valid()`
.data - Only available after calling `is_valid()`

If a `data=` argument is not passed then:

.is_valid() - Not available.
.initial_data - Not available.
.validated_data - Not available.
.errors - Not available.
.data - Available.

**Inherits from:** Field

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L89)



##### Methods

<details>
<summary><code>__init__(instance, data = empty)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L114)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `instance` | *any* | — | — |
| `data` | *any* | `empty` | — |


</details>

<details>
<summary><code>__new__()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L123)



</details>

<details>
<summary><code>__class_getitem__()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L131)



</details>

<details>
<summary><code>many_init()</code> [classmethod]</summary>

This method implements the creation of a `ListSerializer` parent
class when `many=True` is used. You can customize it if you need to
control which keyword arguments are passed to the parent, and
which are passed to the child.

Note that we're over-cautious in passing most arguments to both parent
and child classes in order to try to cover the general case. If you're
overriding this method you'll probably want something much simpler, eg:

@classmethod
def many_init(cls, *args, **kwargs):
    kwargs['child'] = cls()
    return CustomListSerializer(*args, **kwargs)

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L135)



</details>

<details>
<summary><code>to_internal_value(data)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L165)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | *any* | — | — |


</details>

<details>
<summary><code>to_representation(instance)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L168)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `instance` | *any* | — | — |


</details>

<details>
<summary><code>update(instance, validated_data)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L171)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `instance` | *any* | — | — |
| `validated_data` | *any* | — | — |


</details>

<details>
<summary><code>create(validated_data)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L174)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `validated_data` | *any* | — | — |


</details>

<details>
<summary><code>save()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L177)



</details>

<details>
<summary><code>is_valid()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L217)



</details>

<details>
<summary><code>data()</code> [property]</summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L238)



</details>

<details>
<summary><code>errors()</code> [property]</summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L259)



</details>

<details>
<summary><code>validated_data()</code> [property]</summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L266)



</details>


---

#### `SerializerMetaclass`

This metaclass sets a dictionary named `_declared_fields` on the class.

Any instances of `Field` included as attributes on either the class
or on any of its superclasses will be include in the
`_declared_fields` dictionary.

**Inherits from:** type

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L276)



##### Methods

<details>
<summary><code>_get_declared_fields(bases, attrs)</code> [classmethod]</summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L286)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `bases` | *any* | — | — |
| `attrs` | *any* | — | — |


</details>

<details>
<summary><code>__new__(name, bases, attrs)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L309)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | *any* | — | — |
| `bases` | *any* | — | — |
| `attrs` | *any* | — | — |


</details>


---

#### `Serializer`

*No description available.*

**Inherits from:** BaseSerializer

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L352)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `default_error_messages` | *any* | 353 |

##### Methods

<details>
<summary><code>set_value(dictionary, keys, value)</code></summary>

Similar to Python's built in `dictionary[key] = value`,
but takes a list of nested keys instead of a single key.

set_value({'a': 1}, [], {'b': 2}) -> {'a': 1, 'b': 2}
set_value({'a': 1}, ['x'], 2) -> {'a': 1, 'x': 2}
set_value({'a': 1}, ['x', 'y'], 2) -> {'a': 1, 'x': {'y': 2}}

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L357)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dictionary` | *any* | — | — |
| `keys` | *any* | — | — |
| `value` | *any* | — | — |


</details>

<details>
<summary><code>fields()</code> [cached_property]</summary>

A dictionary of {field_name: field_instance}.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L378)



</details>

<details>
<summary><code>_writable_fields()</code> [property]</summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L391)



</details>

<details>
<summary><code>_readable_fields()</code> [property]</summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L397)



</details>

<details>
<summary><code>get_fields()</code></summary>

Returns a dictionary of {field_name: field_instance}.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L402)



</details>

<details>
<summary><code>get_validators()</code></summary>

Returns a list of validator callables.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L411)



</details>

<details>
<summary><code>get_initial()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L420)



</details>

<details>
<summary><code>get_value(dictionary)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L439)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dictionary` | *any* | — | — |


</details>

<details>
<summary><code>run_validation(data = empty)</code></summary>

We override the default `run_validation`, because the validation
performed by validators and the `.validate()` method should
be coerced into an error dictionary with a 'non_fields_error' key.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L446)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | *any* | `empty` | — |


</details>

<details>
<summary><code>_read_only_defaults()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L466)



</details>

<details>
<summary><code>run_validators(value)</code></summary>

Add read_only fields with defaults to value before running validators.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L482)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | *any* | — | — |


</details>

<details>
<summary><code>to_internal_value(data)</code></summary>

Dict of native values <- Dict of primitive datatypes.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L493)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | *any* | — | — |


</details>

<details>
<summary><code>to_representation(instance)</code></summary>

Object instance -> Dict of primitive datatypes.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L530)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `instance` | *any* | — | — |


</details>

<details>
<summary><code>validate(attrs)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L556)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `attrs` | *any* | — | — |


</details>

<details>
<summary><code>__repr__()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L559)



</details>

<details>
<summary><code>__iter__()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L566)



</details>

<details>
<summary><code>__getitem__(key)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L570)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `key` | *any* | — | — |


</details>

<details>
<summary><code>data()</code> [property]</summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L584)



</details>

<details>
<summary><code>errors()</code> [property]</summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L589)



</details>


---

#### `ListSerializer`

*No description available.*

**Inherits from:** BaseSerializer

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L602)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `child` | *any* | 603 |
| `many` | *any* | 604 |
| `default_error_messages` | *any* | 606 |

##### Methods

<details>
<summary><code>__init__()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L613)



</details>

<details>
<summary><code>get_initial()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L623)



</details>

<details>
<summary><code>get_value(dictionary)</code></summary>

Given the input dictionary, return the field value.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L628)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dictionary` | *any* | — | — |


</details>

<details>
<summary><code>run_validation(data = empty)</code></summary>

We override the default `run_validation`, because the validation
performed by validators and the `.validate()` method should
be coerced into an error dictionary with a 'non_fields_error' key.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L638)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | *any* | `empty` | — |


</details>

<details>
<summary><code>run_child_validation(data)</code></summary>

Run validation on child serializer.
You may need to override this method to support multiple updates. For example:

self.child.instance = self.instance.get(pk=data['id'])
self.child.initial_data = data
return super().run_child_validation(data)

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L658)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | *any* | — | — |


</details>

<details>
<summary><code>to_internal_value(data)</code></summary>

List of dicts of native values <- List of dicts of primitive datatypes.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L669)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | *any* | — | — |


</details>

<details>
<summary><code>to_representation(data)</code></summary>

List of object instances -> List of dicts of primitive datatypes.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L719)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | *any* | — | — |


</details>

<details>
<summary><code>validate(attrs)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L731)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `attrs` | *any* | — | — |


</details>

<details>
<summary><code>update(instance, validated_data)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L734)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `instance` | *any* | — | — |
| `validated_data` | *any* | — | — |


</details>

<details>
<summary><code>create(validated_data)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L743)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `validated_data` | *any* | — | — |


</details>

<details>
<summary><code>save()</code></summary>

Save and return a list of object instances.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L748)



</details>

<details>
<summary><code>is_valid()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L779)



</details>

<details>
<summary><code>__repr__()</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L801)



</details>

<details>
<summary><code>data()</code> [property]</summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L808)



</details>

<details>
<summary><code>errors()</code> [property]</summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L813)



</details>


---

#### `ModelSerializer`

A `ModelSerializer` is just a regular `Serializer`, except that:

* A set of default fields are automatically populated.
* A set of default validators are automatically populated.
* Default `.create()` and `.update()` implementations are provided.

The process of automatically determining a set of serializer fields
based on the model fields is reasonably complex, but you almost certainly
don't need to dig into the implementation.

If the `ModelSerializer` class *doesn't* generate the set of fields that
you need you should either declare the extra/differing fields explicitly on
the serializer class, or simply use a `Serializer` class.

**Inherits from:** Serializer

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L910)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `serializer_field_mapping` | *any* | 926 |
| `serializer_related_field` | *any* | 961 |
| `serializer_related_to_field` | *any* | 962 |
| `serializer_url_field` | *any* | 963 |
| `serializer_choice_field` | *any* | 964 |
| `url_field_name` | *any* | 973 |

##### Methods

<details>
<summary><code>create(validated_data)</code></summary>

We have a bit of extra checking around this in order to provide
descriptive messages when something goes wrong, but this method is
essentially just:

    return ExampleModel.objects.create(**validated_data)

If there are many to many fields present on the instance then they
cannot be set until the model is instantiated, in which case the
implementation is like so:

    example_relationship = validated_data.pop('example_relationship')
    instance = ExampleModel.objects.create(**validated_data)
    instance.example_relationship = example_relationship
    return instance

The default implementation also does not handle nested relationships.
If you want to support writable nested relationships you'll need
to write an explicit `.create()` method.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L976)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `validated_data` | *any* | — | — |


</details>

<details>
<summary><code>update(instance, validated_data)</code></summary>

*No description available.*

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1040)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `instance` | *any* | — | — |
| `validated_data` | *any* | — | — |


</details>

<details>
<summary><code>get_fields()</code></summary>

Return the dict of field names -> field instances that should be
used for `self.fields` when instantiating the serializer.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1068)



</details>

<details>
<summary><code>get_field_names(declared_fields, info)</code></summary>

Returns the list of all field names that should be created when
instantiating this serializer class. This is based on the default
set of fields, but also takes into account the `Meta.fields` or
`Meta.exclude` options if they have been specified.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1151)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `declared_fields` | *any* | — | — |
| `info` | *any* | — | — |


</details>

<details>
<summary><code>get_default_field_names(declared_fields, model_info)</code></summary>

Return the default list of field names that will be used if the
`Meta.fields` option is not specified.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1243)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `declared_fields` | *any* | — | — |
| `model_info` | *any* | — | — |


</details>

<details>
<summary><code>build_field(field_name, info, model_class, nested_depth)</code></summary>

Return a two tuple of (cls, kwargs) to build a serializer field with.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1257)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field_name` | *any* | — | — |
| `info` | *any* | — | — |
| `model_class` | *any* | — | — |
| `nested_depth` | *any* | — | — |


</details>

<details>
<summary><code>build_standard_field(field_name, model_field)</code></summary>

Create regular model fields.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1280)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field_name` | *any* | — | — |
| `model_field` | *any* | — | — |


</details>

<details>
<summary><code>build_relational_field(field_name, relation_info)</code></summary>

Create fields for forward and reverse relationships.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1341)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field_name` | *any* | — | — |
| `relation_info` | *any* | — | — |


</details>

<details>
<summary><code>build_nested_field(field_name, relation_info, nested_depth)</code></summary>

Create nested fields for forward and reverse relationships.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1359)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field_name` | *any* | — | — |
| `relation_info` | *any* | — | — |
| `nested_depth` | *any* | — | — |


</details>

<details>
<summary><code>build_property_field(field_name, model_class)</code></summary>

Create a read only field for model methods and properties.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1374)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field_name` | *any* | — | — |
| `model_class` | *any* | — | — |


</details>

<details>
<summary><code>build_url_field(field_name, model_class)</code></summary>

Create a field representing the object's own URL.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1383)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field_name` | *any* | — | — |
| `model_class` | *any* | — | — |


</details>

<details>
<summary><code>build_unknown_field(field_name, model_class)</code></summary>

Raise an error on any unknown fields.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1392)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field_name` | *any* | — | — |
| `model_class` | *any* | — | — |


</details>

<details>
<summary><code>include_extra_kwargs(kwargs, extra_kwargs)</code></summary>

Include any 'extra_kwargs' that have been included for this field,
possibly removing any incompatible existing keyword arguments.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1401)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `kwargs` | *any* | — | — |
| `extra_kwargs` | *any* | — | — |


</details>

<details>
<summary><code>get_extra_kwargs()</code></summary>

Return a dictionary mapping field names to a dictionary of
additional keyword arguments.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1425)



</details>

<details>
<summary><code>get_unique_together_constraints(model)</code></summary>

Returns iterator of (fields, queryset, condition_fields, condition),
each entry describes an unique together constraint on `fields` in `queryset`
with respect of constraint's `condition`.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1455)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | *any* | — | — |


</details>

<details>
<summary><code>get_uniqueness_extra_kwargs(field_names, declared_fields, extra_kwargs)</code></summary>

Return any additional field options that need to be included as a
result of uniqueness constraints on the model. This is returned as
a two-tuple of:

('dict of updated extra kwargs', 'mapping of hidden fields')

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1472)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field_names` | *any* | — | — |
| `declared_fields` | *any* | — | — |
| `extra_kwargs` | *any* | — | — |


</details>

<details>
<summary><code>_get_model_fields(field_names, declared_fields, extra_kwargs)</code></summary>

Returns all the model fields that are being mapped to by fields
on the serializer class.
Returned as a dict of 'model field name' -> 'model field'.
Used internally by `get_uniqueness_field_options`.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1549)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field_names` | *any* | — | — |
| `declared_fields` | *any* | — | — |
| `extra_kwargs` | *any* | — | — |


</details>

<details>
<summary><code>get_validators()</code></summary>

Determine the set of validators to use when instantiating serializer.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1584)



</details>

<details>
<summary><code>_get_constraint_violation_error_message(constraint)</code></summary>

Returns the violation error message for the UniqueConstraint,
or None if the message is the default.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1599)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `constraint` | *any* | — | — |


</details>

<details>
<summary><code>get_unique_together_validators()</code></summary>

Determine a default set of validators for any unique_together constraints.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1610)



</details>

<details>
<summary><code>get_unique_for_date_validators()</code></summary>

Determine a default set of validators for the following constraints:

* unique_for_date
* unique_for_month
* unique_for_year

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1684)



</details>


---

#### `HyperlinkedModelSerializer`

A type of `ModelSerializer` that uses hyperlinked relationships instead
of primary key relationships. Specifically:

* A 'url' field is included instead of the 'id' field.
* Relationships to other instances are hyperlinks, instead of primary keys.

**Inherits from:** ModelSerializer

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1726)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `serializer_related_field` | *any* | 1734 |

##### Methods

<details>
<summary><code>get_default_field_names(declared_fields, model_info)</code></summary>

Return the default list of field names that will be used if the
`Meta.fields` option is not specified.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1736)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `declared_fields` | *any* | — | — |
| `model_info` | *any* | — | — |


</details>

<details>
<summary><code>build_nested_field(field_name, relation_info, nested_depth)</code></summary>

Create nested fields for forward and reverse relationships.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1748)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field_name` | *any* | — | — |
| `relation_info` | *any* | — | — |
| `nested_depth` | *any* | — | — |


</details>


---

#### `NestedSerializer`

*No description available.*

**Inherits from:** ModelSerializer

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1363)




---

#### `NestedSerializer`

*No description available.*

**Inherits from:** HyperlinkedModelSerializer

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1752)




---

#### `Meta`

*No description available.*


**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1364)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `model` | *any* | 1365 |
| `depth` | *any* | 1366 |
| `fields` | *any* | 1367 |


---

#### `Meta`

*No description available.*


**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L1753)


##### Class Attributes

| Attribute | Type | Line |
|-----------|------|------|
| `model` | *any* | 1754 |
| `depth` | *any* | 1755 |
| `fields` | *any* | 1756 |


---


### Functions

#### `as_serializer_error(exc)`

Coerce validation exceptions into a standardized serialized error format.

This function normalizes both Django's `ValidationError` and REST
framework's `ValidationError` into a dictionary structure compatible
with serializer `.errors`, ensuring all values are represented as
lists of error details.

The returned structure conforms to the serializer error contract:
- Field-specific errors are returned as '{field-name: [errors]}'
- Non-field errors are returned under the 'NON_FIELD_ERRORS_KEY'

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L314)


**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `exc` | *any* | — | — |


---

#### `raise_errors_on_nested_writes(method_name, serializer, validated_data)`

Enforce explicit handling of writable nested and dotted-source fields.

This helper raises clear and actionable errors when a serializer attempts
to perform writable nested updates or creates using the default
`ModelSerializer` behavior.

Writable nested relationships and dotted-source fields are intentionally
unsupported by default due to ambiguous persistence semantics. Developers
must either:
- Override the `.create()` / `.update()` methods explicitly, or
- Mark nested serializers as `read_only=True`

This check is invoked internally by default `ModelSerializer.create()`
and `ModelSerializer.update()` implementations.

Eg. Suppose we have a `UserSerializer` with a nested profile. How should
we handle the case of an update, where the `profile` relationship does
not exist? Any of the following might be valid:
* Raise an application error.
* Silently ignore the nested part of the update.
* Automatically create a profile instance.

**Defined in:** [`rest_framework/serializers.py`](rest_framework/serializers.py#L828)


**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `method_name` | *any* | — | — |
| `serializer` | *any* | — | — |
| `validated_data` | *any* | — | — |


---


## Constants

| Name | Value | Line |
|------|-------|------|
| `LIST_SERIALIZER_KWARGS` | `('read_only', 'write_only', 'required', 'default', 'initial', 'source', 'label', 'help_text', 'style', 'error_messages', 'allow_empty', 'instance', 'data', 'partial', 'context', 'allow_null', 'max_length', 'min_length')` | 75 |
| `LIST_SERIALIZER_KWARGS_REMOVE` | `('allow_empty', 'min_length', 'max_length')` | 81 |
| `ALL_FIELDS` | `__all__` | 83 |

---

## Usage Examples

```python
# Example usage of serializers

from rest_framework.serializers import BaseSerializer

# Create instance
obj = BaseSerializer()

# Use methods
# obj.__init__(...)
```

---

## Related Components

**Category:** Unknown

*See also:*
- [Project Overview](../README.md)
- [Architecture](../ARCHITECTURE.md)

---

**Generated:** 2026-03-27 11:57:52
**Component:** serializers
**API Coverage:** 51.2%
**Total APIs:** 84