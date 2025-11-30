import other_functions
import dungeon_functions
import shop
import misc

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
                dungeon_functions.dungeon(current_user)
                user_data = other_functions.load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', other_functions.default_player_data())
                    other_functions.ensure_user_fields(current_user)
            elif choice == '2':
                shop()
                user_data = other_functions.load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', other_functions.default_player_data())
                    other_functions.ensure_user_fields(current_user)
            elif choice == '3':
                other_functions.magic_pack_interface(current_user)
                user_data = other_functions.load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', other_functions.default_player_data())
                    other_functions.ensure_user_fields(current_user)
            elif choice == '4':
                other_functions.permanent_upgrades_interface(current_user)
                user_data = other_functions.load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', other_functions.default_player_data())
                    other_functions.ensure_user_fields(current_user)
            elif choice == '5':
                other_functions.equip_titles_menu(current_user, player_data, None)
                user_data = other_functions.load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', other_functions.default_player_data())
                    other_functions.ensure_user_fields(current_user)
            elif choice == '6':
                other_functions.manage_inventory_menu(current_user, player_data, None)
                user_data = other_functions.load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', other_functions.default_player_data())
                    other_functions.ensure_user_fields(current_user)
            elif choice == '7':
                other_functions.magic_spell_interface(current_user)
                user_data = other_functions.load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', other_functions.default_player_data())
                    other_functions.ensure_user_fields(current_user)
            elif choice == '8':
                other_functions.settings_menu(current_user)
                user_data = other_functions.load_user_data(current_user)
                if user_data:
                    score = user_data.get('score', 0)
                    money = user_data.get('money', 40)
                    player_data = user_data.get('player_data', other_functions.default_player_data())
                    other_functions.ensure_user_fields(current_user)
            elif choice == '9':
                if other_functions.get_leaderboard():
                    print('\n--- Leaderboard ---')
                    leaderboard = other_functions.get_leaderboard()
                    for rank, (uname, user_score) in enumerate(leaderboard, start=1):
                        print(f'{rank}. {uname} - {user_score}')
                else:
                    print('No users yet!')
            elif choice == '10':
                print('Logged out.')
                other_functions.stop_autosave()
                current_user = None
                score = 0
                player_data = None
                money = 40
            elif choice == '11':
                print('Goodbye! Data saved automatically.')
                other_functions.save_all_data()
                break
            elif choice == '10234':
                other_functions.debug_console(current_user, score, money, player_data, misc.misc.USERS_DIR)
            else:
                print('Invalid choice.')
        elif choice == '1':
            machine_id = other_functions.get_machine_id()
            home_accounts = other_functions.get_home_accounts_for_machine(machine_id)
            if home_accounts:
                print(f'Home accounts found: {home_accounts}')
                if len(home_accounts) == 1:
                    username = home_accounts[0]
                    print(f'Home account detected: {username}')
                    confirm = input('Auto-login to this account? (y/n): ').strip().lower()
                    if confirm in ['y', 'yes']:
                        user_data = other_functions.load_user_data(username)
                        if user_data:
                            score = user_data.get('score', 0)
                            money = user_data.get('money', 40)
                            player_data = user_data.get('player_data', other_functions.default_player_data())
                            current_user = username
                            other_functions.ensure_user_fields(current_user)
                            print(f'Auto-login successful! Highscore = {score}')
                        else:
                            print('Auto-login failed!')
                    else:
                        username = input('Username: ').strip().lower()
                        password = input('Password: ').strip()
                        score, money, player_data = other_functions.signin(username, password)
                        if score is not None:
                            other_functions.set_machine_home(username)
                            current_user = username
                            other_functions.ensure_user_fields(current_user)
                            _, _, player_data = other_functions.signin(username, password)
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
                            user_data = other_functions.load_user_data(username)
                            if user_data:
                                score = user_data.get('score', 0)
                                money = user_data.get('money', 40)
                                player_data = user_data.get('player_data', other_functions.default_player_data())
                                current_user = username
                                other_functions.ensure_user_fields(current_user)
                                print(f'Auto-login successful! Highscore = {score}')
                            else:
                                print('Auto-login failed!')
                        elif idx == len(home_accounts):
                            username = input('Username: ').strip().lower()
                            password = input('Password: ').strip()
                            score, money, player_data = other_functions.signin(username, password)
                            if score is not None:
                                other_functions.set_machine_home(username)
                                current_user = username
                                other_functions.ensure_user_fields(current_user)
                                _, _, player_data = other_functions.signin(username, password)
                                print(f'Login successful! Highscore = {score}')
                            else:
                                print('Login failed!')
                        else:
                            print('Invalid choice.')
                    else:
                        username = input('Username: ').strip().lower()
                        password = input('Password: ').strip()
                        score, money, player_data = other_functions.signin(username, password)
                        if score is not None:
                            other_functions.set_machine_home(username)
                            current_user = username
                            other_functions.ensure_user_fields(current_user)
                            _, _, player_data = other_functions.signin(username, password)
                            print(f'Login successful! Highscore = {score}')
                        else:
                            print('Login failed!')
            else:
                print(f'No home accounts found for machine {machine_id}')
                username = input('Username: ').strip().lower()
                password = input('Password: ').strip()
                score, money, player_data = other_functions.signin(username, password)
                if score is not None:
                    other_functions.set_machine_home(username)
                    current_user = username
                    other_functions.ensure_user_fields(current_user)
                    _, _, player_data = other_functions.signin(username, password)
                    print(f'Login successful! Highscore = {score}')
                else:
                    print('Login failed!')
        elif choice == '2':
            username = input('\nUsername: ').strip().lower()
            password = input('Password: ').strip()
            if username in ['', ' ', '  ', '   ', '    '] or password in ['', ' ', '  ', '   ', '    ']:
                print('Password or Username cannot be empty!')
                break
            if other_functions.signup(username, password):
                score, money, player_data = other_functions.signin(username, password)
                current_user = username
                other_functions.ensure_user_fields(current_user)
                _, _, player_data = other_functions.signin(username, password)
                print(f'Signup successful! You are now logged in.')
            else:
                pass
        elif choice == '3':
            if other_functions.get_leaderboard():
                print('\n--- Leaderboard ---')
                leaderboard = other_functions.get_leaderboard()
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
    other_functions.check_file_existence()
    other_functions.setup_db()
    other_functions.atexit.register(other_functions.save_all_data)
    main_menu()