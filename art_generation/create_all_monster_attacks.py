#!/usr/bin/env python3
"""
Monster Attack Animation Generator - Creates attack versions for all monsters
Creates 32x32 pixel art attack animations for each monster with dynamic effects
Based on the monster list from create_all_monsters.py
"""

import numpy as np
from PIL import Image
import os

def create_monster_attack_art(monster_name):
    """Create attack animation pixel art for a specific monster"""
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
    
    # Attack effect colors
    ATTACK_RED = [255, 100, 100, 200]      # Semi-transparent red glow
    ATTACK_ORANGE = [255, 165, 0, 180]     # Orange energy
    ATTACK_YELLOW = [255, 255, 100, 160]   # Yellow sparks
    MOTION_BLUR = [150, 150, 255, 100]     # Blue motion trail
    
    monster_lower = monster_name.lower()
    
    if monster_lower == 'bunny':
        # Aggressive bunny - lunging forward with claws out
        # Head (tilted forward aggressively)
        for y in range(6, 14):
            for x in range(10, 18):
                if (x-14)**2 + (y-10)**2 <= 16:
                    canvas[y][x] = WHITE
        
        # Angry ears (flattened back)
        for y in range(3, 7):
            canvas[y][11] = WHITE
            canvas[y][16] = WHITE
        canvas[4][11] = PINK
        canvas[4][16] = PINK
        
        # Angry red eyes
        canvas[8][12] = RED
        canvas[8][15] = RED
        
        # Snarling mouth
        canvas[10][13] = BLACK
        canvas[10][14] = BLACK
        
        # Body (leaning forward)
        for y in range(14, 22):
            for x in range(9, 19):
                if (x-14)**2/25 + (y-18)**2/12 <= 1:
                    canvas[y][x] = WHITE
        
        # Attacking claws (extended)
        canvas[16][8] = BLACK  # Left claw
        canvas[17][7] = BLACK
        canvas[16][19] = BLACK  # Right claw
        canvas[17][20] = BLACK
        
        # Motion lines behind bunny
        for i in range(3):
            canvas[12+i][4+i] = MOTION_BLUR
            canvas[16+i][3+i] = MOTION_BLUR
        
        # Attack sparks around claws
        canvas[15][6] = ATTACK_YELLOW
        canvas[17][5] = ATTACK_YELLOW
        canvas[15][21] = ATTACK_YELLOW
        canvas[17][22] = ATTACK_YELLOW
    
    elif monster_lower == 'caveman':
        # Caveman swinging club with rage
        SKIN = [222, 184, 135, 255]
        HIDE = [101, 67, 33, 255]
        
        # Head (tilted in attack)
        for y in range(4, 12):
            for x in range(10, 18):
                canvas[y][x] = SKIN
        
        # Wild attacking hair
        for y in range(2, 6):
            for x in range(9, 19):
                canvas[y][x] = DARK_BROWN
        
        # Furious eyes
        canvas[7][12] = RED
        canvas[7][15] = RED
        
        # Shouting mouth
        canvas[9][13] = BLACK
        canvas[9][14] = BLACK
        canvas[9][15] = BLACK
        
        # Body in attacking pose
        for y in range(12, 24):
            for x in range(8, 20):
                canvas[y][x] = HIDE
        
        # Club raised high (wooden weapon)
        for y in range(1, 8):
            canvas[y][20] = BROWN
            canvas[y][21] = DARK_BROWN
        
        # Club head (thick end)
        for y in range(1, 4):
            for x in range(19, 23):
                canvas[y][x] = BROWN
        
        # Motion blur around club
        for i in range(4):
            canvas[2+i][22+i] = MOTION_BLUR
        
        # Attack impact lines
        canvas[5][23] = ATTACK_YELLOW
        canvas[6][24] = ATTACK_ORANGE
        canvas[4][22] = ATTACK_RED
    
    elif monster_lower == 'cyclops':
        # Giant cyclops in mid-punch
        SKIN = [180, 140, 100, 255]
        
        # Large head
        for y in range(4, 16):
            for x in range(8, 24):
                if (x-16)**2/64 + (y-10)**2/36 <= 1:
                    canvas[y][x] = SKIN
        
        # Single large angry eye (glowing red)
        for y in range(8, 12):
            for x in range(14, 18):
                canvas[y][x] = RED
        canvas[9][15] = YELLOW  # Eye center
        canvas[10][16] = WHITE  # Eye glint
        
        # Frowning mouth
        for x in range(13, 19):
            canvas[13][x] = BLACK
        
        # Massive body
        for y in range(16, 30):
            for x in range(6, 26):
                if (x-16)**2/100 + (y-23)**2/49 <= 1:
                    canvas[y][x] = SKIN
        
        # Huge attacking fist (coming forward)
        for y in range(14, 20):
            for x in range(20, 28):
                canvas[y][x] = SKIN
        
        # Knuckles
        canvas[15][22] = DARK_BROWN
        canvas[15][24] = DARK_BROWN
        canvas[15][26] = DARK_BROWN
        canvas[17][22] = DARK_BROWN
        canvas[17][24] = DARK_BROWN
        canvas[17][26] = DARK_BROWN
        
        # Impact effects around fist
        for i in range(3):  # Reduced to stay within bounds
            if 28+i < 32:
                canvas[16][28+i] = ATTACK_ORANGE
            if 29+i < 32:
                canvas[17][29+i] = ATTACK_RED
        
        # Motion blur behind fist
        for i in range(3):
            canvas[15+i][18-i] = MOTION_BLUR
    
    elif monster_lower == 'demon':
        # Demon in hellfire attack pose - claws extended, flames everywhere
        DARK_SKIN = [101, 67, 33, 255]
        HORN = [64, 64, 64, 255]
        FIRE_BLAST = [255, 100, 0, 200]     # Semi-transparent fire
        ENERGY_GLOW = [255, 0, 0, 180]      # Red energy
        HELLFIRE = [255, 69, 0, 220]        # Intense hellfire
        
        # Head (leaning forward in attack)
        for y in range(6, 14):
            for x in range(10, 18):
                if (x-14)**2 + (y-10)**2 <= 16:
                    canvas[y][x] = DARK_SKIN
        
        # Horns (more prominent)
        canvas[4][11] = HORN
        canvas[3][11] = HORN
        canvas[2][10] = HORN
        canvas[4][16] = HORN
        canvas[3][16] = HORN
        canvas[2][17] = HORN
        
        # Eyes (blazing with fury)
        canvas[8][12] = ATTACK_RED
        canvas[8][15] = ATTACK_RED
        canvas[9][12] = ATTACK_YELLOW
        canvas[9][15] = ATTACK_YELLOW
        
        # Snarling mouth with fangs
        canvas[11][12] = BLACK
        canvas[11][13] = BLACK
        canvas[11][14] = BLACK
        canvas[11][15] = BLACK
        canvas[12][12] = WHITE  # Large fangs
        canvas[12][15] = WHITE
        
        # Body (crouched in attack)
        for y in range(14, 22):
            for x in range(8, 20):
                canvas[y][x] = DARK_SKIN
        
        # Arms extended forward (attacking)
        for y in range(16, 20):
            for x in range(4, 8):
                canvas[y][x] = DARK_SKIN  # Left arm
            for x in range(20, 24):
                canvas[y][x] = DARK_SKIN  # Right arm
        
        # Massive claws (enlarged for attack)
        canvas[18][2] = GRAY
        canvas[19][2] = GRAY
        canvas[18][3] = GRAY
        canvas[18][28] = GRAY
        canvas[19][28] = GRAY
        canvas[18][29] = GRAY
        
        # HELLFIRE ATTACK EFFECTS!
        # Fire breath from mouth
        for x in range(16, 24):
            canvas[11][x] = ATTACK_YELLOW
            canvas[12][x] = ATTACK_ORANGE
            canvas[13][x] = ATTACK_RED
        
        # Intense flame aura
        canvas[10][6] = ATTACK_YELLOW
        canvas[12][5] = ATTACK_ORANGE
        canvas[14][4] = FIRE_BLAST
        canvas[10][21] = ATTACK_YELLOW  
        canvas[12][22] = ATTACK_ORANGE
        canvas[14][23] = FIRE_BLAST
        
        # Energy from claws
        canvas[17][1] = ENERGY_GLOW
        canvas[18][0] = HELLFIRE
        canvas[17][30] = ENERGY_GLOW
        canvas[18][31] = HELLFIRE
        
        # Ground fire effects
        canvas[30][12] = ATTACK_RED
        canvas[30][16] = ATTACK_RED
    
    elif monster_lower == 'flytrap':
        # Venus flytrap snapping shut aggressively
        PLANT_GREEN = [34, 139, 34, 255]
        
        # Stem (thick and menacing)
        for y in range(20, 30):
            for x in range(14, 18):
                canvas[y][x] = PLANT_GREEN
        
        # Large attacking mouth (wide open then snapping)
        # Upper jaw
        for y in range(8, 14):
            for x in range(8, 24):
                if y < 11:
                    canvas[y][x] = PLANT_GREEN
        
        # Lower jaw 
        for y in range(14, 20):
            for x in range(8, 24):
                if y > 17:
                    canvas[y][x] = PLANT_GREEN
        
        # Sharp teeth (menacing)
        for x in range(10, 22, 2):
            canvas[13][x] = WHITE  # Upper teeth
            canvas[14][x] = WHITE  # Lower teeth
        
        # Red interior mouth
        for y in range(11, 17):
            for x in range(10, 22):
                if y > 12 and y < 16:
                    canvas[y][x] = DARK_RED
        
        # Motion lines showing snapping action
        for i in range(4):
            canvas[12][6+i] = MOTION_BLUR
            canvas[16][6+i] = MOTION_BLUR
            canvas[12][24+i] = MOTION_BLUR
            canvas[16][24+i] = MOTION_BLUR
        
        # Attack particles around mouth
        canvas[10][7] = ATTACK_RED
        canvas[18][7] = ATTACK_RED
        canvas[10][25] = ATTACK_RED
        canvas[18][25] = ATTACK_RED
    
    elif monster_lower == 'hydra':
        # Multi-headed dragon breathing fire
        DRAGON_GREEN = [0, 100, 0, 255]
        
        # Main body
        for y in range(20, 30):
            for x in range(10, 22):
                canvas[y][x] = DRAGON_GREEN
        
        # Three attacking heads
        # Left head
        for y in range(6, 12):
            for x in range(4, 10):
                canvas[y][x] = DRAGON_GREEN
        canvas[8][6] = RED  # Eye
        canvas[9][2] = ORANGE  # Fire breath
        canvas[9][3] = RED
        canvas[10][1] = YELLOW
        
        # Center head (main)
        for y in range(4, 14):
            for x in range(12, 20):
                if (x-16)**2/16 + (y-9)**2/25 <= 1:
                    canvas[y][x] = DRAGON_GREEN
        canvas[7][15] = RED  # Eye
        canvas[8][14] = RED
        
        # Right head
        for y in range(8, 14):
            for x in range(22, 28):
                canvas[y][x] = DRAGON_GREEN
        canvas[10][24] = RED  # Eye
        canvas[11][28] = ORANGE  # Fire breath
        canvas[11][29] = RED
        canvas[12][30] = YELLOW
        
        # Fire breath from center head
        for x in range(8, 12):  # Reduced range to avoid overlap
            canvas[9][x] = ORANGE
            canvas[10][x] = RED
            canvas[11][x] = YELLOW
        
        # Heat distortion effects
        for i in range(6):
            canvas[8+i][6+i] = ATTACK_ORANGE
    
    elif monster_lower == 'lich':
        # Undead lich casting dark magic
        BONE = [240, 230, 140, 255]
        
        # Skeletal head
        for y in range(4, 12):
            for x in range(12, 20):
                canvas[y][x] = BONE
        
        # Glowing evil eyes
        canvas[7][14] = PURPLE
        canvas[7][17] = PURPLE
        
        # Dark robe
        for y in range(12, 28):
            for x in range(8, 24):
                if (x-16)**2/64 + (y-20)**2/64 <= 1:
                    canvas[y][x] = DARK_PURPLE
        
        # Skeletal hand casting spell
        for y in range(10, 16):
            for x in range(20, 26):
                canvas[y][x] = BONE
        
        # Dark magic orb
        for y in range(8, 12):
            for x in range(24, 28):
                canvas[y][x] = PURPLE
        
        # Magic sparks
        canvas[6][26] = CYAN
        canvas[12][27] = PURPLE
        canvas[8][29] = DARK_PURPLE
        
        # Dark energy swirls
        for i in range(4):
            canvas[9+i][22-i] = [75, 0, 130, 150]  # Indigo trail
    
    elif monster_lower == 'lola':
        # Lola in fierce attack mode (assuming humanoid)
        SKIN = [255, 220, 177, 255]
        HAIR = [255, 200, 100, 255]  # Blonde
        
        # Head (determined expression)
        for y in range(6, 14):
            for x in range(12, 20):
                canvas[y][x] = SKIN
        
        # Flowing hair (in motion)
        for y in range(4, 10):
            for x in range(8, 16):
                canvas[y][x] = HAIR
        
        # Fierce eyes
        canvas[9][14] = BLUE
        canvas[9][17] = BLUE
        
        # Determined mouth
        canvas[11][15] = RED
        canvas[11][16] = RED
        
        # Body in fighting stance
        for y in range(14, 26):
            for x in range(10, 22):
                canvas[y][x] = PINK  # Pink outfit
        
        # Attacking with weapon (sword or staff)
        for y in range(2, 14):
            canvas[y][22] = GRAY  # Weapon shaft
        
        # Weapon tip
        for y in range(2, 6):
            canvas[y][21] = WHITE  # Blade
            canvas[y][23] = WHITE
        
        # Speed lines
        for i in range(4):
            canvas[8+i][24+i] = MOTION_BLUR
        
        # Attack sparkles
        canvas[4][20] = ATTACK_YELLOW
        canvas[6][24] = ATTACK_YELLOW
    
    elif monster_lower == 'maddog':
        # Rabid dog lunging with foam at mouth
        DOG_BROWN = [101, 67, 33, 255]
        
        # Head (snarling, tilted forward)
        for y in range(6, 14):
            for x in range(8, 18):
                canvas[y][x] = DOG_BROWN
        
        # Ears (flattened back in aggression)
        for y in range(4, 8):
            canvas[y][10] = DOG_BROWN
            canvas[y][15] = DOG_BROWN
        
        # Angry red eyes
        canvas[8][11] = RED
        canvas[8][14] = RED
        
        # Snarling mouth with teeth
        canvas[11][12] = BLACK
        canvas[11][13] = WHITE  # Fangs
        canvas[11][14] = BLACK
        canvas[11][15] = WHITE
        
        # Foam at mouth (rabid)
        canvas[12][11] = WHITE
        canvas[12][16] = WHITE
        canvas[13][10] = WHITE
        canvas[13][17] = WHITE
        
        # Body in attacking lunge
        for y in range(14, 24):
            for x in range(6, 20):
                if (x-13)**2/49 + (y-19)**2/25 <= 1:
                    canvas[y][x] = DOG_BROWN
        
        # Legs in motion
        canvas[22][8] = DOG_BROWN   # Front legs
        canvas[23][9] = DOG_BROWN
        canvas[22][17] = DOG_BROWN
        canvas[23][18] = DOG_BROWN
        
        # Motion blur behind dog
        for i in range(5):
            canvas[16+i][2+i] = MOTION_BLUR
        
        # Rage particles
        canvas[8][6] = ATTACK_RED
        canvas[10][5] = ATTACK_RED
    
    elif monster_lower == 'manbearpig':
        # ManBearPig rampaging with claws
        BEAR_BROWN = [101, 67, 33, 255]
        PIG_PINK = [255, 192, 203, 255]
        
        # Large head (mix of features)
        for y in range(4, 14):
            for x in range(10, 22):
                canvas[y][x] = BEAR_BROWN
        
        # Pig snout
        for y in range(10, 12):
            for x in range(14, 18):
                canvas[y][x] = PIG_PINK
        
        # Bear ears
        canvas[5][12] = BEAR_BROWN
        canvas[5][19] = BEAR_BROWN
        
        # Fierce eyes
        canvas[7][13] = RED
        canvas[7][18] = RED
        
        # Massive body
        for y in range(14, 28):
            for x in range(6, 26):
                if (x-16)**2/100 + (y-21)**2/49 <= 1:
                    canvas[y][x] = BEAR_BROWN
        
        # Large attacking claws
        canvas[12][4] = BLACK   # Left claw swipe
        canvas[13][3] = BLACK
        canvas[14][2] = BLACK
        canvas[12][27] = BLACK  # Right claw
        canvas[13][28] = BLACK
        canvas[14][29] = BLACK
        
        # Claw marks in air
        for i in range(3):
            canvas[11+i][5+i] = ATTACK_YELLOW
            canvas[11+i][26-i] = ATTACK_YELLOW
        
        # Rage aura
        for i in range(8):
            if i % 2 == 0:
                canvas[6][8+i] = ATTACK_RED
                canvas[20][8+i] = ATTACK_RED
    
    elif monster_lower == 'manticore':
        # Manticore with poisonous tail strike
        LION_BROWN = [139, 69, 19, 255]
        
        # Lion head
        for y in range(6, 14):
            for x in range(10, 20):
                canvas[y][x] = LION_BROWN
        
        # Mane
        for y in range(4, 8):
            for x in range(8, 22):
                canvas[y][x] = DARK_BROWN
        
        # Predator eyes
        canvas[8][13] = YELLOW
        canvas[8][16] = YELLOW
        
        # Snarling mouth
        canvas[11][14] = WHITE  # Fangs
        canvas[11][15] = BLACK
        canvas[11][16] = WHITE
        
        # Body
        for y in range(14, 26):
            for x in range(8, 24):
                canvas[y][x] = LION_BROWN
        
        # Scorpion tail (curved over, ready to strike)
        tail_points = [(20, 26), (22, 24), (24, 22), (26, 20), (28, 18)]
        for x, y in tail_points:
            if x < 32 and y < 32:
                canvas[y][x] = DARK_BROWN
        
        # Poison stinger
        canvas[16][30] = PURPLE  # Venomous tip
        
        # Poison drip
        canvas[17][29] = PURPLE
        canvas[18][28] = DARK_PURPLE
        
        # Motion lines around tail
        for i in range(3):
            canvas[19+i][25+i] = MOTION_BLUR
    
    elif monster_lower == 'ninja':
        # Enemy ninja throwing shuriken
        NINJA_BLACK = [20, 20, 20, 255]
        
        # Head (masked)
        for y in range(6, 14):
            for x in range(12, 20):
                canvas[y][x] = NINJA_BLACK
        
        # Eyes (only part visible)
        canvas[9][14] = WHITE
        canvas[9][17] = WHITE
        canvas[9][15] = RED   # Angry red pupils
        canvas[9][16] = RED
        
        # Body in throwing stance
        for y in range(14, 26):
            for x in range(10, 22):
                canvas[y][x] = NINJA_BLACK
        
        # Throwing arm extended
        for y in range(12, 16):
            for x in range(20, 26):
                canvas[y][x] = NINJA_BLACK
        
        # Shuriken in flight
        canvas[10][28] = GRAY
        canvas[11][27] = GRAY
        canvas[11][29] = GRAY
        canvas[12][28] = GRAY
        
        # Motion trail of shuriken
        for i in range(4):
            canvas[11][24+i] = MOTION_BLUR
        
        # Speed lines around ninja
        for i in range(3):
            canvas[16+i][8-i] = MOTION_BLUR
            canvas[20-i][8-i] = MOTION_BLUR
    
    elif monster_lower == 'slime':
        # Acidic slime erupting upward
        SLIME_GREEN = [50, 205, 50, 255]
        
        # Main slime body (bubbling)
        for y in range(16, 28):
            for x in range(8, 24):
                if (x-16)**2/64 + (y-22)**2/36 <= 1:
                    canvas[y][x] = SLIME_GREEN
        
        # Bubbles rising (attack pattern)
        canvas[14][12] = SLIME_GREEN
        canvas[12][15] = SLIME_GREEN
        canvas[10][18] = SLIME_GREEN
        canvas[8][21] = SLIME_GREEN
        canvas[6][16] = SLIME_GREEN
        
        # Acidic spray
        for y in range(4, 10):
            for x in range(14, 20):
                if (y + x) % 3 == 0:
                    canvas[y][x] = SLIME_GREEN
        
        # Acid droplets
        canvas[4][13] = DARK_GREEN
        canvas[6][19] = DARK_GREEN
        canvas[8][11] = DARK_GREEN
        canvas[5][22] = DARK_GREEN
        
        # Corrosive effect lines
        for i in range(6):
            canvas[12+i][6+i] = ATTACK_YELLOW
            canvas[12+i][26-i] = ATTACK_YELLOW
    
    elif monster_lower == 'snake':
        # Cobra striking with fangs
        SNAKE_GREEN = [0, 128, 0, 255]
        
        # Coiled body
        for angle in range(0, 360, 20):
            x = int(16 + 8 * np.cos(np.radians(angle)))
            y = int(20 + 4 * np.sin(np.radians(angle)))
            if 0 <= x < 32 and 0 <= y < 32:
                canvas[y][x] = SNAKE_GREEN
        
        # Head striking forward
        for y in range(6, 12):
            for x in range(16, 26):
                canvas[y][x] = SNAKE_GREEN
        
        # Fangs extended
        canvas[9][24] = WHITE
        canvas[10][24] = WHITE
        canvas[9][25] = WHITE
        canvas[10][25] = WHITE
        
        # Forked tongue
        canvas[8][26] = RED
        canvas[7][27] = RED
        canvas[9][27] = RED
        
        # Venom drip
        canvas[11][25] = DARK_GREEN
        canvas[12][25] = YELLOW
        
        # Strike motion blur
        for i in range(4):
            canvas[8+i][12+i] = MOTION_BLUR
        
        # Hood pattern (cobra)
        canvas[7][18] = BLACK
        canvas[7][22] = BLACK
        canvas[8][17] = BLACK
        canvas[8][23] = BLACK
    
    elif monster_lower == 'spider':
        # Spider leaping with legs extended
        SPIDER_BLACK = [20, 20, 20, 255]
        
        # Body (thorax and abdomen)
        for y in range(12, 20):
            for x in range(14, 18):
                canvas[y][x] = SPIDER_BLACK
        
        # Eight legs in attack position
        # Front legs (extended forward)
        canvas[10][12] = SPIDER_BLACK
        canvas[9][11] = SPIDER_BLACK
        canvas[10][19] = SPIDER_BLACK
        canvas[9][20] = SPIDER_BLACK
        
        # Middle legs (spread wide)
        canvas[14][8] = SPIDER_BLACK
        canvas[15][7] = SPIDER_BLACK
        canvas[14][23] = SPIDER_BLACK
        canvas[15][24] = SPIDER_BLACK
        
        # Back legs (pushing off)
        canvas[18][10] = SPIDER_BLACK
        canvas[19][9] = SPIDER_BLACK
        canvas[18][21] = SPIDER_BLACK
        canvas[19][22] = SPIDER_BLACK
        
        # Pedipalps (feeding appendages)
        canvas[11][13] = SPIDER_BLACK
        canvas[11][18] = SPIDER_BLACK
        
        # Multiple eyes reflecting light
        canvas[13][15] = RED
        canvas[13][16] = RED
        canvas[14][15] = RED
        canvas[14][16] = RED
        
        # Web strands being shot
        for i in range(6):
            canvas[8][15+i] = WHITE
            canvas[22][10+i] = WHITE
        
        # Motion blur from leap
        for i in range(3):
            canvas[16+i][12-i] = MOTION_BLUR
    
    elif monster_lower == 'spider2':
        # Larger, more aggressive spider variant
        SPIDER_RED = [139, 0, 0, 255]
        
        # Larger body
        for y in range(10, 22):
            for x in range(12, 20):
                canvas[y][x] = SPIDER_RED
        
        # Massive legs (more threatening)
        # Front legs reaching forward
        for i in range(4):
            canvas[8][14+i] = SPIDER_RED
            canvas[6][12+i] = SPIDER_RED
        
        # Side legs
        canvas[12][6] = SPIDER_RED
        canvas[14][4] = SPIDER_RED
        canvas[16][3] = SPIDER_RED
        canvas[12][25] = SPIDER_RED
        canvas[14][27] = SPIDER_RED
        canvas[16][28] = SPIDER_RED
        
        # Back legs
        canvas[20][8] = SPIDER_RED
        canvas[22][6] = SPIDER_RED
        canvas[20][23] = SPIDER_RED
        canvas[22][25] = SPIDER_RED
        
        # Large fangs dripping venom
        canvas[12][11] = WHITE
        canvas[13][10] = WHITE
        canvas[12][20] = WHITE
        canvas[13][21] = WHITE
        
        # Venom drops
        canvas[14][9] = DARK_GREEN
        canvas[15][8] = YELLOW
        canvas[14][22] = DARK_GREEN
        canvas[15][23] = YELLOW
        
        # Aggressive posture effects
        for i in range(5):
            canvas[6+i][8+i] = ATTACK_RED
            canvas[6+i][23-i] = ATTACK_RED
    
    elif monster_lower == 'tiger':
        # Tiger pouncing with claws extended
        TIGER_ORANGE = [255, 140, 0, 255]
        
        # Head in attack position
        for y in range(6, 14):
            for x in range(10, 20):
                canvas[y][x] = TIGER_ORANGE
        
        # Black stripes on head
        canvas[7][12] = BLACK
        canvas[9][13] = BLACK
        canvas[7][17] = BLACK
        canvas[9][16] = BLACK
        
        # Fierce eyes
        canvas[8][13] = YELLOW
        canvas[8][16] = YELLOW
        
        # Snarling mouth with fangs
        canvas[11][14] = WHITE
        canvas[11][15] = BLACK
        canvas[11][16] = WHITE
        
        # Body in pouncing position
        for y in range(14, 26):
            for x in range(8, 24):
                if (x-16)**2/64 + (y-20)**2/36 <= 1:
                    canvas[y][x] = TIGER_ORANGE
        
        # Tiger stripes on body
        for y in range(16, 24, 2):
            canvas[y][10] = BLACK
            canvas[y][14] = BLACK
            canvas[y][18] = BLACK
            canvas[y][22] = BLACK
        
        # Extended claws
        canvas[12][6] = BLACK   # Left front paw
        canvas[13][5] = BLACK
        canvas[14][4] = BLACK
        canvas[12][25] = BLACK  # Right front paw
        canvas[13][26] = BLACK
        canvas[14][27] = BLACK
        
        # Motion blur from pounce
        for i in range(4):
            canvas[18+i][4+i] = MOTION_BLUR
        
        # Attack intensity lines
        canvas[8][8] = ATTACK_ORANGE
        canvas[10][7] = ATTACK_YELLOW
        canvas[8][23] = ATTACK_ORANGE
        canvas[10][24] = ATTACK_YELLOW
    
    elif monster_lower == 'vampire':
        # Vampire lunging with fangs bared
        PALE_SKIN = [255, 245, 238, 255]
        
        # Pale head
        for y in range(6, 14):
            for x in range(12, 20):
                canvas[y][x] = PALE_SKIN
        
        # Dark hair slicked back
        for y in range(4, 8):
            for x in range(11, 21):
                canvas[y][x] = BLACK
        
        # Glowing red eyes
        canvas[8][14] = RED
        canvas[8][17] = RED
        canvas[9][14] = DARK_RED  # Pupils
        canvas[9][17] = DARK_RED
        
        # Fangs extended
        canvas[10][14] = WHITE
        canvas[11][14] = WHITE
        canvas[10][17] = WHITE
        canvas[11][17] = WHITE
        
        # Blood on fangs
        canvas[12][14] = DARK_RED
        canvas[12][17] = DARK_RED
        
        # Black cape/coat
        for y in range(14, 28):
            for x in range(8, 24):
                if (x-16)**2/64 + (y-21)**2/49 <= 1:
                    canvas[y][x] = BLACK
        
        # Cape flowing in attack motion
        for y in range(16, 24):
            canvas[y][6] = BLACK
            canvas[y][7] = BLACK
        
        # Clawed hands reaching
        canvas[14][22] = PALE_SKIN
        canvas[15][23] = PALE_SKIN
        canvas[16][24] = PALE_SKIN
        
        # Sharp claws
        canvas[13][22] = BLACK
        canvas[14][25] = BLACK
        canvas[15][26] = BLACK
        
        # Dark aura effects
        for i in range(6):
            canvas[10+i][6] = [50, 0, 50, 150]  # Purple shadow
            canvas[10+i][25] = [50, 0, 50, 150]
    
    elif monster_lower == 'wyvern':
        # Dragon wyvern diving with fire breath
        DRAGON_DARK = [0, 100, 0, 255]
        
        # Dragon head angled down (diving)
        for y in range(8, 16):
            for x in range(12, 22):
                canvas[y][x] = DRAGON_DARK
        
        # Horns
        canvas[7][14] = GRAY
        canvas[6][15] = GRAY
        canvas[7][19] = GRAY
        canvas[6][18] = GRAY
        
        # Fierce dragon eye
        canvas[10][15] = YELLOW
        canvas[11][16] = RED
        
        # Fire breath streaming down
        for y in range(16, 26):
            for x in range(14, 20):
                if (x + y) % 2 == 0:
                    canvas[y][x] = ORANGE
                else:
                    canvas[y][x] = RED
        
        # Fire expanding at bottom
        for x in range(10, 24):
            canvas[26][x] = YELLOW
            canvas[27][x] = ORANGE
        
        # Wings spread (partial view)
        for y in range(10, 18):
            canvas[y][8] = DARK_GREEN    # Left wing
            canvas[y][9] = GREEN
            canvas[y][23] = DARK_GREEN   # Right wing
            canvas[y][24] = GREEN
        
        # Motion blur from dive
        for i in range(4):
            canvas[4+i][16+i] = MOTION_BLUR
            canvas[4+i][16-i] = MOTION_BLUR
        
        # Heat distortion from fire
        for i in range(8):
            canvas[20+i][12+i] = ATTACK_ORANGE
    
    else:
        # Default: Create a generic "attacking" version with red glow
        # Simple angry face with attack effects
        for y in range(10, 22):
            for x in range(10, 22):
                canvas[y][x] = RED
        
        # Angry eyes
        canvas[14][13] = BLACK
        canvas[14][18] = BLACK
        
        # Attacking mouth
        canvas[17][15] = BLACK
        canvas[17][16] = BLACK
        
        # Generic attack effects
        for i in range(4):
            canvas[12][8+i] = ATTACK_YELLOW
            canvas[12][20+i] = ATTACK_YELLOW
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up for better visibility (8x scaling = 256x256 final size)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save to art directory
    output_path = f'../art/{monster_name.lower()}_attack.png'
    
    # Create art directory if it doesn't exist
    os.makedirs('../art', exist_ok=True)
    
    img_scaled.save(output_path, 'PNG')
    print(f"⚔️ Created {output_path}")
    
    return canvas

def create_all_monster_attacks():
    """Create attack animations for all monsters"""
    monsters = [
        'Bunny', 'Caveman', 'Cyclops', 'Demon', 'Flytrap', 'Hydra', 'Lich', 'Lola', 
        'Maddog', 'ManBearPig', 'Manticore', 'Ninja', 'Slime', 'Snake', 
        'Spider', 'Spider2', 'Tiger', 'Vampire', 'Wyvern'
    ]
    
    print("⚔️ Creating attack animations for all monsters...")
    print("=" * 60)
    
    for monster in monsters:
        create_monster_attack_art(monster)
    
    print("=" * 60)
    print(f"🎉 Successfully created {len(monsters)} monster attack animations!")
    print("   Size: 256x256 pixels each")
    print("   Style: Dynamic attack poses with motion effects")
    print("   Location: ../art/[monster]_attack.png")
    print("   Features: Motion blur, attack effects, aggressive poses")

if __name__ == '__main__':
    create_all_monster_attacks()