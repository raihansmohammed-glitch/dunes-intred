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
import shop

def save_dungeon_treasure():
    global dungeon_treasure
    try:
        lock_file = misc.DUNGEON_TREASURE_FILE + '.lock'
        while os.path.exists(lock_file):
            time.sleep(0.01)
        with open(lock_file, 'w') as f:
            f.write('')
        temp_file = misc.DUNGEON_TREASURE_FILE + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump({'treasure': dungeon_treasure}, f)
        os.replace(temp_file, misc.DUNGEON_TREASURE_FILE)
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
        if os.path.exists(misc.DUNGEON_TREASURE_FILE):
            with open(misc.DUNGEON_TREASURE_FILE, 'r') as f:
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

def replenish_dungeon_treasure():
    """Replenish dungeon treasure items if below 10"""
    global dungeon_treasure
    if len(dungeon_treasure['items']) < 10:
        num_to_add = random.randint(20, 30) - len(dungeon_treasure['items'])
        consumables = list(misc.POTIONS.keys()) + list(misc.misc.MAGIC_PACKS.keys()) + list(misc.MATERIALS.keys())
        for _ in range(num_to_add):
            item = random.choice(consumables)
            dungeon_treasure['items'].append(item)
        save_dungeon_treasure()

def choose_monster_for_area(area):
    area_monsters = [m for m in misc.MONSTERS if m.get('area', area) == area and (not m['is_boss'])]
    if not area_monsters:
        area_monsters = [m for m in misc.MONSTERS if not m['is_boss']]
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
    area_bosses = [m for m in misc.MONSTERS if m.get('area', area) == area and m['is_boss']]
    if not area_bosses:
        area_bosses = [m for m in misc.MONSTERS if m['is_boss']]
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
    return next((m for m in misc.MONSTERS if m['is_boss']))

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
    w_atk = misc.WEAPONS.get(equip.get('weapon'), {}).get('atk', 0)
    n_atk = misc.NECKLACES.get(equip.get('necklace'), {}).get('atk_bonus', 0)
    a_def = misc.ARMORS.get(equip.get('armor'), {}).get('def', 0)
    n_def = misc.NECKLACES.get(equip.get('necklace'), {}).get('def_bonus', 0)
    robe_magic = misc.ROBES.get(equip.get('robe'), {}).get('magic_def', 0)
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

def check_stats(username):
    """Check if user has negative HP or Mana, and reset to max if so"""
    try:
        user_data = other_functions.load_user_data(username)
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
            other_functions.save_user_data(username, user_data)
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

def explore_dungeon(username):
    """Explore the dungeon to find treasure"""
    user_data = other_functions.load_user_data(username)
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
    other_functions.update_user(username, money=user_data['money'], player_data=user_data['player_data'])

def use_potions_interface(username, player_hp, player_mana, stats, inventory, active_buffs):
    try:
        user_data = other_functions.load_user_data(username)
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
            if count > 0 and key in misc.POTIONS:
                potion_list.append((key, misc.POTIONS[key]['name'], count))
                print(f"{len(potion_list)}. {misc.POTIONS[key]['name']} x{count}")
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
                    effect = misc.POTIONS[potion_key]['effect']
                    amount = misc.POTIONS[potion_key]['amount']
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
                            duration = misc.POTIONS[potion_key]['duration']
                            active_buffs.append({'type': buff_type, 'amount': amount, 'remaining': duration})
                            print(f"You used {potion_name} and gained {amount} {buff_type.replace('_', ' ')} for {duration} fights!")
                    inventory[potion_key] -= qty
                    stats['hp'] = player_hp
                    stats['mana'] = player_mana
                    player_data = {'stats': stats, 'inventory': inventory}
                    user_data = other_functions.load_user_data(username)
                    if user_data:
                        user_data['player_data'] = player_data
                        other_functions.save_user_data(username, user_data)
                else:
                    print(f'Not enough {potion_name} (have {count}).')
            else:
                print('Invalid choice.')
        else:
            print('Invalid choice.')
    return (player_hp, player_mana, active_buffs)

