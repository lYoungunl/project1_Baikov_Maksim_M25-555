#!/usr/bin/env python3

from .constants import COMMANDS
from .player_actions import get_input, move_player, show_inventory, take_item, use_item
from .utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle

game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0
}

def process_command(game_state, command):
    parts = command.lower().split()
    if not parts:
        return
    
    cmd = parts[0]
    
    # Односложные команды движения
    directions = ['north', 'south', 'east', 'west']
    if cmd in directions:
        move_player(game_state, cmd)
        return
    
    match cmd:
        case 'look':
            describe_current_room(game_state)
        case 'go' if len(parts) > 1:
            move_player(game_state, parts[1])
        case 'take' if len(parts) > 1:
            take_item(game_state, parts[1])
        case 'use' if len(parts) > 1:
            use_item(game_state, parts[1])
        case 'inventory':
            show_inventory(game_state)
        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case 'help':
            show_help(COMMANDS)  # ← ПЕРЕДАЕМ АРГУМЕНТ!
        case 'quit' | 'exit':
            print("До свидания!")
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")

def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    
    while not game_state['game_over']:
        command = get_input("\nВведите команду: ")
        process_command(game_state, command)

if __name__ == "__main__":
    main()