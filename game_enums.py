from enum import Enum

class BiomeType(str, Enum):
    GRASSLAND = "grassland"
    DESERT = "desert"
    DUNGEON = "dungeon"
    OCEAN = "ocean"
    TOWN = "town"

class ItemType(str, Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    POTION = "potion"
    MISC = "misc"

class HeroClass(str, Enum):
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ROGUE = "Rogue"
    PALADIN = "Paladin"

class GameStateKey(str, Enum):
    HERO = "hero"
    MONSTERS = "monsters"
    CURRENT_BIOME = "current_biome"
    LAST_BIOME = "last_biome"
