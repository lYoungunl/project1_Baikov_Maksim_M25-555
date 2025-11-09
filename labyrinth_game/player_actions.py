#!/usr/bin/env python3

from .constants import ROOMS
from .utils import describe_current_room, random_event


def get_input(prompt="> "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("\nВаш инвентарь:", ", ".join(inventory))
    else:
        print("\nВаш инвентарь пуст.")


def move_player(game_state, direction):
    room_name = game_state['current_room']
    room = ROOMS[room_name]
    
    if direction in room['exits']:
        game_state['current_room'] = room['exits'][direction]
        game_state['steps_taken'] += 1
        print(f"\nВы пошли {direction}...")
        describe_current_room(game_state)
        # Вызываем случайное событие после перемещения
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    room_name = game_state['current_room']
    room = ROOMS[room_name]
    
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return
    
    if item_name in room['items']:
        game_state['player_inventory'].append(item_name)
        room['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return
    
    if item_name == 'torch':
        print("Вы зажигаете факел. Стало светлее!")
    elif item_name == 'sword':
        print("Вы чувствуете уверенность с мечом в руках.")
    elif item_name == 'bronze_box':
        if 'treasure_key' not in game_state['player_inventory']:
            print("Вы открываете бронзовую шкатулку. Внутри лежит ключ от сокровищ!")
            game_state['player_inventory'].append('treasure_key')
        else:
            print("Шкатулка пуста.")
    elif item_name == 'coin':
        print("Вы подбрасываете монетку... Блестит!")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
