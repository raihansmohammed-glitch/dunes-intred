import json
import random
import os
import math
import time
import atexit
import threading
import socket
import misc
import other_functions
import dungeon_functions

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
    time.sleep(round(random.uniform(0, 1.5), 2))
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

def get_rarity_value(rarity):
    """Get numerical value for rarity sorting"""
    rarity_order = {'common': 1, 'rare': 2, 'mythical': 3, 'prismatic': 4, 'divine': 5, 'transcendent': 6}
    return rarity_order.get(rarity, 0)

def get_item_rarity(item_key):
    """Get the rarity of an item"""
    if item_key in misc.WEAPONS:
        if 'score_price' in misc.WEAPONS[item_key]:
            if misc.WEAPONS[item_key].get('score_price', 0) >= 10000:
                return 'transcendent'
            elif misc.WEAPONS[item_key].get('score_price', 0) >= 3000:
                return 'divine'
            elif misc.WEAPONS[item_key].get('score_price', 0) >= 800:
                return 'prismatic'
            elif misc.WEAPONS[item_key].get('score_price', 0) >= 250:
                return 'mythical'
            elif misc.WEAPONS[item_key].get('score_price', 0) >= 200:
                return 'rare'
            else:
                return 'common'
        elif item_key in ['infinitium_sword']:
            return 'transcendent'
        elif item_key in ['cosmic_blade', 'transcendent_edge']:
            return 'divine'
        elif item_key in ['dragon_slayer', 'holy_avenger', 'thunder_sword', 'flameblade']:
            return 'prismatic'
        elif item_key in ['frostblade']:
            return 'mythical'
        else:
            return 'common'
    elif item_key in misc.ARMORS:
        if 'score_price' in misc.ARMORS[item_key]:
            if misc.ARMORS[item_key].get('score_price', 0) >= 9500:
                return 'transcendent'
            elif misc.ARMORS[item_key].get('score_price', 0) >= 2800:
                return 'divine'
            elif misc.ARMORS[item_key].get('score_price', 0) >= 1400:
                return 'prismatic'
            elif misc.ARMORS[item_key].get('score_price', 0) >= 700:
                return 'mythical'
            elif misc.ARMORS[item_key].get('score_price', 0) >= 200:
                return 'rare'
            else:
                return 'common'
        elif item_key in ['infinitium_armor']:
            return 'transcendent'
        elif item_key in ['cosmic_armor', 'transcendent_armor']:
            return 'divine'
        elif item_key in ['dragon_scale_armor', 'holy_armor', 'thunder_armor', 'flame_armor']:
            return 'prismatic'
        elif item_key in ['frost_armor']:
            return 'mythical'
        else:
            return 'common'
    elif item_key in misc.WANDS:
        if 'score_price' in misc.WANDS[item_key]:
            if misc.WANDS[item_key].get('score_price', 0) >= 9500:
                return 'transcendent'
            elif misc.WANDS[item_key].get('score_price', 0) >= 2800:
                return 'divine'
            elif misc.WANDS[item_key].get('score_price', 0) >= 1400:
                return 'prismatic'
            elif misc.WANDS[item_key].get('score_price', 0) >= 700:
                return 'mythical'
            elif misc.WANDS[item_key].get('score_price', 0) >= 200:
                return 'rare'
            else:
                return 'common'
        elif item_key in ['transcendent_staff']:
            return 'transcendent'
        elif item_key in ['cosmic_scepter']:
            return 'divine'
        elif item_key in ['dragon_staff', 'holy_scepter', 'thunder_wand', 'flame_wand']:
            return 'prismatic'
        elif item_key in ['frost_wand']:
            return 'mythical'
        elif item_key in ['archmage_staff']:
            return 'rare'
        else:
            return 'common'
    elif item_key in misc.ROBES:
        if 'score_price' in misc.ROBES[item_key]:
            if misc.ROBES[item_key].get('score_price', 0) >= 9500:
                return 'transcendent'
            elif misc.ROBES[item_key].get('score_price', 0) >= 2800:
                return 'divine'
            elif misc.ROBES[item_key].get('score_price', 0) >= 1400:
                return 'prismatic'
            elif misc.ROBES[item_key].get('score_price', 0) >= 700:
                return 'mythical'
            elif misc.ROBES[item_key].get('score_price', 0) >= 200:
                return 'rare'
            else:
                return 'common'
        elif item_key in ['transcendent_robe']:
            return 'transcendent'
        elif item_key in ['cosmic_robe']:
            return 'divine'
        elif item_key in ['dragon_robe', 'holy_robe', 'thunder_robe', 'flame_robe']:
            return 'prismatic'
        elif item_key in ['frost_robe']:
            return 'mythical'
        elif item_key in ['void_robe']:
            return 'rare'
        else:
            return 'common'
    elif item_key in misc.NECKLACES:
        if 'score_price' in misc.NECKLACES[item_key]:
            if misc.NECKLACES[item_key].get('score_price', 0) >= 8000:
                return 'transcendent'
            elif misc.NECKLACES[item_key].get('score_price', 0) >= 2400:
                return 'divine'
            elif misc.NECKLACES[item_key].get('score_price', 0) >= 1200:
                return 'prismatic'
            elif misc.NECKLACES[item_key].get('score_price', 0) >= 600:
                return 'mythical'
            elif misc.NECKLACES[item_key].get('score_price', 0) >= 100:
                return 'rare'
            else:
                return 'common'
        elif item_key in ['transcendent_necklace']:
            return 'transcendent'
        elif item_key in ['cosmic_necklace']:
            return 'divine'
        elif item_key in ['dragon_necklace', 'holy_pendant', 'thunder_necklace', 'flame_necklace']:
            return 'prismatic'
        elif item_key in ['frost_necklace']:
            return 'mythical'
        else:
            return 'common'
    elif item_key in misc.POTIONS:
        return 'common'
    elif item_key in misc.PERM_UPGRADES:
        return 'rare'
    elif item_key in misc.MATERIALS:
        return misc.MATERIALS[item_key]['rarity']
    else:
        return 'common'
def get_title(level, achievements=None):
    if achievements is None:
        achievements = []
    level_title = 'Novice'
    if level <= 10:
        level_title = 'Novice'
    elif level <= 20:
        level_title = 'Apprentice'
    elif level <= 30:
        level_title = 'Warrior'
    elif level <= 40:
        level_title = 'Champion'
    elif level <= 50:
        level_title = 'Legend'
    elif level <= 60:
        level_title = 'Master'
    elif level <= 70:
        level_title = 'Grandmaster'
    elif level <= 80:
        level_title = 'Mythic'
    elif level <= 99:
        level_title = 'Transcendent'
    else:
        level_title = 'Godlike'
    best_achievement_title = None
    for ach_key in achievements:
        if ach_key in misc.ACHIEVEMENTS:
            ach_title = misc.ACHIEVEMENTS[ach_key]['title']
            title_priority = {'Slayer': 1, 'Hunter': 2, 'Slayer II': 3, 'Boss Slayer': 4, 'Boss Master': 5, 'Millionaire': 6, 'Arcane Master': 7, 'Artisan': 8, 'Collector': 9, 'Immortal': 10, 'Perfect': 11, 'Legendary': 12, 'Deity': 13, 'Treasure King': 14, "Fortune's Favorite": 15}
            if best_achievement_title is None or title_priority.get(ach_title, 0) > title_priority.get(best_achievement_title, 0):
                best_achievement_title = ach_title
    return best_achievement_title if best_achievement_title else level_title

