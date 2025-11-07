
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

    conn.close()
    return lvls_gained

# -------------------------
# Dungeon treasure persistence
# -------------------------
def load_dungeon_treasure():
    global dungeon_treasure
    if os.path.exists(DUNGEON_TREASURE_FILE):
        try:
            with open(DUNGEON_TREASURE_FILE, "r") as f:
                data = json.load(f)
                dungeon_treasure = int(data.get("treasure", 0))
        except Exception:
            dungeon_treasure = 0
    else:
        dungeon_treasure = 0

    # If dungeon treasure is below 200,000, reroll to between 200,000 and 1,000,000
    if dungeon_treasure < 200000:
        dungeon_treasure = random.randint(200000, 1000000)
        save_dungeon_treasure()

def save_dungeon_treasure():
    global dungeon_treasure
    try:
        with open(DUNGEON_TREASURE_FILE, "w") as f:
            json.dump({"treasure": int(dungeon_treasure)}, f)
        return True
    except Exception as e:
        print(f"Error saving dungeon treasure: {e}")
        return False

load_dungeon_treasure()

# -------------------------
# Autosave functions
# -------------------------
def save_all_data():
    users_saved = save_users()
    treasure_saved = save_dungeon_treasure()
    return users_saved and treasure_saved

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

def get_leaderboard():
    """Get leaderboard from SQLite database"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, score FROM users ORDER BY score DESC LIMIT 10')
    results = c.fetchall()
    conn.close()
    return results

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

def main_menu():
    current_user = None
    score = 0
    player_data = None
    money = 40

    while True:
        if current_user:
            print(f"\nLogged in as: {current_user}")
            print("1. Play number guessing game")
            print("2. Leaderboard")
            print("3. Logout")
            print("4. Exit")
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
                update_user(current_user, score, money, player_data)
            elif choice == '2':
                if get_leaderboard():
                    print("\n--- Leaderboard ---")
                    leaderboard = get_leaderboard()
                    for rank, (uname, user_score) in enumerate(leaderboard, start=1):
                        print(f"{rank}. {uname} - {user_score}")
                else:
                    print("No users yet!")
            elif choice == '3':
                print("Logged out.")
                stop_autosave()  # Stop autosave when logging out
                current_user = None
                score = 0
                player_data = None
                money = 40
            elif choice == '4':
                print("Goodbye! Data saved automatically.")
                save_all_data()
                break
            else:
                print("Invalid choice.")
        else:
            if choice == '1':
                username = input("Username: ").strip()
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
                save_users()
                break
            else:
                print("Oops, looks like you accidentally pressed the wrong button. Go again")
                continue

if __name__ == "__main__":
    setup_db()
    # start_autosave()  # Commented out for now - threading might cause issues
    atexit.register(save_all_data)
    main_menu()