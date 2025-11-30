import json
import random
import os
import math
import time
import atexit
import threading
import socket

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
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Verifying authorization level...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Locking target user profile...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print()
    print('!! WARNING !!')
    print('User deletion is irreversible.')
    print('All personal data, stats, sessions,')
    print('and identifiers will be permanently removed.')
    print()
    print('> Executing purge sequence...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Revoking credentials...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Erasing activity logs...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Scrubbing metadata clusters...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Removing account fingerprint...')
    time.sleep(round(random.uniform(0, 1.5), 2))
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
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Verifying creation permissions...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Allocating registry slot...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Generating user credentials...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Assigning unique identifier...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Building default profile structure...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print('> Registering access keys...')
    time.sleep(round(random.uniform(0, 1.5), 2))
    print()
    print('[CREATION REPORT]')
    print(f' • TARGET      : {username}')
    print(' • STATUS      : successfully created')
    print(' • PROFILE     : baseline configuration applied')
    print(' • SECURITY    : encrypted & verified')
    print()
    print('> Finalizing setup...')
    print('   → Syncing with user registry......OK')
    time.sleep(round(random.uniform(0, 1.5), 2))
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
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_DIR = os.path.join(SCRIPT_DIR, 'users.txt')
DUNGEON_TREASURE_FILE = os.path.join(SCRIPT_DIR, 'dungeon_treasure.json')
dungeon_treasure = {'money': 0, 'items': []}
GLOBAL_KEY = '__global__'
AUTOSAVE_INTERVAL = 30
autosave_timer = None
last_autosave_time = time.time()

check_file_existence()

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
PERM_UPGRADES = {
    'perm_strength_upgrade': {'name': 'Perm Strength Upgrade', 'atk_increase': 10},
    'perm_defense_upgrade': {'name': 'Perm Defense Upgrade', 'def_increase': 5},
    'perm_health_upgrade': {'name': 'Perm Health Upgrade', 'hp_increase': 10},
    'perm_mana_upgrade': {'name': 'Perm Mana Upgrade', 'magic_increase': 20},
    'perm_crit_chance_upgrade': {'name': 'Perm Crit Chance Upgrade', 'crit_chance_increase': 5},
    'perm_mana_regen_upgrade': {'name': 'Perm Mana Regen Upgrade', 'mana_regen_increase': 5},
    'perm_magic_def_upgrade': {'name': 'Perm Magic Defense Upgrade', 'magic_def_increase': 5},
    'perm_lifesteal_upgrade': {'name': 'Perm Lifesteal Upgrade', 'max_lifesteal_increase': 10},
    'perm_lifesteal_chance_upgrade': {'name': 'Perm Lifesteal Chance Upgrade', 'lifesteal_chance_increase': 5},
    'perm_exp_upgrade': {'name': 'Perm Exp Upgrade', 'exp_increase': 10}
    }
POTIONS = {
    'potion': {'name': 'Potion', 'effect': 'heal', 'amount': 30},
    'strong_potion': {'name': 'Strong Potion', 'effect': 'heal', 'amount': 80},
    'ultra_potion': {'name': 'Ultra Potion', 'effect': 'heal', 'amount': 200},
    'strength_boost': {'name': 'Strength Boost', 'effect': 'buff_atk', 'amount': 5, 'duration': 4},
    'defense_boost': {'name': 'Defense Boost', 'effect': 'buff_def', 'amount': 3, 'duration': 4},
    'regen_potion': {'name': 'Regen Potion', 'effect': 'buff_hp_regen', 'amount': 12, 'duration': 4},
    'crit_boost': {'name': 'Crit Boost', 'effect': 'buff_crit', 'amount': 50, 'duration': 4},
    'mana_regen_potion': {'name': 'Mana Regen Potion', 'effect': 'buff_mana_regen', 'amount': 15, 'duration': 4},
    'instant_mana': {'name': 'Instant Mana', 'effect': 'full_mana'},
    'mana_upgrade_potion': {'name': 'Mana Upgrade Potion', 'effect': 'heal_mana', 'amount': 50}
    }
MATERIALS = {
    'slime_gel': {'name': 'Slime Gel', 'rarity': 'common', 'desc': 'Gelatinous substance from slimes.'},
    'goblin_tooth': {'name': 'Goblin Tooth', 'rarity': 'common', 'desc': 'Sharp tooth from goblins.'},
    'wolf_pelt': {'name': 'Wolf Pelt', 'rarity': 'common', 'desc': 'Fur from wolves.'},
    'skeleton_bone': {'name': 'Skeleton Bone', 'rarity': 'common', 'desc': 'Bone from skeletons.'},
    'orc_iron': {'name': 'Orc Iron', 'rarity': 'common', 'desc': 'Iron forged by orcs.'},
    'bandit_cloth': {'name': 'Bandit Cloth', 'rarity': 'common', 'desc': 'Cloth from bandits.'},
    'troll_core': {'name': 'Troll Core', 'rarity': 'rare', 'desc': 'Core from trolls.'},
    'dark_essence': {'name': 'Dark Essence', 'rarity': 'rare', 'desc': 'Essence of darkness.'},
    'prism_fragment': {'name': 'Prism Fragment', 'rarity': 'rare', 'desc': 'Fragment of a prism.'},
    'void_fragment': {'name': 'Void Fragment', 'rarity': 'rare', 'desc': 'Fragment from the void.'},
    'infinitium_piece': {'name': 'Infinitium Piece', 'rarity': 'rare', 'desc': 'Piece of infinitium.'},
    'soul_shard': {'name': 'Soul Shard', 'rarity': 'rare', 'desc': 'Shard containing souls.'},
    'transcendent_heart': {'name': 'Transcendent Heart', 'rarity': 'rare', 'desc': 'Heart from transcendent beings.'},
    'dragon_scale': {'name': 'Dragon Scale', 'rarity': 'mythical', 'desc': 'Scale from dragons.'},
    'phoenix_feather': {'name': 'Phoenix Feather', 'rarity': 'mythical', 'desc': 'Feather from phoenixes.'},
    'frozen_heart': {'name': 'Frozen Heart', 'rarity': 'mythical', 'desc': 'Heart encased in ice.'},
    'thunder_core': {'name': 'Thunder Core', 'rarity': 'mythical', 'desc': 'Core of thunder.'},
    'holy_light': {'name': 'Holy Light', 'rarity': 'mythical', 'desc': 'Light imbued with holiness.'},
    'demon_horn': {'name': 'Demon Horn', 'rarity': 'mythical', 'desc': 'Horn from demons.'},
    'crystal_shard': {'name': 'Crystal Shard', 'rarity': 'mythical', 'desc': 'Shard of crystal.'},
    'star_dust': {'name': 'Star Dust', 'rarity': 'mythical', 'desc': 'Dust from stars.'},
    'moon_rock': {'name': 'Moon Rock', 'rarity': 'mythical', 'desc': 'Rock from the moon.'},
    'sun_stone': {'name': 'Sun Stone', 'rarity': 'mythical', 'desc': 'Stone powered by the sun.'},
    'spider_venom': {'name': 'Spider Venom', 'rarity': 'common', 'desc': 'Venom from giant spiders.'},
    'stone_core': {'name': 'Stone Core', 'rarity': 'common', 'desc': 'Core from stone golems.'},
    'ice_shard': {'name': 'Ice Shard', 'rarity': 'common', 'desc': 'Shard of ice.'},
    'fire_essence': {'name': 'Fire Essence', 'rarity': 'rare', 'desc': 'Essence of fire.'},
    'lightning_feather': {'name': 'Lightning Feather', 'rarity': 'rare', 'desc': 'Feather charged with lightning.'},
    'shadow_cloak': {'name': 'Shadow Cloak', 'rarity': 'rare', 'desc': 'Cloak woven from shadows.'},
    'arcane_tome': {'name': 'Arcane Tome', 'rarity': 'rare', 'desc': 'Tome of arcane knowledge.'},
    'curse_scroll': {'name': 'Curse Scroll', 'rarity': 'rare', 'desc': 'Scroll with curses.'},
    'ember': {'name': 'Ember', 'rarity': 'rare', 'desc': 'Glowing ember.'},
    'bat_wing': {'name': 'Bat Wing', 'rarity': 'common', 'desc': 'Wing from dark bats.'}
    }
CRAFTABLE_WEAPONS = {
    "forged_goblin_dagger": {"name": "Forged Goblin Dagger", "atk": 8, "price": 0, "score_price": 0, "recipe": {"goblin_tooth": 3, "bandit_cloth": 1}, "type": "weapon", "desc": "Crude goblin dagger."},
    "forged_bone_sword": {"name": "Forged Bone Sword", "atk": 15, "price": 500, "recipe": {"skeleton_bone": 5, "orc_iron": 2}, "type": "weapon", "desc": "Sword made of bones."},
    "forged_troll_hammer": {"name": "Forged Troll Hammer", "atk": 40, "price": 2000, "recipe": {"troll_core": 1, "orc_iron": 3}, "type": "weapon", "desc": "Heavy hammer that hums."},
    "forged_frostblade": {"name": "Forged Frostblade", "atk": 120, "price": 5000, "score_price": 200, "recipe": {"frozen_heart": 2, "ice_shard": 5, "crystal_shard": 3}, "type": "weapon", "desc": "Blade imbued with ice power."},
    "forged_flameblade": {"name": "Forged Flameblade", "atk": 130, "price": 5500, "score_price": 250, "recipe": {"fire_essence": 2, "phoenix_feather": 1, "crystal_shard": 3}, "type": "weapon", "desc": "Blade imbued with fire power."},
    "forged_thunder_sword": {"name": "Forged Thunder Sword", "atk": 150, "price": 7000, "score_price": 400, "recipe": {"thunder_core": 2, "lightning_feather": 3, "crystal_shard": 4}, "type": "weapon", "desc": "Sword crackling with lightning."},
    "forged_holy_avenger": {"name": "Forged Holy Avenger", "atk": 1000, "price": 10000, "score_price": 800, "recipe": {"holy_light": 2, "sun_stone": 2, "moon_rock": 2}, "type": "weapon", "desc": "Blessed sword of light."},
    "forged_dragon_slayer": {"name": "Forged Dragon Slayer", "atk": 2500, "price": 15000, "score_price": 1500, "recipe": {"dragon_scale": 5, "thunder_core": 2, "infinitium_piece": 1}, "type": "weapon", "desc": "Legendary sword for dragon hunting."},
    "forged_cosmic_blade": {"name": "Forged Cosmic Blade", "atk": 5000, "price": 30000, "score_price": 3000, "recipe": {"star_dust": 5, "void_fragment": 3, "infinitium_piece": 2}, "type": "weapon", "desc": "Blade forged from cosmic materials."},
    "forged_transcendent_edge": {"name": "Forged Transcendent Edge", "atk": 6000, "price": 100000, "score_price": 10000, "recipe": {"transcendent_heart": 1, "void_fragment": 5, "infinitium_piece": 3, "soul_shard": 2}, "type": "weapon", "desc": "Weapon beyond mortal comprehension."},
    }

CRAFTABLE_ARMORS = {
    "forged_goblin_armor": {"name": "Forged Goblin Armor", "def": 2, "price": 0, "recipe": {"goblin_tooth": 3, "bandit_cloth": 2}, "type": "armor", "desc": "Crude goblin armor."},
    "forged_bone_armor": {"name": "Forged Bone Armor", "def": 8, "price": 500, "recipe": {"skeleton_bone": 5, "orc_iron": 2}, "type": "armor", "desc": "Armor made of bones."},
    "forged_troll_armor": {"name": "Forged Troll Armor", "def": 20, "price": 2000, "recipe": {"troll_core": 1, "orc_iron": 3}, "type": "armor", "desc": "Heavy armor that regenerates."},
    "forged_frost_armor": {"name": "Forged Frost Armor", "def": 40, "price": 4000, "score_price": 150, "recipe": {"frozen_heart": 2, "ice_shard": 5, "crystal_shard": 3}, "type": "armor", "desc": "Armor imbued with ice power."},
    "forged_flame_armor": {"name": "Forged Flame Armor", "def": 45, "price": 4500, "score_price": 200, "recipe": {"fire_essence": 2, "phoenix_feather": 1, "crystal_shard": 3}, "type": "armor", "desc": "Armor imbued with fire power."},
    "forged_thunder_armor": {"name": "Forged Thunder Armor", "def": 55, "price": 6000, "score_price": 350, "recipe": {"thunder_core": 2, "lightning_feather": 3, "crystal_shard": 4}, "type": "armor", "desc": "Armor crackling with lightning."},
    "forged_holy_armor": {"name": "Forged Holy Armor", "def": 70, "price": 9000, "score_price": 700, "recipe": {"holy_light": 2, "sun_stone": 2, "moon_rock": 2}, "type": "armor", "desc": "Blessed armor of light."},
    "forged_dragon_scale_armor": {"name": "Forged Dragon Scale Armor", "def": 100, "price": 14000, "score_price": 1400, "recipe": {"dragon_scale": 5, "thunder_core": 2, "infinitium_piece": 1}, "type": "armor", "desc": "Legendary armor made of dragon scales."},
    "forged_cosmic_armor": {"name": "Forged Cosmic Armor", "def": 200, "price": 28000, "score_price": 2800, "recipe": {"star_dust": 5, "void_fragment": 3, "infinitium_piece": 2}, "type": "armor", "desc": "Armor forged from cosmic materials."},
    "forged_transcendent_armor": {"name": "Forged Transcendent Armor", "def": 500, "price": 95000, "score_price": 9500, "recipe": {"transcendent_heart": 1, "void_fragment": 5, "infinitium_piece": 3, "soul_shard": 2}, "type": "armor", "desc": "Armor beyond mortal comprehension."},
    }

CRAFTABLE_WANDS = {
    "forged_goblin_wand": {"name": "Forged Goblin Wand", "magic_power": 8, "price": 0, "score_price": 0, "recipe": {"goblin_tooth": 3, "bandit_cloth": 1}, "type": "wand", "desc": "Crude goblin wand."},
    "forged_bone_wand": {"name": "Forged Bone Wand", "magic_power": 15, "price": 500, "recipe": {"skeleton_bone": 5, "orc_iron": 2}, "type": "wand", "desc": "Wand made of bones."},
    "forged_troll_staff": {"name": "Forged Troll Staff", "magic_power": 40, "price": 2000, "recipe": {"troll_core": 1, "orc_iron": 3}, "type": "wand", "desc": "Heavy staff that hums."},
    "forged_frost_wand": {"name": "Forged Frost Wand", "magic_power": 60, "price": 4000, "score_price": 150, "recipe": {"frozen_heart": 2, "ice_shard": 5, "crystal_shard": 3}, "type": "wand", "desc": "Wand imbued with ice power."},
    "forged_flame_wand": {"name": "Forged Flame Wand", "magic_power": 65, "price": 4500, "score_price": 200, "recipe": {"fire_essence": 2, "phoenix_feather": 1, "crystal_shard": 3}, "type": "wand", "desc": "Wand imbued with fire power."},
    "forged_thunder_wand": {"name": "Forged Thunder Wand", "magic_power": 75, "price": 6000, "score_price": 350, "recipe": {"thunder_core": 2, "lightning_feather": 3, "crystal_shard": 4}, "type": "wand", "desc": "Wand crackling with lightning."},
    "forged_holy_scepter": {"name": "Forged Holy Scepter", "magic_power": 90, "price": 9000, "score_price": 700, "recipe": {"holy_light": 2, "sun_stone": 2, "moon_rock": 2}, "type": "wand", "desc": "Blessed scepter of light."},
    "forged_dragon_staff": {"name": "Forged Dragon Staff", "magic_power": 125, "price": 14000, "score_price": 1400, "recipe": {"dragon_scale": 5, "thunder_core": 2, "infinitium_piece": 1}, "type": "wand", "desc": "Legendary staff of dragon power."},
    "forged_cosmic_scepter": {"name": "Forged Cosmic Scepter", "magic_power": 250, "price": 28000, "score_price": 2800, "recipe": {"star_dust": 5, "void_fragment": 3, "infinitium_piece": 2}, "type": "wand", "desc": "Scepter forged from cosmic materials."},
    "forged_transcendent_staff": {"name": "Forged Transcendent Staff", "magic_power": 750, "price": 95000, "score_price": 9500, "recipe": {"transcendent_heart": 1, "void_fragment": 5, "infinitium_piece": 3, "soul_shard": 2}, "type": "wand", "desc": "Staff beyond mortal comprehension."},
    }

CRAFTABLE_ROBES = {
    "forged_goblin_robe": {"name": "Forged Goblin Robe", "magic_def": 2, "price": 0, "recipe": {"goblin_tooth": 2, "bandit_cloth": 3}, "type": "robe", "desc": "Crude goblin robe."},
    "forged_bone_robe": {"name": "Forged Bone Robe", "magic_def": 8, "price": 500, "recipe": {"skeleton_bone": 5, "orc_iron": 2}, "type": "robe", "desc": "Robe made of bones."},
    "forged_troll_robe": {"name": "Forged Troll Robe", "magic_def": 20, "price": 2000, "recipe": {"troll_core": 1, "orc_iron": 3}, "type": "robe", "desc": "Heavy robe that regenerates."},
    "forged_frost_robe": {"name": "Forged Frost Robe", "magic_def": 30, "price": 4000, "score_price": 150, "recipe": {"frozen_heart": 2, "ice_shard": 5, "crystal_shard": 3}, "type": "robe", "desc": "Robe imbued with ice power."},
    "forged_flame_robe": {"name": "Forged Flame Robe", "magic_def": 35, "price": 4500, "score_price": 200, "recipe": {"fire_essence": 2, "phoenix_feather": 1, "crystal_shard": 3}, "type": "robe", "desc": "Robe imbued with fire power."},
    "forged_thunder_robe": {"name": "Forged Thunder Robe", "magic_def": 45, "price": 6000, "score_price": 350, "recipe": {"thunder_core": 2, "lightning_feather": 3, "crystal_shard": 4}, "type": "robe", "desc": "Robe crackling with lightning."},
    "forged_holy_robe": {"name": "Forged Holy Robe", "magic_def": 60, "price": 9000, "score_price": 700, "recipe": {"holy_light": 2, "sun_stone": 2, "moon_rock": 2}, "type": "robe", "desc": "Blessed robe of light."},
    "forged_dragon_robe": {"name": "Forged Dragon Robe", "magic_def": 90, "price": 14000, "score_price": 1400, "recipe": {"dragon_scale": 5, "thunder_core": 2, "infinitium_piece": 1}, "type": "robe", "desc": "Legendary robe of dragon power."},
    "forged_cosmic_robe": {"name": "Forged Cosmic Robe", "magic_def": 180, "price": 28000, "score_price": 2800, "recipe": {"star_dust": 5, "void_fragment": 3, "infinitium_piece": 2}, "type": "robe", "desc": "Robe forged from cosmic materials."},
    "forged_transcendent_robe": {"name": "Forged Transcendent Robe", "magic_def": 450, "price": 95000, "score_price": 9500, "recipe": {"transcendent_heart": 1, "void_fragment": 5, "infinitium_piece": 3, "soul_shard": 2}, "type": "robe", "desc": "Robe beyond mortal comprehension."},
    }

CRAFTABLE_NECKLACES = {
    "health_amulet": {"name": "Health Amulet", "hp_bonus": 20, "price": 500, "recipe": {"slime_gel": 3, "wolf_pelt": 2}, "type": "necklace", "desc": "Amulet that boosts health."},
    "mana_amulet": {"name": "Mana Amulet", "mana_bonus": 15, "price": 600, "recipe": {"crystal_shard": 3, "slime_gel": 2}, "type": "necklace", "desc": "Amulet that boosts mana."},
    "strength_amulet": {"name": "Strength Amulet", "atk_bonus": 5, "price": 700, "recipe": {"goblin_tooth": 3, "wolf_pelt": 2}, "type": "necklace", "desc": "Amulet that boosts attack."},
    "defense_amulet": {"name": "Defense Amulet", "def_bonus": 3, "price": 650, "recipe": {"skeleton_bone": 3, "slime_gel": 2}, "type": "necklace", "desc": "Amulet that boosts defense."},
    "crit_amulet": {"name": "Critical Amulet", "crit_bonus": 10, "price": 800, "recipe": {"bandit_cloth": 3, "crystal_shard": 2}, "type": "necklace", "desc": "Amulet that boosts critical chance."},
    "lifesteal_amulet": {"name": "Lifesteal Amulet", "lifesteal_bonus": 5, "price": 900, "recipe": {"spider_venom": 2, "bat_wing": 2}, "type": "necklace", "desc": "Amulet that provides lifesteal."},
    "forged_frost_necklace": {"name": "Forged Frost Necklace", "magic_def_bonus": 15, "hp_bonus": 30, "price": 3000, "score_price": 100, "recipe": {"frozen_heart": 1, "ice_shard": 3, "crystal_shard": 2}, "type": "necklace", "desc": "Necklace imbued with ice power."},
    "forged_flame_necklace": {"name": "Forged Flame Necklace", "magic_atk_bonus": 10, "atk_bonus": 8, "price": 3500, "score_price": 150, "recipe": {"fire_essence": 1, "phoenix_feather": 1, "crystal_shard": 2}, "type": "necklace", "desc": "Necklace imbued with fire power."},
    "forged_thunder_necklace": {"name": "Forged Thunder Necklace", "crit_bonus": 15, "atk_bonus": 10, "price": 5000, "score_price": 300, "recipe": {"thunder_core": 1, "lightning_feather": 3, "crystal_shard": 2}, "type": "necklace", "desc": "Necklace crackling with lightning."},
    "forged_holy_pendant": {"name": "Forged Holy Pendant", "hp_bonus": 50, "mana_bonus": 30, "def_bonus": 5, "price": 8000, "score_price": 600, "recipe": {"holy_light": 1, "sun_stone": 2, "moon_rock": 2}, "type": "necklace", "desc": "Blessed pendant of light."},
    "forged_dragon_necklace": {"name": "Forged Dragon Necklace", "atk_bonus": 20, "def_bonus": 15, "hp_bonus": 70, "price": 12000, "score_price": 1200, "recipe": {"dragon_scale": 3, "thunder_core": 1, "infinitium_piece": 1}, "type": "necklace", "desc": "Legendary necklace of dragon power."},
    "forged_cosmic_necklace": {"name": "Forged Cosmic Necklace", "magic_atk_bonus": 30, "magic_def_bonus": 25, "mana_bonus": 50, "price": 24000, "score_price": 2400, "recipe": {"star_dust": 3, "void_fragment": 2, "infinitium_piece": 1}, "type": "necklace", "desc": "Necklace forged from cosmic materials."},
    "forged_transcendent_necklace": {"name": "Forged Transcendent Necklace", "atk_bonus": 50, "def_bonus": 40, "hp_bonus": 150, "mana_bonus": 100, "crit_bonus": 20, "lifesteal_bonus": 10, "price": 80000, "score_price": 8000, "recipe": {"transcendent_heart": 1, "void_fragment": 3, "infinitium_piece": 2, "soul_shard": 1}, "type": "necklace", "desc": "Necklace beyond mortal comprehension."},
    }

