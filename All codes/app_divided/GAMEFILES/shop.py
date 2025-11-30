import other_functions
import misc
import dungeon_functions
import main

def shop():
    global current_user
    if not current_user:
        print('You must be logged in to access the shop.')
        return
    user_data = other_functions.load_user_data(current_user)
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
        print(f"10. Wooden Sword (+2 ATK) - ${misc.WEAPONS['wooden_sword']['price']}")
        print(f"11. Iron Sword (+5 ATK) - ${misc.WEAPONS['iron_sword']['price']}")
        print(f"12. Steel Sword (+8 ATK) - ${misc.WEAPONS['steel_sword']['price']}")
        print(f"13. Diamond Sword (+50 ATK) - ${misc.WEAPONS['diamond_sword']['price']}")
        print(f"14. Void Sword (+200 ATK) - ${misc.WEAPONS['void_sword']['price']}")
        print(f"15. Infinitium Sword (+2000 ATK) - ${misc.WEAPONS['infinitium_sword']['price']} and {misc.WEAPONS['infinitium_sword'].get('score_price', 0)} score")
        print(f"16. Frostblade (+120 ATK) - ${misc.WEAPONS['frostblade']['price']} and {misc.WEAPONS['frostblade'].get('score_price', 0)} score")
        print(f"17. Flameblade (+130 ATK) - ${misc.WEAPONS['flameblade']['price']} and {misc.WEAPONS['flameblade'].get('score_price', 0)} score")
        print(f"18. Thunder Sword (+150 ATK) - ${misc.WEAPONS['thunder_sword']['price']} and {misc.WEAPONS['thunder_sword'].get('score_price', 0)} score")
        print(f"19. Holy Avenger (+180 ATK) - ${misc.WEAPONS['holy_avenger']['price']} and {misc.WEAPONS['holy_avenger'].get('score_price', 0)} score")
        print(f"20. Dragon Slayer (+250 ATK) - ${misc.WEAPONS['dragon_slayer']['price']} and {misc.WEAPONS['dragon_slayer'].get('score_price', 0)} score")
        print(f"21. Cosmic Blade (+500 ATK) - ${misc.WEAPONS['cosmic_blade']['price']} and {misc.WEAPONS['cosmic_blade'].get('score_price', 0)} score")
        print(f"22. Transcendent Edge (+1500 ATK) - ${misc.WEAPONS['transcendent_edge']['price']} and {misc.WEAPONS['transcendent_edge'].get('score_price', 0)} score")
        print('\n----- Armors -----')
        print(f"23. Leather Armor (+1 DEF) - ${misc.ARMORS['leather_armor']['price']}")
        print(f"24. Chainmail (+3 DEF) - ${misc.ARMORS['chainmail']['price']}")
        print(f"25. Plate Armor (+6 DEF) - ${misc.ARMORS['plate_armor']['price']}")
        print(f"26. Diamond Armor (+25 DEF) - ${misc.ARMORS['diamond_armor']['price']}")
        print(f"27. Void Armor (+75 DEF) - ${misc.ARMORS['void_armor']['price']}")
        print(f"28. Infinitium Armor (+300 DEF) - ${misc.ARMORS['infinitium_armor']['price']} and {misc.ARMORS['infinitium_armor'].get('score_price', 0)} score")
        print(f"29. Frost Armor (+40 DEF) - ${misc.ARMORS['frost_armor']['price']} and {misc.ARMORS['frost_armor'].get('score_price', 0)} score")
        print(f"30. Flame Armor (+45 DEF) - ${misc.ARMORS['flame_armor']['price']} and {misc.ARMORS['flame_armor'].get('score_price', 0)} score")
        print(f"31. Thunder Armor (+55 DEF) - ${misc.ARMORS['thunder_armor']['price']} and {misc.ARMORS['thunder_armor'].get('score_price', 0)} score")
        print(f"32. Holy Armor (+70 DEF) - ${misc.ARMORS['holy_armor']['price']} and {misc.ARMORS['holy_armor'].get('score_price', 0)} score")
        print(f"33. Dragon Scale Armor (+100 DEF) - ${misc.ARMORS['dragon_scale_armor']['price']} and {misc.ARMORS['dragon_scale_armor'].get('score_price', 0)} score")
        print(f"34. Cosmic Armor (+200 DEF) - ${misc.ARMORS['cosmic_armor']['price']} and {misc.ARMORS['cosmic_armor'].get('score_price', 0)} score")
        print(f"35. Transcendent Armor (+500 DEF) - ${misc.ARMORS['transcendent_armor']['price']} and {misc.ARMORS['transcendent_armor'].get('score_price', 0)} score")
        print('\n----- Wands (mana weapons) -----')
        print(f"36. Apprentice Wand (+5 magic) - ${misc.WANDS['apprentice_wand']['price']}")
        print(f"37. Mage Wand (+20 magic) - ${misc.WANDS['mage_wand']['price']}")
        print(f"38. Archmage Staff (+120 magic) - ${misc.WANDS['archmage_staff']['price']} and {misc.WANDS['archmage_staff'].get('score_price', 0)} score")
        print(f"39. Frost Wand (+60 magic) - ${misc.WANDS['frost_wand']['price']} and {misc.WANDS['frost_wand'].get('score_price', 0)} score")
        print(f"40. Flame Wand (+65 magic) - ${misc.WANDS['flame_wand']['price']} and {misc.WANDS['flame_wand'].get('score_price', 0)} score")
        print(f"41. Thunder Wand (+75 magic) - ${misc.WANDS['thunder_wand']['price']} and {misc.WANDS['thunder_wand'].get('score_price', 0)} score")
        print(f"42. Holy Scepter (+90 magic) - ${misc.WANDS['holy_scepter']['price']} and {misc.WANDS['holy_scepter'].get('score_price', 0)} score")
        print(f"43. Dragon Staff (+125 magic) - ${misc.WANDS['dragon_staff']['price']} and {misc.WANDS['dragon_staff'].get('score_price', 0)} score")
        print(f"44. Cosmic Scepter (+250 magic) - ${misc.WANDS['cosmic_scepter']['price']} and {misc.WANDS['cosmic_scepter'].get('score_price', 0)} score")
        print(f"45. Transcendent Staff (+750 magic) - ${misc.WANDS['transcendent_staff']['price']} and {misc.WANDS['transcendent_staff'].get('score_price', 0)} score")
        print('\n----- Robes -----')
        print(f"46. Cloth Robe (+2 magic def) - ${misc.ROBES['cloth_robe']['price']}")
        print(f"47. Silk Robe (+10 magic def) - ${misc.ROBES['silk_robe']['price']}")
        print(f"48. Void Robe (+80 magic def) - ${misc.ROBES['void_robe']['price']} and {misc.ROBES['void_robe'].get('score_price', 0)} score")
        print(f"49. Frost Robe (+30 magic def) - ${misc.ROBES['frost_robe']['price']} and {misc.ROBES['frost_robe'].get('score_price', 0)} score")
        print(f"50. Flame Robe (+35 magic def) - ${misc.ROBES['flame_robe']['price']} and {misc.ROBES['flame_robe'].get('score_price', 0)} score")
        print(f"51. Thunder Robe (+45 magic def) - ${misc.ROBES['thunder_robe']['price']} and {misc.ROBES['thunder_robe'].get('score_price', 0)} score")
        print(f"52. Holy Robe (+60 magic def) - ${misc.ROBES['holy_robe']['price']} and {misc.ROBES['holy_robe'].get('score_price', 0)} score")
        print(f"53. Dragon Robe (+90 magic def) - ${misc.ROBES['dragon_robe']['price']} and {misc.ROBES['dragon_robe'].get('score_price', 0)} score")
        print(f"54. Cosmic Robe (+180 magic def) - ${misc.ROBES['cosmic_robe']['price']} and {misc.ROBES['cosmic_robe'].get('score_price', 0)} score")
        print(f"55. Transcendent Robe (+450 magic def) - ${misc.ROBES['transcendent_robe']['price']} and {misc.ROBES['transcendent_robe'].get('score_price', 0)} score")
        print('\n----- Necklaces -----')
        print(f"56. Health Amulet (+20 HP) - ${misc.NECKLACES['health_amulet']['price']}")
        print(f"57. Mana Amulet (+15 Mana) - ${misc.NECKLACES['mana_amulet']['price']}")
        print(f"58. Strength Amulet (+5 ATK) - ${misc.NECKLACES['strength_amulet']['price']}")
        print(f"59. Defense Amulet (+3 DEF) - ${misc.NECKLACES['defense_amulet']['price']}")
        print(f"60. Critical Amulet (+10% Crit) - ${misc.NECKLACES['crit_amulet']['price']}")
        print(f"61. Lifesteal Amulet (+5% Lifesteal) - ${misc.NECKLACES['lifesteal_amulet']['price']}")
        print(f"62. Frost Necklace (+15 Magic Def, +30 HP) - ${misc.NECKLACES['frost_necklace']['price']} and {misc.NECKLACES['frost_necklace'].get('score_price', 0)} score")
        print(f"63. Flame Necklace (+10 Magic Atk, +8 ATK) - ${misc.NECKLACES['flame_necklace']['price']} and {misc.NECKLACES['flame_necklace'].get('score_price', 0)} score")
        print(f"64. Thunder Necklace (+15% Crit, +10 ATK) - ${misc.NECKLACES['thunder_necklace']['price']} and {misc.NECKLACES['thunder_necklace'].get('score_price', 0)} score")
        print(f"65. Holy Pendant (+50 HP, +30 Mana, +5 DEF) - ${misc.NECKLACES['holy_pendant']['price']} and {misc.NECKLACES['holy_pendant'].get('score_price', 0)} score")
        print(f"66. Dragon Necklace (+20 ATK, +15 DEF, +70 HP) - ${misc.NECKLACES['dragon_necklace']['price']} and {misc.NECKLACES['dragon_necklace'].get('score_price', 0)} score")
        print(f"67. Cosmic Necklace (+30 Magic Atk, +25 Magic Def, +50 Mana) - ${misc.NECKLACES['cosmic_necklace']['price']} and {misc.NECKLACES['cosmic_necklace'].get('score_price', 0)} score")
        print(f"68. Transcendent Necklace (+50 ATK, +40 DEF, +150 HP, +100 Mana, +20% Crit, +10% Lifesteal) - ${misc.NECKLACES['transcendent_necklace']['price']} and {misc.NECKLACES['transcendent_necklace'].get('score_price', 0)} score")
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
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['wooden_sword']['price']
            is_equipment = True
        elif opt == '11':
            item_name = 'iron_sword'
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['iron_sword']['price']
            is_equipment = True
        elif opt == '12':
            item_name = 'steel_sword'
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['steel_sword']['price']
            is_equipment = True
        elif opt == '13':
            item_name = 'diamond_sword'
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['diamond_sword']['price']
            is_equipment = True
        elif opt == '14':
            item_name = 'void_sword'
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['void_sword']['price']
            is_equipment = True
        elif opt == '15':
            item_name = 'infinitium_sword'
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['infinitium_sword']['price']
            score_cost = misc.WEAPONS['infinitium_sword'].get('score_price', 0)
            is_equipment = True
        elif opt == '16':
            item_name = 'frostblade'
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['frostblade']['price']
            score_cost = misc.WEAPONS['frostblade'].get('score_price', 0)
            is_equipment = True
        elif opt == '17':
            item_name = 'flameblade'
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['flameblade']['price']
            score_cost = misc.WEAPONS['flameblade'].get('score_price', 0)
            is_equipment = True
        elif opt == '18':
            item_name = 'thunder_sword'
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['thunder_sword']['price']
            score_cost = misc.WEAPONS['thunder_sword'].get('score_price', 0)
            is_equipment = True
        elif opt == '19':
            item_name = 'holy_avenger'
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['holy_avenger']['price']
            score_cost = misc.WEAPONS['holy_avenger'].get('score_price', 0)
            is_equipment = True
        elif opt == '20':
            item_name = 'dragon_slayer'
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['dragon_slayer']['price']
            score_cost = misc.WEAPONS['dragon_slayer'].get('score_price', 0)
            is_equipment = True
        elif opt == '21':
            item_name = 'cosmic_blade'
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['cosmic_blade']['price']
            score_cost = misc.WEAPONS['cosmic_blade'].get('score_price', 0)
            is_equipment = True
        elif opt == '22':
            item_name = 'transcendent_edge'
            item_dict = misc.WEAPONS
            cost = misc.WEAPONS['transcendent_edge']['price']
            score_cost = misc.WEAPONS['transcendent_edge'].get('score_price', 0)
            is_equipment = True
        elif opt == '23':
            item_name = 'leather_armor'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['leather_armor']['price']
            is_equipment = True
        elif opt == '24':
            item_name = 'chainmail'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['chainmail']['price']
            is_equipment = True
        elif opt == '25':
            item_name = 'plate_armor'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['plate_armor']['price']
            is_equipment = True
        elif opt == '26':
            item_name = 'diamond_armor'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['diamond_armor']['price']
            is_equipment = True
        elif opt == '27':
            item_name = 'void_armor'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['void_armor']['price']
            is_equipment = True
        elif opt == '28':
            item_name = 'infinitium_armor'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['infinitium_armor']['price']
            score_cost = misc.ARMORS['infinitium_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '29':
            item_name = 'frost_armor'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['frost_armor']['price']
            score_cost = misc.ARMORS['frost_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '30':
            item_name = 'flame_armor'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['flame_armor']['price']
            score_cost = misc.ARMORS['flame_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '31':
            item_name = 'thunder_armor'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['thunder_armor']['price']
            score_cost = misc.ARMORS['thunder_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '32':
            item_name = 'holy_armor'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['holy_armor']['price']
            score_cost = misc.ARMORS['holy_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '33':
            item_name = 'dragon_scale_armor'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['dragon_scale_armor']['price']
            score_cost = misc.ARMORS['dragon_scale_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '34':
            item_name = 'cosmic_armor'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['cosmic_armor']['price']
            score_cost = misc.ARMORS['cosmic_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '35':
            item_name = 'transcendent_armor'
            item_dict = misc.ARMORS
            cost = misc.ARMORS['transcendent_armor']['price']
            score_cost = misc.ARMORS['transcendent_armor'].get('score_price', 0)
            is_equipment = True
        elif opt == '36':
            item_name = 'apprentice_wand'
            item_dict = misc.WANDS
            cost = misc.WANDS['apprentice_wand']['price']
            is_equipment = True
        elif opt == '37':
            item_name = 'mage_wand'
            item_dict = misc.WANDS
            cost = misc.WANDS['mage_wand']['price']
            is_equipment = True
        elif opt == '38':
            item_name = 'archmage_staff'
            item_dict = misc.WANDS
            cost = misc.WANDS['archmage_staff']['price']
            score_cost = misc.WANDS['archmage_staff'].get('score_price', 0)
            is_equipment = True
        elif opt == '39':
            item_name = 'frost_wand'
            item_dict = misc.WANDS
            cost = misc.WANDS['frost_wand']['price']
            score_cost = misc.WANDS['frost_wand'].get('score_price', 0)
            is_equipment = True
        elif opt == '40':
            item_name = 'flame_wand'
            item_dict = misc.WANDS
            cost = misc.WANDS['flame_wand']['price']
            score_cost = misc.WANDS['flame_wand'].get('score_price', 0)
            is_equipment = True
        elif opt == '41':
            item_name = 'thunder_wand'
            item_dict = misc.WANDS
            cost = misc.WANDS['thunder_wand']['price']
            score_cost = misc.WANDS['thunder_wand'].get('score_price', 0)
            is_equipment = True
        elif opt == '42':
            item_name = 'holy_scepter'
            item_dict = misc.WANDS
            cost = misc.WANDS['holy_scepter']['price']
            score_cost = misc.WANDS['holy_scepter'].get('score_price', 0)
            is_equipment = True
        elif opt == '43':
            item_name = 'dragon_staff'
            item_dict = misc.WANDS
            cost = misc.WANDS['dragon_staff']['price']
            score_cost = misc.WANDS['dragon_staff'].get('score_price', 0)
            is_equipment = True
        elif opt == '44':
            item_name = 'cosmic_scepter'
            item_dict = misc.WANDS
            cost = misc.WANDS['cosmic_scepter']['price']
            score_cost = misc.WANDS['cosmic_scepter'].get('score_price', 0)
            is_equipment = True
        elif opt == '45':
            item_name = 'transcendent_staff'
            item_dict = misc.WANDS
            cost = misc.WANDS['transcendent_staff']['price']
            score_cost = misc.WANDS['transcendent_staff'].get('score_price', 0)
            is_equipment = True
        elif opt == '46':
            item_name = 'cloth_robe'
            item_dict = misc.misc.ROBES
            cost = misc.misc.ROBES['cloth_robe']['price']
            is_equipment = True
        elif opt == '47':
            item_name = 'silk_robe'
            item_dict = misc.misc.ROBES
            cost = misc.misc.ROBES['silk_robe']['price']
            is_equipment = True
        elif opt == '48':
            item_name = 'void_robe'
            item_dict = misc.misc.ROBES
            cost = misc.misc.ROBES['void_robe']['price']
            score_cost = misc.misc.ROBES['void_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '49':
            item_name = 'frost_robe'
            item_dict = misc.misc.ROBES
            cost = misc.misc.ROBES['frost_robe']['price']
            score_cost = misc.misc.ROBES['frost_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '50':
            item_name = 'flame_robe'
            item_dict = misc.misc.ROBES
            cost = misc.misc.ROBES['flame_robe']['price']
            score_cost = misc.misc.ROBES['flame_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '51':
            item_name = 'thunder_robe'
            item_dict = misc.misc.ROBES
            cost = misc.misc.ROBES['thunder_robe']['price']
            score_cost = misc.misc.ROBES['thunder_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '52':
            item_name = 'holy_robe'
            item_dict = misc.misc.ROBES
            cost = misc.misc.ROBES['holy_robe']['price']
            score_cost = misc.misc.ROBES['holy_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '53':
            item_name = 'dragon_robe'
            item_dict = misc.misc.ROBES
            cost = misc.misc.ROBES['dragon_robe']['price']
            score_cost = misc.misc.ROBES['dragon_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '54':
            item_name = 'cosmic_robe'
            item_dict = misc.misc.ROBES
            cost = misc.misc.ROBES['cosmic_robe']['price']
            score_cost = misc.misc.ROBES['cosmic_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '55':
            item_name = 'transcendent_robe'
            item_dict = misc.misc.ROBES
            cost = misc.misc.ROBES['transcendent_robe']['price']
            score_cost = misc.misc.ROBES['transcendent_robe'].get('score_price', 0)
            is_equipment = True
        elif opt == '56':
            item_name = 'health_amulet'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['health_amulet']['price']
            is_equipment = True
        elif opt == '57':
            item_name = 'mana_amulet'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['mana_amulet']['price']
            is_equipment = True
        elif opt == '58':
            item_name = 'strength_amulet'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['strength_amulet']['price']
            is_equipment = True
        elif opt == '59':
            item_name = 'defense_amulet'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['defense_amulet']['price']
            is_equipment = True
        elif opt == '60':
            item_name = 'crit_amulet'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['crit_amulet']['price']
            is_equipment = True
        elif opt == '61':
            item_name = 'lifesteal_amulet'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['lifesteal_amulet']['price']
            is_equipment = True
        elif opt == '62':
            item_name = 'frost_necklace'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['frost_necklace']['price']
            score_cost = misc.misc.NECKLACES['frost_necklace'].get('score_price', 0)
            is_equipment = True
        elif opt == '63':
            item_name = 'flame_necklace'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['flame_necklace']['price']
            score_cost = misc.misc.NECKLACES['flame_necklace'].get('score_price', 0)
            is_equipment = True
        elif opt == '64':
            item_name = 'thunder_necklace'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['thunder_necklace']['price']
            score_cost = misc.misc.NECKLACES['thunder_necklace'].get('score_price', 0)
            is_equipment = True
        elif opt == '65':
            item_name = 'holy_pendant'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['holy_pendant']['price']
            score_cost = misc.misc.NECKLACES['holy_pendant'].get('score_price', 0)
            is_equipment = True
        elif opt == '66':
            item_name = 'dragon_necklace'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['dragon_necklace']['price']
            score_cost = misc.misc.NECKLACES['dragon_necklace'].get('score_price', 0)
            is_equipment = True
        elif opt == '67':
            item_name = 'cosmic_necklace'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['cosmic_necklace']['price']
            score_cost = misc.misc.NECKLACES['cosmic_necklace'].get('score_price', 0)
            is_equipment = True
        elif opt == '68':
            item_name = 'transcendent_necklace'
            item_dict = misc.misc.NECKLACES
            cost = misc.misc.NECKLACES['transcendent_necklace']['price']
            score_cost = misc.misc.NECKLACES['transcendent_necklace'].get('score_price', 0)
            is_equipment = True
        elif opt == '69':
            other_functions.manage_inventory_menu(current_user, player_data, None)
            user_data = other_functions.load_user_data(current_user)
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
                other_functions.save_user_data(current_user, user_data)
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
                other_functions.save_user_data(current_user, user_data)
                print('Sold 1 potion for $10.')
            else:
                print('No potions to sell.')
            continue
        elif opt == '72':
            other_functions.crafting_interface(current_user)
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
                        other_functions.save_user_data(current_user, user_data)
                        print(f'Purchased {item_name} for ${cost}' + (f' and {score_cost} score' if score_cost > 0 else '') + '!')
                else:
                    total_cost = cost * qty
                    if money >= total_cost:
                        inventory[item_name] = inventory.get(item_name, 0) + qty
                        money -= total_cost
                        player_data['inventory'] = inventory
                        user_data['money'] = money
                        user_data['player_data'] = player_data
                        other_functions.save_user_data(current_user, user_data)
                        print(f'Purchased {qty}x {item_name} for ${total_cost}!')
                    else:
                        print('Not enough money.')
            else:
                print('Not enough money or score.')