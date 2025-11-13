import json
import random
import os
import math
import time
import atexit
import threading
import socket

# -------------------------
# Files & persistence
# -------------------------
USERS_DIR = "users.txt"
DUNGEON_TREASURE_FILE = "dungeon_treasure.json"

# -------------------------
# Globals
# -------------------------
dungeon_treasure = 0
GLOBAL_KEY = "__global__"

AUTOSAVE_INTERVAL = 30  # Autosave every 30 seconds for simplicity
autosave_timer = None
last_autosave_time = time.time()

# -------------------------
# Machine Identification
# -------------------------
def get_machine_id():
    """Get a unique identifier for this machine"""
    try:
        hostname = socket.gethostname()
        return hostname
    except:
        return "unknown_machine"

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
    if level <= 10 and level >= 20:
        level_title = "Novice"
    elif level <= 20 and level >= 20:
        level_title = "Apprentice"
    elif level <= 30 and level >= 20:
        level_title = "Warrior"
    elif level <= 40 and level >= 20:
        level_title = "Champion"
    elif level <= 50 and level >= 20:
        level_title = "Hero"
    elif level <= 60 and level >= 20:
        level_title = "Legend"
    elif level <= 70 and level >= 20:
        level_title = "Master"
    elif level <= 80 and level >= 20:
        level_title = "Grandmaster"
    elif level <= 90 and level >= 20:
        level_title = "Mythic"
    elif level <= 99 and level >= 20:
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
    try:
        user_data = load_user_data(username)
        if not user_data:
            return []

        player_data = user_data.get("player_data", {})
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
                # Find the key for the new title
                title_key = None
                for k, v in TITLES.items():
                    if v['name'] == new_title:
                        title_key = k
                        break
                if title_key and title_key not in stats.get("available_titles", []):
                    stats["available_titles"].append(title_key)
                print(f"🎉 New title unlocked: '{new_title}'!")

            player_data["stats"] = stats
            user_data["player_data"] = player_data
            save_user_data(username, user_data)

        return new_achievements
    except Exception as e:
        print(f"Error checking achievements: {e}")
        return []

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
    try:
        user_data = load_user_data(username)
        if not user_data:
            return []

        player_data = user_data.get("player_data", {})
        stats = player_data["stats"]
        lvls_gained = []
        if stats.get("level", 1) >= MAX_LEVEL:
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

        player_data["stats"] = stats
        user_data["player_data"] = player_data
        save_user_data(username, user_data)
    except Exception as e:
        print(f"Error granting experience: {e}")
        return []

    # Apply permanent upgrades after level up
    apply_permanent_upgrades(username)

    # Auto-equip items if enabled
    auto_equip_items(username)

    return lvls_gained

# -------------------------
# Dungeon treasure persistence (SQLite-based now, but keep global for compatibility)
# -------------------------
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
            json.dump({"treasure": int(dungeon_treasure)}, f)
        os.replace(temp_file, DUNGEON_TREASURE_FILE)
        try:
            os.remove(lock_file)
        except:
            pass
        return True
    except Exception as e:
        print(f"Error saving dungeon treasure: {e}")
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
                dungeon_treasure = int(data.get("treasure", random.randint(200000, 1000000)))
        else:
            dungeon_treasure = random.randint(200000, 1000000)

        # If dungeon treasure is below 200,000, reroll it
        if dungeon_treasure < 200000:
            dungeon_treasure = random.randint(200000, 1000000)
            save_dungeon_treasure()
    except Exception as e:
        print(f"Error loading dungeon treasure: {e}")
        dungeon_treasure = random.randint(200000, 1000000)

load_dungeon_treasure()

# -------------------------
# Autosave functions
# -------------------------
def save_all_data():
    save_dungeon_treasure()

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

adminQanswers = ["31,10,2011","31\10\2011","31/10/2011","31.10.2011"]

def stop_autosave():
    """Stop the autosave timer"""
    global autosave_timer

    if autosave_timer is not None:
        autosave_timer.cancel()
        autosave_timer = None

# -------------------------
# Save & Load functions (SQLite-based)
# -------------------------

def setup_db():
    """Create users.txt file if it doesn't exist and migrate old data"""
    if os.path.isdir(USERS_DIR):
        # Migrate from old directory structure
        users = {}
        if os.path.exists("users"):
            for filename in os.listdir("users"):
                if filename.endswith('.json'):
                    username = filename[:-5]
                    with open(os.path.join("users", filename), 'r') as f:
                        users[username] = json.load(f)
        # Write to users.txt
        with open(USERS_DIR, 'w') as f:
            json.dump(users, f, indent=4)
        # Optionally remove old directory
        import shutil
        shutil.rmtree("users")
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
    save_all_users(users)

def signup(username, password):
    users = load_all_users()
    if username in users:
        print("Username already exists!")
        return False
    user_data = {
        "username": username,
        "password": password,
        "score": 0,
        "money": 40,
        "player_data": default_player_data(),
        "machine_homes": []  # List of machine IDs where this account is set as home
    }
    users[username] = user_data
    save_all_users(users)
    print("Signup successful!")
    return True

def signin(username, password):
    user_data = load_user_data(username)
    if user_data and user_data.get("password") == password:
        return user_data.get("score", 0), user_data.get("money", 40), user_data.get("player_data", default_player_data())
    else:
        return None, None, None

def set_machine_home(username, machine_id=None):
    """Set this machine as a home machine for the account"""
    if not machine_id:
        machine_id = get_machine_id()
    users = load_all_users()
    if username in users:
        if "machine_homes" not in users[username]:
            users[username]["machine_homes"] = []
        if machine_id not in users[username]["machine_homes"]:
            users[username]["machine_homes"].append(machine_id)
            save_all_users(users)
            print(f"This machine ({machine_id}) is now set as a home machine for {username}.")
        else:
            print(f"This machine is already set as a home machine for {username}.")
    else:
        print("User not found.")

def get_home_accounts_for_machine(machine_id=None):
    """Get list of accounts that have this machine set as home"""
    if not machine_id:
        machine_id = get_machine_id()
    users = load_all_users()
    home_accounts = []
    for username, user_data in users.items():
        if machine_id in user_data.get("machine_homes", []):
            home_accounts.append(username)
    return home_accounts

def update_user(username, score=None, money=None, player_data=None):
    users = load_all_users()
    if username in users:
        if score is not None:
            users[username]["score"] = score
        if money is not None:
            users[username]["money"] = money
        if player_data is not None:
            users[username]["player_data"] = player_data
        save_all_users(users)

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
        "score": 0,
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
    area_monsters = [m for m in MONSTERS if m.get("area", area) == area and not m["is_boss"]]
    if not area_monsters:
        # Fallback to any non-boss monster
        area_monsters = [m for m in MONSTERS if not m["is_boss"]]

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
    area_bosses = [m for m in MONSTERS if m.get("area", area) == area and m["is_boss"]]
    if not area_bosses:
        # Fallback to any boss
        area_bosses = [m for m in MONSTERS if m["is_boss"]]

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
    return next(m for m in MONSTERS if m["is_boss"])

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
    equip = stats.get("equipped", {})

    # equipment values (safe defaults)
    w_atk = WEAPONS.get(equip.get("weapon"), {}).get("atk", 0)
    n_atk = NECKLACES.get(equip.get("necklace"), {}).get("atk_bonus", 0)
    a_def = ARMORS.get(equip.get("armor"), {}).get("def", 0)
    n_def = NECKLACES.get(equip.get("necklace"), {}).get("def_bonus", 0)
    robe_magic = ROBES.get(equip.get("robe"), {}).get("magic_def", 0)

    # permanent / title values (these should be added to stats by apply_permanent_upgrades)
    perm_atk = stats.get("perm_atk", 0)
    perm_def = stats.get("perm_def", 0)
    perm_magic_def = stats.get("perm_magic_def", 0)

    title_atk_boost = stats.get("title_atk_boost", 0)
    title_def_boost = stats.get("title_def_boost", 0)
    title_magic_def = stats.get("title_magic_def", 0)

    # base defaults (base_base_atk = default atk (5) unless stats has override)
    base_base_atk = stats.get("atk", 5)
    base_base_def = stats.get("defense", 0)

    # Combine base + perm + title
    total_base_atk = base_base_atk + perm_atk + title_atk_boost
    total_base_def = base_base_def + perm_def + title_def_boost
    total_magic_def = robe_magic + perm_magic_def + title_magic_def

    return {
        "weapon_atk": w_atk,
        "neck_atk": n_atk,
        "armor_def": a_def,
        "neck_def": n_def,
        "robe_magic_def": robe_magic,
        "perm_atk": perm_atk,
        "perm_def": perm_def,
        "perm_magic_def": perm_magic_def,
        "total_base_atk": total_base_atk,
        "total_base_def": total_base_def,
        "total_magic_def": total_magic_def
    }

def calculate_total_crit_chance(stats, active_buffs):
    """Return combined crit chance (perm + active crit buffs). All in 0..1."""
    total = stats.get("perm_crit_chance", 0) / 100.0
    for b in active_buffs:
        if b.get("type") == "crit" and b.get("remaining", 0) > 0:
            total += b.get("amount", 0) / 100.0
    return total

