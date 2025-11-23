from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state):
    """Выводит на экран содержимое инвентаря игрока.

    Args:
        game_state: Словарь с состоянием игры, содержащий player_inventory
    """
    inventory = game_state["player_inventory"]

    if inventory:
        print("Ваш инвентарь: ", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")


def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении, если это возможно.

    Проверяет наличие выхода в указанном направлении. Для входа в комнату сокровищ
    требуется наличие ключа rusty_key в инвентаре. После перемещения обновляет
    счетчик шагов, описывает новую комнату и может вызвать случайное событие.

    Args:
        game_state: Словарь с состоянием игры
        direction: Направление движения (north, south, east, west)
    """
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if direction in room["exits"]:
        next_room = room["exits"][direction]
        if next_room == "treasure_room":
            if "rusty_key" not in game_state["player_inventory"]:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return
            print(
                "Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ."
            )

        game_state["current_room"] = room["exits"][direction]
        game_state["steps_taken"] = game_state["steps_taken"] + 1
        describe_current_room(game_state)
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    """Поднимает предмет из текущей комнаты и добавляет его в инвентарь.

    Проверяет наличие предмета в комнате. Сундук с сокровищами нельзя поднять.

    Args:
        game_state: Словарь с состоянием игры
        item_name: Название предмета для поднятия
    """
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
    """Использует предмет из инвентаря игрока.

    Args:
        game_state: Словарь с состоянием игры
        item_name: Название предмета для использования
    """
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case "torch":
            print("Стало светлее.")

        case "sword":
            print("Вы чувствуете себя более уверенно.")

        case "bronze_box":
            print("Вы открыли бронзовую шкатулку. Внутри вы нашли ржавый ключ!")
            if "rusty_key" not in inventory:
                game_state["player_inventory"].append("rusty_key")
            else:
                print("Ржавый ключ у вас уже есть.")

        case _:
            print(f"Вы не знаете, как использовать {item_name}.")
