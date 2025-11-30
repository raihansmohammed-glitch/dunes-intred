import json
import random
import os
import time
import atexit
import threading
import socket

import dungeon_functions
import misc

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
        if 'atk_increase' in dungeon_functions.PERM_UPGRADES[up_key]:
            stats['perm_atk'] = stats.get('perm_atk', 0) + dungeon_functions.PERM_UPGRADES[up_key]['atk_increase']
        elif 'def_increase' in dungeon_functions.PERM_UPGRADES[up_key]:
            stats['perm_def'] = stats.get('perm_def', 0) + dungeon_functions.PERM_UPGRADES[up_key]['def_increase']
        elif 'hp_increase' in dungeon_functions.PERM_UPGRADES[up_key]:
            stats['perm_hp_max'] = stats.get('perm_hp_max', 0) + dungeon_functions.PERM_UPGRADES[up_key]['hp_increase']
        elif 'magic_increase' in dungeon_functions.PERM_UPGRADES[up_key]:
            stats['perm_mana_max'] = stats.get('perm_mana_max', 0) + dungeon_functions.PERM_UPGRADES[up_key]['magic_increase']
        elif 'crit_chance_increase' in dungeon_functions.PERM_UPGRADES[up_key]:
            stats['perm_crit_chance'] = stats.get('perm_crit_chance', 0) + dungeon_functions.PERM_UPGRADES[up_key]['crit_chance_increase']
        elif 'mana_regen_increase' in dungeon_functions.PERM_UPGRADES[up_key]:
            stats['perm_mana_regen'] = stats.get('perm_mana_regen', 0) + dungeon_functions.PERM_UPGRADES[up_key]['mana_regen_increase']
        elif 'max_lifesteal_increase' in dungeon_functions.PERM_UPGRADES[up_key]:
            stats['perm_lifesteal'] = stats.get('perm_lifesteal', 0) + dungeon_functions.PERM_UPGRADES[up_key]['max_lifesteal_increase']
        elif 'lifesteal_chance_increase' in dungeon_functions.PERM_UPGRADES[up_key]:
            stats['perm_lifesteal_chance'] = stats.get('perm_lifesteal_chance', 0) + dungeon_functions.PERM_UPGRADES[up_key]['lifesteal_chance_increase']
        elif 'exp_increase' in dungeon_functions.PERM_UPGRADES[up_key]:
            old_boost = stats.get('perm_exp_boost', 0)
            stats['perm_exp_boost'] = old_boost + dungeon_functions.PERM_UPGRADES[up_key]['exp_increase']
    while True:
        print('\n--- Permanent Upgrades ---')
        print('Available upgrades (use permanent upgrade items from inventory):')
        for key, upgrade in dungeon_functions.PERM_UPGRADES.items():
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
        if opt == 'all':
            total_applied = 0
            for up_key in dungeon_functions.PERM_UPGRADES:
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
        elif opt in dungeon_functions.PERM_UPGRADES and inventory.get(opt, 0) >= qty:
            inventory[opt] -= qty
            for _ in range(qty):
                apply_single_upgrade(stats, opt)
            player_data['inventory'] = inventory
            player_data['stats'] = stats
            user_data['player_data'] = player_data
            save_user_data(username, user_data)
            check_achievements(username)
            print(f"Used {qty}x {dungeon_functions.PERM_UPGRADES[opt]['name']}!")
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
            elif result_item in dungeon_functions.PERM_UPGRADES:
                result_name = dungeon_functions.PERM_UPGRADES[result_item]['name']
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