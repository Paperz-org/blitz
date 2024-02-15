#

![alt text](./docs/images/blitz_banner.png)
<p align="center">
  <em>⚡️ Lightspeed API builder ⚡️</em>
</p>

![app version](https://img.shields.io/badge/version-0.1.0-brightgreen)
![app license](https://img.shields.io/badge/license-MIT-brightgreen)

> [!CAUTION]
> Do not use in production, this is an alpha version.

Full [Documentation](https://paperz-org.github.io/blitz/) here.

# **What is Blitz ?**
Blitz is a tool that build restfull API on the fly based on a simple and easy to maintain configuration file.

Here is an example of how simple a Blitz file is:
  ```yaml
  config:
    name: Hello world
    description: Here is a simple blitz configuration file.
    version: 0.1.0
  models:
  - name: TodoList
    fields:
      name: str
      description: str
  - name: Todo
    fields:
      name: str
      due_date: str
      todo_list_id: TodoList.id
  ```
> [!NOTE]
> Also available in Json format.

# Quickstart

## Installation

### Using [pipx](https://pipx.pypa.io/stable/installation/) (recommanded)
```bash
pipx install git+ssh://git@github.com/Paperz-org/blitz.git
```

### Using pip
```bash
pip install --user git+ssh://git@github.com/Paperz-org/blitz.git
```

## Create a blitz app

```console
blitz create your-blitz-app
```

## Start your blitz app

```console
blitz start your-blitz-app
```

*And yeah, that's it.*

Just add some resources in the blitz file, and you have now a fully functional API with models and the corresponding database schema with all the modern feature you can expect from a modern app like:

- Automatic Swagger UI for the API
- Admin
- Dashboard
- Data validation and error messages (thanks to Fastapi and SQLModel)
- Automatic database migration based on the changes of your blitz file
- Generated ERD diagram
- and more...

<p align="center">
  <em>Made with :heart: and :coffee: by <a href="https://github.com/mde-pach">mde-pach</a> and <a href="https://github.com/pbrochar">pbrochar</a></em>
</p>


