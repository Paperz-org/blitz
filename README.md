#

![alt text](./docs/images/blitz_banner.png)
<p align="center">
  <em>⚡️ Lightspeed API builder ⚡️</em>
</p>

![app version](https://img.shields.io/badge/version-0.2.0-brightgreen)
![app license](https://img.shields.io/badge/license-MIT-brightgreen)

> [!CAUTION]
> Do not use in production, this is an alpha version.

# :link: Links 

:books: [Documentation](https://blitz.paperz.app/)

:game_die: [Live Demo](https://demo.blitz.paperz.app/)

# **What is Blitz ?**
Blitz is a tool that builds restfull APIs on the fly based on a simple and easy to maintain configuration file.

Here is an example of how simple a Blitz file is:
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
> [!NOTE]
> Also available in Json format.

# Installation

### Using [pipx](https://pipx.pypa.io/stable/installation/) (recommanded)
```bash
pipx install git+https://github.com/Paperz-org/blitz.git@v0.2.0
```

# Quickstart

## Create a demo blitz app

```console
blitz create --demo
```
![Made with VHS](https://vhs.charm.sh/vhs-1tqzLZNxe5qeNhXT26ZCt5.gif)

## Start the demo

```console
blitz start
```

![Made with VHS](https://vhs.charm.sh/vhs-2TEc58IujiV0CB1WoasT99.gif)

## Enjoy the demo

The blitz demo already includes resources to explore all the functionalities of Blitz.
You can see the Dashboard of the demo blitz app in our [Live Demo](https://demo.blitz.paperz.app/).

## Create a blitz app

```console
blitz create
```
![Made with VHS](https://vhs.charm.sh/vhs-2v3VHiIehkXeSkPzXeLch6.gif)

*And yeah, that's it.*

Just add some resources in the blitz file, and you now have a fully functional API and the corresponding database schema, along with all the modern features you can expect from a modern app like:

- **Automatic Swagger UI** for the API
- **Admin Interface**
- **Dashboard**: including GPT builder, Blitz file editor, logs ...
- **Data Validation and Error Messages** (thanks to Fastapi and SQLModel)
- **Automatic Database Migration**
- **Generated ERD Diagram**
- and more...

<p align="center">
  <em>Made with :heart: and :coffee: by <a href="https://github.com/mde-pach">mde-pach</a> and <a href="https://github.com/pbrochar">pbrochar</a></em>
</p>


