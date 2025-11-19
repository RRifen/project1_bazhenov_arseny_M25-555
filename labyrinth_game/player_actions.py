from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room


def show_inventory(game_state):
    inventory = game_state["player_inventory"]

    if inventory:
        print("Ваш инвентарь: ", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")


def move_player(game_state, direction):
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if direction in room["exits"]:
        game_state["current_room"] = room["exits"][direction]
        game_state["steps"] = game_state["steps"] + 1
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if item_name in room["items"]:
        if item_name == "treasure_chest":
            print("Вы не можете поднять сундук, он слишком тяжелый.")
            return

        game_state["player_inventory"].append(item_name)
        room["items"].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case "torch":
            print("Стало светлее.")

        case "sword":
            print("Вы чувствуете себя более уверенно.")

        case "bronze box":
            print("Вы открыли бронзовую шкатулку. Внутри вы нашли ржавый ключ!")
            if "rusty_key" not in inventory:
                game_state["player_inventory"].append("rusty_key")
            else:
                print("Ржавый ключ у вас уже есть.")

        case _:
            print(f"Вы не знаете, как использовать {item_name}.")
