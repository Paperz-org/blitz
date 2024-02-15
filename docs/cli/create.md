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
    <span style="color: #af87ff; font-weight: bold;">blitz start tutu</span>
```

</div>

!!! note
    Use `blitz create --help` to see all available options.
