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
<!-- termynal -->

<div class="termy">
```console
$ blitz create --demo

<span style="color: #af87ff; font-weight: bold;">Demo Blitz App</span> created successfully !
To start your app, you can use:
    <span style="color: #af87ff; font-weight: bold;">blitz start demo-blitz-app</span>
```
</div>

## Start the demo
```console
blitz start
```
<!-- termynal -->
<div class="termy">
```console
$ blitz start

<span style="color: yellow; font-weight: bold;">This is still an alpha. Please do not use in production.</span>
<span style="color: yellow; font-weight: bold;">Please report any issues on https://github.com/Paperz-org/blitz</span>

<span style="color: #af87ff; font-weight: bold;">Blitz app deployed.</span>
<span style="color: #af87ff; font-weight: bold;">  - Blitz UI            : <a style="cursor: pointer" href="http://0.0.0.0:8100" target="_blank" rel="noopener noreferrer">http://0.0.0.0:8100</a></span>
<span style="color: #af87ff; font-weight: bold;">  - Blitz admin         : <a style="cursor: pointer" href="http://0.0.0.0:8100/admin" target="_blank" rel="noopener noreferrer">http://0.0.0.0:8100/admin</a></span>
<span style="color: #af87ff; font-weight: bold;">  - Swagger UI          : <a style="cursor: pointer" href="http://0.0.0.0:8100/api/docs" target="_blank" rel="noopener noreferrer">http://0.0.0.0:8100/api/docs</a></span>

<span style="color: lightblue; font-weight: bold;">INFO</span>      random-blitz-app Started server process [21292026]
<span style="color: lightblue; font-weight: bold;">INFO</span>      random-blitz-app Waiting for application startup.
<span style="color: lightblue; font-weight: bold;">INFO</span>      random-blitz-app Application startup complete.
```
</div>

## Enjoy the demo

The blitz demo already includes resources to explore all the functionalities of Blitz.
You can see the Dashboard of the demo blitz app in our [Live Demo](https://demo.blitz.paperz.app/).

## Create a blitz app

```console
blitz create
```
<!-- termynal -->

<div class="termy">
```console
$ blitz create
Enter the name of your blitz app (Random Blitz App):
// My First App
Enter the description of your blitz app ():
// this is my first blitz app
Choose the format of the blitz file [json/yaml] (yaml):
// yaml

<span style="color: #af87ff; font-weight: bold;">My First App</span> created successfully !
To start your app, you can use:
    <span style="color: #af87ff; font-weight: bold;">blitz start my-first-app</span>
```
</div>

*And yeah, that's it.*

!!! tip "Want to master Blitz?"

    You can **[learn here](/blitz/blitzfile/)** how to create resources.
    
Just add some resources in the blitz file, and you now have a fully functional API and the corresponding database schema, along with all the modern features you can expect from a modern app like:

- **Automatic Swagger UI** for the API
- **Admin Interface**
- **Dashboard**: including GPT builder, Blitz file editor, logs ...
- **Data Validation and Error Messages** (thanks to Fastapi and SQLModel)
- **Automatic Database Migration**
- **Generated ERD Diagram**
- and more...


