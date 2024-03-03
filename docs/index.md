#

![image info](./images/blitz_banner.png)

<p align="center">
  <em>⚡️ Lightspeed API builder ⚡️</em>
</p>

---

# **What is Blitz ?**

Blitz is a tool that build restfull API on the fly based on a simple and easy to maintain configuration file.

Here is an example of how simple a Blitz file is:

=== "Yaml"

    ```yaml
    config:
      name: Hello world
      description: Here is a simple blitz configuration file.
      version: 0.1.0
    resources:
      TodoList:
        name: str
        description: str
      Todo:
        name: str
        due_date: str
        todo_list_id: TodoList.id
        todo_list: TodoList
    ```

=== "Json"

    ```json
    {
      "config": {
        "name": "Hello world",
        "description": "Here is a simple blitz configuration file.",
        "version": "0.1.0"
      },
      "resources": {
        "TodoList": {
          "name": "str",
          "description": "str"
        },
        "Todo": {
          "name": "str",
          "due_date": "str",
          "todo_list_id": "TodoList.id",
          "todo_list": "TodoList"
        }
      }
    }
    ```

Just run:

```
blitz start your-blitz-project
```

_And yeah, that's it._

!!! note

    Assuming a `your-blitz-project` directory created using the blitz create command

---

You have now a fully functional API with two resources and the corresponding database schema with all the modern feature you can expect from a modern app like:

- Automatic Swagger UI for the API
- Data validation and error messages (thanks to [Fastapi](https://fastapi.tiangolo.com/) and [SQLModel](https://sqlmodel.tiangolo.com/))
- Automatic database migration based on the changes of your blitz file
- Generated ERD diagram
- Dashboard
- Admin
- and more...
