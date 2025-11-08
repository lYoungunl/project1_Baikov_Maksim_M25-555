#!/usr/bin/env python3

from .constants import ROOMS


def describe_current_room(game_state):
    room_name = game_state['current_room']
    room = ROOMS[room_name]
    
    print(f"\n== {room_name.upper()} ==")
    print(room['description'])
    
    if room['items']:
        print("Заметные предметы:", ", ".join(room['items']))
    
    if room['exits']:
        exits = [f"{dir} -> {room}" for dir, room in room['exits'].items()]
        print("Выходы:", ", ".join(exits))
    
    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    room_name = game_state['current_room']
    room = ROOMS[room_name]
    
    if not room['puzzle']:
        print("Загадок здесь нет.")
        return
    
    question, answer = room['puzzle']
    print(f"\nЗагадка: {question}")
    
    user_answer = input("Ваш ответ: ").strip()
    
    if user_answer.lower() == answer.lower():
        print("Верно! Загадка решена!")
        # Убираем загадку из комнаты
        ROOMS[room_name]['puzzle'] = None
        # Награда за решение загадки
        if room_name == 'treasure_room':
            attempt_open_treasure(game_state)
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    room_name = game_state['current_room']
    
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if 'treasure_chest' in ROOMS[room_name]['items']:
            ROOMS[room_name]['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        response = input("Сундук заперт. Попробовать ввести код?"
                        " (да/нет): ").strip().lower()
        if response == 'да':
            code = input("Введите код: ").strip()
            if code == '10':  # Правильный код из загадки
                print("Код верный! Сундук открыт!")
                if 'treasure_chest' in ROOMS[room_name]['items']:
                    ROOMS[room_name]['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код.")
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
    print("  help            - показать это сообщение")
