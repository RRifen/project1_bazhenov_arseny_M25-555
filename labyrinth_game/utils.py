import math

from labyrinth_game.constants import COMMANDS, ROOMS

EVENT_DISTRIBUTION = 10
BAD_EVENT_NUMBER = 0
EVENT_TYPES_COUNT = 3
COIN_EVENT = 0
FEAR_EVENT = 1
TRAP_EVENT = 2
DAMAGE_DISTRIBUTION = 10
DAMAGE_CHANCE = 3


def describe_current_room(game_state):
    """Выводит описание текущей комнаты, включая предметы, выходы и наличие загадки.

    Args:
        game_state: Словарь с состоянием игры, содержащий current_room
    """
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
    """Позволяет игроку решить загадку в текущей комнате.

    Запрашивает ответ у игрока и проверяет его. При правильном ответе
    добавляет награду в инвентарь и удаляет загадку из комнаты.
    При неправильном ответе в комнате trap_room активирует ловушку.

    Args:
        game_state: Словарь с состоянием игры
    """
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
    """Попытка открыть сундук с сокровищами.

    Если у игрока есть treasure_key, сундук открывается автоматически.
    Иначе игрок может попытаться ввести код. При успешном открытии
    игра завершается победой.

    Args:
        game_state: Словарь с состоянием игры
    """
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
    """Выводит на экран список доступных команд игры и их описание."""
    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f"{command:<16} - {description}")


def get_input(prompt="> "):
    """Получает ввод от пользователя с обработкой ошибок.

    Args:
        prompt: Приглашение для ввода (по умолчанию "> ")

    Returns:
        str: Введенная пользователем строка в нижнем регистре или "quit"
             при прерывании ввода
    """
    try:
        user_input = input(prompt).strip().lower()
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("Выход из игры.")
        return "quit"


def pseudo_random(seed, modulo):
    """Генерирует псевдослучайное число на основе синусоидальной функции.

    Использует математическую формулу для генерации
    псевдослучайного значения в диапазоне [0, modulo).

    Args:
        seed: Начальное значение для генерации
        modulo: Верхняя граница диапазона (не включается)

    Returns:
        int: Псевдослучайное число от 0 до modulo-1
    """
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return math.floor(fractional * modulo)


def trigger_trap(game_state):
    """Активирует ловушку в комнате.

    Если у игрока есть предметы в инвентаре, случайно удаляет один из них.
    Если инвентарь пуст, с некоторой вероятностью завершает игру проигрышем.

    Args:
        game_state: Словарь с состоянием игры
    """
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]

    if inventory:
        item_index = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory[item_index]
        inventory.remove(lost_item)
        print(f"Из-за тряски вы потеряли: {lost_item}!")
    else:
        damage_chance = pseudo_random(game_state["steps_taken"], DAMAGE_DISTRIBUTION)
        if damage_chance < DAMAGE_CHANCE:
            print("Игра окончена. Вы проиграли!")
            game_state["game_over"] = True
        else:
            print("Вы уцелели.")


def random_event(game_state):
    """Обрабатывает случайные события при перемещении между комнатами.

    С определенной вероятностью может произойти одно из событий:
    - Появление монетки в комнате
    - Странный шорох (защита мечом)
    - Активация ловушки в trap_room (если нет факела)

    Args:
        game_state: Словарь с состоянием игры
    """
    event_chance = pseudo_random(game_state["steps_taken"], EVENT_DISTRIBUTION)
    if event_chance != BAD_EVENT_NUMBER:
        return

    event_type = pseudo_random(game_state["steps_taken"], EVENT_TYPES_COUNT)

    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    inventory = game_state["player_inventory"]

    if event_type == COIN_EVENT:
        room["items"].append("coin")
        print("Вы нашли монетку! Она теперь лежит в этой комнате.")

    elif event_type == FEAR_EVENT:
        print("Вы слышите странный шорох...")
        if "sword" in inventory:
            print("Вы достали меч, и существо убежало.")

    elif event_type == TRAP_EVENT:
        if room_name == "trap_room" and "torch" not in inventory:
            print("Вы чувствуете опасность...")
            trigger_trap(game_state)
