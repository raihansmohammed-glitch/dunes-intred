import json
import random
import os
import math
import time
import atexit
import threading
import socket

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

# Craftable items definitions
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

# Regular items
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
adminQanswers = ['31,10,2011', '31\x08\x811', '31/10/2011', '31.10.2011']
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