def use_buff_interface(username, player_hp, player_mana, stats, inventory, active_buffs):
    try:
        user_data = other_functions.load_user_data(username)
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
            if count > 0 and key in misc.POTIONS and misc.POTIONS[key]['effect'].startswith('buff'):
                buff_list.append((key, misc.POTIONS[key]['name'], count))
                print(f"{len(buff_list)}. {misc.POTIONS[key]['name']} x{count}")
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
                    effect = misc.POTIONS[buff_key]['effect']
                    amount = misc.POTIONS[buff_key]['amount']
                    for _ in range(qty):
                        if effect.startswith('buff'):
                            buff_type = effect[5:]
                            duration = misc.POTIONS[buff_key]['duration']
                            active_buffs.append({'type': buff_type, 'amount': amount, 'remaining': duration})
                            print(f"You used {buff_name} and gained {amount} {buff_type.replace('_', ' ')} for {duration} fights!")
                    inventory[buff_key] -= qty
                    player_data = {'stats': stats, 'inventory': inventory}
                    user_data = other_functions.load_user_data(username)
                    if user_data:
                        user_data['player_data'] = player_data
                        other_functions.save_user_data(username, user_data)
                else:
                    print(f'Not enough {buff_name} (have {count}).')
            else:
                print('Invalid choice.')
        else:
            print('Invalid choice.')
    return (player_hp, player_mana, active_buffs)

