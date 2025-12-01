"""
Game Configuration Constants

Centralized configuration for PyQuest Monster Game.
All magic numbers and game balance constants are defined here.
"""

# ============================================================================
# UI LAYOUT CONSTANTS
# ============================================================================

# Window Dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1050

# Canvas Dimensions (image display area)
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400

# Button Layout
BUTTONS_PER_ROW = 3
BUTTON_WIDTH = 22
BUTTON_HEIGHT = 2

# Text Area
TEXT_AREA_WIDTH = 80
TEXT_AREA_HEIGHT = 15

# ============================================================================
# TIMING CONSTANTS (milliseconds)
# ============================================================================

# UI Delays
VERY_SHORT_DELAY = 200   # Window focus delay
SHORT_DELAY = 1500       # Combat animation delays
MEDIUM_DELAY = 3000      # Item purchase, level up displays
LONG_DELAY = 4000        # Town fountain, tavern, blacksmith completion
VERY_LONG_DELAY = 8000   # Victory fireworks + buffer

# Combat Animation Timings
HERO_ATTACK_ANIMATION_DELAY = 1500
MONSTER_ATTACK_ANIMATION_DELAY = 1500
COMBAT_ROUND_DELAY = 2000
DEATH_ANIMATION_DELAY = 2000

# ============================================================================
# GAME MECHANICS CONSTANTS
# ============================================================================

# Town Services
BLACKSMITH_UPGRADE_COST = 100
BLACKSMITH_ATTACK_BONUS = 1
BLACKSMITH_DEFENSE_BONUS = 1
FOUNTAIN_HEAL_AMOUNT = 3

# Experience & Leveling
XP_PER_LEVEL_MULTIPLIER = 5  # XP needed = level * 5
LEVEL_UP_HP_BONUS = 5
LEVEL_UP_ATTACK_BONUS = 2
LEVEL_UP_DEFENSE_BONUS = 2

# Combat System
DAMAGE_VARIANCE_MIN = 0.8        # 80% minimum damage
DAMAGE_VARIANCE_MAX = 1.2        # 120% maximum damage
LEVEL_MODIFIER_PER_LEVEL = 0.15  # ±15% per level difference
MAX_LEVEL_DIFFERENCE = 5         # Cap level modifier at ±5 levels
MAX_DEFENSE_REDUCTION = 0.85     # Maximum damage reduction from defense (85%)
DEFENSE_SCALING_FACTOR = 15      # Used in defense percentage calculation

# Monster Encounter System
ELITE_ENCOUNTER_CHANCE = 0.10    # 10% chance for elite encounter
ELITE_STAT_MULTIPLIER = 1.5      # Elite monsters have 1.5x stats

# Quest System
QUEST_LEVEL_RANGE_MIN = -2       # Can accept quests for monsters (hero_level - 2)
QUEST_LEVEL_RANGE_MAX = 1        # Can accept quests for monsters (hero_level + 1)

# Bounty System
BOUNTY_COLLECTOR_MIN_KILLS = 3   # Minimum kills for collector bounties
BOUNTY_COLLECTOR_MAX_KILLS = 7   # Maximum kills for collector bounties

# Achievement System
ACHIEVEMENT_REWARD_BRONZE = 20  # Bronze tier achievement reward (gold)
ACHIEVEMENT_REWARD_SILVER = 50  # Silver tier achievement reward (gold)
ACHIEVEMENT_REWARD_GOLD = 100    # Gold tier achievement reward (gold)

# ============================================================================
# AUDIO CONFIGURATION
# ============================================================================

# Audio System
AUDIO_FREQUENCY = 22050
AUDIO_BUFFER_SIZE = 512
AUDIO_CHANNELS = 8               # Number of simultaneous sound channels
MUSIC_VOLUME_DEFAULT = 0.5       # Background music volume (0.0 to 1.0)
SFX_VOLUME_DEFAULT = 0.8         # Sound effects volume (0.0 to 1.0)

# ============================================================================
# COLOR SCHEME
# ============================================================================

# UI Colors
COLOR_BACKGROUND = '#1a1a1a'
COLOR_TEXT_AREA_BG = '#2a2a2a'
COLOR_TEXT_DEFAULT = '#00ff00'    # Green terminal-style text
COLOR_BUTTON_BG = '#4a4a4a'
COLOR_BUTTON_FG = '#ffffff'

# Text Highlighting Colors
COLOR_DAMAGE = '#ff8800'          # Orange for damage numbers
COLOR_ATTACK = '#ff6600'          # Red-orange for attack stats
COLOR_DEFENSE = '#4169e1'         # Royal blue for defense
COLOR_HP = '#ff0000'              # Red for HP
COLOR_GOLD = '#ffd700'            # Gold color
COLOR_XP = '#9370db'              # Medium purple for XP
COLOR_LEVEL = '#00ff00'           # Green for level
COLOR_ERROR = '#ff0000'           # Red for errors
COLOR_SUCCESS = '#00ff00'         # Green for success messages
COLOR_WARNING = '#ffff00'         # Yellow for warnings
COLOR_QUEST = '#87ceeb'           # Sky blue for quests
COLOR_ELITE = '#ff00ff'           # Magenta for elite encounters

