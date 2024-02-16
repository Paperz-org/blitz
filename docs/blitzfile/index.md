!!! warning

    **Please, keep in mind that the Blitz is still in development and may change in the future. We are open to suggestions and contributions.**

The Blitz file is the configuration file used by Blitz to generate the API. It is a simple YAML or JSON file that contains the general configuration of the API and the database models.

> We are building the Blitz File in a way that it is easy to read and understand with every feature needed to build a complete basic API.

## Blitz File Structure

The Blitz file is composed of two main sections: [`config`](#config) and [`resources`](#resources).

### Config

The config section contains the general configuration of the API. It is built as below:

=== "Yaml"

    ```yaml
    config:
      name: Hello world
      description: Here is a simple blitz configuration file.
      version: 0.1.0
    ```

=== "Json"

    ```json
    "config": {
        "name": "Hello world",
        "description": "Here is a simple blitz configuration file.",
        "version": "0.1.0"
    }
    ```

> _Pretty easy right ?_

### Resources

The `resources` section contains the structure of the data you want to manipulate in your Blitz app. It's a bit more complex than the config section but still easy to understand.

!!! note

    We are not talking about `database` or `models` here because Blitz is an abstraction of your data model and things that are represented in your Blitz file as a `resource` may be represented differently in your database.

The resources section is built as below:

=== "Yaml"

    ```yaml
    resources:
    - name: TodoList
      fields:
    - name: Todo
      fields:
    ```

=== "Json"

    ```json
    "models": [
        {
            "name": "TodoList",
            "fields": {}
        },
        {
            "name": "Todo",
            "fields": {}
        }
    ]
    ```

Each model is constructed with a `name` and a `fields` section. The `name` is the name of the model and the `fields` section contains the fields of the model.

> _Still pretty easy right ?_

---

#### Fields

A field can be constructed in 2 way, the **explicit** way and the **shortcut** way.

You can use both way in the same Blitz file because as the name says, the shortcut way is just a shortcut to the explicit way.

Here is an example of a working Blitz file:

=== "Yaml"

    ```yaml
    resources:
    - name: TodoList
      fields:
        owner!: str
        description: str
    - name: Todo
      fields:
        due_date: str
        todo_list_id: TodoList.id
        todo_list: TodoList
    ```

=== "Json"

    ```json
    "models": [
        {
            "name": "TodoList",
            "fields": {
                "owner!": "str",
                "description": "str"
            }
        },
        {
            "name": "Todo",
            "fields": {
                "due_date": "str",
                "todo_list_id": "TodoList.id",
                "todo_list": "TodoList"
            }
        }
    ]
    ```

=== "Yaml (explicit)"

    ```yaml
    resources:
    - name: TodoList
      fields:
        owner:
          type: str
          unique: true
        description:
          type: str
    - name: Todo
      fields:
        due_date:
          type: str
        todo_list_id:
          type: foreign_key
          relationship: TodoList.id
        todo_list:
          type: relationship
          relationship: TodoList
    ```

=== "Json (explicit)"

    ```json
    "models": [
        {
            "name": "TodoList",
            "fields": {
                "owner": {
                    "type": "str",
                    "unique": true
                },
                "description": {
                    "type": "str"
                }
            }
        },
        {
            "name": "Todo",
            "fields": {
                "due_date": {
                    "type": "str"
                },
                "todo_list_id": {
                    "type": "foreign_key",
                    "foreign_key": "TodoList.id"
                },
                "todo_list": {
                    "type": "relationship",
                    "relationship": "TodoList"
                }
            }
        }
    ]
    ```

> _You can try it in the [Blitz Playground](#)_ !

!!! note

    We will maintain the 4 ways of writing fields in the Blitz file because we think that the explicit way is more readable and the shortcut way is more convenient. We are also about to implement in the Blitz dashboard a way to switch between the 4 ways really easily.

Every field is constructed at least with a `name` and a `type`.
