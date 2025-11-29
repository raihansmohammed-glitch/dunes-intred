import json
import random
import os
import math
import time
import atexit
import threading
import socket

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_DIR = os.path.join(SCRIPT_DIR, 'users.txt')
DUNGEON_TREASURE_FILE = os.path.join(SCRIPT_DIR, 'dungeon_treasure.json')
dungeon_treasure = {'money': 0, 'items': []}
GLOBAL_KEY = '__global__'
AUTOSAVE_INTERVAL = 30
autosave_timer = None
last_autosave_time = time.time()

from misc import *
from dungeon_functions import *
from other_functions import *

def main_menu():
    global current_user, score, player_data, money
    current_user = None
    score = 0
    player_data = None
    money = 40
    while True:
        if current_user:
            print(f'\nLogged in as: {current_user}')
            print('1. Explore dungeons')
            print('2. Shop')
            print('3. Magic packs')
            print('4. Permanent upgrades')
            print('5. Equip titles')
            print('6. Manage inventory')
            print('7. Equip spells')
            print('8. Settings')
            print('9. Leaderboard')
            print('10. Logout')
            print('11. Exit')
        else:
            print('\nMain Menu')
            print('1. Login')
            print('2. Signup')
            print('3. Leaderboard')
            print('4. Exit')
        choice = input('Choose an option: ').strip()
        if current_user:
            if choice == '1':
                dungeon(current_user)
                user_data = load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', default_player_data())
                    ensure_user_fields(current_user)
            elif choice == '2':
                shop()
                user_data = load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', default_player_data())
                    ensure_user_fields(current_user)
            elif choice == '3':
                magic_pack_interface(current_user)
                user_data = load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', default_player_data())
                    ensure_user_fields(current_user)
            elif choice == '4':
                permanent_upgrades_interface(current_user)
                user_data = load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', default_player_data())
                    ensure_user_fields(current_user)
            elif choice == '5':
                equip_titles_menu(current_user, player_data, None)
                user_data = load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', default_player_data())
                    ensure_user_fields(current_user)
            elif choice == '6':
                manage_inventory_menu(current_user, player_data, None)
                user_data = load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', default_player_data())
                    ensure_user_fields(current_user)
            elif choice == '7':
                magic_spell_interface(current_user)
                user_data = load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', default_player_data())
                    ensure_user_fields(current_user)
            elif choice == '8':
                settings_menu(current_user)
                user_data = load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', default_player_data())
                    ensure_user_fields(current_user)
            elif choice == '9':
                if get_leaderboard():
                    print('\n--- Leaderboard ---')
                    leaderboard = get_leaderboard()
                    for rank, (uname, user_score) in enumerate(leaderboard, start=1):
                        print(f'{rank}. {uname} - {user_score}')
                else:
                    print('No users yet!')
            elif choice == '10':
                print('Logged out.')
                stop_autosave()
                current_user = None
                score = 0
                player_data = None
                money = 40
            elif choice == '11':
                print('Goodbye! Data saved automatically.')
                save_all_data()
                break
            elif choice == '10234':
                debug_console(current_user, score, money, player_data, USERS_DIR)
            else:
                print('Invalid choice.')
        elif choice == '1':
            machine_id = get_machine_id()
            home_accounts = get_home_accounts_for_machine(machine_id)
            if home_accounts:
                print(f'Home accounts found: {home_accounts}')
                if len(home_accounts) == 1:
                    username = home_accounts[0]
                    print(f'Home account detected: {username}')
                    confirm = input('Auto-login to this account? (y/n): ').strip().lower()
                    if confirm in ['y', 'yes']:
                        user_data = load_user_data(username)
                        if user_data:
                            score = user_data.get('score', 0)
                            money = user_data.get('money', 40)
                            player_data = user_data.get('player_data', default_player_data())
                            current_user = username
                            ensure_user_fields(current_user)
                            print(f'Auto-login successful! Highscore = {score}')
                        else:
                            print('Auto-login failed!')
                    else:
                        username = input('Username: ').strip().lower()
                        password = input('Password: ').strip()
                        score, money, player_data = signin(username, password)
                        if score is not None:
                            set_machine_home(username)
                            current_user = username
                            ensure_user_fields(current_user)
                            _, _, player_data = signin(username, password)
                            print(f'Login successful! Highscore = {score}')
                        else:
                            print('Login failed!')
                else:
                    print('Multiple home accounts detected:')
                    for i, acc in enumerate(home_accounts, 1):
                        print(f'{i}. {acc}')
                    print(f'{len(home_accounts) + 1}. Enter username manually')
                    choice_idx = input('Choose account number for auto-login: ').strip()
                    if choice_idx.isdigit():
                        idx = int(choice_idx) - 1
                        if 0 <= idx < len(home_accounts):
                            username = home_accounts[idx]
                            user_data = load_user_data(username)
                            if user_data:
                                score = user_data.get('score', 0)
                                money = user_data.get('money', 40)
                                player_data = user_data.get('player_data', default_player_data())
                                current_user = username
                                ensure_user_fields(current_user)
                                print(f'Auto-login successful! Highscore = {score}')
                            else:
                                print('Auto-login failed!')
                        elif idx == len(home_accounts):
                            username = input('Username: ').strip().lower()
                            password = input('Password: ').strip()
                            score, money, player_data = signin(username, password)
                            if score is not None:
                                set_machine_home(username)
                                current_user = username
                                ensure_user_fields(current_user)
                                _, _, player_data = signin(username, password)
                                print(f'Login successful! Highscore = {score}')
                            else:
                                print('Login failed!')
                        else:
                            print('Invalid choice.')
                    else:
                        username = input('Username: ').strip().lower()
                        password = input('Password: ').strip()
                        score, money, player_data = signin(username, password)
                        if score is not None:
                            set_machine_home(username)
                            current_user = username
                            ensure_user_fields(current_user)
                            _, _, player_data = signin(username, password)
                            print(f'Login successful! Highscore = {score}')
                        else:
                            print('Login failed!')
            else:
                print(f'No home accounts found for machine {machine_id}')
                username = input('Username: ').strip().lower()
                password = input('Password: ').strip()
                score, money, player_data = signin(username, password)
                if score is not None:
                    set_machine_home(username)
                    current_user = username
                    ensure_user_fields(current_user)
                    _, _, player_data = signin(username, password)
                    print(f'Login successful! Highscore = {score}')
                else:
                    print('Login failed!')
        elif choice == '2':
            username = input('\nUsername: ').strip().lower()
            password = input('Password: ').strip()
            if username in ['', ' ', '  ', '   ', '    '] or password in ['', ' ', '  ', '   ', '    ']:
                print('Password or Username cannot be empty!')
                break
            if signup(username, password):
                score, money, player_data = signin(username, password)
                current_user = username
                ensure_user_fields(current_user)
                _, _, player_data = signin(username, password)
                print(f'Signup successful! You are now logged in.')
            else:
                pass
        elif choice == '3':
            if get_leaderboard():
                print('\n--- Leaderboard ---')
                leaderboard = get_leaderboard()
                for rank, (uname, user_score) in enumerate(leaderboard, start=1):
                    print(f'{rank}. {uname} - {user_score}')
            else:
                print('No users yet!')
        elif choice == '4':
            print('Goodbye! Data saved automatically.')
            break
        else:
            print('Oops, looks like you accidentally pressed the wrong button. Go again')
            continue

if __name__ == '__main__':
    check_file_existence()
    setup_db()
    atexit.register(save_all_data)
    main_menu()