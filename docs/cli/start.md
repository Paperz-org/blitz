The `blitz start` command is used to start an existing blitz app. It will start the blitz API, the blitz admin and the blitz UI.

<!-- termynal -->

<div class="termy">

```console
$ blitz start your-blitz-app

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

!!! note
    Use `blitz create --help` to see all available options.