WEAPONS = {
    'wooden_sword': {'name': 'Wooden Sword', 'atk': 2, 'price': 50, 'score_price': 0},
    'iron_sword': {'name': 'Iron Sword', 'atk': 5, 'price': 150, 'score_price': 0},
    'steel_sword': {'name': 'Steel Sword', 'atk': 8, 'price': 300, 'score_price': 0},
    'diamond_sword': {'name': 'Diamond Sword', 'atk': 50, 'price': 2000, 'score_price': 0},
    'void_sword': {'name': 'Void Sword', 'atk': 200, 'price': 8000, 'score_price': 0},
    'infinitium_sword': {'name': 'Infinitium Sword', 'atk': 2000, 'price': 800000, 'score_price': 25000},
    'frostblade': {'name': 'Frostblade', 'atk': 120, 'price': 5000, 'score_price': 200},
    'flameblade': {'name': 'Flameblade', 'atk': 130, 'price': 5500, 'score_price': 250},
    'thunder_sword': {'name': 'Thunder Sword', 'atk': 150, 'price': 7000, 'score_price': 400},
    'holy_avenger': {'name': 'Holy Avenger', 'atk': 180, 'price': 7500, 'score_price': 800},
    'dragon_slayer': {'name': 'Dragon Slayer', 'atk': 250, 'price': 15000, 'score_price': 1500},
    'cosmic_blade': {'name': 'Cosmic Blade', 'atk': 500, 'price': 30000, 'score_price': 3000},
    'transcendent_edge': {'name': 'Transcendent Edge', 'atk': 1500, 'price': 500000, 'score_price': 10000}
    }

ARMORS = {
    'leather_armor': {'name': 'Leather Armor', 'def': 1, 'price': 50},
    'chainmail': {'name': 'Chainmail', 'def': 3, 'price': 150},
    'plate_armor': {'name': 'Plate Armor', 'def': 6, 'price': 300},
    'diamond_armor': {'name': 'Diamond Armor', 'def': 25, 'price': 2000},
    'void_armor': {'name': 'Void Armor', 'def': 75, 'price': 8000},
    'infinitium_armor': {'name': 'Infinitium Armor', 'def': 300, 'price': 800000, 'score_price': 2500},
    'frost_armor': {'name': 'Frost Armor', 'def': 40, 'price': 4000, 'score_price': 150},
    'flame_armor': {'name': 'Flame Armor', 'def': 45, 'price': 4500, 'score_price': 200},
    'thunder_armor': {'name': 'Thunder Armor', 'def': 55, 'price': 6000, 'score_price': 350},
    'holy_armor': {'name': 'Holy Armor', 'def': 70, 'price': 9000, 'score_price': 700},
    'dragon_scale_armor': {'name': 'Dragon Scale Armor', 'def': 100, 'price': 14000, 'score_price': 1400},
    'cosmic_armor': {'name': 'Cosmic Armor', 'def': 200, 'price': 280000, 'score_price': 2800},
    'transcendent_armor': {'name': 'Transcendent Armor', 'def': 500, 'price': 950000, 'score_price': 9500}
    }

WANDS = {
    'apprentice_wand': {'name': 'Apprentice Wand', 'magic_atk': 5, 'price': 120},
    'mage_wand': {'name': 'Mage Wand', 'magic_atk': 20, 'price': 800},
    'archmage_staff': {'name': 'Archmage Staff', 'magic_atk': 120, 'price': 12000, 'score_price': 200},
    'frost_wand': {'name': 'Frost Wand', 'magic_atk': 60, 'price': 4000, 'score_price': 150},
    'flame_wand': {'name': 'Flame Wand', 'magic_atk': 65, 'price': 4500, 'score_price': 200},
    'thunder_wand': {'name': 'Thunder Wand', 'magic_atk': 75, 'price': 6000, 'score_price': 350},
    'holy_scepter': {'name': 'Holy Scepter', 'magic_atk': 90, 'price': 9000, 'score_price': 700},
    'dragon_staff': {'name': 'Dragon Staff', 'magic_atk': 125, 'price': 14000, 'score_price': 1400},
    'cosmic_scepter': {'name': 'Cosmic Scepter', 'magic_atk': 250, 'price': 28000, 'score_price': 2800},
    'transcendent_staff': {'name': 'Transcendent Staff', 'magic_atk': 750, 'price': 95000, 'score_price': 9500}
    }

ROBES = {
    'cloth_robe': {'name': 'Cloth Robe', 'magic_def': 2, 'price': 100},
    'silk_robe': {'name': 'Silk Robe', 'magic_def': 10, 'price': 900},
    'void_robe': {'name': 'Void Robe', 'magic_def': 80, 'price': 20000, 'score_price': 500},
    'frost_robe': {'name': 'Frost Robe', 'magic_def': 30, 'price': 4000, 'score_price': 150},
    'flame_robe': {'name': 'Flame Robe', 'magic_def': 35, 'price': 4500, 'score_price': 200},
    'thunder_robe': {'name': 'Thunder Robe', 'magic_def': 45, 'price': 6000, 'score_price': 350},
    'holy_robe': {'name': 'Holy Robe', 'magic_def': 60, 'price': 9000, 'score_price': 700},
    'dragon_robe': {'name': 'Dragon Robe', 'magic_def': 90, 'price': 14000, 'score_price': 1400},
    'cosmic_robe': {'name': 'Cosmic Robe', 'magic_def': 180, 'price': 28000, 'score_price': 2800},
    'transcendent_robe': {'name': 'Transcendent Robe', 'magic_def': 450, 'price': 95000, 'score_price': 9500}
    }

NECKLACES = {
    'health_amulet': {'name': 'Health Amulet', 'hp_bonus': 20, 'price': 500},
    'mana_amulet': {'name': 'Mana Amulet', 'mana_bonus': 15, 'price': 600},
    'strength_amulet': {'name': 'Strength Amulet', 'atk_bonus': 5, 'price': 700},
    'defense_amulet': {'name': 'Defense Amulet', 'def_bonus': 3, 'price': 650},
    'crit_amulet': {'name': 'Critical Amulet', 'crit_bonus': 10, 'price': 800},
    'lifesteal_amulet': {'name': 'Lifesteal Amulet', 'lifesteal_bonus': 5, 'price': 900},
    'frost_necklace': {'name': 'Frost Necklace', 'magic_def_bonus': 15, 'hp_bonus': 30, 'price': 3000, 'score_price': 100},
    'flame_necklace': {'name': 'Flame Necklace', 'magic_atk_bonus': 10, 'atk_bonus': 8, 'price': 3500, 'score_price': 150},
    'thunder_necklace': {'name': 'Thunder Necklace', 'crit_bonus': 15, 'atk_bonus': 10, 'price': 5000, 'score_price': 300},
    'holy_pendant': {'name': 'Holy Pendant', 'hp_bonus': 50, 'mana_bonus': 30, 'def_bonus': 5, 'price': 8000, 'score_price': 600},
    'dragon_necklace': {'name': 'Dragon Necklace', 'atk_bonus': 20, 'def_bonus': 15, 'hp_bonus': 70, 'price': 12000, 'score_price': 1200},
    'cosmic_necklace': {'name': 'Cosmic Necklace', 'magic_atk_bonus': 30, 'magic_def_bonus': 25, 'mana_bonus': 50, 'price': 24000, 'score_price': 2400},
    'transcendent_necklace': {'name': 'Transcendent Necklace', 'atk_bonus': 50, 'def_bonus': 40, 'hp_bonus': 150, 'mana_bonus': 100, 'crit_bonus': 20, 'lifesteal_bonus': 10, 'price': 800000, 'score_price': 8000}
    }

# Integrate craftable items into existing dictionaries
for craftable in [CRAFTABLE_WEAPONS, CRAFTABLE_ARMORS, CRAFTABLE_WANDS, CRAFTABLE_ROBES, CRAFTABLE_NECKLACES]:
    for item_key, item_data in craftable.items():
        category = item_data.get('type')
        item_dict = {k: v for k, v in item_data.items() if k not in ['recipe', 'type']}
        if category == 'weapon':
            WEAPONS[item_key] = item_dict
        elif category == 'armor':
            ARMORS[item_key] = item_dict
        elif category == 'wand':
            if 'magic_power' in item_dict:
                item_dict['magic_atk'] = item_dict.pop('magic_power')
            WANDS[item_key] = item_dict
        elif category == 'robe':
            ROBES[item_key] = item_dict
        elif category == 'necklace':
            NECKLACES[item_key] = item_dict
WEAPONS = {
    'wooden_sword': {'name': 'Wooden Sword', 'atk': 2, 'price': 50, 'score_price': 0},
    'iron_sword': {'name': 'Iron Sword', 'atk': 5, 'price': 150, 'score_price': 0},
    'steel_sword': {'name': 'Steel Sword', 'atk': 8, 'price': 300, 'score_price': 0},
    'diamond_sword': {'name': 'Diamond Sword', 'atk': 50, 'price': 2000, 'score_price': 0},
    'void_sword': {'name': 'Void Sword', 'atk': 200, 'price': 8000, 'score_price': 0},
    'infinitium_sword': {'name': 'Infinitium Sword', 'atk': 2000, 'price': 800000, 'score_price': 25000},
    'frostblade': {'name': 'Frostblade', 'atk': 120, 'price': 5000, 'score_price': 200},
    'flameblade': {'name': 'Flameblade', 'atk': 130, 'price': 5500, 'score_price': 250},
    'thunder_sword': {'name': 'Thunder Sword', 'atk': 150, 'price': 7000, 'score_price': 400},
    'holy_avenger': {'name': 'Holy Avenger', 'atk': 180, 'price': 7500, 'score_price': 800},
    'dragon_slayer': {'name': 'Dragon Slayer', 'atk': 250, 'price': 15000, 'score_price': 1500},
    'cosmic_blade': {'name': 'Cosmic Blade', 'atk': 500, 'price': 30000, 'score_price': 3000},
    'transcendent_edge': {'name': 'Transcendent Edge', 'atk': 1500, 'price': 500000, 'score_price': 10000}
    }
ARMORS = {
    'leather_armor': {'name': 'Leather Armor', 'def': 1, 'price': 50},
    'chainmail': {'name': 'Chainmail', 'def': 3, 'price': 150},
    'plate_armor': {'name': 'Plate Armor', 'def': 6, 'price': 300},
    'diamond_armor': {'name': 'Diamond Armor', 'def': 25, 'price': 2000},
    'void_armor': {'name': 'Void Armor', 'def': 75, 'price': 8000},
    'infinitium_armor': {'name': 'Infinitium Armor', 'def': 300, 'price': 800000, 'score_price': 2500},
    'frost_armor': {'name': 'Frost Armor', 'def': 40, 'price': 4000, 'score_price': 150},
    'flame_armor': {'name': 'Flame Armor', 'def': 45, 'price': 4500, 'score_price': 200},
    'thunder_armor': {'name': 'Thunder Armor', 'def': 55, 'price': 6000, 'score_price': 350},
    'holy_armor': {'name': 'Holy Armor', 'def': 70, 'price': 9000, 'score_price': 700},
    'dragon_scale_armor': {'name': 'Dragon Scale Armor', 'def': 100, 'price': 14000, 'score_price': 1400},
    'cosmic_armor': {'name': 'Cosmic Armor', 'def': 200, 'price': 280000, 'score_price': 2800},
    'transcendent_armor': {'name': 'Transcendent Armor', 'def': 500, 'price': 950000, 'score_price': 9500}
    }
WANDS = {
    'apprentice_wand': {'name': 'Apprentice Wand', 'magic_atk': 5, 'price': 120},
    'mage_wand': {'name': 'Mage Wand', 'magic_atk': 20, 'price': 800},
    'archmage_staff': {'name': 'Archmage Staff', 'magic_atk': 120, 'price': 12000, 'score_price': 200},
    'frost_wand': {'name': 'Frost Wand', 'magic_atk': 60, 'price': 4000, 'score_price': 150},
    'flame_wand': {'name': 'Flame Wand', 'magic_atk': 65, 'price': 4500, 'score_price': 200},
    'thunder_wand': {'name': 'Thunder Wand', 'magic_atk': 75, 'price': 6000, 'score_price': 350},
    'holy_scepter': {'name': 'Holy Scepter', 'magic_atk': 90, 'price': 9000, 'score_price': 700},
    'dragon_staff': {'name': 'Dragon Staff', 'magic_atk': 125, 'price': 14000, 'score_price': 1400},
    'cosmic_scepter': {'name': 'Cosmic Scepter', 'magic_atk': 250, 'price': 28000, 'score_price': 2800},
    'transcendent_staff': {'name': 'Transcendent Staff', 'magic_atk': 750, 'price': 95000, 'score_price': 9500}
    }
ROBES = {
    'cloth_robe': {'name': 'Cloth Robe', 'magic_def': 2, 'price': 100},
    'silk_robe': {'name': 'Silk Robe', 'magic_def': 10, 'price': 900},
    'void_robe': {'name': 'Void Robe', 'magic_def': 80, 'price': 20000, 'score_price': 500},
    'frost_robe': {'name': 'Frost Robe', 'magic_def': 30, 'price': 4000, 'score_price': 150},
    'flame_robe': {'name': 'Flame Robe', 'magic_def': 35, 'price': 4500, 'score_price': 200},
    'thunder_robe': {'name': 'Thunder Robe', 'magic_def': 45, 'price': 6000, 'score_price': 350},
    'holy_robe': {'name': 'Holy Robe', 'magic_def': 60, 'price': 9000, 'score_price': 700},
    'dragon_robe': {'name': 'Dragon Robe', 'magic_def': 90, 'price': 14000, 'score_price': 1400},
    'cosmic_robe': {'name': 'Cosmic Robe', 'magic_def': 180, 'price': 28000, 'score_price': 2800},
    'transcendent_robe': {'name': 'Transcendent Robe', 'magic_def': 450, 'price': 95000, 'score_price': 9500}
    }
NECKLACES = {
    'health_amulet': {'name': 'Health Amulet', 'hp_bonus': 20, 'price': 500},
    'mana_amulet': {'name': 'Mana Amulet', 'mana_bonus': 15, 'price': 600},
    'strength_amulet': {'name': 'Strength Amulet', 'atk_bonus': 5, 'price': 700},
    'defense_amulet': {'name': 'Defense Amulet', 'def_bonus': 3, 'price': 650},
    'crit_amulet': {'name': 'Critical Amulet', 'crit_bonus': 10, 'price': 800},
    'lifesteal_amulet': {'name': 'Lifesteal Amulet', 'lifesteal_bonus': 5, 'price': 900},
    'frost_necklace': {'name': 'Frost Necklace', 'magic_def_bonus': 15, 'hp_bonus': 30, 'price': 3000, 'score_price': 100},
    'flame_necklace': {'name': 'Flame Necklace', 'magic_atk_bonus': 10, 'atk_bonus': 8, 'price': 3500, 'score_price': 150},
    'thunder_necklace': {'name': 'Thunder Necklace', 'crit_bonus': 15, 'atk_bonus': 10, 'price': 5000, 'score_price': 300},
    'holy_pendant': {'name': 'Holy Pendant', 'hp_bonus': 50, 'mana_bonus': 30, 'def_bonus': 5, 'price': 8000, 'score_price': 600},
    'dragon_necklace': {'name': 'Dragon Necklace', 'atk_bonus': 20, 'def_bonus': 15, 'hp_bonus': 70, 'price': 12000, 'score_price': 1200},
    'cosmic_necklace': {'name': 'Cosmic Necklace', 'magic_atk_bonus': 30, 'magic_def_bonus': 25, 'mana_bonus': 50, 'price': 24000, 'score_price': 2400},
    'transcendent_necklace': {'name': 'Transcendent Necklace', 'atk_bonus': 50, 'def_bonus': 40, 'hp_bonus': 150, 'mana_bonus': 100, 'crit_bonus': 20, 'lifesteal_bonus': 10, 'price': 800000, 'score_price': 8000}
    }

def get_rarity_value(rarity):
    """Get numerical value for rarity sorting"""
    rarity_order = {'common': 1, 'rare': 2, 'mythical': 3, 'prismatic': 4, 'divine': 5, 'transcendent': 6}
    return rarity_order.get(rarity, 0)

def get_item_rarity(item_key):
    """Get the rarity of an item"""
    if item_key in WEAPONS:
        if 'score_price' in WEAPONS[item_key]:
            if WEAPONS[item_key].get('score_price', 0) >= 10000:
                return 'transcendent'
            elif WEAPONS[item_key].get('score_price', 0) >= 3000:
                return 'divine'
            elif WEAPONS[item_key].get('score_price', 0) >= 800:
                return 'prismatic'
            elif WEAPONS[item_key].get('score_price', 0) >= 250:
                return 'mythical'
            elif WEAPONS[item_key].get('score_price', 0) >= 200:
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
    elif item_key in ARMORS:
        if 'score_price' in ARMORS[item_key]:
            if ARMORS[item_key].get('score_price', 0) >= 9500:
                return 'transcendent'
            elif ARMORS[item_key].get('score_price', 0) >= 2800:
                return 'divine'
            elif ARMORS[item_key].get('score_price', 0) >= 1400:
                return 'prismatic'
            elif ARMORS[item_key].get('score_price', 0) >= 700:
                return 'mythical'
            elif ARMORS[item_key].get('score_price', 0) >= 200:
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
    elif item_key in WANDS:
        if 'score_price' in WANDS[item_key]:
            if WANDS[item_key].get('score_price', 0) >= 9500:
                return 'transcendent'
            elif WANDS[item_key].get('score_price', 0) >= 2800:
                return 'divine'
            elif WANDS[item_key].get('score_price', 0) >= 1400:
                return 'prismatic'
            elif WANDS[item_key].get('score_price', 0) >= 700:
                return 'mythical'
            elif WANDS[item_key].get('score_price', 0) >= 200:
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
    elif item_key in ROBES:
        if 'score_price' in ROBES[item_key]:
            if ROBES[item_key].get('score_price', 0) >= 9500:
                return 'transcendent'
            elif ROBES[item_key].get('score_price', 0) >= 2800:
                return 'divine'
            elif ROBES[item_key].get('score_price', 0) >= 1400:
                return 'prismatic'
            elif ROBES[item_key].get('score_price', 0) >= 700:
                return 'mythical'
            elif ROBES[item_key].get('score_price', 0) >= 200:
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
    elif item_key in NECKLACES:
        if 'score_price' in NECKLACES[item_key]:
            if NECKLACES[item_key].get('score_price', 0) >= 8000:
                return 'transcendent'
            elif NECKLACES[item_key].get('score_price', 0) >= 2400:
                return 'divine'
            elif NECKLACES[item_key].get('score_price', 0) >= 1200:
                return 'prismatic'
            elif NECKLACES[item_key].get('score_price', 0) >= 600:
                return 'mythical'
            elif NECKLACES[item_key].get('score_price', 0) >= 100:
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
    elif item_key in POTIONS:
        return 'common'
    elif item_key in PERM_UPGRADES:
        return 'rare'
    elif item_key in MATERIALS:
        return MATERIALS[item_key]['rarity']
    else:
        return 'common'
