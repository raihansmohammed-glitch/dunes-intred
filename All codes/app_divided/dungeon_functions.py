import json
import random
import os
import math
import time
import threading
import misc
import atexit
import socket

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_DIR = os.path.join(SCRIPT_DIR, 'users.txt')
DUNGEON_TREASURE_FILE = os.path.join(SCRIPT_DIR, 'dungeon_treasure.json')
dungeon_treasure = {'money': 0, 'items': []}
GLOBAL_KEY = '__global__'
AUTOSAVE_INTERVAL = 30
autosave_timer = None
last_autosave_time = time.time()

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
        consumables = list(POTIONS.keys()) + list(misc.MAGIC_PACKS.keys()) + list(MATERIALS.keys())
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

def add_material_drops(inventory, monster):
    """Add material drops from a monster to the inventory and return list of dropped items"""
    dropped = []
    if 'drop' in monster:
        for item, chance in monster['drop'].items():
            if random.random() < chance:
                inventory[item] = inventory.get(item, 0) + 1
                dropped.append(item)
    return dropped

MONSTER_ALIASES = {
    'boss': {'gk': 'Goblin King', 'sk': 'Skeleton King', 'tc': 'Troll Chieftain', 'dl': 'Dark Lord', 'iq': 'Ice Queen', 'pl': 'Phoenix Lord', 'vm': 'Void Master', 'ce': 'Celestial Emperor', 'drl': 'Dragon Lord', 'gr': 'Grim Reaper', 'dk': 'Demon King Muzan'},
    'normal': {'sl': 'Slime', 'g': 'Goblin', 'w': 'Wolf', 'gs': 'Goblin Shaman', 'sf': 'Forest Sprite', 'skel': 'Skeleton', 'o': 'Orc', 'sp': 'Giant Spider', 'bt': 'Dark Bat', 'b': 'Bandit', 'ow': 'Orc Warrior', 'dm': 'Dark Mage', 'sg': 'Stone Golem', 't': 'Troll', 'ie': 'Ice Elemental', 'fe': 'Fire Elemental', 'tb': 'Thunder Bird', 'dk': 'Dark Knight', 'sa': 'Shadow Assassin', 'am': 'Arcane Mage', 'wl': 'Warlock', 'ig': 'Ice Giant', 'p': 'Phoenix', 'cg': 'Crystal Golem', 'sd': 'Storm Dragon', 'vw': 'Void Walker', 'cg2': 'Celestial Guardian', 'sw': 'Star Weaver', 'ms': 'Moon Sentinel', 'sc': 'Sun Champion', 'vl': 'Void Lord', 'dp': 'Divine Paladin', 'cm': 'Cosmic Mage', 'ed': 'Eternal Dragon', 'vr': 'Void Reaper', 'cp': 'Celestial Phoenix', 'ce2': 'Cosmic Entity', 'tb2': 'Transcendent Being', 've': 'Void Emperor', 'da': 'Divine Avatar', 'co': 'Cosmic Overlord'}
    }