def check_achievements(username):
    try:
        user_data = load_user_data(username)
        if not user_data:
            return []
        player_data = user_data.get('player_data', {})
        stats = player_data.get('stats', {})
        unlocked = stats.get('achievements', [])
        new_achievements = []
        for ach_key in misc.ACHIEVEMENTS:
            achievement = misc.ACHIEVEMENTS[ach_key]
        if ach_key not in unlocked and achievement['condition'](stats):
            unlocked.append(ach_key)
            new_achievements.append(ach_key)
            print(f"🏆 Achievement Unlocked: {achievement['name']} - '{achievement['title']}'!")
            print(f" {achievement['desc']}")
        if new_achievements:
            stats['achievements'] = unlocked
            old_title = stats.get('title')
            new_title = get_title(stats.get('level', 1), unlocked)
            if new_title != old_title:
                stats['title'] = new_title
                title_key = None
                for k, v in misc.misc.TITLES.items():
                    if v['name'] == new_title:
                        title_key = k
                        break
                if title_key and title_key not in stats.get('available_titles', []):
                    stats['available_titles'].append(title_key)
                print(f"🎉 New title unlocked: '{new_title}'!")
            player_data['stats'] = stats
            user_data['player_data'] = player_data
            save_user_data(username, user_data)
        return new_achievements
    except Exception as e:
        print(f'Error checking achievements: {e}')
        return []
MAX_LEVEL = 7500
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
    return lvls_gained

def save_all_data():
    dungeon_functions.save_dungeon_treasure()

def autosave():
    """Perform autosave and show a brief notification"""
    global last_autosave_time
    if save_all_data():
        last_autosave_time = time.time()
        print('\n💾 Game auto-saved!')
    else:
        print('\n⚠️ Autosave failed! Check console for details.')

def schedule_autosave():
    """Schedule the next autosave"""
    global autosave_timer
    if autosave_timer is not None:
        autosave_timer.cancel()
    autosave_timer = threading.Timer(misc.AUTOSAVE_INTERVAL, autosave)
    autosave_timer.daemon = True
    autosave_timer.start()
adminQanswers = ['31,10,2011', '31\x08\x811', '31/10/2011', '31.10.2011']

def stop_autosave():
    """Stop the autosave timer"""
    global autosave_timer
    if autosave_timer is not None:
        autosave_timer.cancel()
        autosave_timer = None

def setup_db():
    """Create users.txt file if it doesn't exist and migrate old data"""
    if os.path.isdir(misc.USERS_DIR):
        users = {}
        if os.path.exists('users'):
            for filename in os.listdir('users'):
                if filename.endswith('.json'):
                    username = filename[:-5]
                    with open(os.path.join('users', filename), 'r') as f:
                        users[username] = json.load(f)
        with open(misc.USERS_DIR, 'w') as f:
            json.dump(users, f, indent=4)
        import shutil
        shutil.rmtree('users')
    elif not os.path.exists(misc.USERS_DIR):
        with open(misc.USERS_DIR, 'w') as f:
            json.dump({}, f)

