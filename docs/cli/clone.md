# Clone

With clone you can create a new Blitz project from a Blitz App running on a remote server.

A Blitz App can expose the `/blitz-file` endpoint which is the Blitz file of the current running Blitz App.

!!! tip
    You can desactivate this feature with  `blitz start --no-config-route` option.

You can try it with the demo:
```console
blitz clone https://demo.blitz.paperz.app/blitz-file
```

<!-- termynal -->

<div class="termy">

```console
$ blitz clone https://demo.blitz.paperz.app/blitz-file

<span style="color: #af87ff; font-weight: bold;">Demo Blitz App</span> created successfully !
To start your app, you can use:
    <span style="color: #af87ff; font-weight: bold;">blitz start demo-blitz-app</span>
```

</div>