MONSTERS = [
# Area 1 Monsters (Level 1-5)
{"name": "Slime", "hp": 8, "atk_min": 1, "atk_max": 3, "money_min": 2, "money_max": 7, "class": "D(Common)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.25, "slime_gel": 0.4}, "weight": 18, "area": 1},
{"name": "Goblin", "hp": 10, "atk_min": 3, "atk_max": 5, "money_min": 4, "money_max": 15, "class": "D(Common)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.3, "strength_boost": 0.05, "goblin_tooth": 0.3}, "weight": 15, "area": 1},
{"name": "Wolf", "hp": 12, "atk_min": 3, "atk_max": 6, "money_min": 10, "money_max": 22, "class": "D(Common)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "wolf_pelt": 0.3}, "weight": 14, "area": 1},
{"name": "Goblin Shaman", "hp": 20, "magic_atk_min": 8, "magic_atk_max": 12, "money_min": 10, "money_max": 25, "class": "C(Rare)", "is_boss": False, "is_super_boss": False, "drop": {"mana_regen_potion": 0.1, "goblin_tooth": 0.2}, "weight": 8, "area": 1},
{"name": "Forest Sprite", "hp": 15, "atk_min": 2, "atk_max": 5, "money_min": 8, "money_max": 20, "class": "D(Common)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.25, "mana_regen_potion": 0.1, "crystal_shard": 0.2}, "weight": 12, "area": 1},

# Area 2 Monsters (Level 6-10)
{"name": "Skeleton", "hp": 20, "atk_min": 4, "atk_max": 7, "money_min": 15, "money_max": 30, "class": "D(Common)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.25, "defense_boost": 0.05, "skeleton_bone": 0.4}, "weight": 12, "area": 2},
{"name": "Orc", "hp": 30, "atk_min": 5, "atk_max": 8, "money_min": 20, "money_max": 40, "class": "D(Common)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "orc_iron": 0.3}, "weight": 10, "area": 2},
{"name": "Giant Spider", "hp": 25, "atk_min": 6, "atk_max": 9, "money_min": 25, "money_max": 45, "class": "D(Common)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "crit_boost": 0.05, "spider_venom": 0.3}, "weight": 8, "area": 2},
{"name": "Dark Bat", "hp": 18, "atk_min": 5, "atk_max": 8, "money_min": 18, "money_max": 35, "class": "D(Common)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "bat_wing": 0.3}, "weight": 10, "area": 2},

# Area 3 Monsters (Level 11-15) - 10% chance for all permanent upgrades
{"name": "Bandit", "hp": 40, "atk_min": 7, "atk_max": 12, "money_min": 35, "money_max": 60, "class": "C(Rare)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.15, "crit_boost": 0.04, "common_magic_pack": 0.15, "bandit_cloth": 0.3, "perm_exp_upgrade": 0.1, "perm_strength_upgrade": 0.1, "perm_defense_upgrade": 0.1, "perm_health_upgrade": 0.1, "perm_mana_upgrade": 0.1, "perm_crit_chance_upgrade": 0.1, "perm_mana_regen_upgrade": 0.1, "perm_lifesteal_upgrade": 0.1, "perm_lifesteal_chance_upgrade": 0.1}, "weight": 10, "area": 3},
{"name": "Orc Warrior", "hp": 55, "atk_min": 8, "atk_max": 13, "money_min": 40, "money_max": 70, "class": "C(Rare)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "orc_iron": 0.4, "strength_boost": 0.1, "perm_exp_upgrade": 0.1, "perm_strength_upgrade": 0.1, "perm_defense_upgrade": 0.1, "perm_health_upgrade": 0.1, "perm_mana_upgrade": 0.1, "perm_crit_chance_upgrade": 0.1, "perm_mana_regen_upgrade": 0.1, "perm_lifesteal_upgrade": 0.1, "perm_lifesteal_chance_upgrade": 0.1}, "weight": 8, "area": 3},
{"name": "Dark Mage", "hp": 45, "magic_atk_min": 10, "magic_atk_max": 15, "money_min": 50, "money_max": 80, "class": "C(Rare)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.25, "strength_boost": 0.06, "common_magic_pack": 0.25, "rare_magic_pack": 0.1, "dark_essence": 0.2, "perm_exp_upgrade": 0.1, "perm_strength_upgrade": 0.1, "perm_defense_upgrade": 0.1, "perm_health_upgrade": 0.1, "perm_mana_upgrade": 0.1, "perm_crit_chance_upgrade": 0.1, "perm_mana_regen_upgrade": 0.1, "perm_lifesteal_upgrade": 0.1, "perm_lifesteal_chance_upgrade": 0.1}, "weight": 7, "area": 3},
{"name": "Stone Golem", "hp": 70, "atk_min": 6, "atk_max": 10, "money_min": 45, "money_max": 75, "class": "C(Rare)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "defense_boost": 0.1, "stone_core": 0.3, "perm_exp_upgrade": 0.1, "perm_strength_upgrade": 0.1, "perm_defense_upgrade": 0.1, "perm_health_upgrade": 0.1, "perm_mana_upgrade": 0.1, "perm_crit_chance_upgrade": 0.1, "perm_mana_regen_upgrade": 0.1, "perm_lifesteal_upgrade": 0.1, "perm_lifesteal_chance_upgrade": 0.1}, "weight": 6, "area": 3},

# Area 4 Monsters (Level 16-20) - 10% chance for all permanent upgrades
{"name": "Troll", "hp": 90, "atk_min": 12, "atk_max": 18, "money_min": 80, "money_max": 120, "class": "C(Rare)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "regen_potion": 0.05, "common_magic_pack": 0.1, "rare_magic_pack": 0.05, "troll_core": 0.3, "perm_exp_upgrade": 0.1, "perm_strength_upgrade": 0.1, "perm_defense_upgrade": 0.1, "perm_health_upgrade": 0.1, "perm_mana_upgrade": 0.1, "perm_crit_chance_upgrade": 0.1, "perm_mana_regen_upgrade": 0.1, "perm_lifesteal_upgrade": 0.1, "perm_lifesteal_chance_upgrade": 0.1}, "weight": 6, "area": 4},
{"name": "Ice Elemental", "hp": 75, "magic_atk_min": 15, "magic_atk_max": 20, "money_min": 90, "money_max": 130, "class": "C(Rare)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "frozen_heart": 0.3, "ice_shard": 0.2, "perm_exp_upgrade": 0.1, "perm_strength_upgrade": 0.1, "perm_defense_upgrade": 0.1, "perm_health_upgrade": 0.1, "perm_mana_upgrade": 0.1, "perm_crit_chance_upgrade": 0.1, "perm_mana_regen_upgrade": 0.1, "perm_lifesteal_upgrade": 0.1, "perm_lifesteal_chance_upgrade": 0.1}, "weight": 5, "area": 4},
{"name": "Fire Elemental", "hp": 70, "magic_atk_min": 16, "magic_atk_max": 22, "money_min": 85, "money_max": 125, "class": "C(Rare)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "fire_essence": 0.3, "ember": 0.2, "perm_exp_upgrade": 0.1, "perm_strength_upgrade": 0.1, "perm_defense_upgrade": 0.1, "perm_health_upgrade": 0.1, "perm_mana_upgrade": 0.1, "perm_crit_chance_upgrade": 0.1, "perm_mana_regen_upgrade": 0.1, "perm_lifesteal_upgrade": 0.1, "perm_lifesteal_chance_upgrade": 0.1}, "weight": 5, "area": 4},
{"name": "Thunder Bird", "hp": 65, "magic_atk_min": 14, "magic_atk_max": 21, "money_min": 95, "money_max": 140, "class": "C(Rare)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "thunder_core": 0.3, "lightning_feather": 0.2, "perm_exp_upgrade": 0.1, "perm_strength_upgrade": 0.1, "perm_defense_upgrade": 0.1, "perm_health_upgrade": 0.1, "perm_mana_upgrade": 0.1, "perm_crit_chance_upgrade": 0.1, "perm_mana_regen_upgrade": 0.1, "perm_lifesteal_upgrade": 0.1, "perm_lifesteal_chance_upgrade": 0.1}, "weight": 5, "area": 4},

# Area 5 Monsters (Level 21-25) - 12% chance for all permanent upgrades
{"name": "Dark Knight", "hp": 120, "atk_min": 18, "atk_max": 25, "money_min": 120, "money_max": 180, "class": "B(Mythical)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.15, "defense_boost": 0.1, "rare_magic_pack": 0.2, "dark_essence": 0.3, "perm_exp_upgrade": 0.12, "perm_strength_upgrade": 0.12, "perm_defense_upgrade": 0.12, "perm_health_upgrade": 0.12, "perm_mana_upgrade": 0.12, "perm_crit_chance_upgrade": 0.12, "perm_mana_regen_upgrade": 0.12, "perm_lifesteal_upgrade": 0.12, "perm_lifesteal_chance_upgrade": 0.12}, "weight": 4, "area": 5},
{"name": "Shadow Assassin", "hp": 100, "atk_min": 20, "atk_max": 28, "money_min": 130, "money_max": 190, "class": "B(Mythical)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.15, "crit_boost": 0.1, "rare_magic_pack": 0.2, "shadow_cloak": 0.2, "perm_exp_upgrade": 0.12, "perm_strength_upgrade": 0.12, "perm_defense_upgrade": 0.12, "perm_health_upgrade": 0.12, "perm_mana_upgrade": 0.12, "perm_crit_chance_upgrade": 0.12, "perm_mana_regen_upgrade": 0.12, "perm_lifesteal_upgrade": 0.12, "perm_lifesteal_chance_upgrade": 0.12}, "weight": 4, "area": 5},
{"name": "Arcane Mage", "hp": 110, "magic_atk_min": 22, "magic_atk_max": 30, "money_min": 140, "money_max": 200, "class": "B(Mythical)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "mana_upgrade_potion": 0.1, "rare_magic_pack": 0.25, "mythical_magic_pack": 0.1, "arcane_tome": 0.2, "perm_exp_upgrade": 0.12, "perm_strength_upgrade": 0.12, "perm_defense_upgrade": 0.12, "perm_health_upgrade": 0.12, "perm_mana_upgrade": 0.12, "perm_crit_chance_upgrade": 0.12, "perm_mana_regen_upgrade": 0.12, "perm_lifesteal_upgrade": 0.12, "perm_lifesteal_chance_upgrade": 0.12}, "weight": 3, "area": 5},
{"name": "Warlock", "hp": 105, "atk_min": 21, "atk_max": 29, "money_min": 135, "money_max": 195, "class": "B(Mythical)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "curse_scroll": 0.2, "rare_magic_pack": 0.2, "mythical_magic_pack": 0.1, "demon_horn": 0.2, "perm_exp_upgrade": 0.12, "perm_strength_upgrade": 0.12, "perm_defense_upgrade": 0.12, "perm_health_upgrade": 0.12, "perm_mana_upgrade": 0.12, "perm_crit_chance_upgrade": 0.12, "perm_mana_regen_upgrade": 0.12, "perm_lifesteal_upgrade": 0.12, "perm_lifesteal_chance_upgrade": 0.12}, "weight": 3, "area": 5},

# Area 6 Monsters (Level 26-30) - 14% chance for all permanent upgrades
{"name": "Ice Giant", "hp": 150, "atk_min": 25, "atk_max": 35, "money_min": 180, "money_max": 250, "class": "B(Mythical)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "frozen_heart": 0.4, "mythical_magic_pack": 0.2, "ice_shard": 0.3, "perm_exp_upgrade": 0.14, "perm_strength_upgrade": 0.14, "perm_defense_upgrade": 0.14, "perm_health_upgrade": 0.14, "perm_mana_upgrade": 0.14, "perm_crit_chance_upgrade": 0.14, "perm_mana_regen_upgrade": 0.14, "perm_lifesteal_upgrade": 0.14, "perm_lifesteal_chance_upgrade": 0.14}, "weight": 3, "area": 6},
{"name": "Phoenix", "hp": 130, "atk_min": 28, "atk_max": 38, "money_min": 200, "money_max": 280, "class": "B(Mythical)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "phoenix_feather": 0.3, "mythical_magic_pack": 0.25, "fire_essence": 0.3, "perm_exp_upgrade": 0.14, "perm_strength_upgrade": 0.14, "perm_defense_upgrade": 0.14, "perm_health_upgrade": 0.14, "perm_mana_upgrade": 0.14, "perm_crit_chance_upgrade": 0.14, "perm_mana_regen_upgrade": 0.14, "perm_lifesteal_upgrade": 0.14, "perm_lifesteal_chance_upgrade": 0.14}, "weight": 2, "area": 6},
{"name": "Crystal Golem", "hp": 160, "atk_min": 24, "atk_max": 34, "money_min": 190, "money_max": 260, "class": "B(Mythical)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "crystal_shard": 0.4, "mythical_magic_pack": 0.2, "stone_core": 0.3, "perm_exp_upgrade": 0.14, "perm_strength_upgrade": 0.14, "perm_defense_upgrade": 0.14, "perm_health_upgrade": 0.14, "perm_mana_upgrade": 0.14, "perm_crit_chance_upgrade": 0.14, "perm_mana_regen_upgrade": 0.14, "perm_lifesteal_upgrade": 0.14, "perm_lifesteal_chance_upgrade": 0.14}, "weight": 2, "area": 6},
{"name": "Storm Dragon", "hp": 140, "atk_min": 27, "atk_max": 37, "money_min": 210, "money_max": 290, "class": "B(Mythical)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "thunder_core": 0.4, "mythical_magic_pack": 0.25, "dragon_scale": 0.2, "perm_exp_upgrade": 0.14, "perm_strength_upgrade": 0.14, "perm_defense_upgrade": 0.14, "perm_health_upgrade": 0.14, "perm_mana_upgrade": 0.14, "perm_crit_chance_upgrade": 0.14, "perm_mana_regen_upgrade": 0.14, "perm_lifesteal_upgrade": 0.14, "perm_lifesteal_chance_upgrade": 0.14}, "weight": 2, "area": 6},

# Area 7 Monsters (Level 31-35) - 16% chance for all permanent upgrades
{"name": "Void Walker", "hp": 180, "magic_atk_min": 32, "magic_atk_max": 42, "money_min": 250, "money_max": 350, "class": "A(Prismatic)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.15, "void_fragment": 0.3, "mythical_magic_pack": 0.2, "prismatic_magic_pack": 0.1, "perm_exp_upgrade": 0.16, "perm_strength_upgrade": 0.16, "perm_defense_upgrade": 0.16, "perm_health_upgrade": 0.16, "perm_mana_upgrade": 0.16, "perm_crit_chance_upgrade": 0.16, "perm_mana_regen_upgrade": 0.16, "perm_lifesteal_upgrade": 0.16, "perm_lifesteal_chance_upgrade": 0.16}, "weight": 2, "area": 7},
{"name": "Celestial Guardian", "hp": 200, "atk_min": 30, "atk_max": 40, "money_min": 280, "money_max": 380, "class": "A(Prismatic)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "holy_light": 0.3, "mythical_magic_pack": 0.25, "prismatic_magic_pack": 0.15, "perm_exp_upgrade": 0.16, "perm_strength_upgrade": 0.16, "perm_defense_upgrade": 0.16, "perm_health_upgrade": 0.16, "perm_mana_upgrade": 0.16, "perm_crit_chance_upgrade": 0.16, "perm_mana_regen_upgrade": 0.16, "perm_lifesteal_upgrade": 0.16, "perm_lifesteal_chance_upgrade": 0.16}, "weight": 2, "area": 7},
{"name": "Star Weaver", "hp": 170, "atk_min": 33, "atk_max": 43, "money_min": 260, "money_max": 360, "class": "A(Prismatic)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "star_dust": 0.4, "mythical_magic_pack": 0.2, "prismatic_magic_pack": 0.1, "perm_exp_upgrade": 0.16, "perm_strength_upgrade": 0.16, "perm_defense_upgrade": 0.16, "perm_health_upgrade": 0.16, "perm_mana_upgrade": 0.16, "perm_crit_chance_upgrade": 0.16, "perm_mana_regen_upgrade": 0.16, "perm_lifesteal_upgrade": 0.16, "perm_lifesteal_chance_upgrade": 0.16}, "weight": 2, "area": 7},
{"name": "Moon Sentinel", "hp": 190, "atk_min": 31, "atk_max": 41, "money_min": 270, "money_max": 370, "class": "A(Prismatic)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "moon_rock": 0.3, "mythical_magic_pack": 0.2, "prismatic_magic_pack": 0.15, "perm_exp_upgrade": 0.16, "perm_strength_upgrade": 0.16, "perm_defense_upgrade": 0.16, "perm_health_upgrade": 0.16, "perm_mana_upgrade": 0.16, "perm_crit_chance_upgrade": 0.16, "perm_mana_regen_upgrade": 0.16, "perm_lifesteal_upgrade": 0.16, "perm_lifesteal_chance_upgrade": 0.16}, "weight": 2, "area": 7},

# Area 8 Monsters (Level 36-40) - 18% chance for all permanent upgrades
{"name": "Sun Champion", "hp": 220, "atk_min": 36, "atk_max": 46, "money_min": 320, "money_max": 420, "class": "A(Prismatic)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "sun_stone": 0.3, "prismatic_magic_pack": 0.25, "divine_magic_pack": 0.1, "perm_exp_upgrade": 0.18, "perm_strength_upgrade": 0.18, "perm_defense_upgrade": 0.18, "perm_health_upgrade": 0.18, "perm_mana_upgrade": 0.18, "perm_crit_chance_upgrade": 0.18, "perm_mana_regen_upgrade": 0.18, "perm_lifesteal_upgrade": 0.18, "perm_lifesteal_chance_upgrade": 0.18}, "weight": 1, "area": 8},
{"name": "Void Lord", "hp": 240, "magic_atk_min": 38, "magic_atk_max": 48, "money_min": 350, "money_max": 450, "class": "A(Prismatic)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "void_fragment": 0.4, "prismatic_magic_pack": 0.25, "divine_magic_pack": 0.15, "perm_exp_upgrade": 0.18, "perm_strength_upgrade": 0.18, "perm_defense_upgrade": 0.18, "perm_health_upgrade": 0.18, "perm_mana_upgrade": 0.18, "perm_crit_chance_upgrade": 0.18, "perm_mana_regen_upgrade": 0.18, "perm_lifesteal_upgrade": 0.18, "perm_lifesteal_chance_upgrade": 0.18}, "weight": 1, "area": 8},
{"name": "Divine Paladin", "hp": 210, "atk_min": 37, "atk_max": 47, "money_min": 330, "money_max": 430, "class": "A(Prismatic)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "holy_light": 0.4, "prismatic_magic_pack": 0.3, "divine_magic_pack": 0.15, "perm_exp_upgrade": 0.18, "perm_strength_upgrade": 0.18, "perm_defense_upgrade": 0.18, "perm_health_upgrade": 0.18, "perm_mana_upgrade": 0.18, "perm_crit_chance_upgrade": 0.18, "perm_mana_regen_upgrade": 0.18, "perm_lifesteal_upgrade": 0.18, "perm_lifesteal_chance_upgrade": 0.18}, "weight": 1, "area": 8},
{"name": "Cosmic Mage", "hp": 230, "magic_atk_min": 35, "magic_atk_max": 45, "money_min": 340, "money_max": 440, "class": "A(Prismatic)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "star_dust": 0.3, "prismatic_magic_pack": 0.25, "divine_magic_pack": 0.2, "perm_exp_upgrade": 0.18, "perm_strength_upgrade": 0.18, "perm_defense_upgrade": 0.18, "perm_health_upgrade": 0.18, "perm_mana_upgrade": 0.18, "perm_crit_chance_upgrade": 0.18, "perm_mana_regen_upgrade": 0.18, "perm_lifesteal_upgrade": 0.18, "perm_lifesteal_chance_upgrade": 0.18}, "weight": 1, "area": 8},

# Area 9 Monsters (Level 41-45) - 20% chance for all permanent upgrades
{"name": "Eternal Dragon", "hp": 300, "atk_min": 42, "atk_max": 54, "money_min": 450, "money_max": 600, "class": "S(Divine)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.15, "dragon_scale": 0.4, "divine_magic_pack": 0.3, "transcendent_magic_pack": 0.1, "perm_exp_upgrade": 0.2, "perm_strength_upgrade": 0.2, "perm_defense_upgrade": 0.2, "perm_health_upgrade": 0.2, "perm_mana_upgrade": 0.2, "perm_crit_chance_upgrade": 0.2, "perm_mana_regen_upgrade": 0.2, "perm_lifesteal_upgrade": 0.2, "perm_lifesteal_chance_upgrade": 0.2}, "weight": 1, "area": 9},
{"name": "Void Reaper", "hp": 280, "magic_atk_min": 45, "magic_atk_max": 57, "money_min": 480, "money_max": 630, "class": "S(Divine)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "void_fragment": 0.4, "divine_magic_pack": 0.3, "transcendent_magic_pack": 0.15, "perm_exp_upgrade": 0.2, "perm_strength_upgrade": 0.2, "perm_defense_upgrade": 0.2, "perm_health_upgrade": 0.2, "perm_mana_upgrade": 0.2, "perm_crit_chance_upgrade": 0.2, "perm_mana_regen_upgrade": 0.2, "perm_lifesteal_upgrade": 0.2, "perm_lifesteal_chance_upgrade": 0.2}, "weight": 1, "area": 9},
{"name": "Celestial Phoenix", "hp": 290, "atk_min": 43, "atk_max": 55, "money_min": 470, "money_max": 620, "class": "S(Divine)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "phoenix_feather": 0.4, "divine_magic_pack": 0.35, "transcendent_magic_pack": 0.15, "perm_exp_upgrade": 0.2, "perm_strength_upgrade": 0.2, "perm_defense_upgrade": 0.2, "perm_health_upgrade": 0.2, "perm_mana_upgrade": 0.2, "perm_crit_chance_upgrade": 0.2, "perm_mana_regen_upgrade": 0.2, "perm_lifesteal_upgrade": 0.2, "perm_lifesteal_chance_upgrade": 0.2}, "weight": 1, "area": 9},
{"name": "Cosmic Entity", "hp": 310, "magic_atk_min": 41, "magic_atk_max": 53, "money_min": 460, "money_max": 610, "class": "S(Divine)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "star_dust": 0.4, "divine_magic_pack": 0.3, "transcendent_magic_pack": 0.2, "perm_exp_upgrade": 0.2, "perm_strength_upgrade": 0.2, "perm_defense_upgrade": 0.2, "perm_health_upgrade": 0.2, "perm_mana_upgrade": 0.2, "perm_crit_chance_upgrade": 0.2, "perm_mana_regen_upgrade": 0.2, "perm_lifesteal_upgrade": 0.2, "perm_lifesteal_chance_upgrade": 0.2}, "weight": 1, "area": 9},

# Area 10 Monsters (Level 46-50) - 20% chance for all permanent upgrades
{"name": "Transcendent Being", "hp": 400, "atk_min": 50, "atk_max": 65, "money_min": 600, "money_max": 800, "class": "SS(Transcendent)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "transcendent_heart": 0.2, "divine_magic_pack": 0.3, "transcendent_magic_pack": 0.3, "perm_exp_upgrade": 0.2, "perm_strength_upgrade": 0.2, "perm_defense_upgrade": 0.2, "perm_health_upgrade": 0.2, "perm_mana_upgrade": 0.2, "perm_crit_chance_upgrade": 0.2, "perm_mana_regen_upgrade": 0.2, "perm_lifesteal_upgrade": 0.2, "perm_lifesteal_chance_upgrade": 0.2}, "weight": 1, "area": 10},
{"name": "Void Emperor", "hp": 420, "magic_atk_min": 52, "magic_atk_max": 67, "money_min": 650, "money_max": 850, "class": "SS(Transcendent)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "void_fragment": 0.4, "divine_magic_pack": 0.3, "transcendent_magic_pack": 0.35, "perm_exp_upgrade": 0.2, "perm_strength_upgrade": 0.2, "perm_defense_upgrade": 0.2, "perm_health_upgrade": 0.2, "perm_mana_upgrade": 0.2, "perm_crit_chance_upgrade": 0.2, "perm_mana_regen_upgrade": 0.2, "perm_lifesteal_upgrade": 0.2, "perm_lifesteal_chance_upgrade": 0.2}, "weight": 1, "area": 10},
{"name": "Divine Avatar", "hp": 410, "atk_min": 51, "atk_max": 66, "money_min": 630, "money_max": 830, "class": "SS(Transcendent)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "holy_light": 0.4, "divine_magic_pack": 0.35, "transcendent_magic_pack": 0.3, "perm_exp_upgrade": 0.2, "perm_strength_upgrade": 0.2, "perm_defense_upgrade": 0.2, "perm_health_upgrade": 0.2, "perm_mana_upgrade": 0.2, "perm_crit_chance_upgrade": 0.2, "perm_mana_regen_upgrade": 0.2, "perm_lifesteal_upgrade": 0.2, "perm_lifesteal_chance_upgrade": 0.2}, "weight": 1, "area": 10},
{"name": "Cosmic Overlord", "hp": 430, "atk_min": 53, "atk_max": 68, "money_min": 670, "money_max": 870, "class": "SS(Transcendent)", "is_boss": False, "is_super_boss": False, "drop": {"potion": 0.2, "star_dust": 0.4, "divine_magic_pack": 0.3, "transcendent_magic_pack": 0.4, "perm_exp_upgrade": 0.2, "perm_strength_upgrade": 0.2, "perm_defense_upgrade": 0.2, "perm_health_upgrade": 0.2, "perm_mana_upgrade": 0.2, "perm_crit_chance_upgrade": 0.2, "perm_mana_regen_upgrade": 0.2, "perm_lifesteal_upgrade": 0.2, "perm_lifesteal_chance_upgrade": 0.2}, "weight": 1, "area": 10},

# Bosses - 100% chance for all permanent upgrades
{"name": "Goblin King", "hp": 200, "atk_min": 50, "atk_max": 100, "money_min": 200, "money_max": 400, "class": "D(Common)", "is_boss": True, "is_super_boss": False, "drop": {"potion": 1.0, "strength_boost": 0.5, "defense_boost": 0.3, "goblin_tooth": 1.0, "common_magic_pack": 0.5, "perm_exp_upgrade": 1.0, "perm_strength_upgrade": 1.0, "perm_defense_upgrade": 1.0, "perm_health_upgrade": 1.0, "perm_mana_upgrade": 1.0, "perm_crit_chance_upgrade": 1.0, "perm_mana_regen_upgrade": 1.0, "perm_lifesteal_upgrade": 1.0, "perm_lifesteal_chance_upgrade": 1.0}, "weight": 1, "area": 1},
{"name": "Skeleton King", "hp": 500, "atk_min": 110, "atk_max": 175, "money_min": 750, "money_max": 2000, "class": "B(Mythical)", "is_boss": True, "is_super_boss": False, "drop": {"potion": 1.0, "strength_boost": 0.8, "defense_boost": 0.5, "crit_boost": 0.4, "rare_magic_pack": 0.8, "mythical_magic_pack": 0.4, "skeleton_bone": 1.0, "perm_exp_upgrade": 1.0, "perm_strength_upgrade": 1.0, "perm_defense_upgrade": 1.0, "perm_health_upgrade": 1.0, "perm_mana_upgrade": 1.0, "perm_crit_chance_upgrade": 1.0, "perm_mana_regen_upgrade": 1.0, "perm_lifesteal_upgrade": 1.0, "perm_lifesteal_chance_upgrade": 1.0}, "weight": 1, "area": 1},
{"name": "Troll Chieftain", "hp": 800, "atk_min": 120, "atk_max": 150, "money_min": 1500, "money_max": 3000, "class": "C(Rare)", "is_boss": True, "is_super_boss": False, "drop": {"potion": 1.0, "strength_boost": 0.7, "defense_boost": 0.6, "regen_potion": 0.5, "rare_magic_pack": 0.7, "mythical_magic_pack": 0.3, "troll_core": 1.0, "perm_exp_upgrade": 1.0, "perm_strength_upgrade": 1.0, "perm_defense_upgrade": 1.0, "perm_health_upgrade": 1.0, "perm_mana_upgrade": 1.0, "perm_crit_chance_upgrade": 1.0, "perm_mana_regen_upgrade": 1.0, "perm_lifesteal_upgrade": 1.0, "perm_lifesteal_chance_upgrade": 1.0}, "weight": 1, "area": 3},
{"name": "Dark Lord", "hp": 1200, "atk_min": 135, "atk_max": 189, "money_min": 2500, "money_max": 5000, "class": "B(Mythical)", "is_boss": True, "is_super_boss": False, "drop": {"potion": 1.0, "strength_boost": 0.8, "defense_boost": 0.6, "crit_boost": 0.5, "mythical_magic_pack": 0.8, "prismatic_magic_pack": 0.4, "dark_essence": 1.0, "perm_exp_upgrade": 1.0, "perm_strength_upgrade": 1.0, "perm_defense_upgrade": 1.0, "perm_health_upgrade": 1.0, "perm_mana_upgrade": 1.0, "perm_crit_chance_upgrade": 1.0, "perm_mana_regen_upgrade": 1.0, "perm_lifesteal_upgrade": 1.0, "perm_lifesteal_chance_upgrade": 1.0}, "weight": 1, "area": 4},
{"name": "Ice Queen", "hp": 1500, "magic_atk_min": 150, "magic_atk_max": 75, "money_min": 3500, "money_max": 6000, "class": "B(Mythical)", "is_boss": True, "is_super_boss": False, "drop": {"potion": 1.0, "defense_boost": 0.8, "regen_potion": 0.7, "mythical_magic_pack": 0.7, "prismatic_magic_pack": 0.5, "frozen_heart": 1.0, "perm_exp_upgrade": 1.0, "perm_strength_upgrade": 1.0, "perm_defense_upgrade": 1.0, "perm_health_upgrade": 1.0, "perm_mana_upgrade": 1.0, "perm_crit_chance_upgrade": 1.0, "perm_mana_regen_upgrade": 1.0, "perm_lifesteal_upgrade": 1.0, "perm_lifesteal_chance_upgrade": 1.0}, "weight": 1, "area": 5},
{"name": "Phoenix Lord", "hp": 1800, "atk_min": 100, "atk_max": 150, "money_min": 4500, "money_max": 7500, "class": "A(Prismatic)", "is_boss": True, "is_super_boss": False, "drop": {"potion": 1.0, "strength_boost": 0.8, "mana_upgrade_potion": 0.6, "mythical_magic_pack": 0.8, "prismatic_magic_pack": 0.6, "phoenix_feather": 1.0, "perm_exp_upgrade": 1.0, "perm_strength_upgrade": 1.0, "perm_defense_upgrade": 1.0, "perm_health_upgrade": 1.0, "perm_mana_upgrade": 1.0, "perm_crit_chance_upgrade": 1.0, "perm_mana_regen_upgrade": 1.0, "perm_lifesteal_upgrade": 1.0, "perm_lifesteal_chance_upgrade": 1.0}, "weight": 1, "area": 6},
{"name": "Void Master", "hp": 2200, "atk_min": 190, "atk_max": 240, "money_min": 6000, "money_max": 10000, "class": "A(Prismatic)", "is_boss": True, "is_super_boss": False, "drop": {"potion": 1.0, "strength_boost": 0.9, "defense_boost": 0.8, "crit_boost": 0.7, "prismatic_magic_pack": 0.8, "divine_magic_pack": 0.4, "void_fragment": 1.0, "perm_exp_upgrade": 1.0, "perm_strength_upgrade": 1.0, "perm_defense_upgrade": 1.0, "perm_health_upgrade": 1.0, "perm_mana_upgrade": 1.0, "perm_crit_chance_upgrade": 1.0, "perm_mana_regen_upgrade": 1.0, "perm_lifesteal_upgrade": 1.0, "perm_lifesteal_chance_upgrade": 1.0}, "weight": 1, "area": 7},
{"name": "Celestial Emperor", "hp": 2800, "atk_min": 250, "atk_max": 350, "money_min": 8000, "money_max": 13000, "class": "S(Divine)", "is_boss": True, "is_super_boss": False, "drop": {"potion": 1.0, "strength_boost": 0.9, "defense_boost": 0.9, "mana_upgrade_potion": 0.7, "prismatic_magic_pack": 0.8, "divine_magic_pack": 0.6, "holy_light": 1.0, "perm_exp_upgrade": 1.0, "perm_strength_upgrade": 1.0, "perm_defense_upgrade": 1.0, "perm_health_upgrade": 1.0, "perm_mana_upgrade": 1.0, "perm_crit_chance_upgrade": 1.0, "perm_mana_regen_upgrade": 1.0, "perm_lifesteal_upgrade": 1.0, "perm_lifesteal_chance_upgrade": 1.0}, "weight": 1, "area": 8},
{"name": "Dragon Lord", "hp": 3500, "atk_min": 250, "atk_max": 350, "money_min": 10000, "money_max": 16000, "class": "S(Divine)", "is_boss": True, "is_super_boss": False, "drop": {"potion": 1.0, "strength_boost": 1.0, "defense_boost": 0.9, "crit_boost": 0.8, "divine_magic_pack": 0.8, "transcendent_magic_pack": 0.4, "dragon_scale": 1.0, "perm_exp_upgrade": 1.0, "perm_strength_upgrade": 1.0, "perm_defense_upgrade": 1.0, "perm_health_upgrade": 1.0, "perm_mana_upgrade": 1.0, "perm_crit_chance_upgrade": 1.0, "perm_mana_regen_upgrade": 1.0, "perm_lifesteal_upgrade": 1.0, "perm_lifesteal_chance_upgrade": 1.0}, "weight": 1, "area": 9},
{"name": "Grim Reaper", "hp": 4000, "magic_atk_min": 300, "magic_atk_max": 500, "money_min": 12000, "money_max": 20000, "class": "S(Divine)", "is_boss": True, "is_super_boss": False, "drop": {"potion": 1.0, "strength_boost": 1.0, "defense_boost": 1.0, "crit_boost": 1.0, "prismatic_magic_pack": 0.8, "divine_magic_pack": 0.8, "soul_shard": 1.0, "perm_exp_upgrade": 1.0, "perm_strength_upgrade": 1.0, "perm_defense_upgrade": 1.0, "perm_health_upgrade": 1.0, "perm_mana_upgrade": 1.0, "perm_crit_chance_upgrade": 1.0, "perm_mana_regen_upgrade": 1.0, "perm_lifesteal_upgrade": 1.0, "perm_lifesteal_chance_upgrade": 1.0}, "weight": 1, "area": 10},
{"name": "Demon King Muzan", "hp": 12000, "atk_min": 400, "atk_max": 550, "money_min": 100000, "money_max": 500000, "class": "SS(Transcendent)", "is_boss": True, "is_super_boss": True, "drop": {"potion": 1.0, "strength_boost": 1, "defense_boost": 1, "crit_boost": 1, "transcendent_heart": 0.5, "divine_magic_pack": 0.8, "transcendent_magic_pack": 0.4, "demon_horn": 1.0, "perm_exp_upgrade": 1.0, "perm_strength_upgrade": 1.0, "perm_defense_upgrade": 1.0, "perm_health_upgrade": 1.0, "perm_mana_upgrade": 1.0, "perm_crit_chance_upgrade": 1.0, "perm_mana_regen_upgrade": 1.0, "perm_lifesteal_upgrade": 1.0, "perm_lifesteal_chance_upgrade": 1.0}, "weight": 0.01, "area": 10},
]

def get_leaderboard():
    """Get leaderboard from users.txt"""
    users_data = []
    users = load_all_users()
    for username, user_data in users.items():
        score = user_data.get("score", 0)
        users_data.append((username, score))
    users_data.sort(key=lambda x: x[1], reverse=True)
    return users_data[:10]

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
                # Save the updated score
                update_user(current_user, score=score)
                return score
        except ValueError:
            print("Please enter a valid number.")

def explore_dungeon(username):
    """Explore the dungeon to find treasure"""
    user_data = load_user_data(username)
    if not user_data:
        return "User not found."

    player_data = user_data["player_data"]
    stats = player_data["stats"]
    inventory = player_data["inventory"]

    # Check if player has enough health to explore
    if stats["hp"] < stats["hp_max"] * 0.3:
        return "You need at least 30% health to explore the dungeon."

    # Consume some health for exploration
    stats["hp"] = max(1, stats["hp"] - stats["hp_max"] * 0.1)

    # Calculate treasure found based on player level and area
    area = stats.get("current_area", 1)
    level = stats.get("level", 1)

    # Base treasure amount
    base_treasure = 100 + (area * 50) + (level * 20)

    # Apply treasure boost from titles if available
    treasure_boost = stats.get("title_treasure_boost", 0)
    if treasure_boost > 0:
        boosted_amount = base_treasure * (treasure_boost / 100.0)
        base_treasure += boosted_amount

    # Random factor
    treasure_found = int(base_treasure * random.uniform(0.8, 1.5))

    # Cap at dungeon_treasure
    global dungeon_treasure
    treasure_found = min(treasure_found, dungeon_treasure)

    # Update player money and stats
    user_data["money"] += treasure_found
    stats["dungeon_treasure_collected"] = stats.get("dungeon_treasure_collected", 0) + treasure_found
    stats["total_money_earned"] = stats.get("total_money_earned", 0) + treasure_found

    # Reduce dungeon treasure
    dungeon_treasure -= treasure_found

    load_dungeon_treasure()
    save_dungeon_treasure()
    # Check for achievements
    check_achievements(username)

    # Save player data
    update_user(username, money=user_data["money"], player_data=user_data["player_data"])

# -------------------------
# Dungeon game function (needed for main menu)
# -------------------------
# Debug Console
# -------------------------
def debug_console(current_user, score, money, player_data, USERS_DIR):
    debugconsoleaccess = "accepted" if current_user == "tester01" else None
    if current_user != "tester01":
        adminQ = input("When is the game developer's bestfriends BOD?: ")
        if adminQ in adminQanswers:
            print("Access Accepted")
            debugconsoleaccess = "accepted"
        else:
            print("Access Denied")
            debugconsoleaccess = "denied"
    print("\nOpening DEBUG Console...\n...\n...")
    while True:
        if debugconsoleaccess == "denied":
            break
        else:
            pass
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
            leaderboard = get_leaderboard()
            print("\n--- Top 10 Users ---")
            for uname, uscore in leaderboard:
                user_data = load_user_data(uname)
                umoney = user_data.get("money", 0) if user_data else 0
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
                users = load_all_users()
                if u in users:
                    del users[u]
                    save_all_users(users)
                    print(f"User {u} deleted.")
                else:
                    print("User not found.")
            else:
                print("Usage: deluser <username>")
        elif cmd_base == "reset":
            save_all_users({})
            print("All users reset.")
        elif cmd_base == "resetplayer":
            if args:
                u = args.strip()
                user_data = load_user_data(u)
                if user_data:
                    player_data = default_player_data()
                    user_data["score"] = 0
                    user_data["money"] = 40
                    user_data["player_data"] = player_data
                    save_user_data(u, user_data)
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
                        user_data = load_user_data(u)
                        if user_data:
                            user_data["score"] = n
                            save_user_data(u, user_data)
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
                        user_data = load_user_data(u)
                        if user_data:
                            user_data["money"] = n
                            save_user_data(u, user_data)
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
                        user_data = load_user_data(u)
                        if user_data:
                            user_data["player_data"]["stats"]["exp"] = n
                            save_user_data(u, user_data)
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
                        user_data = load_user_data(u)
                        if user_data:
                            user_data["player_data"]["stats"]["level"] = n
                            save_user_data(u, user_data)
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
                        user_data = load_user_data(u)
                        if user_data:
                            stats = user_data["player_data"]["stats"]
                            if typ.lower() in ["monsters", "monster"]:
                                stats["monsters_defeated"] = n
                            elif typ.lower() in ["bosses", "boss"]:
                                stats["bosses_defeated"] = n
                            else:
                                print(f"Invalid type: {typ}")
                                continue
                            save_user_data(u, user_data)
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
                        user_data = load_user_data(u)
                        if user_data:
                            stats = user_data["player_data"]["stats"]
                            if stat in stats:
                                stats[stat] = n
                                save_user_data(u, user_data)
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
                user_data = load_user_data(u)
                if user_data:
                    player_data = user_data.get("player_data", {})
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
                        user_data = load_user_data(u)
                        if user_data:
                            inventory = user_data["player_data"].get("inventory", {})
                            inventory[item] = inventory.get(item, 0) + qty
                            user_data["player_data"]["inventory"] = inventory
                            save_user_data(u, user_data)
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
                user_data = load_user_data(u)
                if user_data:
                    player_data = user_data["player_data"]
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
                    apply_title_boosts(u)
                    user_data["score"] = 999999
                    user_data["money"] = 999999
                    save_user_data(u, user_data)
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
# -------------------------

def add_material_drops(inventory, monster):
    """Add material drops from a monster to the inventory and return list of dropped items"""
    dropped = []
    if "drop" in monster:
        for item, chance in monster["drop"].items():
            if random.random() < chance:
                inventory[item] = inventory.get(item, 0) + 1
                dropped.append(item)
                print(f"Found {item}!")
    return dropped

def dungeon(username):
    """
    Dungeon combat loop that uses:
      - apply_permanent_upgrades(username)
      - compute_effective_stats(...)
      - get_equip_and_perm_bonuses(stats)
      - apply_damage_with_defense(...) and apply_magic_damage(...)
      - calculate_total_crit_chance(...)
    """

    # Ensure permanent upgrades applied first to populate perm_* fields
    try:
        apply_permanent_upgrades(username)
    except Exception:
        # If your apply_permanent_upgrades signature / behaviour differs, this still safely continues
        pass

    # Reload player data and score after applying permanent upgrades
    user_data = load_user_data(username)
    if not user_data:
        print("User not found.")
        return

    player_data = user_data.get("player_data", {})
    score = user_data.get("score", 0)
    money = user_data.get("money", 40)

    stats = player_data.get("stats", {})
    inventory = player_data.get("inventory", {})

    # Auto-equip best equipment after upgrading if enabled
    settings = stats.get("settings", {})
    if settings.get("auto_equip_best", False) or settings.get("auto_equip_everything", False):
        try:
            auto_equip_items(username)
            # reload stats/inventory if auto-equip mutates them
            user_data = load_user_data(username)
            player_data = user_data.get("player_data", {})
            stats = player_data.get("stats", {})
            inventory = player_data.get("inventory", {})
        except Exception:
            pass

    active_buffs = []
    forced_monster = None

    print("\n⚔️ Welcome to the Dungeon, brave adventurer!")
    player_hp = stats.get("hp", stats.get("hp_max", 100))
    player_mana = stats.get("mana", stats.get("mana_max", 50))

    # Compute simple equipped ATK/DEF display (perm applied in apply_permanent_upgrades)
    bonuses = get_equip_and_perm_bonuses(stats)
    w_atk = bonuses.get("weapon_atk", 0)
    a_def = bonuses.get("armor_def", 0)
    n_atk = bonuses.get("neck_atk", 0)
    equipped_atk = bonuses.get("total_base_atk", stats.get("atk", 5)) + w_atk + n_atk
    equipped_def = bonuses.get("total_base_def", stats.get("defense", 0)) + a_def + bonuses.get("neck_def", 0)

    current_area = stats.get("current_area", 1)
    print(f"Entering dungeon with HP: {player_hp}, MANA: {player_mana}, ATK: {equipped_atk}, DEF: {equipped_def}, LVL: {stats.get('level',1)}, AREA: {current_area}")
    print(f"Base ATK (with perm): {bonuses.get('total_base_atk', stats.get('atk',5))}, Base DEF (with perm): {bonuses.get('total_base_def', stats.get('defense',0))}")

    # Main loop
    while True:
        cmd = input("\nType 'explore' to find a monster, 'status' to view stats, 'shop' to access shop, 'packs' to open magic packs, 'upgrades' to use permanent upgrades, 'move' to change areas, or 'exit' to leave the dungeon: ").strip()
        if not cmd:
            continue
        lc = cmd.lower().strip()

        if lc == "exit":
            print("You leave the dungeon safely.")
            stats["hp"] = player_hp
            stats["mana"] = player_mana
            player_data["stats"] = stats
            player_data["inventory"] = inventory
            user_data["player_data"] = player_data
            save_user_data(username, user_data)
            return

        if lc == "shop":
            shop()
            # reload after shop
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get("player_data", {})
            stats = player_data.get("stats", {})
            inventory = player_data.get("inventory", {})
            player_mana = stats.get("mana", stats.get("mana_max", 50))
            player_hp = stats.get("hp", stats.get("hp_max", 100))
            continue

        if lc == "packs":
            magic_pack_interface(username)
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get("player_data", {})
            stats = player_data.get("stats", {})
            inventory = player_data.get("inventory", {})
            player_mana = stats.get("mana", stats.get("mana_max", 50))
            player_hp = stats.get("hp", stats.get("hp_max", 100))
            continue

        if lc == "titles":
            equip_titles_menu(username, player_data, None)
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get("player_data", {})
            stats = player_data.get("stats", {})
            inventory = player_data.get("inventory", {})
            player_mana = stats.get("mana", stats.get("mana_max", 50))
            player_hp = stats.get("hp", stats.get("hp_max", 100))
            continue

        if lc == "inventory":
            manage_inventory_menu(username, player_data, None)
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get("player_data", {})
            stats = player_data.get("stats", {})
            inventory = player_data.get("inventory", {})
            player_mana = stats.get("mana", stats.get("mana_max", 50))
            player_hp = stats.get("hp", stats.get("hp_max", 100))
            continue

        if lc == "spells":
            magic_spell_interface(username)
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get("player_data", {})
            stats = player_data.get("stats", {})
            inventory = player_data.get("inventory", {})
            player_mana = stats.get("mana", stats.get("mana_max", 50))
            player_hp = stats.get("hp", stats.get("hp_max", 100))
            continue

        if lc == "status":
            # ensure perm is applied and effective stats are fresh
            try:
                apply_permanent_upgrades(username)
            except Exception:
                pass
            effective_atk, effective_def, effective_magic_atk, effective_magic_def, _, _, _, _ = compute_effective_stats(stats, active_buffs)
            next_exp = exp_to_next(stats.get("level",1)) if stats.get("level",1) < MAX_LEVEL else "MAX"
            name_display = username
            if stats.get("settings", {}).get("call_including_title", True) and stats.get("title"):
                name_display = f"{stats['title']} {username}"
            exp_display = create_exp_bar(stats.get('exp'), next_exp) if stats.get("settings", {}).get("show_exp_bar", False) else f"{stats.get('exp')}/{next_exp}"
            print(f"{name_display} - HP: {player_hp}/{stats.get('hp_max')}, MANA: {player_mana}/{stats.get('mana_max')}, ATK: {effective_atk}, DEF: {effective_def}, Money: ${player_data.get('money',0)}, LVL: {stats.get('level')}, EXP: {exp_display}, AREA: {stats.get('current_area', 1)}")
            if active_buffs:
                print("Active buffs:")
                for b in active_buffs:
                    if b.get('remaining',0) > 0:
                        print(f" - {b}")
            continue

        if lc == "shop":
            shop()
            # reload after shop
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get("player_data", {})
            stats = player_data.get("stats", {})
            inventory = player_data.get("inventory", {})
            player_mana = stats.get("mana", stats.get("mana_max", 50))
            player_hp = stats.get("hp", stats.get("hp_max", 100))
            continue

        if lc == "packs":
            magic_pack_interface(username)
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get("player_data", {})
            stats = player_data.get("stats", {})
            inventory = player_data.get("inventory", {})
            player_mana = stats.get("mana", stats.get("mana_max", 50))
            player_hp = stats.get("hp", stats.get("hp_max", 100))
            continue

        if lc == "upgrades":
            permanent_upgrades_interface(username)
            ensure_user_fields(username)
            user_data = load_user_data(username)
            player_data = user_data.get("player_data", {})
            stats = player_data.get("stats", {})
            inventory = player_data.get("inventory", {})
            player_mana = stats.get("mana", stats.get("mana_max", 50))
            player_hp = stats.get("hp", stats.get("hp_max", 100))
            continue

        if lc == "move":
            print(f"\nCurrent Area: {stats.get('current_area', 1)}")
            print("You can move to areas 1-10. Higher areas have stronger monsters.")
            try:
                new_area = input("Enter area number (1-10) or 'cancel': ").strip()
                if new_area.lower() == "cancel":
                    continue
                new_area = int(new_area)
                if 1 <= new_area <= 10:
                    stats["current_area"] = new_area
                    current_area = new_area
                    player_data["stats"] = stats
                    user_data["player_data"] = player_data
                    save_user_data(username, user_data)
                    print(f"Moved to Area {new_area}!")
                else:
                    print("Invalid area. Must be between 1 and 10.")
            except Exception:
                print("Invalid input. Enter a number between 1 and 10.")
            continue

        if lc.startswith("explore"):
            parts = cmd.split()
            # force spawn syntax support retained (same as your original)
            if len(parts) >= 4:
                code = parts[1].strip()
                is_boss_flag = parts[2].strip().lower()
                monster_name = " ".join(parts[3:]).strip().lower()
                if code == "10234":
                    boss_flags = ("yes", "y", "true", "boss", "b")
                    normal_flags = ("no", "n", "false", "normal", "monster", "m")
                    if is_boss_flag in boss_flags:
                        found = next((m for m in MONSTERS if m["name"].lower() == monster_name and m.get("is_boss")), None)
                        if found:
                            forced_monster = found.copy()
                            print(f"Forced boss spawn: {forced_monster['name']}")
                        else:
                            print("Boss not found.")
                        continue
                    elif is_boss_flag in normal_flags:
                        found = next((m for m in MONSTERS if m["name"].lower() == monster_name and not m.get("is_boss")), None)
                        if found:
                            forced_monster = found.copy()
                            print(f"Forced monster spawn: {forced_monster['name']}")
                        else:
                            print("Monster not found.")
                        continue
                    else:
                        print("Invalid flag.")
                        continue
                else:
                    print("Invalid code.")
                    continue

            # choose monster
            if forced_monster is not None:
                monster = forced_monster.copy()
                forced_monster = None
            else:
                roll = random.randint(1, 100)
                if roll <= 5:
                    area = stats.get("current_area", 1)
                    monster = choose_boss_for_area(area)
                    print(f"\n🔥 BOSS APPEARS: {monster['name']}! (HP {monster.get('hp')}, ATK {monster.get('atk_min','?')}–{monster.get('atk_max','?')})")
                else:
                    area = stats.get("current_area", 1)
                    monster = choose_monster_for_area(area)
                    print(f"\nA wild {monster['name']} appears! (HP {monster.get('hp')}, ATK {monster.get('atk_min','?')}–{monster.get('atk_max','?')})")

            # fight loop
            fight_happened = False
            while monster.get("hp", 0) > 0 and player_hp > 0:
                fight_happened = True

                # ensure permanent upgrades applied and recompute effective stats
                try:
                    apply_permanent_upgrades(username)
                except Exception:
                    pass
                effective_atk, effective_def, effective_magic_atk, effective_magic_def, _, _, _, _ = compute_effective_stats(stats, active_buffs)

                # compute total crit chance from perm + active buffs
                total_crit_chance = calculate_total_crit_chance(stats, active_buffs)

                action = input("Do you want to (a)ttack, (m)agic, (p)otion, (u)se buff, or (r)un? ").lower().strip()

                # ---------- PLAYER PHYSICAL ATTACK ----------
                if action == "a":
                    bonuses = get_equip_and_perm_bonuses(stats)
                    weapon_bonus = bonuses.get("weapon_atk", 0) + bonuses.get("neck_atk", 0)
                    total_base_atk = bonuses.get("total_base_atk", effective_atk)
                    base_roll = random.randint(max(1, total_base_atk - 2), total_base_atk + 3)
                    dmg = 5 + base_roll + weapon_bonus

                    # physical attacks are weak vs magic-type monsters
                    if "magic_atk_min" in monster or "magic_atk_max" in monster:
                        dmg = max(1, dmg // 4)

                    # crit check
                    if random.random() <= total_crit_chance:
                        dmg = int(dmg * 2)
                        stats["critical_hits"] = stats.get("critical_hits", 0) + 1
                        print("💥 CRITICAL HIT!")

                    # apply monster physical defense (if any)
                    monster_def = monster.get("def", 0)
                    damage_after = apply_damage_with_defense(dmg, monster_def)
                    monster["hp"] = monster.get("hp", 0) - damage_after
                    print(f"You hit the {monster['name']} for {damage_after} damage! (Monster HP: {max(0, monster['hp'])})")

                    # lifesteal (from actual damage dealt)
                    lifesteal_chance = stats.get("perm_lifesteal_chance", 0) / 100.0
                    lifesteal_percent = stats.get("perm_lifesteal", 0) / 100.0
                    if random.random() <= lifesteal_chance and lifesteal_percent > 0:
                        heal_amount = int(damage_after * lifesteal_percent)
                        if heal_amount > 0:
                            player_hp = min(player_hp + heal_amount, stats.get("hp_max"))
                            print(f"🩸 LIFESTEAL! You stole {heal_amount} HP! (Your HP: {player_hp}/{stats.get('hp_max')})")
                            stats["hp"] = player_hp
                            stats["mana"] = player_mana

                    # persist minimal state
                    player_data["stats"] = stats
                    player_data["inventory"] = inventory
                    user_data["player_data"] = player_data
                    save_user_data(username, user_data)

                # ---------- PLAYER MAGIC ATTACK (spells) ----------
                elif action == "m":
                    equipped_spells = stats.get("equipped_spells", [None, None, None, None])
                    if not any(equipped_spells):
                        print("You haven't equipped any spells yet. Visit the Magic Spells interface to equip spells!")
                        continue
                    available = [SPELLS_BY_KEY[s] for s in equipped_spells if s is not None and s in SPELLS_BY_KEY]
                    if not available:
                        print("You don't have any equipped spells.")
                        continue
                    print("Equipped spells:")
                    for i, s in enumerate(available, start=1):
                        print(f"{i}. {s['name']} (mana {s['mana']}) - {s.get('desc','')}")
                    sel = input("Choose spell number or 'cancel': ").strip().lower()
                    if sel in ("cancel", "c"):
                        continue
                    try:
                        idx = int(sel) - 1
                        if idx < 0 or idx >= len(available):
                            print("Invalid selection.")
                            continue
                        s = available[idx]
                    except Exception:
                        print("Invalid selection.")
                        continue

                    if player_mana < s.get("mana", 0):
                        print("Not enough mana.")
                        continue

                    player_mana -= s.get("mana", 0)

                    # compute magic damage: spell power + wand + perm magic atk
                    wand_magic = WANDS.get(stats.get("equipped", {}).get("wand"), {}).get("magic_atk", 0)
                    perm_magic_atk = stats.get("perm_magic_atk", 0)
                    dmg = s.get("power", 0) + wand_magic + perm_magic_atk + random.randint(-(s.get("power",0)//8), s.get("power",0)//8)

                    # use combined crit (perm + buffs) for spells too
                    if random.random() <= total_crit_chance:
                        dmg = int(dmg * 2)
                        stats["critical_hits"] = stats.get("critical_hits", 0) + 1
                        print("✨ CRITICAL SPELL HIT!")

                    # Magic ignores physical armor and is reduced by monster.magic_def
                    monster_magic_def = monster.get("magic_def", 0)
                    damage_after = apply_magic_damage(dmg, monster_magic_def)
                    monster["hp"] = monster.get("hp", 0) - damage_after
                    print(f"You cast {s['name']} dealing {damage_after} magic damage! (Monster HP: {max(0, monster['hp'])})")

                    # lifesteal (from actual damage dealt)
                    lifesteal_chance = stats.get("perm_lifesteal_chance", 0) / 100.0
                    lifesteal_percent = stats.get("perm_lifesteal", 0) / 100.0
                    if random.random() <= lifesteal_chance and lifesteal_percent > 0:
                        heal_amount = int(damage_after * lifesteal_percent)
                        if heal_amount > 0:
                            player_hp = min(player_hp + heal_amount, stats.get("hp_max"))
                            print(f"🩸 LIFESTEAL! You stole {heal_amount} HP! (Your HP: {player_hp}/{stats.get('hp_max')})")
                            stats["hp"] = player_hp
                            stats["mana"] = player_mana

                    # persist
                    player_data["stats"] = stats
                    player_data["inventory"] = inventory
                    user_data["player_data"] = player_data
                    save_user_data(username, user_data)

                elif action == "p":
                    # potion use (keeps original behaviour)
                    if inventory.get("potion", 0) > 0:
                        inventory["potion"] -= 1
                        heal_amount = min(stats.get("hp_max",100) - player_hp, 50)
                        player_hp = min(player_hp + heal_amount, stats.get("hp_max"))
                        print(f"You used a potion and healed {heal_amount} HP! (HP: {player_hp}/{stats.get('hp_max')})")
                        player_data["inventory"] = inventory
                        player_data["stats"] = stats
                        user_data["player_data"] = player_data
                        save_user_data(username, user_data)
                    else:
                        print("No potions available.")

                elif action == "u":
                    print("Use buff not implemented in this simplified dungeon flow.")
                    continue

                elif action == "r":
                    if random.random() < 0.5:
                        print("You ran away successfully!")
                        break
                    else:
                        print("Failed to run!")

                # Monster attacks if still alive
                if monster.get("hp", 0) > 0:
                    # Monster attack
                    monster_dmg = random.randint(monster.get("atk_min", 1), monster.get("atk_max", monster.get("atk_min", 1)))
                    player_def = get_equip_and_perm_bonuses(stats)["total_base_def"]
                    damage_to_player = apply_damage_with_defense(monster_dmg, player_def)
                    player_hp -= damage_to_player
                    print(f"The {monster['name']} attacks! You take {damage_to_player} damage! (Your HP: {max(0, player_hp)}/{stats.get('hp_max')})")

                    # Persist minimal state
                    stats["hp"] = player_hp
                    player_data["stats"] = stats
                    user_data["player_data"] = player_data
                    save_user_data(username, user_data)

                    # Check if player died
                    if player_hp <= 0:
                        print("You have been defeated!")
                        stats["hp"] = player_hp
                        stats["mana"] = player_mana
                        stats["times_died"] = stats.get("times_died", 0) + 1
                        player_data["stats"] = stats
                        user_data["player_data"] = player_data
                        save_user_data(username, user_data)
                        return

                # ----- Victory check -----
                if monster.get("hp", 0) <= 0:
                    # compute money reward
                    money_reward = random.randint(monster.get("money_min", 1), monster.get("money_max", 1))

                    # --- SYNCHRONIZE money from DB (authoritative) ---
                    user_data = load_user_data(username)
                    if user_data:
                        money = int(user_data.get("money", 0))
                    else:
                        # fallback to player_data stored money
                        money = int(player_data.get("money", 0))

                    # add monster reward
                    money += money_reward
                
                    # Save money into the user_data money field
                    user_data["money"] = money
                    # also update the player_data money field so JSON and user_data stay consistent
                    player_data["money"] = money

                    # ---- drops / materials ----
                    drops = []
                    for item_name, chance in monster.get("drop", {}).items():
                        if random.random() <= chance:
                            inventory[item_name] = inventory.get(item_name, 0) + 1
                            drops.append(item_name)
                    mat_drops = add_material_drops(inventory, monster)
                    if mat_drops:
                        drops.extend(mat_drops)

                    # Boss guaranteed perm drops
                    if monster.get("is_boss") and monster["name"] != "Skeleton King":
                        for perm_key in PERM_UPGRADES:
                            inventory[perm_key] = inventory.get(perm_key, 0) + 1
                            drops.append(f"{PERM_UPGRADES[perm_key]['name']} (Permanent Upgrade)")

                    # Track achievements & total money earned
                    stats["monsters_defeated"] = stats.get("monsters_defeated", 0) + 1
                    if monster.get("is_boss"):
                        stats["bosses_defeated"] = stats.get("bosses_defeated", 0) + 1
                    stats["total_money_earned"] = stats.get("total_money_earned", 0) + money_reward

                    # Experience
                    exp_gain = max(1, (monster.get("hp", 0) * 2) + random.randint(5, 30))
                    if monster.get("is_boss"):
                        exp_gain *= 2
                    grant_exp(username, exp_gain)

                    # Reload data after grant_exp in case of level up changes
                    user_data = load_user_data(username)
                    player_data = user_data.get("player_data", {})
                    stats = player_data.get("stats", {})
                    inventory = player_data.get("inventory", {})
                    # Update local hp/mana in case level up changed them
                    player_hp = stats.get("hp", player_hp)
                    player_mana = stats.get("mana", player_mana)

                    # Score / boss handling (keep your existing logic)
                    if monster.get("is_boss"):
                        boss_bonus = random.randint(50, 150)
                        print(f"🎉 You defeated the BOSS {monster['name']}! +${money_reward} money, +{boss_bonus} score, +{exp_gain} EXP")
                        score += boss_bonus
                        user_data["score"] = score

                        # dungeon treasure (if any) - add to money and save
                        if dungeon_treasure > 0:
                            # Apply treasure boost from titles if any (keeping your logic)
                            treasure_boost_percent = stats.get("title_treasure_boost_percent", 0)
                            recovered_treasure = dungeon_treasure
                            if treasure_boost_percent > 0:
                                recovered_treasure = int(dungeon_treasure * (1 + treasure_boost_percent / 100.0))
                            print(f"🏆 You recovered the dungeon treasure: ${recovered_treasure}!")
                            money += recovered_treasure
                            user_data["money"] = money
                            player_data["money"] = money
                            stats["dungeon_treasure_collected"] = stats.get("dungeon_treasure_collected", 0) + recovered_treasure
                            dungeon_treasure = 0
                            save_dungeon_treasure()
                    else:
                        normal_bonus = random.randint(5, 20)
                        print(f"🎉 You defeated the {monster['name']}! +${money_reward} money, +{normal_bonus} score, +{exp_gain} EXP")
                        score += normal_bonus
                        user_data["score"] = score

                    if drops:
                        print("You found:", ", ".join(drops))

                    # Persist player_data (stats/inventory) and ensure money field is consistent in JSON too
                    stats["hp"] = player_hp
                    stats["mana"] = player_mana
                    player_data["stats"] = stats
                    player_data["inventory"] = inventory
                    # player_data["money"] already updated above
                    user_data["player_data"] = player_data
                    save_user_data(username, user_data)
                
                    # Achievements checked after all data is saved
                    check_achievements(username)
                    save_all_data()
                    save_user_data(username, user_data)
                    break
                
# -------------------------
# Shop Interface
# -------------------------
def shop():
    global current_user
    if not current_user:
        print("You must be logged in to access the shop.")
        return

    user_data = load_user_data(current_user)
    if not user_data:
        print("User data not found.")
        return

    score = user_data.get("score", 0)
    money = user_data.get("money", 40)
    player_data = user_data.get("player_data", {})
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

        choice = input("\nChoose an option (e.g., 1 or 1 5 for quantity 5): ").strip().lower()
        parts = choice.split()
        if not parts:
            continue
        opt = parts[0]
        qty = int(parts[1]) if len(parts) > 1 else 1
        if qty < 1:
            qty = 1

        if opt in ("exit", "74"):
            break

        item_name = None
        item_dict = None
        cost = 0
        score_cost = 0
        is_equipment = False

        if opt == "1":
            item_name = "potion"
            cost = 20
        elif opt == "2":
            item_name = "strong_potion"
            cost = 80
        elif opt == "3":
            item_name = "ultra_potion"
            cost = 350
        elif opt == "4":
            item_name = "mana_regen_potion"
            cost = 120
        elif opt == "5":
            item_name = "instant_mana"
            cost = 60
        elif opt == "6":
            item_name = "strength_boost"
            cost = 60
        elif opt == "7":
            item_name = "defense_boost"
            cost = 60
        elif opt == "8":
            item_name = "regen_potion"
            cost = 80
        elif opt == "9":
            item_name = "crit_boost"
            cost = 80
        elif opt == "10":
            item_name = "wooden_sword"
            item_dict = WEAPONS
            cost = WEAPONS["wooden_sword"]["price"]
            is_equipment = True
        elif opt == "11":
            item_name = "iron_sword"
            item_dict = WEAPONS
            cost = WEAPONS["iron_sword"]["price"]
            is_equipment = True
        elif opt == "12":
            item_name = "steel_sword"
            item_dict = WEAPONS
            cost = WEAPONS["steel_sword"]["price"]
            is_equipment = True
        elif opt == "13":
            item_name = "diamond_sword"
            item_dict = WEAPONS
            cost = WEAPONS["diamond_sword"]["price"]
            is_equipment = True
        elif opt == "14":
            item_name = "void_sword"
            item_dict = WEAPONS
            cost = WEAPONS["void_sword"]["price"]
            is_equipment = True
        elif opt == "15":
            item_name = "infinitium_sword"
            item_dict = WEAPONS
            cost = WEAPONS["infinitium_sword"]["price"]
            score_cost = WEAPONS["infinitium_sword"].get("score_price", 0)
            is_equipment = True
        elif opt == "16":
            item_name = "frostblade"
            item_dict = WEAPONS
            cost = WEAPONS["frostblade"]["price"]
            score_cost = WEAPONS["frostblade"].get("score_price", 0)
            is_equipment = True
        elif opt == "17":
            item_name = "flameblade"
            item_dict = WEAPONS
            cost = WEAPONS["flameblade"]["price"]
            score_cost = WEAPONS["flameblade"].get("score_price", 0)
            is_equipment = True
        elif opt == "18":
            item_name = "thunder_sword"
            item_dict = WEAPONS
            cost = WEAPONS["thunder_sword"]["price"]
            score_cost = WEAPONS["thunder_sword"].get("score_price", 0)
            is_equipment = True
        elif opt == "19":
            item_name = "holy_avenger"
            item_dict = WEAPONS
            cost = WEAPONS["holy_avenger"]["price"]
            score_cost = WEAPONS["holy_avenger"].get("score_price", 0)
            is_equipment = True
        elif opt == "20":
            item_name = "dragon_slayer"
            item_dict = WEAPONS
            cost = WEAPONS["dragon_slayer"]["price"]
            score_cost = WEAPONS["dragon_slayer"].get("score_price", 0)
            is_equipment = True
        elif opt == "21":
            item_name = "cosmic_blade"
            item_dict = WEAPONS
            cost = WEAPONS["cosmic_blade"]["price"]
            score_cost = WEAPONS["cosmic_blade"].get("score_price", 0)
            is_equipment = True
        elif opt == "22":
            item_name = "transcendent_edge"
            item_dict = WEAPONS
            cost = WEAPONS["transcendent_edge"]["price"]
            score_cost = WEAPONS["transcendent_edge"].get("score_price", 0)
            is_equipment = True
        elif opt == "23":
            item_name = "leather_armor"
            item_dict = ARMORS
            cost = ARMORS["leather_armor"]["price"]
            is_equipment = True
        elif opt == "24":
            item_name = "chainmail"
            item_dict = ARMORS
            cost = ARMORS["chainmail"]["price"]
            is_equipment = True
        elif opt == "25":
            item_name = "plate_armor"
            item_dict = ARMORS
            cost = ARMORS["plate_armor"]["price"]
            is_equipment = True
        elif opt == "26":
            item_name = "diamond_armor"
            item_dict = ARMORS
            cost = ARMORS["diamond_armor"]["price"]
            is_equipment = True
        elif opt == "27":
            item_name = "void_armor"
            item_dict = ARMORS
            cost = ARMORS["void_armor"]["price"]
            is_equipment = True
        elif opt == "28":
            item_name = "infinitium_armor"
            item_dict = ARMORS
            cost = ARMORS["infinitium_armor"]["price"]
            score_cost = ARMORS["infinitium_armor"].get("score_price", 0)
            is_equipment = True
        elif opt == "29":
            item_name = "frost_armor"
            item_dict = ARMORS
            cost = ARMORS["frost_armor"]["price"]
            score_cost = ARMORS["frost_armor"].get("score_price", 0)
            is_equipment = True
        elif opt == "30":
            item_name = "flame_armor"
            item_dict = ARMORS
            cost = ARMORS["flame_armor"]["price"]
            score_cost = ARMORS["flame_armor"].get("score_price", 0)
            is_equipment = True
        elif opt == "31":
            item_name = "thunder_armor"
            item_dict = ARMORS
            cost = ARMORS["thunder_armor"]["price"]
            score_cost = ARMORS["thunder_armor"].get("score_price", 0)
            is_equipment = True
        elif opt == "32":
            item_name = "holy_armor"
            item_dict = ARMORS
            cost = ARMORS["holy_armor"]["price"]
            score_cost = ARMORS["holy_armor"].get("score_price", 0)
            is_equipment = True
        elif opt == "33":
            item_name = "dragon_scale_armor"
            item_dict = ARMORS
            cost = ARMORS["dragon_scale_armor"]["price"]
            score_cost = ARMORS["dragon_scale_armor"].get("score_price", 0)
            is_equipment = True
        elif opt == "34":
            item_name = "cosmic_armor"
            item_dict = ARMORS
            cost = ARMORS["cosmic_armor"]["price"]
            score_cost = ARMORS["cosmic_armor"].get("score_price", 0)
            is_equipment = True
        elif opt == "35":
            item_name = "transcendent_armor"
            item_dict = ARMORS
            cost = ARMORS["transcendent_armor"]["price"]
            score_cost = ARMORS["transcendent_armor"].get("score_price", 0)
            is_equipment = True
        elif opt == "36":
            item_name = "apprentice_wand"
            item_dict = WANDS
            cost = WANDS["apprentice_wand"]["price"]
            is_equipment = True
        elif opt == "37":
            item_name = "mage_wand"
            item_dict = WANDS
            cost = WANDS["mage_wand"]["price"]
            is_equipment = True
        elif opt == "38":
            item_name = "archmage_staff"
            item_dict = WANDS
            cost = WANDS["archmage_staff"]["price"]
            score_cost = WANDS["archmage_staff"].get("score_price", 0)
            is_equipment = True
        elif opt == "39":
            item_name = "frost_wand"
            item_dict = WANDS
            cost = WANDS["frost_wand"]["price"]
            score_cost = WANDS["frost_wand"].get("score_price", 0)
            is_equipment = True
        elif opt == "40":
            item_name = "flame_wand"
            item_dict = WANDS
            cost = WANDS["flame_wand"]["price"]
            score_cost = WANDS["flame_wand"].get("score_price", 0)
            is_equipment = True
        elif opt == "41":
            item_name = "thunder_wand"
            item_dict = WANDS
            cost = WANDS["thunder_wand"]["price"]
            score_cost = WANDS["thunder_wand"].get("score_price", 0)
            is_equipment = True
        elif opt == "42":
            item_name = "holy_scepter"
            item_dict = WANDS
            cost = WANDS["holy_scepter"]["price"]
            score_cost = WANDS["holy_scepter"].get("score_price", 0)
            is_equipment = True
        elif opt == "43":
            item_name = "dragon_staff"
            item_dict = WANDS
            cost = WANDS["dragon_staff"]["price"]
            score_cost = WANDS["dragon_staff"].get("score_price", 0)
            is_equipment = True
        elif opt == "44":
            item_name = "cosmic_scepter"
            item_dict = WANDS
            cost = WANDS["cosmic_scepter"]["price"]
            score_cost = WANDS["cosmic_scepter"].get("score_price", 0)
            is_equipment = True
        elif opt == "45":
            item_name = "transcendent_staff"
            item_dict = WANDS
            cost = WANDS["transcendent_staff"]["price"]
            score_cost = WANDS["transcendent_staff"].get("score_price", 0)
            is_equipment = True
        elif opt == "46":
            item_name = "cloth_robe"
            item_dict = ROBES
            cost = ROBES["cloth_robe"]["price"]
            is_equipment = True
        elif opt == "47":
            item_name = "silk_robe"
            item_dict = ROBES
            cost = ROBES["silk_robe"]["price"]
            is_equipment = True
        elif opt == "48":
            item_name = "void_robe"
            item_dict = ROBES
            cost = ROBES["void_robe"]["price"]
            score_cost = ROBES["void_robe"].get("score_price", 0)
            is_equipment = True
        elif opt == "49":
            item_name = "frost_robe"
            item_dict = ROBES
            cost = ROBES["frost_robe"]["price"]
            score_cost = ROBES["frost_robe"].get("score_price", 0)
            is_equipment = True
        elif opt == "50":
            item_name = "flame_robe"
            item_dict = ROBES
            cost = ROBES["flame_robe"]["price"]
            score_cost = ROBES["flame_robe"].get("score_price", 0)
            is_equipment = True
        elif opt == "51":
            item_name = "thunder_robe"
            item_dict = ROBES
            cost = ROBES["thunder_robe"]["price"]
            score_cost = ROBES["thunder_robe"].get("score_price", 0)
            is_equipment = True
        elif opt == "52":
            item_name = "holy_robe"
            item_dict = ROBES
            cost = ROBES["holy_robe"]["price"]
            score_cost = ROBES["holy_robe"].get("score_price", 0)
            is_equipment = True
        elif opt == "53":
            item_name = "dragon_robe"
            item_dict = ROBES
            cost = ROBES["dragon_robe"]["price"]
            score_cost = ROBES["dragon_robe"].get("score_price", 0)
            is_equipment = True
        elif opt == "54":
            item_name = "cosmic_robe"
            item_dict = ROBES
            cost = ROBES["cosmic_robe"]["price"]
            score_cost = ROBES["cosmic_robe"].get("score_price", 0)
            is_equipment = True
        elif opt == "55":
            item_name = "transcendent_robe"
            item_dict = ROBES
            cost = ROBES["transcendent_robe"]["price"]
            score_cost = ROBES["transcendent_robe"].get("score_price", 0)
            is_equipment = True
        elif opt == "56":
            item_name = "health_amulet"
            item_dict = NECKLACES
            cost = NECKLACES["health_amulet"]["price"]
            is_equipment = True
        elif opt == "57":
            item_name = "mana_amulet"
            item_dict = NECKLACES
            cost = NECKLACES["mana_amulet"]["price"]
            is_equipment = True
        elif opt == "58":
            item_name = "strength_amulet"
            item_dict = NECKLACES
            cost = NECKLACES["strength_amulet"]["price"]
            is_equipment = True
        elif opt == "59":
            item_name = "defense_amulet"
            item_dict = NECKLACES
            cost = NECKLACES["defense_amulet"]["price"]
            is_equipment = True
        elif opt == "60":
            item_name = "crit_amulet"
            item_dict = NECKLACES
            cost = NECKLACES["crit_amulet"]["price"]
            is_equipment = True
        elif opt == "61":
            item_name = "lifesteal_amulet"
            item_dict = NECKLACES
            cost = NECKLACES["lifesteal_amulet"]["price"]
            is_equipment = True
        elif opt == "62":
            item_name = "frost_necklace"
            item_dict = NECKLACES
            cost = NECKLACES["frost_necklace"]["price"]
            score_cost = NECKLACES["frost_necklace"].get("score_price", 0)
            is_equipment = True
        elif opt == "63":
            item_name = "flame_necklace"
            item_dict = NECKLACES
            cost = NECKLACES["flame_necklace"]["price"]
            score_cost = NECKLACES["flame_necklace"].get("score_price", 0)
            is_equipment = True
        elif opt == "64":
            item_name = "thunder_necklace"
            item_dict = NECKLACES
            cost = NECKLACES["thunder_necklace"]["price"]
            score_cost = NECKLACES["thunder_necklace"].get("score_price", 0)
            is_equipment = True
        elif opt == "65":
            item_name = "holy_pendant"
            item_dict = NECKLACES
            cost = NECKLACES["holy_pendant"]["price"]
            score_cost = NECKLACES["holy_pendant"].get("score_price", 0)
            is_equipment = True
        elif opt == "66":
            item_name = "dragon_necklace"
            item_dict = NECKLACES
            cost = NECKLACES["dragon_necklace"]["price"]
            score_cost = NECKLACES["dragon_necklace"].get("score_price", 0)
            is_equipment = True
        elif opt == "67":
            item_name = "cosmic_necklace"
            item_dict = NECKLACES
            cost = NECKLACES["cosmic_necklace"]["price"]
            score_cost = NECKLACES["cosmic_necklace"].get("score_price", 0)
            is_equipment = True
        elif opt == "68":
            item_name = "transcendent_necklace"
            item_dict = NECKLACES
            cost = NECKLACES["transcendent_necklace"]["price"]
            score_cost = NECKLACES["transcendent_necklace"].get("score_price", 0)
            is_equipment = True
        elif opt == "69":
            manage_inventory_menu(current_user, player_data, None)
            # Reload data after inventory changes
            user_data = load_user_data(current_user)
            if user_data:
                player_data = user_data.get("player_data", {})
                inventory = player_data.get("inventory", {})
                money = user_data.get("money", 40)
            continue
        elif opt == "70":
            # Unequip item
            print("Unequip which item? (weapon/armor/wand/robe/necklace)")
            item_type = input("Item type: ").strip().lower()
            stats = player_data["stats"]
            equipped = stats.get("equipped", {})
            if item_type in ["weapon", "armor", "wand", "robe", "necklace"]:
                equipped[item_type] = None
                player_data["stats"] = stats
                user_data["player_data"] = player_data
                save_user_data(current_user, user_data)
                print(f"Unequipped {item_type}.")
                continue
            else:
                print("Invalid item type.")
                continue
        elif opt == "71":
            # Sell potion
            if inventory.get("potion", 0) > 0:
                inventory["potion"] -= 1
                money += 10
                player_data["inventory"] = inventory
                user_data["money"] = money
                user_data["player_data"] = player_data
                save_user_data(current_user, user_data)
                print("Sold 1 potion for $10.")
            else:
                print("No potions to sell.")
            continue
        elif opt == "72":
            # Craft items - placeholder
            print("Crafting not implemented yet.")
            continue
        elif opt == "73":
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
                        user_data["money"] = money
                        user_data["score"] = score
                        user_data["player_data"] = player_data
                        save_user_data(current_user, user_data)
                        print(f"Purchased {item_name} for ${cost}" + (f" and {score_cost} score" if score_cost > 0 else "") + "!")
                else:
                    # Consumables can be bought multiple times
                    total_cost = cost * qty
                    if money >= total_cost:
                        inventory[item_name] = inventory.get(item_name, 0) + qty
                        money -= total_cost
                        player_data["inventory"] = inventory
                        user_data["money"] = money
                        user_data["player_data"] = player_data
                        save_user_data(current_user, user_data)
                        print(f"Purchased {qty}x {item_name} for ${total_cost}!")
                    else:
                        print("Not enough money.")
            else:
                print("Not enough money or score.")

    # No database connection to close

def parse_qty_from_choice(choice_str):
    try:
        return int(choice_str)
    except ValueError:
        return 1

# -------------------------
# Permanent Upgrades Interface
# -------------------------
def permanent_upgrades_interface(username):
    user_data = load_user_data(username)
    if not user_data:
        print("User data not found.")
        return

    player_data = user_data.get("player_data", {})
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
            user_data["player_data"] = player_data
            save_user_data(username, user_data)
            print(f"Used {PERM_UPGRADES[choice]['name']}!")
        else:
            print("Invalid choice or not owned.")

    # No database connection to close

# -------------------------
# Magic Pack Interface
# -------------------------
def magic_pack_interface(username):
    user_data = load_user_data(username)
    if not user_data:
        print("User data not found.")
        return

    player_data = user_data.get("player_data", {})
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

        choice = input("Choose pack to open (e.g., transcendent 5): ").strip().lower()
        parts = choice.split()
        if not parts:
            continue
        pack_alias = parts[0]
        qty = int(parts[1]) if len(parts) > 1 else 1
        if qty < 1:
            qty = 1

        if pack_alias == "0":
            break

        # Handle aliases
        if pack_alias in MAGIC_PACK_ALIASES:
            pack_alias = MAGIC_PACK_ALIASES[pack_alias]

        if pack_alias in MAGIC_PACKS and inventory.get(pack_alias, 0) >= qty:
            success, message = open_magic_pack(username, pack_alias, qty)
            if success:
                print(message)
                # Reload inventory
                user_data = load_user_data(username)
                if user_data:
                    player_data = user_data.get("player_data", {})
                    inventory = player_data.get("inventory", {})
            else:
                print(message)
        else:
            print("Invalid choice or not enough owned.")

    # No database connection to close

# -------------------------
# Apply permanent upgrades function (needed for leveling)
# -------------------------
def apply_permanent_upgrades(username):
    try:
        user_data = load_user_data(username)
        if not user_data:
            return

        player_data = user_data["player_data"]
        stats = player_data["stats"]
        inventory = player_data["inventory"]

        # Apply permanent upgrades
        stats["perm_atk"] = inventory.get("perm_strength_upgrade", 0) * PERM_UPGRADES["perm_strength_upgrade"]["atk_increase"]
        stats["perm_def"] = inventory.get("perm_defense_upgrade", 0) * PERM_UPGRADES["perm_defense_upgrade"]["def_increase"]
        stats["perm_hp_max"] = inventory.get("perm_health_upgrade", 0) * PERM_UPGRADES["perm_health_upgrade"]["hp_increase"]
        stats["perm_mana_max"] = inventory.get("perm_mana_upgrade", 0) * PERM_UPGRADES["perm_mana_upgrade"]["magic_increase"]
        stats["perm_magic_def"] = inventory.get("perm_magic_def_upgrade", 0) * PERM_UPGRADES["perm_magic_def_upgrade"]["magic_def_increase"]
        stats["perm_crit_chance"] = inventory.get("perm_crit_chance_upgrade", 0) * PERM_UPGRADES["perm_crit_chance_upgrade"]["crit_chance_increase"]
        stats["perm_mana_regen"] = inventory.get("perm_mana_regen_upgrade", 0) * PERM_UPGRADES["perm_mana_regen_upgrade"]["mana_regen_increase"]
        stats["perm_lifesteal"] = inventory.get("perm_lifesteal_upgrade", 0) * PERM_UPGRADES["perm_lifesteal_upgrade"]["max_lifesteal_increase"]
        stats["perm_lifesteal_chance"] = inventory.get("perm_lifesteal_chance_upgrade", 0) * PERM_UPGRADES["perm_lifesteal_chance_upgrade"]["lifesteal_chance_increase"]
        stats["perm_exp_boost"] = inventory.get("perm_exp_upgrade", 0) * PERM_UPGRADES["perm_exp_upgrade"]["exp_increase"]

        # Apply title boosts
        apply_title_boosts(username)

        player_data["stats"] = stats
        user_data["player_data"] = player_data
        save_user_data(username, user_data)
    except Exception as e:
        print(f"Error applying permanent upgrades: {e}")

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
    users = load_all_users()
    if username not in users:  # Check if user exists in users dict
        return False, "Invalid user."
    if pack_key not in MAGIC_PACKS:
        return False, "Unknown magic pack."

    user_data = users[username]
    player_data = user_data.get("player_data", {})
    inventory = player_data.get("inventory", {})
    stats = player_data.get("stats", {})

    if inventory.get(pack_key, 0) < quantity:
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
    user_data["player_data"] = player_data
    save_user_data(username, user_data)

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
    user_data = load_user_data(username)
    if not user_data:
        return

    try:
        player_data = user_data["player_data"]
    except (KeyError, TypeError):
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
    user_data["player_data"] = player_data
    save_user_data(username, user_data)

# -------------------------
# Settings Menu
# -------------------------
def settings_menu(username):
    if not username:
        return

    user_data = load_user_data(username)
    if not user_data:
        return

    player_data = user_data.get("player_data", {})
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
        print("8. Set this machine as home")
        print("9. Back to Main Menu")

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
            equip_titles_menu(username, player_data, None)
        elif choice == '8':
            set_machine_home(username)
        elif choice == '9':
            break
        else:
            print("Invalid choice.")

        # Save settings
        stats['settings'] = settings
        player_data['stats'] = stats
        user_data['player_data'] = player_data
        save_user_data(username, user_data)

    # No database connection to close

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
    apply_title_boosts(username)  # Pass username directly
    # No need to save here, as apply_title_boosts will save

# -------------------------
# Apply Title Boosts
# -------------------------
def apply_title_boosts(username):
    try:
        user_data = load_user_data(username)
        if not user_data:
            return

        player_data = user_data["player_data"]
        stats = player_data["stats"]

        # Reset title boosts
        stats["title_atk_boost"] = 0
        stats["title_def_boost"] = 0
        stats["title_hp_boost"] = 0
        stats["title_mana_boost"] = 0
        stats["title_exp_boost"] = 0
        stats["title_magic_def_boost"] = 0

        # Apply equipped title boosts
        for title_id in stats.get("equipped_titles", []):
            if title_id and title_id in TITLES:
                title = TITLES[title_id]
                stats["title_atk_boost"] += title.get("atk_boost", 0)
                stats["title_def_boost"] += title.get("def_boost", 0)
                stats["title_hp_boost"] += title.get("hp_boost", 0)
                stats["title_mana_boost"] += title.get("mana_boost", 0)
                stats["title_exp_boost"] += title.get("exp_boost", 0)
                stats["title_magic_def_boost"] += title.get("magic_def_boost", 0)

        player_data["stats"] = stats
        user_data["player_data"] = player_data
        save_user_data(username, user_data)
    except Exception as e:
        print(f"Error applying title boosts: {e}")

# -------------------------
# Auto Equip Items
# -------------------------
def auto_equip_items(username):
    try:
        user_data = load_user_data(username)
        if not user_data:
            return

        player_data = user_data["player_data"]
        stats = player_data["stats"]
        inventory = player_data["inventory"]
        equipped = stats["equipped"]

        # Only auto-equip if the setting is enabled
        if not stats["settings"].get("auto_equip_best", False):
            return

        # Auto-equip best weapon
        best_weapon = None
        best_weapon_atk = 0
        for weapon_id, count in inventory.items():
            if count > 0 and weapon_id in WEAPONS:
                weapon_atk = WEAPONS[weapon_id]["atk"]
                if weapon_atk > best_weapon_atk:
                    best_weapon = weapon_id
                    best_weapon_atk = weapon_atk

        if best_weapon and best_weapon != equipped["weapon"]:
            equipped["weapon"] = best_weapon

        # Auto-equip best armor
        best_armor = None
        best_armor_def = 0
        for armor_id, count in inventory.items():
            if count > 0 and armor_id in ARMORS:
                armor_def = ARMORS[armor_id]["def"]
                if armor_def > best_armor_def:
                    best_armor = armor_id
                    best_armor_def = armor_def

        if best_armor and best_armor != equipped["armor"]:
            equipped["armor"] = best_armor

        # Auto-equip best wand
        best_wand = None
        best_wand_magic_atk = 0
        for wand_id, count in inventory.items():
            if count > 0 and wand_id in WANDS:
                wand_magic_atk = WANDS[wand_id]["magic_atk"]
                if wand_magic_atk > best_wand_magic_atk:
                    best_wand = wand_id
                    best_wand_magic_atk = wand_magic_atk

        if best_wand and best_wand != equipped["wand"]:
            equipped["wand"] = best_wand

        # Auto-equip best robe
        best_robe = None
        best_robe_magic_def = 0
        for robe_id, count in inventory.items():
            if count > 0 and robe_id in ROBES:
                robe_magic_def = ROBES[robe_id]["magic_def"]
                if robe_magic_def > best_robe_magic_def:
                    best_robe = robe_id
                    best_robe_magic_def = robe_magic_def

        if best_robe and best_robe != equipped["robe"]:
            equipped["robe"] = best_robe

        # Auto-equip best necklace
        best_necklace = None
        best_necklace_value = 0
        for necklace_id, count in inventory.items():
            if count > 0 and necklace_id in NECKLACES:
                # Calculate total value of necklace bonuses
                necklace = NECKLACES[necklace_id]
                total_value = (
                    necklace.get("hp_bonus", 0) * 1 +
                    necklace.get("mana_bonus", 0) * 1 +
                    necklace.get("atk_bonus", 0) * 2 +
                    necklace.get("def_bonus", 0) * 2 +
                    necklace.get("magic_atk_bonus", 0) * 2 +
                    necklace.get("magic_def_bonus", 0) * 2 +
                    necklace.get("crit_bonus", 0) * 3 +
                    necklace.get("lifesteal_bonus", 0) * 3
                )
                if total_value > best_necklace_value:
                    best_necklace = necklace_id
                    best_necklace_value = total_value

        if best_necklace and best_necklace != equipped["necklace"]:
            equipped["necklace"] = best_necklace

        player_data["stats"]["equipped"] = equipped
        user_data["player_data"] = player_data
        save_user_data(username, user_data)
    except Exception as e:
        print(f"Error auto-equipping items: {e}")

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
    user_data = load_user_data(username)
    if user_data:
        user_data['player_data'] = player_data
        save_user_data(username, user_data)

# -------------------------
# View Achievements Menu
# -------------------------
def view_achievements_menu(username):
    user_data = load_user_data(username)
    if not user_data:
        return

    player_data = user_data.get("player_data", {})
    stats = player_data.get('stats', {})
    unlocked = stats.get('achievements', [])

    print("\n--- Achievements ---")
    for ach_key, achievement in ACHIEVEMENTS.items():
        status = "✓" if ach_key in unlocked else "✗"
        print(f"{status} {achievement['name']}: {achievement['desc']}")

    # No database connection to close

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

    global effective_atk, effective_def, effective_magic_atk, effective_magic_def, effective_hp_bonus, effective_mana_bonus

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

def magic_spell_interface(username):
    user_data = load_user_data(username)
    if not user_data:
        print("User data not found.")
        return

    player_data = user_data.get("player_data", {})
    stats = player_data.get("stats", {})
    learned_spells = stats.get("learned_spells", [])
    equipped_spells = stats.get("equipped_spells", [None, None, None, None])

    while True:
        print("\n--- Magic Spells ---")
        print("Equipped Spells:")
        for i in range(4):
            spell = equipped_spells[i]
            if spell and spell in SPELLS_BY_KEY:
                s = SPELLS_BY_KEY[spell]
                print(f"{i+1}. Slot {i+1}: {s['name']} ({s['mana']} mana)")
            else:
                print(f"{i+1}. Slot {i+1}: None")

        print("\nLearned Spells:")
        for i, spell_key in enumerate(learned_spells, start=1):
            s = SPELLS_BY_KEY.get(spell_key, {})
            print(f"{i+4}. {s.get('name', 'Unknown')} (lvl {s.get('lvl', '?')}, {s.get('mana', '?')} mana) - {s.get('desc', '')}")

        print("0. Back")

        choice = input("Choose slot to equip/unequip or spell to equip: ").strip()

        if choice == '0':
            break
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < 4:  # Unequip slot
                equipped_spells[idx] = None
                print(f"Unequipped slot {idx+1}.")
            elif 4 <= idx < 4 + len(learned_spells):  # Equip spell
                spell_idx = idx - 4
                spell_key = learned_spells[spell_idx]
                s = SPELLS_BY_KEY.get(spell_key, {})
                # Find first empty slot
                empty_slots = [i for i, sp in enumerate(equipped_spells) if sp is None]
                if empty_slots:
                    slot = empty_slots[0]
                    equipped_spells[slot] = spell_key
                    print(f"Equipped {s.get('name', 'Unknown')} in slot {slot+1}.")
                else:
                    print("No empty slots. Unequip a slot first.")
            else:
                print("Invalid choice.")
        else:
            print("Invalid choice.")

    stats["equipped_spells"] = equipped_spells
    player_data["stats"] = stats
    user_data["player_data"] = player_data
    save_user_data(username, user_data)

def main_menu():
    global current_user, score, player_data, money
    current_user = None
    score = 0
    player_data = None
    money = 40

    while True:
        if current_user:
            print(f"\nLogged in as: {current_user}")
            print("1. Play number guessing game")
            print("2. Explore dungeons")
            print("3. Shop")
            print("4. Magic packs")
            print("5. Permanent upgrades")
            print("6. Equip titles")
            print("7. Manage inventory")
            print("8. Equip spells")
            print("9. Settings")
            print("10. Leaderboard")
            print("11. Logout")
            print("12. Exit")
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
                dungeon(current_user)
                # Reload data after dungeon
                score, money, player_data = signin(current_user, password="")
            elif choice == '3':
                shop()
                # Reload data after shop
                score, money, player_data = signin(current_user, password="")
            elif choice == '4':
                magic_pack_interface(current_user)
                # Reload data after packs
                score, money, player_data = signin(current_user, password="")
            elif choice == '5':
                equip_titles_menu(current_user, player_data, None)
                # Reload data after titles
                score, money, player_data = signin(current_user, password="")
            elif choice == '6':
                manage_inventory_menu(current_user, player_data, None)
                # Reload data after inventory
                score, money, player_data = signin(current_user, password="")
            elif choice == '7':
                magic_spell_interface(current_user)
                # Reload data after spells
                score, money, player_data = signin(current_user, password="")
            elif choice == '8':
                settings_menu(current_user)
                # Reload data after settings
                score, money, player_data = signin(current_user, password="")
            elif choice == '9':
                if get_leaderboard():
                    print("\n--- Leaderboard ---")
                    leaderboard = get_leaderboard()
                    for rank, (uname, user_score) in enumerate(leaderboard, start=1):
                        print(f"{rank}. {uname} - {user_score}")
                else:
                    print("No users yet!")
            elif choice == '10':
                print("Logged out.")
                stop_autosave()  # Stop autosave when logging out
                current_user = None
                score = 0
                player_data = None
                money = 40
            elif choice == '11':
                print("Goodbye! Data saved automatically.")
                save_all_data()
                break
            elif choice == '5':
                permanent_upgrades_interface(current_user)
                # Reload data after upgrades
                score, money, player_data = signin(current_user, password="")
            elif choice == '10234':
                debug_console(current_user, score, money, player_data, USERS_DIR)
            else:
                print("Invalid choice.")
        else:
            if choice == '1':
                machine_id = get_machine_id()
                home_accounts = get_home_accounts_for_machine(machine_id)

                if home_accounts:
                    if len(home_accounts) == 1:
                        username = home_accounts[0]
                        print(f"Home account detected: {username}")
                        confirm = input("Login to this account? (y/n): ").strip().lower()
                        if confirm in ['y', 'yes']:
                            password = input("Password: ").strip()
                            score, money, player_data = signin(username, password)
                            if score is not None:
                                current_user = username
                                ensure_user_fields(current_user)
                                _, _, player_data = signin(username, password)
                                print(f"Login successful! Highscore = {score}")
                            else:
                                print("Login failed!")
                        else:
                            print("Login cancelled.")
                    else:
                        print("Multiple home accounts detected:")
                        for i, acc in enumerate(home_accounts, 1):
                            print(f"{i}. {acc}")
                        choice_idx = input("Choose account number or enter username manually: ").strip()
                        if choice_idx.isdigit():
                            idx = int(choice_idx) - 1
                            if 0 <= idx < len(home_accounts):
                                username = home_accounts[idx]
                            else:
                                username = input("Username: ").strip().lower()
                        else:
                            username = choice_idx.strip().lower()
                        password = input("Password: ").strip()
                        score, money, player_data = signin(username, password)
                        if score is not None:
                            current_user = username
                            ensure_user_fields(current_user)
                            _, _, player_data = signin(username, password)
                            print(f"Login successful! Highscore = {score}")
                        else:
                            print("Login failed!")
                else:
                    username = input("Username: ").strip().lower()
                    password = input("Password: ").strip()
                    score, money, player_data = signin(username, password)
                    if score is not None:
                        current_user = username
                        ensure_user_fields(current_user)
                        _, _, player_data = signin(username, password)
                        print(f"Login successful! Highscore = {score}")
                    else:
                        print("Login failed!")
            elif choice == '2':
                username = input("\nUsername: ").strip()
                password = input("Password: ").strip()
                if signup(username, password):
                    score, money, player_data = signin(username, password)
                    current_user = username
                    ensure_user_fields(current_user)
                    # Reload updated player data
                    _, _, player_data = signin(username, password)
                    print(f"Signup successful! You are now logged in.")
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