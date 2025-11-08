#!/usr/bin/env python3
"""
Monster Art Generator - Creates pixel art for all monsters
Creates 32x32 pixel art monsters in the style of create_magician_art.py
"""

import numpy as np
from PIL import Image
import os

def create_monster_art(monster_name):
    """Create pixel art for a specific monster"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Common color palette
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    RED = [255, 50, 50, 255]
    DARK_RED = [180, 30, 30, 255]
    GREEN = [50, 180, 50, 255]
    DARK_GREEN = [30, 120, 30, 255]
    BROWN = [139, 69, 19, 255]
    DARK_BROWN = [101, 67, 33, 255]
    GRAY = [128, 128, 128, 255]
    DARK_GRAY = [64, 64, 64, 255]
    PURPLE = [128, 0, 128, 255]
    DARK_PURPLE = [75, 0, 75, 255]
    ORANGE = [255, 165, 0, 255]
    YELLOW = [255, 255, 0, 255]
    BLUE = [50, 50, 255, 255]
    CYAN = [0, 255, 255, 255]
    PINK = [255, 192, 203, 255]
    
    monster_lower = monster_name.lower()
    
    if monster_lower == 'bunny':
        # Cute bunny - white with pink ears
        # Head (round)
        for y in range(8, 16):
            for x in range(12, 20):
                if (x-16)**2 + (y-12)**2 <= 16:  # Circular head
                    canvas[y][x] = WHITE
        
        # Ears (long rabbit ears)
        for y in range(4, 10):
            canvas[y][14] = WHITE
            canvas[y][17] = WHITE
        # Pink inner ears
        canvas[5][14] = PINK
        canvas[6][14] = PINK
        canvas[5][17] = PINK
        canvas[6][17] = PINK
        
        # Eyes
        canvas[10][14] = BLACK
        canvas[10][17] = BLACK
        
        # Nose
        canvas[12][15] = PINK
        canvas[12][16] = PINK
        
        # Body (oval)
        for y in range(16, 26):
            for x in range(11, 21):
                if (x-16)**2/20 + (y-21)**2/16 <= 1:
                    canvas[y][x] = WHITE
        
        # Tail (fluffy)
        canvas[24][19] = WHITE
        canvas[25][19] = WHITE
        canvas[25][20] = WHITE
        
        # Legs
        for x in range(13, 15):
            canvas[26][x] = WHITE
            canvas[27][x] = WHITE
        for x in range(17, 19):
            canvas[26][x] = WHITE
            canvas[27][x] = WHITE
    
    elif monster_lower == 'caveman':
        # Primitive caveman - brown hair, beige skin, animal hide
        SKIN = [222, 184, 135, 255]
        HIDE = [101, 67, 33, 255]
        
        # Head
        for y in range(6, 14):
            for x in range(12, 20):
                canvas[y][x] = SKIN
        
        # Wild hair
        for y in range(4, 8):
            for x in range(11, 21):
                canvas[y][x] = DARK_BROWN
        
        # Eyes (angry)
        canvas[9][14] = BLACK
        canvas[9][17] = BLACK
        
        # Unibrow
        for x in range(13, 19):
            canvas[8][x] = DARK_BROWN
        
        # Nose and mouth
        canvas[11][15] = DARK_BROWN
        canvas[12][15] = BLACK
        canvas[12][16] = BLACK
        
        # Body (animal hide)
        for y in range(14, 26):
            for x in range(11, 21):
                canvas[y][x] = HIDE
        
        # Hide spots
        canvas[16][13] = DARK_BROWN
        canvas[18][18] = DARK_BROWN
        canvas[20][14] = DARK_BROWN
        
        # Arms
        for y in range(16, 22):
            canvas[y][9] = SKIN   # Left arm
            canvas[y][22] = SKIN  # Right arm
        
        # Legs
        for y in range(26, 30):
            canvas[y][13] = SKIN
            canvas[y][18] = SKIN
    
    elif monster_lower == 'cyclops':
        # Giant cyclops - one big eye, muscular
        SKIN = [180, 150, 120, 255]
        
        # Large head
        for y in range(4, 16):
            for x in range(10, 22):
                canvas[y][x] = SKIN
        
        # One giant eye (centered)
        for y in range(8, 12):
            for x in range(14, 18):
                canvas[y][x] = WHITE
        canvas[9][15] = BLACK
        canvas[10][16] = BLACK
        canvas[9][16] = BLACK
        
        # Angry eyebrow
        for x in range(13, 19):
            canvas[7][x] = DARK_BROWN
        
        # Big nose
        canvas[12][15] = DARK_BROWN
        canvas[13][15] = DARK_BROWN
        
        # Mouth (grimacing)
        for x in range(14, 18):
            canvas[14][x] = BLACK
        
        # Muscular body
        for y in range(16, 28):
            for x in range(8, 24):
                canvas[y][x] = SKIN
        
        # Chest muscles
        canvas[18][13] = DARK_BROWN  # Shadow
        canvas[18][18] = DARK_BROWN
        
        # Arms (thick)
        for y in range(18, 26):
            for x in range(6, 9):
                canvas[y][x] = SKIN  # Left arm
            for x in range(23, 26):
                canvas[y][x] = SKIN  # Right arm
    
    elif monster_lower == 'demon':
        # Infernal demon - horns, red eyes, claws, hellfire aura
        DARK_SKIN = [101, 67, 33, 255]
        HORN = [64, 64, 64, 255]
        FLAME_RED = [255, 69, 0, 255]
        FLAME_ORANGE = [255, 140, 0, 255]
        FLAME_YELLOW = [255, 215, 0, 255]
        
        # Head (dark skin)
        for y in range(8, 16):
            for x in range(12, 20):
                if (x-16)**2 + (y-12)**2 <= 16:  # Circular head
                    canvas[y][x] = DARK_SKIN
        
        # Horns (curved upward)
        canvas[6][13] = HORN
        canvas[5][13] = HORN
        canvas[4][12] = HORN
        canvas[6][18] = HORN
        canvas[5][18] = HORN
        canvas[4][19] = HORN
        
        # Eyes (glowing red)
        canvas[10][14] = RED
        canvas[10][17] = RED
        canvas[11][14] = FLAME_RED
        canvas[11][17] = FLAME_RED
        
        # Evil grin with fangs
        canvas[13][14] = BLACK
        canvas[13][15] = BLACK
        canvas[13][16] = BLACK
        canvas[13][17] = BLACK
        canvas[14][14] = WHITE  # Fangs
        canvas[14][17] = WHITE
        
        # Muscular body
        for y in range(16, 26):
            for x in range(10, 22):
                canvas[y][x] = DARK_SKIN
        
        # Arms
        for y in range(18, 24):
            canvas[y][8] = DARK_SKIN   # Left arm
            canvas[y][9] = DARK_SKIN
            canvas[y][22] = DARK_SKIN  # Right arm
            canvas[y][23] = DARK_SKIN
        
        # Clawed hands
        canvas[22][6] = GRAY
        canvas[23][6] = GRAY
        canvas[22][7] = GRAY
        canvas[22][24] = GRAY
        canvas[23][24] = GRAY
        canvas[22][25] = GRAY
        
        # Legs
        for y in range(26, 30):
            for x in range(12, 16):
                canvas[y][x] = DARK_SKIN  # Left leg
            for x in range(16, 20):
                canvas[y][x] = DARK_SKIN  # Right leg
        
        # Hooves
        for x in range(12, 16):
            canvas[30][x] = BLACK
        for x in range(16, 20):
            canvas[30][x] = BLACK
        
        # Tail
        canvas[20][24] = DARK_SKIN
        canvas[19][25] = DARK_SKIN
        canvas[18][26] = DARK_SKIN
        canvas[17][27] = DARK_SKIN
        
        # Flame aura
        canvas[12][10] = FLAME_YELLOW
        canvas[15][9] = FLAME_ORANGE
        canvas[18][8] = FLAME_RED
        canvas[12][21] = FLAME_YELLOW
        canvas[15][22] = FLAME_ORANGE
        canvas[18][23] = FLAME_RED
    
    elif monster_lower == 'flytrap':
        # Venus flytrap monster - plant with teeth
        STEM = [34, 139, 34, 255]
        TRAP_OUTSIDE = [50, 150, 50, 255]
        TRAP_INSIDE = [255, 20, 147, 255]  # Pink inside
        
        # Main stem
        for y in range(20, 30):
            for x in range(15, 17):
                canvas[y][x] = STEM
        
        # Bulb base
        for y in range(16, 22):
            for x in range(13, 19):
                canvas[y][x] = TRAP_OUTSIDE
        
        # Upper jaw
        for y in range(6, 12):
            for x in range(10, 22):
                if y <= 8 or (x >= 13 and x <= 18):
                    canvas[y][x] = TRAP_OUTSIDE
        
        # Lower jaw
        for y in range(12, 18):
            for x in range(10, 22):
                if y >= 15 or (x >= 13 and x <= 18):
                    canvas[y][x] = TRAP_OUTSIDE
        
        # Inside mouth (pink)
        for y in range(9, 15):
            for x in range(14, 18):
                canvas[y][x] = TRAP_INSIDE
        
        # Teeth (white spikes)
        canvas[8][12] = WHITE
        canvas[8][19] = WHITE
        canvas[15][12] = WHITE
        canvas[15][19] = WHITE
        canvas[9][11] = WHITE
        canvas[14][20] = WHITE
        
        # Eyes on stalks
        canvas[4][13] = GREEN
        canvas[3][13] = BLACK  # Eye
        canvas[4][18] = GREEN
        canvas[3][18] = BLACK  # Eye
    
    elif monster_lower == 'hydra':
        # Multi-headed dragon hydra
        SCALES = [34, 139, 34, 255]
        
        # Main body
        for y in range(18, 28):
            for x in range(8, 24):
                canvas[y][x] = SCALES
        
        # Three heads
        # Left head
        for y in range(6, 12):
            for x in range(6, 12):
                canvas[y][x] = SCALES
        canvas[8][8] = RED    # Eye
        canvas[10][9] = BLACK # Nostril
        
        # Center head (larger)
        for y in range(4, 12):
            for x in range(13, 19):
                canvas[y][x] = SCALES
        canvas[7][15] = RED   # Eye
        canvas[9][16] = BLACK # Nostril
        
        # Right head  
        for y in range(6, 12):
            for x in range(20, 26):
                canvas[y][x] = SCALES
        canvas[8][22] = RED   # Eye
        canvas[10][23] = BLACK# Nostril
        
        # Necks connecting to heads
        for y in range(12, 18):
            canvas[y][9] = SCALES   # Left neck
            canvas[y][16] = SCALES  # Center neck
            canvas[y][23] = SCALES  # Right neck
        
        # Spikes along back
        canvas[16][12] = DARK_GREEN
        canvas[16][16] = DARK_GREEN
        canvas[16][20] = DARK_GREEN
    
    elif monster_lower == 'lich':
        # Undead lich - skeletal, dark robes, glowing eyes
        BONE = [245, 245, 220, 255]
        ROBE = [25, 25, 112, 255]
        GLOW = [0, 255, 0, 255]
        
        # Skull head
        for y in range(6, 14):
            for x in range(12, 20):
                canvas[y][x] = BONE
        
        # Eye sockets (glowing green)
        canvas[9][14] = BLACK
        canvas[9][15] = GLOW
        canvas[9][16] = BLACK
        canvas[9][17] = GLOW
        
        # Nasal cavity
        canvas[11][15] = BLACK
        canvas[12][15] = BLACK
        
        # Dark robes
        for y in range(14, 28):
            for x in range(10, 22):
                canvas[y][x] = ROBE
        
        # Robe shadows
        for y in range(16, 26):
            canvas[y][11] = BLACK
            canvas[y][20] = BLACK
        
        # Skeletal hands
        canvas[18][8] = BONE   # Left hand
        canvas[19][8] = BONE
        canvas[18][23] = BONE  # Right hand
        canvas[19][23] = BONE
        
        # Staff (magical)
        for y in range(10, 20):
            canvas[y][7] = DARK_BROWN
        # Glowing orb on staff
        canvas[8][7] = GLOW
        canvas[9][7] = GLOW
    
    elif monster_lower == 'lola':
        # Black and white dog face - friendly border collie style
        DOG_WHITE = [255, 255, 255, 255]
        DOG_BLACK = [25, 25, 25, 255]
        DOG_PINK = [255, 182, 193, 255]  # Light pink for nose/tongue
        
        # Main head shape (white base)
        for y in range(6, 18):
            for x in range(10, 22):
                canvas[y][x] = DOG_WHITE
        
        # Black markings around eyes (border collie pattern)
        # Left eye marking
        for y in range(7, 12):
            for x in range(10, 15):
                canvas[y][x] = DOG_BLACK
        
        # Right eye marking  
        for y in range(7, 12):
            for x in range(17, 22):
                canvas[y][x] = DOG_BLACK
        
        # White area around eyes (classic border collie blaze)
        for y in range(8, 11):
            for x in range(15, 17):
                canvas[y][x] = DOG_WHITE
        
        # Ears (black, floppy)
        for y in range(4, 8):
            canvas[y][11] = DOG_BLACK  # Left ear
            canvas[y][12] = DOG_BLACK
            canvas[y][19] = DOG_BLACK  # Right ear  
            canvas[y][20] = DOG_BLACK
        
        # Eyes (friendly, brown)
        canvas[9][13] = BROWN
        canvas[9][18] = BROWN
        # Eye highlights
        canvas[8][13] = WHITE
        canvas[8][18] = WHITE
        
        # Snout (white with black nose)
        for y in range(12, 16):
            for x in range(14, 18):
                canvas[y][x] = DOG_WHITE
        
        # Black nose
        canvas[13][15] = DOG_BLACK
        canvas[13][16] = DOG_BLACK
        canvas[14][15] = DOG_BLACK
        canvas[14][16] = DOG_BLACK
        
        # Mouth (happy expression)
        canvas[15][14] = DOG_BLACK  # Left side of mouth
        canvas[15][17] = DOG_BLACK  # Right side of mouth
        canvas[16][15] = DOG_PINK   # Tongue showing
        canvas[16][16] = DOG_PINK
        
        # Black markings on top of head
        for y in range(6, 9):
            for x in range(13, 19):
                canvas[y][x] = DOG_BLACK
        
        # Body (keeping it simple - just the head/neck area)
        for y in range(18, 26):
            for x in range(12, 20):
                canvas[y][x] = DOG_WHITE
        
        # Black patches on body
        for y in range(20, 24):
            canvas[y][13] = DOG_BLACK
            canvas[y][18] = DOG_BLACK
    
    elif monster_lower == 'maddog':
        # Rabid dog - snarling, foam at mouth
        FUR = [101, 67, 33, 255]
        
        # Head (dog shaped)
        for y in range(8, 16):
            for x in range(10, 22):
                canvas[y][x] = FUR
        
        # Snout (extended)
        for y in range(12, 16):
            for x in range(22, 26):
                canvas[y][x] = FUR
        
        # Ears (floppy)
        for y in range(6, 10):
            canvas[y][12] = FUR
            canvas[y][19] = FUR
        
        # Eyes (angry red)
        canvas[10][14] = RED
        canvas[10][17] = RED
        
        # Nose
        canvas[13][24] = BLACK
        
        # Mouth (snarling with teeth)
        canvas[15][22] = BLACK
        canvas[15][23] = WHITE  # Tooth
        canvas[15][24] = BLACK
        canvas[15][25] = WHITE  # Tooth
        
        # Foam at mouth
        canvas[16][23] = WHITE
        canvas[16][24] = WHITE
        
        # Body
        for y in range(16, 26):
            for x in range(8, 24):
                canvas[y][x] = FUR
        
        # Legs
        for y in range(26, 30):
            canvas[y][11] = FUR
            canvas[y][14] = FUR
            canvas[y][17] = FUR
            canvas[y][20] = FUR
        
        # Tail (aggressive, raised)
        for y in range(14, 18):
            canvas[y][6] = FUR
            canvas[y][7] = FUR
    
    elif monster_lower == 'manbearpig':
        # Hybrid creature - man/bear/pig features
        FUR = [101, 67, 33, 255]
        SKIN = [255, 192, 203, 255]  # Pig pink
        
        # Head (mix of features)
        for y in range(6, 16):
            for x in range(10, 22):
                canvas[y][x] = FUR
        
        # Pig snout
        for y in range(12, 15):
            for x in range(20, 24):
                canvas[y][x] = SKIN
        # Nostrils
        canvas[13][21] = BLACK
        canvas[13][22] = BLACK
        
        # Bear ears
        canvas[7][12] = FUR
        canvas[7][19] = FUR
        canvas[6][12] = FUR
        canvas[6][19] = FUR
        
        # Human-like eyes
        canvas[10][14] = WHITE
        canvas[10][17] = WHITE
        canvas[10][14] = BLACK
        canvas[10][17] = BLACK
        
        # Large body (bear-like)
        for y in range(16, 28):
            for x in range(8, 24):
                canvas[y][x] = FUR
        
        # Arms (human-like but furry)
        for y in range(18, 26):
            for x in range(5, 8):
                canvas[y][x] = FUR
            for x in range(24, 27):
                canvas[y][x] = FUR
        
        # Claws
        canvas[25][5] = BLACK
        canvas[25][26] = BLACK
    
    elif monster_lower == 'manticore':
        # Lion body, human head, scorpion tail
        MANE = [218, 165, 32, 255]  # Golden
        BODY = [160, 82, 45, 255]   # Saddle brown
        
        # Human-like head
        for y in range(6, 14):
            for x in range(12, 20):
                canvas[y][x] = [222, 184, 135, 255]  # Skin
        
        # Lion mane
        for y in range(4, 10):
            for x in range(10, 22):
                canvas[y][x] = MANE
        for y in range(10, 16):
            canvas[y][10] = MANE
            canvas[y][21] = MANE
        
        # Eyes (intelligent but fierce)
        canvas[9][14] = BLACK
        canvas[9][17] = BLACK
        
        # Lion body
        for y in range(14, 24):
            for x in range(8, 24):
                canvas[y][x] = BODY
        
        # Legs
        for y in range(24, 28):
            canvas[y][10] = BODY
            canvas[y][13] = BODY
            canvas[y][18] = BODY
            canvas[y][21] = BODY
        
        # Scorpion tail (curved up)
        canvas[12][26] = DARK_BROWN
        canvas[10][27] = DARK_BROWN
        canvas[8][28] = DARK_BROWN
        canvas[6][29] = DARK_BROWN
        # Stinger
        canvas[5][29] = BLACK
        
        # Wings
        for y in range(12, 18):
            canvas[y][6] = GRAY
            canvas[y][25] = GRAY
    
    elif monster_lower == 'ninja':
        # Stealthy ninja in black
        NINJA_BLACK = [25, 25, 25, 255]
        
        # Head (mostly covered)
        for y in range(6, 14):
            for x in range(12, 20):
                canvas[y][x] = NINJA_BLACK
        
        # Eyes (only visible part)
        canvas[9][14] = WHITE
        canvas[9][15] = BLACK
        canvas[9][16] = WHITE
        canvas[9][17] = BLACK
        
        # Body (ninja outfit)
        for y in range(14, 26):
            for x in range(11, 21):
                canvas[y][x] = NINJA_BLACK
        
        # Arms
        for y in range(16, 24):
            for x in range(8, 11):
                canvas[y][x] = NINJA_BLACK
            for x in range(21, 24):
                canvas[y][x] = NINJA_BLACK
        
        # Legs
        for y in range(26, 30):
            canvas[y][13] = NINJA_BLACK
            canvas[y][18] = NINJA_BLACK
        
        # Katana (sword)
        for y in range(8, 18):
            canvas[y][6] = GRAY  # Blade
        canvas[18][6] = DARK_BROWN  # Handle
        canvas[19][6] = DARK_BROWN
        
        # Throwing stars
        canvas[12][26] = GRAY
        canvas[14][27] = GRAY
    
    elif monster_lower == 'slime':
        # Gelatinous slime creature
        SLIME_GREEN = [50, 205, 50, 255]
        SLIME_DARK = [34, 139, 34, 255]
        
        # Main slime blob (oval/circular)
        for y in range(8, 24):
            for x in range(8, 24):
                if (x-16)**2/64 + (y-16)**2/64 <= 1:
                    canvas[y][x] = SLIME_GREEN
        
        # Darker slime core
        for y in range(12, 20):
            for x in range(12, 20):
                if (x-16)**2/16 + (y-16)**2/16 <= 1:
                    canvas[y][x] = SLIME_DARK
        
        # Eyes floating in slime
        canvas[13][14] = BLACK
        canvas[13][18] = BLACK
        # Eye highlights
        canvas[12][14] = WHITE
        canvas[12][18] = WHITE
        
        # Slime drips
        canvas[24][10] = SLIME_GREEN
        canvas[25][11] = SLIME_GREEN
        canvas[24][21] = SLIME_GREEN
        canvas[25][20] = SLIME_GREEN
        
        # Bubbles in slime
        canvas[15][13] = [144, 238, 144, 255]  # Light green
        canvas[17][19] = [144, 238, 144, 255]
    
    elif monster_lower == 'snake':
        # Serpent - long and coiled
        SNAKE_GREEN = [34, 139, 34, 255]
        
        # Snake body (coiled pattern)
        # Starting from head
        for x in range(20, 26):
            canvas[8][x] = SNAKE_GREEN   # Head
        
        # Body coils
        for y in range(9, 12):
            canvas[y][19] = SNAKE_GREEN
        for x in range(15, 20):
            canvas[12][x] = SNAKE_GREEN
        for y in range(13, 16):
            canvas[y][14] = SNAKE_GREEN
        for x in range(14, 18):
            canvas[16][x] = SNAKE_GREEN
        for y in range(17, 20):
            canvas[y][18] = SNAKE_GREEN
        for x in range(18, 22):
            canvas[20][x] = SNAKE_GREEN
        for y in range(21, 24):
            canvas[y][22] = SNAKE_GREEN
        
        # Head details
        canvas[8][24] = RED      # Eye
        canvas[8][25] = BLACK    # Pupil
        canvas[9][26] = RED      # Forked tongue
        canvas[10][26] = RED
        
        # Scale pattern
        canvas[12][16] = DARK_GREEN
        canvas[16][16] = DARK_GREEN
        canvas[20][20] = DARK_GREEN
    
    elif monster_lower == 'spider':
        # Eight-legged spider
        SPIDER_BLACK = [25, 25, 25, 255]
        
        # Body (abdomen)
        for y in range(12, 20):
            for x in range(12, 20):
                canvas[y][x] = SPIDER_BLACK
        
        # Head (cephalothorax)
        for y in range(8, 14):
            for x in range(14, 18):
                canvas[y][x] = SPIDER_BLACK
        
        # Eyes (multiple)
        canvas[9][15] = RED
        canvas[9][16] = RED
        canvas[10][14] = RED
        canvas[10][17] = RED
        
        # Legs (8 legs - 4 on each side)
        # Left legs
        canvas[10][8] = SPIDER_BLACK   # Leg 1
        canvas[11][6] = SPIDER_BLACK
        canvas[13][7] = SPIDER_BLACK   # Leg 2
        canvas[14][5] = SPIDER_BLACK
        canvas[16][8] = SPIDER_BLACK   # Leg 3
        canvas[17][6] = SPIDER_BLACK
        canvas[18][9] = SPIDER_BLACK   # Leg 4
        canvas[19][7] = SPIDER_BLACK
        
        # Right legs
        canvas[10][23] = SPIDER_BLACK  # Leg 1
        canvas[11][25] = SPIDER_BLACK
        canvas[13][24] = SPIDER_BLACK  # Leg 2
        canvas[14][26] = SPIDER_BLACK
        canvas[16][23] = SPIDER_BLACK  # Leg 3
        canvas[17][25] = SPIDER_BLACK
        canvas[18][22] = SPIDER_BLACK  # Leg 4
        canvas[19][24] = SPIDER_BLACK
        
        # Web pattern (optional)
        canvas[4][16] = WHITE
        canvas[5][15] = WHITE
        canvas[5][17] = WHITE
    
    elif monster_lower == 'spider2':
        # Variant spider - maybe larger or different colored
        SPIDER_BROWN = [101, 67, 33, 255]
        
        # Larger body
        for y in range(10, 22):
            for x in range(10, 22):
                canvas[y][x] = SPIDER_BROWN
        
        # Head
        for y in range(6, 12):
            for x in range(13, 19):
                canvas[y][x] = SPIDER_BROWN
        
        # Multiple eyes
        canvas[8][14] = RED
        canvas[8][15] = RED
        canvas[8][16] = RED
        canvas[8][17] = RED
        
        # Fangs
        canvas[10][15] = WHITE
        canvas[10][16] = WHITE
        
        # Legs (thicker)
        # Left side
        for x in range(4, 10):
            canvas[12][x] = SPIDER_BROWN
            canvas[16][x] = SPIDER_BROWN
            canvas[20][x] = SPIDER_BROWN
        
        # Right side  
        for x in range(22, 28):
            canvas[12][x] = SPIDER_BROWN
            canvas[16][x] = SPIDER_BROWN
            canvas[20][x] = SPIDER_BROWN
        
        # Markings
        canvas[14][16] = RED
        canvas[16][16] = RED
        canvas[18][16] = RED
    
    elif monster_lower == 'tiger':
        # Orange tiger with black stripes
        TIGER_ORANGE = [255, 140, 0, 255]
        
        # Head
        for y in range(6, 14):
            for x in range(12, 20):
                canvas[y][x] = TIGER_ORANGE
        
        # Ears
        canvas[6][13] = TIGER_ORANGE
        canvas[6][18] = TIGER_ORANGE
        canvas[5][13] = BLACK  # Ear interior
        canvas[5][18] = BLACK
        
        # Eyes
        canvas[9][14] = YELLOW
        canvas[9][17] = YELLOW
        canvas[9][14] = BLACK  # Pupils
        canvas[9][17] = BLACK
        
        # Nose
        canvas[11][15] = PINK
        canvas[11][16] = PINK
        
        # Whiskers
        canvas[12][11] = BLACK
        canvas[12][20] = BLACK
        
        # Body
        for y in range(14, 26):
            for x in range(10, 22):
                canvas[y][x] = TIGER_ORANGE
        
        # Tiger stripes
        for y in range(8, 24):
            if y % 3 == 0:
                canvas[y][13] = BLACK
                canvas[y][16] = BLACK
                canvas[y][19] = BLACK
        
        # Tail
        for y in range(18, 22):
            canvas[y][5] = TIGER_ORANGE
        canvas[20][5] = BLACK  # Stripe on tail
        
        # Legs
        for y in range(26, 30):
            canvas[y][12] = TIGER_ORANGE
            canvas[y][15] = TIGER_ORANGE
            canvas[y][17] = TIGER_ORANGE
            canvas[y][20] = TIGER_ORANGE
    
    elif monster_lower == 'vampire':
        # Pale vampire with cape
        PALE = [245, 245, 220, 255]
        CAPE = [139, 0, 0, 255]  # Dark red cape
        
        # Pale head
        for y in range(6, 14):
            for x in range(12, 20):
                canvas[y][x] = PALE
        
        # Dark hair (slicked back)
        for y in range(4, 8):
            for x in range(12, 20):
                canvas[y][x] = BLACK
        
        # Eyes (red)
        canvas[9][14] = RED
        canvas[9][17] = RED
        
        # Fangs
        canvas[12][14] = WHITE
        canvas[12][17] = WHITE
        
        # Cape/cloak
        for y in range(14, 28):
            for x in range(8, 24):
                canvas[y][x] = CAPE
        
        # Cape collar (high)
        for y in range(12, 16):
            canvas[y][10] = CAPE
            canvas[y][21] = CAPE
        
        # Pale hands
        canvas[18][7] = PALE
        canvas[18][24] = PALE
        
        # Cape interior (black)
        for y in range(16, 26):
            for x in range(14, 18):
                canvas[y][x] = BLACK
    
    elif monster_lower == 'wyvern':
        # Dragon-like creature with wings
        DRAGON_GREEN = [34, 139, 34, 255]
        
        # Head
        for y in range(6, 12):
            for x in range(14, 20):
                canvas[y][x] = DRAGON_GREEN
        
        # Horns
        canvas[4][15] = BLACK
        canvas[4][18] = BLACK
        canvas[5][15] = BLACK
        canvas[5][18] = BLACK
        
        # Eyes (fierce)
        canvas[8][15] = RED
        canvas[8][18] = RED
        
        # Nostrils
        canvas[10][16] = BLACK
        canvas[10][17] = BLACK
        
        # Body
        for y in range(12, 22):
            for x in range(12, 20):
                canvas[y][x] = DRAGON_GREEN
        
        # Wings (spread)
        for y in range(8, 16):
            for x in range(4, 12):
                canvas[y][x] = GRAY  # Left wing
            for x in range(20, 28):
                canvas[y][x] = GRAY  # Right wing
        
        # Wing membrane
        canvas[10][6] = DARK_GRAY
        canvas[12][8] = DARK_GRAY
        canvas[10][25] = DARK_GRAY
        canvas[12][23] = DARK_GRAY
        
        # Tail (long with spikes)
        for y in range(22, 28):
            canvas[y][16] = DRAGON_GREEN
        # Tail spikes
        canvas[24][15] = BLACK
        canvas[26][17] = BLACK
        
        # Claws
        canvas[20][11] = BLACK
        canvas[20][20] = BLACK
    
    # Convert to PIL Image and save
    img = Image.fromarray(canvas.astype(np.uint8), 'RGBA')
    
    # Scale up 8x for visibility (like magician art)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    output_path = f'{monster_name.lower()}_monster.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    
    return canvas

def create_all_monsters():
    """Create pixel art for all monsters in the monsters directory"""
    monsters = [
        'Bunny', 'Caveman', 'Cyclops', 'Demon', 'Flytrap', 'Hydra', 'Lich', 'Lola', 
        'Maddog', 'ManBearPig', 'Manticore', 'Ninja', 'Slime', 'Snake', 
        'Spider', 'Spider2', 'Tiger', 'Vampire', 'Wyvern'
    ]
    
    print("🎨 Creating pixel art for all monsters...")
    print("=" * 50)
    
    for monster in monsters:
        create_monster_art(monster)
    
    print("=" * 50)
    print(f"🎉 Successfully created {len(monsters)} monster pixel art files!")
    print("   Size: 256x256 pixels each")
    print("   Style: Minecraft-style pixel art matching magician art")
    print("   Format: PNG with transparency")

if __name__ == '__main__':
    create_all_monsters()