# API

The Blitz API contains all the exposed CRUD operations defined on the [Blitz File](/blitz/blitzfile/), but also the `/blitz-file` which is, as its name suggests, the Json representation of the running Blitz File.

This feature is used for the [clone command](/blitz/cli/clone/) and the [--url option of the start command](/blitz/cli/start).

This feature can be disabled with the `--no-config-route` option of the start command.

For exemple, this is the return of the demo `/blitz-file`:

```json
{
    "config":{
        "name":"Demo Blitz App",
        "description":"This is a demo blitz app",
        "version":"0.1.0"
    },
    "resources":{
        "Food":{
            "name":{
                "type":"str",
                "nullable":false,
                "unique":true
            },
            "expiration_date":{
                "type":"datetime",
                "nullable":false,
                "unique":false
            }
        },
        "Ingredient":{
            "food_id":{
                "type":"uuid",
                "foreign_key":"Food.id",
                "nullable":true,
                "unique":false
            },
            "food":{
                "type":"relationship",
                "relationship":"Food",
                "relationship_list":false,
                "nullable":false,
                "unique":false
            },
            "recipe_id":{
                "type":"uuid",
                "foreign_key":"Recipe.id",
                "nullable":true,
                "unique":false
            },
            "recipe":{
                "type":"relationship",
                "relationship":"Recipe",
                "relationship_list":false,
                "nullable":false,
                "unique":false
            }
        },
        "Recipe":{
            "name":{
                "type":"str",
                "nullable":false,
                "unique":true
            },
            "ingredients":{
                "type":"relationship",
                "relationship":"Ingredient",
                "relationship_list":true,
                "nullable":false,
                "unique":false
            },
            "cook_id":{
                "type":"uuid",
                "foreign_key":"Cook.id",
                "nullable":true,
                "unique":false
            },
            "cook":{
                "type":"relationship",
                "relationship":"Cook",
                "relationship_list":false,
                "nullable":false,
                "unique":false
            }
        },
        "Cook":{
            "name":{
                "type":"str",
                "nullable":false,
                "unique":true
            },
            "age":{
                "type":"int",
                "nullable":false,
                "unique":false
            },
            "recipes":{
                "type":"relationship",
                "relationship":"Recipe",
                "relationship_list":true,
                "nullable":false,
                "unique":false
            },
            "rat":{
                "type":"relationship",
                "relationship":"Rat",
                "relationship_list":false,
                "nullable":false,
                "unique":false
            }
        },
        "Rat":{
            "name":{
                "type":"str",
                "nullable":false,
                "unique":true
            },
            "age":{
                "type":"int",
                "nullable":false,
                "unique":false
            },
            "cook_id":{
                "type":"uuid",
                "foreign_key":"Cook.id",
                "nullable":true,
                "unique":true
            },
            "cook":{
                "type":"relationship",
                "relationship":"Cook",
                "relationship_list":false,
                "nullable":false,
                "unique":false
            }
        }
    }
}
```

!!! tip "Want to master the syntax of Blitz?"

    You can **[learn here](/blitz/blitzfile/)** how the Blitz File work.