# Biome Fallback Colors
COLOR_BIOME_GRASSLAND = '#4a7c59'
COLOR_BIOME_DESERT = '#daa520'
COLOR_BIOME_DUNGEON = '#2d1f1a'
COLOR_BIOME_OCEAN = '#0077be'
COLOR_BIOME_TOWN = '#2B4C3D'

# ============================================================================
# BIOME CONFIGURATION
# ============================================================================

# Valid Biome Names
BIOMES_COMBAT = ['grassland', 'desert', 'dungeon', 'ocean']
BIOMES_ALL = ['grassland', 'desert', 'dungeon', 'ocean', 'town']

# Biome Backgrounds
BIOME_BACKGROUNDS = {
    'grassland': 'art/grassy_background.png',
    'desert': 'art/desert_background.png',
    'dungeon': 'art/dungeon_background.png',
    'ocean': 'art/ocean_background.png',
    'town': 'art/town_background.png'
}

# ============================================================================
# HERO CLASSES
# ============================================================================

VALID_HERO_CLASSES = ['Warrior', 'Ninja', 'Magician']
SHOP_CLASS_ALL = 'All'  # Items available to all classes

# ============================================================================
# FILE PATHS
# ============================================================================

# Directories
DIR_MONSTERS = 'monsters/'
DIR_HEROES = 'heros/'
DIR_ART = 'art/'
DIR_SOUNDS = 'sounds/'
DIR_SAVES = 'saves/'
DIR_LOGS = 'logs/'

# Data Files
FILE_STORE = 'store.yaml'
FILE_TAVERN = 'tavern.yaml'

# Special Backgrounds
BACKGROUND_SHOP = 'art/shop_background.png'
BACKGROUND_BLACKSMITH = 'art/blacksmith_background.png'
BACKGROUND_TAVERN = 'art/tavern_background.png'

# Special Images
IMAGE_GAME_OVER = 'art/game_over_logo.png'
IMAGE_VICTORY_FIREWORKS = 'art/victory_fireworks.png'

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Log Levels by Module (can be overridden)
LOGGING_LEVELS = {
    'game_state': 'INFO',
    'combat': 'DEBUG',
    'gui': 'INFO',
    'audio': 'WARNING',
}

LOG_TIMESTAMP_FORMAT = '%Y%m%d_%H%M%S'
LOG_FILE_PREFIX = 'game_'
LOG_FILE_EXTENSION = '.log'

# ============================================================================
# VALIDATION CONSTANTS
# ============================================================================

# Python Version Requirements
PYTHON_VERSION_MIN_MAJOR = 3
PYTHON_VERSION_MIN_MINOR = 7

# Required Packages
REQUIRED_PACKAGES = {
    'tkinter': 'tkinter (built-in)',
    'PIL': 'Pillow>=10.0.0',
    'pygame': 'pygame>=2.5.0',
    'yaml': 'PyYAML>=6.0'
}

# ============================================================================
# IMAGE DISPLAY SETTINGS
# ============================================================================

# Image Sizing
IMAGE_DEFAULT_SIZE = (200, 150)
IMAGE_SINGLE_SIZE = (400, 300)

# Layout Types
LAYOUT_SINGLE = "single"
LAYOUT_HORIZONTAL = "horizontal"
LAYOUT_VERTICAL = "vertical"
LAYOUT_GRID = "grid"
LAYOUT_AUTO = "auto"

# ============================================================================
# AUDIO CONSTANTS
# ============================================================================

SOUND_BLACKSMITH_HAMMER = 'smith-hammer.mp3'
SOUND_BLACKSMITH_SHARPEN = 'blacksmith-sharpen.mp3'

# ============================================================================
# GAME BALANCE NOTES
# ============================================================================

"""
BALANCING NOTES:

Combat System:
- Damage variance (80-120%) keeps combat unpredictable but not random
- Level modifier (±15% per level) makes level differences matter
- Defense cap (85%) prevents total immunity
- Minimum damage scales with level to prevent stalemates

Economy:
- Blacksmith upgrades (100 gold) are expensive early game, cheap late game
- Fountain (3 HP) provides minor healing without trivializing combat
- Achievement rewards scale with difficulty

Progression:
- XP requirement (level * 5) creates linear progression curve
- Level up bonuses (+5 HP, +2 ATK, +2 DEF) are meaningful but balanced
- Quest level range (±2 levels) prevents impossible quests

To adjust difficulty:
- Increase DAMAGE_VARIANCE_MAX for more chaos
- Increase LEVEL_MODIFIER_PER_LEVEL for harder level scaling
- Decrease FOUNTAIN_HEAL_AMOUNT for harder game
- Increase XP_PER_LEVEL_MULTIPLIER for slower progression
"""
