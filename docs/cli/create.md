The `blitz create` command is used to create a new blitz app. It will ask you for the name of your app, the description of your app and the format of the blitz file.

The default format is `yaml`. You can also use `json` format.

<!-- termynal -->

<div class="termy">

```console
$ blitz create your-blitz-app
Enter the description of your blitz app ():
// this is my first blitz app
Choose the format of the blitz file [json/yaml] (yaml):
// yaml

<span style="color: #af87ff; font-weight: bold;">your-blitz-app</span> created successfully !
To start your app, you can use:
    <span style="color: #af87ff; font-weight: bold;">blitz start your-blitz-app</span>
```

</div>

!!! tip

    You can also use `--demo` to create an already configured blitz app with some resources and relationships.

<!-- termynal -->

<div class="termy">

```console
$ blitz create --demo
<span style="color: #af87ff; font-weight: bold;">Demo Blitz App</span> created successfully !
To start your app, you can use:
    <span style="color: #af87ff; font-weight: bold;">blitz start demo-blitz-app</span>

$ blitz start demo-blitz-app
<span style="color: yellow; font-weight: bold;">This is still an alpha. Please do not use in production.</span>
<span style="color: yellow; font-weight: bold;">Please report any issues on https://github.com/Paperz-org/blitz</span>

<span style="color: #af87ff; font-weight: bold;">Blitz app deployed.</span>
<span style="color: #af87ff; font-weight: bold;">  - Blitz UI            : <a style="cursor: pointer" href="http://0.0.0.0:8100" target="_blank" rel="noopener noreferrer">http://0.0.0.0:8100</a></span>
<span style="color: #af87ff; font-weight: bold;">  - Blitz admin         : <a style="cursor: pointer" href="http://0.0.0.0:8100/admin" target="_blank" rel="noopener noreferrer">http://0.0.0.0:8100/admin</a></span>
<span style="color: #af87ff; font-weight: bold;">  - Swagger UI          : <a style="cursor: pointer" href="http://0.0.0.0:8100/api/docs" target="_blank" rel="noopener noreferrer">http://0.0.0.0:8100/api/docs</a></span>

<span style="color: lightblue; font-weight: bold;">INFO</span>      demo-blitz-app Started server process [21292026]
<span style="color: lightblue; font-weight: bold;">INFO</span>      demo-blitz-app Waiting for application startup.
<span style="color: lightblue; font-weight: bold;">INFO</span>      demo-blitz-app Application startup complete.
```

</div>

!!! note

    Use `blitz create --help` to see all available options.