def dungeon(username):
    global exp_gain
    '\n    Dungeon combat loop that uses:\n      - apply_permanent_upgrades(username)\n      - compute_effective_stats(...)\n      - get_equip_and_perm_bonuses(stats)\n      - apply_damage_with_defense(...) and apply_magic_damage(...)\n      - calculate_total_crit_chance(...)\n    '
    try:
        other_functions.apply_permanent_upgrades(username)
    except Exception:
        pass
    user_data = other_functions.load_user_data(username)
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
            other_functions.auto_equip_items(username)
            user_data = other_functions.load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
        except Exception:
            pass
    if settings.get('auto_equip_spells', False) or settings.get('auto_equip_everything', False):
        try:
            other_functions.auto_equip_spells(username)
            user_data = other_functions.load_user_data(username)
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
            other_functions.save_user_data(username, user_data)
            return
        if lc == 'shop':
            shop.shop()
            other_functions.ensure_user_fields(username)
            user_data = other_functions.load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'packs':
            other_functions.magic_pack_interface(username)
            other_functions.ensure_user_fields(username)
            user_data = other_functions.load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'titles':
            other_functions.equip_titles_menu(username, player_data, None)
            other_functions.ensure_user_fields(username)
            user_data = other_functions.load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'inventory':
            other_functions.manage_inventory_menu(username, player_data, None)
            other_functions.ensure_user_fields(username)
            user_data = other_functions.load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'spells':
            other_functions.magic_spell_interface(username)
            other_functions.ensure_user_fields(username)
            user_data = other_functions.load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'status':
            try:
                other_functions.apply_permanent_upgrades(username)
            except Exception:
                pass
            effective_atk, effective_def, effective_magic_atk, effective_magic_def, _, _, _, _ = other_functions.compute_effective_stats(stats, active_buffs)
            next_exp = other_functions.exp_to_next(stats.get('level', 1)) if stats.get('level', 1) < other_functions.MAX_LEVEL else 'MAX'
            money = user_data.get('money')
            name_display = username
            if stats.get('settings', {}).get('call_including_title', True) and stats.get('title'):
                name_display = f"{stats['title']} {username}"
            exp_display = other_functions.create_exp_bar(stats.get('exp'), next_exp) if stats.get('settings', {}).get('show_exp_bar', False) else f"{stats.get('exp')}/{next_exp}"
            print(f"{name_display} - HP: {player_hp}/{stats.get('hp_max')}, MANA: {player_mana}/{stats.get('mana_max')}, ATK: {effective_atk}, DEF: {effective_def}, Money: ${money}, LVL: {stats.get('level')}, EXP: {exp_display}, AREA: {stats.get('current_area', 1)}")
            print(f"Permanent Boosts: ATK +{stats.get('perm_atk', 0)}, DEF +{stats.get('perm_def', 0)}, HP +{stats.get('perm_hp_max', 0)}, Mana +{stats.get('perm_mana_max', 0)}, Crit +{stats.get('perm_crit_chance', 0)}%, Regen +{stats.get('perm_mana_regen', 0)}, Lifesteal +{stats.get('perm_lifesteal', 0)}%, Exp +{stats.get('perm_exp_boost', 0)}%")
            if active_buffs:
                print('Active buffs:')
                for b in active_buffs:
                    if b.get('remaining', 0) > 0:
                        print(f' - {b}')
            continue
        if lc == 'shop':
            shop.shop()
            other_functions.ensure_user_fields(username)
            user_data = other_functions.load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'packs':
            other_functions.magic_pack_interface(username)
            other_functions.ensure_user_fields(username)
            user_data = other_functions.load_user_data(username)
            player_data = user_data.get('player_data', {})
            stats = player_data.get('stats', {})
            inventory = player_data.get('inventory', {})
            player_mana = stats.get('mana', stats.get('mana_max', 50))
            player_hp = stats.get('hp', stats.get('hp_max', 100))
            continue
        if lc == 'upgrades':
            other_functions.permanent_upgrades_interface(username)
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
                    min_level = (new_area - 1) * other_functions.LEVELS_PER_AREA + 1
                    if player_level < min_level:
                        print(f'You need to be at least level {min_level} to enter Area {new_area}. Your current level is {player_level}.')
                        continue
                    stats['current_area'] = new_area
                    current_area = new_area
                    player_data['stats'] = stats
                    user_data['player_data'] = player_data
                    other_functions.save_user_data(username, user_data)
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
                        aliases = misc.MONSTER_ALIASES.get('boss', {})
                        monster_name = aliases.get(alias)
                        if monster_name:
                            found = next((m for m in misc.MONSTERS if m['name'].lower() == monster_name.lower()), None)
                            if found:
                                monster = found.copy()
                                print(f"\n🔥 BOSS APPEARS: {monster['name']}! (HP {monster.get('hp')}, ATK {monster.get('atk_min', '?')}–{monster.get('atk_max', '?')})")
                            else:
                                continue
                        else:
                            continue
                    elif flag in ('n', 'no', 'normal', 'monster', 'm'):
                        aliases = misc.MONSTER_ALIASES.get('normal', {})
                        monster_name = aliases.get(alias)
                        if monster_name:
                            found = next((m for m in misc.MONSTERS if m['name'].lower() == monster_name.lower()), None)
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
                    other_functions.apply_permanent_upgrades(username)
                except Exception:
                    pass
                effective_atk, effective_def, effective_magic_atk, effective_magic_def, _, _, _, _ = other_functions.compute_effective_stats(stats, active_buffs)
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
                    other_functions.save_user_data(username, user_data)
                elif action == 'm':
                    equipped_spells = stats.get('equipped_spells', [None, None, None, None])
                    if not any(equipped_spells):
                        print("You haven't equipped any spells yet. Visit the Magic Spells interface to equip spells!")
                        continue
                    available = [misc.SPELLS_BY_KEY[s] for s in equipped_spells if s is not None and s in misc.SPELLS_BY_KEY]
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
                        wand_magic = misc.WANDS.get(stats.get('equipped', {}).get('wand'), {}).get('magic_atk', 0)
                        perm_magic_atk = stats.get('perm_magic_atk', 0)
                        heal_power = s.get('power', 0) + wand_magic + perm_magic_atk + random.randint(-(s.get('power', 0) // 8), s.get('power', 0) // 8)
                        if random.random() <= total_crit_chance:
                            heal_power = int(heal_power * 2)
                            stats['critical_hits'] = stats.get('critical_hits', 0) + 1
                            print('✨ CRITICAL HEAL!')
                        player_hp = min(player_hp + heal_power, stats.get('hp_max', 100))
                        print(f"You cast {s['name']} healing yourself for {heal_power} HP! (Your HP: {player_hp}/{stats.get('hp_max')})")
                    else:
                        wand_magic = misc.WANDS.get(stats.get('equipped', {}).get('wand'), {}).get('magic_atk', 0)
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
                    other_functions.save_user_data(username, user_data)
                elif action == 'p':
                    player_hp, player_mana, active_buffs = use_potions_interface(username, player_hp, player_mana, stats, inventory, active_buffs)
                    user_data = other_functions.load_user_data(username)
                    player_data = user_data.get('player_data', {})
                    stats = player_data.get('stats', {})
                elif action == 'u':
                    player_hp, player_mana, active_buffs = use_buff_interface(username, player_hp, player_mana, stats, inventory, active_buffs)
                    user_data = other_functions.load_user_data(username)
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
                    other_functions.save_user_data(username, user_data)
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
                        losable_items = [k for k, v in inventory.items() if v > 0 and k not in misc.PERM_UPGRADES]
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
                        other_functions.save_user_data(username, user_data)
                        save_dungeon_treasure()
                        return
                if monster.get('hp', 0) <= 0:
                    money_reward = random.randint(monster.get('money_min', 1), monster.get('money_max', 1))
                    user_data = other_functions.load_user_data(username)
                    if user_data:
                        money = int(user_data.get('money', 0))
                    else:
                        money = int(player_data.get('money', 0))
                    money += money_reward
                    user_data['money'] = money
                    player_data['money'] = money
                    other_functions.save_user_data(username, user_data)
                    drops = []
                    for item_name, chance in monster.get('drop', {}).items():
                        if random.random() <= chance:
                            inventory[item_name] = inventory.get(item_name, 0) + 1
                            drops.append(item_name)
                    mat_drops = add_material_drops(inventory, monster)
                    if mat_drops:
                        drops.extend(mat_drops)
                    if monster.get('is_boss') and monster['name'] != 'Skeleton King':
                        for perm_key in misc.PERM_UPGRADES:
                            inventory[perm_key] = inventory.get(perm_key, 0) + 1
                            drops.append(f"{misc.PERM_UPGRADES[perm_key]['name']} (Permanent Upgrade)")
                    stats['monsters_defeated'] = stats.get('monsters_defeated', 0) + 1
                    if monster.get('is_boss'):
                        stats['bosses_defeated'] = stats.get('bosses_defeated', 0) + 1
                    stats['total_money_earned'] = stats.get('total_money_earned', 0) + money_reward
                    stats['hp'] = player_hp
                    stats['mana'] = player_mana
                    player_data['stats'] = stats
                    player_data['inventory'] = inventory
                    user_data['player_data'] = player_data
                    other_functions.save_user_data(username, user_data)
                    exp_gain = random.randint(monster['exp_min'], monster['exp_max'])
                    exp_gain = other_functions.grant_exp(username, exp_gain)
                    user_data = other_functions.load_user_data(username)
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
                        for perm_key in misc.PERM_UPGRADES:
                            inventory[perm_key] = inventory.get(perm_key, 0) + 1
                            drops.append(f"{misc.PERM_UPGRADES[perm_key]['name']} (Permanent Upgrade)")
                        boss_drop_pool = list(misc.MATERIALS.keys()) + list(misc.POTIONS.keys()) + list(misc.misc.MAGIC_PACKS.keys())
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
                    other_functions.save_user_data(username, user_data)
                    other_functions.check_achievements(username)
                    other_functions.save_all_data()
                    other_functions.save_user_data(username, user_data)
                    break