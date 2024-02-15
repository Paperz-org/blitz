#

## Resources

The `resources` section contains your Blitz resources description. It is built as below:

=== "Yaml"

    ```yaml
    resources:
    - name: Book
      fields:
    ```

=== "Json"

    ```json
    "resources": [
        {
            "name": "Book",
            "fields": {}
        }
    ]
    ```

Each resource contains at least a `name` and a `fields` section. The `name` is the name of the resource and the `fields` section contains the fields of the resource.

## Fields

!!! note
    The field section can be constructed in 2 way, the **explicit** way and the **shortcut** way. You can use both way in the same Blitz file because as the name says, the shortcut way is just a shortcut to the explicit way.

Each field must contain at least a `name` and a `type`.

The available field types are listed below:

| Type | Description | Example |
| ---- | ----------- | ------- |
| `str` | A string | `Hello world` |
| `int` | An integer | `42` |
| `float` | A float | `3.14` |
| `bool` | A boolean | `true` |
| `uuid` | A UUID | `123e4567-e89b-12d3-a456-42661417` |
| `datetime` | A datetime | `2021-01-01T00:00:00` |

=== "Yaml"
    ```yaml
    fields:
      description: str
    ```

=== "Json"
    ```json
    "fields": {
        "description": "str"
    }
    ```

=== "Yaml (explicit)"
    ```yaml
    fields:
      description:
        type: str
    ```

=== "Json (explicit)"
    ```json
    "fields": {
        "description": {
            "type": "str"
        }
    }
    ```

!!! note
    In this example, the name of the field is `description` and the type is `str`.

Let's have a look with a complete resource and then break it down:

