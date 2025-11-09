import sqlite3
import json
import random
import os
import math
import time
import atexit
import threading

# -------------------------
# Files & persistence
# -------------------------
USERS_FILE = "users.txt"  # Keep for compatibility but use SQLite
DUNGEON_TREASURE_FILE = "dungeon_treasure.json"

# -------------------------
# Globals
# -------------------------
dungeon_treasure = 0

AUTOSAVE_INTERVAL = 30  # Autosave every 30 seconds for simplicity
autosave_timer = None
last_autosave_time = time.time()

# -------------------------
# Permanent Upgrades
# -------------------------
PERM_UPGRADES = {
    "perm_strength_upgrade": {"name": "Perm Strength Upgrade", "atk_increase": 10},
    "perm_defense_upgrade": {"name": "Perm Defense Upgrade", "def_increase": 5},
    "perm_health_upgrade": {"name": "Perm Health Upgrade", "hp_increase": 10},
    "perm_mana_upgrade": {"name": "Perm Mana Upgrade", "magic_increase": 20},
    "perm_crit_chance_upgrade": {"name": "Perm Crit Chance Upgrade", "crit_chance_increase": 5},
    "perm_mana_regen_upgrade": {"name": "Perm Mana Regen Upgrade", "mana_regen_increase": 5},
    "perm_magic_def_upgrade": {"name": "Perm Magic Defense Upgrade", "magic_def_increase": 5},
    "perm_lifesteal_upgrade": {"name": "Perm Lifesteal Upgrade", "max_lifesteal_increase": 10},
    "perm_lifesteal_chance_upgrade": {"name": "Perm Lifesteal Chance Upgrade", "lifesteal_chance_increase": 5},
    "perm_exp_upgrade": {"name": "Perm Exp Upgrade", "exp_increase": 5},
}

# -------------------------
# Equipment: weapons, armors, wands, robes, necklaces
# -------------------------
WEAPONS = {
    "wooden_sword": {"name": "Wooden Sword", "atk": 2, "price": 50, "score_price": 0},
    "iron_sword": {"name": "Iron Sword", "atk": 5, "price": 150, "score_price": 0},
    "steel_sword": {"name": "Steel Sword", "atk": 8, "price": 300, "score_price": 0},
    "diamond_sword": {"name": "Diamond Sword", "atk": 50, "price": 2000, "score_price": 0},
    "void_sword": {"name": "Void Sword", "atk": 200, "price": 8000, "score_price": 0},
    "infinitium_sword": {"name": "Infinitium Sword", "atk": 2000, "price": 800000, "score_price": 25000},
    # New weapons
    "frostblade": {"name": "Frostblade", "atk": 120, "price": 5000, "score_price": 200},
    "flameblade": {"name": "Flameblade", "atk": 130, "price": 5500, "score_price": 250},
    "thunder_sword": {"name": "Thunder Sword", "atk": 150, "price": 7000, "score_price": 400},
    "holy_avenger": {"name": "Holy Avenger", "atk": 180, "price": 7500, "score_price": 800},
    "dragon_slayer": {"name": "Dragon Slayer", "atk": 250, "price": 15000, "score_price": 1500},
    "cosmic_blade": {"name": "Cosmic Blade", "atk": 500, "price": 30000, "score_price": 3000},
    "transcendent_edge": {"name": "Transcendent Edge", "atk": 1500, "price": 500000, "score_price": 10000},
}

ARMORS = {
    "leather_armor": {"name": "Leather Armor", "def": 1, "price": 50},
    "chainmail": {"name": "Chainmail", "def": 3, "price": 150},
    "plate_armor": {"name": "Plate Armor", "def": 6, "price": 300},
    "diamond_armor": {"name": "Diamond Armor", "def": 25, "price": 2000},
    "void_armor": {"name": "Void Armor", "def": 75, "price": 8000},
    "infinitium_armor": {"name": "Infinitium Armor", "def": 300, "price": 800000, "score_price": 2500},
    # New armors
    "frost_armor": {"name": "Frost Armor", "def": 40, "price": 4000, "score_price": 150},
    "flame_armor": {"name": "Flame Armor", "def": 45, "price": 4500, "score_price": 200},
    "thunder_armor": {"name": "Thunder Armor", "def": 55, "price": 6000, "score_price": 350},
    "holy_armor": {"name": "Holy Armor", "def": 70, "price": 9000, "score_price": 700},
    "dragon_scale_armor": {"name": "Dragon Scale Armor", "def": 100, "price": 14000, "score_price": 1400},
    "cosmic_armor": {"name": "Cosmic Armor", "def": 200, "price": 280000, "score_price": 2800},
    "transcendent_armor": {"name": "Transcendent Armor", "def": 500, "price": 950000, "score_price": 9500},
}

WANDS = {
    "apprentice_wand": {"name": "Apprentice Wand", "magic_atk": 5, "price": 120},
    "mage_wand": {"name": "Mage Wand", "magic_atk": 20, "price": 800},
    "archmage_staff": {"name": "Archmage Staff", "magic_atk": 120, "price": 12000, "score_price": 200},
    # New wands
    "frost_wand": {"name": "Frost Wand", "magic_atk": 60, "price": 4000, "score_price": 150},
    "flame_wand": {"name": "Flame Wand", "magic_atk": 65, "price": 4500, "score_price": 200},
    "thunder_wand": {"name": "Thunder Wand", "magic_atk": 75, "price": 6000, "score_price": 350},
    "holy_scepter": {"name": "Holy Scepter", "magic_atk": 90, "price": 9000, "score_price": 700},
    "dragon_staff": {"name": "Dragon Staff", "magic_atk": 125, "price": 14000, "score_price": 1400},
    "cosmic_scepter": {"name": "Cosmic Scepter", "magic_atk": 250, "price": 28000, "score_price": 2800},
    "transcendent_staff": {"name": "Transcendent Staff", "magic_atk": 750, "price": 95000, "score_price": 9500},
}

ROBES = {
    "cloth_robe": {"name": "Cloth Robe", "magic_def": 2, "price": 100},
    "silk_robe": {"name": "Silk Robe", "magic_def": 10, "price": 900},
    "void_robe": {"name": "Void Robe", "magic_def": 80, "price": 20000, "score_price": 500},
    # New robes
    "frost_robe": {"name": "Frost Robe", "magic_def": 30, "price": 4000, "score_price": 150},
    "flame_robe": {"name": "Flame Robe", "magic_def": 35, "price": 4500, "score_price": 200},
    "thunder_robe": {"name": "Thunder Robe", "magic_def": 45, "price": 6000, "score_price": 350},
    "holy_robe": {"name": "Holy Robe", "magic_def": 60, "price": 9000, "score_price": 700},
    "dragon_robe": {"name": "Dragon Robe", "magic_def": 90, "price": 14000, "score_price": 1400},
    "cosmic_robe": {"name": "Cosmic Robe", "magic_def": 180, "price": 28000, "score_price": 2800},
    "transcendent_robe": {"name": "Transcendent Robe", "magic_def": 450, "price": 95000, "score_price": 9500},
}

# New necklaces
NECKLACES = {
    "health_amulet": {"name": "Health Amulet", "hp_bonus": 20, "price": 500},
    "mana_amulet": {"name": "Mana Amulet", "mana_bonus": 15, "price": 600},
    "strength_amulet": {"name": "Strength Amulet", "atk_bonus": 5, "price": 700},
    "defense_amulet": {"name": "Defense Amulet", "def_bonus": 3, "price": 650},
    "crit_amulet": {"name": "Critical Amulet", "crit_bonus": 10, "price": 800},
    "lifesteal_amulet": {"name": "Lifesteal Amulet", "lifesteal_bonus": 5, "price": 900},
    "frost_necklace": {"name": "Frost Necklace", "magic_def_bonus": 15, "hp_bonus": 30, "price": 3000, "score_price": 100},
    "flame_necklace": {"name": "Flame Necklace", "magic_atk_bonus": 10, "atk_bonus": 8, "price": 3500, "score_price": 150},
    "thunder_necklace": {"name": "Thunder Necklace", "crit_bonus": 15, "atk_bonus": 10, "price": 5000, "score_price": 300},
    "holy_pendant": {"name": "Holy Pendant", "hp_bonus": 50, "mana_bonus": 30, "def_bonus": 5, "price": 8000, "score_price": 600},
    "dragon_necklace": {"name": "Dragon Necklace", "atk_bonus": 20, "def_bonus": 15, "hp_bonus": 70, "price": 12000, "score_price": 1200},
    "cosmic_necklace": {"name": "Cosmic Necklace", "magic_atk_bonus": 30, "magic_def_bonus": 25, "mana_bonus": 50, "price": 24000, "score_price": 2400},
    "transcendent_necklace": {"name": "Transcendent Necklace", "atk_bonus": 50, "def_bonus": 40, "hp_bonus": 150, "mana_bonus": 100, "crit_bonus": 20, "lifesteal_bonus": 10, "price": 800000, "score_price": 8000},
}

def get_rarity_value(rarity):
    """Get numerical value for rarity sorting"""
    rarity_order = {"common": 1, "rare": 2, "mythical": 3, "prismatic": 4, "divine": 5, "transcendent": 6}
    return rarity_order.get(rarity, 0)

