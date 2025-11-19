import random

from labyrinth_game.constants import REWARDS, ROOMS


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

    print(f"Загадка: {room['puzzle'][0]}")

    answer = get_input("Ваш ответ: ").strip().lower()

    if answer == room["puzzle"][1]:
        print("Верно! Загадка разгадана.")

        room["puzzle"] = None

        reward = random.choice(REWARDS)

        game_state["player_inventory"].append(reward)
        print(f"Вы получили: {reward}!")

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

        if code == room["puzzle"](1):
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
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")


def get_input(prompt="> "):
    try:
        user_input = input(prompt).strip().lower()
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("Выход из игры.")
        return "quit"