=== "Yaml"
    ```yaml
    resources:
    - name: Book
      fields:
        title: str! # (1)!
        identifier!: uuid! # (2)!
        author: str? # (3)!
        description: # (4)!
          type: str
          default: "Here is a description"
    ```

    1. The field `title` is **required** because of the `!` modifier at the end of the field type (`str!`). See the [required field](#required-field) for more details.
    2. The field `ìdentifier` is **unique** because of the `!` modifier at the end of the field name (`identifier!`). See the [unique field](#unique-field) for more details.<br><br>
    The field `identifier` is **required** because of the `!` modifier at the end of the field type (`uuid!`). See the [required field](#required-field) for more details.
    3. The field `author` is **nullable** because of the `?` modifier at the end of the field type (`str?`). See the [nullable field](#nullable-field) for more details.
    4. The field `description` has a **default value** because of the `default` property (`default: "Here is a description"`). See the [default value](#default-value) for more details.

=== "Json"
    ```json
    "resources": [
        {
            "name": "Book",
            "fields": {
                "title": "str!", // (1)!
                "identifier!": "uuid!", // (2)!
                "author": "str?", // (3)!
                "description": { // (4)!
                    "type": "str",
                    "default": "Here is a description"
                }
            }
        }
    ]
    ```

    1. The field `title` is **required** because of the `!` modifier at the end of the field type (`str!`). See the [required field](#required-field) for more details.
    2. The field `ìdentifier` is **unique** because of the `!` modifier at the end of the field name (`identifier!`). See the [unique field](#unique-field) for more details.<br><br>
    The field `identifier` is **required** because of the `!` modifier at the end of the field type (`uuid!`). See the [required field](#required-field) for more details.
    3. The field `author` is **nullable** because of the `?` modifier at the end of the field type (`str?`). See the [nullable field](#nullable-field) for more details.
    4. The field `description` has a **default value** because of the `default` property (`"default": "Here is a description"`). See the [default value](#default-value) for more details.

=== "Yaml (explicit)"
    ```yaml
    resources:
    - name: Book
      fields:
        title: # (1)!
          type: str
          required: true
        identifier: # (2)!
          type: uuid
          unique: true
        author: # (3)!
          type: str
          nullable: true
        description: # (4)!
          type: str
          default: "Here is a description"
    ```

    1. The field `title` is **required** because of the `required` propertry (`required: true`). See the [required field](#required-field) for more details.
    2. The field `ìdentifier` is **unique** because of the `unique` property at the end of the field name (`unique: true`). See the [unique field](#unique-field) for more details.<br><br>
    The field `identifier` is **required** because of the `required` property (`required: true`). See the [required field](#required-field) for more details.
    3. The field `author` is **nullable** because of the `nullable` property (`nullable: true`). See the [nullable field](#nullable-field) for more details.
    4. The field `description` has a **default value** because of the `default` property (`default: "Here is a description"`). See the [default value](#default-value) for more details.


=== "Json (explicit)"
    ```json
    "resources": [
        {
            "name": "Book",
            "fields": {
                "title": { // (1)!
                    "type": "str",
                    "required": true
                },
                "identifier": { // (2)!
                    "type": "uuid",
                    "unique": true
                },
                "author": { // (3)!
                    "type": "str",
                    "nullable": true
                },
                "description": { // (4)!
                    "type": "str",
                    "default": "Here is a description"
                }
            }
        }
    ]
    ```

    1. The field `title` is **required** because of the `required` propertry (`"required": true`). See the [required field](#required-field) for more details.
    2. The field `ìdentifier` is **unique** because of the `unique` property at the end of the field name (`"unique": true`). See the [unique field](#unique-field) for more details.<br><br>
    The field `identifier` is **required** because of the `required` property (`"required": true`). See the [required field](#required-field) for more details.
    3. The field `author` is **nullable** because of the `nullable` property (`"nullable": true`). See the [nullable field](#nullable-field) for more details.
    4. The field `description` has a **default value** because of the `default` property (`"default": "Here is a description"`). See the [default value](#default-value) for more details.

        



### Unique field

You can specify if a field is **unique** by adding a `!` at the end of the field name or by setting the `unique` property to `true`.

=== "Yaml"
    ```yaml
    fields:
      identifier!: uuid
    ```

=== "Json"
    ```json
    "fields": {
        "identifier!": "uuid"
    }
    ```

=== "Yaml (explicit)"
    ```yaml
    fields:
      identifier:
        type: uuid
        unique: true
    ```

=== "Json (explicit)"
    ```json
    "fields": {
        "identifier": {
            "type": "uuid",
            "unique": true
        }
    }
    ```

### Nullable field

You can specify if a field is **nullable** by adding a `?` at the end of the field type or by setting the `nullable` property to `true`.

=== "Yaml"
    ```yaml
    fields:
      author: str?
    ```
=== "Json"
    ```json
    "fields": {
        "author": "str?"
    }
    ```
=== "Yaml (explicit)"
    ```yaml
    fields:
      author:
        type: str
        nullable: true
    ```
=== "Json (explicit)"
    ```json
    "fields": {
        "author": {
            "type": "str",
            "nullable": true
        }
    }
    ```

The default value will be set to `null` if the field is nullable. If you want to specify another default value, you can use the [`default`](#default) property.

### Required field

You can specify if a field is **required** by adding a `!` at the end of the field type or by setting the `required` property to `true`.

=== "Yaml"
    ```yaml
    fields:
      title: str!
    ```
=== "Json"
    ```json
    "fields": {
        "title": "str!"
    }
    ```
=== "Yaml (explicit)"
    ```yaml
    fields:
      title:
        type: str
        required: true
    ```
=== "Json (explicit)"
    ```json
    "fields": {
        "title": {
            "type": "str",
            "required": true
        }
    }
    ```

### Default value

??? example "No shortcut yet"
    There is no shortcut yet for the `default`property.

You can specify a **default value** for a field by setting the `default` property to the value you want.

=== "Yaml"
    ```yaml
    fields:
      description:
        type: str
        default: "Here is a description"
    ```

=== "Json"
    ```json
    "fields": {
        "description": {
            "type": "str",
            "default": "Here is a description"
        }
    }
    ```