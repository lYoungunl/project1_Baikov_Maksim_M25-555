#!/usr/bin/env python3

import math

from .constants import ROOMS


def pseudo_random(seed, modulo):
    """Генерирует псевдослучайное число в диапазоне [0, modulo)"""
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return int(fractional * modulo)


def trigger_trap(game_state):
    """Активирует ловушку с негативными последствиями"""
    print("Ловушка активирована! Пол стал дрожать...")
    
    inventory = game_state['player_inventory']
    
    if inventory:
        # Случайно выбираем предмет для удаления
        index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Из вашего инвентаря выпал: {lost_item}")
    else:
        # Если инвентарь пуст - проверяем на поражение
        chance = pseudo_random(game_state['steps_taken'], 10)
        if chance < 3:
            print("Вы не удержались и упали в пропасть! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам чудом удалось удержаться!")


def random_event(game_state):
    """Случайные события при перемещении"""
    # 10% вероятность события
    if pseudo_random(game_state['steps_taken'], 10) != 0:
        return
    
    event_type = pseudo_random(game_state['steps_taken'] + 1, 3)
    current_room = game_state['current_room']
    
    if event_type == 0:
        # Находка
        print("Вы заметили что-то блестящее на полу... Это монетка!")
        ROOMS[current_room]['items'].append('coin')
    
    elif event_type == 1:
        # Испуг
        print("Вы слышите подозрительный шорох из темноты...")
        if 'sword' in game_state['player_inventory']:
            print("Вы достаете меч, и существо отступает!")
        else:
            print("Вы замираете от страха...")
    
    elif event_type == 2:
        # Ловушка
        if (current_room == 'trap_room' and 
            'torch' not in game_state['player_inventory']):
            print("Опасность! Вы не видите ловушку в темноте!")
            trigger_trap(game_state)


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