def load_all_users():
    """Load all user data from users.txt"""
    if not os.path.exists(misc.USERS_DIR):
        return {}
    try:
        with open(misc.USERS_DIR, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_all_users(users):
    """Save all user data to users.txt atomically with locking"""
    lock_file = misc.USERS_DIR + '.lock'
    try:
        while os.path.exists(lock_file):
            time.sleep(0.01)
        with open(lock_file, 'w') as f:
            f.write('')
        temp_file = misc.USERS_DIR + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump(users, f, indent=4)
        os.replace(temp_file, misc.USERS_DIR)
        return True
    except PermissionError as e:
        print(f'Save failed due to permission error: {e}. Data not saved.')
        return False
    except Exception as e:
        print(f'Save failed: {e}. Data not saved.')
        return False
    finally:
        try:
            os.remove(lock_file)
        except:
            pass

def load_user_data(username):
    """Load user data from the users dict"""
    users = load_all_users()
    return users.get(username)

def save_user_data(username, user_data):
    """Save user data by updating the users dict and saving to file atomically"""
    users = load_all_users()
    users[username] = user_data
    success = save_all_users(users)
    if not success:
        print(f'Warning: Failed to save data for {username}. Inventory changes may not persist.')
    return success

def signup(username, password):
    users = load_all_users()
    if username in users:
        print('Username already exists!')
        return False
    user_data = {'username': username, 'password': password, 'score': 0, 'money': 40, 'player_data': default_player_data(), 'machine_homes': []}
    users[username] = user_data
    save_all_users(users)
    set_machine_home(username)
    print('Signup successful!')
    return True

def signin(username, password):
    user_data = load_user_data(username)
    if user_data and user_data.get('password') == password:
        return (user_data.get('score', 0), user_data.get('money', 40), user_data.get('player_data', default_player_data()))
    else:
        return (None, None, None)

def set_machine_home(username, machine_id=None):
    """Set this machine as a home machine for the account"""
    if not machine_id:
        machine_id = get_machine_id()
    users = load_all_users()
    if username in users:
        if 'machine_homes' not in users[username]:
            users[username]['machine_homes'] = []
        if machine_id not in users[username]['machine_homes']:
            users[username]['machine_homes'].append(machine_id)
            save_all_users(users)
            print(f'This machine ({machine_id}) is now set as a home machine for {username}.')
        else:
            print(f'This machine is already set as a home machine for {username}.')
    else:
        print('User not found.')

def get_home_accounts_for_machine(machine_id=None):
    """Get list of accounts that have this machine set as home"""
    if not machine_id:
        machine_id = get_machine_id()
    users = load_all_users()
    home_accounts = []
    for username, user_data in users.items():
        if machine_id in user_data.get('machine_homes', []):
            home_accounts.append(username)
    return home_accounts

def update_user(username, score=None, money=None, player_data=None):
    users = load_all_users()
    if username in users:
        if score is not None:
            users[username]['score'] = score
        if money is not None:
            users[username]['money'] = money
        if player_data is not None:
            users[username]['player_data'] = player_data
        save_all_users(users)

def default_player_data():
    inv = {'potion': 1, 'strong_potion': 0, 'ultra_potion': 0, 'strength_boost': 0, 'defense_boost': 0, 'regen_potion': 0, 'crit_boost': 0, 'wooden_sword': 1, 'leather_armor': 1, 'mana_upgrade_potion': 0, 'mana_regen_potion': 0, 'instant_mana': 0, 'slime_gel': 0, 'goblin_tooth': 0, 'wolf_pelt': 0, 'skeleton_bone': 0, 'orc_iron': 0, 'bandit_cloth': 0, 'troll_core': 0, 'dark_essence': 0, 'prism_fragment': 0, 'void_fragment': 0, 'infinitium_piece': 0, 'soul_shard': 0, 'transcendent_heart': 0, 'dragon_scale': 0, 'phoenix_feather': 0, 'frozen_heart': 0, 'thunder_core': 0, 'holy_light': 0, 'demon_horn': 0, 'crystal_shard': 0, 'star_dust': 0, 'moon_rock': 0, 'sun_stone': 0, 'common_magic_pack': 0, 'rare_magic_pack': 0, 'mythical_magic_pack': 0, 'prismatic_magic_pack': 0, 'divine_magic_pack': 0, 'transcendent_magic_pack': 0, 'perm_strength_upgrade': 0, 'perm_defense_upgrade': 0, 'perm_health_upgrade': 0, 'perm_mana_upgrade': 0, 'perm_crit_chance_upgrade': 0, 'perm_mana_regen_upgrade': 0, 'perm_lifesteal_upgrade': 0, 'perm_lifesteal_chance_upgrade': 0, 'perm_magic_def_upgrade': 0, 'perm_exp_upgrade': 0}
    return {'money': 40, 'score': 0, 'stats': {'hp_max': 100, 'hp': 100, 'atk': 5, 'defense': 0, 'level': 1, 'exp': 0, 'mana_max': 100, 'mana': 100, 'current_area': 1, 'equipped': {'weapon': None, 'armor': None, 'wand': None, 'robe': None, 'necklace': None},
    'settings': {'call_including_title': True, 'show_exp_bar': False, 'auto_equip_best': False, 'auto_equip_spells': False, 'auto_equip_titles': False, 'auto_equip_everything': False},
    'perm_atk': 0, 'perm_def': 0, 'perm_hp_max': 0, 'perm_mana_max': 0, 'perm_magic_def': 0, 'perm_crit_chance': 0, 'perm_mana_regen': 0, 'perm_lifesteal': 0, 'perm_lifesteal_chance': 0, 'perm_exp_boost': 0, 'title': get_title(1), 'achievements': [], 'monsters_defeated': 0, 'bosses_defeated': 0, 'total_money_earned': 0, 'items_crafted': 0, 'materials_collected': 0, 'times_died': 0, 'dungeon_treasure_collected': 0, 'critical_hits': 0, 'stats_manually_set': {'hp': False, 'hp_max': False, 'atk': False, 'defense': False, 'mana': False, 'mana_max': False},
    'dodge_points': 3, 'max_dodge': 3, 'learned_spells': [], 'equipped_spells': [None, None, None, None], 'available_titles': ['novice'], 'equipped_titles': [None, None, None, None, None], 'title_atk_boost': 0, 'title_def_boost': 0, 'title_hp_boost': 0, 'title_mana_boost': 0, 'title_exp_boost': 0},
    'inventory': inv}

def magic_spell_interface(username):
    user_data = load_user_data(username)
    if not user_data:
        print('User data not found.')
        return
    player_data = user_data.get('player_data', {})
    stats = player_data.get('stats', {})
    learned_spells = stats.get('learned_spells', [])
    equipped_spells = stats.get('equipped_spells', [None, None, None, None])
    while True:
        print('\n--- Magic Spells ---')
        print('Equipped Spells:')
        for i in range(4):
            spell = equipped_spells[i]
            if spell and spell in misc.SPELLS_BY_KEY:
                s = misc.SPELLS_BY_KEY[spell]
                print(f"{i + 1}. Slot {i + 1}: {s['name']} ({s['mana']} mana)")
            else:
                print(f'{i + 1}. Slot {i + 1}: None')
        print('\nLearned Spells:')
        for i, spell_key in enumerate(learned_spells, start=1):
            s = misc.SPELLS_BY_KEY.get(spell_key, {})
            print(f"{i + 4}. {s.get('name', 'Unknown')} (lvl {s.get('lvl', '?')},{s.get('mana', '?')} mana) - {s.get('desc', '')}")
        print('\nQuick Equip:')
        print('b. Equip best spells automatically')
        print('0. Back')
        choice = input('Choose slot to equip/unequip, spell to equip, or "b" for auto-equip best: ').strip()
        if choice == '0':
            break
        elif choice == 'b':
            heal_spells = [s for s in learned_spells if misc.SPELLS_BY_KEY.get(s, {}).get('type') == 'heal']
            non_heal_spells = [s for s in learned_spells if misc.SPELLS_BY_KEY.get(s, {}).get('type') != 'heal']
            heal_spells_sorted = sorted(heal_spells, key=lambda s: misc.SPELLS_BY_KEY.get(s, {}).get('lvl', 0), reverse=True)
            non_heal_sorted = sorted(non_heal_spells, key=lambda s: misc.SPELLS_BY_KEY.get(s, {}).get('lvl', 0), reverse=True)
            equipped_spells = [None] * 4
            for i in range(min(3, len(non_heal_sorted))):
                equipped_spells[i] = non_heal_sorted[i]
            if heal_spells_sorted:
                equipped_spells[3] = heal_spells_sorted[0]
            print('Auto-equipped best spells.')
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < 4:
                equipped_spells[idx] = None
                print(f'Unequipped slot {idx + 1}.')
            elif 4 <= idx < 4 + len(learned_spells):
                spell_idx = idx - 4
                spell_key = learned_spells[spell_idx]
                s = misc.SPELLS_BY_KEY.get(spell_key, {})
                empty_slots = [i for i, sp in enumerate(equipped_spells) if sp is None]
                if empty_slots:
                    slot = empty_slots[0]
                    equipped_spells[slot] = spell_key
                    print(f"Equipped {s.get('name', 'Unknown')} in slot {slot + 1}.")
                else:
                    print('No empty slots. Unequip a slot first.')
            else:
                print('Invalid choice.')
        else:
            print('Invalid choice.')
    stats['equipped_spells'] = equipped_spells
    player_data['stats'] = stats
    user_data['player_data'] = player_data
    save_user_data(username, user_data)

def parse_qty_from_choice(choice_str):
    try:
        return int(choice_str)
    except ValueError:
        return 1

def permanent_upgrades_interface(username):
    try:
        user_data = load_user_data(username)
        if user_data:
            saved_player_data = user_data.get('player_data', {})
            saved_inventory = saved_player_data.get('inventory', {})
            saved_stats = saved_player_data.get('stats', {})
            inventory = saved_inventory
            stats = saved_stats
        else:
            print('User data not found.')
            return
    except Exception as e:
        pass
    player_data = {'stats': stats, 'inventory': inventory}
    upgrade_aliases = {'str': 'perm_strength_upgrade', 'def': 'perm_defense_upgrade', 'hp': 'perm_health_upgrade', 'mana': 'perm_mana_upgrade', 'crit': 'perm_crit_chance_upgrade', 'magic_def': 'perm_magic_def_upgrade', 'lifesteal': 'perm_lifesteal_upgrade', 'lifesteal_chance': 'perm_lifesteal_chance_upgrade', 'exp': 'perm_exp_upgrade', 'perm_def': 'perm_defense_upgrade'}

    def apply_single_upgrade(stats, up_key):
        if 'atk_increase' in misc.PERM_UPGRADES[up_key]:
            stats['perm_atk'] = stats.get('perm_atk', 0) + misc.PERM_UPGRADES[up_key]['atk_increase']
        elif 'def_increase' in misc.PERM_UPGRADES[up_key]:
            stats['perm_def'] = stats.get('perm_def', 0) + misc.PERM_UPGRADES[up_key]['def_increase']
        elif 'hp_increase' in misc.PERM_UPGRADES[up_key]:
            stats['perm_hp_max'] = stats.get('perm_hp_max', 0) + misc.PERM_UPGRADES[up_key]['hp_increase']
        elif 'magic_increase' in misc.PERM_UPGRADES[up_key]:
            stats['perm_mana_max'] = stats.get('perm_mana_max', 0) + misc.PERM_UPGRADES[up_key]['magic_increase']
        elif 'crit_chance_increase' in misc.PERM_UPGRADES[up_key]:
            stats['perm_crit_chance'] = stats.get('perm_crit_chance', 0) + misc.PERM_UPGRADES[up_key]['crit_chance_increase']
        elif 'mana_regen_increase' in misc.PERM_UPGRADES[up_key]:
            stats['perm_mana_regen'] = stats.get('perm_mana_regen', 0) + misc.PERM_UPGRADES[up_key]['mana_regen_increase']
        elif 'max_lifesteal_increase' in misc.PERM_UPGRADES[up_key]:
            stats['perm_lifesteal'] = stats.get('perm_lifesteal', 0) + misc.PERM_UPGRADES[up_key]['max_lifesteal_increase']
        elif 'lifesteal_chance_increase' in misc.PERM_UPGRADES[up_key]:
            stats['perm_lifesteal_chance'] = stats.get('perm_lifesteal_chance', 0) + misc.PERM_UPGRADES[up_key]['lifesteal_chance_increase']
        elif 'exp_increase' in misc.PERM_UPGRADES[up_key]:
            old_boost = stats.get('perm_exp_boost', 0)
            stats['perm_exp_boost'] = old_boost + misc.PERM_UPGRADES[up_key]['exp_increase']
    while True:
        print('\n--- Permanent Upgrades ---')
        print('Available upgrades (use permanent upgrade items from inventory):')
        for key, upgrade in misc.PERM_UPGRADES.items():
            count = inventory.get(key, 0)
            if count > 0:
                print(f"{key}: {upgrade['name']} (x{count})")
            else:
                print(f"{key}: {upgrade['name']} (not owned)")
        print(f"Current Permanent Boosts: ATK +{stats.get('perm_atk', 0)}, DEF +{stats.get('perm_def', 0)}, HP +{stats.get('perm_hp_max', 0)}, Mana +{stats.get('perm_mana_max', 0)}, Crit +{stats.get('perm_crit_chance', 0)}%, Regen +{stats.get('perm_mana_regen', 0)}, Lifesteal +{stats.get('perm_lifesteal', 0)}%, Exp +{stats.get('perm_exp_boost', 0)}%")
        print('0. Back')
        choice = input('Choose upgrade to use: ').strip().lower()
        parts = choice.split()
        if not parts or parts[0] == '0':
            break
        opt = parts[0]
        qty = int(parts[1]) if len(parts) > 1 else 1
        if qty < 1:
            qty = 1
        if opt in upgrade_aliases:
            opt = upgrade_aliases[opt]
        if opt in ['all', 'full']:
            total_applied = 0
            for up_key in misc.PERM_UPGRADES:
                qty_owned = inventory.get(up_key, 0)
                if qty_owned > 0:
                    inventory[up_key] -= qty_owned
                    for _ in range(qty_owned):
                        apply_single_upgrade(stats, up_key)
                    total_applied += qty_owned
            if total_applied > 0:
                player_data['inventory'] = inventory
                player_data['stats'] = stats
                user_data['player_data'] = player_data
                save_user_data(username, user_data)
                check_achievements(username)
                print(f'Used {total_applied} permanent upgrades!')
            else:
                print('No permanent upgrades to use.')
        elif opt in misc.PERM_UPGRADES and inventory.get(opt, 0) >= qty:
            inventory[opt] -= qty
            for _ in range(qty):
                apply_single_upgrade(stats, opt)
            player_data['inventory'] = inventory
            player_data['stats'] = stats
            user_data['player_data'] = player_data
            save_user_data(username, user_data)
            check_achievements(username)
            print(f"Used {qty}x {misc.PERM_UPGRADES[opt]['name']}!")
        else:
            print('Invalid choice or not enough owned.')

def magic_pack_interface(username):
    user_data = load_user_data(username)
    if not user_data:
        print('User data not found.')
        return
    player_data = user_data.get('player_data', {})
    inventory = player_data.get('inventory', {})
    while True:
        print('\n--- Magic Packs ---')
        print('Available packs:')
        for pack_key, pack in misc.MAGIC_PACKS.items():
            count = inventory.get(pack_key, 0)
            if count > 0:
                print(f"{pack_key}: {pack['name']} (x{count}) - {pack['description']}")
            else:
                print(f"{pack_key}: {pack['name']} - {pack['description']} (not owned)")
        print('0. Back')
        choice = input('Choose pack to open (e.g., transcendent 5 or transcendent all or all): ').strip().lower()
        parts = choice.split()
        if not parts:
            continue
        pack_alias = parts[0]
        if len(parts) > 1:
            if parts[1] == 'all':
                qty = inventory.get(pack_alias, 0) if pack_alias in misc.MAGIC_PACKS else 0
            else:
                try:
                    qty = int(parts[1])
                except ValueError:
                    qty = 1
        else:
            qty = 1
        if qty < 1:
            qty = 1
        if pack_alias == '0':
            break
        if pack_alias in misc.MAGIC_PACK_ALIASES:
            pack_alias = misc.MAGIC_PACK_ALIASES[pack_alias]
        if pack_alias == 'all':
            total_opened = 0
            for p_key in misc.MAGIC_PACKS:
                if inventory.get(p_key, 0) > 0:
                    success, message = open_magic_pack(username, p_key, inventory[p_key])
                    if success:
                        print(f"{p_key}: {message}")
                        total_opened += inventory[p_key]
                        inventory[p_key] = 0
                    else:
                        print(f"{p_key}: {message}")
            if total_opened > 0:
                user_data = load_user_data(username)
                if user_data:
                    player_data = user_data.get('player_data', {})
                    inventory = player_data.get('inventory', {})
                print(f"Opened {total_opened} packs in total!")
            else:
                print('No packs to open.')
        elif pack_alias in misc.MAGIC_PACKS and inventory.get(pack_alias, 0) >= qty:
            success, message = open_magic_pack(username, pack_alias, qty)
            if success:
                print(message)
                user_data = load_user_data(username)
                if user_data:
                    player_data = user_data.get('player_data', {})
                    inventory = player_data.get('inventory', {})
            else:
                print(message)
        else:
            print('Invalid choice or not enough owned.')

def apply_permanent_upgrades(username):
    try:
        user_data = load_user_data(username)
        if not user_data:
            return
        player_data = user_data['player_data']
        stats = player_data['stats']
        inventory = player_data['inventory']
        apply_title_boosts(username)
        player_data['stats'] = stats
        user_data['player_data'] = player_data
        save_user_data(username, user_data)
    except Exception as e:
        print(f'Error applying permanent upgrades: {e}')

def crafting_interface(username):
    try:
        user_data = load_user_data(username)
        if user_data:
            saved_player_data = user_data.get('player_data', {})
            saved_inventory = saved_player_data.get('inventory', {})
            inventory = saved_inventory
        else:
            print('User data not found.')
            return
    except Exception as e:
        pass
    while True:
        print('\n--- Crafting Interface ---')
        print('Available recipes:')
        recipe_list = []
        for recipe_key, recipe in misc.RECIPES.items():
            can_craft = True
            materials_needed = recipe['materials']
            for mat, qty in materials_needed.items():
                if inventory.get(mat, 0) < qty:
                    can_craft = False
                    break
            status = '✓' if can_craft else '✗'
            result_item = recipe['result']
            result_name = 'Unknown'
            if result_item in misc.POTIONS:
                result_name = misc.POTIONS[result_item]['name']
            elif result_item in misc.PERM_UPGRADES:
                result_name = misc.PERM_UPGRADES[result_item]['name']
            elif result_item in misc.CRAFTABLE_WEAPONS:
                result_name = misc.CRAFTABLE_WEAPONS[result_item]['name']
            elif result_item in misc.CRAFTABLE_WANDS:
                result_name = misc.CRAFTABLE_WANDS[result_item]['name']
            elif result_item in misc.CRAFTABLE_NECKLACES:
                result_name = misc.CRAFTABLE_NECKLACES[result_item]['name']
            elif result_item in misc.CRAFTABLE_ROBES:
                result_name = misc.CRAFTABLE_ROBES[result_item]['name']
            elif result_item in misc.CRAFTABLE_misc.ARMORS:
                result_name = misc.CRAFTABLE_misc.ARMORS[result_item]['name']
            recipe_list.append((recipe_key, result_name, can_craft))
            materials_str = ', '.join([f"{mat} x{qty}" for mat, qty in materials_needed.items()])
            print(f"{len(recipe_list)}. {status} {result_name} - Requires: {materials_str}")
        print('0. Back')
        choice = input('Choose recipe to craft (e.g., 1 or 1 3 for quantity 3): ').strip().lower()
        parts = choice.split()
        if not parts or parts[0] == '0':
            break
        opt = parts[0]
        qty = int(parts[1]) if len(parts) > 1 else 1
        if qty < 1:
            qty = 1
        if opt.isdigit():
            idx = int(opt) - 1
            if 0 <= idx < len(recipe_list):
                recipe_key, result_name, can_craft = recipe_list[idx]
                if can_craft:
                    recipe = misc.RECIPES[recipe_key]
                    materials_needed = recipe['materials']
                    result = recipe['result']
                    result_qty = recipe['qty']
                    total_result_qty = result_qty * qty
                    # Check if can craft qty times
                    can_craft_qty = True
                    for mat, qty_needed in materials_needed.items():
                        if inventory.get(mat, 0) < qty_needed * qty:
                            can_craft_qty = False
                            break
                    if can_craft_qty:
                        # Deduct materials
                        for mat, qty_needed in materials_needed.items():
                            inventory[mat] -= qty_needed * qty
                        # Add result
                        inventory[result] = inventory.get(result, 0) + total_result_qty
                        player_data = {'inventory': inventory}
                        user_data['player_data'] = player_data
                        save_user_data(username, user_data)
                        print(f"Successfully crafted {total_result_qty}x {result_name}!")
                    else:
                        print(f'Not enough materials to craft {qty}x {result_name}.')
                else:
                    print(f'Cannot craft {result_name} - missing materials.')
            else:
                print('Invalid choice.')
        else:
            print('Invalid choice.')

def open_magic_pack(username, pack_key, quantity=1):
    users = load_all_users()
    if username not in users:
        return (False, 'Invalid user.')
    if pack_key not in misc.MAGIC_PACKS:
        return (False, 'Unknown magic pack.')
    user_data = users[username]
    player_data = user_data.get('player_data', {})
    inventory = player_data.get('inventory', {})
    stats = player_data.get('stats', {})
    if inventory.get(pack_key, 0) < quantity:
        return (False, f"You don't have enough {misc.MAGIC_PACKS[pack_key]['name']}.")
    pack = misc.MAGIC_PACKS[pack_key]
    spells_pool = pack['spells']
    min_count, max_count = pack['drop_count']
    if 'learned_spells' not in stats:
        stats['learned_spells'] = []
    inventory[pack_key] -= quantity
    new_spells = []
    for _ in range(quantity):
        count = random.randint(min_count, max_count)
        for _ in range(count):
            spell_key = random.choice(spells_pool)
            if spell_key not in stats['learned_spells']:
                stats['learned_spells'].append(spell_key)
                new_spells.append(misc.SPELLS_BY_KEY[spell_key]['name'])
    player_data['inventory'] = inventory
    player_data['stats'] = stats
    user_data['player_data'] = player_data
    save_user_data(username, user_data)
    if new_spells:
        return (True, f"You opened {quantity} {pack['name']}(s) and learned: {', '.join(new_spells)}")
    else:
        return (True, f"You opened {quantity} {pack['name']}(s) but didn't learn any new spells.")

def parse_qty_from_choice(choice_str):
    parts = choice_str.split()
    if len(parts) >= 2:
        try:
            q = int(parts[1])
            if q < 1:
                q = 1
            return (q, ' '.join(parts[2:]) if len(parts) > 2 else '')
        except:
            return (1, ' '.join(parts[1:]))
    return (1, '')

def ensure_user_fields(username):
    """
    Normalize a user's data to ensure all expected keys exist so older saves won't crash.
    Call this after loading, signup, login, and before any operation that uses stats/inventory.
    """
    user_data = load_user_data(username)
    if not user_data:
        return
    try:
        player_data = user_data['player_data']
    except (KeyError, TypeError):
        player_data = default_player_data()
    default = default_player_data()
    stats = player_data.get('stats', {})
    for k, v in default['stats'].items():
        if k not in stats:
            stats[k] = v
    if 'current_area' not in stats:
        stats['current_area'] = 1
    if 'learned_spells' not in stats:
        stats['learned_spells'] = []
    if 'equipped_spells' not in stats:
        stats['equipped_spells'] = [None, None, None, None]
    if 'available_titles' not in stats:
        stats['available_titles'] = []
    if 'equipped_titles' not in stats:
        stats['equipped_titles'] = [None, None, None, None, None]
    for boost_field in ['title_atk_boost', 'title_def_boost', 'title_hp_boost', 'title_mana_boost', 'title_exp_boost']:
        if boost_field not in stats:
            stats[boost_field] = 0
    if 'equipped' not in stats or not isinstance(stats['equipped'], dict):
        stats['equipped'] = default['stats']['equipped'].copy()
    else:
        for slot in default['stats']['equipped']:
            if slot not in stats['equipped']:
                stats['equipped'][slot] = default['stats']['equipped'][slot]
    if 'stats_manually_set' not in stats:
        stats['stats_manually_set'] = default['stats']['stats_manually_set'].copy()
    inventory = player_data.get('inventory', {})
    for k, v in default['inventory'].items():
        if k not in inventory:
            inventory[k] = v
    player_data['stats'] = stats
    player_data['inventory'] = inventory
    user_data['player_data'] = player_data
    save_user_data(username, user_data)

def settings_menu(username):
    if not username:
        return
    user_data = load_user_data(username)
    if not user_data:
        return
    player_data = user_data.get('player_data', {})
    stats = player_data.get('stats', {})
    settings = stats.get('settings', {})
    while True:
        print('\n--- Settings ---')
        print(f"1. Show EXP bar: {('ON' if settings.get('show_exp_bar', False) else 'OFF')}")
        print(f"2. Auto-equip best items: {('ON' if settings.get('auto_equip_best', False) else 'OFF')}")
        print(f"3. Auto-equip spells: {('ON' if settings.get('auto_equip_spells', False) else 'OFF')}")
        print(f"4. Auto-equip titles: {('ON' if settings.get('auto_equip_titles', False) else 'OFF')}")
        print(f"5. Auto-equip everything: {('ON' if settings.get('auto_equip_everything', False) else 'OFF')}")
        print(f"6. Call including title: {('ON' if settings.get('call_including_title', True) else 'OFF')}")
        print('7. Equip Titles')
        print('8. Set this machine as home')
        print('9. Back to Main Menu')
        choice = input('Choose setting: ').strip()
        if choice == '1':
            settings['show_exp_bar'] = not settings.get('show_exp_bar', False)
            print(f"EXP bar display {('enabled' if settings['show_exp_bar'] else 'disabled')}.")
        elif choice == '2':
            settings['auto_equip_best'] = not settings.get('auto_equip_best', False)
            print(f"Auto-equip best items {('enabled' if settings['auto_equip_best'] else 'disabled')}.")
        elif choice == '3':
            settings['auto_equip_spells'] = not settings.get('auto_equip_spells', False)
            print(f"Auto-equip spells {('enabled' if settings['auto_equip_spells'] else 'disabled')}.")
            if settings['auto_equip_spells']:
                try:
                    auto_equip_spells(username)
                except Exception as e:
                    print(f'Error auto-equipping spells: {e}')
        elif choice == '4':
            settings['auto_equip_titles'] = not settings.get('auto_equip_titles', False)
            print(f"Auto-equip titles {('enabled' if settings['auto_equip_titles'] else 'disabled')}.")
        elif choice == '5':
            settings['auto_equip_everything'] = not settings.get('auto_equip_everything', False)
            print(f"Auto-equip everything {('enabled' if settings['auto_equip_everything'] else 'disabled')}.")
        elif choice == '6':
            settings['call_including_title'] = not settings.get('call_including_title', True)
            print(f"Call including title {('enabled' if settings['call_including_title'] else 'disabled')}.")
        elif choice == '7':
            equip_titles_menu(username, player_data, None)
        elif choice == '8':
            set_machine_home(username)
        elif choice == '9':
            break
        else:
            print('Invalid choice.')
        stats['settings'] = settings
        player_data['stats'] = stats
        user_data['player_data'] = player_data
        save_user_data(username, user_data)

def equip_titles_menu(username, player_data, cursor):
    stats = player_data.get('stats', {})
    available_titles = stats.get('available_titles', [])
    equipped_titles = stats.get('equipped_titles', [None, None, None, None, None])
    while True:
        print('\n--- Equip Titles ---')
        for i in range(5):
            title = equipped_titles[i]
            print(f"{i + 1}. Slot {i + 1}: {(misc.TITLES.get(title, {}).get('name', 'None') if title else 'None')}")
        print('\nAvailable Titles:')
        for i, title_key in enumerate(available_titles, start=1):
            title_name = misc.TITLES.get(title_key, {}).get('name', title_key)
            print(f'{i + 5}. {title_name}')
        print('0. Back')
        choice = input('Choose slot to equip/unequip or title to equip: ').strip()
        if choice == '0':
            break
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < 5:
                equipped_titles[idx] = None
                print(f'Unequipped slot {idx + 1}.')
            elif 5 <= idx < 5 + len(available_titles):
                title_idx = idx - 5
                title_key = available_titles[title_idx]
                empty_slots = [i for i, t in enumerate(equipped_titles) if t is None]
                if empty_slots:
                    slot = empty_slots[0]
                    equipped_titles[slot] = title_key
                    print(f"Equipped {misc.TITLES[title_key]['name']} in slot {slot + 1}.")
                else:
                    print('No empty slots. Unequip a slot first.')
            else:
                print('Invalid choice.')
        else:
            print('Invalid choice.')
    apply_title_boosts(username)

def apply_title_boosts(username):
    try:
        user_data = load_user_data(username)
        if not user_data:
            return
        player_data = user_data['player_data']
        stats = player_data['stats']
        stats['title_atk_boost'] = 0
        stats['title_def_boost'] = 0
        stats['title_hp_boost'] = 0
        stats['title_mana_boost'] = 0
        stats['title_exp_boost'] = 0
        stats['title_magic_def_boost'] = 0
        for title_id in stats.get('equipped_titles', []):
            if title_id and title_id in misc.TITLES:
                title = misc.TITLES[title_id]
                stats['title_atk_boost'] += title.get('atk_boost', 0)
                stats['title_def_boost'] += title.get('def_boost', 0)
                stats['title_hp_boost'] += title.get('hp_boost', 0)
                stats['title_mana_boost'] += title.get('mana_boost', 0)
                stats['title_exp_boost'] += title.get('exp_boost', 0)
                stats['title_magic_def_boost'] += title.get('magic_def_boost', 0)
        player_data['stats'] = stats
        user_data['player_data'] = player_data
        save_user_data(username, user_data)
    except Exception as e:
        print(f'Error applying title boosts: {e}')

def auto_equip_spells(username):
    try:
        user_data = load_user_data(username)
        if not user_data:
            return
        player_data = user_data['player_data']
        stats = player_data['stats']
        settings = stats.get('settings', {})
        if not settings.get('auto_equip_spells', False) and (not settings.get('auto_equip_everything', False)):
            return
        learned_spells = stats.get('learned_spells', [])
        if not learned_spells:
            return
        heal_spells = [s for s in learned_spells if misc.SPELLS_BY_KEY.get(s, {}).get('type') == 'heal']
        non_heal_spells = [s for s in learned_spells if misc.SPELLS_BY_KEY.get(s, {}).get('type') != 'heal']
        heal_spells_sorted = sorted(heal_spells, key=lambda s: misc.SPELLS_BY_KEY.get(s, {}).get('lvl', 0), reverse=True)
        non_heal_sorted = sorted(non_heal_spells, key=lambda s: misc.SPELLS_BY_KEY.get(s, {}).get('lvl', 0), reverse=True)
        equipped_spells = [None] * 4
        for i in range(min(3, len(non_heal_sorted))):
            equipped_spells[i] = non_heal_sorted[i]
        if heal_spells_sorted:
            equipped_spells[3] = heal_spells_sorted[0]
        stats['equipped_spells'] = equipped_spells
        player_data['stats'] = stats
        user_data['player_data'] = player_data
        save_user_data(username, user_data)
    except Exception as e:
        print(f'Error auto-equipping spells: {e}')

def auto_equip_items(username):
    try:
        user_data = load_user_data(username)
        if not user_data:
            return
        player_data = user_data['player_data']
        stats = player_data['stats']
        inventory = player_data['inventory']
        equipped = stats['equipped']
        if not (stats['settings'].get('auto_equip_best', False) or stats['settings'].get('auto_equip_everything', False)):
            return
        best_weapon = None
        best_weapon_atk = 0
        for weapon_id, count in inventory.items():
            if count > 0 and weapon_id in misc.WEAPONS:
                weapon_atk = misc.WEAPONS[weapon_id]['atk']
                if weapon_atk > best_weapon_atk:
                    best_weapon = weapon_id
                    best_weapon_atk = weapon_atk
        if best_weapon and best_weapon != equipped['weapon']:
            equipped['weapon'] = best_weapon
        best_armor = None
        best_armor_def = 0
        for armor_id, count in inventory.items():
            if count > 0 and armor_id in misc.ARMORS:
                armor_def = misc.ARMORS[armor_id]['def']
                if armor_def > best_armor_def:
                    best_armor = armor_id
                    best_armor_def = armor_def
        if best_armor and best_armor != equipped['armor']:
            equipped['armor'] = best_armor
        if stats['settings'].get('auto_equip_everything', False):
            best_wand = None
            best_wand_magic_atk = 0
            for wand_id, count in inventory.items():
                if count > 0 and wand_id in misc.WANDS:
                    wand_magic_atk = misc.WANDS[wand_id]['magic_atk']
                    if wand_magic_atk > best_wand_magic_atk:
                        best_wand = wand_id
                        best_wand_magic_atk = wand_magic_atk
            if best_wand and best_wand != equipped['wand']:
                equipped['wand'] = best_wand
            best_robe = None
            best_robe_magic_def = 0
            for robe_id, count in inventory.items():
                if count > 0 and robe_id in misc.ROBES:
                    robe_magic_def = misc.ROBES[robe_id]['magic_def']
                    if robe_magic_def > best_robe_magic_def:
                        best_robe = robe_id
                        best_robe_magic_def = robe_magic_def
            if best_robe and best_robe != equipped['robe']:
                equipped['robe'] = best_robe
            best_necklace = None
            best_necklace_value = 0
            for necklace_id, count in inventory.items():
                if count > 0 and necklace_id in misc.NECKLACES:
                    necklace = misc.NECKLACES[necklace_id]
                    total_value = necklace.get('hp_bonus', 0) * 1 + necklace.get('mana_bonus', 0) * 1 + necklace.get('atk_bonus', 0) * 2 + necklace.get('def_bonus', 0) * 2 + necklace.get('magic_atk_bonus', 0) * 2 + necklace.get('magic_def_bonus', 0) * 2 + necklace.get('crit_bonus', 0) * 3 + necklace.get('lifesteal_bonus', 0) * 3
                    if total_value > best_necklace_value:
                        best_necklace = necklace_id
                        best_necklace_value = total_value
            if best_necklace and best_necklace != equipped['necklace']:
                equipped['necklace'] = best_necklace
        player_data['stats']['equipped'] = equipped
        user_data['player_data'] = player_data
        save_user_data(username, user_data)
    except Exception as e:
        print(f'Error auto-equipping items: {e}')

def manage_inventory_menu(username, player_data, cursor):
    user_data = load_user_data(username)
    if not user_data:
        return
    money = user_data.get('money', 0)
    stats = player_data['stats']
    inventory = player_data['inventory']
    equipped = stats.get('equipped', {})
    while True:
        print('\n--- Manage Inventory ---')
        print(f'Money: {money}')
        print('Equipped:')
        weapon = equipped.get('weapon')
        print(f"  Weapon: {(misc.WEAPONS.get(weapon, {}).get('name', 'None') if weapon else 'None')}")
        armor = equipped.get('armor')
        print(f"  Armor: {(misc.ARMORS.get(armor, {}).get('name', 'None') if armor else 'None')}")
        wand = equipped.get('wand')
        print(f"  Wand: {(misc.WANDS.get(wand, {}).get('name', 'None') if wand else 'None')}")
        robe = equipped.get('robe')
        print(f"  Robe: {(misc.ROBES.get(robe, {}).get('name', 'None') if robe else 'None')}")
        necklace = equipped.get('necklace')
        print(f"  Necklace: {(misc.NECKLACES.get(necklace, {}).get('name', 'None') if necklace else 'None')}")
        print('\nInventory:')
        item_list = []
        for key, count in inventory.items():
            if count > 0:
                name = 'Unknown'
                if key in misc.WEAPONS:
                    name = misc.WEAPONS[key]['name']
                elif key in misc.ARMORS:
                    name = misc.ARMORS[key]['name']
                elif key in misc.WANDS:
                    name = misc.WANDS[key]['name']
                elif key in misc.ROBES:
                    name = misc.ROBES[key]['name']
                elif key in misc.NECKLACES:
                    name = misc.NECKLACES[key]['name']
                else:
                    continue
                item_list.append((key, name, count))
                print(f'  {len(item_list)}. {name} x{count}')
        print('\nQuick Equip:')
        print('w. Equip best weapon')
        print('a. Equip best armor')
        print('m. Equip best wand')
        print('r. Equip best robe')
        print('n. Equip best necklace')
        print('0. Back')
        choice = input("Choose item to equip (number), 'u' + slot to unequip, or quick equip option: ").strip().lower()
        if choice == '0':
            break
        elif choice == 'w':
            best_weapon = None
            best_weapon_atk = 0
            for weapon_id, count in inventory.items():
                if count > 0 and weapon_id in misc.WEAPONS:
                    weapon_atk = misc.WEAPONS[weapon_id]['atk']
                    if weapon_atk > best_weapon_atk:
                        best_weapon = weapon_id
                        best_weapon_atk = weapon_atk
            if best_weapon:
                equipped['weapon'] = best_weapon
                print(f'Equipped best weapon: {misc.WEAPONS[best_weapon]["name"]}')
            else:
                print('No weapons to equip.')
        elif choice == 'a':
            best_armor = None
            best_armor_def = 0
            for armor_id, count in inventory.items():
                if count > 0 and armor_id in misc.ARMORS:
                    armor_def = misc.ARMORS[armor_id]['def']
                    if armor_def > best_armor_def:
                        best_armor = armor_id
                        best_armor_def = armor_def
            if best_armor:
                equipped['armor'] = best_armor
                print(f'Equipped best armor: {misc.ARMORS[best_armor]["name"]}')
            else:
                print('No armors to equip.')
        elif choice == 'm':
            best_wand = None
            best_wand_magic_atk = 0
            for wand_id, count in inventory.items():
                if count > 0 and wand_id in misc.WANDS:
                    wand_magic_atk = misc.WANDS[wand_id]['magic_atk']
                    if wand_magic_atk > best_wand_magic_atk:
                        best_wand = wand_id
                        best_wand_magic_atk = wand_magic_atk
            if best_wand:
                equipped['wand'] = best_wand
                print(f'Equipped best wand: {misc.WANDS[best_wand]["name"]}')
            else:
                print('No wands to equip.')
        elif choice == 'r':
            best_robe = None
            best_robe_magic_def = 0
            for robe_id, count in inventory.items():
                if count > 0 and robe_id in misc.ROBES:
                    robe_magic_def = misc.ROBES[robe_id]['magic_def']
                    if robe_magic_def > best_robe_magic_def:
                        best_robe = robe_id
                        best_robe_magic_def = robe_magic_def
            if best_robe:
                equipped['robe'] = best_robe
                print(f'Equipped best robe: {misc.ROBES[best_robe]["name"]}')
            else:
                print('No robes to equip.')
        elif choice == 'n':
            best_necklace = None
            best_necklace_value = 0
            for necklace_id, count in inventory.items():
                if count > 0 and necklace_id in misc.NECKLACES:
                    necklace = misc.NECKLACES[necklace_id]
                    total_value = necklace.get('hp_bonus', 0) * 1 + necklace.get('mana_bonus', 0) * 1 + necklace.get('atk_bonus', 0) * 2 + necklace.get('def_bonus', 0) * 2 + necklace.get('magic_atk_bonus', 0) * 2 + necklace.get('magic_def_bonus', 0) * 2 + necklace.get('crit_bonus', 0) * 3 + necklace.get('lifesteal_bonus', 0) * 3
                    if total_value > best_necklace_value:
                        best_necklace = necklace_id
                        best_necklace_value = total_value
            if best_necklace:
                equipped['necklace'] = best_necklace
                print(f'Equipped best necklace: {misc.NECKLACES[best_necklace]["name"]}')
            else:
                print('No necklaces to equip.')
        elif choice.startswith('u'):
            slot_num = choice[1:]
            if slot_num == '1':
                equipped['weapon'] = None
                print('Unequipped weapon.')
            elif slot_num == '2':
                equipped['armor'] = None
                print('Unequipped armor.')
            elif slot_num == '3':
                equipped['wand'] = None
                print('Unequipped wand.')
            elif slot_num == '4':
                equipped['robe'] = None
                print('Unequipped robe.')
            elif slot_num == '5':
                equipped['necklace'] = None
                print('Unequipped necklace.')
            else:
                print('Invalid slot.')
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(item_list):
                item_key, item_name, count = item_list[idx]
                if item_key in misc.WEAPONS:
                    equipped['weapon'] = item_key
                    print(f'Equipped {item_name} as weapon.')
                elif item_key in misc.ARMORS:
                    equipped['armor'] = item_key
                    print(f'Equipped {item_name} as armor.')
                elif item_key in misc.WANDS:
                    equipped['wand'] = item_key
                    print(f'Equipped {item_name} as wand.')
                elif item_key in misc.ROBES:
                    equipped['robe'] = item_key
                    print(f'Equipped {item_name} as robe.')
                elif item_key in misc.NECKLACES:
                    equipped['necklace'] = item_key
                    print(f'Equipped {item_name} as necklace.')
            else:
                print('Invalid choice.')
        else:
            print('Invalid choice.')
    player_data['stats'] = stats
    player_data['inventory'] = inventory
    user_data = load_user_data(username)
    if user_data:
        user_data['player_data'] = player_data
        save_user_data(username, user_data)

def view_achievements_menu(username):
    user_data = load_user_data(username)
    if not user_data:
        return
    player_data = user_data.get('player_data', {})
    stats = player_data.get('stats', {})
    unlocked = stats.get('achievements', [])
    print('\n--- Achievements ---')
    for ach_key, achievement in misc.ACHIEVEMENTS.items():
        status = '✓' if ach_key in unlocked else '✗'
        print(f"{status} {achievement['name']}: {achievement['desc']}")

def compute_effective_stats(stats, active_buffs):
    base_atk = stats.get('atk', 5)
    base_def = stats.get('defense', 0)
    base_magic_atk = 0
    base_magic_def = 0
    weapon = stats.get('equipped', {}).get('weapon')
    armor = stats.get('equipped', {}).get('armor')
    wand = stats.get('equipped', {}).get('wand')
    robe = stats.get('equipped', {}).get('robe')
    necklace = stats.get('equipped', {}).get('necklace')
    w_atk = misc.WEAPONS.get(weapon, {}).get('atk', 0) if weapon else 0
    a_def = misc.ARMORS.get(armor, {}).get('def', 0) if armor else 0
    wand_magic = misc.WANDS.get(wand, {}).get('magic_atk', 0) if wand else 0
    robe_def = misc.ROBES.get(robe, {}).get('magic_def', 0) if robe else 0
    n_atk = misc.NECKLACES.get(necklace, {}).get('atk_bonus', 0) if necklace else 0
    n_def = misc.NECKLACES.get(necklace, {}).get('def_bonus', 0) if necklace else 0
    n_hp = misc.NECKLACES.get(necklace, {}).get('hp_bonus', 0) if necklace else 0
    n_mana = misc.NECKLACES.get(necklace, {}).get('mana_bonus', 0) if necklace else 0
    n_crit = misc.NECKLACES.get(necklace, {}).get('crit_bonus', 0) if necklace else 0
    n_lifesteal = misc.NECKLACES.get(necklace, {}).get('lifesteal_bonus', 0) if necklace else 0
    n_magic_atk = misc.NECKLACES.get(necklace, {}).get('magic_atk_bonus', 0) if necklace else 0
    n_magic_def = misc.NECKLACES.get(necklace, {}).get('magic_def_bonus', 0) if necklace else 0
    t_atk = stats.get('title_atk_boost', 0)
    t_def = stats.get('title_def_boost', 0)
    t_hp = stats.get('title_hp_boost', 0)
    t_mana = stats.get('title_mana_boost', 0)
    t_atk_percent = stats.get('title_atk_percent', 0)
    t_def_percent = stats.get('title_def_percent', 0)
    t_hp_percent = stats.get('title_hp_percent', 0)
    t_mana_percent = stats.get('title_mana_percent', 0)
    atk_buff = sum((b['amount'] for b in active_buffs if b['type'] == 'atk' and b['remaining'] > 0))
    def_buff = sum((b['amount'] for b in active_buffs if b['type'] == 'def' and b['remaining'] > 0))
    global effective_atk, effective_def, effective_magic_atk, effective_magic_def, effective_hp_bonus, effective_mana_bonus
    effective_atk = base_atk + w_atk + n_atk + t_atk + atk_buff
    effective_def = base_def + a_def + n_def + t_def + def_buff
    effective_magic_atk = wand_magic + n_magic_atk
    effective_magic_def = robe_def + n_magic_def
    effective_hp_bonus = n_hp + t_hp
    effective_mana_bonus = n_mana + t_mana
    effective_atk = int(effective_atk * (1 + t_atk_percent / 100.0))
    effective_def = int(effective_def * (1 + t_def_percent / 100.0))
    effective_hp_bonus = int(effective_hp_bonus * (1 + t_hp_percent / 100.0))
    effective_mana_bonus = int(effective_mana_bonus * (1 + t_mana_percent / 100.0))
    # Add permanent boosts
    effective_atk += stats.get('perm_atk', 0)
    effective_def += stats.get('perm_def', 0)
    effective_magic_def += stats.get('perm_magic_def', 0) + stats.get('title_magic_def_boost', 0)
    effective_hp_bonus += stats.get('perm_hp_max', 0)
    effective_mana_bonus += stats.get('perm_mana_max', 0)
    return (effective_atk, effective_def, effective_magic_atk, effective_magic_def, effective_hp_bonus, effective_mana_bonus, n_crit, n_lifesteal)

def get_leaderboard():
    """Get leaderboard from users.txt"""
    users_data = []
    users = load_all_users()
    for username, user_data in users.items():
        score = user_data.get('score', 0)
        users_data.append((username, score))
    users_data.sort(key=lambda x: x[1], reverse=True)
    return users_data[:10]

def guessing_game(current_user, score):
    number = random.randint(1, 100)
    attempts = 0
    print('Welcome to the Number Guessing Game!')
    print("I'm thinking of a number between 1 and 100.")
    while True:
        try:
            guess = int(input('Enter your guess: '))
            attempts += 1
            if guess < number:
                print('Too low!')
            elif guess > number:
                print('Too high!')
            else:
                print(f'Correct! You guessed it in {attempts} attempts.')
                score += max(0, 10 - attempts)
                print(f'Score updated. New score: {score}')
                update_user(current_user, score=score)
                return score
        except ValueError:
            print('Please enter a valid number.')

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
            print('setdefeated <u> <type> <n> - set defeated count for type (monsters, bosses, etc.)')
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
                    time.sleep()
                    print('Action → reset.account')
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
                    print(f' • TARGET      : {u}')
                    print(' • MODE        : irreversible purge')
                    print(' • STATUS      : Complete')
                    print(' • TRACE       : all identifiers wiped')
                    print()
                    print('> Finalizing cleanup...')
                    print('   → Scrubbing data blocks.........OK')
                    print('   → Flushing cache entries........OK')
                    time.sleep(round(random.uniform(0, 1.5), 2))
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
                    other_functions.save_dungeon_treasure()
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
            if success == True:
                show_memory_patch()
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
            if success == True:
                show_memory_patch()
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
                        upgrade_aliases = {'str': 'perm_strength_upgrade', 'def': 'perm_defense_upgrade', 'hp': 'perm_health_upgrade', 'mana': 'perm_mana_upgrade', 'crit': 'perm_crit_chance_upgrade', 'magic_def': 'perm_magic_def_upgrade', 'lifesteal': 'perm_lifesteal_upgrade', 'lifesteal_chance': 'perm_lifesteal_chance_upgrade', 'exp': 'perm_exp_upgrade', 'perm_str': 'perm_strength_upgrade', 'perm_def': 'perm_defense_upgrade', 'perm_hp': 'perm_health_upgrade', 'perm_mana': 'perm_mana_upgrade', 'perm_crit': 'perm_crit_chance_upgrade', 'perm_magic_def': 'perm_magic_def_upgrade', 'perm_lifesteal': 'perm_lifesteal_upgrade', 'perm_lifesteal_chance': 'perm_lifesteal_chance_upgrade', 'perm_exp': 'perm_exp_upgrade', 'perm_strength_upgrade': 'perm_strength_upgrade', 'perm_defense_upgrade': 'perm_defense_upgrade', 'perm_health_upgrade': 'perm_health_upgrade', 'perm_mana_upgrade': 'perm_mana_upgrade', 'perm_crit_chance_upgrade': 'perm_crit_chance_upgrade', 'perm_magic_def_upgrade': 'perm_magic_def_upgrade', 'perm_lifesteal_upgrade': 'perm_lifesteal_upgrade', 'perm_lifesteal_chance_upgrade': 'perm_lifesteal_chance_upgrade', 'perm_exp_upgrade': 'perm_exp_upgrade'}
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
                            if success == True:
                                show_memory_patch()
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
            if success == True:
                show_memory_patch
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
                stats['achievements'] = list(misc.ACHIEVEMENTS.keys())
                stats['available_titles'] = list(misc.TITLES.keys())
                stats['equipped_titles'] = list(misc.TITLES.keys())
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
                for eq in [misc.WEAPONS, misc.ARMORS, misc.WANDS, misc.ROBES, misc.NECKLACES]:
                    for item in eq:
                        inventory[item] = 1
                for mat in misc.MATERIALS:
                    inventory[mat] = 500
                for up in misc.PERM_UPGRADES:
                    inventory[up] = 250
                for mp in misc.MAGIC_PACKS:
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

