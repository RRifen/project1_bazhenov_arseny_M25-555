#!/usr/bin/env python3


from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import (
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    get_input,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command):
    """Обрабатывает команду игрока и выполняет соответствующее действие.

    Args:
        game_state: Словарь с состоянием игры
        command: Строка с командой игрока (может содержать аргументы)
    """
    parts = command.split()

    action = parts[0]
    argument = parts[1] if len(parts) > 1 else None

    match action:
        case "look":
            describe_current_room(game_state)

        case "use":
            if argument:
                use_item(game_state, argument)
            else:
                print("Укажите предмет.")

        case "go":
            if argument:
                move_player(game_state, argument)
            else:
                print("Укажите направление.")

        case "north" | "south" | "east" | "west":
            move_player(game_state, action)

        case "take":
            if argument:
                take_item(game_state, argument)
            else:
                print("Укажите предмет.")

        case "inventory":
            show_inventory(game_state)

        case "solve":
            room_name = game_state["current_room"]
            room = ROOMS[room_name]
            if "treasure_chest" in room.get("items", []):
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)

        case "quit" | "exit":
            game_state["game_over"] = True

        case "help":
            show_help()

        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")


def main():
    """Главная функция игры. Инициализирует состояние игры и запускает игровой цикл.

    Создает начальное состояние игры и обрабатывает команды игрока до тех пор,
    пока игра не будет завершена.
    """
    game_state = {
        "player_inventory": [],  # Инвентарь игрока
        "current_room": "entrance",  # Текущая комната
        "game_over": False,  # Значения окончания игры
        "steps_taken": 0,  # Количество шагов
    }

    print("Добро пожаловать в Лабиринт сокровищ!\n")

    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input("Введите команду: ")
        print(command)
        process_command(game_state, command)


if __name__ == "__main__":
    main()