MONSTERS = [
    {'name': 'Slime', 'hp': 8, 'atk_min': 1, 'atk_max': 3, 'money_min': 2, 'money_max': 7, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.25, 'slime_gel': 0.4},'weight': 18, 'area': 1, 'element': 'nature', 'exp_min': 10, 'exp_max': 25},
    {'name': 'Goblin', 'hp': 10, 'atk_min': 3, 'atk_max': 5, 'money_min': 4, 'money_max': 15, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.3, 'strength_boost': 0.05, 'goblin_tooth': 0.3},'weight': 15, 'area': 1, 'element': 'mana', 'exp_min': 10, 'exp_max': 25},
    {'name': 'Wolf', 'hp': 12, 'atk_min': 3, 'atk_max': 6, 'money_min': 10, 'money_max': 22, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'wolf_pelt': 0.3},'weight': 14, 'area': 1, 'element': 'nature', 'exp_min': 10, 'exp_max': 25},
    {'name': 'Goblin Shaman', 'hp': 20, 'magic_atk_min': 8, 'magic_atk_max': 12, 'money_min': 10, 'money_max': 25, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'mana_regen_potion': 0.1, 'goblin_tooth': 0.2},'weight': 8, 'area': 1, 'element': 'mana', 'exp_min': 10, 'exp_max': 25},
    {'name': 'Forest Sprite', 'hp': 15, 'atk_min': 2, 'atk_max': 5, 'money_min': 8, 'money_max': 20, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.25, 'mana_regen_potion': 0.1, 'crystal_shard': 0.2},'weight': 12, 'area': 1, 'element': 'nature', 'exp_min': 10, 'exp_max': 25},
    {'name': 'Skeleton', 'hp': 20, 'atk_min': 4, 'atk_max': 7, 'money_min': 15, 'money_max': 30, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.25, 'defense_boost': 0.05, 'skeleton_bone': 0.4},'weight': 12, 'area': 2, 'element': 'mana', 'exp_min': 15, 'exp_max': 37},
    {'name': 'Orc', 'hp': 30, 'atk_min': 5, 'atk_max': 8, 'money_min': 20, 'money_max': 40, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'orc_iron': 0.3},'weight': 10, 'area': 2, 'element': 'mana', 'exp_min': 15, 'exp_max': 37},
    {'name': 'Giant Spider', 'hp': 25, 'atk_min': 6, 'atk_max': 9, 'money_min': 25, 'money_max': 45, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'crit_boost': 0.05, 'spider_venom': 0.3},'weight': 8, 'area': 2, 'element': 'nature', 'exp_min': 15, 'exp_max': 37},
    {'name': 'Dark Bat', 'hp': 18, 'atk_min': 5, 'atk_max': 8, 'money_min': 18, 'money_max': 35, 'class': 'D(Common)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'bat_wing': 0.3},'weight': 10, 'area': 2, 'element': 'nature', 'exp_min': 15, 'exp_max': 37},
    {'name': 'Bandit', 'hp': 40, 'atk_min': 7, 'atk_max': 12, 'money_min': 35, 'money_max': 60, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.15, 'crit_boost': 0.04, 'common_magic_pack': 0.15, 'bandit_cloth': 0.3, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1},'weight': 10, 'area': 3, 'element': 'mana', 'exp_min': 22, 'exp_max': 56},
    {'name': 'Orc Warrior', 'hp': 55, 'atk_min': 8, 'atk_max': 13, 'money_min': 40, 'money_max': 70, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'orc_iron': 0.4, 'strength_boost': 0.1, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1},'weight': 8, 'area': 3, 'element': 'mana', 'exp_min': 22, 'exp_max': 56},
    {'name': 'Dark Mage', 'hp': 45, 'magic_atk_min': 10, 'magic_atk_max': 15, 'money_min': 50, 'money_max': 80, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.25, 'strength_boost': 0.06, 'common_magic_pack': 0.25, 'rare_magic_pack': 0.1, 'dark_essence': 0.2, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1},'weight': 7, 'area': 3, 'element': 'mana', 'exp_min': 22, 'exp_max': 56},
    {'name': 'Stone Golem', 'hp': 70, 'atk_min': 6, 'atk_max': 10, 'money_min': 45, 'money_max': 75, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'defense_boost': 0.1, 'stone_core': 0.3, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1},'weight': 6, 'area': 3, 'element': 'nature', 'exp_min': 22, 'exp_max': 56},
    {'name': 'Troll', 'hp': 90, 'atk_min': 12, 'atk_max': 18, 'money_min': 80, 'money_max': 120, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'regen_potion': 0.05, 'common_magic_pack': 0.1, 'rare_magic_pack': 0.05, 'troll_core': 0.3, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1},'weight': 6, 'area': 4, 'element': 'nature', 'exp_min': 33, 'exp_max': 84},
    {'name': 'Ice Elemental', 'hp': 75, 'magic_atk_min': 15, 'magic_atk_max': 20, 'money_min': 90, 'money_max': 130, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'frozen_heart': 0.3, 'ice_shard': 0.2, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1},'weight': 5, 'area': 4, 'element': 'ice', 'exp_min': 33, 'exp_max': 84},
    {'name': 'Fire Elemental', 'hp': 70, 'magic_atk_min': 16, 'magic_atk_max': 22, 'money_min': 85, 'money_max': 125, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'fire_essence': 0.3, 'ember': 0.2, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1},'weight': 5, 'area': 4, 'element': 'fire', 'exp_min': 33, 'exp_max': 84},
    {'name': 'Thunder Bird', 'hp': 65, 'magic_atk_min': 14, 'magic_atk_max': 21, 'money_min': 95, 'money_max': 140, 'class': 'C(Rare)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'thunder_core': 0.3, 'lightning_feather': 0.2, 'perm_exp_upgrade': 0.1, 'perm_strength_upgrade': 0.1, 'perm_defense_upgrade': 0.1, 'perm_health_upgrade': 0.1, 'perm_mana_upgrade': 0.1, 'perm_crit_chance_upgrade': 0.1, 'perm_mana_regen_upgrade': 0.1, 'perm_lifesteal_upgrade': 0.1, 'perm_lifesteal_chance_upgrade': 0.1},'weight': 5, 'area': 4, 'element': 'lightning', 'exp_min': 33, 'exp_max': 84},
    {'name': 'Dark Knight', 'hp': 120, 'atk_min': 18, 'atk_max': 25, 'money_min': 120, 'money_max': 180, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.15, 'defense_boost': 0.1, 'rare_magic_pack': 0.2, 'dark_essence': 0.3, 'perm_exp_upgrade': 0.12, 'perm_strength_upgrade': 0.12, 'perm_defense_upgrade': 0.12, 'perm_health_upgrade': 0.12, 'perm_mana_upgrade': 0.12, 'perm_crit_chance_upgrade': 0.12, 'perm_mana_regen_upgrade': 0.12, 'perm_lifesteal_upgrade': 0.12, 'perm_lifesteal_chance_upgrade': 0.12},'weight': 4, 'area': 5, 'element': 'mana', 'exp_min': 50, 'exp_max': 126},
    {'name': 'Shadow Assassin', 'hp': 100, 'atk_min': 20, 'atk_max': 28, 'money_min': 130, 'money_max': 190, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.15, 'crit_boost': 0.1, 'rare_magic_pack': 0.2, 'shadow_cloak': 0.2, 'perm_exp_upgrade': 0.12, 'perm_strength_upgrade': 0.12, 'perm_defense_upgrade': 0.12, 'perm_health_upgrade': 0.12, 'perm_mana_upgrade': 0.12, 'perm_crit_chance_upgrade': 0.12, 'perm_mana_regen_upgrade': 0.12, 'perm_lifesteal_upgrade': 0.12, 'perm_lifesteal_chance_upgrade': 0.12},'weight': 4, 'area': 5, 'element': 'mana', 'exp_min': 50, 'exp_max': 126},
    {'name': 'Arcane Mage', 'hp': 110, 'magic_atk_min': 22, 'magic_atk_max': 30, 'money_min': 140, 'money_max': 200, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'mana_upgrade_potion': 0.1, 'rare_magic_pack': 0.25, 'mythical_magic_pack': 0.1, 'arcane_tome': 0.2, 'perm_exp_upgrade': 0.12, 'perm_strength_upgrade': 0.12, 'perm_defense_upgrade': 0.12, 'perm_health_upgrade': 0.12, 'perm_mana_upgrade': 0.12, 'perm_crit_chance_upgrade': 0.12, 'perm_mana_regen_upgrade': 0.12, 'perm_lifesteal_upgrade': 0.12, 'perm_lifesteal_chance_upgrade': 0.12},'weight': 3, 'area': 5, 'element': 'mana', 'exp_min': 50, 'exp_max': 126},
    {'name': 'Warlock', 'hp': 105, 'atk_min': 21, 'atk_max': 29, 'money_min': 135, 'money_max': 195, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'curse_scroll': 0.2, 'rare_magic_pack': 0.2, 'mythical_magic_pack': 0.1, 'demon_horn': 0.2, 'perm_exp_upgrade': 0.12, 'perm_strength_upgrade': 0.12, 'perm_defense_upgrade': 0.12, 'perm_health_upgrade': 0.12, 'perm_mana_upgrade': 0.12, 'perm_crit_chance_upgrade': 0.12, 'perm_mana_regen_upgrade': 0.12, 'perm_lifesteal_upgrade': 0.12, 'perm_lifesteal_chance_upgrade': 0.12},'weight': 3, 'area': 5, 'element': 'mana', 'exp_min': 50, 'exp_max': 126},
    {'name': 'Ice Giant', 'hp': 150, 'atk_min': 25, 'atk_max': 35, 'money_min': 180, 'money_max': 250, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'frozen_heart': 0.4, 'mythical_magic_pack': 0.2, 'ice_shard': 0.3, 'perm_exp_upgrade': 0.14, 'perm_strength_upgrade': 0.14, 'perm_defense_upgrade': 0.14, 'perm_health_upgrade': 0.14, 'perm_mana_upgrade': 0.14, 'perm_crit_chance_upgrade': 0.14, 'perm_mana_regen_upgrade': 0.14, 'perm_lifesteal_upgrade': 0.14, 'perm_lifesteal_chance_upgrade': 0.14},'weight': 3, 'area': 6, 'element': 'ice', 'exp_min': 75, 'exp_max': 189},
    {'name': 'Phoenix', 'hp': 130, 'atk_min': 28, 'atk_max': 38, 'money_min': 200, 'money_max': 280, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'phoenix_feather': 0.3, 'mythical_magic_pack': 0.25, 'fire_essence': 0.3, 'perm_exp_upgrade': 0.14, 'perm_strength_upgrade': 0.14, 'perm_defense_upgrade': 0.14, 'perm_health_upgrade': 0.14, 'perm_mana_upgrade': 0.14, 'perm_crit_chance_upgrade': 0.14, 'perm_mana_regen_upgrade': 0.14, 'perm_lifesteal_upgrade': 0.14, 'perm_lifesteal_chance_upgrade': 0.14},'weight': 2, 'area': 6, 'element': 'fire', 'exp_min': 75, 'exp_max': 189},
    {'name': 'Crystal Golem', 'hp': 160, 'atk_min': 24, 'atk_max': 34, 'money_min': 190, 'money_max': 260, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'crystal_shard': 0.4, 'mythical_magic_pack': 0.2, 'stone_core': 0.3, 'perm_exp_upgrade': 0.14, 'perm_strength_upgrade': 0.14, 'perm_defense_upgrade': 0.14, 'perm_health_upgrade': 0.14, 'perm_mana_upgrade': 0.14, 'perm_crit_chance_upgrade': 0.14, 'perm_mana_regen_upgrade': 0.14, 'perm_lifesteal_upgrade': 0.14, 'perm_lifesteal_chance_upgrade': 0.14},'weight': 2, 'area': 6, 'element': 'nature', 'exp_min': 75, 'exp_max': 189},
    {'name': 'Storm Dragon', 'hp': 140, 'atk_min': 27, 'atk_max': 37, 'money_min': 210, 'money_max': 290, 'class': 'B(Mythical)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'thunder_core': 0.4, 'mythical_magic_pack': 0.25, 'dragon_scale': 0.2, 'perm_exp_upgrade': 0.14, 'perm_strength_upgrade': 0.14, 'perm_defense_upgrade': 0.14, 'perm_health_upgrade': 0.14, 'perm_mana_upgrade': 0.14, 'perm_crit_chance_upgrade': 0.14, 'perm_mana_regen_upgrade': 0.14, 'perm_lifesteal_upgrade': 0.14, 'perm_lifesteal_chance_upgrade': 0.14},'weight': 2, 'area': 6, 'element': 'lightning', 'exp_min': 75, 'exp_max': 189},
    {'name': 'Void Walker', 'hp': 180, 'magic_atk_min': 32, 'magic_atk_max': 42, 'money_min': 250, 'money_max': 350, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.15, 'void_fragment': 0.3, 'mythical_magic_pack': 0.2, 'prismatic_magic_pack': 0.1, 'perm_exp_upgrade': 0.16, 'perm_strength_upgrade': 0.16, 'perm_defense_upgrade': 0.16, 'perm_health_upgrade': 0.16, 'perm_mana_upgrade': 0.16, 'perm_crit_chance_upgrade': 0.16, 'perm_mana_regen_upgrade': 0.16, 'perm_lifesteal_upgrade': 0.16, 'perm_lifesteal_chance_upgrade': 0.16},'weight': 2, 'area': 7, 'element': 'mana', 'exp_min': 113, 'exp_max': 284},
    {'name': 'Celestial Guardian', 'hp': 200, 'atk_min': 30, 'atk_max': 40, 'money_min': 280, 'money_max': 380, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'holy_light': 0.3, 'mythical_magic_pack': 0.25, 'prismatic_magic_pack': 0.15, 'perm_exp_upgrade': 0.16, 'perm_strength_upgrade': 0.16, 'perm_defense_upgrade': 0.16, 'perm_health_upgrade': 0.16, 'perm_mana_upgrade': 0.16, 'perm_crit_chance_upgrade': 0.16, 'perm_mana_regen_upgrade': 0.16, 'perm_lifesteal_upgrade': 0.16, 'perm_lifesteal_chance_upgrade': 0.16},'weight': 2, 'area': 7, 'element': 'mana', 'exp_min': 113, 'exp_max': 284},
    {'name': 'Star Weaver', 'hp': 170, 'atk_min': 33, 'atk_max': 43, 'money_min': 260, 'money_max': 360, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'star_dust': 0.4, 'mythical_magic_pack': 0.2, 'prismatic_magic_pack': 0.1, 'perm_exp_upgrade': 0.16, 'perm_strength_upgrade': 0.16, 'perm_defense_upgrade': 0.16, 'perm_health_upgrade': 0.16, 'perm_mana_upgrade': 0.16, 'perm_crit_chance_upgrade': 0.16, 'perm_mana_regen_upgrade': 0.16, 'perm_lifesteal_upgrade': 0.16, 'perm_lifesteal_chance_upgrade': 0.16},'weight': 2, 'area': 7, 'element': 'mana', 'exp_min': 113, 'exp_max': 284},
    {'name': 'Moon Sentinel', 'hp': 190, 'atk_min': 31, 'atk_max': 41, 'money_min': 270, 'money_max': 370, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'moon_rock': 0.3, 'mythical_magic_pack': 0.2, 'prismatic_magic_pack': 0.15, 'perm_exp_upgrade': 0.16, 'perm_strength_upgrade': 0.16, 'perm_defense_upgrade': 0.16, 'perm_health_upgrade': 0.16, 'perm_mana_upgrade': 0.16, 'perm_crit_chance_upgrade': 0.16, 'perm_mana_regen_upgrade': 0.16, 'perm_lifesteal_upgrade': 0.16, 'perm_lifesteal_chance_upgrade': 0.16},'weight': 2, 'area': 7, 'element': 'mana', 'exp_min': 113, 'exp_max': 284},
    {'name': 'Sun Champion', 'hp': 220, 'atk_min': 36, 'atk_max': 46, 'money_min': 320, 'money_max': 420, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'sun_stone': 0.3, 'prismatic_magic_pack': 0.25, 'divine_magic_pack': 0.1, 'perm_exp_upgrade': 0.18, 'perm_strength_upgrade': 0.18, 'perm_defense_upgrade': 0.18, 'perm_health_upgrade': 0.18, 'perm_mana_upgrade': 0.18, 'perm_crit_chance_upgrade': 0.18, 'perm_mana_regen_upgrade': 0.18, 'perm_lifesteal_upgrade': 0.18, 'perm_lifesteal_chance_upgrade': 0.18},'weight': 1, 'area': 8, 'element': 'fire', 'exp_min': 170, 'exp_max': 427},
    {'name': 'Void Lord', 'hp': 240, 'magic_atk_min': 38, 'magic_atk_max': 48, 'money_min': 350, 'money_max': 450, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'void_fragment': 0.4, 'prismatic_magic_pack': 0.25, 'divine_magic_pack': 0.15, 'perm_exp_upgrade': 0.18, 'perm_strength_upgrade': 0.18, 'perm_defense_upgrade': 0.18, 'perm_health_upgrade': 0.18, 'perm_mana_upgrade': 0.18, 'perm_crit_chance_upgrade': 0.18, 'perm_mana_regen_upgrade': 0.18, 'perm_lifesteal_upgrade': 0.18, 'perm_lifesteal_chance_upgrade': 0.18},'weight': 1, 'area': 8, 'element': 'mana', 'exp_min': 170, 'exp_max': 427},
    {'name': 'Divine Paladin', 'hp': 210, 'atk_min': 37, 'atk_max': 47, 'money_min': 330, 'money_max': 430, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'holy_light': 0.4, 'prismatic_magic_pack': 0.3, 'divine_magic_pack': 0.15, 'perm_exp_upgrade': 0.18, 'perm_strength_upgrade': 0.18, 'perm_defense_upgrade': 0.18, 'perm_health_upgrade': 0.18, 'perm_mana_upgrade': 0.18, 'perm_crit_chance_upgrade': 0.18, 'perm_mana_regen_upgrade': 0.18, 'perm_lifesteal_upgrade': 0.18, 'perm_lifesteal_chance_upgrade': 0.18},'weight': 1, 'area': 8, 'element': 'mana', 'exp_min': 170, 'exp_max': 427},
    {'name': 'Cosmic Mage', 'hp': 230, 'magic_atk_min': 35, 'magic_atk_max': 45, 'money_min': 340, 'money_max': 440, 'class': 'A(Prismatic)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'star_dust': 0.3, 'prismatic_magic_pack': 0.25, 'divine_magic_pack': 0.2, 'perm_exp_upgrade': 0.18, 'perm_strength_upgrade': 0.18, 'perm_defense_upgrade': 0.18, 'perm_health_upgrade': 0.18, 'perm_mana_upgrade': 0.18, 'perm_crit_chance_upgrade': 0.18, 'perm_mana_regen_upgrade': 0.18, 'perm_lifesteal_upgrade': 0.18, 'perm_lifesteal_chance_upgrade': 0.18},'weight': 1, 'area': 8, 'element': 'mana', 'exp_min': 170, 'exp_max': 427},
    {'name': 'Eternal Dragon', 'hp': 300, 'atk_min': 42, 'atk_max': 54, 'money_min': 450, 'money_max': 600, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.15, 'dragon_scale': 0.4, 'divine_magic_pack': 0.3, 'transcendent_magic_pack': 0.1, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2},'weight': 1, 'area': 9, 'element': 'fire', 'exp_min': 256, 'exp_max': 640},
    {'name': 'Void Reaper', 'hp': 280, 'magic_atk_min': 45, 'magic_atk_max': 57, 'money_min': 480, 'money_max': 630, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'void_fragment': 0.4, 'divine_magic_pack': 0.3, 'transcendent_magic_pack': 0.15, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2},'weight': 1, 'area': 9, 'element': 'mana', 'exp_min': 256, 'exp_max': 640},
    {'name': 'Celestial Phoenix', 'hp': 290, 'atk_min': 43, 'atk_max': 55, 'money_min': 470, 'money_max': 620, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'phoenix_feather': 0.4, 'divine_magic_pack': 0.35, 'transcendent_magic_pack': 0.15, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2},'weight': 1, 'area': 9, 'element': 'fire', 'exp_min': 256, 'exp_max': 640},
    {'name': 'Cosmic Entity', 'hp': 310, 'magic_atk_min': 41, 'magic_atk_max': 53, 'money_min': 460, 'money_max': 610, 'class': 'S(Divine)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'star_dust': 0.4, 'divine_magic_pack': 0.3, 'transcendent_magic_pack': 0.2, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2},'weight': 1, 'area': 9, 'element': 'mana', 'exp_min': 256, 'exp_max': 640},
    {'name': 'Transcendent Being', 'hp': 400, 'atk_min': 50, 'atk_max': 65, 'money_min': 600, 'money_max': 800, 'class': 'SS(Transcendent)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'transcendent_heart': 0.2, 'divine_magic_pack': 0.3, 'transcendent_magic_pack': 0.3, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2},'weight': 1, 'area': 10, 'element': 'mana', 'exp_min': 384, 'exp_max': 961},
    {'name': 'Void Emperor', 'hp': 420, 'magic_atk_min': 52, 'magic_atk_max': 67, 'money_min': 650, 'money_max': 850, 'class': 'SS(Transcendent)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'void_fragment': 0.4, 'divine_magic_pack': 0.3, 'transcendent_magic_pack': 0.35, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2},'weight': 1, 'area': 10, 'element': 'mana', 'exp_min': 384, 'exp_max': 961},
    {'name': 'Divine Avatar', 'hp': 410, 'atk_min': 51, 'atk_max': 66, 'money_min': 630, 'money_max': 830, 'class': 'SS(Transcendent)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'holy_light': 0.4, 'divine_magic_pack': 0.35, 'transcendent_magic_pack': 0.3, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2},'weight': 1, 'area': 10, 'element': 'mana', 'exp_min': 384, 'exp_max': 961},
    {'name': 'Cosmic Overlord', 'hp': 430, 'atk_min': 53, 'atk_max': 68, 'money_min': 670, 'money_max': 870, 'class': 'SS(Transcendent)', 'is_boss': False, 'is_super_boss': False, 'drop': {'potion': 0.2, 'star_dust': 0.4, 'divine_magic_pack': 0.3, 'transcendent_magic_pack': 0.4, 'perm_exp_upgrade': 0.2, 'perm_strength_upgrade': 0.2, 'perm_defense_upgrade': 0.2, 'perm_health_upgrade': 0.2, 'perm_mana_upgrade': 0.2, 'perm_crit_chance_upgrade': 0.2, 'perm_mana_regen_upgrade': 0.2, 'perm_lifesteal_upgrade': 0.2, 'perm_lifesteal_chance_upgrade': 0.2},'weight': 1, 'area': 10, 'element': 'mana', 'exp_min': 384, 'exp_max': 961},
    {'name': 'Goblin King', 'hp': 200, 'atk_min': 50, 'atk_max': 100, 'money_min': 200, 'money_max': 400, 'class': 'D(Common)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.5, 'defense_boost': 0.3, 'goblin_tooth': 1.0, 'common_magic_pack': 0.5, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0},'weight': 1, 'area': 1, 'exp_min': 250, 'exp_max': 500},
    {'name': 'Skeleton King', 'hp': 500, 'atk_min': 110, 'atk_max': 175, 'money_min': 750, 'money_max': 2000, 'class': 'B(Mythical)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.8, 'defense_boost': 0.5, 'crit_boost': 0.4, 'rare_magic_pack': 0.8, 'mythical_magic_pack': 0.4, 'skeleton_bone': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0},'weight': 1, 'area': 1, 'exp_min': 250, 'exp_max': 500},
    {'name': 'Troll Chieftain', 'hp': 800, 'atk_min': 120, 'atk_max': 150, 'money_min': 1500, 'money_max': 3000, 'class': 'C(Rare)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.7, 'defense_boost': 0.6, 'regen_potion': 0.5, 'rare_magic_pack': 0.7, 'mythical_magic_pack': 0.3, 'troll_core': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0},'weight': 1, 'area': 3, 'exp_min': 562, 'exp_max': 1125},
    {'name': 'Dark Lord', 'hp': 1200, 'atk_min': 135, 'atk_max': 189, 'money_min': 2500, 'money_max': 5000, 'class': 'B(Mythical)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.8, 'defense_boost': 0.6, 'crit_boost': 0.5, 'mythical_magic_pack': 0.8, 'prismatic_magic_pack': 0.4, 'dark_essence': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0},'weight': 1, 'area': 4, 'exp_min': 843, 'exp_max': 1687},
    {'name': 'Ice Queen', 'hp': 1500, 'magic_atk_min': 150, 'magic_atk_max': 75, 'money_min': 3500, 'money_max': 6000, 'class': 'B(Mythical)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'defense_boost': 0.8, 'regen_potion': 0.7, 'mythical_magic_pack': 0.7, 'prismatic_magic_pack': 0.5, 'frozen_heart': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0},'weight': 1, 'area': 5, 'exp_min': 1265, 'exp_max': 2531},
    {'name': 'Phoenix Lord', 'hp': 1800, 'atk_min': 100, 'atk_max': 150, 'money_min': 4500, 'money_max': 7500, 'class': 'A(Prismatic)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.8, 'mana_upgrade_potion': 0.6, 'mythical_magic_pack': 0.8, 'prismatic_magic_pack': 0.6, 'phoenix_feather': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0},'weight': 1, 'area': 6, 'exp_min': 1898, 'exp_max': 3796},
    {'name': 'Void Master', 'hp': 2200, 'atk_min': 190, 'atk_max': 240, 'money_min': 6000, 'money_max': 10000, 'class': 'A(Prismatic)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.9, 'defense_boost': 0.8, 'crit_boost': 0.7, 'prismatic_magic_pack': 0.8, 'divine_magic_pack': 0.4, 'void_fragment': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0},'weight': 1, 'area': 7, 'exp_min': 2847, 'exp_max': 5695},
    {'name': 'Celestial Emperor', 'hp': 2800, 'atk_min': 250, 'atk_max': 350, 'money_min': 8000, 'money_max': 13000, 'class': 'S(Divine)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 0.9, 'defense_boost': 0.9, 'mana_upgrade_potion': 0.7, 'prismatic_magic_pack': 0.8, 'divine_magic_pack': 0.6, 'holy_light': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0},'weight': 1, 'area': 8, 'exp_min': 4271, 'exp_max': 8542},
    {'name': 'Dragon Lord', 'hp': 3500, 'atk_min': 250, 'atk_max': 350, 'money_min': 10000, 'money_max': 16000, 'class': 'S(Divine)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 0.9, 'crit_boost': 0.8, 'divine_magic_pack': 0.8, 'transcendent_magic_pack': 0.4, 'dragon_scale': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0},'weight': 1, 'area': 9, 'exp_min': 6407, 'exp_max': 12814},
    {'name': 'Grim Reaper', 'hp': 4000, 'magic_atk_min': 300, 'magic_atk_max': 500, 'money_min': 12000, 'money_max': 20000, 'class': 'S(Divine)', 'is_boss': True, 'is_super_boss': False, 'drop': {'potion': 1.0, 'strength_boost': 1.0, 'defense_boost': 1.0, 'crit_boost': 1.0, 'prismatic_magic_pack': 0.8, 'divine_magic_pack': 0.8, 'soul_shard': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0},'weight': 1, 'area': 10, 'exp_min': 9610, 'exp_max': 19221},
    {'name': 'Demon King Muzan', 'hp': 12000, 'atk_min': 400, 'atk_max': 550, 'money_min': 100000, 'money_max': 500000, 'class': 'SS(Transcendent)', 'is_boss': True, 'is_super_boss': True, 'drop': {'potion': 1.0, 'strength_boost': 1, 'defense_boost': 1, 'crit_boost': 1, 'transcendent_heart': 0.5, 'divine_magic_pack': 0.8, 'transcendent_magic_pack': 0.4, 'demon_horn': 1.0, 'perm_exp_upgrade': 1.0, 'perm_strength_upgrade': 1.0, 'perm_defense_upgrade': 1.0, 'perm_health_upgrade': 1.0, 'perm_mana_upgrade': 1.0, 'perm_crit_chance_upgrade': 1.0, 'perm_mana_regen_upgrade': 1.0, 'perm_lifesteal_upgrade': 1.0, 'perm_lifesteal_chance_upgrade': 1.0},'weight': 0.01, 'area': 10, 'exp_min': 8000000000, 'exp_max': 10000000000}
    ]

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

# Titles
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
# Helper functions for dungeon functionality
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

def load_dungeon_treasure():
    """Load dungeon treasure from file"""
    global dungeon_treasure
    try:
        with open(DUNGEON_TREASURE_FILE, 'r') as f:
            dungeon_treasure = json.load(f)
    except:
        dungeon_treasure = {'money': 0, 'items': []}
        save_dungeon_treasure()

def save_dungeon_treasure():
    """Save dungeon treasure to file"""
    with open(DUNGEON_TREASURE_FILE, 'w') as f:
        json.dump(dungeon_treasure, f)
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
            print('You can move to areas 1-10. Higher areas have stronger monsters.')
            try:
                new_area = input("Enter area number (1-10) or 'cancel': ").strip()
                if new_area.lower() == 'cancel':
                    continue
                new_area = int(new_area)
                if 1 <= new_area <= 10:
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
                    print('Invalid area. Must be between 1 and 10.')
            except Exception:
                print('Invalid input. Enter a number between 1 and 10.')
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
                        boss_drop_pool = list(MATERIALS.keys()) + list(POTIONS.keys()) + list(misc.MAGIC_PACKS.keys())
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