TITLES = {
    'novice': {'name': 'Novice', 'rarity': 'common', 'atk_boost': 0, 'def_boost': 0, 'hp_boost': 0, 'mana_boost': 0, 'exp_boost': 0, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'A beginner adventurer'},
    'apprentice': {'name': 'Apprentice', 'rarity': 'common', 'atk_boost': 1, 'def_boost': 1, 'hp_boost': 5, 'mana_boost': 5, 'exp_boost': 0, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Learning the ways of combat'},
    'warrior': {'name': 'Warrior', 'rarity': 'common', 'atk_boost': 2, 'def_boost': 2, 'hp_boost': 10, 'mana_boost': 0, 'exp_boost': 0, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'A skilled fighter'},
    'champion': {'name': 'Champion', 'rarity': 'rare', 'atk_boost': 3, 'def_boost': 3, 'hp_boost': 15, 'mana_boost': 10, 'exp_boost': 5, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'A true hero'},
    'legend': {'name': 'Legend', 'rarity': 'rare', 'atk_boost': 4, 'def_boost': 4, 'hp_boost': 20, 'mana_boost': 15, 'exp_boost': 10, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Known throughout the lands'},
    'master': {'name': 'Master', 'rarity': 'rare', 'atk_boost': 5, 'def_boost': 5, 'hp_boost': 25, 'mana_boost': 20, 'exp_boost': 15, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'A master of their craft'},
    'grandmaster': {'name': 'Grandmaster', 'rarity': 'mythical', 'atk_boost': 6, 'def_boost': 6, 'hp_boost': 30, 'mana_boost': 25, 'exp_boost': 20, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'A supreme expert'},
    'slayer': {'name': 'Slayer', 'rarity': 'mythical', 'atk_boost': 7, 'def_boost': 7, 'hp_boost': 35, 'mana_boost': 30, 'exp_boost': 25, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 10, 'def_percent': 5, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Monster slayer extraordinaire'},
    'hunter': {'name': 'Hunter', 'rarity': 'mythical', 'atk_boost': 8, 'def_boost': 8, 'hp_boost': 40, 'mana_boost': 35, 'exp_boost': 30, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 20, 'def_percent': 10, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Master hunter'},
    'slayer_ii': {'name': 'Slayer II', 'rarity': 'prismatic', 'atk_boost': 9, 'def_boost': 9, 'hp_boost': 45, 'mana_boost': 40, 'exp_boost': 35, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 25, 'def_percent': 15, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Legendary monster slayer'},
    'boss_slayer': {'name': 'Boss Slayer', 'rarity': 'prismatic', 'atk_boost': 10, 'def_boost': 10, 'hp_boost': 50, 'mana_boost': 45, 'exp_boost': 40, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 30, 'def_percent': 20, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Boss defeating champion'},
    'boss_master': {'name': 'Boss Master', 'rarity': 'prismatic', 'atk_boost': 11, 'def_boost': 11, 'hp_boost': 55, 'mana_boost': 50, 'exp_boost': 45, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 35, 'def_percent': 25, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Master of bosses'},
    'millionaire': {'name': 'Millionaire', 'rarity': 'divine', 'atk_boost': 12, 'def_boost': 12, 'hp_boost': 60, 'mana_boost': 55, 'exp_boost': 50, 'material_discount_percent': 0, 'money_boost_percent': 20, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Extremely wealthy'},
    'arcane_master': {'name': 'Arcane Master', 'rarity': 'divine', 'atk_boost': 13, 'def_boost': 13, 'hp_boost': 65, 'mana_boost': 60, 'exp_boost': 55, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 10, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 20, 'desc': 'Master of magic'},
    'artisan': {'name': 'Artisan', 'rarity': 'divine', 'atk_boost': 14, 'def_boost': 14, 'hp_boost': 70, 'mana_boost': 65, 'exp_boost': 60, 'material_discount_percent': 20, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Master craftsman'},
    'collector': {'name': 'Collector', 'rarity': 'transcendent', 'atk_boost': 15, 'def_boost': 15, 'hp_boost': 75, 'mana_boost': 70, 'exp_boost': 65, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 20, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Ultimate collector'},
    'immortal': {'name': 'Immortal', 'rarity': 'transcendent', 'atk_boost': 16, 'def_boost': 16, 'hp_boost': 80, 'mana_boost': 75, 'exp_boost': 70, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': -30, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Has cheated death many times'},
    'perfect': {'name': 'Perfect', 'rarity': 'transcendent', 'atk_boost': 17, 'def_boost': 17, 'hp_boost': 85, 'mana_boost': 80, 'exp_boost': 75, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 10, 'def_percent': 10, 'hp_percent': 20, 'mana_percent': 20, 'desc': 'Achieved perfection'},
    'legendary': {'name': 'Legendary', 'rarity': 'transcendent', 'atk_boost': 18, 'def_boost': 18, 'hp_boost': 90, 'mana_boost': 85, 'exp_boost': 80, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 30, 'def_percent': 30, 'hp_percent': 20, 'mana_percent': 0, 'desc': 'A living legend'},
    'deity': {'name': 'Deity', 'rarity': 'transcendent', 'atk_boost': 19, 'def_boost': 19, 'hp_boost': 95, 'mana_boost': 90, 'exp_boost': 85, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 40, 'def_percent': 40, 'hp_percent': 30, 'mana_percent': 30, 'desc': 'God among men'},
    'treasure_king': {'name': 'Treasure King', 'rarity': 'transcendent', 'atk_boost': 20, 'def_boost': 20, 'hp_boost': 100, 'mana_boost': 95, 'exp_boost': 90, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 20, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Master of treasures'},
    'fortunes_favorite': {'name': "Fortune's Favorite", 'rarity': 'transcendent', 'atk_boost': 21, 'def_boost': 21, 'hp_boost': 105, 'mana_boost': 100, 'exp_boost': 95, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 20, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Always lucky'},
    'mytic': {'name': 'Mythic', 'rarity': 'mythical', 'atk_boost': 8, 'def_boost': 8, 'hp_boost': 40, 'mana_boost': 35, 'exp_boost': 30, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Mythical being'},
    'transcendent': {'name': 'Transcendent', 'rarity': 'transcendent', 'atk_boost': 15, 'def_boost': 15, 'hp_boost': 75, 'mana_boost': 70, 'exp_boost': 65, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'Beyond mortal limits'},
    'godlike': {'name': 'Godlike', 'rarity': 'transcendent', 'atk_boost': 22, 'def_boost': 22, 'hp_boost': 110, 'mana_boost': 105, 'exp_boost': 100, 'material_discount_percent': 0, 'money_boost_percent': 0, 'material_boost_percent': 0, 'treasure_boost_percent': 0, 'crit_chance_percent': 0, 'death_penalty_percent': 0, 'hp_regen_percent': 0, 'atk_percent': 0, 'def_percent': 0, 'hp_percent': 0, 'mana_percent': 0, 'desc': 'A god among mortals'}
    }
RECIPES = {
    'potion': {'materials': {'slime_gel': 1, 'goblin_tooth': 1}, 'result': 'potion', 'qty': 1},
    'strong_potion': {'materials': {'slime_gel': 2, 'wolf_pelt': 1}, 'result': 'strong_potion', 'qty': 1},
    'ultra_potion': {'materials': {'slime_gel': 3, 'skeleton_bone': 2}, 'result': 'ultra_potion', 'qty': 1},
    'mana_upgrade_potion': {'materials': {'orc_iron': 2, 'bandit_cloth': 1}, 'result': 'mana_upgrade_potion', 'qty': 1},
    'perm_strength_upgrade': {'materials': {'troll_core': 5, 'dragon_scale': 1}, 'result': 'perm_strength_upgrade', 'qty': 1},
    'perm_defense_upgrade': {'materials': {'stone_core': 5, 'frozen_heart': 1}, 'result': 'perm_defense_upgrade', 'qty': 1},
    'perm_health_upgrade': {'materials': {'phoenix_feather': 3, 'holy_light': 2}, 'result': 'perm_health_upgrade', 'qty': 1},
    'perm_mana_upgrade': {'materials': {'demon_horn': 3, 'star_dust': 2}, 'result': 'perm_mana_upgrade', 'qty': 1},
    'perm_crit_chance_upgrade': {'materials': {'thunder_core': 5, 'lightning_feather': 3}, 'result': 'perm_crit_chance_upgrade', 'qty': 1},
    'perm_mana_regen_upgrade': {'materials': {'fire_essence': 4, 'ice_shard': 2}, 'result': 'perm_mana_regen_upgrade', 'qty': 1},
    'perm_lifesteal_upgrade': {'materials': {'demon_horn': 4, 'soul_shard': 2}, 'result': 'perm_lifesteal_upgrade', 'qty': 1},
    'perm_lifesteal_chance_upgrade': {'materials': {'void_fragment': 3, 'shadow_cloak': 1}, 'result': 'perm_lifesteal_chance_upgrade', 'qty': 1},
    'perm_magic_def_upgrade': {'materials': {'crystal_shard': 5, 'holy_light': 3}, 'result': 'perm_magic_def_upgrade', 'qty': 1},
    'perm_exp_upgrade': {'materials': {'moon_rock': 4, 'sun_stone': 2}, 'result': 'perm_exp_upgrade', 'qty': 1}
    }

# Add recipes for craftable items
for craftable in [CRAFTABLE_WEAPONS, CRAFTABLE_ARMORS, CRAFTABLE_WANDS, CRAFTABLE_ROBES, CRAFTABLE_NECKLACES]:
    for item_key, item_data in craftable.items():
        RECIPES[item_key] = {'materials': item_data['recipe'], 'result': item_key, 'qty': 1}
MAGIC_PACKS = {
    'common_magic_pack': {'name': 'Common Magic Pack', 'tier': 'D(Common)', 'spells': ['spark', 'ember', 'aqua_jet', 'gust', 'stone_toss', 'mana_bolt'], 'drop_count': (1, 2), 'description': 'Contains 1-2 common spells'},
    'rare_magic_pack': {'name': 'Rare Magic Pack', 'tier': 'C(Rare)', 'spells': ['spark', 'ember', 'aqua_jet', 'gust', 'stone_toss', 'mana_bolt', 'fireball', 'ice_spike', 'shadow_shot', 'thunder_strike', 'poison_mist', 'spark_chain'], 'drop_count': (1, 3), 'description': 'Contains 1-3 spells (common or rare)'},
    'mythical_magic_pack': {'name': 'Mythical Magic Pack', 'tier': 'B(Mythical)', 'spells': ['fireball', 'ice_spike', 'shadow_shot', 'thunder_strike', 'poison_mist', 'spark_chain', 'meteor', 'frost_nova', 'void_bolt', 'life_drain', 'earth_quake', 'glacial_prison'], 'drop_count': (2, 4), 'description': 'Contains 2-4 spells (rare or mythical)'},
    'prismatic_magic_pack': {'name': 'Prismatic Magic Pack', 'tier': 'A(Prismatic)', 'spells': ['meteor', 'frost_nova', 'void_bolt', 'life_drain', 'earth_quake', 'glacial_prison', 'prism_beam', 'lightning_storm', 'aether_blast', 'mirror_shield', 'prismatic_orb', 'prismatic_shard'], 'drop_count': (2, 4), 'description': 'Contains 2-4 spells (mythical or prismatic)'},
    'divine_magic_pack': {'name': 'Divine Magic Pack', 'tier': 'S(Divine)', 'spells': ['prism_beam', 'lightning_storm', 'aether_blast', 'mirror_shield', 'prismatic_orb', 'prismatic_shard', 'divine_wrath', 'holy_barrier', 'celestial_fall', 'purge', 'resurgence', 'spectral_bind'], 'drop_count': (3, 5), 'description': 'Contains 3-5 spells (prismatic or divine)'},
    'transcendent_magic_pack': {'name': 'Transcendent Magic Pack', 'tier': 'SS(Transcendent)', 'spells': ['divine_wrath', 'holy_barrier', 'celestial_fall', 'purge', 'resurgence', 'spectral_bind', 'transcendence', 'unmaking', 'voidstorm', 'eternal_echo', 'reality_rend'], 'drop_count': (3, 5), 'description': 'Contains 3-5 spells (divine or transcendent)'}
    }
SPELLS_BY_KEY = {
    'spark': {'name': 'Spark', 'class': 'D(Common)', 'type': 'lightning', 'mana': 4, 'power': 8, 'lvl': 1, 'desc': 'Small electric spark.'},
    'ember': {'name': 'Ember', 'class': 'D(Common)', 'type': 'fire', 'mana': 4, 'power': 9, 'lvl': 1, 'desc': 'Tiny firebolt.'},
    'aqua_jet': {'name': 'Aqua Jet', 'class': 'D(Common)', 'type': 'ice', 'mana': 5, 'power': 10, 'lvl': 2, 'desc': 'Jet of melted ice.'},
    'gust': {'name': 'Gust', 'class': 'D(Common)', 'type': 'wind', 'mana': 4, 'power': 7, 'lvl': 1, 'desc': 'Blows at enemy.'},
    'stone_toss': {'name': 'Stone Toss', 'class': 'D(Common)', 'type': 'nature', 'mana': 6, 'power': 12, 'lvl': 2, 'desc': 'Small rock hurled.'},
    'mana_bolt': {'name': 'Mana Bolt', 'class': 'D(Common)', 'type': 'mana', 'mana': 6, 'power': 14, 'lvl': 3, 'desc': 'Basic mana projectile.'},
    'spark_chain': {'name': 'Spark Chain', 'class': 'C(Rare)', 'type': 'lightning', 'mana': 22, 'power': 80, 'lvl': 15, 'desc': 'Chaining sparks.'},
    'fireball': {'name': 'Fireball', 'class': 'C(Rare)', 'type': 'fire', 'mana': 15, 'power': 40, 'lvl': 10, 'desc': 'Explosive orb.'},
    'ice_spike': {'name': 'Ice Spike', 'class': 'C(Rare)', 'type': 'ice', 'mana': 14, 'power': 36, 'lvl': 9, 'desc': 'Sharp ice.'},
    'shadow_shot': {'name': 'Shadow Shot', 'class': 'C(Rare)', 'type': 'mana', 'mana': 16, 'power': 45, 'lvl': 11, 'desc': 'Dark bolt.'},
    'thunder_strike': {'name': 'Thunder Strike', 'class': 'C(Rare)', 'type': 'lightning', 'mana': 18, 'power': 50, 'lvl': 12, 'desc': 'Powerful lightning.'},
    'poison_mist': {'name': 'Poison Mist', 'class': 'C(Rare)', 'type': 'wind', 'mana': 12, 'power': 30, 'lvl': 10, 'desc': 'Toxic cloud.'},
    'meteor': {'name': 'Meteor', 'class': 'B(Mythical)', 'type': 'nature', 'mana': 55, 'power': 220, 'lvl': 30, 'desc': 'Crushing meteor.'},
    'frost_nova': {'name': 'Frost Nova', 'class': 'B(Mythical)', 'type': 'ice', 'mana': 45, 'power': 160, 'lvl': 28, 'desc': 'Freezes area.'},
    'void_bolt': {'name': 'Void Bolt', 'class': 'B(Mythical)', 'type': 'mana', 'mana': 60, 'power': 250, 'lvl': 32, 'desc': 'Nullifying energy.'},
    'life_drain': {'name': 'Life Drain', 'class': 'B(Mythical)', 'type': 'mana', 'mana': 50, 'power': 150, 'lvl': 30, 'desc': 'Steal HP.'},
    'earth_quake': {'name': 'nature Quake', 'class': 'B(Mythical)', 'type': 'nature', 'mana': 48, 'power': 180, 'lvl': 31, 'desc': 'Shake the ground.'},
    'glacial_prison': {'name': 'Glacial Prison', 'class': 'B(Mythical)', 'type': 'ice', 'mana': 70, 'power': 300, 'lvl': 35, 'desc': 'Encase the enemy.'},
    'prism_beam': {'name': 'Prism Beam', 'class': 'A(Prismatic)', 'type': 'mana', 'mana': 120, 'power': 700, 'lvl': 50, 'desc': 'Shredding beam.'},
    'lightning_storm': {'name': 'Lightning Storm', 'class': 'A(Prismatic)', 'type': 'lightning', 'mana': 110, 'power': 650, 'lvl': 48, 'desc': 'Storm of lightning.'},
    'aether_blast': {'name': 'Aether Blast', 'class': 'A(Prismatic)', 'type': 'mana', 'mana': 100, 'power': 600, 'lvl': 46, 'desc': 'Pure aether.'},
    'mirror_shield': {'name': 'Mirror Shield', 'class': 'A(Prismatic)', 'type': 'mana', 'mana': 40, 'power': 0, 'lvl': 45, 'desc': 'Reflect attacks.'},
    'prismatic_orb': {'name': 'Prismatic Orb', 'class': 'A(Prismatic)', 'type': 'mana', 'mana': 90, 'power': 520, 'lvl': 47, 'desc': 'Orb of prismatic energy.'},
    'prismatic_shard': {'name': 'Prismatic Shard', 'class': 'A(Prismatic)', 'type': 'mana', 'mana': 95, 'power': 560, 'lvl': 52, 'desc': 'Shards of light.'},
    'divine_wrath': {'name': 'Divine Wrath', 'class': 'S(Divine)', 'type': 'mana', 'mana': 300, 'power': 2000, 'lvl': 75, 'desc': 'Wrath of the gods.'},
    'holy_barrier': {'name': 'Holy Barrier', 'class': 'S(Divine)', 'type': 'heal', 'mana': 120, 'power': 0, 'lvl': 70, 'desc': 'Major protection.'},
    'celestial_fall': {'name': 'Celestial Fall', 'class': 'S(Divine)', 'type': 'nature', 'mana': 250, 'power': 1500, 'lvl': 72, 'desc': 'Celestial impact.'},
    'purge': {'name': 'Purge', 'class': 'S(Divine)', 'type': '', 'mana': 100, 'power': 480, 'lvl': 68, 'desc': 'Remove curses.'},
    'resurgence': {'name': 'Resurgence', 'class': 'S(Divine)', 'type': 'heal', 'mana': 200, 'power': 0, 'lvl': 74, 'desc': 'Large heal.'},
    'spectral_bind': {'name': 'Spectral Bind', 'class': 'S(Divine)', 'type': 'mana', 'mana': 180, 'power': 820, 'lvl': 66, 'desc': 'Bind spirit.'},
    'transcendence': {'name': 'Transcendence', 'class': 'SS(Transcendent)', 'type': 'mana', 'mana': 900, 'power': 8000, 'lvl': 95, 'desc': 'Transcend reality.'},
    'unmaking': {'name': 'Unmaking', 'class': 'SS(Transcendent)', 'type': 'mana', 'mana': 800, 'power': 7000, 'lvl': 90, 'desc': 'Unmake existence.'},
    'voidstorm': {'name': 'Voidstorm', 'class': 'SS(Transcendent)', 'type': 'mana', 'mana': 850, 'power': 7500, 'lvl': 92, 'desc': 'Storm of void.'},
    'eternal_echo': {'name': 'Eternal Echo', 'class': 'SS(Transcendent)', 'type': 'mana', 'mana': 950, 'power': 8500, 'lvl': 96, 'desc': 'Echo through eternity.'},
    'reality_rend': {'name': 'Reality Rend', 'class': 'SS(Transcendent)', 'type': 'mana', 'mana': 1000, 'power': 9000, 'lvl': 98, 'desc': 'Tear reality apart.'}
    }
MAGIC_PACK_ALIASES = {
    'common': 'common_magic_pack', 'c': 'common_magic_pack', 'rare': 'rare_magic_pack', 'r': 'rare_magic_pack', 'mythical': 'mythical_magic_pack', 'm': 'mythical_magic_pack', 'prismatic': 'prismatic_magic_pack', 'p': 'prismatic_magic_pack', 'divine': 'divine_magic_pack', 'd': 'divine_magic_pack', 'transcendent': 'transcendent_magic_pack', 't': 'transcendent_magic_pack'}
ACHIEVEMENTS = {
    'first_monster': {'name': 'First Blood', 'title': 'Slayer', 'condition': lambda stats: stats.get('monsters_defeated', 0) >= 1, 'desc': 'Defeat 1 monster'},
    'hundred_monsters': {'name': 'Monster Hunter', 'title': 'Hunter', 'condition': lambda stats: stats.get('monsters_defeated', 0) >= 100, 'desc': 'Defeat 100 monsters'},
    'thousand_monsters': {'name': 'Monster Slayer', 'title': 'Slayer II', 'condition': lambda stats: stats.get('monsters_defeated', 0) >= 1000, 'desc': 'Defeat 1000 monsters'},
    'boss_defeats_10': {'name': 'Boss Hunter', 'title': 'Boss Slayer', 'condition': lambda stats: stats.get('bosses_defeated', 0) >= 10, 'desc': 'Defeat 10 bosses'},
    'boss_defeats_50': {'name': 'Boss Master', 'title': 'Boss Master', 'condition': lambda stats: stats.get('bosses_defeated', 0) >= 50, 'desc': 'Defeat 50 bosses'},
    'millionaire': {'name': 'Wealthy', 'title': 'Millionaire', 'condition': lambda stats: stats.get('total_money_earned', 0) >= 1000000, 'desc': 'Earn 1,000,000 total money'},
    'spell_master': {'name': 'Spellcaster', 'title': 'Arcane Master', 'condition': lambda stats: len(stats.get('learned_spells', [])) >= 10, 'desc': 'Learn 10 spells'},
    'crafting_expert': {'name': 'Craftsman', 'title': 'Artisan', 'condition': lambda stats: stats.get('items_crafted', 0) >= 50, 'desc': 'Craft 50 items'},
    'collector': {'name': 'Collector', 'title': 'Collector', 'condition': lambda stats: stats.get('materials_collected', 0) >= 500, 'desc': 'Collect 500 materials'},
    'survivor': {'name': 'Survivor', 'title': 'Immortal', 'condition': lambda stats: stats.get('times_died', 0) >= 100, 'desc': 'Die 100 times'},
    'perfectionist': {'name': 'Perfect Game', 'title': 'Perfect', 'condition': lambda stats: stats.get('monsters_defeated', 0) >= 1000 and stats.get('bosses_defeated', 0) >= 10 and (len(stats.get('learned_spells', [])) >= 5) and (stats.get('level', 1) >= 50), 'desc': 'Defeat 1000 monsters, 10 bosses, learn 5 spells, reach level 50'},
    'legendary': {'name': 'Legendary Adventurer', 'title': 'Legendary', 'condition': lambda stats: stats.get('monsters_defeated', 0) >= 5000 and stats.get('bosses_defeated', 0) >= 100 and (stats.get('level', 1) >= 80), 'desc': 'Defeat 5000 monsters, 100 bosses, reach level 80'},
    'godlike': {'name': 'God Among Men', 'title': 'Deity', 'condition': lambda stats: stats.get('monsters_defeated', 0) >= 10000 and stats.get('bosses_defeated', 0) >= 200 and (stats.get('level', 1) >= 100), 'desc': 'Defeat 10000 monsters, 200 bosses, reach level 100'},
    'treasure_hunter': {'name': 'Treasure Hunter', 'title': 'Treasure King', 'condition': lambda stats: stats.get('dungeon_treasure_collected', 0) >= 500000, 'desc': 'Collect 500,000 from dungeon treasure'},
    'lucky': {'name': 'Lucky', 'title': "Fortune's Favorite", 'condition': lambda stats: stats.get('critical_hits', 0) >= 1000, 'desc': 'Land 1000 critical hits'}
    }

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
        if ach_key in ACHIEVEMENTS:
            ach_title = ACHIEVEMENTS[ach_key]['title']
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
        for ach_key in ACHIEVEMENTS:
            achievement = ACHIEVEMENTS[ach_key]
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
                for k, v in TITLES.items():
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

def save_dungeon_treasure():
    global dungeon_treasure
    try:
        lock_file = DUNGEON_TREASURE_FILE + '.lock'
        while os.path.exists(lock_file):
            time.sleep(0.01)
        with open(lock_file, 'w') as f:
            f.write('')
        temp_file = DUNGEON_TREASURE_FILE + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump({'treasure': dungeon_treasure}, f)
        os.replace(temp_file, DUNGEON_TREASURE_FILE)
        try:
            os.remove(lock_file)
        except:
            pass
        return True
    except Exception as e:
        print(f'Error saving dungeon treasure: {e}')
        try:
            os.remove(lock_file)
        except:
            pass
        return False

def load_dungeon_treasure():
    global dungeon_treasure
    try:
        if os.path.exists(DUNGEON_TREASURE_FILE):
            with open(DUNGEON_TREASURE_FILE, 'r') as f:
                data = json.load(f)
                loaded_treasure = data.get('treasure', {})
                if isinstance(loaded_treasure, int):
                    dungeon_treasure = {'money': loaded_treasure, 'items': []}
                else:
                    dungeon_treasure = loaded_treasure.copy()
                    dungeon_treasure.setdefault('money', 0)
                    dungeon_treasure.setdefault('items', [])
        else:
            dungeon_treasure = {'money': random.randint(200000, 1000000), 'items': []}
        if dungeon_treasure['money'] < 200000:
            dungeon_treasure['money'] = random.randint(200000, 1000000)
            save_dungeon_treasure()
    except Exception as e:
        print(f'Error loading dungeon treasure: {e}')
        dungeon_treasure = {'money': random.randint(200000, 1000000), 'items': []}
load_dungeon_treasure()

def save_all_data():
    save_dungeon_treasure()

def replenish_dungeon_treasure():
    """Replenish dungeon treasure items if below 10"""
    global dungeon_treasure
    if len(dungeon_treasure['items']) < 10:
        num_to_add = random.randint(20, 30) - len(dungeon_treasure['items'])
        consumables = list(POTIONS.keys()) + list(MAGIC_PACKS.keys()) + list(MATERIALS.keys())
        for _ in range(num_to_add):
            item = random.choice(consumables)
            dungeon_treasure['items'].append(item)
        save_dungeon_treasure()

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
    autosave_timer = threading.Timer(AUTOSAVE_INTERVAL, autosave)
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
    if os.path.isdir(USERS_DIR):
        users = {}
        if os.path.exists('users'):
            for filename in os.listdir('users'):
                if filename.endswith('.json'):
                    username = filename[:-5]
                    with open(os.path.join('users', filename), 'r') as f:
                        users[username] = json.load(f)
        with open(USERS_DIR, 'w') as f:
            json.dump(users, f, indent=4)
        import shutil
        shutil.rmtree('users')
    elif not os.path.exists(USERS_DIR):
        with open(USERS_DIR, 'w') as f:
            json.dump({}, f)

def load_all_users():
    """Load all user data from users.txt"""
    if not os.path.exists(USERS_DIR):
        return {}
    try:
        with open(USERS_DIR, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_all_users(users):
    """Save all user data to users.txt atomically with locking"""
    lock_file = USERS_DIR + '.lock'
    try:
        while os.path.exists(lock_file):
            time.sleep(0.01)
        with open(lock_file, 'w') as f:
            f.write('')
        temp_file = USERS_DIR + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump(users, f, indent=4)
        os.replace(temp_file, USERS_DIR)
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

def choose_monster_for_area(area):
    area_monsters = [m for m in MONSTERS if m.get('area', area) == area and (not m['is_boss'])]
    if not area_monsters:
        area_monsters = [m for m in MONSTERS if not m['is_boss']]
    weights = [m.get('weight', 1) for m in area_monsters]
    chosen = random.choices(area_monsters, weights=weights, k=1)[0].copy()
    if 'atk_min' not in chosen:
        chosen['atk_min'] = chosen.get('magic_atk_min', 1)
    if 'atk_max' not in chosen:
        chosen['atk_max'] = chosen.get('magic_atk_max', chosen['atk_min'])
    scale = 1.0 + (area - 1) * 0.15
    chosen['hp'] = max(1, int(chosen.get('hp', 1) * scale))
    chosen['atk_min'] = max(1, int(chosen.get('atk_min', 1) * scale))
    chosen['atk_max'] = max(chosen['atk_min'], int(chosen.get('atk_max', chosen['atk_min']) * scale))
    chosen['money_min'] = int(chosen.get('money_min', 1) * (1 + (area - 1) * 0.3))
    chosen['money_max'] = int(chosen.get('money_max', chosen['money_min']) * (1 + (area - 1) * 0.3))
    return chosen

def choose_boss_for_area(area):
    area_bosses = [m for m in MONSTERS if m.get('area', area) == area and m['is_boss']]
    if not area_bosses:
        area_bosses = [m for m in MONSTERS if m['is_boss']]
    weights = [m.get('weight', 1) for m in area_bosses]
    chosen = random.choices(area_bosses, weights=weights, k=1)[0].copy()
    if 'atk_min' not in chosen:
        chosen['atk_min'] = chosen.get('magic_atk_min', 1)
    if 'atk_max' not in chosen:
        chosen['atk_max'] = chosen.get('magic_atk_max', chosen['atk_min'])
    scale = 1.0 + (area - 1) * 0.1
    chosen['hp'] = max(1, int(chosen.get('hp', 1) * scale))
    chosen['atk_min'] = max(1, int(chosen.get('atk_min', 1) * scale))
    chosen['atk_max'] = max(chosen['atk_min'], int(chosen.get('atk_max', chosen['atk_min']) * scale))
    chosen['money_min'] = int(chosen.get('money_min', 1) * (1 + (area - 1) * 0.2))
    chosen['money_max'] = int(chosen.get('money_max', chosen['money_min']) * (1 + (area - 1) * 0.2))
    return chosen

def get_boss_template():
    return next((m for m in MONSTERS if m['is_boss']))

def apply_damage_with_defense(damage, defense):
    reduced = damage - defense
    return reduced if reduced >= 1 else 1

def apply_magic_damage(damage, magic_def):
    """Magic damage reduced by magic_def (robes + perm). Minimum 1."""
    reduced = damage - magic_def
    return reduced if reduced >= 1 else 1

def get_equip_and_perm_bonuses(stats):
    """
    Return a dict combining equipment, permanent and title bonuses used in combat.
    Keys: weapon_atk, neck_atk, armor_def, neck_def, robe_magic_def,
          perm_atk, perm_def, perm_magic_def,
          total_base_atk, total_base_def, total_magic_def
    """
    equip = stats.get('equipped', {})
    w_atk = WEAPONS.get(equip.get('weapon'), {}).get('atk', 0)
    n_atk = NECKLACES.get(equip.get('necklace'), {}).get('atk_bonus', 0)
    a_def = ARMORS.get(equip.get('armor'), {}).get('def', 0)
    n_def = NECKLACES.get(equip.get('necklace'), {}).get('def_bonus', 0)
    robe_magic = ROBES.get(equip.get('robe'), {}).get('magic_def', 0)
    perm_atk = stats.get('perm_atk', 0)
    perm_def = stats.get('perm_def', 0)
    perm_magic_def = stats.get('perm_magic_def', 0)
    title_atk_boost = stats.get('title_atk_boost', 0)
    title_def_boost = stats.get('title_def_boost', 0)
    title_magic_def = stats.get('title_magic_def', 0)
    base_base_atk = stats.get('atk', 5)
    base_base_def = stats.get('defense', 0)
    total_base_atk = base_base_atk + perm_atk + title_atk_boost
    total_base_def = base_base_def + perm_def + title_def_boost
    total_magic_def = robe_magic + perm_magic_def + title_magic_def
    return {'weapon_atk': w_atk, 'neck_atk': n_atk, 'armor_def': a_def, 'neck_def': n_def, 'robe_magic_def': robe_magic, 'perm_atk': perm_atk, 'perm_def': perm_def, 'perm_magic_def': perm_magic_def, 'total_base_atk': total_base_atk, 'total_base_def': total_base_def, 'total_magic_def': total_magic_def}

def calculate_total_crit_chance(stats, active_buffs):
    """Return combined crit chance (perm + active crit buffs). All in 0..1."""
    total = stats.get('perm_crit_chance', 0) / 100.0
    for b in active_buffs:
        if b.get('type') == 'crit' and b.get('remaining', 0) > 0:
            total += b.get('amount', 0) / 100.0
    return total
MONSTERS = [
    # D(Common) monsters - Areas 1-20
    {'name': 'Slime', 'hp': 15, 'atk_min': 3, 'atk_max': 6, 'money_min': 2, 'money_max': 7, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.25, 'slime_gel': 0.4}, 'weight': 18, 'area': 1, 'element': 'nature', 'exp_min': 10, 'exp_max': 25},
    {'name': 'Goblin', 'hp': 20, 'atk_min': 5, 'atk_max': 8, 'money_min': 4, 'money_max': 15, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.3, 'strength_boost': 0.05, 'goblin_tooth': 0.3}, 'weight': 15, 'area': 1, 'element': 'mana', 'exp_min': 10, 'exp_max': 25},
    {'name': 'Wolf', 'hp': 25, 'atk_min': 6, 'atk_max': 10, 'money_min': 10, 'money_max': 22, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'wolf_pelt': 0.3}, 'weight': 14, 'area': 2, 'element': 'nature', 'exp_min': 10, 'exp_max': 25},
    {'name': 'Forest Sprite', 'hp': 30, 'atk_min': 5, 'atk_max': 9, 'money_min': 8, 'money_max': 20, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.25, 'mana_regen_potion': 0.1, 'crystal_shard': 0.2}, 'weight': 12, 'area': 3, 'element': 'nature', 'exp_min': 10, 'exp_max': 25},
    {'name': 'Skeleton', 'hp': 40, 'atk_min': 8, 'atk_max': 12, 'money_min': 15, 'money_max': 30, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.25, 'defense_boost': 0.05, 'skeleton_bone': 0.4}, 'weight': 12, 'area': 5, 'element': 'mana', 'exp_min': 15, 'exp_max': 37},
    {'name': 'Orc', 'hp': 60, 'atk_min': 10, 'atk_max': 15, 'money_min': 20, 'money_max': 40, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'orc_iron': 0.3}, 'weight': 10, 'area': 7, 'element': 'mana', 'exp_min': 15, 'exp_max': 37},
    {'name': 'Giant Spider', 'hp': 50, 'atk_min': 12, 'atk_max': 18, 'money_min': 25, 'money_max': 45, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'crit_boost': 0.05, 'spider_venom': 0.3}, 'weight': 8, 'area': 9, 'element': 'nature', 'exp_min': 15, 'exp_max': 37},
    {'name': 'Dark Bat', 'hp': 35, 'atk_min': 10, 'atk_max': 15, 'money_min': 18, 'money_max': 35, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'bat_wing': 0.3}, 'weight': 10, 'area': 11, 'element': 'nature', 'exp_min': 15, 'exp_max': 37},
    
    # C(Rare) monsters - Areas 21-40
    {'name': 'Goblin Shaman', 'hp': 80, 'atk_min': 16, 'atk_max': 24, 'money_min': 10, 'money_max': 25, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'mana_regen_potion': 0.1, 'goblin_tooth': 0.2}, 'weight': 8, 'area': 21, 'element': 'mana', 'exp_min': 10, 'exp_max': 25},
    {'name': 'Bandit', 'hp': 160, 'atk_min': 14, 'atk_max': 24, 'money_min': 35, 'money_max': 60, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.15, 'crit_boost': 0.04, 'common_magic_pack': 0.15, 'bandit_cloth': 0.3, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1}, 'weight': 10, 'area': 25, 'element': 'mana', 'exp_min': 22, 'exp_max': 56},
    {'name': 'Orc Warrior', 'hp': 220, 'atk_min': 16, 'atk_max': 26, 'money_min': 40, 'money_max': 70, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'orc_iron': 0.4, 'strength_boost': 0.1, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1}, 'weight': 8, 'area': 27, 'element': 'mana', 'exp_min': 22, 'exp_max': 56},
    {'name': 'Dark Mage', 'hp': 180, 'atk_min': 20, 'atk_max': 30, 'money_min': 50, 'money_max': 80, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.25, 'strength_boost': 0.06, 'common_magic_pack': 0.25, 'rare_magic_pack': 0.1, 'dark_essence': 0.2, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1}, 'weight': 7, 'area': 29, 'element': 'mana', 'exp_min': 22, 'exp_max': 56},
    {'name': 'Stone Golem', 'hp': 280, 'atk_min': 12, 'atk_max': 20, 'money_min': 45, 'money_max': 75, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'defense_boost': 0.1, 'stone_core': 0.3, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1}, 'weight': 6, 'area': 31, 'element': 'nature', 'exp_min': 22, 'exp_max': 56},
    {'name': 'Troll', 'hp': 360, 'atk_min': 24, 'atk_max': 36, 'money_min': 80, 'money_max': 120, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'regen_potion': 0.05, 'common_magic_pack': 0.1, 'rare_magic_pack': 0.05, 'troll_core': 0.3, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1}, 'weight': 6, 'area': 33, 'element': 'nature', 'exp_min': 33, 'exp_max': 84},
    {'name': 'Ice Elemental', 'hp': 300, 'atk_min': 30, 'atk_max': 40, 'money_min': 90, 'money_max': 130, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'frozen_heart': 0.3, 'ice_shard': 0.2, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1}, 'weight': 5, 'area': 35, 'element': 'ice', 'exp_min': 33, 'exp_max': 84},
    {'name': 'Fire Elemental', 'hp': 280, 'atk_min': 32, 'atk_max': 44, 'money_min': 85, 'money_max': 125, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'fire_essence': 0.3, 'ember': 0.2, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1}, 'weight': 5, 'area': 37, 'element': 'fire', 'exp_min': 33, 'exp_max': 84},
    {'name': 'Thunder Bird', 'hp': 260, 'atk_min': 28, 'atk_max': 42, 'money_min': 95, 'money_max': 140, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'thunder_core': 0.3, 'lightning_feather': 0.2, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1}, 'weight': 5, 'area': 39, 'element': 'lightning', 'exp_min': 33, 'exp_max': 84},
    
    # B(Mythical) monsters - Areas 41-60
    {'name': 'Dark Knight', 'hp': 480, 'atk_min': 36, 'atk_max': 50, 'money_min': 120, 'money_max': 180, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.15, 'defense_boost': 0.1, 'rare_magic_pack': 0.2, 'dark_essence': 0.3, 'perm_exp_upgrade': 0.12, 'perm_strength_upgrade': 0.12, 'perm_defense_upgrade': 0.12, 'perm_health_upgrade': 0.12, 'perm_mana_upgrade': 0.12, 'perm_crit_chance_upgrade': 0.12, 'perm_mana_regen_upgrade': 0.12, 'perm_lifesteal_upgrade': 0.12, 'perm_lifesteal_chance_upgrade': 0.12}, 'weight': 4, 'area': 41, 'element': 'mana', 'exp_min': 50, 'exp_max': 126},
    {'name': 'Shadow Assassin', 'hp': 400, 'atk_min': 40, 'atk_max': 56, 'money_min': 130, 'money_max': 190, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.15, 'crit_boost': 0.1, 'rare_magic_pack': 0.2, 'shadow_cloak': 0.2, 'perm_exp_upgrade': 0.12, 'perm_strength_upgrade': 0.12, 'perm_defense_upgrade': 0.12, 'perm_health_upgrade': 0.12, 'perm_mana_upgrade': 0.12, 'perm_crit_chance_upgrade': 0.12, 'perm_mana_regen_upgrade': 0.12, 'perm_lifesteal_upgrade': 0.12, 'perm_lifesteal_chance_upgrade': 0.12}, 'weight': 4, 'area': 43, 'element': 'mana', 'exp_min': 50, 'exp_max': 126},
    {'name': 'Arcane Mage', 'hp': 440, 'atk_min': 44, 'atk_max': 60, 'money_min': 140, 'money_max': 200, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'mana_upgrade_potion': 0.1, 'rare_magic_pack': 0.25, 'mythical_magic_pack': 0.1, 'arcane_tome': 0.2, 'perm_exp_upgrade': 0.12, 'perm_strength_upgrade': 0.12, 'perm_defense_upgrade': 0.12, 'perm_health_upgrade': 0.12, 'perm_mana_upgrade': 0.12, 'perm_crit_chance_upgrade': 0.12, 'perm_mana_regen_upgrade': 0.12, 'perm_lifesteal_upgrade': 0.12, 'perm_lifesteal_chance_upgrade': 0.12}, 'weight': 3, 'area': 45, 'element': 'mana', 'exp_min': 50, 'exp_max': 126},
    {'name': 'Warlock', 'hp': 420, 'atk_min': 42, 'atk_max': 58, 'money_min': 135, 'money_max': 195, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'curse_scroll': 0.2, 'rare_magic_pack': 0.2, 'mythical_magic_pack': 0.1, 'demon_horn': 0.2, 'perm_exp_upgrade': 0.12, 'perm_strength_upgrade': 0.12, 'perm_defense_upgrade': 0.12, 'perm_health_upgrade': 0.12, 'perm_mana_upgrade': 0.12, 'perm_crit_chance_upgrade': 0.12, 'perm_mana_regen_upgrade': 0.12, 'perm_lifesteal_upgrade': 0.12, 'perm_lifesteal_chance_upgrade': 0.12}, 'weight': 3, 'area': 47, 'element': 'mana', 'exp_min': 50, 'exp_max': 126},
    {'name': 'Ice Giant', 'hp': 600, 'atk_min': 50, 'atk_max': 70, 'money_min': 180, 'money_max': 250, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'frozen_heart': 0.4, 'mythical_magic_pack': 0.2, 'ice_shard': 0.3, 'perm_exp_upgrade': 0.14, 'perm_strength_upgrade': 0.14, 'perm_defense_upgrade': 0.14, 'perm_health_upgrade': 0.14, 'perm_mana_upgrade': 0.14, 'perm_crit_chance_upgrade': 0.14, 'perm_mana_regen_upgrade': 0.14, 'perm_lifesteal_upgrade': 0.14, 'perm_lifesteal_chance_upgrade': 0.14}, 'weight': 3, 'area': 49, 'element': 'ice', 'exp_min': 75, 'exp_max': 189},
    {'name': 'Phoenix', 'hp': 520, 'atk_min': 56, 'atk_max': 76, 'money_min': 200, 'money_max': 280, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'phoenix_feather': 0.3, 'mythical_magic_pack': 0.25, 'fire_essence': 0.3, 'perm_exp_upgrade': 0.14, 'perm_strength_upgrade': 0.14, 'perm_defense_upgrade': 0.14, 'perm_health_upgrade': 0.14, 'perm_mana_upgrade': 0.14, 'perm_crit_chance_upgrade': 0.14, 'perm_mana_regen_upgrade': 0.14, 'perm_lifesteal_upgrade': 0.14, 'perm_lifesteal_chance_upgrade': 0.14}, 'weight': 2, 'area': 51, 'element': 'fire', 'exp_min': 75, 'exp_max': 189},
    {'name': 'Crystal Golem', 'hp': 640, 'atk_min': 48, 'atk_max': 68, 'money_min': 190, 'money_max': 260, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'crystal_shard': 0.4, 'mythical_magic_pack': 0.2, 'stone_core': 0.3, 'perm_exp_upgrade': 0.14, 'perm_strength_upgrade': 0.14, 'perm_defense_upgrade': 0.14, 'perm_health_upgrade': 0.14, 'perm_mana_upgrade': 0.14, 'perm_crit_chance_upgrade': 0.14, 'perm_mana_regen_upgrade': 0.14, 'perm_lifesteal_upgrade': 0.14, 'perm_lifesteal_chance_upgrade': 0.14}, 'weight': 2, 'area': 53, 'element': 'nature', 'exp_min': 75, 'exp_max': 189},
    {'name': 'Storm Dragon', 'hp': 560, 'atk_min': 54, 'atk_max': 74, 'money_min': 210, 'money_max': 290, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'thunder_core': 0.4, 'mythical_magic_pack': 0.25, 'dragon_scale': 0.2, 'perm_exp_upgrade': 0.14, 'perm_strength_upgrade': 0.14, 'perm_defense_upgrade': 0.14, 'perm_health_upgrade': 0.14, 'perm_mana_upgrade': 0.14, 'perm_crit_chance_upgrade': 0.14, 'perm_mana_regen_upgrade': 0.14, 'perm_lifesteal_upgrade': 0.14, 'perm_lifesteal_chance_upgrade': 0.14}, 'weight': 2, 'area': 55, 'element': 'lightning', 'exp_min': 75, 'exp_max': 189},
    
    # A(Prismatic) monsters - Areas 61-80
    {'name': 'Void Walker', 'hp': 720, 'atk_min': 64, 'atk_max': 84, 'money_min': 250, 'money_max': 350, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.15, 'void_fragment': 0.3, 'mythical_magic_pack': 0.2, 'prismatic_magic_pack': 0.1, 'perm_exp_upgrade': 0.16, 'perm_strength_upgrade': 0.16, 'perm_defense_upgrade': 0.16, 'perm_health_upgrade': 0.16, 'perm_mana_upgrade': 0.16, 'perm_crit_chance_upgrade': 0.16, 'perm_mana_regen_upgrade': 0.16, 'perm_lifesteal_upgrade': 0.16, 'perm_lifesteal_chance_upgrade': 0.16}, 'weight': 2, 'area': 61, 'element': 'mana', 'exp_min': 113, 'exp_max': 284},
    {'name': 'Celestial Guardian', 'hp': 800, 'atk_min': 60, 'atk_max': 80, 'money_min': 280, 'money_max': 380, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'holy_light': 0.3, 'mythical_magic_pack': 0.25, 'prismatic_magic_pack': 0.15, 'perm_exp_upgrade': 0.16, 'perm_strength_upgrade': 0.16, 'perm_defense_upgrade': 0.16, 'perm_health_upgrade': 0.16, 'perm_mana_upgrade': 0.16, 'perm_crit_chance_upgrade': 0.16, 'perm_mana_regen_upgrade': 0.16, 'perm_lifesteal_upgrade': 0.16, 'perm_lifesteal_chance_upgrade': 0.16}, 'weight': 2, 'area': 63, 'element': 'mana', 'exp_min': 113, 'exp_max': 284},
    {'name': 'Star Weaver', 'hp': 680, 'atk_min': 66, 'atk_max': 86, 'money_min': 260, 'money_max': 360, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'star_dust': 0.4, 'mythical_magic_pack': 0.2, 'prismatic_magic_pack': 0.1, 'perm_exp_upgrade': 0.16, 'perm_strength_upgrade': 0.16, 'perm_defense_upgrade': 0.16, 'perm_health_upgrade': 0.16, 'perm_mana_upgrade': 0.16, 'perm_crit_chance_upgrade': 0.16, 'perm_mana_regen_upgrade': 0.16, 'perm_lifesteal_upgrade': 0.16, 'perm_lifesteal_chance_upgrade': 0.16}, 'weight': 2, 'area': 65, 'element': 'mana', 'exp_min': 113, 'exp_max': 284},
    {'name': 'Moon Sentinel', 'hp': 760, 'atk_min': 62, 'atk_max': 82, 'money_min': 270, 'money_max': 370, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'moon_rock': 0.3, 'mythical_magic_pack': 0.2, 'prismatic_magic_pack': 0.15, 'perm_exp_upgrade': 0.16, 'perm_strength_upgrade': 0.16, 'perm_defense_upgrade': 0.16, 'perm_health_upgrade': 0.16, 'perm_mana_upgrade': 0.16, 'perm_crit_chance_upgrade': 0.16, 'perm_mana_regen_upgrade': 0.16, 'perm_lifesteal_upgrade': 0.16, 'perm_lifesteal_chance_upgrade': 0.16}, 'weight': 2, 'area': 67, 'element': 'mana', 'exp_min': 113, 'exp_max': 284},
    {'name': 'Sun Champion', 'hp': 880, 'atk_min': 72, 'atk_max': 92, 'money_min': 320, 'money_max': 420, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'sun_stone': 0.3, 'prismatic_magic_pack': 0.25, 'divine_magic_pack': 0.1, 'perm_exp_upgrade': 0.18, 'perm_strength_upgrade': 0.18, 'perm_defense_upgrade': 0.18, 'perm_health_upgrade': 0.18, 'perm_mana_upgrade': 0.18, 'perm_crit_chance_upgrade': 0.18, 'perm_mana_regen_upgrade': 0.18, 'perm_lifesteal_upgrade': 0.18, 'perm_lifesteal_chance_upgrade': 0.18}, 'weight': 1, 'area': 69, 'element': 'fire', 'exp_min': 170, 'exp_max': 427},
    {'name': 'Void Lord', 'hp': 960, 'atk_min': 76, 'atk_max': 96, 'money_min': 350, 'money_max': 450, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'void_fragment': 0.4, 'prismatic_magic_pack': 0.25, 'divine_magic_pack': 0.15, 'perm_exp_upgrade': 0.18, 'perm_strength_upgrade': 0.18, 'perm_defense_upgrade': 0.18, 'perm_health_upgrade': 0.18, 'perm_mana_upgrade': 0.18, 'perm_crit_chance_upgrade': 0.18, 'perm_mana_regen_upgrade': 0.18, 'perm_lifesteal_upgrade': 0.18, 'perm_lifesteal_chance_upgrade': 0.18}, 'weight': 1, 'area': 71, 'element': 'mana', 'exp_min': 170, 'exp_max': 427},
    {'name': 'Divine Paladin', 'hp': 840, 'atk_min': 74, 'atk_max': 94, 'money_min': 330, 'money_max': 430, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'holy_light': 0.4, 'prismatic_magic_pack': 0.3, 'divine_magic_pack': 0.15, 'perm_exp_upgrade': 0.18, 'perm_strength_upgrade': 0.18, 'perm_defense_upgrade': 0.18, 'perm_health_upgrade': 0.18, 'perm_mana_upgrade': 0.18, 'perm_crit_chance_upgrade': 0.18, 'perm_mana_regen_upgrade': 0.18, 'perm_lifesteal_upgrade': 0.18, 'perm_lifesteal_chance_upgrade': 0.18}, 'weight': 1, 'area': 73, 'element': 'mana', 'exp_min': 170, 'exp_max': 427},
    {'name': 'Cosmic Mage', 'hp': 920, 'atk_min': 70, 'atk_max': 90, 'money_min': 340, 'money_max': 440, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'star_dust': 0.3, 'prismatic_magic_pack': 0.25, 'divine_magic_pack': 0.2, 'perm_exp_upgrade': 0.18, 'perm_strength_upgrade': 0.18, 'perm_defense_upgrade': 0.18, 'perm_health_upgrade': 0.18, 'perm_mana_upgrade': 0.18, 'perm_crit_chance_upgrade': 0.18, 'perm_mana_regen_upgrade': 0.18, 'perm_lifesteal_upgrade': 0.18, 'perm_lifesteal_chance_upgrade': 0.18}, 'weight': 1, 'area': 75, 'element': 'mana', 'exp_min': 170, 'exp_max': 427},
    
    # S(Divine) monsters - Areas 81-99
    {'name': 'Eternal Dragon', 'hp': 1200, 'atk_min': 84, 'atk_max': 108, 'money_min': 450, 'money_max': 600, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.15, 'dragon_scale': 0.4, 'divine_magic_pack': 0.3, 'transcendent_magic_pack': 0.1, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2}, 'weight': 1, 'area': 81, 'element': 'fire', 'exp_min': 256, 'exp_max': 640},
    {'name': 'Void Reaper', 'hp': 1120, 'atk_min': 90, 'atk_max': 114, 'money_min': 480, 'money_max': 630, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'void_fragment': 0.4, 'divine_magic_pack': 0.3, 'transcendent_magic_pack': 0.15, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2}, 'weight': 1, 'area': 83, 'element': 'mana', 'exp_min': 256, 'exp_max': 640},
    {'name': 'Celestial Phoenix', 'hp': 1160, 'atk_min': 86, 'atk_max': 110, 'money_min': 470, 'money_max': 620, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'phoenix_feather': 0.4, 'divine_magic_pack': 0.35, 'transcendent_magic_pack': 0.15, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2}, 'weight': 1, 'area': 85, 'element': 'fire', 'exp_min': 256, 'exp_max': 640},
    {'name': 'Cosmic Entity', 'hp': 1240, 'atk_min': 82, 'atk_max': 106, 'money_min': 460, 'money_max': 610, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'star_dust': 0.4, 'divine_magic_pack': 0.3, 'transcendent_magic_pack': 0.2, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2}, 'weight': 1, 'area': 87, 'element': 'mana', 'exp_min': 256, 'exp_max': 640},
    {'name': 'Shadow Wraith', 'hp': 2000, 'atk_min': 120, 'atk_max': 160, 'money_min': 1000, 'money_max': 1500, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 1.0, 'crit_boost': 1.0, 'prismatic_magic_pack': 0.8, 'divine_magic_pack': 0.8, 'soul_shard': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 89, 'element': 'mana', 'exp_min': 500, 'exp_max': 1000},
    {'name': 'Celestial Beast', 'hp': 2400, 'atk_min': 110, 'atk_max': 150, 'money_min': 1200, 'money_max': 1800, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 1.0, 'crit_boost': 1.0, 'prismatic_magic_pack': 0.8, 'divine_magic_pack': 0.8, 'soul_shard': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 91, 'element': 'mana', 'exp_min': 600, 'exp_max': 1200},
    {'name': 'Void Walker II', 'hp': 2800, 'atk_min': 140, 'atk_max': 180, 'money_min': 1400, 'money_max': 2000, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 1.0, 'crit_boost': 1.0, 'prismatic_magic_pack': 0.8, 'divine_magic_pack': 0.8, 'soul_shard': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 93, 'element': 'mana', 'exp_min': 700, 'exp_max': 1400},
    {'name': 'Dragon Hatchling', 'hp': 3200, 'atk_min': 130, 'atk_max': 170, 'money_min': 1600, 'money_max': 2300, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 1.0, 'crit_boost': 1.0, 'prismatic_magic_pack': 0.8, 'divine_magic_pack': 0.8, 'soul_shard': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 95, 'element': 'fire', 'exp_min': 800, 'exp_max': 1600},
    {'name': 'Storm Elemental', 'hp': 3600, 'atk_min': 160, 'atk_max': 200, 'money_min': 1800, 'money_max': 2600, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 1.0, 'crit_boost': 1.0, 'prismatic_magic_pack': 0.8, 'divine_magic_pack': 0.8, 'soul_shard': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 97, 'element': 'lightning', 'exp_min': 900, 'exp_max': 1800},
    {'name': 'Phoenix Chick', 'hp': 4000, 'atk_min': 150, 'atk_max': 190, 'money_min': 2000, 'money_max': 2900, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 1.0, 'crit_boost': 1.0, 'prismatic_magic_pack': 0.8, 'divine_magic_pack': 0.8, 'soul_shard': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 99, 'element': 'fire', 'exp_min': 1000, 'exp_max': 2000},
    
    # SS(Transcendent) monsters - Areas 90-99
    {'name': 'Transcendent Being', 'hp': 1600, 'atk_min': 100, 'atk_max': 130, 'money_min': 600, 'money_max': 800, 'class': 'SS(Transcendent)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'transcendent_heart': 0.2, 'divine_magic_pack': 0.3, 'transcendent_magic_pack': 0.3, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2}, 'weight': 1, 'area': 90, 'element': 'mana', 'exp_min': 384, 'exp_max': 961},
    {'name': 'Void Emperor', 'hp': 1680, 'atk_min': 104, 'atk_max': 134, 'money_min': 650, 'money_max': 850, 'class': 'SS(Transcendent)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'void_fragment': 0.4, 'divine_magic_pack': 0.3, 'transcendent_magic_pack': 0.35, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2}, 'weight': 1, 'area': 92, 'element': 'mana', 'exp_min': 384, 'exp_max': 961},
    {'name': 'Divine Avatar', 'hp': 1640, 'atk_min': 102, 'atk_max': 132, 'money_min': 630, 'money_max': 830, 'class': 'SS(Transcendent)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'holy_light': 0.4, 'divine_magic_pack': 0.35, 'transcendent_magic_pack': 0.3, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2}, 'weight': 1, 'area': 94, 'element': 'mana', 'exp_min': 384, 'exp_max': 961},
    {'name': 'Cosmic Overlord', 'hp': 1720, 'atk_min': 106, 'atk_max': 136, 'money_min': 670, 'money_max': 870, 'class': 'SS(Transcendent)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'star_dust': 0.4, 'divine_magic_pack': 0.3, 'transcendent_magic_pack': 0.4, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2}, 'weight': 1, 'area': 96, 'element': 'mana', 'exp_min': 384, 'exp_max': 961},
    {'name': 'Void Emperor II', 'hp': 6400, 'atk_min': 220, 'atk_max': 260, 'money_min': 3200, 'money_max': 4700, 'class': 'SS(Transcendent)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 1.0, 'crit_boost': 1.0, 'divine_magic_pack': 0.8, 'transcendent_magic_pack': 0.8, 'soul_shard': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 98, 'element': 'mana', 'exp_min': 1600, 'exp_max': 3200},
    {'name': 'Celestial Emperor II', 'hp': 6800, 'atk_min': 230, 'atk_max': 270, 'money_min': 3400, 'money_max': 5000, 'class': 'SS(Transcendent)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 1.0, 'crit_boost': 1.0, 'divine_magic_pack': 0.8, 'transcendent_magic_pack': 0.8, 'soul_shard': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 99, 'element': 'mana', 'exp_min': 1700, 'exp_max': 3400},
    {'name': 'Dragon Overlord', 'hp': 7200, 'atk_min': 250, 'atk_max': 290, 'money_min': 3600, 'money_max': 5300, 'class': 'SS(Transcendent)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 1.0, 'crit_boost': 1.0, 'divine_magic_pack': 0.8, 'transcendent_magic_pack': 0.8, 'soul_shard': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 99, 'element': 'fire', 'exp_min': 1800, 'exp_max': 3600},
    {'name': 'God of Chaos', 'hp': 8000, 'atk_min': 260, 'atk_max': 300, 'money_min': 4000, 'money_max': 6000, 'class': 'SS(Transcendent)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 1.0, 'crit_boost': 1.0, 'divine_magic_pack': 0.8, 'transcendent_magic_pack': 0.8, 'soul_shard': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 99, 'element': 'mana', 'exp_min': 2000, 'exp_max': 4000},
    
    # Normal Boss monsters - Distributed across all areas
    {'name': 'Goblin King', 'hp': 100, 'atk_min': 15, 'atk_max': 25, 'money_min': 100, 'money_max': 200, 'class': 'D(Common)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 0.8, 'strength_boost': 0.3, 'defense_boost': 0.2, 'goblin_tooth': 0.8, 'common_magic_pack': 0.3, 'perm_exp_upgrade': 0.5, 'perm_strength_upgrade': 0.5, 'perm_defense_upgrade': 0.5, 'perm_health_upgrade': 0.5, 'perm_mana_upgrade': 0.5, 'perm_crit_chance_upgrade': 0.5, 'perm_mana_regen_upgrade': 0.5, 'perm_lifesteal_upgrade': 0.5, 'perm_lifesteal_chance_upgrade': 0.5}, 'weight': 0.5, 'area': 10, 'exp_min': 50, 'exp_max': 100},
    {'name': 'Wolf Alpha', 'hp': 150, 'atk_min': 20, 'atk_max': 30, 'money_min': 150, 'money_max': 250, 'class': 'D(Common)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 0.8, 'strength_boost': 0.3, 'defense_boost': 0.2, 'wolf_pelt': 0.8, 'common_magic_pack': 0.3, 'perm_exp_upgrade': 0.5, 'perm_strength_upgrade': 0.5, 'perm_defense_upgrade': 0.5, 'perm_health_upgrade': 0.5, 'perm_mana_upgrade': 0.5, 'perm_crit_chance_upgrade': 0.5, 'perm_mana_regen_upgrade': 0.5, 'perm_lifesteal_upgrade': 0.5, 'perm_lifesteal_chance_upgrade': 0.5}, 'weight': 0.5, 'area': 20, 'exp_min': 75, 'exp_max': 150},
    {'name': 'Dark Mage Lord', 'hp': 400, 'atk_min': 40, 'atk_max': 60, 'money_min': 300, 'money_max': 500, 'class': 'C(Rare)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 0.8, 'strength_boost': 0.4, 'defense_boost': 0.3, 'crit_boost': 0.2, 'rare_magic_pack': 0.5, 'dark_essence': 0.8, 'perm_exp_upgrade': 0.6, 'perm_strength_upgrade': 0.6, 'perm_defense_upgrade': 0.6, 'perm_health_upgrade': 0.6, 'perm_mana_upgrade': 0.6, 'perm_crit_chance_upgrade': 0.6, 'perm_mana_regen_upgrade': 0.6, 'perm_lifesteal_upgrade': 0.6, 'perm_lifesteal_chance_upgrade': 0.6}, 'weight': 0.5, 'area': 30, 'exp_min': 150, 'exp_max': 300},
    {'name': 'Troll King', 'hp': 800, 'atk_min': 60, 'atk_max': 90, 'money_min': 500, 'money_max': 800, 'class': 'C(Rare)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 0.8, 'strength_boost': 0.5, 'defense_boost': 0.4, 'regen_potion': 0.4, 'rare_magic_pack': 0.6, 'troll_core': 0.8, 'perm_exp_upgrade': 0.7, 'perm_strength_upgrade': 0.7, 'perm_defense_upgrade': 0.7, 'perm_health_upgrade': 0.7, 'perm_mana_upgrade': 0.7, 'perm_crit_chance_upgrade': 0.7, 'perm_mana_regen_upgrade': 0.7, 'perm_lifesteal_upgrade': 0.7, 'perm_lifesteal_chance_upgrade': 0.7}, 'weight': 0.5, 'area': 40, 'exp_min': 250, 'exp_max': 500},
    {'name': 'Shadow Assassin Master', 'hp': 1200, 'atk_min': 80, 'atk_max': 120, 'money_min': 800, 'money_max': 1200, 'class': 'B(Mythical)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 0.8, 'strength_boost': 0.6, 'defense_boost': 0.5, 'crit_boost': 0.4, 'mythical_magic_pack': 0.6, 'shadow_cloak': 0.8, 'perm_exp_upgrade': 0.8, 'perm_strength_upgrade': 0.8, 'perm_defense_upgrade': 0.8, 'perm_health_upgrade': 0.8, 'perm_mana_upgrade': 0.8, 'perm_crit_chance_upgrade': 0.8, 'perm_mana_regen_upgrade': 0.8, 'perm_lifesteal_upgrade': 0.8, 'perm_lifesteal_chance_upgrade': 0.8}, 'weight': 0.5, 'area': 50, 'exp_min': 400, 'exp_max': 800},
    {'name': 'Ice Queen', 'hp': 1800, 'atk_min': 100, 'atk_max': 150, 'money_min': 1200, 'money_max': 1800, 'class': 'B(Mythical)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 0.8, 'strength_boost': 0.6, 'defense_boost': 0.6, 'regen_potion': 0.5, 'mythical_magic_pack': 0.7, 'frozen_heart': 0.8, 'perm_exp_upgrade': 0.8, 'perm_strength_upgrade': 0.8, 'perm_defense_upgrade': 0.8, 'perm_health_upgrade': 0.8, 'perm_mana_upgrade': 0.8, 'perm_crit_chance_upgrade': 0.8, 'perm_mana_regen_upgrade': 0.8, 'perm_lifesteal_upgrade': 0.8, 'perm_lifesteal_chance_upgrade': 0.8}, 'weight': 0.5, 'area': 60, 'exp_min': 600, 'exp_max': 1200},
    {'name': 'Void Lord Prime', 'hp': 2400, 'atk_min': 150, 'atk_max': 200, 'money_min': 1800, 'money_max': 2500, 'class': 'A(Prismatic)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 0.8, 'strength_boost': 0.7, 'defense_boost': 0.6, 'crit_boost': 0.5, 'prismatic_magic_pack': 0.7, 'void_fragment': 0.8, 'perm_exp_upgrade': 0.9, 'perm_strength_upgrade': 0.9, 'perm_defense_upgrade': 0.9, 'perm_health_upgrade': 0.9, 'perm_mana_upgrade': 0.9, 'perm_crit_chance_upgrade': 0.9, 'perm_mana_regen_upgrade': 0.9, 'perm_lifesteal_upgrade': 0.9, 'perm_lifesteal_chance_upgrade': 0.9}, 'weight': 0.5, 'area': 70, 'exp_min': 900, 'exp_max': 1800},
    {'name': 'Celestial Emperor', 'hp': 3200, 'atk_min': 200, 'atk_max': 280, 'money_min': 2500, 'money_max': 3500, 'class': 'A(Prismatic)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 0.8, 'strength_boost': 0.8, 'defense_boost': 0.7, 'mana_upgrade_potion': 0.6, 'prismatic_magic_pack': 0.8, 'holy_light': 0.8, 'perm_exp_upgrade': 0.9, 'perm_strength_upgrade': 0.9, 'perm_defense_upgrade': 0.9, 'perm_health_upgrade': 0.9, 'perm_mana_upgrade': 0.9, 'perm_crit_chance_upgrade': 0.9, 'perm_mana_regen_upgrade': 0.9, 'perm_lifesteal_upgrade': 0.9, 'perm_lifesteal_chance_upgrade': 0.9}, 'weight': 0.5, 'area': 80, 'exp_min': 1200, 'exp_max': 2400},
    {'name': 'Eternal Dragon Lord', 'hp': 4800, 'atk_min': 300, 'atk_max': 400, 'money_min': 3500, 'money_max': 5000, 'class': 'S(Divine)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 0.8, 'strength_boost': 0.9, 'defense_boost': 0.8, 'crit_boost': 0.7, 'divine_magic_pack': 0.8, 'dragon_scale': 0.8, 'perm_exp_upgrade': 0.9, 'perm_strength_upgrade': 0.9, 'perm_defense_upgrade': 0.9, 'perm_health_upgrade': 0.9, 'perm_mana_upgrade': 0.9, 'perm_crit_chance_upgrade': 0.9, 'perm_mana_regen_upgrade': 0.9, 'perm_lifesteal_upgrade': 0.9, 'perm_lifesteal_chance_upgrade': 0.9}, 'weight': 0.5, 'area': 90, 'exp_min': 1800, 'exp_max': 3600},
    
    # Boss monsters - Area 100 (Original bosses with increased stats)
    {'name': 'Goblin King', 'hp': 400, 'atk_min': 100, 'atk_max': 200, 'money_min': 200, 'money_max': 400, 'class': 'D(Common)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.5, 'defense_boost': 0.3, 'goblin_tooth': 1.0, 'common_magic_pack': 0.5, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 100, 'exp_min': 250, 'exp_max': 500},
    {'name': 'Skeleton King', 'hp': 1000, 'atk_min': 220, 'atk_max': 350, 'money_min': 750, 'money_max': 2000, 'class': 'B(Mythical)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.8, 'defense_boost': 0.5, 'crit_boost': 0.4, 'rare_magic_pack': 0.8, 'mythical_magic_pack': 0.4, 'skeleton_bone': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 100, 'exp_min': 250, 'exp_max': 500},
    {'name': 'Troll Chieftain', 'hp': 1600, 'atk_min': 240, 'atk_max': 300, 'money_min': 1500, 'money_max': 3000, 'class': 'C(Rare)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.7, 'defense_boost': 0.6, 'regen_potion': 0.5, 'rare_magic_pack': 0.7, 'mythical_magic_pack': 0.3, 'troll_core': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 100, 'exp_min': 562, 'exp_max': 1125},
    {'name': 'Dark Lord', 'hp': 2400, 'atk_min': 270, 'atk_max': 378, 'money_min': 2500, 'money_max': 5000, 'class': 'B(Mythical)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.8, 'defense_boost': 0.6, 'crit_boost': 0.5, 'mythical_magic_pack': 0.8, 'prismatic_magic_pack': 0.4, 'dark_essence': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 100, 'exp_min': 843, 'exp_max': 1687},
    {'name': 'Ice Queen', 'hp': 3000, 'atk_min': 300, 'atk_max': 400, 'money_min': 3500, 'money_max': 6000, 'class': 'B(Mythical)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'defense_boost': 0.8, 'regen_potion': 0.7, 'mythical_magic_pack': 0.7, 'prismatic_magic_pack': 0.5, 'frozen_heart': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 100, 'exp_min': 1265, 'exp_max': 2531},
    {'name': 'Phoenix Lord', 'hp': 3600, 'atk_min': 200, 'atk_max': 300, 'money_min': 4500, 'money_max': 7500, 'class': 'A(Prismatic)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.8, 'mana_upgrade_potion': 0.6, 'mythical_magic_pack': 0.8, 'prismatic_magic_pack': 0.6, 'phoenix_feather': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 100, 'exp_min': 1898, 'exp_max': 3796},
    {'name': 'Void Master', 'hp': 4400, 'atk_min': 380, 'atk_max': 480, 'money_min': 6000, 'money_max': 10000, 'class': 'A(Prismatic)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.9, 'defense_boost': 0.8, 'crit_boost': 0.7, 'prismatic_magic_pack': 0.8, 'divine_magic_pack': 0.4, 'void_fragment': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 100, 'exp_min': 2847, 'exp_max': 5695},
    {'name': 'Celestial Emperor', 'hp': 5600, 'atk_min': 500, 'atk_max': 700, 'money_min': 8000, 'money_max': 13000, 'class': 'S(Divine)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.9, 'defense_boost': 0.9, 'mana_upgrade_potion': 0.7, 'prismatic_magic_pack': 0.8, 'divine_magic_pack': 0.6, 'holy_light': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 100, 'exp_min': 4271, 'exp_max': 8542},
    {'name': 'Dragon Lord', 'hp': 7000, 'atk_min': 500, 'atk_max': 700, 'money_min': 10000, 'money_max': 16000, 'class': 'S(Divine)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 0.9, 'crit_boost': 0.8, 'divine_magic_pack': 0.8, 'transcendent_magic_pack': 0.4, 'dragon_scale': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 100, 'exp_min': 6407, 'exp_max': 12814},
    {'name': 'Grim Reaper', 'hp': 8000, 'atk_min': 600, 'atk_max': 1000, 'money_min': 12000, 'money_max': 20000, 'class': 'S(Divine)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 1.0, 'crit_boost': 1.0, 'prismatic_magic_pack': 0.8, 'divine_magic_pack': 0.8, 'soul_shard': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 1, 'area': 100, 'exp_min': 9615670, 'exp_max': 10926721},
    
    # Super Boss monsters - Area 100 (Stats remain as they are already extremely high)
    {'name': 'Demon King Muzan', 'hp': 136980000, 'atk_min': 40000, 'atk_max': 50000, 'money_min': 100000000, 'money_max': 50000000000, 'class': 'SS(Transcendent)', 'is_boss': True, 'is_super_boss': True, 'drop': {'potion': 1.0, 'strength_boost': 1, 'defense_boost': 1, 'crit_boost': 1, 'transcendent_heart': 0.5, 'divine_magic_pack': 0.8, 'transcendent_magic_pack': 0.4, 'demon_horn': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 0.01, 'area': 100, 'exp_min': 8000000000, 'exp_max': 10000000000},
    {'name': 'Abyssal Dragon', 'hp': 120000000, 'atk_min': 35000, 'atk_max': 45000, 'money_min': 50000000, 'money_max': 30000000000, 'class': 'SS(Transcendent)', 'is_boss': True, 'is_super_boss': True, 'drop': {'potion': 1.0, 'strength_boost': 1, 'defense_boost': 1, 'crit_boost': 1, 'transcendent_heart': 0.4, 'divine_magic_pack': 0.7, 'transcendent_magic_pack': 0.5, 'dragon_scale': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 0.01, 'area': 100, 'exp_min': 7000000000, 'exp_max': 9000000000},
    {'name': 'Void Emperor', 'hp': 125000000, 'atk_min': 36000, 'atk_max': 46000, 'money_min': 60000000, 'money_max': 35000000000, 'class': 'SS(Transcendent)', 'is_boss': True, 'is_super_boss': True, 'drop': {'potion': 1.0, 'strength_boost': 1, 'defense_boost': 1, 'crit_boost': 1, 'transcendent_heart': 0.45, 'divine_magic_pack': 0.75, 'transcendent_magic_pack': 0.45, 'void_core': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 0.01, 'area': 100, 'exp_min': 7500000000, 'exp_max': 9500000000},
    {'name': 'Celestial Phoenix', 'hp': 118000000, 'atk_min': 34000, 'atk_max': 44000, 'money_min': 55000000, 'money_max': 32000000000, 'class': 'SS(Transcendent)', 'is_boss': True, 'is_super_boss': True, 'drop': {'potion': 1.0, 'strength_boost': 1, 'defense_boost': 1, 'crit_boost': 1, 'transcendent_heart': 0.42, 'divine_magic_pack': 0.72, 'transcendent_magic_pack': 0.42, 'phoenix_feather': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 0.01, 'area': 100, 'exp_min': 7200000000, 'exp_max': 9200000000},
    {'name': 'Eternal Titan', 'hp': 130000000, 'atk_min': 37000, 'atk_max': 47000, 'money_min': 65000000, 'money_max': 40000000000, 'class': 'SS(Transcendent)', 'is_boss': True, 'is_super_boss': True, 'drop': {'potion': 1.0, 'strength_boost': 1, 'defense_boost': 1, 'crit_boost': 1, 'transcendent_heart': 0.48, 'divine_magic_pack': 0.78, 'transcendent_magic_pack': 0.48, 'titan_core': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0}, 'weight': 0.01, 'area': 100, 'exp_min': 7700000000, 'exp_max': 9700000000},
]
MONSTER_ALIASES = {
    'boss': {'gk': 'Goblin King', 'sk': 'Skeleton King', 'tc': 'Troll Chieftain', 'dl': 'Dark Lord', 'iq': 'Ice Queen', 'pl': 'Phoenix Lord', 'vm': 'Void Master', 'ce': 'Celestial Emperor', 'drl': 'Dragon Lord', 'gr': 'Grim Reaper', 'dkm': 'Demon King Muzan', 'ad': 'Abyssal Dragon', 'vesb': 'Void Emperor', 'cpsb': 'Celestial Phoenix', 'et': 'Eternal Titan'},
    'normal': {'sl': 'Slime', 'g': 'Goblin', 'w': 'Wolf', 'gs': 'Goblin Shaman', 'sf': 'Forest Sprite', 'skel': 'Skeleton', 'o': 'Orc', 'sp': 'Giant Spider', 'bt': 'Dark Bat', 'b': 'Bandit', 'ow': 'Orc Warrior', 'dm': 'Dark Mage', 'sg': 'Stone Golem', 't': 'Troll', 'ie': 'Ice Elemental', 'fe': 'Fire Elemental', 'tb': 'Thunder Bird', 'dk': 'Dark Knight', 'sa': 'Shadow Assassin', 'am': 'Arcane Mage', 'wl': 'Warlock', 'ig': 'Ice Giant', 'p': 'Phoenix', 'cg': 'Crystal Golem', 'sd': 'Storm Dragon', 'vw': 'Void Walker', 'cg2': 'Celestial Guardian', 'sw': 'Star Weaver', 'ms': 'Moon Sentinel', 'sc': 'Sun Champion', 'vl': 'Void Lord', 'dp': 'Divine Paladin', 'cm': 'Cosmic Mage', 'ed': 'Eternal Dragon', 'vr': 'Void Reaper', 'cp': 'Celestial Phoenix', 'ce2': 'Cosmic Entity', 'tb2': 'Transcendent Being', 've': 'Void Emperor', 'da': 'Divine Avatar', 'co': 'Cosmic Overlord', 'swr': 'Shadow Wraith', 'cb': 'Celestial Beast', 'vwii': 'Void Walker II', 'dh': 'Dragon Hatchling', 'se': 'Storm Elemental', 'pc': 'Phoenix Chick', 'af': 'Abyssal Fiend', 'tt': 'Thunder Titan', 'hp': 'Holy Paladin', 'cw': 'Cosmic Wanderer', 'ef': 'Eternal Flame', 'veii': 'Void Emperor II', 'cei': 'Celestial Emperor II', 'do': 'Dragon Overlord', 'goc': 'God of Chaos'}
    }

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

def explore_dungeon(username):
    """Explore the dungeon to find treasure"""
    user_data = load_user_data(username)
    if not user_data:
        return 'User not found.'
    player_data = user_data['player_data']
    stats = player_data['stats']
    inventory = player_data['inventory']
    if stats['hp'] < stats['hp_max'] * 0.3:
        return 'You need at least 30% health to explore the dungeon.'
    stats['hp'] = max(1, stats['hp'] - stats['hp_max'] * 0.1)
    area = stats.get('current_area', 1)
    level = stats.get('level', 1)
    base_treasure = 100 + area * 50 + level * 20
    treasure_boost = stats.get('title_treasure_boost', 0)
    if treasure_boost > 0:
        boosted_amount = base_treasure * (treasure_boost / 100.0)
        base_treasure += boosted_amount
    treasure_found = int(base_treasure * random.uniform(0.8, 1.5))
    global dungeon_treasure
    treasure_found = min(treasure_found, dungeon_treasure)
    user_data['money'] += treasure_found
    stats['dungeon_treasure_collected'] = stats.get('dungeon_treasure_collected', 0) + treasure_found
    stats['total_money_earned'] = stats.get('total_money_earned', 0) + treasure_found
    dungeon_treasure -= treasure_found
    load_dungeon_treasure()
    save_dungeon_treasure()
    update_user(username, money=user_data['money'], player_data=user_data['player_data'])

def use_potions_interface(username, player_hp, player_mana, stats, inventory, active_buffs):
    try:
        user_data = load_user_data(username)
        if user_data:
            saved_player_data = user_data.get('player_data', {})
            saved_stats = saved_player_data.get('stats', {})
            saved_inventory = saved_player_data.get('inventory', {})
            player_hp = saved_stats.get('hp', player_hp)
            player_mana = saved_stats.get('mana', player_mana)
            stats = saved_stats
            inventory = saved_inventory
    except Exception as e:
        pass
    while True:
        print('\n--- Use Potions ---')
        print(f"HP: {player_hp}/{stats.get('hp_max')} | Mana: {player_mana}/{stats.get('mana_max')}")
        print('Available potions:')
        potion_list = []
        for key, count in inventory.items():
            if count > 0 and key in POTIONS:
                potion_list.append((key, POTIONS[key]['name'], count))
                print(f"{len(potion_list)}. {POTIONS[key]['name']} x{count}")
        print('0. Back')
        choice = input('Choose potion to use (e.g., 1 or 1 3 for quantity): ').strip()
        parts = choice.split()
        if not parts or not parts[0].isdigit():
            print('Invalid choice.')
            continue
        opt = parts[0]
        qty = int(parts[1]) if len(parts) > 1 else 1
        if qty < 1:
            qty = 1
        if opt == '0':
            break
        elif opt.isdigit():
            idx = int(opt) - 1
            if 0 <= idx < len(potion_list):
                potion_key, potion_name, count = potion_list[idx]
                if count >= qty:
                    effect = POTIONS[potion_key]['effect']
                    amount = POTIONS[potion_key].get('amount', 0)
                    for _ in range(qty):
                        if effect == 'heal':
                            heal_amount = min(amount, stats.get('hp_max', 100) - player_hp)
                            if heal_amount > 0:
                                player_hp += heal_amount
                                print(f"You used {potion_name} and healed {heal_amount} HP! (HP: {player_hp}/{stats.get('hp_max')})")
                            else:
                                print('You are already at full HP.')
                        elif effect == 'heal_mana':
                            mana_heal = min(amount, stats.get('mana_max', 50) - player_mana)
                            if mana_heal > 0:
                                player_mana += mana_heal
                                print(f"You used {potion_name} and restored {mana_heal} Mana! (Mana: {player_mana}/{stats.get('mana_max')})")
                            else:
                                print('You are already at full Mana.')
                        elif effect == 'full_mana':
                            player_mana = stats.get('mana_max', 50)
                            print(f"You used {potion_name} and restored full Mana! (Mana: {player_mana}/{stats.get('mana_max')})")
                        elif effect.startswith('buff'):
                            buff_type = effect[5:]
                            duration = POTIONS[potion_key]['duration']
                            active_buffs.append({'type': buff_type, 'amount': amount, 'remaining': duration})
                            print(f"You used {potion_name} and gained {amount} {buff_type.replace('_', ' ')} for {duration} fights!")
                    inventory[potion_key] -= qty
                    stats['hp'] = player_hp
                    stats['mana'] = player_mana
                    player_data = {'stats': stats, 'inventory': inventory}
                    user_data = load_user_data(username)
                    if user_data:
                        user_data['player_data'] = player_data
                        save_user_data(username, user_data)
                else:
                    print(f'Not enough {potion_name} (have {count}).')
            else:
                print('Invalid choice.')
        else:
            print('Invalid choice.')
    return (player_hp, player_mana, active_buffs)

def use_buff_interface(username, player_hp, player_mana, stats, inventory, active_buffs):
    try:
        user_data = load_user_data(username)
        if user_data:
            saved_player_data = user_data.get('player_data', {})
            saved_inventory = saved_player_data.get('inventory', {})
            inventory = saved_inventory
    except Exception as e:
        pass
    while True:
        print('\n--- Use Buffs ---')
        print('Available buffs:')
        buff_list = []
        for key, count in inventory.items():
            if count > 0 and key in POTIONS and POTIONS[key]['effect'].startswith('buff'):
                buff_list.append((key, POTIONS[key]['name'], count))
                print(f"{len(buff_list)}. {POTIONS[key]['name']} x{count}")
        print('0. Back')
        choice = input('Choose buff to use (e.g., 1 or 1 3 for quantity): ').strip()
        parts = choice.split()
        if not parts or not parts[0].isdigit():
            print('Invalid choice.')
            continue
        opt = parts[0]
        qty = int(parts[1]) if len(parts) > 1 else 1
        if qty < 1:
            qty = 1
        if opt == '0':
            break
        elif opt.isdigit():
            idx = int(opt) - 1
            if 0 <= idx < len(buff_list):
                buff_key, buff_name, count = buff_list[idx]
                if count >= qty:
                    effect = POTIONS[buff_key]['effect']
                    amount = POTIONS[buff_key]['amount']
                    for _ in range(qty):
                        if effect.startswith('buff'):
                            buff_type = effect[5:]
                            duration = POTIONS[buff_key]['duration']
                            active_buffs.append({'type': buff_type, 'amount': amount, 'remaining': duration})
                            print(f"You used {buff_name} and gained {amount} {buff_type.replace('_', ' ')} for {duration} fights!")
                    inventory[buff_key] -= qty
                    player_data = {'stats': stats, 'inventory': inventory}
                    user_data = load_user_data(username)
                    if user_data:
                        user_data['player_data'] = player_data
                        save_user_data(username, user_data)
                else:
                    print(f'Not enough {buff_name} (have {count}).')
            else:
                print('Invalid choice.')
        else:
            print('Invalid choice.')
    return (player_hp, player_mana, active_buffs)

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
                stats['hp_max'] += 2500
                stats['mana_max'] += 750
                stats['atk'] += 1000
                stats['defense'] += 500
                stats['perm_atk'] += 500
                stats['perm_def'] += 200
                stats['perm_hp_max'] += 5000
                stats['perm_mana_max'] += 250
                stats['perm_crit_chance'] += 500
                stats['perm_mana_regen'] += 200
                stats['perm_lifesteal'] += 200
                stats['perm_lifesteal_chance'] += 200
                stats['perm_exp_boost'] += 500
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

def dungeon(username):
    global exp_gain
    '\n    Dungeon combat loop that uses:\n      - apply_permanent_upgrades(username)\n      - compute_effective_stats(...)\n      - get_equip_and_perm_bonuses(stats)\n      - apply_damage_with_defense(...) and apply_magic_damage(...)\n      - calculate_total_crit_chance(...)\n    '
    try:
        apply_permanent_upgrades(username)
    except Exception:
        pass
    user_data = load_user_data(username)
    if not user_data:
        print('User not found.')
        return
    player_data = user_data.get('player_data', {})
    score = user_data.get('score', 0)
    money = user_data.get('money', 40)
    stats = player_data.get('stats', {})
    inventory = player_data.get('inventory', {})
    settings = stats.get('settings', {})
    if settings.get('auto_equip_best', False) or settings.get('auto_equip_everything', False):
        try:
            auto_equip_items(username)
            user_data = load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
        except Exception:
            pass
    if settings.get('auto_equip_spells', False) or settings.get('auto_equip_everything', False):
        try:
            auto_equip_spells(username)
            user_data = load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
        except Exception:
            pass
    active_buffs = []
    forced_monster = None
    if stats.get('settings', {}).get('call_including_title', True) and stats.get('title'):
        name_display = f"{stats['title']} {username}"
    print(f'\n⚔️ Welcome to the Dungeon, brave {name_display}!')
    check_stats(username)
    player_hp = stats.get('hp', stats.get('hp_max', 100))
    player_mana = stats.get('mana', stats.get('mana_max', 50))
    bonuses = get_equip_and_perm_bonuses(stats)
    w_atk = bonuses.get('weapon_atk', 0)
    a_def = bonuses.get('armor_def', 0)
    n_atk = bonuses.get('neck_atk', 0)
    equipped_atk = bonuses.get('total_base_atk', stats.get('atk', 5)) + w_atk + n_atk
    equipped_def = bonuses.get('total_base_def', stats.get('defense', 0)) + a_def + bonuses.get('neck_def', 0)
    current_area = stats.get('current_area', 1)
    print(f"Entering dungeon with HP: {player_hp}, MANA: {player_mana}, ATK: {equipped_atk}, DEF: {equipped_def}, LVL: {stats.get('level', 1)}, AREA: {current_area}")
    print(f"Base ATK (with perm): {bonuses.get('total_base_atk', stats.get('atk', 5))}, Base DEF (with perm): {bonuses.get('total_base_def', stats.get('defense', 0))}")
    while True:
        cmd = input("\nType 'explore' to find a monster, 'status' to view stats, 'shop' to access shop, 'packs' to open magic packs, 'upgrades' to use permanent upgrades, 'potions' to use potions, 'move' to change areas, or 'exit' to leave the dungeon: ").strip()
        if not cmd:
            continue
        lc = cmd.lower().strip()
        if lc == 'exit':
            print('You leave the dungeon safely.')
            stats['hp'] = player_hp
            stats['mana'] = player_mana
            player_data['stats'] = stats
            player_data['inventory'] = inventory
            user_data['player_data'] = player_data
            save_user_data(username, user_data)
            return
        if lc == 'shop':
            shop()
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'packs':
            magic_pack_interface(username)
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'titles':
            equip_titles_menu(username, player_data, None)
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'inventory':
            manage_inventory_menu(username, player_data, None)
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'spells':
            magic_spell_interface(username)
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'status':
            try:
                apply_permanent_upgrades(username)
            except Exception:
                pass
            effective_atk, effective_def, effective_magic_atk, effective_magic_def, _, _, _, _ = compute_effective_stats(stats, active_buffs)
            next_exp = exp_to_next(stats.get('level', 1)) if stats.get('level', 1) < MAX_LEVEL else 'MAX'
            money = user_data.get('money')
            name_display = username
            if stats.get('settings', {}).get('call_including_title', True) and stats.get('title'):
                name_display = f"{stats['title']} {username}"
            exp_display = create_exp_bar(stats.get('exp'), next_exp) if stats.get('settings', {}).get('show_exp_bar', False) else f"{stats.get('exp')}/{next_exp}"
            print(f"{name_display} - HP: {player_hp}/{stats.get('hp_max')}, MANA: {player_mana}/{stats.get('mana_max')}, ATK: {effective_atk}, DEF: {effective_def}, Money: ${money}, LVL: {stats.get('level')}, EXP: {exp_display}, AREA: {stats.get('current_area', 1)}")
            print(f"Permanent Boosts: ATK +{stats.get('perm_atk', 0)}, DEF +{stats.get('perm_def', 0)}, HP +{stats.get('perm_hp_max', 0)}, Mana +{stats.get('perm_mana_max', 0)}, Crit +{stats.get('perm_crit_chance', 0)}%, Regen +{stats.get('perm_mana_regen', 0)}, Lifesteal +{stats.get('perm_lifesteal', 0)}%, Exp +{stats.get('perm_exp_boost', 0)}%")
            if active_buffs:
                print('Active buffs:')
                for b in active_buffs:
                    if b.get('remaining', 0) > 0:
                        print(f' - {b}')
            continue
        if lc == 'shop':
            shop()
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'packs':
            magic_pack_interface(username)
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'upgrades':
            permanent_upgrades_interface(username)
            continue
        if lc == 'potions':
            player_hp, player_mana, active_buffs = use_potions_interface(username, player_hp, player_mana, stats, inventory, active_buffs)
            continue
        if lc == 'move':
            print(f"\nCurrent Area: {stats.get('current_area', 1)}")
            print('You can move to areas 1-100. Higher areas have stronger monsters.')
            try:
                new_area = input("Enter area number (1-10) or 'cancel': ").strip()
                if new_area.lower() == 'cancel':
                    continue
                new_area = int(new_area)
                if 1 <= new_area <= 100:
                    player_level = stats.get('level', 1)
                    min_level = (new_area - 1) * LEVELS_PER_AREA + 1
                    if player_level < min_level:
                        print(f'You need to be at least level {min_level} to enter Area {new_area}. Your current level is {player_level}.')
                        continue
                    stats['current_area'] = new_area
                    current_area = new_area
                    player_data['stats'] = stats
                    user_data['player_data'] = player_data
                    save_user_data(username, user_data)
                    print(f'Moved to Area {new_area}!')
                else:
                    print('Invalid area. Must be between 1 and 100.')
            except Exception:
                print('Invalid input. Enter a number between 1 and 100.')
            continue
        if lc.startswith('explore'):
            parts = cmd.split()
            if len(parts) >= 4:
                code = parts[1].strip()
                if code == '10234':
                    flag = parts[2].strip().lower()
                    alias = parts[3].strip().lower()
                    if flag in ('y', 'yes', 'boss', 'b'):
                        aliases = MONSTER_ALIASES.get('boss', {})
                        monster_name = aliases.get(alias)
                        if monster_name:
                            found = next((m for m in MONSTERS if m['name'].lower() == monster_name.lower()), None)
                            if found:
                                monster = found.copy()
                                print(f"\n🔥 BOSS APPEARS: {monster['name']}! (HP {monster.get('hp')}, ATK {monster.get('atk_min', '?')}–{monster.get('atk_max', '?')})")
                            else:
                                continue
                        else:
                            continue
                    elif flag in ('n', 'no', 'normal', 'monster', 'm'):
                        aliases = MONSTER_ALIASES.get('normal', {})
                        monster_name = aliases.get(alias)
                        if monster_name:
                            found = next((m for m in MONSTERS if m['name'].lower() == monster_name.lower()), None)
                            if found:
                                monster = found.copy()
                                print(f"\nA wild {monster['name']} appears! (HP {monster.get('hp')}, ATK {monster.get('atk_min', '?')}–{monster.get('atk_max', '?')})")
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            else:
                roll = random.randint(1, 100)
                if roll <= 5:
                    area = stats.get('current_area', 1)
                    monster = choose_boss_for_area(area)
                    print(f"\n🔥 BOSS APPEARS: {monster['name']}! (HP {monster.get('hp')}, ATK {monster.get('atk_min', '?')}–{monster.get('atk_max', '?')})")
                else:
                    area = stats.get('current_area', 1)
                    monster = choose_monster_for_area(area)
                    print(f"\nA wild {monster['name']} appears! (HP {monster.get('hp')}, ATK {monster.get('atk_min', '?')}–{monster.get('atk_max', '?')})")
            monster_original_hp = monster['hp']
            fight_happened = False
            monster_stunned = False
            while monster.get('hp', 0) > 0 and player_hp > 0:
                fight_happened = True
                try:
                    apply_permanent_upgrades(username)
                except Exception:
                    pass
                effective_atk, effective_def, effective_magic_atk, effective_magic_def, _, _, _, _ = compute_effective_stats(stats, active_buffs)
                total_crit_chance = calculate_total_crit_chance(stats, active_buffs)
                while True:
                    action = input('Do you want to (a)ttack, (m)agic, (d)odge, (p)otion, (u)se buff, or (r)un? ').lower().strip()
                    if action in ['a', 'm', 'd', 'p', 'u', 'r']:
                        break
                    else:
                        print('Invalid action. Please choose (a)ttack, (m)agic, (d)odge, (p)otion, (u)se buff, or (r)un.')
                if action == 'a':
                    bonuses = get_equip_and_perm_bonuses(stats)
                    weapon_bonus = bonuses.get('weapon_atk', 0) + bonuses.get('neck_atk', 0)
                    total_base_atk = bonuses.get('total_base_atk', effective_atk)
                    base_roll = random.randint(max(1, total_base_atk - 2), total_base_atk + 3)
                    dmg = base_roll + weapon_bonus
                    if 'magic_atk_min' in monster or 'magic_atk_max' in monster:
                        dmg = max(total_base_atk, dmg // 2)
                    if random.random() <= total_crit_chance:
                        dmg = int(dmg * 2)
                        stats['critical_hits'] = stats.get('critical_hits', 0) + 1
                        print('💥 CRITICAL HIT!')
                    monster_def = monster.get('def', 0)
                    damage_after = apply_damage_with_defense(dmg, monster_def)
                    monster['hp'] = monster.get('hp', 0) - damage_after
                    print(f"You hit the {monster['name']} for {damage_after} damage! (Monster HP: {max(0, monster['hp'])})")
                    if random.random() < 0.05:
                        monster_stunned = True
                        print(f"🎯 STUN! The {monster['name']} is stunned!")
                    lifesteal_chance = stats.get('perm_lifesteal_chance', 0) / 100.0
                    lifesteal_percent = stats.get('perm_lifesteal', 0) / 100.0
                    if random.random() <= lifesteal_chance and lifesteal_percent > 0:
                        heal_amount = int(damage_after * lifesteal_percent)
                        if heal_amount > 0:
                            player_hp = min(player_hp + heal_amount, stats.get('hp_max'))
                            print(f"🩸 LIFESTEAL! You stole {heal_amount} HP! (Your HP: {player_hp}/{stats.get('hp_max')})")
                            stats['hp'] = player_hp
                            stats['mana'] = player_mana
                    player_data['stats'] = stats
                    player_data['inventory'] = inventory
                    user_data['player_data'] = player_data
                    save_user_data(username, user_data)
                elif action == 'm':
                    equipped_spells = stats.get('equipped_spells', [None, None, None, None])
                    if not any(equipped_spells):
                        print("You haven't equipped any spells yet. Visit the Magic Spells interface to equip spells!")
                        continue
                    available = [SPELLS_BY_KEY[s] for s in equipped_spells if s is not None and s in SPELLS_BY_KEY]
                    if not available:
                        print("You don't have any equipped spells.")
                        continue
                    print('Equipped spells:')
                    for i, s in enumerate(available, start=1):
                        print(f"{i}. {s['name']} (mana {s['mana']}) - {s.get('desc', '')}")
                    sel = input("Choose spell number or 'cancel': ").strip().lower()
                    if sel in ('cancel', 'c'):
                        continue
                    try:
                        idx = int(sel) - 1
                        if idx < 0 or idx >= len(available):
                            print('Invalid selection.')
                            continue
                        s = available[idx]
                    except Exception:
                        print('Invalid selection.')
                        continue
                    if player_mana < s.get('mana', 0):
                        print('Not enough mana.')
                        continue
                    player_mana -= s.get('mana', 0)
                    if s.get('type') == 'heal':
                        wand_magic = WANDS.get(stats.get('equipped', {}).get('wand'), {}).get('magic_atk', 0)
                        perm_magic_atk = stats.get('perm_magic_atk', 0)
                        heal_power = s.get('power', 0) + wand_magic + perm_magic_atk + random.randint(-(s.get('power', 0) // 8), s.get('power', 0) // 8)
                        if random.random() <= total_crit_chance:
                            heal_power = int(heal_power * 2)
                            stats['critical_hits'] = stats.get('critical_hits', 0) + 1
                            print('✨ CRITICAL HEAL!')
                        player_hp = min(player_hp + heal_power, stats.get('hp_max', 100))
                        print(f"You cast {s['name']} healing yourself for {heal_power} HP! (Your HP: {player_hp}/{stats.get('hp_max')})")
                    else:
                        wand_magic = WANDS.get(stats.get('equipped', {}).get('wand'), {}).get('magic_atk', 0)
                        perm_magic_atk = stats.get('perm_magic_atk', 0)
                        dmg = s.get('power', 0) + wand_magic + perm_magic_atk + random.randint(-(s.get('power', 0) // 8), s.get('power', 0) // 8)
                        if random.random() <= total_crit_chance:
                            dmg = int(dmg * 2)
                            stats['critical_hits'] = stats.get('critical_hits', 0) + 1
                            print('✨ CRITICAL SPELL HIT!')
                        monster_magic_def = monster.get('magic_def', 0)
                        damage_after = apply_magic_damage(dmg, monster_magic_def)
                        monster['hp'] = monster.get('hp', 0) - damage_after
                        print(f"You cast {s['name']} dealing {damage_after} magic damage! (Monster HP: {max(0, monster['hp'])})")
                        if s.get('type') == 'lightning':
                            monster_element = monster.get('element')
                            if monster_element == 'lightning':
                                stun_chance = 0.2
                            else:
                                stun_chance = 0.95
                            if random.random() < stun_chance:
                                monster_stunned = True
                                print(f"⚡ STUN! The {monster['name']} is stunned!")
                        if s.get('type') == 'ice':
                            monster_element = monster.get('element')
                            if monster_element == 'ice':
                                stun_chance = 0.2
                            else:
                                stun_chance = 0.95
                            if random.random() < stun_chance:
                                monster_stunned = True
                                print(f"🧊 STUN! The {monster['name']} is stunned!")
                        lifesteal_chance = stats.get('perm_lifesteal_chance', 0) / 100.0
                        lifesteal_percent = stats.get('perm_lifesteal', 0) / 100.0
                        if random.random() <= lifesteal_chance and lifesteal_percent > 0:
                            heal_amount = int(damage_after * lifesteal_percent)
                            if heal_amount > 0:
                                player_hp = min(player_hp + heal_amount, stats.get('hp_max'))
                                print(f"🩸 LIFESTEAL! You stole {heal_amount} HP! (Your HP: {player_hp}/{stats.get('hp_max')})")
                                stats['hp'] = player_hp
                                stats['mana'] = player_mana
                    player_data['stats'] = stats
                    player_data['inventory'] = inventory
                    user_data['player_data'] = player_data
                    save_user_data(username, user_data)
                elif action == 'p':
                    player_hp, player_mana, active_buffs = use_potions_interface(username, player_hp, player_mana, stats, inventory, active_buffs)
                    user_data = load_user_data(username)
                    player_data = user_data.get('player_data', {})
                    stats = player_data.get('stats', {})
                elif action == 'u':
                    player_hp, player_mana, active_buffs = use_buff_interface(username, player_hp, player_mana, stats, inventory, active_buffs)
                    user_data = load_user_data(username)
                    player_data = user_data.get('player_data', {})
                    stats = player_data.get('stats', {})
                elif action == 'd':
                    if stats.get('dodge_points', 3) > 0:
                        stats['dodge_points'] -= 1
                        print(f"You dodge the attack! Dodges remaining: {stats['dodge_points']}")
                        continue
                    else:
                        print('No dodges remaining!')
                elif action == 'r':
                    if random.random() < 0.5:
                        print('You ran away successfully!')
                        break
                    else:
                        print('Failed to run!')
                if monster.get('hp', 0) > 0:
                    if monster_stunned:
                        print(f"The {monster['name']} is stunned and cannot attack!")
                        monster_stunned = False
                    elif random.random() < 0.05:
                        print(f"The {monster['name']} hesitates and does not attack!")
                    else:
                        monster_dmg = random.randint(monster.get('atk_min', 1), monster.get('atk_max', monster.get('atk_min', 1)))
                        player_def = get_equip_and_perm_bonuses(stats)['total_base_def']
                        damage_to_player = apply_damage_with_defense(monster_dmg, player_def)
                        player_hp -= damage_to_player
                        print(f"The {monster['name']} attacks! You take {damage_to_player} damage! (Your HP: {max(0, player_hp)}/{stats.get('hp_max')})")
                    stats['hp'] = player_hp
                    player_data['stats'] = stats
                    user_data['player_data'] = player_data
                    save_user_data(username, user_data)
                if action != 'd' and stats.get('dodge_points', 0) < stats.get('max_dodge', 3):
                    stats['dodge_points'] = min(stats['max_dodge'], stats['dodge_points'] + 1)
                    print(f"Dodge regenerated! Dodges: {stats['dodge_points']}/{stats['max_dodge']}")
                    if player_hp <= 0:
                        print('You have been defeated!')
                        lost_money = int(user_data['money'] * 0.25)
                        user_data['money'] -= lost_money
                        dungeon_treasure['money'] += lost_money
                        print(f'You lost ${lost_money} to dungeon treasure!')
                        lost_items = []
                        losable_items = [k for k, v in inventory.items() if v > 0 and k not in PERM_UPGRADES]
                        if losable_items:
                            num_to_lose = random.randint(1, min(5, len(losable_items)))
                            for _ in range(num_to_lose):
                                item = random.choice(losable_items)
                                if inventory[item] > 0:
                                    inventory[item] -= 1
                                    lost_items.append(item)
                                    losable_items.remove(item)
                        if lost_items:
                            print(f"You also lost: {', '.join(lost_items)}!")
                        else:
                            print("You didn't lose any items (no items to lose).")
                        player_hp = stats['hp_max']
                        player_mana = stats['mana_max']
                        print(f"But your stats are fully restored! HP: {player_hp}/{stats.get('hp_max')}, Mana: {player_mana}/{stats.get('mana_max')}")
                        replenish_dungeon_treasure()
                        stats['hp'] = player_hp
                        stats['mana'] = player_mana
                        stats['times_died'] = stats.get('times_died', 0) + 1
                        player_data['stats'] = stats
                        player_data['inventory'] = inventory
                        user_data['player_data'] = player_data
                        save_user_data(username, user_data)
                        save_dungeon_treasure()
                        return
                if monster.get('hp', 0) <= 0:
                    money_reward = random.randint(monster.get('money_min', 1), monster.get('money_max', 1))
                    user_data = load_user_data(username)
                    if user_data:
                        money = int(user_data.get('money', 0))
                    else:
                        money = int(player_data.get('money', 0))
                    money += money_reward
                    user_data['money'] = money
                    player_data['money'] = money
                    save_user_data(username, user_data)
                    drops = []
                    for item_name, chance in monster.get('drop', {}).items():
                        if random.random() <= chance:
                            inventory[item_name] = inventory.get(item_name, 0) + 1
                            drops.append(item_name)
                    mat_drops = add_material_drops(inventory, monster)
                    if mat_drops:
                        drops.extend(mat_drops)
                    if monster.get('is_boss') and monster['name'] != 'Skeleton King':
                        for perm_key in PERM_UPGRADES:
                            inventory[perm_key] = inventory.get(perm_key, 0) + 1
                            drops.append(f"{PERM_UPGRADES[perm_key]['name']} (Permanent Upgrade)")
                    stats['monsters_defeated'] = stats.get('monsters_defeated', 0) + 1
                    if monster.get('is_boss'):
                        stats['bosses_defeated'] = stats.get('bosses_defeated', 0) + 1
                    stats['total_money_earned'] = stats.get('total_money_earned', 0) + money_reward
                    stats['hp'] = player_hp
                    stats['mana'] = player_mana
                    player_data['stats'] = stats
                    player_data['inventory'] = inventory
                    user_data['player_data'] = player_data
                    save_user_data(username, user_data)
                    exp_gain = random.randint(monster['exp_min'], monster['exp_max'])
                    exp_gain = grant_exp(username, exp_gain)
                    user_data = load_user_data(username)
                    player_data = user_data.get('player_data', {})
                    stats = player_data.get('stats', {})
                    inventory = player_data.get('inventory', {})
                    player_hp = stats.get('hp', player_hp)
                    player_mana = stats.get('mana', player_mana)
                    if monster.get('is_boss'):
                        boss_bonus = monster_original_hp // 10 * random.randint(10, 50)
                        print(f"🎉 You defeated the BOSS {monster['name']}! +${money_reward} money, +{boss_bonus} score, +{exp_gain} EXP")
                        score += boss_bonus
                        user_data['score'] = score
                        if dungeon_treasure['money'] > 0:
                            treasure_boost_percent = stats.get('title_treasure_boost_percent', 0)
                            recovered_treasure = int(dungeon_treasure['money'] * 0.1)
                            if treasure_boost_percent > 0:
                                recovered_treasure = int(recovered_treasure * (1 + treasure_boost_percent / 100.0))
                            print(f'🏆 You recovered 20% of the dungeon treasure: ${recovered_treasure}!')
                            money += recovered_treasure
                            user_data['money'] = money
                            player_data['money'] = money
                            stats['dungeon_treasure_collected'] = stats.get('dungeon_treasure_collected', 0) + recovered_treasure
                            dungeon_treasure['money'] -= int(dungeon_treasure['money'] * 0.2)
                        for perm_key in PERM_UPGRADES:
                            inventory[perm_key] = inventory.get(perm_key, 0) + 1
                            drops.append(f"{PERM_UPGRADES[perm_key]['name']} (Permanent Upgrade)")
                        boss_drop_pool = list(MATERIALS.keys()) + list(POTIONS.keys()) + list(MAGIC_PACKS.keys())
                        num_random_drops = random.randint(2, 7)
                        boss_drops = random.sample(boss_drop_pool, min(num_random_drops, len(boss_drop_pool)))
                        for item in boss_drops:
                            inventory[item] = inventory.get(item, 0) + 1
                            drops.append(item)
                        if boss_drops:
                            print(f"🎁 Boss reward items: {', '.join(boss_drops)}!")
                        save_dungeon_treasure()
                    else:
                        normal_bonus = monster_original_hp // 5 * random.randint(1, 10)
                        print(f"🎉 You defeated the {monster['name']}! +${money_reward} money, +{normal_bonus} score, +{exp_gain} EXP")
                        score += normal_bonus
                        user_data['score'] = score
                    if drops:
                        print('You found:', ', '.join(drops))
                    stats['hp'] = player_hp
                    stats['mana'] = player_mana
                    player_data['stats'] = stats
                    player_data['inventory'] = inventory
                    user_data['player_data'] = player_data
                    save_user_data(username, user_data)
                    check_achievements(username)
                    save_all_data()
                    save_user_data(username, user_data)
                    break

def shop():
    global current_user
    if not current_user:
        print('You must be logged in to access the shop.')
        return
    user_data = load_user_data(current_user)
    if not user_data:
        print('User data not found.')
        return
    score = user_data.get('score', 0)
    money = user_data.get('money', 40)
    player_data = user_data.get('player_data', {})
    inventory = player_data.get('inventory', {})
    while True:
        print('\n--- Shop ---')
        print(f'Money: ${money} | Score: {score}')
        print("Type the number to purchase, or 'exit' to leave shop.")
        print('----- Potions & Mana -----')
        print('1. Potion (restores 30 HP) - $20')
        print('2. Strong Potion (restores 80 HP) - $80')
        print('3. Ultra Potion (restores 200 HP) - $350')
        print('4. Mana Regen Potion (+15 mana per fight for 4 fights) - $120')
        print('5. Instant Mana (restore full mana) - $60')
        print('\n----- Buffs -----')
        print('6. Strength Boost (+5 ATK next fights) - $60')
        print('7. Defense Boost (+3 DEF next fights) - $60')
        print('8. Regen Potion (+12 HP/fight next fights) - $80')
        print('9. Crit Boost (+50% crit next fights) - $80')
        print('\n----- Weapons -----')
        print(f"10. Wooden Sword (+2 ATK) - ${WEAPONS['wooden_sword']['price']}")
        print(f"11. Iron Sword (+5 ATK) - ${WEAPONS['iron_sword']['price']}")
        print(f"12. Steel Sword (+8 ATK) - ${WEAPONS['steel_sword']['price']}")
        print(f"13. Diamond Sword (+50 ATK) - ${WEAPONS['diamond_sword']['price']}")
        print(f"14. Void Sword (+200 ATK) - ${WEAPONS['void_sword']['price']}")
        print(f"15. Infinitium Sword (+2000 ATK) - ${WEAPONS['infinitium_sword']['price']} and {WEAPONS['infinitium_sword'].get('score_price', 0)} score")
        print(f"16. Frostblade (+120 ATK) - ${WEAPONS['frostblade']['price']} and {WEAPONS['frostblade'].get('score_price', 0)} score")
        print(f"17. Flameblade (+130 ATK) - ${WEAPONS['flameblade']['price']} and {WEAPONS['flameblade'].get('score_price', 0)} score")
        print(f"18. Thunder Sword (+150 ATK) - ${WEAPONS['thunder_sword']['price']} and {WEAPONS['thunder_sword'].get('score_price', 0)} score")
        print(f"19. Holy Avenger (+180 ATK) - ${WEAPONS['holy_avenger']['price']} and {WEAPONS['holy_avenger'].get('score_price', 0)} score")
        print(f"20. Dragon Slayer (+250 ATK) - ${WEAPONS['dragon_slayer']['price']} and {WEAPONS['dragon_slayer'].get('score_price', 0)} score")
        print(f"21. Cosmic Blade (+500 ATK) - ${WEAPONS['cosmic_blade']['price']} and {WEAPONS['cosmic_blade'].get('score_price', 0)} score")
        print(f"22. Transcendent Edge (+1500 ATK) - ${WEAPONS['transcendent_edge']['price']} and {WEAPONS['transcendent_edge'].get('score_price', 0)} score")
        print('\n----- Armors -----')
        print(f"23. Leather Armor (+1 DEF) - ${ARMORS['leather_armor']['price']}")
        print(f"24. Chainmail (+3 DEF) - ${ARMORS['chainmail']['price']}")
        print(f"25. Plate Armor (+6 DEF) - ${ARMORS['plate_armor']['price']}")
        print(f"26. Diamond Armor (+25 DEF) - ${ARMORS['diamond_armor']['price']}")
        print(f"27. Void Armor (+75 DEF) - ${ARMORS['void_armor']['price']}")
        print(f"28. Infinitium Armor (+300 DEF) - ${ARMORS['infinitium_armor']['price']} and {ARMORS['infinitium_armor'].get('score_price', 0)} score")
        print(f"29. Frost Armor (+40 DEF) - ${ARMORS['frost_armor']['price']} and {ARMORS['frost_armor'].get('score_price', 0)} score")
        print(f"30. Flame Armor (+45 DEF) - ${ARMORS['flame_armor']['price']} and {ARMORS['flame_armor'].get('score_price', 0)} score")
        print(f"31. Thunder Armor (+55 DEF) - ${ARMORS['thunder_armor']['price']} and {ARMORS['thunder_armor'].get('score_price', 0)} score")
        print(f"32. Holy Armor (+70 DEF) - ${ARMORS['holy_armor']['price']} and {ARMORS['holy_armor'].get('score_price', 0)} score")
        print(f"33. Dragon Scale Armor (+100 DEF) - ${ARMORS['dragon_scale_armor']['price']} and {ARMORS['dragon_scale_armor'].get('score_price', 0)} score")
        print(f"34. Cosmic Armor (+200 DEF) - ${ARMORS['cosmic_armor']['price']} and {ARMORS['cosmic_armor'].get('score_price', 0)} score")
        print(f"35. Transcendent Armor (+500 DEF) - ${ARMORS['transcendent_armor']['price']} and {ARMORS['transcendent_armor'].get('score_price', 0)} score")
        print('\n----- Wands (mana weapons) -----')
        print(f"36. Apprentice Wand (+5 magic) - ${WANDS['apprentice_wand']['price']}")
        print(f"37. Mage Wand (+20 magic) - ${WANDS['mage_wand']['price']}")
        print(f"38. Archmage Staff (+120 magic) - ${WANDS['archmage_staff']['price']} and {WANDS['archmage_staff'].get('score_price', 0)} score")
        print(f"39. Frost Wand (+60 magic) - ${WANDS['frost_wand']['price']} and {WANDS['frost_wand'].get('score_price', 0)} score")
        print(f"40. Flame Wand (+65 magic) - ${WANDS['flame_wand']['price']} and {WANDS['flame_wand'].get('score_price', 0)} score")
        print(f"41. Thunder Wand (+75 magic) - ${WANDS['thunder_wand']['price']} and {WANDS['thunder_wand'].get('score_price', 0)} score")
        print(f"42. Holy Scepter (+90 magic) - ${WANDS['holy_scepter']['price']} and {WANDS['holy_scepter'].get('score_price', 0)} score")
        print(f"43. Dragon Staff (+125 magic) - ${WANDS['dragon_staff']['price']} and {WANDS['dragon_staff'].get('score_price', 0)} score")
        print(f"44. Cosmic Scepter (+250 magic) - ${WANDS['cosmic_scepter']['price']} and {WANDS['cosmic_scepter'].get('score_price', 0)} score")
        print(f"45. Transcendent Staff (+750 magic) - ${WANDS['transcendent_staff']['price']} and {WANDS['transcendent_staff'].get('score_price', 0)} score")
        print('\n----- Robes -----')
        print(f"46. Cloth Robe (+2 magic def) - ${ROBES['cloth_robe']['price']}")
        print(f"47. Silk Robe (+10 magic def) - ${ROBES['silk_robe']['price']}")
        print(f"48. Void Robe (+80 magic def) - ${ROBES['void_robe']['price']} and {ROBES['void_robe'].get('score_price', 0)} score")
        print(f"49. Frost Robe (+30 magic def) - ${ROBES['frost_robe']['price']} and {ROBES['frost_robe'].get('score_price', 0)} score")
        print(f"50. Flame Robe (+35 magic def) - ${ROBES['flame_robe']['price']} and {ROBES['flame_robe'].get('score_price', 0)} score")
        print(f"51. Thunder Robe (+45 magic def) - ${ROBES['thunder_robe']['price']} and {ROBES['thunder_robe'].get('score_price', 0)} score")
        print(f"52. Holy Robe (+60 magic def) - ${ROBES['holy_robe']['price']} and {ROBES['holy_robe'].get('score_price', 0)} score")
        print(f"53. Dragon Robe (+90 magic def) - ${ROBES['dragon_robe']['price']} and {ROBES['dragon_robe'].get('score_price', 0)} score")
        print(f"54. Cosmic Robe (+180 magic def) - ${ROBES['cosmic_robe']['price']} and {ROBES['cosmic_robe'].get('score_price', 0)} score")
        print(f"55. Transcendent Robe (+450 magic def) - ${ROBES['transcendent_robe']['price']} and {ROBES['transcendent_robe'].get('score_price', 0)} score")
        print('\n----- Necklaces -----')
        print(f"56. Health Amulet (+20 HP) - ${NECKLACES['health_amulet']['price']}")
        print(f"57. Mana Amulet (+15 Mana) - ${NECKLACES['mana_amulet']['price']}")
        print(f"58. Strength Amulet (+5 ATK) - ${NECKLACES['strength_amulet']['price']}")
        print(f"59. Defense Amulet (+3 DEF) - ${NECKLACES['defense_amulet']['price']}")
        print(f"60. Critical Amulet (+10% Crit) - ${NECKLACES['crit_amulet']['price']}")
        print(f"61. Lifesteal Amulet (+5% Lifesteal) - ${NECKLACES['lifesteal_amulet']['price']}")
        print(f"62. Frost Necklace (+15 Magic Def, +30 HP) - ${NECKLACES['frost_necklace']['price']} and {NECKLACES['frost_necklace'].get('score_price', 0)} score")
        print(f"63. Flame Necklace (+10 Magic Atk, +8 ATK) - ${NECKLACES['flame_necklace']['price']} and {NECKLACES['flame_necklace'].get('score_price', 0)} score")
        print(f"64. Thunder Necklace (+15% Crit, +10 ATK) - ${NECKLACES['thunder_necklace']['price']} and {NECKLACES['thunder_necklace'].get('score_price', 0)} score")
        print(f"65. Holy Pendant (+50 HP, +30 Mana, +5 DEF) - ${NECKLACES['holy_pendant']['price']} and {NECKLACES['holy_pendant'].get('score_price', 0)} score")
        print(f"66. Dragon Necklace (+20 ATK, +15 DEF, +70 HP) - ${NECKLACES['dragon_necklace']['price']} and {NECKLACES['dragon_necklace'].get('score_price', 0)} score")
        print(f"67. Cosmic Necklace (+30 Magic Atk, +25 Magic Def, +50 Mana) - ${NECKLACES['cosmic_necklace']['price']} and {NECKLACES['cosmic_necklace'].get('score_price', 0)} score")
        print(f"68. Transcendent Necklace (+50 ATK, +40 DEF, +150 HP, +100 Mana, +20% Crit, +10% Lifesteal) - ${NECKLACES['transcendent_necklace']['price']} and {NECKLACES['transcendent_necklace'].get('score_price', 0)} score")
        print('\n----- Other Actions -----')
        print('69. Equip item from inventory')
        print('70. Unequip item')
        print('71. Sell Potion (sell 1 potion for $10)')
        print('72. Craft Items')
        print('73. View dungeon treasure')
        print('74. Exit shop')
        choice = input('\nChoose an option (e.g., 1 or 1 5 for quantity 5): ').strip().lower()
        parts = choice.split()
        opt = parts[0]
        qty = int(parts[1]) if len(parts) > 1 else 1
        if qty < 1:
            qty = 1
        if opt in ('exit', '74'):
            break
        item_name = None
        item_dict = None
        cost = 0
        score_cost = 0
        is_equipment = False
        if opt == '1':
            item_name = 'potion'
            cost = 20
        elif opt == '2':
            item_name = 'strong_potion'
            cost = 80
        elif opt == '3':
            item_name = 'ultra_potion'
            cost = 350
        elif opt == '4':
            item_name = 'mana_regen_potion'
            cost = 120
        elif opt == '5':
            item_name = 'instant_mana'
            cost = 60
        elif opt == '6':
            item_name = 'strength_boost'
            cost = 60
        elif opt == '7':
            item_name = 'defense_boost'
            cost = 60
        elif opt == '8':
            item_name = 'regen_potion'
            cost = 80
        elif opt == '9':
            item_name = 'crit_boost'
            cost = 80
        elif opt == '10':
            item_name = 'wooden_sword'
            item_dict = WEAPONS
            cost = WEAPONS['wooden_sword']['price']
            is_equipment = True
        elif opt == '11':
            item_name = 'iron_sword'
            item_dict = WEAPONS
            cost = WEAPONS['iron_sword']['price']
            is_equipment = True
        elif opt == '12':
            item_name = 'steel_sword'
            item_dict = WEAPONS
            cost = WEAPONS['steel_sword']['price']
            is_equipment = True
        elif opt == '13':
            item_name = 'diamond_sword'
            item_dict = WEAPONS
            cost = WEAPONS['diamond_sword']['price']
            is_equipment = True
        elif opt == '14':
            item_name = 'void_sword'
            item_dict = WEAPONS
            cost = WEAPONS['void_sword']['price']
            is_equipment = True
        elif opt == '15':
            item_name = 'infinitium_sword'
            item_dict = WEAPONS
            cost = WEAPONS['infinitium_sword']['price']
            score_cost = WEAPONS['infinitium_sword'].get('score_price', 0)
            is_equipment = True
        elif opt == '16':
            item_name = 'frostblade'
            item_dict = WEAPONS
            cost = WEAPONS['frostblade']['price']
            score_cost = WEAPONS['frostblade'].get('score_price', 0)
            is_equipment = True
        elif opt == '17':
            item_name = 'flameblade'
            item_dict = WEAPONS
            cost = WEAPONS['flameblade']['price']
            score_cost = WEAPONS['flameblade'].get('score_price', 0)
            is_equipment = True
        elif opt == '18':
            item_name = 'thunder_sword'
            item_dict = WEAPONS
            cost = WEAPONS['thunder_sword']['price']
            score_cost = WEAPONS['thunder_sword'].get('score_price', 0)
            is_equipment = True
        elif opt == '19':
            item_name = 'holy_avenger'
            item_dict = WEAPONS
            cost = WEAPONS['holy_avenger']['price']
            score_cost = WEAPONS['holy_avenger'].get('score_price', 0)
            is_equipment = True
        elif opt == '20':
            item_name = 'dragon_slayer'
            item_dict = WEAPONS
            cost = WEAPONS['dragon_slayer']['price']
            score_cost = WEAPONS['dragon_slayer'].get('score_price', 0)
            is_equipment = True
        elif opt == '21':
            item_name = 'cosmic_blade'
            item_dict = WEAPONS
            cost = WEAPONS['cosmic_blade']['price']
            score_cost = WEAPONS['cosmic_blade'].get('score_price', 0)
            is_equipment = True
        elif opt == '22':
            item_name = 'transcendent_edge'
            item_dict = WEAPONS
            cost = WEAPONS['transcendent_edge']['price']
            score_cost = WEAPONS['transcendent_edge'].get('score_price', 0)
            is_equipment = True
        elif opt == '23':
            item_name = 'leather_armor'
            item_dict = ARMORS
            cost = ARMORS['leather_armor']['price']
            is_equipment = True
        elif opt == '24':
            item_name = 'chainmail'
            item_dict = ARMORS
            cost = ARMORS['chainmail']['price']
            is_equipment = True
        elif opt == '25':
            item_name = 'plate_armor'
            item_dict = ARMORS
            cost = ARMORS['plate_armor']['price']
            is_equipment = True
        elif opt == '26':
            item_name = 'diamond_armor'
            item_dict = ARMORS
            cost = ARMORS['diamond_armor']['price']
            is_equipment = True
        elif opt == '27':
            item_name = 'void_armor'
            item_dict = ARMORS
            cost = ARMORS['void_armor']['price']
            is_equipment = True
        elif opt == '28':
            item_name = 'infinitium_armor'
            item_dict = ARMORS
            cost = ARMORS['infinitium_armor']['price']
            score_cost = ARMORS['infinitium_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '29':
            item_name = 'frost_armor'
            item_dict = ARMORS
            cost = ARMORS['frost_armor']['price']
            score_cost = ARMORS['frost_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '30':
            item_name = 'flame_armor'
            item_dict = ARMORS
            cost = ARMORS['flame_armor']['price']
            score_cost = ARMORS['flame_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '31':
            item_name = 'thunder_armor'
            item_dict = ARMORS
            cost = ARMORS['thunder_armor']['price']
            score_cost = ARMORS['thunder_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '32':
            item_name = 'holy_armor'
            item_dict = ARMORS
            cost = ARMORS['holy_armor']['price']
            score_cost = ARMORS['holy_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '33':
            item_name = 'dragon_scale_armor'
            item_dict = ARMORS
            cost = ARMORS['dragon_scale_armor']['price']
            score_cost = ARMORS['dragon_scale_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '34':
            item_name = 'cosmic_armor'
            item_dict = ARMORS
            cost = ARMORS['cosmic_armor']['price']
            score_cost = ARMORS['cosmic_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '35':
            item_name = 'transcendent_armor'
            item_dict = ARMORS
            cost = ARMORS['transcendent_armor']['price']
            score_cost = ARMORS['transcendent_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '36':
            item_name = 'apprentice_wand'
            item_dict = WANDS
            cost = WANDS['apprentice_wand']['price']
            is_equipment = True
        elif opt == '37':
            item_name = 'mage_wand'
            item_dict = WANDS
            cost = WANDS['mage_wand']['price']
            is_equipment = True
        elif opt == '38':
            item_name = 'archmage_staff'
            item_dict = WANDS
            cost = WANDS['archmage_staff']['price']
            score_cost = WANDS['archmage_staff'].get('score_price', 0)
            is_equipment = True
        elif opt == '39':
            item_name = 'frost_wand'
            item_dict = WANDS
            cost = WANDS['frost_wand']['price']
            score_cost = WANDS['frost_wand'].get('score_price', 0)
            is_equipment = True
        elif opt == '40':
            item_name = 'flame_wand'
            item_dict = WANDS
            cost = WANDS['flame_wand']['price']
            score_cost = WANDS['flame_wand'].get('score_price', 0)
            is_equipment = True
        elif opt == '41':
            item_name = 'thunder_wand'
            item_dict = WANDS
            cost = WANDS['thunder_wand']['price']
            score_cost = WANDS['thunder_wand'].get('score_price', 0)
            is_equipment = True
        elif opt == '42':
            item_name = 'holy_scepter'
            item_dict = WANDS
            cost = WANDS['holy_scepter']['price']
            score_cost = WANDS['holy_scepter'].get('score_price', 0)
            is_equipment = True
        elif opt == '43':
            item_name = 'dragon_staff'
            item_dict = WANDS
            cost = WANDS['dragon_staff']['price']
            score_cost = WANDS['dragon_staff'].get('score_price', 0)
            is_equipment = True
        elif opt == '44':
            item_name = 'cosmic_scepter'
            item_dict = WANDS
            cost = WANDS['cosmic_scepter']['price']
            score_cost = WANDS['cosmic_scepter'].get('score_price', 0)
            is_equipment = True
        elif opt == '45':
            item_name = 'transcendent_staff'
            item_dict = WANDS
            cost = WANDS['transcendent_staff']['price']
            score_cost = WANDS['transcendent_staff'].get('score_price', 0)
            is_equipment = True
        elif opt == '46':
            item_name = 'cloth_robe'
            item_dict = ROBES
            cost = ROBES['cloth_robe']['price']
            is_equipment = True
        elif opt == '47':
            item_name = 'silk_robe'
            item_dict = ROBES
            cost = ROBES['silk_robe']['price']
            is_equipment = True
        elif opt == '48':
            item_name = 'void_robe'
            item_dict = ROBES
            cost = ROBES['void_robe']['price']
            score_cost = ROBES['void_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '49':
            item_name = 'frost_robe'
            item_dict = ROBES
            cost = ROBES['frost_robe']['price']
            score_cost = ROBES['frost_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '50':
            item_name = 'flame_robe'
            item_dict = ROBES
            cost = ROBES['flame_robe']['price']
            score_cost = ROBES['flame_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '51':
            item_name = 'thunder_robe'
            item_dict = ROBES
            cost = ROBES['thunder_robe']['price']
            score_cost = ROBES['thunder_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '52':
            item_name = 'holy_robe'
            item_dict = ROBES
            cost = ROBES['holy_robe']['price']
            score_cost = ROBES['holy_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '53':
            item_name = 'dragon_robe'
            item_dict = ROBES
            cost = ROBES['dragon_robe']['price']
            score_cost = ROBES['dragon_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '54':
            item_name = 'cosmic_robe'
            item_dict = ROBES
            cost = ROBES['cosmic_robe']['price']
            score_cost = ROBES['cosmic_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '55':
            item_name = 'transcendent_robe'
            item_dict = ROBES
            cost = ROBES['transcendent_robe']['price']
            score_cost = ROBES['transcendent_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '56':
            item_name = 'health_amulet'
            item_dict = NECKLACES
            cost = NECKLACES['health_amulet']['price']
            is_equipment = True
        elif opt == '57':
            item_name = 'mana_amulet'
            item_dict = NECKLACES
            cost = NECKLACES['mana_amulet']['price']
            is_equipment = True
        elif opt == '58':
            item_name = 'strength_amulet'
            item_dict = NECKLACES
            cost = NECKLACES['strength_amulet']['price']
            is_equipment = True
        elif opt == '59':
            item_name = 'defense_amulet'
            item_dict = NECKLACES
            cost = NECKLACES['defense_amulet']['price']
            is_equipment = True
        elif opt == '60':
            item_name = 'crit_amulet'
            item_dict = NECKLACES
            cost = NECKLACES['crit_amulet']['price']
            is_equipment = True
        elif opt == '61':
            item_name = 'lifesteal_amulet'
            item_dict = NECKLACES
            cost = NECKLACES['lifesteal_amulet']['price']
            is_equipment = True
        elif opt == '62':
            item_name = 'frost_necklace'
            item_dict = NECKLACES
            cost = NECKLACES['frost_necklace']['price']
            score_cost = NECKLACES['frost_necklace'].get('score_price', 0)
            is_equipment = True
        elif opt == '63':
            item_name = 'flame_necklace'
            item_dict = NECKLACES
            cost = NECKLACES['flame_necklace']['price']
            score_cost = NECKLACES['flame_necklace'].get('score_price', 0)
            is_equipment = True
        elif opt == '64':
            item_name = 'thunder_necklace'
            item_dict = NECKLACES
            cost = NECKLACES['thunder_necklace']['price']
            score_cost = NECKLACES['thunder_necklace'].get('score_price', 0)
            is_equipment = True
        elif opt == '65':
            item_name = 'holy_pendant'
            item_dict = NECKLACES
            cost = NECKLACES['holy_pendant']['price']
            score_cost = NECKLACES['holy_pendant'].get('score_price', 0)
            is_equipment = True
        elif opt == '66':
            item_name = 'dragon_necklace'
            item_dict = NECKLACES
            cost = NECKLACES['dragon_necklace']['price']
            score_cost = NECKLACES['dragon_necklace'].get('score_price', 0)
            is_equipment = True
        elif opt == '67':
            item_name = 'cosmic_necklace'
            item_dict = NECKLACES
            cost = NECKLACES['cosmic_necklace']['price']
            score_cost = NECKLACES['cosmic_necklace'].get('score_price', 0)
            is_equipment = True
        elif opt == '68':
            item_name = 'transcendent_necklace'
            item_dict = NECKLACES
            cost = NECKLACES['transcendent_necklace']['price']
            score_cost = NECKLACES['transcendent_necklace'].get('score_price', 0)
            is_equipment = True
        elif opt == '69':
            manage_inventory_menu(current_user, player_data, None)
            user_data = load_user_data(current_user)
            if user_data:
                player_data = user_data.get('player_data', {})
                inventory = player_data.get('inventory', {})
                money = user_data.get('money', 40)
            continue
        elif opt == '70':
            print('Unequip which item? (weapon/armor/wand/robe/necklace)')
            item_type = input('Item type: ').strip().lower()
            stats = player_data['stats']
            equipped = stats.get('equipped', {})
            if item_type in ['weapon', 'armor', 'wand', 'robe', 'necklace']:
                equipped[item_type] = None
                player_data['stats'] = stats
                user_data['player_data'] = player_data
                save_user_data(current_user, user_data)
                print(f'Unequipped {item_type}.')
                continue
            else:
                print('Invalid item type.')
                continue
        elif opt == '71':
            if inventory.get('potion', 0) > 0:
                inventory['potion'] -= 1
                money += 10
                player_data['inventory'] = inventory
                user_data['money'] = money
                user_data['player_data'] = player_data
                save_user_data(current_user, user_data)
                print('Sold 1 potion for $10.')
            else:
                print('No potions to sell.')
            continue
        elif opt == '72':
            crafting_interface(current_user)
            continue
        elif opt == '73':
            global dungeon_treasure
            print(f"Current dungeon treasure money: ${dungeon_treasure['money']}")
            if dungeon_treasure['items']:
                print('Items in dungeon treasure:')
                item_counts = {}
                for item in dungeon_treasure['items']:
                    item_counts[item] = item_counts.get(item, 0) + 1
                for item, count in item_counts.items():
                    print(f'  {item}: {count}')
            else:
                print('No items in dungeon treasure.')
            continue
        else:
            print('Invalid choice.')
            continue
        if item_name:
            if money >= cost and score >= score_cost:
                if is_equipment:
                    if inventory.get(item_name, 0) > 0:
                        print('You already own this item.')
                    else:
                        inventory[item_name] = inventory.get(item_name, 0) + 1
                        money -= cost
                        score -= score_cost
                        player_data['inventory'] = inventory
                        user_data['money'] = money
                        user_data['score'] = score
                        user_data['player_data'] = player_data
                        save_user_data(current_user, user_data)
                        print(f'Purchased {item_name} for ${cost}' + (f' and {score_cost} score' if score_cost > 0 else '') + '!')
                else:
                    total_cost = cost * qty
                    if money >= total_cost:
                        inventory[item_name] = inventory.get(item_name, 0) + qty
                        money -= total_cost
                        player_data['inventory'] = inventory
                        user_data['money'] = money
                        user_data['player_data'] = player_data
                        save_user_data(current_user, user_data)
                        print(f'Purchased {qty}x {item_name} for ${total_cost}!')
                    else:
                        print('Not enough money.')
            else:
                print('Not enough money or score.')

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
        if 'atk_increase' in PERM_UPGRADES[up_key]:
            stats['perm_atk'] = stats.get('perm_atk', 0) + PERM_UPGRADES[up_key]['atk_increase']
        elif 'def_increase' in PERM_UPGRADES[up_key]:
            stats['perm_def'] = stats.get('perm_def', 0) + PERM_UPGRADES[up_key]['def_increase']
        elif 'hp_increase' in PERM_UPGRADES[up_key]:
            stats['perm_hp_max'] = stats.get('perm_hp_max', 0) + PERM_UPGRADES[up_key]['hp_increase']
        elif 'magic_increase' in PERM_UPGRADES[up_key]:
            stats['perm_mana_max'] = stats.get('perm_mana_max', 0) + PERM_UPGRADES[up_key]['magic_increase']
        elif 'crit_chance_increase' in PERM_UPGRADES[up_key]:
            stats['perm_crit_chance'] = stats.get('perm_crit_chance', 0) + PERM_UPGRADES[up_key]['crit_chance_increase']
        elif 'mana_regen_increase' in PERM_UPGRADES[up_key]:
            stats['perm_mana_regen'] = stats.get('perm_mana_regen', 0) + PERM_UPGRADES[up_key]['mana_regen_increase']
        elif 'max_lifesteal_increase' in PERM_UPGRADES[up_key]:
            stats['perm_lifesteal'] = stats.get('perm_lifesteal', 0) + PERM_UPGRADES[up_key]['max_lifesteal_increase']
        elif 'lifesteal_chance_increase' in PERM_UPGRADES[up_key]:
            stats['perm_lifesteal_chance'] = stats.get('perm_lifesteal_chance', 0) + PERM_UPGRADES[up_key]['lifesteal_chance_increase']
        elif 'exp_increase' in PERM_UPGRADES[up_key]:
            old_boost = stats.get('perm_exp_boost', 0)
            stats['perm_exp_boost'] = old_boost + PERM_UPGRADES[up_key]['exp_increase']
    while True:
        print('\n--- Permanent Upgrades ---')
        print('Available upgrades (use permanent upgrade items from inventory):')
        for key, upgrade in PERM_UPGRADES.items():
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
            for up_key in PERM_UPGRADES:
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
        elif opt in PERM_UPGRADES and inventory.get(opt, 0) >= qty:
            inventory[opt] -= qty
            for _ in range(qty):
                apply_single_upgrade(stats, opt)
            player_data['inventory'] = inventory
            player_data['stats'] = stats
            user_data['player_data'] = player_data
            save_user_data(username, user_data)
            check_achievements(username)
            print(f"Used {qty}x {PERM_UPGRADES[opt]['name']}!")
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
        for pack_key, pack in MAGIC_PACKS.items():
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
                qty = inventory.get(pack_alias, 0) if pack_alias in MAGIC_PACKS else 0
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
        if pack_alias in MAGIC_PACK_ALIASES:
            pack_alias = MAGIC_PACK_ALIASES[pack_alias]
        if pack_alias == 'all':
            total_opened = 0
            for p_key in MAGIC_PACKS:
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
        elif pack_alias in MAGIC_PACKS and inventory.get(pack_alias, 0) >= qty:
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
        for recipe_key, recipe in RECIPES.items():
            can_craft = True
            materials_needed = recipe['materials']
            for mat, qty in materials_needed.items():
                if inventory.get(mat, 0) < qty:
                    can_craft = False
                    break
            status = '✓' if can_craft else '✗'
            result_item = recipe['result']
            result_name = 'Unknown'
            if result_item in POTIONS:
                result_name = POTIONS[result_item]['name']
            elif result_item in PERM_UPGRADES:
                result_name = PERM_UPGRADES[result_item]['name']
            elif result_item in CRAFTABLE_WEAPONS:
                result_name = CRAFTABLE_WEAPONS[result_item]['name']
            elif result_item in CRAFTABLE_WANDS:
                result_name = CRAFTABLE_WANDS[result_item]['name']
            elif result_item in CRAFTABLE_NECKLACES:
                result_name = CRAFTABLE_NECKLACES[result_item]['name']
            elif result_item in CRAFTABLE_ROBES:
                result_name = CRAFTABLE_ROBES[result_item]['name']
            elif result_item in CRAFTABLE_ARMORS:
                result_name = CRAFTABLE_ARMORS[result_item]['name']
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
                    recipe = RECIPES[recipe_key]
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
    if pack_key not in MAGIC_PACKS:
        return (False, 'Unknown magic pack.')
    user_data = users[username]
    player_data = user_data.get('player_data', {})
    inventory = player_data.get('inventory', {})
    stats = player_data.get('stats', {})
    if inventory.get(pack_key, 0) < quantity:
        return (False, f"You don't have enough {MAGIC_PACKS[pack_key]['name']}.")
    pack = MAGIC_PACKS[pack_key]
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
                new_spells.append(SPELLS_BY_KEY[spell_key]['name'])
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
            print(f"{i + 1}. Slot {i + 1}: {(TITLES.get(title, {}).get('name', 'None') if title else 'None')}")
        print('\nAvailable Titles:')
        for i, title_key in enumerate(available_titles, start=1):
            title_name = TITLES.get(title_key, {}).get('name', title_key)
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
                    print(f"Equipped {TITLES[title_key]['name']} in slot {slot + 1}.")
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
            if title_id and title_id in TITLES:
                title = TITLES[title_id]
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
        heal_spells = [s for s in learned_spells if SPELLS_BY_KEY.get(s, {}).get('type') == 'heal']
        non_heal_spells = [s for s in learned_spells if SPELLS_BY_KEY.get(s, {}).get('type') != 'heal']
        heal_spells_sorted = sorted(heal_spells, key=lambda s: SPELLS_BY_KEY.get(s, {}).get('lvl', 0), reverse=True)
        non_heal_sorted = sorted(non_heal_spells, key=lambda s: SPELLS_BY_KEY.get(s, {}).get('lvl', 0), reverse=True)
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
            if count > 0 and weapon_id in WEAPONS:
                weapon_atk = WEAPONS[weapon_id]['atk']
                if weapon_atk > best_weapon_atk:
                    best_weapon = weapon_id
                    best_weapon_atk = weapon_atk
        if best_weapon and best_weapon != equipped['weapon']:
            equipped['weapon'] = best_weapon
        best_armor = None
        best_armor_def = 0
        for armor_id, count in inventory.items():
            if count > 0 and armor_id in ARMORS:
                armor_def = ARMORS[armor_id]['def']
                if armor_def > best_armor_def:
                    best_armor = armor_id
                    best_armor_def = armor_def
        if best_armor and best_armor != equipped['armor']:
            equipped['armor'] = best_armor
        if stats['settings'].get('auto_equip_everything', False):
            best_wand = None
            best_wand_magic_atk = 0
            for wand_id, count in inventory.items():
                if count > 0 and wand_id in WANDS:
                    wand_magic_atk = WANDS[wand_id]['magic_atk']
                    if wand_magic_atk > best_wand_magic_atk:
                        best_wand = wand_id
                        best_wand_magic_atk = wand_magic_atk
            if best_wand and best_wand != equipped['wand']:
                equipped['wand'] = best_wand
            best_robe = None
            best_robe_magic_def = 0
            for robe_id, count in inventory.items():
                if count > 0 and robe_id in ROBES:
                    robe_magic_def = ROBES[robe_id]['magic_def']
                    if robe_magic_def > best_robe_magic_def:
                        best_robe = robe_id
                        best_robe_magic_def = robe_magic_def
            if best_robe and best_robe != equipped['robe']:
                equipped['robe'] = best_robe
            best_necklace = None
            best_necklace_value = 0
            for necklace_id, count in inventory.items():
                if count > 0 and necklace_id in NECKLACES:
                    necklace = NECKLACES[necklace_id]
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
        print(f"  Weapon: {(WEAPONS.get(weapon, {}).get('name', 'None') if weapon else 'None')}")
        armor = equipped.get('armor')
        print(f"  Armor: {(ARMORS.get(armor, {}).get('name', 'None') if armor else 'None')}")
        wand = equipped.get('wand')
        print(f"  Wand: {(WANDS.get(wand, {}).get('name', 'None') if wand else 'None')}")
        robe = equipped.get('robe')
        print(f"  Robe: {(ROBES.get(robe, {}).get('name', 'None') if robe else 'None')}")
        necklace = equipped.get('necklace')
        print(f"  Necklace: {(NECKLACES.get(necklace, {}).get('name', 'None') if necklace else 'None')}")
        print('\nInventory:')
        item_list = []
        for key, count in inventory.items():
            if count > 0:
                name = 'Unknown'
                if key in WEAPONS:
                    name = WEAPONS[key]['name']
                elif key in ARMORS:
                    name = ARMORS[key]['name']
                elif key in WANDS:
                    name = WANDS[key]['name']
                elif key in ROBES:
                    name = ROBES[key]['name']
                elif key in NECKLACES:
                    name = NECKLACES[key]['name']
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
                if count > 0 and weapon_id in WEAPONS:
                    weapon_atk = WEAPONS[weapon_id]['atk']
                    if weapon_atk > best_weapon_atk:
                        best_weapon = weapon_id
                        best_weapon_atk = weapon_atk
            if best_weapon:
                equipped['weapon'] = best_weapon
                print(f'Equipped best weapon: {WEAPONS[best_weapon]["name"]}')
            else:
                print('No weapons to equip.')
        elif choice == 'a':
            best_armor = None
            best_armor_def = 0
            for armor_id, count in inventory.items():
                if count > 0 and armor_id in ARMORS:
                    armor_def = ARMORS[armor_id]['def']
                    if armor_def > best_armor_def:
                        best_armor = armor_id
                        best_armor_def = armor_def
            if best_armor:
                equipped['armor'] = best_armor
                print(f'Equipped best armor: {ARMORS[best_armor]["name"]}')
            else:
                print('No armors to equip.')
        elif choice == 'm':
            best_wand = None
            best_wand_magic_atk = 0
            for wand_id, count in inventory.items():
                if count > 0 and wand_id in WANDS:
                    wand_magic_atk = WANDS[wand_id]['magic_atk']
                    if wand_magic_atk > best_wand_magic_atk:
                        best_wand = wand_id
                        best_wand_magic_atk = wand_magic_atk
            if best_wand:
                equipped['wand'] = best_wand
                print(f'Equipped best wand: {WANDS[best_wand]["name"]}')
            else:
                print('No wands to equip.')
        elif choice == 'r':
            best_robe = None
            best_robe_magic_def = 0
            for robe_id, count in inventory.items():
                if count > 0 and robe_id in ROBES:
                    robe_magic_def = ROBES[robe_id]['magic_def']
                    if robe_magic_def > best_robe_magic_def:
                        best_robe = robe_id
                        best_robe_magic_def = robe_magic_def
            if best_robe:
                equipped['robe'] = best_robe
                print(f'Equipped best robe: {ROBES[best_robe]["name"]}')
            else:
                print('No robes to equip.')
        elif choice == 'n':
            best_necklace = None
            best_necklace_value = 0
            for necklace_id, count in inventory.items():
                if count > 0 and necklace_id in NECKLACES:
                    necklace = NECKLACES[necklace_id]
                    total_value = necklace.get('hp_bonus', 0) * 1 + necklace.get('mana_bonus', 0) * 1 + necklace.get('atk_bonus', 0) * 2 + necklace.get('def_bonus', 0) * 2 + necklace.get('magic_atk_bonus', 0) * 2 + necklace.get('magic_def_bonus', 0) * 2 + necklace.get('crit_bonus', 0) * 3 + necklace.get('lifesteal_bonus', 0) * 3
                    if total_value > best_necklace_value:
                        best_necklace = necklace_id
                        best_necklace_value = total_value
            if best_necklace:
                equipped['necklace'] = best_necklace
                print(f'Equipped best necklace: {NECKLACES[best_necklace]["name"]}')
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
                if item_key in WEAPONS:
                    equipped['weapon'] = item_key
                    print(f'Equipped {item_name} as weapon.')
                elif item_key in ARMORS:
                    equipped['armor'] = item_key
                    print(f'Equipped {item_name} as armor.')
                elif item_key in WANDS:
                    equipped['wand'] = item_key
                    print(f'Equipped {item_name} as wand.')
                elif item_key in ROBES:
                    equipped['robe'] = item_key
                    print(f'Equipped {item_name} as robe.')
                elif item_key in NECKLACES:
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
    for ach_key, achievement in ACHIEVEMENTS.items():
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
    w_atk = WEAPONS.get(weapon, {}).get('atk', 0) if weapon else 0
    a_def = ARMORS.get(armor, {}).get('def', 0) if armor else 0
    wand_magic = WANDS.get(wand, {}).get('magic_atk', 0) if wand else 0
    robe_def = ROBES.get(robe, {}).get('magic_def', 0) if robe else 0
    n_atk = NECKLACES.get(necklace, {}).get('atk_bonus', 0) if necklace else 0
    n_def = NECKLACES.get(necklace, {}).get('def_bonus', 0) if necklace else 0
    n_hp = NECKLACES.get(necklace, {}).get('hp_bonus', 0) if necklace else 0
    n_mana = NECKLACES.get(necklace, {}).get('mana_bonus', 0) if necklace else 0
    n_crit = NECKLACES.get(necklace, {}).get('crit_bonus', 0) if necklace else 0
    n_lifesteal = NECKLACES.get(necklace, {}).get('lifesteal_bonus', 0) if necklace else 0
    n_magic_atk = NECKLACES.get(necklace, {}).get('magic_atk_bonus', 0) if necklace else 0
    n_magic_def = NECKLACES.get(necklace, {}).get('magic_def_bonus', 0) if necklace else 0
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
            if spell and spell in SPELLS_BY_KEY:
                s = SPELLS_BY_KEY[spell]
                print(f"{i + 1}. Slot {i + 1}: {s['name']} ({s['mana']} mana)")
            else:
                print(f'{i + 1}. Slot {i + 1}: None')
        print('\nLearned Spells:')
        for i, spell_key in enumerate(learned_spells, start=1):
            s = SPELLS_BY_KEY.get(spell_key, {})
            print(f"{i + 4}. {s.get('name', 'Unknown')} (lvl {s.get('lvl', '?')},{s.get('mana', '?')} mana) - {s.get('desc', '')}")
        print('\nQuick Equip:')
        print('b. Equip best spells automatically')
        print('0. Back')
        choice = input('Choose slot to equip/unequip, spell to equip, or "b" for auto-equip best: ').strip()
        if choice == '0':
            break
        elif choice == 'b':
            heal_spells = [s for s in learned_spells if SPELLS_BY_KEY.get(s, {}).get('type') == 'heal']
            non_heal_spells = [s for s in learned_spells if SPELLS_BY_KEY.get(s, {}).get('type') != 'heal']
            heal_spells_sorted = sorted(heal_spells, key=lambda s: SPELLS_BY_KEY.get(s, {}).get('lvl', 0), reverse=True)
            non_heal_sorted = sorted(non_heal_spells, key=lambda s: SPELLS_BY_KEY.get(s, {}).get('lvl', 0), reverse=True)
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
                s = SPELLS_BY_KEY.get(spell_key, {})
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