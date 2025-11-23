import math

from labyrinth_game.constants import COMMANDS, ROOMS


def describe_current_room(game_state):
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    print(f"== {room_name.upper()} ==")

    print(room["description"])

    if room.get("items"):
        print("Заметные предметы: ", ", ".join(room["items"]))

    print("Выходы: ", ", ".join(room["exits"].keys()))

    if room.get("puzzle"):
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if not room["puzzle"]:
        print("Загадок здесь нет.")
        return

    print(f"Загадка: {room['puzzle']['question']}")

    answer = get_input("Ваш ответ: ").strip().lower()

    if answer in room["puzzle"]["answers"]:
        print("Верно! Загадка разгадана.")

        reward = room["puzzle"]["reward"]
        room["puzzle"] = None

        game_state["player_inventory"].append(reward)
        print(f"Вы получили: {reward}!")

    else:
        if room_name == "trap_room":
            trigger_trap(game_state)
        else:
            print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if "treasure_key" in game_state["player_inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")

        room["items"].remove("treasure_chest")

        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    choice = get_input("Сундук заперт. ... Ввести код? (да/нет): ").strip().lower()

    if choice == "да":
        code = get_input("Введите код: ").strip().lower()

        if code in room["puzzle"]["answers"]:
            print("Замок щёлкает! Сундук открыт!")

            room["items"].remove("treasure_chest")

            print("В сундуке сокровище! Вы победили!")
            game_state["game_over"] = True
        else:
            print("Код не подошел. Замок не открылся.")
    else:
        print("Вы отступаете от сундука.")


def show_help():
    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f"{command:<16} - {description}")


def get_input(prompt="> "):
    try:
        user_input = input(prompt).strip().lower()
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("Выход из игры.")
        return "quit"


def pseudo_random(seed, modulo):
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return math.floor(fractional * modulo)


def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]

    if inventory:
        item_index = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory[item_index]
        inventory.remove(lost_item)
        print(f"Из-за тряски вы потеряли: {lost_item}!")
    else:
        damage_chance = pseudo_random(game_state["steps_taken"], 10)
        if damage_chance < 3:
            print("Игра окончена. Вы проиграли!")
            game_state["game_over"] = True
        else:
            print("Вы уцелели.")


def random_event(game_state):
    event_chance = pseudo_random(game_state["steps_taken"], 10)
    if event_chance != 0:
        return

    event_type = pseudo_random(game_state["steps_taken"], 3)

    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    inventory = game_state["player_inventory"]

    if event_type == 0:
        room["items"].append("coin")
        print("Вы нашли монетку! Она теперь лежит в этой комнате.")

    elif event_type == 1:
        print("Вы слышите странный шорох...")
        if "sword" in inventory:
            print("Вы достали меч, и существо убежало.")

    elif event_type == 2:
        if room_name == "trap_room" and "torch" not in inventory:
            print("Вы чувствуете опасность...")
            trigger_trap(game_state)
