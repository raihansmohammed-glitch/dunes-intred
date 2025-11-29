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

def check_file_existence():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files_to_check = ['users.txt', 'dungeon_treasure.json']
    for file in files_to_check:
        current_path = os.path.join(script_dir, file)
        if os.path.exists(current_path):
            print(f"[OK] {file} exists in script directory")
        else:
            parent_path = os.path.join(script_dir, '..', file)
            if os.path.exists(parent_path):
                print(f"[OK] {file} exists in parent directory")
            else:
                print(f"[MISSING] {file} does not exist in parent directory")
            # Create in script directory since it doesn't exist here
            if file == 'users.txt':
                with open(os.path.join(script_dir, file), 'w') as f:
                    json.dump({}, f)
                print(f"[CREATE] {file} did not exist in script directory, created empty file.")
            elif file == 'dungeon_treasure.json':
                with open(os.path.join(script_dir, file), 'w') as f:
                    json.dump({'treasure': {'money': random.randint(200000, 1000000), 'items': []}}, f)
                print(f"✗ {file} did not exist in script directory, created with default treasure.")

def show_memory_patch():
    print('\n[SYS://VALUE_WRITE]')
    print('Target parameter detected.')
    print('> Initializing memory patch...')
    print('> Allocating sector...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Injecting payload...\n')
    time.sleep(round(random.uniform(0, 1.5), 2))
    current = 0
    while current < 100:
        increment = random.randint(5, 25)
        current = min(current + increment, 100)
        filled = current // 10
        bar = '■' * filled + '□' * (10 - filled)
        print(f'[{bar}] Writing {current}%')
        time.sleep(round(random.uniform(0, 1.5), 2))
    print('\n> Verifying integrity...')
    print('> Syncing with core bus...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Commit successful.')
    print('[✓] MEMORY CELL UPDATED \n')

def random_progress_bar():
    bar_current = 0
    while bar_current < 10:
        increment = random.randint(1, 3)
        bar_current = min(bar_current + increment, 10)
        yield bar_current

def show_game_reset():
    print('\n[SYS://GAME_RESET]')
    print('Critical system command received.')
    print('Action → full.reset\n')
    print('> Accessing core save-state...')
    print('> Validating reset permissions...')
    print('> Locking active runtime channels...\n')
    print('!! WARNING !!')
    print('This operation will erase ALL progress,')
    print('saved data, configurations, and user states.\n')
    print('> Initiating master-wipe protocol...\n')
    print('[RESET SEQUENCE]')
    current = 0
    messages = ['Purging player data...', 'Clearing inventory cache...', 'Resetting world matrices...', 'Annihilating progression logs...', 'Rebuilding base environment...', 'Restoring factory defaults...']
    msg_index = 0
    bar_gen = random_progress_bar()
    while current < 100:
        increment = random.randint(5, 25)
        current = min(current + increment, 100)
        try:
            filled = next(bar_gen)
        except StopIteration:
            filled = 10
        bar = '▓' * filled + '□' * (10 - filled)
        msg = messages[min(msg_index, len(messages) - 1)] if current < 100 else messages[-1]
        print(f'[{bar}] {current}%  → {msg}')
        time.sleep(0.05)
        if msg_index < len(messages) - 1 and random.random() < 0.3:
            msg_index += 1
    print('\n[RESET REPORT]')
    print(' • SCOPE       : entire game environment')
    print(' • EFFECT      : irreversible reset')
    print(' • DATA LOSS   : 100%')
    print(' • STATUS      : clean state restored\n')
    print('> Executing finalization steps...')
    print('   → Regenerating default config...OK')
    print('   → Restarting core engine........OK\n')
    print('[✓] FULL GAME RESET COMPLETE')

