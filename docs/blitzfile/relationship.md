## Relationship
Currently supported relationships are:
- One-to-many
- One-to-one

### One-to-Many
> A **Player** has many **Item**s.

In the following example, a **player has many items**
=== "Yaml"
    ```yaml
    - name: Player
        fields:
            name: str
            items: Item[]
    - name: Item
        fields:
            name: str
            player_id: Player.id
            player: Player
    ```

=== "Json"
    ```json
    [
        {
            "name": "Player",
            "fields": {
                "name": "str",
                "items": "Item[]"
            }
        },
        {
            "name": "Item",
            "fields": {
                "name": "str",
                "player_id": "Player.id",
                "player": "Player"
            }
        }
    ]
    ```

=== "Yaml (explicit)"
    ```yaml
    - name: Player
        fields:
            name:
                type: str
            items:
                type: relationship
                relationship: Item
                relationship_list: true
    - name: Item
        fields:
            name: 
                type: str
            player_id:
                type: foreign_key
                foreign_key: Player.id
            player:
                type: relationship
                relationship: Player
    ```

=== "Json (explicit)"
    ```json
    [
        {
            "name": "Player",
            "fields": {
                "name": {
                    "type": "str"
                },
                "items": {
                    "type": "relationship",
                    "relationship": "Item",
                    "relationship_list": true
                }
            }
        },
        {
            "name": "Item",
            "fields": {
                "name": {
                    "type": "str"
                },
                "player_id": {
                    "type": "foreign_key",
                    "foreign_key": "Player.id"

                },
                "player": {
                    "type": "relationship",
                    "relationship": "Player"
                }
            }
        }
    ]
    ```


By specifying the player relationship from the **Item** entity, we made a `Item->Player` relationship where an **Item** is related to a single **Player**.

Because the **Player** entity don't have any relationship declared, there is no rules concerning the relationship between `Player->Item`.

!!! note
    As you can see, you can declare a `items` relationship in the `Player` resource to make the relationship usable from the `Player` entity.

    This is fully optional and it don't do anything about the real relationship between `Player` and `Item` because evrything is set in the `Item` resource, but it allow the `Player` resource to display the linked `Item`s resources.


Then, one **Item** belongs to one **Player** entity and one **Player** can have multiple **Item** entities. This is a **One to Many** relationship.


### One to One

In the following example, a **player has one bank account** and a **bank has many accounts**.
=== "Yaml"
    ```yaml
    - name: Player
        fields:
            name: str
            account: BankAccount
    - name: Bank
        fields:
            name: str
    - name: BankAccount
        fields:
            bank_id: Bank.id
            bank: Bank
            player_id: Player.id
            player: Player
    ```

=== "Json"
    ```json
    [
        {
            "name": "Player",
            "fields": {
                "name": "str",
                "account": "BankAccount"
            }
        },
        {
            "name": "Bank",
            "fields": {
                "name": "str"
            }
        },
        {
            "name": "BankAccount",
            "fields": {
                "bank_id": "Bank.id",
                "bank": "Bank",
                "player_id": "Player.id",
                "player": "Player"
            }
        }
    ]
    ```

=== "Yaml (explicit)"
    ```yaml
    - name: Player
        fields:
            name:
                type: str
            account:
                type: relationship
                relationship: BankAccount
    - name: Bank
        fields:
            name: str
    - name: BankAccount
        fields:
            bank_id:
                type: foreign_key
                foreign_key: Bank.id
            bank:
                type: relationship
                relationship: Bank
            player_id:
                type: foreign_key
                foreign_key: Player.id
                unique: true
            player:
                type: relationship
                relationship: Player
    ```

=== "Json (explicit)"
    ```json
    [
        {
            "name": "Player",
            "fields": {
                "name": {
                    "type": "str"
                },
                "account": {
                    "type": "relationship",
                    "relationship": "BankAccount"
                }
            }
        },
        {
            "name": "Bank",
            "fields": {
                "name": "str"
            }
        },
        {
            "name": "BankAccount",
            "fields": {
                "bank_id": {
                    "type": "foreign_key",
                    "foreign_key": "Bank.id"
                },
                "bank": {
                    "type": "relationship",
                    "relationship": "Bank"
                },
                "player_id": {
                    "type": "foreign_key",
                    "foreign_key": "Player.id",
                    "unique": true
                },
                "player": {
                    "type": "relationship",
                    "relationship": "Player"
                }
            }
        }
    ]
    ```

By specifying the player relationship from the **BankAccount** entity, we made a `BankAccount->Player` relationship where a BankAccount is related to a single **Player**.

Because we also specify the **player_id** to be unique, The relationship to a player id can only exists once. Then a **Player** can have only one **BankAccount**.


!!! note
    As you can see, you can declare a `account` relationship in the `Player` resource to make the relationship usable from the `Player` entity.

    This is fully optional and it don't do anything about the real relationship between `Player` and `BankAccount` because evrything is set in the `BankAccount` resource, but it allow the `Player` resource to display the linked `BankAccount` resource.

Then, one **Player** has one **BankAccount** entity and one **BankAccount** is related to a single **Player**. This is a **One to One** relationship.

## Known issues
- Currently you **MUST** specify a foreign key and a relationship attribute to make it work correctly.