# -------------------------
# Titles (with rarities and boosts)
# -------------------------
TITLES = {
    # Common Titles
    "novice": {"name": "Novice", "rarity": "common", "atk_boost": 0, "def_boost": 0, "hp_boost": 0, "mana_boost": 0, "exp_boost": 0, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "A beginner adventurer"},
    "apprentice": {"name": "Apprentice", "rarity": "common", "atk_boost": 1, "def_boost": 1, "hp_boost": 5, "mana_boost": 5, "exp_boost": 0, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "Learning the ways of combat"},
    "warrior": {"name": "Warrior", "rarity": "common", "atk_boost": 2, "def_boost": 2, "hp_boost": 10, "mana_boost": 0, "exp_boost": 0, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "A skilled fighter"},

    # Rare Titles
    "champion": {"name": "Champion", "rarity": "rare", "atk_boost": 3, "def_boost": 3, "hp_boost": 15, "mana_boost": 10, "exp_boost": 5, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "A true hero"},
    "legend": {"name": "Legend", "rarity": "rare", "atk_boost": 4, "def_boost": 4, "hp_boost": 20, "mana_boost": 15, "exp_boost": 10, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "Known throughout the lands"},
    "master": {"name": "Master", "rarity": "rare", "atk_boost": 5, "def_boost": 5, "hp_boost": 25, "mana_boost": 20, "exp_boost": 15, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "A master of their craft"},

    # Mythical Titles
    "grandmaster": {"name": "Grandmaster", "rarity": "mythical", "atk_boost": 6, "def_boost": 6, "hp_boost": 30, "mana_boost": 25, "exp_boost": 20, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "A supreme expert"},
    "slayer": {"name": "Slayer", "rarity": "mythical", "atk_boost": 7, "def_boost": 7, "hp_boost": 35, "mana_boost": 30, "exp_boost": 25, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 10, "def_percent": 5, "hp_percent": 0, "mana_percent": 0, "desc": "Monster slayer extraordinaire"},
    "hunter": {"name": "Hunter", "rarity": "mythical", "atk_boost": 8, "def_boost": 8, "hp_boost": 40, "mana_boost": 35, "exp_boost": 30, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 20, "def_percent": 10, "hp_percent": 0, "mana_percent": 0, "desc": "Master hunter"},

    # Prismatic Titles
    "slayer_ii": {"name": "Slayer II", "rarity": "prismatic", "atk_boost": 9, "def_boost": 9, "hp_boost": 45, "mana_boost": 40, "exp_boost": 35, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 25, "def_percent": 15, "hp_percent": 0, "mana_percent": 0, "desc": "Legendary monster slayer"},
    "boss_slayer": {"name": "Boss Slayer", "rarity": "prismatic", "atk_boost": 10, "def_boost": 10, "hp_boost": 50, "mana_boost": 45, "exp_boost": 40, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 30, "def_percent": 20, "hp_percent": 0, "mana_percent": 0, "desc": "Boss defeating champion"},
    "boss_master": {"name": "Boss Master", "rarity": "prismatic", "atk_boost": 11, "def_boost": 11, "hp_boost": 55, "mana_boost": 50, "exp_boost": 45, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 35, "def_percent": 25, "hp_percent": 0, "mana_percent": 0, "desc": "Master of bosses"},

    # Divine Titles
    "millionaire": {"name": "Millionaire", "rarity": "divine", "atk_boost": 12, "def_boost": 12, "hp_boost": 60, "mana_boost": 55, "exp_boost": 50, "material_discount_percent": 0, "money_boost_percent": 20, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "Extremely wealthy"},
    "arcane_master": {"name": "Arcane Master", "rarity": "divine", "atk_boost": 13, "def_boost": 13, "hp_boost": 65, "mana_boost": 60, "exp_boost": 55, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 10, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 20, "desc": "Master of magic"},
    "artisan": {"name": "Artisan", "rarity": "divine", "atk_boost": 14, "def_boost": 14, "hp_boost": 70, "mana_boost": 65, "exp_boost": 60, "material_discount_percent": 20, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "Master craftsman"},

    # Transcendent Titles
    "collector": {"name": "Collector", "rarity": "transcendent", "atk_boost": 15, "def_boost": 15, "hp_boost": 75, "mana_boost": 70, "exp_boost": 65, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 20, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "Ultimate collector"},
    "immortal": {"name": "Immortal", "rarity": "transcendent", "atk_boost": 16, "def_boost": 16, "hp_boost": 80, "mana_boost": 75, "exp_boost": 70, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": -30, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "Has cheated death many times"},
    "perfect": {"name": "Perfect", "rarity": "transcendent", "atk_boost": 17, "def_boost": 17, "hp_boost": 85, "mana_boost": 80, "exp_boost": 75, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 10, "def_percent": 10, "hp_percent": 20, "mana_percent": 20, "desc": "Achieved perfection"},
    "legendary": {"name": "Legendary", "rarity": "transcendent", "atk_boost": 18, "def_boost": 18, "hp_boost": 90, "mana_boost": 85, "exp_boost": 80, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 30, "def_percent": 30, "hp_percent": 20, "mana_percent": 0, "desc": "A living legend"},
    "deity": {"name": "Deity", "rarity": "transcendent", "atk_boost": 19, "def_boost": 19, "hp_boost": 95, "mana_boost": 90, "exp_boost": 85, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 40, "def_percent": 40, "hp_percent": 30, "mana_percent": 30, "desc": "God among men"},
    "treasure_king": {"name": "Treasure King", "rarity": "transcendent", "atk_boost": 20, "def_boost": 20, "hp_boost": 100, "mana_boost": 95, "exp_boost": 90, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 20, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "Master of treasures"},
    "fortunes_favorite": {"name": "Fortune's Favorite", "rarity": "transcendent", "atk_boost": 21, "def_boost": 21, "hp_boost": 105, "mana_boost": 100, "exp_boost": 95, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 20, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "Always lucky"},

    # Mythic Title (for level 90)
    "mytic": {"name": "Mythic", "rarity": "mythical", "atk_boost": 8, "def_boost": 8, "hp_boost": 40, "mana_boost": 35, "exp_boost": 30, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "Mythical being"},

    # Transcendent Title (for level 99)
    "transcendent": {"name": "Transcendent", "rarity": "transcendent", "atk_boost": 15, "def_boost": 15, "hp_boost": 75, "mana_boost": 70, "exp_boost": 65, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "Beyond mortal limits"},

    # Godlike Title (for level 100)
    "godlike": {"name": "Godlike", "rarity": "transcendent", "atk_boost": 22, "def_boost": 22, "hp_boost": 110, "mana_boost": 105, "exp_boost": 100, "material_discount_percent": 0, "money_boost_percent": 0, "material_boost_percent": 0, "treasure_boost_percent": 0, "crit_chance_percent": 0, "death_penalty_percent": 0, "hp_regen_percent": 0, "atk_percent": 0, "def_percent": 0, "hp_percent": 0, "mana_percent": 0, "desc": "A god among mortals"},
}

# -------------------------
# Achievement System
# -------------------------
ACHIEVEMENTS = {
    "first_monster": {
        "name": "First Blood",
        "title": "Slayer",
        "condition": lambda stats: stats.get("monsters_defeated", 0) >= 1,
        "desc": "Defeat 1 monster"
    },
    "hundred_monsters": {
        "name": "Monster Hunter",
        "title": "Hunter",
        "condition": lambda stats: stats.get("monsters_defeated", 0) >= 100,
        "desc": "Defeat 100 monsters"
    },
    "thousand_monsters": {
        "name": "Monster Slayer",
        "title": "Slayer II",
        "condition": lambda stats: stats.get("monsters_defeated", 0) >= 1000,
        "desc": "Defeat 1000 monsters"
    },
    "boss_defeats_10": {
        "name": "Boss Hunter",
        "title": "Boss Slayer",
        "condition": lambda stats: stats.get("bosses_defeated", 0) >= 10,
        "desc": "Defeat 10 bosses"
    },
    "boss_defeats_50": {
        "name": "Boss Master",
        "title": "Boss Master",
        "condition": lambda stats: stats.get("bosses_defeated", 0) >= 50,
        "desc": "Defeat 50 bosses"
    },
    "millionaire": {
        "name": "Wealthy",
        "title": "Millionaire",
        "condition": lambda stats: stats.get("total_money_earned", 0) >= 1000000,
        "desc": "Earn 1,000,000 total money"
    },
    "spell_master": {
        "name": "Spellcaster",
        "title": "Arcane Master",
        "condition": lambda stats: len(stats.get("learned_spells", [])) >= 10,
        "desc": "Learn 10 spells"
    },
    "crafting_expert": {
        "name": "Craftsman",
        "title": "Artisan",
        "condition": lambda stats: stats.get("items_crafted", 0) >= 50,
        "desc": "Craft 50 items"
    },
    "collector": {
        "name": "Collector",
        "title": "Collector",
        "condition": lambda stats: stats.get("materials_collected", 0) >= 500,
        "desc": "Collect 500 materials"
    },
    "survivor": {
        "name": "Survivor",
        "title": "Immortal",
        "condition": lambda stats: stats.get("times_died", 0) >= 100,
        "desc": "Die 100 times"
    },
    "perfectionist": {
        "name": "Perfect Game",
        "title": "Perfect",
        "condition": lambda stats: (stats.get("monsters_defeated", 0) >= 1000 and
        stats.get("bosses_defeated", 0) >= 10 and
        len(stats.get("learned_spells", [])) >= 5 and
        stats.get("level", 1) >= 50),
        "desc": "Defeat 1000 monsters, 10 bosses, learn 5 spells, reach level 50"
    },
    "legendary": {
        "name": "Legendary Adventurer",
        "title": "Legendary",
        "condition": lambda stats: (stats.get("monsters_defeated", 0) >= 5000 and
        stats.get("bosses_defeated", 0) >= 100 and
        stats.get("level", 1) >= 80),
        "desc": "Defeat 5000 monsters, 100 bosses, reach level 80"
    },
    "godlike": {
        "name": "God Among Men",
        "title": "Deity",
        "condition": lambda stats: (stats.get("monsters_defeated", 0) >= 10000 and
        stats.get("bosses_defeated", 0) >= 200 and
        stats.get("level", 1) >= 100),
        "desc": "Defeat 10000 monsters, 200 bosses, reach level 100"
    },
    "treasure_hunter": {
        "name": "Treasure Hunter",
        "title": "Treasure King",
        "condition": lambda stats: stats.get("dungeon_treasure_collected", 0) >= 500000,
        "desc": "Collect 500,000 from dungeon treasure"
    },
    "lucky": {
        "name": "Lucky",
        "title": "Fortune's Favorite",
        "condition": lambda stats: stats.get("critical_hits", 0) >= 1000,
        "desc": "Land 1000 critical hits"
    }
}

# -------------------------
# Title System (combines level and achievements)
# -------------------------
def get_title(level, achievements=None):
    if achievements is None:
        achievements = []

    # Level-based titles (base)
    level_title = "Novice"
    if level <= 10:
        level_title = "Novice"
    elif level <= 20:
        level_title = "Apprentice"
    elif level <= 30:
        level_title = "Warrior"
    elif level <= 40:
        level_title = "Champion"
    elif level <= 50:
        level_title = "Hero"
    elif level <= 60:
        level_title = "Legend"
    elif level <= 70:
        level_title = "Master"
    elif level <= 80:
        level_title = "Grandmaster"
    elif level <= 90:
        level_title = "Mythic"
    elif level <= 99:
        level_title = "Transcendent"
    else:  # level 100
        level_title = "Godlike"

    # Achievement-based titles (override level titles if better)
    best_achievement_title = None
    for ach_key in achievements:
        if ach_key in ACHIEVEMENTS:
            ach_title = ACHIEVEMENTS[ach_key]["title"]
            # Priority order for achievement titles
            title_priority = {
                "Slayer": 1, "Hunter": 2, "Slayer II": 3, "Boss Slayer": 4, "Boss Master": 5,
                "Millionaire": 6, "Arcane Master": 7, "Artisan": 8, "Collector": 9,
                "Immortal": 10, "Perfect": 11, "Legendary": 12, "Deity": 13,
                "Treasure King": 14, "Fortune's Favorite": 15
            }
            if best_achievement_title is None or title_priority.get(ach_title, 0) > title_priority.get(best_achievement_title, 0):
                best_achievement_title = ach_title

    return best_achievement_title if best_achievement_title else level_title

def check_achievements(username):
    """Check and unlock achievements for a user"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if not result:
        conn.close()
        return []

    player_data = json.loads(result[0])
    stats = player_data.get("stats", {})
    unlocked = stats.get("achievements", [])
    new_achievements = []

    for ach_key, achievement in ACHIEVEMENTS.items():
        if ach_key not in unlocked and achievement["condition"](stats):
            unlocked.append(ach_key)
            new_achievements.append(ach_key)
            print(f"🏆 Achievement Unlocked: {achievement['name']} - '{achievement['title']}'!")
            print(f" {achievement['desc']}")

    if new_achievements:
        stats["achievements"] = unlocked
        # Update title if new achievement gives better title
        old_title = stats.get("title")
        new_title = get_title(stats.get("level", 1), unlocked)
        if new_title != old_title:
            stats["title"] = new_title
            if new_title not in stats.get("available_titles", []):
                stats["available_titles"].append(new_title)
            print(f"🎉 New title unlocked: '{new_title}'!")

        player_data["stats"] = stats
        c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), username))
        conn.commit()

    conn.close()
    return new_achievements

# -------------------------
# XP / Leveling system
# -------------------------
MAX_LEVEL = 100
AREAS_COUNT = 10
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
    # Improved exp curve
    base_exp = 100
    growth_factor = 1.15
    return int(base_exp * (level ** 1.5) * (growth_factor ** (level - 1)))

def create_exp_bar(current_exp, next_exp):
    if next_exp == "MAX":
        return "[██████████] MAX LEVEL"
    bar_length = 10
    if next_exp > 0:
        progress = min(current_exp / next_exp, 1.0)
        filled = int(progress * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        percentage = int(progress * 100)
        return f"[{bar}] {percentage}%"
    return "[░░░░░░░░░░] 0%"

def grant_exp(username, amount):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if not result:
        conn.close()
        return []

    player_data = json.loads(result[0])
    stats = player_data["stats"]
    lvls_gained = []
    if stats.get("level", 1) >= MAX_LEVEL:
        conn.close()
        return lvls_gained

    # Apply experience boost if available
    exp_boost = stats.get("perm_exp_boost", 0)
    title_exp_boost = stats.get("title_exp_boost", 0)
    total_exp_boost = exp_boost + title_exp_boost
    if total_exp_boost > 0:
        boosted_amount = amount * (total_exp_boost / 100.0)
        print(f"Experience boost applied! +{boosted_amount:.1f} bonus EXP")
        amount += boosted_amount

    stats["exp"] = stats.get("exp", 0) + amount
    old_title = stats.get("title")
    while stats["level"] < MAX_LEVEL and stats["exp"] >= exp_to_next(stats["level"]):
        req = exp_to_next(stats["level"])
        stats["exp"] -= req
        old_level = stats["level"]
        stats["level"] += 1

        # Improved stat gains per level
        hp_increase = 10 + stats["level"] // 2
        atk_increase = 1 + stats["level"] // 5
        mana_increase = 5 + stats["level"] // 3

        # Check if stats were manually set below default
        default_stats = default_player_data()["stats"]

        # Handle HP
        if not stats["stats_manually_set"]["hp_max"]:
            stats["hp_max"] = stats.get("hp_max", 100) + hp_increase
        if not stats["stats_manually_set"]["hp"]:
            stats["hp"] = min(stats.get("hp", stats["hp_max"]) + stats["hp_max"] // 4, stats["hp_max"])

        # Handle ATK
        if not stats["stats_manually_set"]["atk"]:
            stats["atk"] = stats.get("atk", 5) + atk_increase

        # Handle Mana
        if not stats["stats_manually_set"]["mana_max"]:
            stats["mana_max"] = stats.get("mana_max", 50) + mana_increase
        if not stats["stats_manually_set"]["mana"]:
            stats["mana"] = min(stats.get("mana", stats["mana_max"]) + stats["mana_max"] // 3, stats["mana_max"])

        # Handle DEF
        if not stats["stats_manually_set"]["defense"]:
            stats["defense"] = stats.get("defense", 0) + 1

        lvls_gained.append(stats["level"])

        # Apply permanent upgrades after level up
        apply_permanent_upgrades(username)

        # Reload user data after applying upgrades
        c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
        result = c.fetchone()
        if result:
            player_data = json.loads(result[0])
            stats = player_data["stats"]

        # Update title if level changed
        new_title = get_title(stats["level"], stats.get("achievements", []))
        if new_title != old_title:
            stats["title"] = new_title

        # Check for new achievements after leveling up
        check_achievements(username)

        player_data["stats"] = stats
        c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), username))
        conn.commit()

    auto_equip_items(username)
    conn.close()
    return lvls_gained

# -------------------------
# Dungeon treasure persistence (SQLite-based now, but keep global for compatibility)
# -------------------------
def load_dungeon_treasure():
    global dungeon_treasure
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Create table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS dungeon_treasure (
        id INTEGER PRIMARY KEY,
        treasure INTEGER DEFAULT 0
    )''')
    c.execute('SELECT treasure FROM dungeon_treasure WHERE id = 1')
    result = c.fetchone()
    if result:
        dungeon_treasure = int(result[0])
    else:
        dungeon_treasure = random.randint(200000, 1000000)
        c.execute('INSERT INTO dungeon_treasure (id, treasure) VALUES (1, ?)', (dungeon_treasure,))
        conn.commit()

    # If dungeon treasure is below 200,000, reroll to between 200,000 and 1,000,000
    if dungeon_treasure < 200000:
        dungeon_treasure = random.randint(200000, 1000000)
        save_dungeon_treasure()

    conn.close()

def save_dungeon_treasure():
    global dungeon_treasure
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE dungeon_treasure SET treasure = ? WHERE id = 1', (int(dungeon_treasure),))
    conn.commit()
    conn.close()
    return True

load_dungeon_treasure()

# -------------------------
# Autosave functions
# -------------------------
def save_all_data():
    treasure_saved = save_dungeon_treasure()
    return treasure_saved

def autosave():
    """Perform autosave and show a brief notification"""
    global last_autosave_time

    if save_all_data():
        last_autosave_time = time.time()
        print("\n💾 Game auto-saved!")
    else:
        print("\n⚠️ Autosave failed! Check console for details.")

def schedule_autosave():
    """Schedule the next autosave"""
    global autosave_timer

    # Cancel any existing timer
    if autosave_timer is not None:
        autosave_timer.cancel()

    # Create a new timer
    autosave_timer = threading.Timer(AUTOSAVE_INTERVAL, autosave)
    autosave_timer.daemon = True  # Allows program to exit even if timer is running
    autosave_timer.start()

def stop_autosave():
    """Stop the autosave timer"""
    global autosave_timer

    if autosave_timer is not None:
        autosave_timer.cancel()
        autosave_timer = None

# -------------------------
# Save & Load functions (SQLite-based)
# -------------------------
def save_users():
    # This function is now a no-op since we save to SQLite directly
    return True

def setup_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        money INTEGER DEFAULT 40,
        player_data TEXT
    )''')
    # Ensure money column exists (for backward compatibility)
    try:
        c.execute('ALTER TABLE users ADD COLUMN money INTEGER DEFAULT 40')
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.commit()
    conn.close()

def signup(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password, player_data) VALUES (?, ?, ?)',
                  (username, password, json.dumps(default_player_data())))
        conn.commit()
        print("Signup successful!")
        return True
    except sqlite3.IntegrityError:
        print("Username already exists!")
        return False
    finally:
        conn.close()

def signin(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password, score, money, player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    if result and result[0] == password:
        return result[1], result[2], json.loads(result[3])
    else:
        return None, None, None

def update_user(username, score, money, player_data):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET score = ?, money = ?, player_data = ? WHERE username = ?',
              (score, money, json.dumps(player_data), username))
    conn.commit()
    conn.close()

def default_player_data():
    inv = {
        "potion": 1,
        "strong_potion": 0,
        "ultra_potion": 0,
        "strength_boost": 0,
        "defense_boost": 0,
        "regen_potion": 0,
        "crit_boost": 0,
        # Starting equipment
        "wooden_sword": 1,
        "leather_armor": 1,
        # mana items
        "mana_upgrade_potion": 0,
        "mana_regen_potion": 0,
        "instant_mana": 0,
        # materials
        "slime_gel": 0,
        "goblin_tooth": 0,
        "wolf_pelt": 0,
        "skeleton_bone": 0,
        "orc_iron": 0,
        "bandit_cloth": 0,
        "troll_core": 0,
        "dark_essence": 0,
        "prism_fragment": 0,
        "void_fragment": 0,
        "infinitium_piece": 0,
        "soul_shard": 0,
        "transcendent_heart": 0,
        # New materials
        "dragon_scale": 0,
        "phoenix_feather": 0,
        "frozen_heart": 0,
        "thunder_core": 0,
        "holy_light": 0,
        "demon_horn": 0,
        "crystal_shard": 0,
        "star_dust": 0,
        "moon_rock": 0,
        "sun_stone": 0,
        # magic packs
        "common_magic_pack": 0,
        "rare_magic_pack": 0,
        "mythical_magic_pack": 0,
        "prismatic_magic_pack": 0,
        "divine_magic_pack": 0,
        "transcendent_magic_pack": 0,
        # permanent upgrades
        "perm_strength_upgrade": 0,
        "perm_defense_upgrade": 0,
        "perm_health_upgrade": 0,
        "perm_mana_upgrade": 0,
        "perm_crit_chance_upgrade": 0,
        "perm_mana_regen_upgrade": 0,
        "perm_lifesteal_upgrade": 0,
        "perm_lifesteal_chance_upgrade": 0,
        "perm_magic_def_upgrade": 0,
        "perm_exp_upgrade": 0,
    }
    return {
        "money": 40,
        "stats": {
            "hp_max": 100,
            "hp": 100,
            "atk": 5,
            "defense": 0,
            "level": 1,
            "exp": 0,
            "mana_max": 50,
            "mana": 50,
            "current_area": 1,
            "equipped": {"weapon": None, "armor": None, "wand": None, "robe": None, "necklace": None},
            "settings": {"call_including_title": True, "show_exp_bar": False, "auto_equip_best": False, "auto_equip_spells": False, "auto_equip_titles": False, "auto_equip_everything": False},
            # Permanent upgrade stats
            "perm_atk": 0,
            "perm_def": 0,
            "perm_hp_max": 0,
            "perm_mana_max": 0,
            "perm_magic_def": 0,
            "perm_crit_chance": 0,
            "perm_mana_regen": 0,
            "perm_lifesteal": 0,
            "perm_lifesteal_chance": 0,
            "perm_exp_boost": 0,
            "title": get_title(1),
            # Achievement tracking
            "achievements": [],
            "monsters_defeated": 0,
            "bosses_defeated": 0,
            "total_money_earned": 0,
            "items_crafted": 0,
            "materials_collected": 0,
            "times_died": 0,
            "dungeon_treasure_collected": 0,
            "critical_hits": 0,
            "battle_logs": [],
            # Track if stats were manually set below default
            "stats_manually_set": {
                "hp": False,
                "hp_max": False,
                "atk": False,
                "defense": False,
                "mana": False,
                "mana_max": False,
            },
            # Magic and Title systems
            "learned_spells": [],
            "equipped_spells": [None, None, None, None],
            "available_titles": [],
            "equipped_titles": [None, None, None, None, None],
            # Title boost tracking
            "title_atk_boost": 0,
            "title_def_boost": 0,
            "title_hp_boost": 0,
            "title_mana_boost": 0,
            "title_exp_boost": 0,
        },
        "inventory": inv
    }
def choose_monster_for_area(area):
    # Filter monsters by area
    area_monsters = [m for m in monsters if m.get("area", area) == area and not m["is_boss"]]
    if not area_monsters:
        # Fallback to any non-boss monster
        area_monsters = [m for m in monsters if not m["is_boss"]]

    weights = [m.get("weight", 1) for m in area_monsters]
    chosen = random.choices(area_monsters, weights=weights, k=1)[0].copy()

    # Ensure atk_min and atk_max exist (some monsters have magic_atk_min instead)
    if "atk_min" not in chosen:
        chosen["atk_min"] = chosen.get("magic_atk_min", 1)
    if "atk_max" not in chosen:
        chosen["atk_max"] = chosen.get("magic_atk_max", chosen["atk_min"])

    # Scale monster stats based on area
    scale = 1.0 + (area - 1) * 0.15
    chosen["hp"] = max(1, int(chosen.get("hp", 1) * scale))
    chosen["atk_min"] = max(1, int(chosen.get("atk_min", 1) * scale))
    chosen["atk_max"] = max(chosen["atk_min"], int(chosen.get("atk_max", chosen["atk_min"]) * scale))
    chosen["money_min"] = int(chosen.get("money_min", 1) * (1 + (area - 1) * 0.3))
    chosen["money_max"] = int(chosen.get("money_max", chosen["money_min"]) * (1 + (area - 1) * 0.3))
    return chosen

def choose_boss_for_area(area):
    # Filter bosses by area
    area_bosses = [m for m in monsters if m.get("area", area) == area and m["is_boss"]]
    if not area_bosses:
        # Fallback to any boss
        area_bosses = [m for m in monsters if m["is_boss"]]

    weights = [m.get("weight", 1) for m in area_bosses]
    chosen = random.choices(area_bosses, weights=weights, k=1)[0].copy()

    # Ensure atk_min and atk_max exist (some bosses have magic_atk_min instead)
    if "atk_min" not in chosen:
        chosen["atk_min"] = chosen.get("magic_atk_min", 1)
    if "atk_max" not in chosen:
        chosen["atk_max"] = chosen.get("magic_atk_max", chosen["atk_min"])

    # Scale boss stats based on area
    scale = 1.0 + (area - 1) * 0.1
    chosen["hp"] = max(1, int(chosen.get("hp", 1) * scale))
    chosen["atk_min"] = max(1, int(chosen.get("atk_min", 1) * scale))
    chosen["atk_max"] = max(chosen["atk_min"], int(chosen.get("atk_max", chosen["atk_min"]) * scale))
    chosen["money_min"] = int(chosen.get("money_min", 1) * (1 + (area - 1) * 0.2))
    chosen["money_max"] = int(chosen.get("money_max", chosen["money_min"]) * (1 + (area - 1) * 0.2))
    return chosen

def get_boss_template():
    return next(m for m in monsters if m["is_boss"])

def apply_damage_with_defense(damage, defense):
    reduced = damage - defense
    return reduced if reduced >= 1 else 1

MONSTERS = {
    "slime": {"name": "Slime", "hp": 10, "atk": 2, "def": 0, "exp": 5, "gold": 5, "materials": ["slime_gel"]},
    "goblin": {"name": "Goblin", "hp": 15, "atk": 4, "def": 1, "exp": 8, "gold": 8, "materials": ["goblin_tooth"]},
    "orc": {"name": "Orc", "hp": 25, "atk": 6, "def": 2, "exp": 12, "gold": 12, "materials": ["orc_iron"]},
    "wolf": {"name": "Wolf", "hp": 20, "atk": 7, "def": 1, "exp": 10, "gold": 10, "materials": ["wolf_pelt"]},
    "skeleton": {"name": "Skeleton", "hp": 30, "atk": 8, "def": 3, "exp": 15, "gold": 15, "materials": ["skeleton_bone"]},
    "bandit": {"name": "Bandit", "hp": 35, "atk": 9, "def": 4, "exp": 18, "gold": 18, "materials": ["bandit_cloth"]},
    "troll": {"name": "Troll", "hp": 50, "atk": 12, "def": 6, "exp": 25, "gold": 25, "materials": ["troll_core"]},
    "shadow_beast": {"name": "Shadow Beast", "hp": 45, "atk": 14, "def": 5, "exp": 22, "gold": 22, "materials": ["dark_essence"]},
    "dark_knight": {"name": "Dark Knight", "hp": 70, "atk": 18, "def": 8, "exp": 35, "gold": 35, "materials": ["prism_fragment"]},
    "necromancer": {"name": "Necromancer", "hp": 60, "atk": 16, "def": 7, "exp": 30, "gold": 30, "materials": ["void_fragment"]},
    "dragon_whelp": {"name": "Dragon Whelp", "hp": 80, "atk": 22, "def": 10, "exp": 40, "gold": 40, "materials": ["dragon_scale"]},
    "frost_giant": {"name": "Frost Giant", "hp": 90, "atk": 20, "def": 12, "exp": 45, "gold": 45, "materials": ["frozen_heart"]},
    "void_creature": {"name": "Void Creature", "hp": 100, "atk": 25, "def": 15, "exp": 50, "gold": 50, "materials": ["thunder_core"]},
    "phoenix": {"name": "Phoenix", "hp": 85, "atk": 28, "def": 14, "exp": 48, "gold": 48, "materials": ["phoenix_feather"]},
    "prism_guardian": {"name": "Prism Guardian", "hp": 120, "atk": 30, "def": 18, "exp": 60, "gold": 60, "materials": ["holy_light"]},
    "demon_lord": {"name": "Demon Lord", "hp": 110, "atk": 32, "def": 20, "exp": 65, "gold": 65, "materials": ["demon_horn"]},
    "celestial_beast": {"name": "Celestial Beast", "hp": 150, "atk": 35, "def": 25, "exp": 75, "gold": 75, "materials": ["crystal_shard"]},
    "ancient_dragon": {"name": "Ancient Dragon", "hp": 140, "atk": 38, "def": 28, "exp": 80, "gold": 80, "materials": ["star_dust"]},
    "god_of_dungeons": {"name": "God of Dungeons", "hp": 200, "atk": 50, "def": 30, "exp": 100, "gold": 100, "materials": ["moon_rock", "sun_stone"]}
}

BOSSES = {
    "boss_slime": {"name": "King Slime", "hp": 100, "atk": 20, "def": 10, "exp": 100, "gold": 200, "materials": ["slime_gel", "prism_fragment"]},
    "boss_goblin": {"name": "Goblin King", "hp": 150, "atk": 25, "def": 12, "exp": 150, "gold": 300, "materials": ["goblin_tooth", "orc_iron"]},
    "boss_orc": {"name": "Orc Warlord", "hp": 200, "atk": 30, "def": 15, "exp": 200, "gold": 400, "materials": ["orc_iron", "troll_core"]},
    "boss_wolf": {"name": "Alpha Wolf", "hp": 180, "atk": 28, "def": 14, "exp": 180, "gold": 360, "materials": ["wolf_pelt", "dark_essence"]},
    "boss_skeleton": {"name": "Lich Lord", "hp": 250, "atk": 35, "def": 18, "exp": 250, "gold": 500, "materials": ["skeleton_bone", "void_fragment"]},
    "boss_bandit": {"name": "Bandit Chief", "hp": 220, "atk": 32, "def": 16, "exp": 220, "gold": 440, "materials": ["bandit_cloth", "prism_fragment"]},
    "boss_troll": {"name": "Troll King", "hp": 300, "atk": 40, "def": 20, "exp": 300, "gold": 600, "materials": ["troll_core", "dragon_scale"]},
    "boss_shadow_beast": {"name": "Shadow Lord", "hp": 280, "atk": 38, "def": 19, "exp": 280, "gold": 560, "materials": ["dark_essence", "frozen_heart"]},
    "boss_dark_knight": {"name": "Death Knight", "hp": 350, "atk": 45, "def": 22, "exp": 350, "gold": 700, "materials": ["prism_fragment", "thunder_core"]},
    "boss_necromancer": {"name": "Arch Necromancer", "hp": 320, "atk": 42, "def": 21, "exp": 320, "gold": 640, "materials": ["void_fragment", "phoenix_feather"]},
    "boss_dragon_whelp": {"name": "Young Dragon", "hp": 400, "atk": 50, "def": 25, "exp": 400, "gold": 800, "materials": ["dragon_scale", "holy_light"]},
    "boss_frost_giant": {"name": "Frost Titan", "hp": 380, "atk": 48, "def": 24, "exp": 380, "gold": 760, "materials": ["frozen_heart", "demon_horn"]},
    "boss_void_creature": {"name": "Void Lord", "hp": 450, "atk": 55, "def": 27, "exp": 450, "gold": 900, "materials": ["thunder_core", "crystal_shard"]},
    "boss_phoenix": {"name": "Phoenix Lord", "hp": 420, "atk": 52, "def": 26, "exp": 420, "gold": 840, "materials": ["phoenix_feather", "star_dust"]},
    "boss_prism_guardian": {"name": "Prism Warden", "hp": 500, "atk": 60, "def": 30, "exp": 500, "gold": 1000, "materials": ["holy_light", "moon_rock"]},
    "boss_demon_lord": {"name": "Demon Overlord", "hp": 480, "atk": 58, "def": 29, "exp": 480, "gold": 960, "materials": ["demon_horn", "sun_stone"]},
    "boss_celestial_beast": {"name": "Celestial Guardian", "hp": 550, "atk": 65, "def": 32, "exp": 550, "gold": 1100, "materials": ["crystal_shard", "transcendent_heart"]},
    "boss_ancient_dragon": {"name": "Elder Dragon", "hp": 520, "atk": 62, "def": 31, "exp": 520, "gold": 1040, "materials": ["star_dust", "soul_shard"]},
    "boss_god_of_dungeons": {"name": "Supreme Dungeon God", "hp": 600, "atk": 70, "def": 35, "exp": 600, "gold": 1200, "materials": ["moon_rock", "sun_stone", "transcendent_heart", "soul_shard"]}
}

# Define monsters list with required fields
monsters = []
for k, v in MONSTERS.items():
    v_copy = v.copy()
    v_copy["is_boss"] = False
    v_copy["area"] = 1
    v_copy["weight"] = 1
    monsters.append(v_copy)
for k, v in BOSSES.items():
    v_copy = v.copy()
    v_copy["is_boss"] = True
    v_copy["area"] = 1
    v_copy["weight"] = 1
    monsters.append(v_copy)

def get_leaderboard():
    """Get leaderboard from SQLite database"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, score FROM users ORDER BY score DESC LIMIT 10')
    results = c.fetchall()
    conn.close()
    return results

def guessing_game(current_user, score):
    number = random.randint(1, 100)
    attempts = 0
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    while True:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1
            if guess < number:
                print("Too low!")
            elif guess > number:
                print("Too high!")
            else:
                print(f"Correct! You guessed it in {attempts} attempts.")
                score += max(0, 10 - attempts)  # Simple scoring: bonus for fewer attempts
                print(f"Score updated. New score: {score}")
                return score
        except ValueError:
            print("Please enter a valid number.")
def combat(username, monster_key, is_boss=False):
    """
    Basic combat function for dungeon battles.
    Returns (victory: bool, exp_gained: int, gold_gained: int, materials_gained: list)
    """
    if not any(user[0] == username for user in get_leaderboard()):  # Simple user check
        return False, 0, 0, []

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if not result:
        conn.close()
        return False, 0, 0, []

    player_data = json.loads(result[0])
    stats = player_data["stats"]
    inventory = player_data.get("inventory", {})

    # Ensure user fields are normalized before combat
    ensure_user_fields(username)

    # Reload after normalization
    c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    player_data = json.loads(result[0])
    stats = player_data["stats"]
    inventory = player_data.get("inventory", {})

    # Get monster data
    monster_dict = BOSSES if is_boss else MONSTERS
    if monster_key not in monster_dict:
        conn.close()
        return False, 0, 0, []

    monster = monster_dict[monster_key]

    # Calculate player effective stats (including equipment and titles)
    player_hp = stats["hp"]
    player_atk = stats["atk"] + stats.get("title_atk_boost", 0)
    player_def = stats["defense"] + stats.get("title_def_boost", 0)
    player_magic_def = stats.get("perm_magic_def", 0)

    # Equipment bonuses
    equipped = stats.get("equipped", {})
    if equipped.get("weapon") and equipped["weapon"] in WEAPONS:
        player_atk += WEAPONS[equipped["weapon"]]["atk"]
    if equipped.get("armor") and equipped["armor"] in ARMORS:
        player_def += ARMORS[equipped["armor"]]["def"]
    if equipped.get("necklace") and equipped["necklace"] in NECKLACES:
        player_atk += NECKLACES[equipped["necklace"]].get("atk_bonus", 0)
        player_def += NECKLACES[equipped["necklace"]].get("def_bonus", 0)
        player_hp += NECKLACES[equipped["necklace"]].get("hp_bonus", 0)

    monster_hp = monster["hp"]
    monster_atk = monster["atk"]
    monster_def = monster["def"]

    print(f"\n⚔️  Battle: {stats.get('title', 'Adventurer')} vs {monster['name']}!")
    print(f"Your HP: {player_hp} | ATK: {player_atk} | DEF: {player_def}")
    print(f"{monster['name']}'s HP: {monster_hp} | ATK: {monster_atk} | DEF: {monster_def}")

    # Simple turn-based combat
    while player_hp > 0 and monster_hp > 0:
        # Player turn
        damage_to_monster = max(1, player_atk - monster_def)
        monster_hp -= damage_to_monster
        print(f"You deal {damage_to_monster} damage! {monster['name']} HP: {max(0, monster_hp)}")

        if monster_hp <= 0:
            break

        # Monster turn
        damage_to_player = max(1, monster_atk - player_def)
        player_hp -= damage_to_player
        print(f"{monster['name']} deals {damage_to_player} damage! Your HP: {max(0, player_hp)}")

        if player_hp <= 0:
            break

        # For simplicity, no player choice - auto attack
        pass

    victory = player_hp > 0

    if victory:
        exp_gained = monster["exp"]
        gold_gained = monster["gold"]
        materials_gained = monster["materials"][:]  # Copy list

        print(f"\n🎉 Victory! You defeated {monster['name']}!")
        print(f"Gained {exp_gained} EXP, {gold_gained} gold, and materials: {', '.join(materials_gained)}")

        # Grant EXP
        lvls_gained = grant_exp(username, exp_gained)

        # Add gold
        player_data["money"] += gold_gained

        # Add materials
        for mat in materials_gained:
            inventory[mat] = inventory.get(mat, 0) + 1

        # Update battle stats
        stats["monsters_defeated"] = stats.get("monsters_defeated", 0) + 1
        if is_boss:
            stats["bosses_defeated"] = stats.get("bosses_defeated", 0) + 1

        player_data["inventory"] = inventory
        player_data["stats"] = stats
        c.execute('UPDATE users SET player_data = ?, money = ? WHERE username = ?',
                  (json.dumps(player_data), player_data["money"], username))
        conn.commit()

        # Auto equip if enabled
        auto_equip_items(username)

        # Check achievements
        check_achievements(username)

    else:
        print(f"\n💀 Defeat! You were defeated by {monster['name']}.")
        # Death penalty: lose some gold
        gold_lost = min(player_data["money"] // 10, 100)  # Lose 10% or 100, whichever is less
        player_data["money"] -= gold_lost
        player_data["money"] = max(0, player_data["money"])

        # Update death stats
        stats["times_died"] = stats.get("times_died", 0) + 1

        player_data["stats"] = stats
        c.execute('UPDATE users SET player_data = ?, money = ? WHERE username = ?',
                  (json.dumps(player_data), player_data["money"], username))
        conn.commit()

        if gold_lost > 0:
            print(f"You lost {gold_lost} gold due to death penalty.")

    conn.close()
    return victory, exp_gained if victory else 0, gold_gained if victory else 0, materials_gained if victory else []
    """Get leaderboard from SQLite database"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, score FROM users ORDER BY score DESC LIMIT 10')
    results = c.fetchall()
    conn.close()
    return results

# -------------------------
# Dungeon game function (needed for main menu)
# -------------------------
# Debug Console
# -------------------------
def debug_console(current_user, score, money, player_data, users_db_path='users.db'):
    conn = sqlite3.connect(users_db_path)
    c = conn.cursor()
    print("\n--- Debug Console --- (Type 'help' for commands)")
    while True:
        cmd = input("Debug> ").strip().lower().split(" ", 1)
        cmd_base = cmd[0] if cmd else ""
        args = cmd[1] if len(cmd) > 1 else ""

        if cmd_base == "help" or cmd_base == "h" or cmd_base == "?":
            print("\n--- Debug Commands ---")
            print("users - display all registered users (limited info)")
            print("current - display current user and score")
            print("numbers - display generated random numbers (if any)")
            print("adduser <u> <p> - create a new user account with password")
            print("deluser <u> - delete a user account")
            print("reset - reset all users and highscores")
            print("resetplayer <u> - reset a single user to default stats")
            print("setdmoney <n> - set dungeon treasure amount to n")
            print("setscore <u> <n> - set a user's score to n")
            print("setmoney <u> <n> - set a user's money to n")
            print("setexp <u> <n> - set a user's experience to n")
            print("setlvl <u> <n> - set a user's level to n")
            print("setdefeated <u> <type> <n> - set defeated count for type (monsters, bosses, etc.)")
            print("set <u> <stat> <n> - set a user's stat to n (hp, mana, atk, def, etc.)")
            print("showfull <u> - display full data for user u")
            print("give <u> <item> [qty] - grant an item to user (saves automatically)")
            print(" (items: potion, strong_potion, ultra_potion, etc.)")
            print(" (upgrades: perm_strength_upgrade, perm_defense_upgrade, etc.)")
            print(" (aliases: str, def, hp, mana, crit, etc.)")
            print("ruinthefun <u> - grant all achievements, items (500x usable), max stats")
            print("exit - close debug console")
            print("-----------------------\n")
        elif cmd_base == "users" or cmd_base == "usrs" or cmd_base == "u":
            c.execute('SELECT username, score, money FROM users ORDER BY score DESC LIMIT 10')
            results = c.fetchall()
            print("\n--- Top 10 Users ---")
            for uname, uscore, umoney in results:
                print(f"{uname}: Score {uscore}, Money ${umoney}")
            print("---\n")
        elif cmd_base == "current" or cmd_base == "curr" or cmd_base == "c":
            if current_user:
                print(f"Current user: {current_user}, Score: {score}, Money: ${money}")
            else:
                print("No current user logged in.")
        elif cmd_base == "numbers":
            print("Random numbers generated this session: (not tracked)")
        elif cmd_base == "adduser":
            if args:
                parts = args.split(" ", 1)
                if len(parts) == 2:
                    u, p = parts
                    if signup(u, p):
                        print(f"User {u} created.")
                    else:
                        print("Failed to create user.")
                else:
                    print("Usage: adduser <username> <password>")
            else:
                print("Usage: adduser <username> <password>")
        elif cmd_base == "deluser":
            if args:
                u = args.strip()
                c.execute('DELETE FROM users WHERE username = ?', (u,))
                conn.commit()
                if c.rowcount > 0:
                    print(f"User {u} deleted.")
                else:
                    print("User not found.")
            else:
                print("Usage: deluser <username>")
        elif cmd_base == "reset":
            c.execute('DELETE FROM users')
            conn.commit()
            print("All users reset.")
        elif cmd_base == "resetplayer":
            if args:
                u = args.strip()
                c.execute('SELECT username FROM users WHERE username = ?', (u,))
                if c.fetchone():
                    player_data = default_player_data()
                    c.execute('UPDATE users SET score = 0, money = 40, player_data = ? WHERE username = ?', (json.dumps(player_data), u))
                    conn.commit()
                    print(f"Player {u} reset to defaults.")
                else:
                    print("User not found.")
            else:
                print("Usage: resetplayer <username>")
        elif cmd_base == "setdmoney":
            if args:
                try:
                    global dungeon_treasure
                    dungeon_treasure = int(args.strip())
                    save_dungeon_treasure()
                    print(f"Dungeon treasure set to ${dungeon_treasure}")
                except ValueError:
                    print("Invalid number.")
            else:
                print("Usage: setdmoney <n>")
        elif cmd_base == "setscore":
            if args:
                parts = args.split(" ", 1)
                if len(parts) == 2:
                    u, n = parts
                    try:
                        n = int(n)
                        c.execute('UPDATE users SET score = ? WHERE username = ?', (n, u))
                        conn.commit()
                        if c.rowcount > 0:
                            print(f"Score for {u} set to {n}.")
                        else:
                            print("User not found.")
                    except ValueError:
                        print("Invalid score.")
                else:
                    print("Usage: setscore <username> <score>")
            else:
                print("Usage: setscore <username> <score>")
        elif cmd_base == "setmoney":
            if args:
                parts = args.split(" ", 1)
                if len(parts) == 2:
                    u, n = parts
                    try:
                        n = int(n)
                        c.execute('UPDATE users SET money = ? WHERE username = ?', (n, u))
                        conn.commit()
                        if c.rowcount > 0:
                            print(f"Money for {u} set to ${n}.")
                        else:
                            print("User not found.")
                    except ValueError:
                        print("Invalid money.")
                else:
                    print("Usage: setmoney <username> <money>")
            else:
                print("Usage: setmoney <username> <money>")
        elif cmd_base == "setexp":
            if args:
                parts = args.split(" ", 1)
                if len(parts) == 2:
                    u, n = parts
                    try:
                        n = int(n)
                        c.execute('SELECT player_data FROM users WHERE username = ?', (u,))
                        result = c.fetchone()
                        if result:
                            player_data = json.loads(result[0])
                            stats = player_data["stats"]
                            stats["exp"] = n
                            player_data["stats"] = stats
                            c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), u))
                            conn.commit()
                            print(f"EXP for {u} set to {n}.")
                        else:
                            print("User not found.")
                    except ValueError:
                        print("Invalid EXP.")
                else:
                    print("Usage: setexp <username> <exp>")
            else:
                print("Usage: setexp <username> <exp>")
        elif cmd_base == "setlvl":
            if args:
                parts = args.split(" ", 1)
                if len(parts) == 2:
                    u, n = parts
                    try:
                        n = int(n)
                        c.execute('SELECT player_data FROM users WHERE username = ?', (u,))
                        result = c.fetchone()
                        if result:
                            player_data = json.loads(result[0])
                            stats = player_data["stats"]
                            stats["level"] = n
                            player_data["stats"] = stats
                            c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), u))
                            conn.commit()
                            print(f"Level for {u} set to {n}.")
                        else:
                            print("User not found.")
                    except ValueError:
                        print("Invalid level.")
                else:
                    print("Usage: setlvl <username> <level>")
            else:
                print("Usage: setlvl <username> <level>")
        elif cmd_base == "setdefeated":
            if args:
                parts = args.split(" ", 2)
                if len(parts) == 3:
                    u, typ, n = parts
                    try:
                        n = int(n)
                        c.execute('SELECT player_data FROM users WHERE username = ?', (u,))
                        result = c.fetchone()
                        if result:
                            player_data = json.loads(result[0])
                            stats = player_data["stats"]
                            if typ.lower() in ["monsters", "monster"]:
                                stats["monsters_defeated"] = n
                            elif typ.lower() in ["bosses", "boss"]:
                                stats["bosses_defeated"] = n
                            else:
                                print(f"Invalid type: {typ}")
                                continue
                            player_data["stats"] = stats
                            c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), u))
                            conn.commit()
                            print(f"{typ} defeated for {u} set to {n}.")
                        else:
                            print("User not found.")
                    except ValueError:
                        print("Invalid number.")
                else:
                    print("Usage: setdefeated <username> <type> <n>")
            else:
                print("Usage: setdefeated <username> <type> <n>")
        elif cmd_base == "set":
            if args:
                parts = args.split(" ", 2)
                if len(parts) == 3:
                    u, stat, n = parts
                    try:
                        n = int(n)
                        c.execute('SELECT player_data FROM users WHERE username = ?', (u,))
                        result = c.fetchone()
                        if result:
                            player_data = json.loads(result[0])
                            stats = player_data["stats"]
                            if stat in stats:
                                stats[stat] = n
                                player_data["stats"] = stats
                                c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), u))
                                conn.commit()
                                print(f"{stat} for {u} set to {n}.")
                            else:
                                print(f"Invalid stat: {stat}")
                        else:
                            print("User not found.")
                    except ValueError:
                        print("Invalid number.")
                else:
                    print("Usage: set <username> <stat> <n>")
            else:
                print("Usage: set <username> <stat> <n>")
        elif cmd_base == "showfull":
            if args:
                u = args.strip()
                c.execute('SELECT player_data FROM users WHERE username = ?', (u,))
                result = c.fetchone()
                if result:
                    player_data = json.loads(result[0])
                    print(f"\nFull data for {u}:")
                    for key, value in player_data.items():
                        if isinstance(value, dict):
                            print(f"{key}:")
                            for subkey, subvalue in value.items():
                                print(f"  {subkey}: {subvalue}")
                        else:
                            print(f"{key}: {value}")
                    print("---")
                else:
                    print("User not found.")
            else:
                print("Usage: showfull <username>")
        elif cmd_base == "give":
            if args:
                parts = args.split(" ", 2)
                if len(parts) >= 2:
                    u, item = parts[0], parts[1]
                    qty = int(parts[2]) if len(parts) > 2 else 1
                    try:
                        qty = int(qty) if isinstance(qty, str) else qty
                        c.execute('SELECT player_data FROM users WHERE username = ?', (u,))
                        result = c.fetchone()
                        if result:
                            player_data = json.loads(result[0])
                            inventory = player_data.get("inventory", {})
                            inventory[item] = inventory.get(item, 0) + qty
                            player_data["inventory"] = inventory
                            c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), u))
                            conn.commit()
                            print(f"Gave {qty}x {item} to {u}.")
                        else:
                            print("User not found.")
                    except ValueError:
                        print("Invalid quantity.")
                else:
                    print("Usage: give <username> <item> [qty]")
            else:
                print("Usage: give <username> <item> [qty]")
        elif cmd_base == "ruinthefun":
            if args:
                u = args.strip()
                c.execute('SELECT player_data FROM users WHERE username = ?', (u,))
                result = c.fetchone()
                if result:
                    player_data = json.loads(result[0])
                    stats = player_data["stats"]
                    inventory = player_data["inventory"]
                    # Max stats
                    stats["level"] = MAX_LEVEL
                    stats["exp"] = exp_to_next(MAX_LEVEL) - 1
                    stats["hp_max"] = 1000
                    stats["mana_max"] = 500
                    stats["atk"] = 100
                    stats["defense"] = 50
                    stats["perm_atk"] = 50
                    stats["perm_def"] = 25
                    stats["perm_hp_max"] = 500
                    stats["perm_mana_max"] = 250
                    stats["perm_crit_chance"] = 50
                    stats["perm_mana_regen"] = 20
                    stats["perm_lifesteal"] = 20
                    stats["perm_lifesteal_chance"] = 20
                    stats["perm_exp_boost"] = 50
                    # All achievements
                    stats["achievements"] = list(ACHIEVEMENTS.keys())
                    stats["available_titles"] = list(TITLES.keys())
                    # Equip all titles
                    stats["equipped_titles"] = list(TITLES.keys())
                    # 500x usable items
                    inventory["potion"] = 500
                    inventory["strong_potion"] = 500
                    inventory["ultra_potion"] = 500
                    inventory["mana_regen_potion"] = 500
                    inventory["instant_mana"] = 500
                    inventory["strength_boost"] = 500
                    inventory["defense_boost"] = 500
                    inventory["regen_potion"] = 500
                    inventory["crit_boost"] = 500
                    inventory["mana_upgrade_potion"] = 500
                    # All equipment
                    for eq in [WEAPONS, ARMORS, WANDS, ROBES, NECKLACES]:
                        for item in eq:
                            inventory[item] = 1
                    # All permanent upgrades
                    for up in PERM_UPGRADES:
                        inventory[up] = 1
                    player_data["stats"] = stats
                    player_data["inventory"] = inventory
                    apply_title_boosts(stats)
                    c.execute('UPDATE users SET player_data = ?, score = 999999, money = 999999 WHERE username = ?', (json.dumps(player_data), u))
                    conn.commit()
                    print(f"Ruin the fun activated for {u}.")
                else:
                    print("User not found.")
            else:
                print("Usage: ruinthefun <username>")
        elif cmd_base == "exit" or cmd_base == "quit" or cmd_base == "q":
            print("Exiting debug console.")
            break
        else:
            print("Unknown command. Type 'help' for commands.")
    conn.close()
# -------------------------
def dungeon():
    global current_user
    if not current_user:
        print("You must be logged in to enter the dungeon.")
        return
    ensure_user_fields(current_user)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT player_data FROM users WHERE username = ?', (current_user,))
    result = c.fetchone()
    player_data = json.loads(result[0])
# -------------------------
# Shop Interface
# -------------------------
def shop():
    global current_user
    if not current_user:
        print("You must be logged in to access the shop.")
        return

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT score, money, player_data FROM users WHERE username = ?', (current_user,))
    result = c.fetchone()
    if not result:
        print("User data not found.")
        conn.close()
        return

    score, money, player_data_json = result
    player_data = json.loads(player_data_json)
    inventory = player_data.get("inventory", {})

    while True:
        print("\n--- Shop ---")
        print(f"Money: ${money} | Score: {score}")
        print("Type the number to purchase, or 'exit' to leave shop.")
        print("----- Potions & Mana -----")
        print("1. Potion (restores 30 HP) - $20")
        print("2. Strong Potion (restores 80 HP) - $80")
        print("3. Ultra Potion (restores 200 HP) - $350")
        print("4. Mana Regen Potion (+15 mana per fight for 4 fights) - $120")
        print("5. Instant Mana (restore full mana) - $60")
        print("\n----- Buffs -----")
        print("6. Strength Boost (+5 ATK next fights) - $60")
        print("7. Defense Boost (+3 DEF next fights) - $60")
        print("8. Regen Potion (+12 HP/fight next fights) - $80")
        print("9. Crit Boost (+50% crit next fights) - $80")
        print("\n----- Weapons -----")
        print(f"10. Wooden Sword (+2 ATK) - ${WEAPONS['wooden_sword']['price']}")
        print(f"11. Iron Sword (+5 ATK) - ${WEAPONS['iron_sword']['price']}")
        print(f"12. Steel Sword (+8 ATK) - ${WEAPONS['steel_sword']['price']}")
        print(f"13. Diamond Sword (+50 ATK) - ${WEAPONS['diamond_sword']['price']}")
        print(f"14. Void Sword (+200 ATK) - ${WEAPONS['void_sword']['price']}")
        print(f"15. Infinitium Sword (+2000 ATK) - ${WEAPONS['infinitium_sword']['price']} and {WEAPONS['infinitium_sword'].get('score_price',0)} score")
        print(f"16. Frostblade (+120 ATK) - ${WEAPONS['frostblade']['price']} and {WEAPONS['frostblade'].get('score_price',0)} score")
        print(f"17. Flameblade (+130 ATK) - ${WEAPONS['flameblade']['price']} and {WEAPONS['flameblade'].get('score_price',0)} score")
        print(f"18. Thunder Sword (+150 ATK) - ${WEAPONS['thunder_sword']['price']} and {WEAPONS['thunder_sword'].get('score_price',0)} score")
        print(f"19. Holy Avenger (+180 ATK) - ${WEAPONS['holy_avenger']['price']} and {WEAPONS['holy_avenger'].get('score_price',0)} score")
        print(f"20. Dragon Slayer (+250 ATK) - ${WEAPONS['dragon_slayer']['price']} and {WEAPONS['dragon_slayer'].get('score_price',0)} score")
        print(f"21. Cosmic Blade (+500 ATK) - ${WEAPONS['cosmic_blade']['price']} and {WEAPONS['cosmic_blade'].get('score_price',0)} score")
        print(f"22. Transcendent Edge (+1500 ATK) - ${WEAPONS['transcendent_edge']['price']} and {WEAPONS['transcendent_edge'].get('score_price',0)} score")
        print("\n----- Armors -----")
        print(f"23. Leather Armor (+1 DEF) - ${ARMORS['leather_armor']['price']}")
        print(f"24. Chainmail (+3 DEF) - ${ARMORS['chainmail']['price']}")
        print(f"25. Plate Armor (+6 DEF) - ${ARMORS['plate_armor']['price']}")
        print(f"26. Diamond Armor (+25 DEF) - ${ARMORS['diamond_armor']['price']}")
        print(f"27. Void Armor (+75 DEF) - ${ARMORS['void_armor']['price']}")
        print(f"28. Infinitium Armor (+300 DEF) - ${ARMORS['infinitium_armor']['price']} and {ARMORS['infinitium_armor'].get('score_price',0)} score")
        print(f"29. Frost Armor (+40 DEF) - ${ARMORS['frost_armor']['price']} and {ARMORS['frost_armor'].get('score_price',0)} score")
        print(f"30. Flame Armor (+45 DEF) - ${ARMORS['flame_armor']['price']} and {ARMORS['flame_armor'].get('score_price',0)} score")
        print(f"31. Thunder Armor (+55 DEF) - ${ARMORS['thunder_armor']['price']} and {ARMORS['thunder_armor'].get('score_price',0)} score")
        print(f"32. Holy Armor (+70 DEF) - ${ARMORS['holy_armor']['price']} and {ARMORS['holy_armor'].get('score_price',0)} score")
        print(f"33. Dragon Scale Armor (+100 DEF) - ${ARMORS['dragon_scale_armor']['price']} and {ARMORS['dragon_scale_armor'].get('score_price',0)} score")
        print(f"34. Cosmic Armor (+200 DEF) - ${ARMORS['cosmic_armor']['price']} and {ARMORS['cosmic_armor'].get('score_price',0)} score")
        print(f"35. Transcendent Armor (+500 DEF) - ${ARMORS['transcendent_armor']['price']} and {ARMORS['transcendent_armor'].get('score_price',0)} score")
        print("\n----- Wands (mana weapons) -----")
        print(f"36. Apprentice Wand (+5 magic) - ${WANDS['apprentice_wand']['price']}")
        print(f"37. Mage Wand (+20 magic) - ${WANDS['mage_wand']['price']}")
        print(f"38. Archmage Staff (+120 magic) - ${WANDS['archmage_staff']['price']} and {WANDS['archmage_staff'].get('score_price',0)} score")
        print(f"39. Frost Wand (+60 magic) - ${WANDS['frost_wand']['price']} and {WANDS['frost_wand'].get('score_price',0)} score")
        print(f"40. Flame Wand (+65 magic) - ${WANDS['flame_wand']['price']} and {WANDS['flame_wand'].get('score_price',0)} score")
        print(f"41. Thunder Wand (+75 magic) - ${WANDS['thunder_wand']['price']} and {WANDS['thunder_wand'].get('score_price',0)} score")
        print(f"42. Holy Scepter (+90 magic) - ${WANDS['holy_scepter']['price']} and {WANDS['holy_scepter'].get('score_price',0)} score")
        print(f"43. Dragon Staff (+125 magic) - ${WANDS['dragon_staff']['price']} and {WANDS['dragon_staff'].get('score_price',0)} score")
        print(f"44. Cosmic Scepter (+250 magic) - ${WANDS['cosmic_scepter']['price']} and {WANDS['cosmic_scepter'].get('score_price',0)} score")
        print(f"45. Transcendent Staff (+750 magic) - ${WANDS['transcendent_staff']['price']} and {WANDS['transcendent_staff'].get('score_price',0)} score")
        print("\n----- Robes -----")
        print(f"46. Cloth Robe (+2 magic def) - ${ROBES['cloth_robe']['price']}")
        print(f"47. Silk Robe (+10 magic def) - ${ROBES['silk_robe']['price']}")
        print(f"48. Void Robe (+80 magic def) - ${ROBES['void_robe']['price']} and {ROBES['void_robe'].get('score_price',0)} score")
        print(f"49. Frost Robe (+30 magic def) - ${ROBES['frost_robe']['price']} and {ROBES['frost_robe'].get('score_price',0)} score")
        print(f"50. Flame Robe (+35 magic def) - ${ROBES['flame_robe']['price']} and {ROBES['flame_robe'].get('score_price',0)} score")
        print(f"51. Thunder Robe (+45 magic def) - ${ROBES['thunder_robe']['price']} and {ROBES['thunder_robe'].get('score_price',0)} score")
        print(f"52. Holy Robe (+60 magic def) - ${ROBES['holy_robe']['price']} and {ROBES['holy_robe'].get('score_price',0)} score")
        print(f"53. Dragon Robe (+90 magic def) - ${ROBES['dragon_robe']['price']} and {ROBES['dragon_robe'].get('score_price',0)} score")
        print(f"54. Cosmic Robe (+180 magic def) - ${ROBES['cosmic_robe']['price']} and {ROBES['cosmic_robe'].get('score_price',0)} score")
        print(f"55. Transcendent Robe (+450 magic def) - ${ROBES['transcendent_robe']['price']} and {ROBES['transcendent_robe'].get('score_price',0)} score")
        print("\n----- Necklaces -----")
        print(f"56. Health Amulet (+20 HP) - ${NECKLACES['health_amulet']['price']}")
        print(f"57. Mana Amulet (+15 Mana) - ${NECKLACES['mana_amulet']['price']}")
        print(f"58. Strength Amulet (+5 ATK) - ${NECKLACES['strength_amulet']['price']}")
        print(f"59. Defense Amulet (+3 DEF) - ${NECKLACES['defense_amulet']['price']}")
        print(f"60. Critical Amulet (+10% Crit) - ${NECKLACES['crit_amulet']['price']}")
        print(f"61. Lifesteal Amulet (+5% Lifesteal) - ${NECKLACES['lifesteal_amulet']['price']}")
        print(f"62. Frost Necklace (+15 Magic Def, +30 HP) - ${NECKLACES['frost_necklace']['price']} and {NECKLACES['frost_necklace'].get('score_price',0)} score")
        print(f"63. Flame Necklace (+10 Magic Atk, +8 ATK) - ${NECKLACES['flame_necklace']['price']} and {NECKLACES['flame_necklace'].get('score_price',0)} score")
        print(f"64. Thunder Necklace (+15% Crit, +10 ATK) - ${NECKLACES['thunder_necklace']['price']} and {NECKLACES['thunder_necklace'].get('score_price',0)} score")
        print(f"65. Holy Pendant (+50 HP, +30 Mana, +5 DEF) - ${NECKLACES['holy_pendant']['price']} and {NECKLACES['holy_pendant'].get('score_price',0)} score")
        print(f"66. Dragon Necklace (+20 ATK, +15 DEF, +70 HP) - ${NECKLACES['dragon_necklace']['price']} and {NECKLACES['dragon_necklace'].get('score_price',0)} score")
        print(f"67. Cosmic Necklace (+30 Magic Atk, +25 Magic Def, +50 Mana) - ${NECKLACES['cosmic_necklace']['price']} and {NECKLACES['cosmic_necklace'].get('score_price',0)} score")
        print(f"68. Transcendent Necklace (+50 ATK, +40 DEF, +150 HP, +100 Mana, +20% Crit, +10% Lifesteal) - ${NECKLACES['transcendent_necklace']['price']} and {NECKLACES['transcendent_necklace'].get('score_price',0)} score")
        print("\n----- Other Actions -----")
        print("69. Equip item from inventory")
        print("70. Unequip item")
        print("71. Sell Potion (sell 1 potion for $10)")
        print("72. Craft Items")
        print("73. View dungeon treasure")
        print("74. Exit shop")

        choice = input("\nChoose an option: ").strip().lower()
        if choice in ("exit", "74"):
            break

        item_name = None
        item_dict = None
        cost = 0
        score_cost = 0
        is_equipment = False

        if choice == "1":
            item_name = "potion"
            cost = 20
        elif choice == "2":
            item_name = "strong_potion"
            cost = 80
        elif choice == "3":
            item_name = "ultra_potion"
            cost = 350
        elif choice == "4":
            item_name = "mana_regen_potion"
            cost = 120
        elif choice == "5":
            item_name = "instant_mana"
            cost = 60
        elif choice == "6":
            item_name = "strength_boost"
            cost = 60
        elif choice == "7":
            item_name = "defense_boost"
            cost = 60
        elif choice == "8":
            item_name = "regen_potion"
            cost = 80
        elif choice == "9":
            item_name = "crit_boost"
            cost = 80
        elif choice == "10":
            item_name = "wooden_sword"
            item_dict = WEAPONS
            cost = WEAPONS["wooden_sword"]["price"]
            is_equipment = True
        elif choice == "11":
            item_name = "iron_sword"
            item_dict = WEAPONS
            cost = WEAPONS["iron_sword"]["price"]
            is_equipment = True
        elif choice == "12":
            item_name = "steel_sword"
            item_dict = WEAPONS
            cost = WEAPONS["steel_sword"]["price"]
            is_equipment = True
        elif choice == "13":
            item_name = "diamond_sword"
            item_dict = WEAPONS
            cost = WEAPONS["diamond_sword"]["price"]
            is_equipment = True
        elif choice == "14":
            item_name = "void_sword"
            item_dict = WEAPONS
            cost = WEAPONS["void_sword"]["price"]
            is_equipment = True
        elif choice == "15":
            item_name = "infinitium_sword"
            item_dict = WEAPONS
            cost = WEAPONS["infinitium_sword"]["price"]
            score_cost = WEAPONS["infinitium_sword"].get("score_price", 0)
            is_equipment = True
        elif choice == "16":
            item_name = "frostblade"
            item_dict = WEAPONS
            cost = WEAPONS["frostblade"]["price"]
            score_cost = WEAPONS["frostblade"].get("score_price", 0)
            is_equipment = True
        elif choice == "17":
            item_name = "flameblade"
            item_dict = WEAPONS
            cost = WEAPONS["flameblade"]["price"]
            score_cost = WEAPONS["flameblade"].get("score_price", 0)
            is_equipment = True
        elif choice == "18":
            item_name = "thunder_sword"
            item_dict = WEAPONS
            cost = WEAPONS["thunder_sword"]["price"]
            score_cost = WEAPONS["thunder_sword"].get("score_price", 0)
            is_equipment = True
        elif choice == "19":
            item_name = "holy_avenger"
            item_dict = WEAPONS
            cost = WEAPONS["holy_avenger"]["price"]
            score_cost = WEAPONS["holy_avenger"].get("score_price", 0)
            is_equipment = True
        elif choice == "20":
            item_name = "dragon_slayer"
            item_dict = WEAPONS
            cost = WEAPONS["dragon_slayer"]["price"]
            score_cost = WEAPONS["dragon_slayer"].get("score_price", 0)
            is_equipment = True
        elif choice == "21":
            item_name = "cosmic_blade"
            item_dict = WEAPONS
            cost = WEAPONS["cosmic_blade"]["price"]
            score_cost = WEAPONS["cosmic_blade"].get("score_price", 0)
            is_equipment = True
        elif choice == "22":
            item_name = "transcendent_edge"
            item_dict = WEAPONS
            cost = WEAPONS["transcendent_edge"]["price"]
            score_cost = WEAPONS["transcendent_edge"].get("score_price", 0)
            is_equipment = True
        elif choice == "23":
            item_name = "leather_armor"
            item_dict = ARMORS
            cost = ARMORS["leather_armor"]["price"]
            is_equipment = True
        elif choice == "24":
            item_name = "chainmail"
            item_dict = ARMORS
            cost = ARMORS["chainmail"]["price"]
            is_equipment = True
        elif choice == "25":
            item_name = "plate_armor"
            item_dict = ARMORS
            cost = ARMORS["plate_armor"]["price"]
            is_equipment = True
        elif choice == "26":
            item_name = "diamond_armor"
            item_dict = ARMORS
            cost = ARMORS["diamond_armor"]["price"]
            is_equipment = True
        elif choice == "27":
            item_name = "void_armor"
            item_dict = ARMORS
            cost = ARMORS["void_armor"]["price"]
            is_equipment = True
        elif choice == "28":
            item_name = "infinitium_armor"
            item_dict = ARMORS
            cost = ARMORS["infinitium_armor"]["price"]
            score_cost = ARMORS["infinitium_armor"].get("score_price", 0)
            is_equipment = True
        elif choice == "29":
            item_name = "frost_armor"
            item_dict = ARMORS
            cost = ARMORS["frost_armor"]["price"]
            score_cost = ARMORS["frost_armor"].get("score_price", 0)
            is_equipment = True
        elif choice == "30":
            item_name = "flame_armor"
            item_dict = ARMORS
            cost = ARMORS["flame_armor"]["price"]
            score_cost = ARMORS["flame_armor"].get("score_price", 0)
            is_equipment = True
        elif choice == "31":
            item_name = "thunder_armor"
            item_dict = ARMORS
            cost = ARMORS["thunder_armor"]["price"]
            score_cost = ARMORS["thunder_armor"].get("score_price", 0)
            is_equipment = True
        elif choice == "32":
            item_name = "holy_armor"
            item_dict = ARMORS
            cost = ARMORS["holy_armor"]["price"]
            score_cost = ARMORS["holy_armor"].get("score_price", 0)
            is_equipment = True
        elif choice == "33":
            item_name = "dragon_scale_armor"
            item_dict = ARMORS
            cost = ARMORS["dragon_scale_armor"]["price"]
            score_cost = ARMORS["dragon_scale_armor"].get("score_price", 0)
            is_equipment = True
        elif choice == "34":
            item_name = "cosmic_armor"
            item_dict = ARMORS
            cost = ARMORS["cosmic_armor"]["price"]
            score_cost = ARMORS["cosmic_armor"].get("score_price", 0)
            is_equipment = True
        elif choice == "35":
            item_name = "transcendent_armor"
            item_dict = ARMORS
            cost = ARMORS["transcendent_armor"]["price"]
            score_cost = ARMORS["transcendent_armor"].get("score_price", 0)
            is_equipment = True
        elif choice == "36":
            item_name = "apprentice_wand"
            item_dict = WANDS
            cost = WANDS["apprentice_wand"]["price"]
            is_equipment = True
        elif choice == "37":
            item_name = "mage_wand"
            item_dict = WANDS
            cost = WANDS["mage_wand"]["price"]
            is_equipment = True
        elif choice == "38":
            item_name = "archmage_staff"
            item_dict = WANDS
            cost = WANDS["archmage_staff"]["price"]
            score_cost = WANDS["archmage_staff"].get("score_price", 0)
            is_equipment = True
        elif choice == "39":
            item_name = "frost_wand"
            item_dict = WANDS
            cost = WANDS["frost_wand"]["price"]
            score_cost = WANDS["frost_wand"].get("score_price", 0)
            is_equipment = True
        elif choice == "40":
            item_name = "flame_wand"
            item_dict = WANDS
            cost = WANDS["flame_wand"]["price"]
            score_cost = WANDS["flame_wand"].get("score_price", 0)
            is_equipment = True
        elif choice == "41":
            item_name = "thunder_wand"
            item_dict = WANDS
            cost = WANDS["thunder_wand"]["price"]
            score_cost = WANDS["thunder_wand"].get("score_price", 0)
            is_equipment = True
        elif choice == "42":
            item_name = "holy_scepter"
            item_dict = WANDS
            cost = WANDS["holy_scepter"]["price"]
            score_cost = WANDS["holy_scepter"].get("score_price", 0)
            is_equipment = True
        elif choice == "43":
            item_name = "dragon_staff"
            item_dict = WANDS
            cost = WANDS["dragon_staff"]["price"]
            score_cost = WANDS["dragon_staff"].get("score_price", 0)
            is_equipment = True
        elif choice == "44":
            item_name = "cosmic_scepter"
            item_dict = WANDS
            cost = WANDS["cosmic_scepter"]["price"]
            score_cost = WANDS["cosmic_scepter"].get("score_price", 0)
            is_equipment = True
        elif choice == "45":
            item_name = "transcendent_staff"
            item_dict = WANDS
            cost = WANDS["transcendent_staff"]["price"]
            score_cost = WANDS["transcendent_staff"].get("score_price", 0)
            is_equipment = True
        elif choice == "46":
            item_name = "cloth_robe"
            item_dict = ROBES
            cost = ROBES["cloth_robe"]["price"]
            is_equipment = True
        elif choice == "47":
            item_name = "silk_robe"
            item_dict = ROBES
            cost = ROBES["silk_robe"]["price"]
            is_equipment = True
        elif choice == "48":
            item_name = "void_robe"
            item_dict = ROBES
            cost = ROBES["void_robe"]["price"]
            score_cost = ROBES["void_robe"].get("score_price", 0)
            is_equipment = True
        elif choice == "49":
            item_name = "frost_robe"
            item_dict = ROBES
            cost = ROBES["frost_robe"]["price"]
            score_cost = ROBES["frost_robe"].get("score_price", 0)
            is_equipment = True
        elif choice == "50":
            item_name = "flame_robe"
            item_dict = ROBES
            cost = ROBES["flame_robe"]["price"]
            score_cost = ROBES["flame_robe"].get("score_price", 0)
            is_equipment = True
        elif choice == "51":
            item_name = "thunder_robe"
            item_dict = ROBES
            cost = ROBES["thunder_robe"]["price"]
            score_cost = ROBES["thunder_robe"].get("score_price", 0)
            is_equipment = True
        elif choice == "52":
            item_name = "holy_robe"
            item_dict = ROBES
            cost = ROBES["holy_robe"]["price"]
            score_cost = ROBES["holy_robe"].get("score_price", 0)
            is_equipment = True
        elif choice == "53":
            item_name = "dragon_robe"
            item_dict = ROBES
            cost = ROBES["dragon_robe"]["price"]
            score_cost = ROBES["dragon_robe"].get("score_price", 0)
            is_equipment = True
        elif choice == "54":
            item_name = "cosmic_robe"
            item_dict = ROBES
            cost = ROBES["cosmic_robe"]["price"]
            score_cost = ROBES["cosmic_robe"].get("score_price", 0)
            is_equipment = True
        elif choice == "55":
            item_name = "transcendent_robe"
            item_dict = ROBES
            cost = ROBES["transcendent_robe"]["price"]
            score_cost = ROBES["transcendent_robe"].get("score_price", 0)
            is_equipment = True
        elif choice == "56":
            item_name = "health_amulet"
            item_dict = NECKLACES
            cost = NECKLACES["health_amulet"]["price"]
            is_equipment = True
        elif choice == "57":
            item_name = "mana_amulet"
            item_dict = NECKLACES
            cost = NECKLACES["mana_amulet"]["price"]
            is_equipment = True
        elif choice == "58":
            item_name = "strength_amulet"
            item_dict = NECKLACES
            cost = NECKLACES["strength_amulet"]["price"]
            is_equipment = True
        elif choice == "59":
            item_name = "defense_amulet"
            item_dict = NECKLACES
            cost = NECKLACES["defense_amulet"]["price"]
            is_equipment = True
        elif choice == "60":
            item_name = "crit_amulet"
            item_dict = NECKLACES
            cost = NECKLACES["crit_amulet"]["price"]
            is_equipment = True
        elif choice == "61":
            item_name = "lifesteal_amulet"
            item_dict = NECKLACES
            cost = NECKLACES["lifesteal_amulet"]["price"]
            is_equipment = True
        elif choice == "62":
            item_name = "frost_necklace"
            item_dict = NECKLACES
            cost = NECKLACES["frost_necklace"]["price"]
            score_cost = NECKLACES["frost_necklace"].get("score_price", 0)
            is_equipment = True
        elif choice == "63":
            item_name = "flame_necklace"
            item_dict = NECKLACES
            cost = NECKLACES["flame_necklace"]["price"]
            score_cost = NECKLACES["flame_necklace"].get("score_price", 0)
            is_equipment = True
        elif choice == "64":
            item_name = "thunder_necklace"
            item_dict = NECKLACES
            cost = NECKLACES["thunder_necklace"]["price"]
            score_cost = NECKLACES["thunder_necklace"].get("score_price", 0)
            is_equipment = True
        elif choice == "65":
            item_name = "holy_pendant"
            item_dict = NECKLACES
            cost = NECKLACES["holy_pendant"]["price"]
            score_cost = NECKLACES["holy_pendant"].get("score_price", 0)
            is_equipment = True
        elif choice == "66":
            item_name = "dragon_necklace"
            item_dict = NECKLACES
            cost = NECKLACES["dragon_necklace"]["price"]
            score_cost = NECKLACES["dragon_necklace"].get("score_price", 0)
            is_equipment = True
        elif choice == "67":
            item_name = "cosmic_necklace"
            item_dict = NECKLACES
            cost = NECKLACES["cosmic_necklace"]["price"]
            score_cost = NECKLACES["cosmic_necklace"].get("score_price", 0)
            is_equipment = True
        elif choice == "68":
            item_name = "transcendent_necklace"
            item_dict = NECKLACES
            cost = NECKLACES["transcendent_necklace"]["price"]
            score_cost = NECKLACES["transcendent_necklace"].get("score_price", 0)
            is_equipment = True
        elif choice == "69":
            manage_inventory_menu(current_user, player_data, c)
            # Reload data after inventory changes
            c.execute('SELECT player_data FROM users WHERE username = ?', (current_user,))
            result = c.fetchone()
            if result:
                player_data = json.loads(result[0])
                inventory = player_data.get("inventory", {})
            continue
        elif choice == "70":
            # Unequip item
            print("Unequip which item? (weapon/armor/wand/robe/necklace)")
            item_type = input("Item type: ").strip().lower()
            stats = player_data["stats"]
            equipped = stats.get("equipped", {})
            if item_type in ["weapon", "armor", "wand", "robe", "necklace"]:
                equipped[item_type] = None
                player_data["stats"] = stats
                c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), current_user))
                conn.commit()
                print(f"Unequipped {item_type}.")
                continue
            else:
                print("Invalid item type.")
                continue
        elif choice == "71":
            # Sell potion
            if inventory.get("potion", 0) > 0:
                inventory["potion"] -= 1
                money += 10
                player_data["inventory"] = inventory
                c.execute('UPDATE users SET money = ?, player_data = ? WHERE username = ?', (money, json.dumps(player_data), current_user))
                conn.commit()
                print("Sold 1 potion for $10.")
            else:
                print("No potions to sell.")
            continue
        elif choice == "72":
            # Craft items - placeholder
            print("Crafting not implemented yet.")
            continue
        elif choice == "73":
            # View dungeon treasure
            global dungeon_treasure
            print(f"Current dungeon treasure: ${dungeon_treasure}")
            continue
        else:
            print("Invalid choice.")
            continue

        if item_name:
            if money >= cost and score >= score_cost:
                if is_equipment:
                    if inventory.get(item_name, 0) > 0:
                        print("You already own this item.")
                    else:
                        inventory[item_name] = inventory.get(item_name, 0) + 1
                        money -= cost
                        score -= score_cost
                        player_data["inventory"] = inventory
                        c.execute('UPDATE users SET money = ?, score = ?, player_data = ? WHERE username = ?', (money, score, json.dumps(player_data), current_user))
                        conn.commit()
                        print(f"Purchased {item_name} for ${cost}" + (f" and {score_cost} score" if score_cost > 0 else "") + "!")
                else:
                    # Consumables can be bought multiple times
                    qty = parse_qty_from_choice(input("How many? (default 1): ").strip())
                    if qty <= 0:
                        qty = 1
                    total_cost = cost * qty
                    if money >= total_cost:
                        inventory[item_name] = inventory.get(item_name, 0) + qty
                        money -= total_cost
                        player_data["inventory"] = inventory
                        c.execute('UPDATE users SET money = ?, player_data = ? WHERE username = ?', (money, json.dumps(player_data), current_user))
                        conn.commit()
                        print(f"Purchased {qty}x {item_name} for ${total_cost}!")
                    else:
                        print("Not enough money.")
            else:
                print("Not enough money or score.")

    conn.close()

def parse_qty_from_choice(choice_str):
    try:
        return int(choice_str)
    except ValueError:
        return 1

    # Apply permanent upgrades before entering dungeon
    apply_permanent_upgrades(current_user)
    # Reload player data after applying upgrades
    c.execute('SELECT player_data FROM users WHERE username = ?', (current_user,))
    result = c.fetchone()
    player_data = json.loads(result[0])
    stats = player_data["stats"]
    inventory = player_data["inventory"]

    # Auto-equip best equipment after upgrading if enabled
    settings = stats.get("settings", {})
    if settings.get("auto_equip_best", False) or settings.get("auto_equip_everything", False):
        auto_equip_items(current_user)

    active_buffs = []
    forced_monster = None

    print("\n⚔️ Welcome to the Dungeon, brave adventurer!")
    player_hp = stats.get("hp", stats.get("hp_max", 100))
    player_mana = stats.get("mana", stats.get("mana_max", 50))

    # Calculate effective base ATK and DEF (including equipment and permanent upgrades)
    effective_base_atk, effective_base_def, _, _, _, _, _, _ = compute_effective_stats(stats, [])

    # Calculate base ATK and DEF with equipment (permanent upgrades + equipment)
    w_atk = WEAPONS.get(stats.get("equipped", {}).get("weapon"), {}).get("atk", 0)
    a_def = ARMORS.get(stats.get("equipped", {}).get("armor"), {}).get("def", 0)
    n_atk = NECKLACES.get(stats.get("equipped", {}).get("necklace"), {}).get("atk_bonus", 0)
    n_def = NECKLACES.get(stats.get("equipped", {}).get("necklace"), {}).get("def_bonus", 0)
    normal_atk = stats.get("atk", 5)
    normal_def = stats.get("defense", 0)
    equipped_atk = normal_atk + w_atk + n_atk
    equipped_def = normal_def + a_def + n_def

    current_area = stats.get("current_area", 1)
    print(f"Entering dungeon with HP: {player_hp}, MANA: {player_mana}, ATK: {equipped_atk}, DEF: {equipped_def}, LVL: {stats.get('level',1)}, AREA: {current_area}")
    print(f"Normal ATK + Perm: {normal_atk}, Normal DEF + Perm: {normal_def}")

    while True:
        cmd = input("\nType 'explore' to find a monster, 'status' to view stats, 'shop' to access shop, 'packs' to open magic packs, 'upgrades' to use permanent upgrades, 'move' to change areas, or 'exit' to leave the dungeon: ").strip()
        if not cmd:
            continue
        lc = cmd.lower().strip()
        if lc == "exit":
            print("You leave the dungeon safely.")
            stats["hp"] = player_hp
            stats["mana"] = player_mana
            update_user(current_user, users[current_user][1], users[current_user][2], player_data)
            conn.commit()
            conn.close()
            return
        if lc == "status":
            effective_atk, effective_def, _, _, _, _, _, _ = compute_effective_stats(stats, active_buffs)
            crit_chance = sum(b['amount'] for b in active_buffs if b['type']=='crit' and b['remaining']>0)
            regen_total = sum(b['amount'] for b in active_buffs if b['type']=='regen' and b['remaining']>0)
            mana_regen_total = sum(b['amount'] for b in active_buffs if b['type']=='mana_regen' and b['remaining']>0)
            next_exp = exp_to_next(stats.get("level",1)) if stats.get("level",1) < MAX_LEVEL else "MAX"
            name_display = current_user
            if stats.get("settings", {}).get("call_including_title", True) and stats.get("title"):
                name_display = f"{stats['title']} {current_user}"
            print(f"HP: {player_hp}/{stats.get('hp_max')}, MANA: {player_mana}/{stats.get('mana_max')}, ATK: {effective_atk}, DEF: {effective_def}, Money: ${player_data.get('money',0)}, LVL: {stats.get('level')}, EXP: {stats.get('exp')}/{next_exp}, AREA: {stats.get('current_area', 1)}")
            if stats.get("settings", {}).get("show_exp_bar", False):
                exp_bar = create_exp_bar(stats.get("exp", 0), next_exp if next_exp != "MAX" else exp_to_next(stats["level"]))
                print(f"EXP Bar: {exp_bar}")
            print("Equipped:", stats.get("equipped"))
            print("Inventory (highlights):", {k:v for k,v in inventory.items() if v>0 and k in ['potion','strong_potion','mana_regen_potion','instant_mana']})
            print("\nCurrent permanent stats:")
            print(f"ATK Bonus: +{stats.get('perm_atk', 0)}")
            print(f"DEF Bonus: +{stats.get('perm_def', 0)}")
            print(f"HP Bonus: +{stats.get('perm_hp_max', 0)}")
            print(f"Mana Bonus: +{stats.get('perm_mana_max', 0)}")
            print(f"Crit Chance Bonus: +{stats.get('perm_crit_chance', 0)}%")
            print(f"Mana Regen Bonus: +{stats.get('perm_mana_regen', 0)} per fight")
            print(f"Lifesteal Bonus: +{stats.get('perm_lifesteal', 0)}% of damage")
            print(f"Lifesteal Chance Bonus: +{stats.get('perm_lifesteal_chance', 0)}% chance")
            print(f"Experience Boost: +{stats.get('perm_exp_boost', 0)}%")
            if active_buffs:
                print("Active buffs (fights remaining):")
                for b in active_buffs:
                    if b['remaining']>0:
                        print(f" - {b}")
            continue
        if lc == "shop":
            shop()
            # Reload data after shop
            ensure_user_fields(current_user)
            c.execute('SELECT player_data FROM users WHERE username = ?', (current_user,))
            result = c.fetchone()
            player_data = json.loads(result[0])
            stats = player_data["stats"]
            inventory = player_data["inventory"]
            player_mana = stats.get("mana", stats.get("mana_max", 50))
            continue
        if lc == "packs":
            magic_pack_interface(current_user)
            # Reload data after packs
            ensure_user_fields(current_user)
            c.execute('SELECT player_data FROM users WHERE username = ?', (current_user,))
            result = c.fetchone()
            player_data = json.loads(result[0])
            stats = player_data["stats"]
            inventory = player_data["inventory"]
            continue
        if lc == "upgrades":
            permanent_upgrades_interface(current_user)
            # Reload data after upgrades
            ensure_user_fields(current_user)
            c.execute('SELECT player_data FROM users WHERE username = ?', (current_user,))
            result = c.fetchone()
            player_data = json.loads(result[0])
            stats = player_data["stats"]
            inventory = player_data["inventory"]
            player_mana = stats.get("mana", stats.get("mana_max", 50))
            continue
        if lc == "move":
            print(f"\nCurrent Area: {stats.get('current_area', 1)}")
            print("You can move to areas 1-10. Higher areas have stronger monsters.")
            try:
                new_area = int(input("Enter area number (1-10) or 'cancel': ").strip())
                if new_area == "cancel":
                    continue
                if 1 <= new_area <= 10:
                    stats["current_area"] = new_area
                    current_area = new_area
                    c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), current_user))
                    conn.commit()
                    print(f"Moved to Area {new_area}!")
                else:
                    print("Invalid area. Must be between 1 and 10.")
            except ValueError:
                print("Invalid input. Enter a number between 1 and 10.")
            continue

        if lc.startswith("explore "):
            parts = cmd.split()
            if len(parts) >= 4:
                code = parts[1].strip()
                is_boss_flag = parts[2].strip().lower()
                monster_name = " ".join(parts[3:]).strip().lower()
                if code == "10234":
                    boss_flags = ("yes", "y", "true", "boss", "b")
                    normal_flags = ("no", "n", "false", "normal", "monster", "m")
                    if is_boss_flag in boss_flags:
                        # Force boss
                        print("Forced boss spawn not implemented.")
                    elif is_boss_flag in normal_flags:
                        # Force normal monster
                        print("Forced monster spawn not implemented.")
                    else:
                        print("Invalid flag.")
                else:
                    print("Invalid code.")
            continue
        elif lc != "explore":
            print("Unknown command. Try 'explore', 'status', 'shop', 'packs', 'upgrades', 'move', or 'exit'.")
            continue

        # Explore logic
        if forced_monster is not None:
            monster = forced_monster.copy()
            forced_monster = None
            # Use existing monster data
        else:
            roll = random.randint(1,100)
            if roll <= 5:  # Boss chance
                # Choose random boss
                boss_keys = list(BOSSES.keys())
                boss_key = random.choice(boss_keys)
                monster = BOSSES[boss_key].copy()
                monster['is_boss'] = True
            else:
                # Choose random monster
                monster_keys = list(MONSTERS.keys())
                monster_key = random.choice(monster_keys)
                monster = MONSTERS[monster_key].copy()
                monster['is_boss'] = False

        # Scale monster stats based on area
        scale = 1.0 + (current_area - 1) * 0.15
        monster["hp"] = max(1, int(monster.get("hp", 1) * scale))
        monster["atk"] = max(1, int(monster["atk"] * scale))
        monster["def"] = max(0, int(monster["def"] * scale))
        monster["gold"] = max(1, int(monster["gold"] * scale))

        print(f"\nA wild {monster['name']} appears! (HP {monster['hp']}, ATK {monster['atk']}, DEF {monster['def']})")

        # Combat loop
        fight_happened = True
        battle_log = {
            "timestamp": time.time(),
            "monster_name": monster["name"],
            "monster_class": "Unknown",
            "monster_hp": monster["hp"],
            "monster_atk": monster["atk"],
            "player_hp_start": player_hp,
            "player_mana_start": player_mana,
            "actions": []
        }

    conn.close()

# -------------------------
# Permanent Upgrades Interface
# -------------------------
def permanent_upgrades_interface(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if not result:
        print("User data not found.")
        conn.close()
        return

    player_data = json.loads(result[0])
    inventory = player_data.get("inventory", {})
    stats = player_data.get("stats", {})

    while True:
        print("\n--- Permanent Upgrades ---")
        print("Available upgrades (use permanent upgrade items from inventory):")
        for key, upgrade in PERM_UPGRADES.items():
            count = inventory.get(key, 0)
            if count > 0:
                print(f"{key}: {upgrade['name']} (x{count})")
            else:
                print(f"{key}: {upgrade['name']} (not owned)")

        print("0. Back")

        choice = input("Choose upgrade to use: ").strip().lower()
        if choice == "0":
            break

        if choice in PERM_UPGRADES and inventory.get(choice, 0) > 0:
            inventory[choice] -= 1
            # Apply the upgrade
            if "atk_increase" in PERM_UPGRADES[choice]:
                stats["perm_atk"] = stats.get("perm_atk", 0) + PERM_UPGRADES[choice]["atk_increase"]
            elif "def_increase" in PERM_UPGRADES[choice]:
                stats["perm_def"] = stats.get("perm_def", 0) + PERM_UPGRADES[choice]["def_increase"]
            elif "hp_increase" in PERM_UPGRADES[choice]:
                stats["perm_hp_max"] = stats.get("perm_hp_max", 0) + PERM_UPGRADES[choice]["hp_increase"]
            elif "magic_increase" in PERM_UPGRADES[choice]:
                stats["perm_mana_max"] = stats.get("perm_mana_max", 0) + PERM_UPGRADES[choice]["magic_increase"]
            elif "crit_chance_increase" in PERM_UPGRADES[choice]:
                stats["perm_crit_chance"] = stats.get("perm_crit_chance", 0) + PERM_UPGRADES[choice]["crit_chance_increase"]
            elif "mana_regen_increase" in PERM_UPGRADES[choice]:
                stats["perm_mana_regen"] = stats.get("perm_mana_regen", 0) + PERM_UPGRADES[choice]["mana_regen_increase"]
            elif "max_lifesteal_increase" in PERM_UPGRADES[choice]:
                stats["perm_lifesteal"] = stats.get("perm_lifesteal", 0) + PERM_UPGRADES[choice]["max_lifesteal_increase"]
            elif "lifesteal_chance_increase" in PERM_UPGRADES[choice]:
                stats["perm_lifesteal_chance"] = stats.get("perm_lifesteal_chance", 0) + PERM_UPGRADES[choice]["lifesteal_chance_increase"]
            elif "exp_increase" in PERM_UPGRADES[choice]:
                stats["perm_exp_boost"] = stats.get("perm_exp_boost", 0) + PERM_UPGRADES[choice]["exp_increase"]

            # Reapply permanent upgrades to current stats
            apply_permanent_upgrades(username)

            player_data["inventory"] = inventory
            player_data["stats"] = stats
            c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), username))
            conn.commit()
            print(f"Used {PERM_UPGRADES[choice]['name']}!")
        else:
            print("Invalid choice or not owned.")

    conn.close()

# -------------------------
# Magic Pack Interface
# -------------------------
def magic_pack_interface(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if not result:
        print("User data not found.")
        conn.close()
        return

    player_data = json.loads(result[0])
    inventory = player_data.get("inventory", {})

    while True:
        print("\n--- Magic Packs ---")
        print("Available packs:")
        for pack_key, pack in MAGIC_PACKS.items():
            count = inventory.get(pack_key, 0)
            if count > 0:
                print(f"{pack_key}: {pack['name']} (x{count}) - {pack['description']}")
            else:
                print(f"{pack_key}: {pack['name']} - {pack['description']} (not owned)")

        print("0. Back")

        choice = input("Choose pack to open: ").strip().lower()
        if choice == "0":
            break

        # Handle aliases
        if choice in MAGIC_PACK_ALIASES:
            choice = MAGIC_PACK_ALIASES[choice]

        if choice in MAGIC_PACKS and inventory.get(choice, 0) > 0:
            success, message = open_magic_pack(username, choice, 1)
            if success:
                print(message)
                # Reload inventory
                c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
                result = c.fetchone()
                if result:
                    player_data = json.loads(result[0])
                    inventory = player_data.get("inventory", {})
            else:
                print(message)
        else:
            print("Invalid choice or not owned.")

    conn.close()
    effective_atk, effective_def, _, _, _, _, _, _ = compute_effective_stats(stats, active_buffs)
    crit_chance = sum(b['amount'] for b in active_buffs if b['type']=='crit' and b['remaining']>0) / 100.0
    base_crit = 0.05
    title_crit_percent = stats.get("title_crit_chance_percent", 0) / 100.0
    total_crit_chance = base_crit + crit_chance + title_crit_percent

    action = input("Do you want to (a)ttack, (m)agic, (p)otion, (u)se buff, or (r)un? ").lower().strip()
    if action == "a":
        dmg = random.randint(max(1, effective_atk - 2), effective_atk + 3)
        crit_hit = False
        if random.random() <= total_crit_chance:
            dmg *= 2
            crit_hit = True
            print("💥 CRITICAL HIT!")
            stats["critical_hits"] = stats.get("critical_hits", 0) + 1
        monster["hp"] -= dmg
        print(f"You hit the {monster['name']} for {dmg} damage! (Monster HP: {max(0, monster['hp'])})")
        battle_log["actions"].append({
            "action": "attack",
            "damage": dmg,
            "critical": crit_hit,
            "monster_hp_after": max(0, monster["hp"]),
            "player_hp_after": player_hp
        })

        # Apply lifesteal
        lifesteal_chance = stats.get("perm_lifesteal_chance", 0) / 100.0
        lifesteal_percent = stats.get("perm_lifesteal", 0) / 100.0
        if random.random() <= lifesteal_chance and lifesteal_percent > 0:
            heal_amount = int(dmg * lifesteal_percent)
            if heal_amount > 0:
                player_hp = min(player_hp + heal_amount, stats.get("hp_max"))
                print(f"🩸 LIFESTEAL! You stole {heal_amount} HP! (Your HP: {player_hp}/{stats.get('hp_max')})")

    elif action == "m":
        # Magic not fully implemented, skip
        print("Magic not implemented.")
    elif action == "p":
        # Simple potion use
        if inventory.get("potion", 0) > 0:
            inventory["potion"] -= 1
            heal = 30
            player_hp = min(player_hp + heal, stats.get("hp_max"))
            print(f"You used a potion and healed {heal} HP! (HP: {player_hp}/{stats.get('hp_max')})")
            battle_log["actions"].append({
                "action": "potion",
                "type": "potion",
                "heal": heal,
                "player_hp_after": player_hp
            })
        else:
            print("No potions!")
    elif action == "u":
        # Buff not implemented
        print("Buffs not implemented.")
    elif action == "r":
        if random.random() <= 0.7:
            print("You ran away safely!")
            battle_log["actions"].append({
                "action": "run",
                "success": True
            })
            break
        else:
            print("You failed to run away!")
            battle_log["actions"].append({
                "action": "run",
                "success": False,
                "damage_taken": 0,
                "player_hp_after": player_hp
            })
    else:
        print("Invalid action.")

    if monster["hp"] <= 0:
        break

    # Monster attack
    mon_atk = random.randint(monster["atk"] - 2, monster["atk"] + 2)
    damage_to_player = max(1, mon_atk - effective_def)
    player_hp -= damage_to_player
    print(f"The {monster['name']} hits you for {damage_to_player} damage! (Your HP: {max(0, player_hp)})")

    # Regen
    regen_amount = sum(b['amount'] for b in active_buffs if b['type']=='regen' and b['remaining']>0)
    hp_regen_percent = stats.get("title_hp_regen_percent", 0)
    regen_amount = int(regen_amount * (1 + hp_regen_percent / 100.0))
    if regen_amount > 0 and player_hp > 0:
        player_hp = min(player_hp + regen_amount, stats.get("hp_max"))
        print(f"🌿 Regen healed you for {regen_amount} HP! (HP: {player_hp}/{stats.get('hp_max')})")
    mana_regen_amount = sum(b['amount'] for b in active_buffs if b['type']=='mana_regen' and b['remaining']>0)
    permanent_mana_regen = stats.get("perm_mana_regen", 0)
    if mana_regen_amount > 0 or permanent_mana_regen > 0:
        total_mana_regen = mana_regen_amount + permanent_mana_regen
        if total_mana_regen > 0 and player_mana >= 0:
            player_mana = min(player_mana + total_mana_regen, stats.get("mana_max"))
            print(f"🔵 Mana Regen restored {total_mana_regen} mana! (MANA: {player_mana}/{stats.get('mana_max')})")

    # After fight
    if fight_happened:
        if player_hp <= 0:
            battle_log["outcome"] = "defeat"
        elif monster["hp"] <= 0:
            battle_log["outcome"] = "victory"
        else:
            battle_log["outcome"] = "run_success"

        # Append battle log
        stats["battle_logs"].append(battle_log)
        if len(stats["battle_logs"]) > 50:
            stats["battle_logs"] = stats["battle_logs"][-50:]

    if player_hp <= 0:
        print("💀 You have fallen in the dungeon...")
        money_now = player_data.get("money", 0)
        if money_now > 0:
            lost = money_now // 4
            if lost < 1:
                lost = 1
            death_penalty_percent = stats.get("title_death_penalty_percent", 0)
            lost = int(lost * (1 + death_penalty_percent / 100.0))
            if lost < 0:
                lost = 0
            if lost < 1:
                lost = 1
            player_data["money"] = max(0, money_now - lost)
            global dungeon_treasure
            dungeon_treasure += lost
            save_dungeon_treasure()
            print(f"You wake up outside the dungeon and lost ${lost}. The money has been added to the dungeon treasure.")
        else:
            print("You wake up outside the dungeon with no money to lose.")

        stats["times_died"] = stats.get("times_died", 0) + 1
        stats["hp"] = max(1, stats.get("hp_max",100))
        stats["mana"] = stats.get("mana_max",50)
        player_hp = stats["hp"]
        player_mana = stats["mana"]
        check_achievements(current_user)
        c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), current_user))
        conn.commit()
        continue

    if monster["hp"] <= 0:
        money_reward = monster["gold"]
        money_boost_percent = stats.get("title_money_boost_percent", 0)
        if money_boost_percent > 0:
            money_reward = int(money_reward * (1 + money_boost_percent / 100.0))
        player_data["money"] += money_reward

        exp_gain = max(1, (monster.get("hp",0) * 2) + random.randint(5, 30))
        if monster.get("is_boss"):
            exp_gain *= 2
        grant_exp(current_user, exp_gain)

        if monster.get("is_boss"):
            boss_bonus = random.randint(50, 150)
            print(f"🎉 You defeated the BOSS {monster['name']}! +${money_reward} money, +{exp_gain} EXP")
        else:
            normal_bonus = random.randint(5, 20)
            print(f"🎉 You defeated the {monster['name']}! +${money_reward} money, +{exp_gain} EXP")

        # Materials
        mats = monster.get("materials", [])
        for mat in mats:
            inventory[mat] = inventory.get(mat, 0) + 1
        if mats:
            print("You found:", ", ".join(mats))

        stats["monsters_defeated"] = stats.get("monsters_defeated", 0) + 1
        if monster.get("is_boss"):
            stats["bosses_defeated"] = stats.get("bosses_defeated", 0) + 1
        stats["total_money_earned"] = stats.get("total_money_earned", 0) + money_reward

        check_achievements(current_user)

    # Update buffs
    for b in active_buffs:
        if b["remaining"] > 0:
            b["remaining"] -= 1
    active_buffs = [b for b in active_buffs if b["remaining"] > 0]

    c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), current_user))
    conn.commit()

    conn.close()

# -------------------------
# Apply permanent upgrades function (needed for leveling)
# -------------------------
def apply_permanent_upgrades(username):
    """
    Apply all permanent upgrades from inventory to the player's stats.
    This function should be called after loading user data and before combat.
    """
    if username not in [user[0] for user in get_leaderboard()]:  # Simple check if user exists
        return

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if not result:
        conn.close()
        return

    player_data = json.loads(result[0])
    stats = player_data["stats"]
    inventory = player_data.get("inventory", {})

    # Reset permanent stats to base values
    base_stats = default_player_data()["stats"]
    for key in ["perm_atk", "perm_def", "perm_hp_max", "perm_mana_max", "perm_magic_def", "perm_crit_chance", "perm_mana_regen", "perm_lifesteal", "perm_lifesteal_chance", "perm_exp_boost"]:
        if key in stats:
            stats[key] = 0

    # Apply all permanent upgrades from inventory
    for perm_key, upgrade in PERM_UPGRADES.items():
        count = inventory.get(perm_key, 0)
        if count > 0:
            if "atk_increase" in upgrade:
                stats["perm_atk"] = stats.get("perm_atk", 0) + (upgrade["atk_increase"] * count)
            elif "def_increase" in upgrade:
                stats["perm_def"] = stats.get("perm_def", 0) + (upgrade["def_increase"] * count)
            elif "hp_increase" in upgrade:
                stats["perm_hp_max"] = stats.get("perm_hp_max", 0) + (upgrade["hp_increase"] * count)
            elif "magic_increase" in upgrade:
                stats["perm_mana_max"] = stats.get("perm_mana_max", 0) + (upgrade["magic_increase"] * count)
            elif "crit_chance_increase" in upgrade:
                stats["perm_crit_chance"] = stats.get("perm_crit_chance", 0) + (upgrade["crit_chance_increase"] * count)
            elif "mana_regen_increase" in upgrade:
                stats["perm_mana_regen"] = stats.get("perm_mana_regen", 0) + (upgrade["mana_regen_increase"] * count)
            elif "max_lifesteal_increase" in upgrade:
                stats["perm_lifesteal"] = stats.get("perm_lifesteal", 0) + (upgrade["max_lifesteal_increase"] * count)
            elif "lifesteal_chance_increase" in upgrade:
                stats["perm_lifesteal_chance"] = stats.get("perm_lifesteal_chance", 0) + (upgrade["lifesteal_chance_increase"] * count)
            elif "exp_increase" in upgrade:
                stats["perm_exp_boost"] = stats.get("perm_exp_boost", 0) + (upgrade["exp_increase"] * count)

    stats["hp"] = min(stats.get("hp", stats["hp_max"]), stats["hp_max"])
    stats["mana"] = min(stats.get("mana", stats["mana_max"]), stats["mana_max"])

    # Apply permanent stats to current stats only if they weren't manually set below default
    default_stats = default_player_data()["stats"]

    if not stats["stats_manually_set"]["atk"]:
        stats["atk"] = default_stats["atk"] + stats.get("perm_atk", 0)
    if not stats["stats_manually_set"]["defense"]:
        stats["defense"] = default_stats["defense"] + stats.get("perm_def", 0)
    if not stats["stats_manually_set"]["hp_max"]:
        stats["hp_max"] = default_stats["hp_max"] + stats.get("perm_hp_max", 0)
    if not stats["stats_manually_set"]["hp"]:
        stats["hp"] = min(stats.get("hp", stats["hp_max"]) + stats["hp_max"] // 4, stats["hp_max"])
    if not stats["stats_manually_set"]["mana_max"]:
        stats["mana_max"] = default_stats["mana_max"] + stats.get("perm_mana_max", 0)
    if not stats["stats_manually_set"]["mana"]:
        stats["mana"] = min(stats.get("mana", stats["mana_max"]) + stats["mana_max"] // 3, stats["mana_max"])

    # Ensure current HP/Mana don't exceed new max
    stats["hp"] = min(stats.get("hp", stats["hp_max"]), stats["hp_max"])
    stats["mana"] = min(stats.get("mana", stats["mana_max"]), stats["mana_max"])

    player_data["stats"] = stats
    c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), username))
    conn.commit()
    conn.close()

# -------------------------
# Magic Pack System
# -------------------------
MAGIC_PACKS = {
    "common_magic_pack": {
        "name": "Common Magic Pack",
        "tier": "D(Common)",
        "spells": ["spark", "ember", "aqua_jet", "gust", "stone_toss", "mana_bolt"],
        "drop_count": (1, 2), # min, max spells to give
        "description": "Contains 1-2 common spells"
    },
    "rare_magic_pack": {
        "name": "Rare Magic Pack",
        "tier": "C(Rare)",
        "spells": ["spark", "ember", "aqua_jet", "gust", "stone_toss", "mana_bolt",
        "fireball", "ice_spike", "shadow_shot", "thunder_strike", "poison_mist", "spark_chain"],
        "drop_count": (1, 3),
        "description": "Contains 1-3 spells (common or rare)"
    },
    "mythical_magic_pack": {
        "name": "Mythical Magic Pack",
        "tier": "B(Mythical)",
        "spells": ["fireball", "ice_spike", "shadow_shot", "thunder_strike", "poison_mist", "spark_chain",
        "meteor", "frost_nova", "void_bolt", "life_drain", "earth_quake", "glacial_prison"],
        "drop_count": (2, 4),
        "description": "Contains 2-4 spells (rare or mythical)"
    },
    "prismatic_magic_pack": {
        "name": "Prismatic Magic Pack",
        "tier": "A(Prismatic)",
        "spells": ["meteor", "frost_nova", "void_bolt", "life_drain", "earth_quake", "glacial_prison",
        "prism_beam", "lightning_storm", "aether_blast", "mirror_shield", "prismatic_orb", "prismatic_shard"],
        "drop_count": (2, 4),
        "description": "Contains 2-4 spells (mythical or prismatic)"
    },
    "divine_magic_pack": {
        "name": "Divine Magic Pack",
        "tier": "S(Divine)",
        "spells": ["prism_beam", "lightning_storm", "aether_blast", "mirror_shield", "prismatic_orb", "prismatic_shard",
        "divine_wrath", "holy_barrier", "celestial_fall", "purge", "resurgence", "spectral_bind"],
        "drop_count": (3, 5),
        "description": "Contains 3-5 spells (prismatic or divine)"
    },
    "transcendent_magic_pack": {
        "name": "Transcendent Magic Pack",
        "tier": "SS(Transcendent)",
        "spells": ["divine_wrath", "holy_barrier", "celestial_fall", "purge", "resurgence", "spectral_bind",
        "transcendence", "unmaking", "voidstorm", "eternal_echo", "reality_rend"],
        "drop_count": (3, 5),
        "description": "Contains 3-5 spells (divine or transcendent)"
    }
}

SPELLS_BY_KEY = {
    "spark": {"name": "Spark", "school": "D(Common)", "mana": 4, "power": 8, "lvl": 1, "desc": "Small electric spark."},
    "ember": {"name": "Ember", "school": "D(Common)", "mana": 4, "power": 9, "lvl": 1, "desc": "Tiny firebolt."},
    "aqua_jet": {"name": "Aqua Jet", "school": "D(Common)", "mana": 5, "power": 10, "lvl": 2, "desc": "Jet of water."},
    "gust": {"name": "Gust", "school": "D(Common)", "mana": 4, "power": 7, "lvl": 1, "desc": "Blows at enemy."},
    "stone_toss": {"name": "Stone Toss", "school": "D(Common)", "mana": 6, "power": 12, "lvl": 2, "desc": "Small rock hurled."},
    "mana_bolt": {"name": "Mana Bolt", "school": "D(Common)", "mana": 6, "power": 14, "lvl": 3, "desc": "Basic mana projectile."},
    "spark_chain": {"name": "Spark Chain", "school": "C(Rare)", "mana": 22, "power": 80, "lvl": 15, "desc": "Chaining sparks."},
    "fireball": {"name": "Fireball", "school": "C(Rare)", "mana": 15, "power": 40, "lvl": 10, "desc": "Explosive orb."},
    "ice_spike": {"name": "Ice Spike", "school": "C(Rare)", "mana": 14, "power": 36, "lvl": 9, "desc": "Sharp ice."},
    "shadow_shot": {"name": "Shadow Shot", "school": "C(Rare)", "mana": 16, "power": 45, "lvl": 11, "desc": "Dark bolt."},
    "thunder_strike": {"name": "Thunder Strike", "school": "C(Rare)", "mana": 18, "power": 50, "lvl": 12, "desc": "Powerful lightning."},
    "poison_mist": {"name": "Poison Mist", "school": "C(Rare)", "mana": 12, "power": 30, "lvl": 10, "desc": "Toxic cloud."},
    "meteor": {"name": "Meteor", "school": "B(Mythical)", "mana": 55, "power": 220, "lvl": 30, "desc": "Crushing meteor."},
    "frost_nova": {"name": "Frost Nova", "school": "B(Mythical)", "mana": 45, "power": 160, "lvl": 28, "desc": "Freezes area."},
    "void_bolt": {"name": "Void Bolt", "school": "B(Mythical)", "mana": 60, "power": 250, "lvl": 32, "desc": "Nullifying energy."},
    "life_drain": {"name": "Life Drain", "school": "B(Mythical)", "mana": 50, "power": 150, "lvl": 30, "desc": "Steal HP."},
    "earth_quake": {"name": "Earth Quake", "school": "B(Mythical)", "mana": 48, "power": 180, "lvl": 31, "desc": "Shake the ground."},
    "glacial_prison": {"name": "Glacial Prison", "school": "B(Mythical)", "mana": 70, "power": 300, "lvl": 35, "desc": "Encase the enemy."},
    "prism_beam": {"name": "Prism Beam", "school": "A(Prismatic)", "mana": 120, "power": 700, "lvl": 50, "desc": "Shredding beam."},
    "lightning_storm": {"name": "Lightning Storm", "school": "A(Prismatic)", "mana": 110, "power": 650, "lvl": 48, "desc": "Storm of lightning."},
    "aether_blast": {"name": "Aether Blast", "school": "A(Prismatic)", "mana": 100, "power": 600, "lvl": 46, "desc": "Pure aether."},
    "mirror_shield": {"name": "Mirror Shield", "school": "A(Prismatic)", "mana": 40, "power": 0, "lvl": 45, "desc": "Reflect attacks."},
    "prismatic_orb": {"name": "Prismatic Orb", "school": "A(Prismatic)", "mana": 90, "power": 520, "lvl": 47, "desc": "Orb of prismatic energy."},
    "prismatic_shard": {"name": "Prismatic Shard", "school": "A(Prismatic)", "mana": 95, "power": 560, "lvl": 52, "desc": "Shards of light."},
    "divine_wrath": {"name": "Divine Wrath", "school": "S(Divine)", "mana": 300, "power": 2000, "lvl": 75, "desc": "Wrath of the gods."},
    "holy_barrier": {"name": "Holy Barrier", "school": "S(Divine)", "mana": 120, "power": 0, "lvl": 70, "desc": "Major protection."},
    "celestial_fall": {"name": "Celestial Fall", "school": "S(Divine)", "mana": 250, "power": 1500, "lvl": 72, "desc": "Celestial impact."},
    "purge": {"name": "Purge", "school": "S(Divine)", "mana": 100, "power": 480, "lvl": 68, "desc": "Remove curses."},
    "resurgence": {"name": "Resurgence", "school": "S(Divine)", "mana": 200, "power": 0, "lvl": 74, "desc": "Large heal."},
    "spectral_bind": {"name": "Spectral Bind", "school": "S(Divine)", "mana": 180, "power": 820, "lvl": 66, "desc": "Bind spirit."},
    "transcendence": {"name": "Transcendence", "school": "SS(Transcendent)", "mana": 900, "power": 8000, "lvl": 95, "desc": "Transcend reality."},
    "unmaking": {"name": "Unmaking", "school": "SS(Transcendent)", "mana": 800, "power": 7000, "lvl": 90, "desc": "Unmake existence."},
    "voidstorm": {"name": "Voidstorm", "school": "SS(Transcendent)", "mana": 850, "power": 7500, "lvl": 92, "desc": "Storm of void."},
    "eternal_echo": {"name": "Eternal Echo", "school": "SS(Transcendent)", "mana": 950, "power": 8500, "lvl": 96, "desc": "Echo through eternity."},
    "reality_rend": {"name": "Reality Rend", "school": "SS(Transcendent)", "mana": 1000, "power": 9000, "lvl": 98, "desc": "Tear reality apart."}
}

MAGIC_PACK_ALIASES = {
    "common": "common_magic_pack",
    "c": "common_magic_pack",
    "rare": "rare_magic_pack",
    "r": "rare_magic_pack",
    "mythical": "mythical_magic_pack",
    "m": "mythical_magic_pack",
    "prismatic": "prismatic_magic_pack",
    "p": "prismatic_magic_pack",
    "divine": "divine_magic_pack",
    "d": "divine_magic_pack",
    "transcendent": "transcendent_magic_pack",
    "t": "transcendent_magic_pack",
}

def open_magic_pack(username, pack_key, quantity=1):
    if not any(user[0] == username for user in get_leaderboard()):  # Simple user check
        return False, "Invalid user."
    if pack_key not in MAGIC_PACKS:
        return False, "Unknown magic pack."

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if not result:
        conn.close()
        return False, "User data not found."

    player_data = json.loads(result[0])
    inventory = player_data.get("inventory", {})
    stats = player_data.get("stats", {})

    if inventory.get(pack_key, 0) < quantity:
        conn.close()
        return False, f"You don't have enough {MAGIC_PACKS[pack_key]['name']}."

    pack = MAGIC_PACKS[pack_key]
    spells_pool = pack["spells"]
    min_count, max_count = pack["drop_count"]

    # Initialize learned spells if not present
    if "learned_spells" not in stats:
        stats["learned_spells"] = []

    # Use the packs
    inventory[pack_key] -= quantity

    # Get random spells from the pool
    new_spells = []
    for _ in range(quantity):
        count = random.randint(min_count, max_count)
        for _ in range(count):
            spell_key = random.choice(spells_pool)
            if spell_key not in stats["learned_spells"]:
                stats["learned_spells"].append(spell_key)
                new_spells.append(SPELLS_BY_KEY[spell_key]["name"])

    player_data["inventory"] = inventory
    player_data["stats"] = stats
    c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), username))
    conn.commit()
    conn.close()

    if new_spells:
        return True, f"You opened {quantity} {pack['name']}(s) and learned: {', '.join(new_spells)}"
    else:
        return True, f"You opened {quantity} {pack['name']}(s) but didn't learn any new spells."

def parse_qty_from_choice(choice_str):
    parts = choice_str.split()
    if len(parts) >= 2:
        try:
            q = int(parts[1])
            if q < 1:
                q = 1
            return q, " ".join(parts[2:]) if len(parts) > 2 else ""
        except:
            return 1, " ".join(parts[1:])
    return 1, ""

# -------------------------
# User field normalization function
# -------------------------
def ensure_user_fields(username):
    """
    Normalize a user's data to ensure all expected keys exist so older saves won't crash.
    Call this after loading, signup, login, and before any operation that uses stats/inventory.
    """
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()

    if not result:
        conn.close()
        return

    try:
        player_data = json.loads(result[0])
    except json.JSONDecodeError:
        player_data = default_player_data()

    default = default_player_data()

    # Normalize stats: fill missing keys
    stats = player_data.get("stats", {})
    for k, v in default["stats"].items():
        if k not in stats:
            stats[k] = v

    # Ensure current_area exists
    if "current_area" not in stats:
        stats["current_area"] = 1

    # Normalize new fields
    if "learned_spells" not in stats:
        stats["learned_spells"] = []
    if "equipped_spells" not in stats:
        stats["equipped_spells"] = [None, None, None, None]
    if "available_titles" not in stats:
        stats["available_titles"] = []
    if "equipped_titles" not in stats:
        stats["equipped_titles"] = [None, None, None, None, None]
    for boost_field in ["title_atk_boost", "title_def_boost", "title_hp_boost", "title_mana_boost", "title_exp_boost"]:
        if boost_field not in stats:
            stats[boost_field] = 0
    # Ensure equipped has all slots
    if "equipped" not in stats or not isinstance(stats["equipped"], dict):
        stats["equipped"] = default["stats"]["equipped"].copy()
    else:
        for slot in default["stats"]["equipped"]:
            if slot not in stats["equipped"]:
                stats["equipped"][slot] = default["stats"]["equipped"][slot]

    # Ensure stats_manually_set exists
    if "stats_manually_set" not in stats:
        stats["stats_manually_set"] = default["stats"]["stats_manually_set"].copy()

    # Normalize inventory: ensure all default keys exist
    inventory = player_data.get("inventory", {})
    for k, v in default["inventory"].items():
        if k not in inventory:
            inventory[k] = v

    player_data["stats"] = stats
    player_data["inventory"] = inventory

    # Save the normalized data
    c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), username))
    conn.commit()
    conn.close()

# -------------------------
# Settings Menu
# -------------------------
def settings_menu(username):
    if not username:
        return

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if not result:
        conn.close()
        return

    player_data = json.loads(result[0])
    stats = player_data.get("stats", {})
    settings = stats.get("settings", {})

    while True:
        print("\n--- Settings ---")
        print(f"1. Show EXP bar: {'ON' if settings.get('show_exp_bar', False) else 'OFF'}")
        print(f"2. Auto-equip best items: {'ON' if settings.get('auto_equip_best', False) else 'OFF'}")
        print(f"3. Auto-equip spells: {'ON' if settings.get('auto_equip_spells', False) else 'OFF'}")
        print(f"4. Auto-equip titles: {'ON' if settings.get('auto_equip_titles', False) else 'OFF'}")
        print(f"5. Auto-equip everything: {'ON' if settings.get('auto_equip_everything', False) else 'OFF'}")
        print(f"6. Call including title: {'ON' if settings.get('call_including_title', True) else 'OFF'}")
        print("7. Equip Titles")
        print("8. Back to Main Menu")

        choice = input("Choose setting: ").strip()

        if choice == '1':
            settings['show_exp_bar'] = not settings.get('show_exp_bar', False)
            print(f"EXP bar display {'enabled' if settings['show_exp_bar'] else 'disabled'}.")
        elif choice == '2':
            settings['auto_equip_best'] = not settings.get('auto_equip_best', False)
            print(f"Auto-equip best items {'enabled' if settings['auto_equip_best'] else 'disabled'}.")
        elif choice == '3':
            settings['auto_equip_spells'] = not settings.get('auto_equip_spells', False)
            print(f"Auto-equip spells {'enabled' if settings['auto_equip_spells'] else 'disabled'}.")
        elif choice == '4':
            settings['auto_equip_titles'] = not settings.get('auto_equip_titles', False)
            print(f"Auto-equip titles {'enabled' if settings['auto_equip_titles'] else 'disabled'}.")
        elif choice == '5':
            settings['auto_equip_everything'] = not settings.get('auto_equip_everything', False)
            print(f"Auto-equip everything {'enabled' if settings['auto_equip_everything'] else 'disabled'}.")
        elif choice == '6':
            settings['call_including_title'] = not settings.get('call_including_title', True)
            print(f"Call including title {'enabled' if settings['call_including_title'] else 'disabled'}.")
        elif choice == '7':
            equip_titles_menu(username, player_data, c)
        elif choice == '8':
            break
        else:
            print("Invalid choice.")

        # Save settings
        stats['settings'] = settings
        player_data['stats'] = stats
        c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), username))
        conn.commit()

    conn.close()

# -------------------------
# Equip Titles Menu
# -------------------------
def equip_titles_menu(username, player_data, cursor):
    stats = player_data.get("stats", {})
    available_titles = stats.get("available_titles", [])
    equipped_titles = stats.get("equipped_titles", [None, None, None, None, None])

    while True:
        print("\n--- Equip Titles ---")
        for i in range(5):
            title = equipped_titles[i]
            print(f"{i+1}. Slot {i+1}: {TITLES.get(title, {}).get('name', 'None') if title else 'None'}")

        print("\nAvailable Titles:")
        for i, title_key in enumerate(available_titles, start=1):
            title_name = TITLES.get(title_key, {}).get('name', title_key)
            print(f"{i+5}. {title_name}")

        print("0. Back")

        choice = input("Choose slot to equip/unequip or title to equip: ").strip()

        if choice == '0':
            break
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < 5:  # Unequip slot
                equipped_titles[idx] = None
                print(f"Unequipped slot {idx+1}.")
            elif 5 <= idx < 5 + len(available_titles):  # Equip title
                title_idx = idx - 5
                title_key = available_titles[title_idx]
                # Find first empty slot
                empty_slots = [i for i, t in enumerate(equipped_titles) if t is None]
                if empty_slots:
                    slot = empty_slots[0]
                    equipped_titles[slot] = title_key
                    print(f"Equipped {TITLES[title_key]['name']} in slot {slot+1}.")
                else:
                    print("No empty slots. Unequip a slot first.")
            else:
                print("Invalid choice.")
        else:
            print("Invalid choice.")

    # Apply title boosts
    apply_title_boosts(stats)
    player_data['stats'] = stats
    cursor.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), username))

# -------------------------
# Apply Title Boosts
# -------------------------
def apply_title_boosts(stats):
    equipped_titles = stats.get("equipped_titles", [None] * 5)
    total_atk = 0
    total_def = 0
    total_hp = 0
    total_mana = 0
    total_exp = 0
    for title_key in equipped_titles:
        if title_key and title_key in TITLES:
            title = TITLES[title_key]
            total_atk += title.get("atk_boost", 0)
            total_def += title.get("def_boost", 0)
            total_hp += title.get("hp_boost", 0)
            total_mana += title.get("mana_boost", 0)
            total_exp += title.get("exp_boost", 0)

    stats["title_atk_boost"] = total_atk
    stats["title_def_boost"] = total_def
    stats["title_hp_boost"] = total_hp
    stats["title_mana_boost"] = total_mana
    stats["title_exp_boost"] = total_exp

# -------------------------
# Auto Equip Items
# -------------------------
def auto_equip_items(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if not result:
        conn.close()
        return

    player_data = json.loads(result[0])
    stats = player_data['stats']
    inventory = player_data['inventory']
    settings = stats.get('settings', {})

    equipped = stats.get('equipped', {})

    if settings.get('auto_equip_best') or settings.get('auto_equip_everything'):
        # Equip best weapon
        best_weapon = None
        best_atk = equipped.get('weapon') and WEAPONS.get(equipped['weapon'], {}).get('atk', 0) or 0
        for w_key, w_data in WEAPONS.items():
            if inventory.get(w_key, 0) > 0 and w_data['atk'] > best_atk:
                best_weapon = w_key
                best_atk = w_data['atk']
        if best_weapon:
            equipped['weapon'] = best_weapon
            print(f"Auto-equipped {WEAPONS[best_weapon]['name']} as weapon.")

        # Equip best armor
        best_armor = None
        best_def = equipped.get('armor') and ARMORS.get(equipped['armor'], {}).get('def', 0) or 0
        for a_key, a_data in ARMORS.items():
            if inventory.get(a_key, 0) > 0 and a_data['def'] > best_def:
                best_armor = a_key
                best_def = a_data['def']
        if best_armor:
            equipped['armor'] = best_armor
            print(f"Auto-equipped {ARMORS[best_armor]['name']} as armor.")

        # Equip best wand
        best_wand = None
        best_magic_atk = equipped.get('wand') and WANDS.get(equipped['wand'], {}).get('magic_atk', 0) or 0
        for w_key, w_data in WANDS.items():
            if inventory.get(w_key, 0) > 0 and w_data['magic_atk'] > best_magic_atk:
                best_wand = w_key
                best_magic_atk = w_data['magic_atk']
        if best_wand:
            equipped['wand'] = best_wand
            print(f"Auto-equipped {WANDS[best_wand]['name']} as wand.")

        # Equip best robe
        best_robe = None
        best_magic_def = equipped.get('robe') and ROBES.get(equipped['robe'], {}).get('magic_def', 0) or 0
        for r_key, r_data in ROBES.items():
            if inventory.get(r_key, 0) > 0 and r_data['magic_def'] > best_magic_def:
                best_robe = r_key
                best_magic_def = r_data['magic_def']
        if best_robe:
            equipped['robe'] = best_robe
            print(f"Auto-equipped {ROBES[best_robe]['name']} as robe.")

        # Equip best necklace
        best_necklace = None
        best_hp = equipped.get('necklace') and NECKLACES.get(equipped['necklace'], {}).get('hp_bonus', 0) or 0
        for n_key, n_data in NECKLACES.items():
            if inventory.get(n_key, 0) > 0 and n_data.get('hp_bonus', 0) > best_hp:
                best_necklace = n_key
                best_hp = n_data['hp_bonus']
        if best_necklace:
            equipped['necklace'] = best_necklace
            print(f"Auto-equipped {NECKLACES[best_necklace]['name']} as necklace.")

    if settings.get('auto_equip_spells') or settings.get('auto_equip_everything'):
        learned_spells = stats.get('learned_spells', [])
        equipped_spells = stats.get('equipped_spells', [None, None, None, None])
        # Sort learned spells by power desc
        sorted_spells = sorted(learned_spells, key=lambda s: SPELLS_BY_KEY.get(s, {}).get('power', 0), reverse=True)
        for i in range(4):
            if i < len(sorted_spells):
                equipped_spells[i] = sorted_spells[i]
        stats['equipped_spells'] = equipped_spells
        print("Auto-equipped best spells.")

    if settings.get('auto_equip_titles') or settings.get('auto_equip_everything'):
        available_titles = stats.get('available_titles', [])
        equipped_titles = stats.get('equipped_titles', [None] * 5)
        # Sort by rarity or some score
        title_scores = {}
        for t_key in available_titles:
            title_scores[t_key] = get_rarity_value(TITLES.get(t_key, {}).get('rarity', 'common'))
        sorted_titles = sorted(available_titles, key=lambda t: title_scores.get(t, 0), reverse=True)
        for i in range(5):
            if i < len(sorted_titles):
                equipped_titles[i] = sorted_titles[i]
        stats['equipped_titles'] = equipped_titles
        apply_title_boosts(stats)
        print("Auto-equipped best titles.")

    player_data['stats'] = stats
    player_data['inventory'] = inventory
    c.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), username))
    conn.commit()
    conn.close()

# -------------------------
# Manage Inventory Menu
# -------------------------
def manage_inventory_menu(username, player_data, cursor):
    stats = player_data['stats']
    inventory = player_data['inventory']
    equipped = stats.get('equipped', {})

    while True:
        print("\n--- Manage Inventory ---")
        print(f"Money: {player_data['money']}")
        print("Equipped:")
        weapon = equipped.get('weapon')
        print(f"  Weapon: {WEAPONS.get(weapon, {}).get('name', 'None') if weapon else 'None'}")
        armor = equipped.get('armor')
        print(f"  Armor: {ARMORS.get(armor, {}).get('name', 'None') if armor else 'None'}")
        wand = equipped.get('wand')
        print(f"  Wand: {WANDS.get(wand, {}).get('name', 'None') if wand else 'None'}")
        robe = equipped.get('robe')
        print(f"  Robe: {ROBES.get(robe, {}).get('name', 'None') if robe else 'None'}")
        necklace = equipped.get('necklace')
        print(f"  Necklace: {NECKLACES.get(necklace, {}).get('name', 'None') if necklace else 'None'}")

        print("\nInventory:")
        item_list = []
        for key, count in inventory.items():
            if count > 0:
                name = "Unknown"
                if key in WEAPONS: name = WEAPONS[key]['name']
                elif key in ARMORS: name = ARMORS[key]['name']
                elif key in WANDS: name = WANDS[key]['name']
                elif key in ROBES: name = ROBES[key]['name']
                elif key in NECKLACES: name = NECKLACES[key]['name']
                else: continue  # Skip non-equip items
                item_list.append((key, name, count))
                print(f"  {len(item_list)}. {name} x{count}")

        print("0. Back")

        choice = input("Choose item to equip (number), or 'u' + slot to unequip (e.g. u1 for weapon): ").strip().lower()

        if choice == '0':
            break
        elif choice.startswith('u'):
            slot_num = choice[1:]
            if slot_num == '1':
                equipped['weapon'] = None
                print("Unequipped weapon.")
            elif slot_num == '2':
                equipped['armor'] = None
                print("Unequipped armor.")
            elif slot_num == '3':
                equipped['wand'] = None
                print("Unequipped wand.")
            elif slot_num == '4':
                equipped['robe'] = None
                print("Unequipped robe.")
            elif slot_num == '5':
                equipped['necklace'] = None
                print("Unequipped necklace.")
            else:
                print("Invalid slot.")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(item_list):
                item_key, item_name, count = item_list[idx]
                if item_key in WEAPONS:
                    equipped['weapon'] = item_key
                    print(f"Equipped {item_name} as weapon.")
                elif item_key in ARMORS:
                    equipped['armor'] = item_key
                    print(f"Equipped {item_name} as armor.")
                elif item_key in WANDS:
                    equipped['wand'] = item_key
                    print(f"Equipped {item_name} as wand.")
                elif item_key in ROBES:
                    equipped['robe'] = item_key
                    print(f"Equipped {item_name} as robe.")
                elif item_key in NECKLACES:
                    equipped['necklace'] = item_key
                    print(f"Equipped {item_name} as necklace.")
            else:
                print("Invalid choice.")
        else:
            print("Invalid choice.")

    player_data['stats'] = stats
    player_data['inventory'] = inventory
    cursor.execute('UPDATE users SET player_data = ? WHERE username = ?', (json.dumps(player_data), username))

# -------------------------
# View Achievements Menu
# -------------------------
def view_achievements_menu(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT player_data FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if not result:
        conn.close()
        return

    player_data = json.loads(result[0])
    stats = player_data['stats']
    unlocked = stats.get('achievements', [])

    print("\n--- Achievements ---")
    for ach_key, achievement in ACHIEVEMENTS.items():
        status = "✓" if ach_key in unlocked else "✗"
        print(f"{status} {achievement['name']}: {achievement['desc']}")

    conn.close()

# -------------------------
# Effective stats computation (includes equipped wand/robe/necklace)
# -------------------------
def compute_effective_stats(stats, active_buffs):
    base_atk = stats.get("atk",5)
    base_def = stats.get("defense",0)
    base_magic_atk = 0
    base_magic_def = 0

    weapon = stats.get("equipped",{}).get("weapon")
    armor = stats.get("equipped",{}).get("armor")
    wand = stats.get("equipped",{}).get("wand")
    robe = stats.get("equipped",{}).get("robe")
    necklace = stats.get("equipped",{}).get("necklace")

    w_atk = WEAPONS.get(weapon,{}).get("atk",0) if weapon else 0
    a_def = ARMORS.get(armor,{}).get("def",0) if armor else 0
    wand_magic = WANDS.get(wand,{}).get("magic_atk",0) if wand else 0
    robe_def = ROBES.get(robe,{}).get("magic_def",0) if robe else 0

    # Necklace bonuses
    n_atk = NECKLACES.get(necklace,{}).get("atk_bonus",0) if necklace else 0
    n_def = NECKLACES.get(necklace,{}).get("def_bonus",0) if necklace else 0
    n_hp = NECKLACES.get(necklace,{}).get("hp_bonus",0) if necklace else 0
    n_mana = NECKLACES.get(necklace,{}).get("mana_bonus",0) if necklace else 0
    n_crit = NECKLACES.get(necklace,{}).get("crit_bonus",0) if necklace else 0
    n_lifesteal = NECKLACES.get(necklace,{}).get("lifesteal_bonus",0) if necklace else 0
    n_magic_atk = NECKLACES.get(necklace,{}).get("magic_atk_bonus",0) if necklace else 0
    n_magic_def = NECKLACES.get(necklace,{}).get("magic_def_bonus",0) if necklace else 0

    # Title bonuses
    t_atk = stats.get("title_atk_boost", 0)
    t_def = stats.get("title_def_boost", 0)
    t_hp = stats.get("title_hp_boost", 0)
    t_mana = stats.get("title_mana_boost", 0)
    t_atk_percent = stats.get("title_atk_percent", 0)
    t_def_percent = stats.get("title_def_percent", 0)
    t_hp_percent = stats.get("title_hp_percent", 0)
    t_mana_percent = stats.get("title_mana_percent", 0)

    atk_buff = sum(b["amount"] for b in active_buffs if b["type"]=="atk" and b["remaining"]>0)
    def_buff = sum(b["amount"] for b in active_buffs if b["type"]=="def" and b["remaining"]>0)

    # Calculate effective stats before percent multipliers
    effective_atk = base_atk + w_atk + n_atk + t_atk + atk_buff
    effective_def = base_def + a_def + n_def + t_def + def_buff
    effective_magic_atk = wand_magic + n_magic_atk
    effective_magic_def = robe_def + n_magic_def
    effective_hp_bonus = n_hp + t_hp
    effective_mana_bonus = n_mana + t_mana

    # Apply percent multipliers
    effective_atk = int(effective_atk * (1 + t_atk_percent / 100.0))
    effective_def = int(effective_def * (1 + t_def_percent / 100.0))
    effective_hp_bonus = int(effective_hp_bonus * (1 + t_hp_percent / 100.0))
    effective_mana_bonus = int(effective_mana_bonus * (1 + t_mana_percent / 100.0))

    return effective_atk, effective_def, effective_magic_atk, effective_magic_def, effective_hp_bonus, effective_mana_bonus, n_crit, n_lifesteal

def main_menu():
    current_user = None
    score = 0
    player_data = None
    money = 40

    while True:
        if current_user:
            print(f"\nLogged in as: {current_user}")
            print("1. Play number guessing game")
            print("2. Explore dungeons")
            print("3. Settings")
            print("4. Leaderboard")
            print("5. Logout")
            print("6. Exit")
        else:
            print("\nMain Menu")
            print("1. Login")
            print("2. Signup")
            print("3. Leaderboard")
            print("4. Exit")

        choice = input("Choose an option: ").strip()

        if current_user:
            if choice == '1':
                score = guessing_game(current_user, score)
                # Data is already saved via update_user in the functions
            elif choice == '2':
                dungeon()
                # Reload data after dungeon
                score, money, player_data = signin(current_user, password="")
            elif choice == '3':
                settings_menu(current_user)
                # Reload data after settings
                score, money, player_data = signin(current_user, password="")
            elif choice == '4':
                if get_leaderboard():
                    print("\n--- Leaderboard ---")
                    leaderboard = get_leaderboard()
                    for rank, (uname, user_score) in enumerate(leaderboard, start=1):
                        print(f"{rank}. {uname} - {user_score}")
                else:
                    print("No users yet!")
            elif choice == '5':
                print("Logged out.")
                stop_autosave()  # Stop autosave when logging out
                current_user = None
                score = 0
                player_data = None
                money = 40
            elif choice == '6':
                print("Goodbye! Data saved automatically.")
                save_all_data()
                break
            else:
                print("Invalid choice.")
        else:
            if choice == '1':
                username = input("Username: ").strip().lower()
                password = input("Password: ").strip()
                score, money, player_data = signin(username, password)
                if score is not None:
                    current_user = username
                    ensure_user_fields(current_user)
                    # Reload updated player data
                    _, _, player_data = signin(username, password)
                    print(f"Login successful! Highscore = {score}")
                else:
                    print("Login failed!")
            elif choice == '2':
                username = input("\nUsername: ").strip()
                password = input("Password: ").strip()
                if signup(username, password):
                    score, money, player_data = signin(username, password)
                    pass  # Already printed success
                else:
                    pass  # Already printed error
            elif choice == '3':
                if get_leaderboard():
                    print("\n--- Leaderboard ---")
                    leaderboard = get_leaderboard()
                    for rank, (uname, user_score) in enumerate(leaderboard, start=1):
                        print(f"{rank}. {uname} - {user_score}")
                else:
                    print("No users yet!")
            elif choice == '4':
                print("Goodbye! Data saved automatically.")
                break
            else:
                print("Oops, looks like you accidentally pressed the wrong button. Go again")
                continue

if __name__ == "__main__":
    setup_db()
    # start_autosave()  # Commented out for now - threading might cause issues
    atexit.register(save_all_data)
    main_menu()