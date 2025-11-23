# labyrinth_game/constants.py
ROOMS = {
    "entrance": {
        "description": (
            "Вы в темном входе лабиринта. Стены покрыты мхом. На полу лежит "
            "старый факел."
        ),
        "exits": {"north": "hall", "east": "trap_room"},
        "items": ["torch"],
        "puzzle": None,
    },
    "hall": {
        "description": (
            "Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком."
        ),
        "exits": {"south": "entrance", "west": "library", "north": "treasure_room"},
        "items": [],
        "puzzle": {
            "question": (
                'На пьедестале надпись: "Назовите число, которое идет после девяти". '
                "Введите ответ цифрой или словом."
            ),
            "answers": ["10", "десять"],
            "reward": "branch",
        },
    },
    "trap_room": {
        "description": (
            "Комната с хитрой плиточной поломкой. На стене видна надпись: "
            '"Осторожно — ловушка".'
        ),
        "exits": {"west": "entrance", "east": "gaga_room"},
        "items": ["rusty_key"],
        "puzzle": {
            "question": (
                'Система плит активна. Чтобы пройти, назовите слово "шаг" три раза '
                'подряд (введите "шаг шаг шаг")'
            ),
            "answers": ["шаг шаг шаг"],
            "reward": "coin",
        },
    },
    "library": {
        "description": (
            "Пыльная библиотека. На полках старые свитки. Где-то здесь "
            "может быть ключ от сокровищницы."
        ),
        "exits": {"east": "hall", "north": "armory"},
        "items": ["ancient_book"],
        "puzzle": {
            "question": (
                'В одном свитке загадка: "Что растет, когда его съедают?" '
                "(ответ одно слово)"
            ),
            "answers": ["резонанс"],
            "reward": "treasure_key",
        },
    },
    "armory": {
        "description": (
            "Старая оружейная комната. На стене висит меч, рядом — "
            "небольшая бронзовая шкатулка."
        ),
        "exits": {"south": "library"},
        "items": ["sword", "bronze_box"],
        "puzzle": None,
    },
    "treasure_room": {
        "description": (
            "Комната, на столе большой сундук. Дверь заперта — нужен особый ключ."
        ),
        "exits": {"south": "hall"},
        "items": ["treasure_chest"],
        "puzzle": {
            "question": (
                "Дверь защищена кодом. Введите код (подсказка: это число пятикратного"
                " шага, 2*5= ? )"
            ),
            "answers": ["10", "десять"],
            "reward": "candy",
        },
    },
    "gaga_room": {
        "description": (
            "Комната с большшим числом зеркал. В центре находится каменная "
            "женская статуя, покрытая кусками мяса"
        ),
        "exits": {"west": "trap_room", "east": "portal_room"},
        "items": ["meat"],
        "puzzle": {
            "question": (
                'Вы слышите голос в голове, который говорит: "Чтобы пройти дальше, '
                'введи название последнего альбома Леди Гаги"'
            ),
            "answers": ["mayhem"],
            "reward": "mayhem_album",
        },
    },
    "portal_room": {
        "description": "Абсолютно черная комната с порталами на каждой из 4 стен.",
        "exits": {
            "west": "portal_room",
            "east": "portal_room",
            "north": "portal_room",
            "south": "hall",
        },
        "items": [],
        "puzzle": {
            "question": (
                'На потолке написано: "Там все стороны света — на север глядят.'
            ),
            "answers": ["юг", "south"],
            "reward": "coin",
        },
    },
}

COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "solve": "попытаться решить загадку в комнате",
    "inventory": "показать инвентарь",
    "help": "показать справку",
    "quit, exit": "выйти из игры",
}