def show_account_purge(username):
    print('\n[SYS://ACCOUNT_PURGE]')
    print('High-security operation requested.')
    print('Action → delete.account')
    print('> Initializing identity module...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Verifying authorization token...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Syncing with user registry...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print()
    print('!! CRITICAL OPERATION WARNING !!')
    print('Target account flagged for full removal.')
    print()
    print('> Executing purge protocol...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Revoking linked credentials...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Dropping session keys...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Anonymizing residual metadata...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print()
    print('[DELETE REPORT]')
    print(f' • TARGET      : {username}')
    print(' • MODE        : irreversible purge')
    print(' • STATUS      : Complete')
    print(' • TRACE       : all identifiers wiped')
    print()
    print('> Finalizing cleanup...')
    print('   → Scrubbing data blocks.........OK')
    print('   → Flushing cache entries........OK')
    print('   → Seal-locking registry path....OK')
    print()
    print('[✓] ACCOUNT DELETED — NO RECOVERY')
    print()

def show_deluser(username):
    print('\n[SYS://DELUSER]')
    print('High-risk command received.')
    print('Action → delete.user')
    print('> Accessing user registry...')
    print('> Verifying authorization level...')
    print('> Locking target user profile...')
    print()
    print('!! WARNING !!')
    print('User deletion is irreversible.')
    print('All personal data, stats, sessions,')
    print('and identifiers will be permanently removed.')
    print()
    print('> Executing purge sequence...')
    print('> Revoking credentials...')
    print('> Erasing activity logs...')
    print('> Scrubbing metadata clusters...')
    print('> Removing account fingerprint...')
    print()
    print('[DELETE REPORT]')
    print(f' • TARGET      : {username}')
    print(' • STATUS      : purged')
    print(' • TRACE       : identifiers destroyed')
    print(' • EFFECT      : non-recoverable deletion')
    print()
    print('> Performing cleanup...')
    print('   → Flushing registry cache.......OK')
    print('   → Closing orphaned handles......OK')
    print('   → Re-sealing registry path......OK')
    print()
    print('[✓] USER DELETED — NO POSSIBLE RECOVERY')
    print()

def show_adduser(username):
    print('\n[SYS://ADDUSER]')
    print('Operation request acknowledged.')
    print('Action → create.user')
    print('> Initializing identity module...')
    print('> Verifying creation permissions...')
    print('> Allocating registry slot...')
    print('> Generating user credentials...')
    print('> Assigning unique identifier...')
    print('> Building default profile structure...')
    print('> Registering access keys...')
    print()
    print('[CREATION REPORT]')
    print(f' • TARGET      : {username}')
    print(' • STATUS      : successfully created')
    print(' • PROFILE     : baseline configuration applied')
    print(' • SECURITY    : encrypted & verified')
    print()
    print('> Finalizing setup...')
    print('   → Syncing with user registry......OK')
    print('   → Sealing credential block........OK')
    print('   → Activating account modules......OK')
    print()
    print('[✓] USER ADDED SUCCESSFULLY')
    print()

def collect_user_database():
    print('\n[SYS://USERDB_COLLECT]')
    print('Operation request acknowledged.')
    print('Action → collect.user_database')
    print()
    print('> Initializing data-scan module...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Establishing secure link to registry...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Parsing account index...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print()
    print('> Harvesting identifiers...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Extracting metadata clusters...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Aggregating session records...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Compiling unified dataset...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print()
    print('[COLLECTION REPORT]')
    print(' • SOURCE      : global user registry')
    print(' • RECORDS     : synchronized')
    print(' • STATUS      : compilation complete')
    print(' • SECURITY    : all channels encrypted')
    print()
    print('> Finalizing dataset...')
    print('   → Validating checksum............OK')
    print('   → Encrypting storage block.......OK')
    print('   → Sealing access path............OK')
    print()
    print('[✓] USER DATABASE SUCCESSFULLY COLLECTED')
    print()

def simulate_cmd_execution(command, success=True):
    print('\n[SYS://CMD_EXECUTE]')
    print('Operation request received.')
    print(f'Command → {command}')
    initial_step_pool = ['Initializing execution layer...', 'Linking runtime channels...', 'Dispatching opcode...', 'Allocating resources...', 'Establishing secure connection...', 'Loading command modules...', 'Verifying command syntax...', 'Preparing execution environment...', 'Synchronizing subsystems...', 'Activating protocol handler...']
    steps = random.sample(initial_step_pool, 3)
    for step in steps:
        print(f'> {step}')
        time.sleep(round(random.uniform(0, 0.5), 2))
    if success:
        success_pool = ['Validating instruction set...', 'Performing integrity checks...', 'Scanning for anomalies...', 'Executing safety protocols...', 'Confirming resource availability...']
        success_steps = random.sample(success_pool, random.randint(2, 4))
        for step in success_steps:
            print(f'> {step}')
            time.sleep(round(random.uniform(0, 0.5), 2))
        print('> All checks passed.')
        print('> No anomalies detected.')
        print('> Executing protected routine...')
        print()
        print('[SUCCESS REPORT]')
        code = f'0x{random.randint(0, 255):02X}-OK'
        module = f"/core/{command.replace('.', '/').replace(' ', '_')}.axl"
        result_pool = ['Operation completed', 'Task executed', 'Command processed', 'Routine finished', 'Action successful']
        result = random.choice(result_pool)
        status_pool = ['Stable', 'Nominal', 'Operational', 'Secure', 'Verified']
        status = random.choice(status_pool)
        print(f' • CODE        : {code}')
        print(f' • MODULE      : {module}')
        print(f' • RESULT      : {result}')
        print(f' • STATUS      : {status}')
        print()
        print('> Finalizing process...')
        final_step_pool = ['Committing changes', 'Syncing with core bus', 'Updating state registers', 'Saving configuration', 'Releasing resources', 'Logging execution', 'Clearing temporary data']
        final_steps = random.sample(final_step_pool, 3)
        for step in final_steps:
            print(f'   → {step}...........OK')
            time.sleep(round(random.uniform(0, 0.5), 2))
        print()
        print('[✓] COMMAND EXECUTED SUCCESSFULLY')
    else:
        print()
        print('!! ERROR DETECTED !!')
        command_parts = command.split('.')
        base_cmd = command_parts[0] if command_parts else command
        error_base = [f'Exec-channel integrity failure during {base_cmd}', f'Opcode rejected by secure gate for {command}', f'Memory allocation failure in {base_cmd} module', f'Permission denied for {command} execution', f'Invalid instruction sequence in {base_cmd}', f'System overload detected by {command}', f'Security breach attempt via {command}', f'Resource conflict with {base_cmd} command']
        reason_desc = random.choice(error_base)
        print(f'> {reason_desc}')
        if random.random() < 0.5:
            print('> Integrity check failed')
        if random.random() < 0.3:
            print('> System anomaly detected')
        print()
        print('[FAIL REPORT]')
        code = f'0x{random.randint(16384, 65535):04X}-CMDFAIL'
        location = f"/core/{command.replace('.', '/').replace(' ', '_')}.axl"
        reason_pool = [f'Unsafe {command} sequence', f'Access violation in {base_cmd}', f'Resource exhaustion by {command}', f'Invalid parameters for {command}', f'Command {command} not recognized', f'Dependency failure for {command}']
        reason = random.choice(reason_pool)
        status_pool = ['Immediate abort', 'Forced termination', 'Error halt', 'Critical failure', 'System halt']
        status = random.choice(status_pool)
        print(f' • CODE        : {code}')
        print(f' • LOCATION    : {location}')
        print(f' • REASON      : {reason}')
        print(f' • STATUS      : {status}')
        print()
        print('> Initiating rollback...')
        rollback_step_pool = ['Flushing partial writes', 'Restoring snapshot', 'Stabilizing core bus', 'Reverting changes', 'Clearing error state', 'Logging failure']
        rollback_steps = random.sample(rollback_step_pool, 3)
        for step in rollback_steps:
            print(f'   → {step}...........OK')
            time.sleep(round(random.uniform(0, 0.5), 2))
        print()
        print('[✖] COMMAND FAILED — SYSTEM SAFE')
    print()

def get_machine_id():
    """Get a unique identifier for this machine"""
    try:
        hostname = socket.gethostname()
        import platform
        system = platform.system()
        machine = platform.machine()
        return f'{hostname}_{system}_{machine}'
    except:
        return 'unknown_machine'
MAX_LEVEL = 1500
AREAS_COUNT = 100
LEVELS_PER_AREA = MAX_LEVEL // AREAS_COUNT

def level_to_area(level):
    if level < 1:
        level = 1
    area = (level - 1) // LEVELS_PER_AREA + 1
    if area > AREAS_COUNT:
        area = AREAS_COUNT
    return area

def exp_to_next(level):
    if level >= MAX_LEVEL:
        return float('inf')
    base_exp = 100
    growth_factor = 1.25
    return int(base_exp * level ** 1.5 * growth_factor ** (level - 1))

def create_exp_bar(current_exp, next_exp):
    if next_exp == 'MAX':
        return '[██████████] MAX LEVEL'
    bar_length = 10
    if next_exp > 0:
        progress = min(current_exp / next_exp, 1.0)
        filled = int(progress * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        percentage = int(progress * 100)
        return f'[{bar}] {percentage}%'
    return '[░░░░░░░░░░] 0%'

def grant_exp(username, amount):
    try:
        user_data = load_user_data(username)
        if not user_data:
            return 0
        player_data = user_data.get('player_data', {})
        stats = player_data['stats']
        lvls_gained = []
        granted = amount
        if stats.get('level', 1) >= MAX_LEVEL:
            return granted
        exp_boost = stats.get('perm_exp_boost', 0)
        title_exp_boost = stats.get('title_exp_boost', 0)
        total_exp_boost = exp_boost + title_exp_boost
        if total_exp_boost > 0:
            boosted_amount = round(amount * (total_exp_boost / 100.0))
            print(f'Experience boost applied! +{boosted_amount} bonus EXP')
            granted += boosted_amount
        stats['exp'] = stats.get('exp', 0) + granted
        old_title = stats.get('title')
        while stats['level'] < MAX_LEVEL and stats['exp'] >= exp_to_next(stats['level']):
            req = exp_to_next(stats['level'])
            stats['exp'] -= req
            old_level = stats['level']
            stats['level'] += 1
            hp_increase = 10
            atk_increase = 1 + stats['level'] // 5
            mana_increase = 10
            stats['max_dodge'] = min(10, stats.get('max_dodge', 3) + 1)
            default_stats = default_player_data()['stats']
            if not stats['stats_manually_set']['hp_max']:
                stats['hp_max'] = stats.get('hp_max', 10) + hp_increase
            if not stats['stats_manually_set']['hp']:
                stats['hp'] = min(stats.get('hp', stats['hp_max']) + stats['hp_max'] // 4, stats['hp_max'])
            if not stats['stats_manually_set']['atk']:
                stats['atk'] = stats.get('atk', 10) + atk_increase
            if not stats['stats_manually_set']['mana_max']:
                stats['mana_max'] = stats.get('mana_max', 10) + mana_increase
            if not stats['stats_manually_set']['mana']:
                stats['mana'] = min(stats.get('mana', stats['mana_max']) + stats['mana_max'] // 3, stats['mana_max'])
            if not stats['stats_manually_set']['defense']:
                stats['defense'] = stats.get('defense', 10) + 1
            lvls_gained.append(stats['level'])
            print(f"You leveled up to level {stats['level']}!")
        player_data['stats'] = stats
        user_data['player_data'] = player_data
        save_user_data(username, user_data)
        apply_permanent_upgrades(username)
        auto_equip_items(username)
        auto_equip_spells(username)
    except Exception as e:
        print(f'Error granting experience: {e}')
        return 0
    return granted
def check_stats(username):
    """Check if user has negative HP or Mana, and reset to max if so"""
    try:
        user_data = load_user_data(username)
        if not user_data:
            return
        player_data = user_data.get('player_data', {})
        stats = player_data.get('stats', {})
        hp_max = stats.get('hp_max', 100)
        mana_max = stats.get('mana_max', 50)
        hp = stats.get('hp', hp_max)
        mana = stats.get('mana', mana_max)
        changed = False
        if hp < 1:
            stats['hp'] = hp_max
            changed = True
            print(f'HP was negative, reset to {hp_max}.')
        if mana < 1:
            stats['mana'] = mana_max
            changed = True
            print(f'Mana was negative, reset to {mana_max}.')
        if changed:
            player_data['stats'] = stats
            user_data['player_data'] = player_data
            save_user_data(username, user_data)
    except Exception as e:
        print(f'Error checking stats: {e}')

def add_material_drops(inventory, monster):
    """Add material drops from a monster to the inventory and return list of dropped items"""
    dropped = []
    if 'drop' in monster:
        for item, chance in monster['drop'].items():
            if random.random() < chance:
                inventory[item] = inventory.get(item, 0) + 1
                dropped.append(item)
    return dropped

def debug_console(current_user, score, money, player_data, USERS_DIR):
    debugconsoleaccess = 'accepted' if current_user == 'tester01' else None
    if current_user != 'tester01':
        adminQ = input("When is the game developer's bestfriends BOD?: ")
        if adminQ in adminQanswers:
            print('Access Accepted')
            debugconsoleaccess = 'accepted'
        else:
            print('Access Denied')
            debugconsoleaccess = 'denied'
    if debugconsoleaccess != 'denied':
        print('[BOOTSEQ://DEBUG_CONSOLE]')
        time.sleep(round(random.uniform(0, 1.5), 2))
        print('→ Linking subsystems...')
        time.sleep(round(random.uniform(0, 1.5), 2))
        print('→ Bypassing safety locks...')
        time.sleep(round(random.uniform(0, 1.5), 2))
        print('→ Syncing I/O...')
        time.sleep(round(random.uniform(0, 1.5), 2))
        print(':: DEBUG MODE ENGAGED ::')
    while True:
        if debugconsoleaccess == 'denied':
            break
        else:
            pass
        command_executed = False
        success = False
        cmd = input('>> ').strip().lower().split(' ', 1)
        cmd_base = cmd[0] if cmd else ''
        args = cmd[1] if len(cmd) > 1 else ''
        if cmd_base == 'help' or cmd_base == 'h' or cmd_base == '?':
            command_executed = True
            success = True
            print('\n--- Debug Commands ---')
            print('users - display all registered users (limited info)')
            print('current - display current user and score')
            print('numbers - display generated random numbers (if any)')
            print('play - play the number guessing game')
            print('adduser <u> <p> - create a new user account with password')
            print('deluser <u> - delete a user account')
            print('reset - reset all users and highscores')
            print('resetplayer <u> - reset a single user to default stats')
            print('setdmoney <n> - set dungeon treasure amount to n')
            print("setscore <u> <n> - set a user's score to n")
            print("setmoney <u> <n> - set a user's money to n")
            print("setexp <u> <n> - set a user's experience to n")
            print("setlvl <u> <n> - set a user's level to n")
            print("set <u> <stat> <n> - set a user's stat to n (hp, mana, atk, def, etc.)")
            print('showfull <u> - display full data for user u')
            print('give <u> <item> [qty] - grant an item to user (saves automatically)')
            print(' (items: potion, strong_potion, ultra_potion, etc.)')
            print(' (upgrades: perm_strength_upgrade, perm_defense_upgrade, etc.)')
            print(' (aliases: str, def, hp, mana, crit, etc.)')
            print('ruinthefun(username) - grant all achievements, items (500x usable), max stats')
            print("setdodge <u> <n> - set a user's dodge points to n")
            print('exit - close debug console')
            print('-----------------------\n')
        elif cmd_base == 'users' or cmd_base == 'usrs' or cmd_base == 'u':
            command_executed = True
            success = True
            leaderboard = get_leaderboard()
            simulate_cmd_execution('users', success=True)
            time.sleep(round(random.uniform(2, 5), 2))
            collect_user_database()
            print('\n--- Top 10 Users ---')
            for uname, uscore in leaderboard:
                user_data = load_user_data(uname)
                umoney = user_data.get('money', 0) if user_data else 0
                print(f'{uname}: Score {uscore}, Money ${umoney}')
            print('---\n')
        elif cmd_base == 'current' or cmd_base == 'curr' or cmd_base == 'c':
            command_executed = True
            if current_user:
                success = True
                print(f'Current user: {current_user}, Score: {score}, Money: ${money}')
            else:
                success = False
                print('No current user logged in.')
            simulate_cmd_execution('current', success=success)
            if success:
                show_memory_patch()
                time.sleep(round(random.uniform(2, 5), 2))
                collect_user_database()
        elif cmd_base == 'play':
            command_executed = True
            if current_user:
                simulate_cmd_execution('play number guessing game', success=success)
                score = guessing_game(current_user, score)
                success = True
                print(f'Game over. Updated score: {score}')
            else:
                success = False
                print('No current user logged in.')
            if success:
                show_memory_patch()
        elif cmd_base == 'numbers':
            command_executed = True
            success = True
            print('Random numbers generated this session: (not tracked)')
            simulate_cmd_execution('numbers', success=True)
            show_memory_patch()
        elif cmd_base == 'adduser':
            command_executed = True
            if args:
                parts = args.split(' ', 1)
                if len(parts) == 2:
                    u, p = parts
                    if signup(u, p):
                        success = True
                        show_adduser(u)
                    else:
                        success = False
                        print('Failed to create user.')
                else:
                    success = False
                    print('Usage: adduser <username> <password>')
            else:
                success = False
                print('Usage: adduser <username> <password>')
            simulate_cmd_execution('adduser', success=success)
        elif cmd_base == 'deluser':
            command_executed = True
            if args:
                u = args.strip()
                users = load_all_users()
                if u in users:
                    del users[u]
                    save_all_users(users)
                    success = True
                    show_deluser(u)
                else:
                    success = False
                    print('User not found.')
            else:
                success = False
                print('Usage: deluser <username>')
            simulate_cmd_execution('deluser', success=success)
        elif cmd_base == 'reset':
            command_executed = True
            success = True
            save_all_users({})
            print('All users reset.')
            simulate_cmd_execution('reset', success=success)
        elif cmd_base == 'resetplayer':
            command_executed = True
            if args:
                u = args.strip()
                user_data = load_user_data(u)
                if user_data:
                    print('\n[SYS://ACCOUNT_RESET]')
                    print('High-security operation detected.')
                    print('Action → reset.account')
                    print('> Initializing identity module...')
                    print('> Verifying authorization token...')
                    print('> Syncing with user registry...')
                    print()
                    print('!! CRITICAL OPERATION WARNING !!')
                    print('Target account flagged for full removal.')
                    print()
                    print('> Executing purge protocol...')
                    print('> Revoking linked credentials...')
                    print('> Dropping session keys...')
                    print('> Anonymizing residual metadata...')
                    print()
                    print('[DELETE REPORT]')
                    print(f' • TARGET      : {u}')
                    print(' • MODE        : irreversible purge')
                    print(' • STATUS      : Complete')
                    print(' • TRACE       : all identifiers wiped')
                    print()
                    print('> Finalizing cleanup...')
                    print('   → Scrubbing data blocks.........OK')
                    print('   → Flushing cache entries........OK')
                    print('   → Seal-locking registry path....OK')
                    print()
                    print('[✓] ACCOUNT DELETED — NO RECOVERY')
                    print()
                    show_memory_patch()
                    player_data = default_player_data()
                    user_data['score'] = 0
                    user_data['money'] = 40
                    user_data['player_data'] = player_data
                    save_user_data(u, user_data)
                    success = True
                    print(f'Player {u} reset to defaults.')
                else:
                    success = False
                    print('User not found.')
            else:
                success = False
                print('Usage: resetplayer <username>')
            simulate_cmd_execution('resetplayer', success=success)
            if success:
                show_memory_patch()
        elif cmd_base == 'setdmoney':
            command_executed = True
            success = False
            if args:
                try:
                    global dungeon_treasure
                    dungeon_treasure = int(args.strip())
                    save_dungeon_treasure()
                    print(f'Dungeon treasure set to ${dungeon_treasure}')
                    success = True
                except ValueError:
                    print('Invalid number.')
            else:
                print('Usage: setdmoney <n>')
            simulate_cmd_execution('setdmoney', success=success)
            if success:
                show_memory_patch()
        elif cmd_base == 'setscore':
            command_executed = True
            if args:
                parts = args.split(' ', 1)
                if len(parts) == 2:
                    u, n = parts
                    try:
                        n = int(n)
                        user_data = load_user_data(u)
                        if user_data:
                            user_data['score'] = n
                            save_user_data(u, user_data)
                            success = True
                            print(f'Score for {u} set to {n}.')
                        else:
                            success = False
                            print('User not found.')
                    except ValueError:
                        success = False
                        print('Invalid score.')
                else:
                    success = False
                    print('Usage: setscore <username> <score>')
            else:
                success = False
                print('Usage: setscore <username> <score>')
            simulate_cmd_execution('setscore', success=success)
        elif cmd_base == 'setmoney':
            command_executed = True
            success = False
            if args:
                parts = args.split(' ', 1)
                if len(parts) == 2:
                    u, n = parts
                    try:
                        n = int(n)
                        user_data = load_user_data(u)
                        if user_data:
                            user_data['money'] = n
                            save_user_data(u, user_data)
                            print(f'Money for {u} set to ${n}.')
                            success = True
                        else:
                            print('User not found.')
                    except ValueError:
                        print('Invalid money.')
                else:
                    print('Usage: setmoney <username> <money>')
            else:
                print('Usage: setmoney <username> <money>')
            simulate_cmd_execution('setmoney', success=success)
            if success:
                show_memory_patch()
        elif cmd_base == 'setexp':
            command_executed = True
            if args:
                parts = args.split(' ', 1)
                if len(parts) == 2:
                    u, n = parts
                    try:
                        n = int(n)
                        user_data = load_user_data(u)
                        if user_data:
                            user_data['player_data']['stats']['exp'] = n
                            save_user_data(u, user_data)
                            success = True
                            print(f'EXP for {u} set to {n}.')
                        else:
                            success = False
                            print('User not found.')
                    except ValueError:
                        success = False
                        print('Invalid EXP.')
                else:
                    success = False
                    print('Usage: setexp <username> <exp>')
            else:
                success = False
                print('Usage: setexp <username> <exp>')
            simulate_cmd_execution('setexp', success=success)
        elif cmd_base == 'setlvl':
            command_executed = True
            if args:
                parts = args.split(' ', 1)
                if len(parts) == 2:
                    u, n = parts
                    try:
                        n = int(n)
                        user_data = load_user_data(u)
                        if user_data:
                            user_data['player_data']['stats']['level'] = n
                            save_user_data(u, user_data)
                            success = True
                            print(f'Level for {u} set to {n}.')
                        else:
                            success = False
                            print('User not found.')
                    except ValueError:
                        success = False
                        print('Invalid level.')
                else:
                    success = False
                    print('Usage: setlvl <username> <level>')
            else:
                success = False
                print('Usage: setlvl <username> <level>')
            simulate_cmd_execution('setlvl', success=success)
            if success:
                show_memory_patch()
        elif cmd_base == 'setdefeated':
            command_executed = True
            success = False
            if args:
                parts = args.split(' ', 2)
                if len(parts) == 3:
                    u, typ, n = parts
                    try:
                        n = int(n)
                        user_data = load_user_data(u)
                        if user_data:
                            stats = user_data['player_data']['stats']
                            if typ.lower() in ['monsters', 'monster']:
                                stats['monsters_defeated'] = n
                            elif typ.lower() in ['bosses', 'boss']:
                                stats['bosses_defeated'] = n
                            else:
                                print(f'Invalid type: {typ}')
                            success = True
                            save_user_data(u, user_data)
                            print(f'{typ} defeated for {u} set to {n}.')
                        else:
                            print('User not found.')
                    except ValueError:
                        print('Invalid number.')
                else:
                    print('Usage: setdefeated <username> <type> <n>')
            else:
                print('Usage: setdefeated <username> <type> <n>')
            simulate_cmd_execution('setdefeated', success=success)
            if success:
                show_memory_patch()
        elif cmd_base == 'set':
            command_executed = True
            if args:
                parts = args.split(' ', 2)
                if len(parts) == 3:
                    u, stat, n = parts
                    try:
                        n = int(n)
                        user_data = load_user_data(u)
                        if user_data:
                            stats = user_data['player_data']['stats']
                            if stat in stats:
                                stats[stat] = n
                                save_user_data(u, user_data)
                                success = True
                                print(f'{stat} for {u} set to {n}.')
                            else:
                                success = False
                                print(f'Invalid stat: {stat}')
                        else:
                            success = False
                            print('User not found.')
                    except ValueError:
                        success = False
                        print('Invalid number.')
                else:
                    success = False
                    print('Usage: set <username> <stat> <n>')
            else:
                success = False
                print('Usage: set <username> <stat> <n>')
            simulate_cmd_execution('set', success=success)
            if success == True:
                show_memory_patch()
        elif cmd_base == 'showfull':
            command_executed = True
            collect_user_database()
            if args:
                u = args.strip()
                user_data = load_user_data(u)
                if user_data:
                    success = True
                    simulate_cmd_execution('showfull', success=success)
                    player_data = user_data.get('player_data', {})
                    print(f'\nFull data for {u}:')
                    for key, value in player_data.items():
                        if isinstance(value, dict):
                            print(f'{key}:')
                            for subkey, subvalue in value.items():
                                print(f'  {subkey}: {subvalue}')
                        else:
                            print(f'{key}: {value}')
                    print('---')
                else:
                    success = False
                    print('User not found.')
            else:
                success = False
                print('Usage: showfull <username>')
        elif cmd_base == 'give':
            command_executed = True
            success = False
            if args:
                parts = args.split(' ', 2)
                if len(parts) >= 2:
                    u, item = (parts[0], parts[1])
                    qty_str = parts[2] if len(parts) > 2 else '1'
                    try:
                        qty = int(qty_str)
                        if qty < 1:
                            qty = 1
                        upgrade_aliases = {'str': 'perm_strength_upgrade', 'def': 'perm_defense_upgrade', 'hp': 'perm_health_upgrade', 'mana': 'perm_mana_upgrade', 'crit': 'perm_crit_chance_upgrade', 'magic_def': 'perm_magic_def_upgrade', 'lifesteal': 'perm_lifesteal_upgrade', 'lifesteal_chance': 'perm_lifesteal_chance_upgrade', 'exp': 'perm_exp_upgrade', 'perm_str': 'perm_strength_upgrade', 'perm_def': 'perm_defense_upgrade', 'perm_hp': 'perm_health_upgrade', 'perm_mana': 'perm_mana_upgrade', 'perm_crit': 'perm_crit_chance_upgrade', 'perm_magic_def': 'perm_magic_def_upgrade', 'perm_lifesteal': 'perm_lifesteal_upgrade', 'perm_lifesteal_chance': 'perm_lifesteal_chance_upgrade', 'perm_exp': 'perm_exp_upgrade'}
                        if item in upgrade_aliases:
                            item = upgrade_aliases[item]
                        user_data = load_user_data(u)
                        if user_data:
                            inventory = user_data['player_data'].get('inventory', {})
                            inventory[item] = inventory.get(item, 0) + qty
                            user_data['player_data']['inventory'] = inventory
                            save_user_data(u, user_data)
                            success = True
                            simulate_cmd_execution('give', success=success)
                            print(f'Gave {qty}x {item} to {u}.')
                        else:
                            print('User not found.')
                    except ValueError:
                        print('Invalid quantity. Quantity must be a positive integer.')
                else:
                    print('Usage: give <username> <item> [qty]')
            else:
                print('Usage: give <username> <item> [qty]')
            if success:
                show_memory_patch()
        elif cmd_base == 'setdodge':
            command_executed = True
            success = False
            if args:
                parts = args.split(' ', 1)
                if len(parts) == 2:
                    u, n = parts
                    try:
                        n = int(n)
                        user_data = load_user_data(u)
                        if user_data:
                            user_data['player_data']['stats']['dodge_points'] = n
                            user_data['player_data']['stats']['max_dodge'] = n
                            save_user_data(u, user_data)
                            print(f'Dodge points for {u} set to {n}.')
                            success = True
                        else:
                            print('User not found.')
                    except ValueError:
                        print('Invalid number.')
                else:
                    print('Usage: setdodge <username> <n>')
            else:
                print('Usage: setdodge <username> <n>')
            simulate_cmd_execution('setdodge', success=success)
        elif cmd_base == 'ruinthefun' or (cmd_base.startswith('ruinthefun(') and cmd_base.endswith(')')):
            command_executed = True
            if cmd_base.startswith('ruinthefun(') and cmd_base.endswith(')'):
                u = cmd_base[11:-1]
            elif args:
                u = args.strip()
            else:
                success = False
                print('Usage: ruinthefun(username)')
                simulate_cmd_execution('ruinthefun', success=False)
                continue
            user_data = load_user_data(u)
            if user_data:
                success = True
                player_data = user_data['player_data']
                stats = player_data['stats']
                inventory = player_data['inventory']
                stats['level'] = MAX_LEVEL
                stats['exp'] = exp_to_next(MAX_LEVEL) - 1
                stats['hp_max'] = 1000
                stats['mana_max'] = 500
                stats['atk'] = 100
                stats['defense'] = 50
                stats['perm_atk'] = 50
                stats['perm_def'] = 25
                stats['perm_hp_max'] = 500
                stats['perm_mana_max'] = 250
                stats['perm_crit_chance'] = 50
                stats['perm_mana_regen'] = 20
                stats['perm_lifesteal'] = 20
                stats['perm_lifesteal_chance'] = 20
                stats['perm_exp_boost'] = 50
                stats['achievements'] = list(ACHIEVEMENTS.keys())
                stats['available_titles'] = list(TITLES.keys())
                stats['equipped_titles'] = list(TITLES.keys())
                inventory['potion'] = 500
                inventory['strong_potion'] = 500
                inventory['ultra_potion'] = 500
                inventory['mana_regen_potion'] = 500
                inventory['instant_mana'] = 500
                inventory['strength_boost'] = 500
                inventory['defense_boost'] = 500
                inventory['regen_potion'] = 500
                inventory['crit_boost'] = 500
                inventory['mana_upgrade_potion'] = 500
                for eq in [WEAPONS, ARMORS, WANDS, ROBES, NECKLACES]:
                    for item in eq:
                        inventory[item] = 1
                for mat in MATERIALS:
                    inventory[mat] = 500
                for up in PERM_UPGRADES:
                    inventory[up] = 250
                for mp in MAGIC_PACKS:
                    inventory[mp] = 500
                apply_title_boosts(u)
                user_data['score'] = 1000000
                user_data['money'] = 1000000
                save_user_data(u, user_data)
                print(f'Ruin the fun activated for {u}.')
            else:
                success = False
                print('User not found.')
            simulate_cmd_execution('ruinthefun', success=success)
            if success == True:
                show_memory_patch()
        elif cmd_base in ['exit', '.', 'dilsaf', 'get out', 'getout', 'out', 'quit']:
            command_executed = True
            success = True
            print('Exiting debug console.')
            break
        else:
            command_executed = True
            success = False
            print("Unknown command. Type 'help' for commands.")

adminQanswers = ['31,10,2011', '31\x08\x811', '31/10/2011', '31.10.2011']