#!/usr/bin/env python3
"""
Create pixel art Shiva in the mountains background PNG
Inspired by the Bangalore Shiva statue
"""
from PIL import Image
import numpy as np
import random

def create_shiva_mountains_background():
    """Create a pixel art scene of Shiva meditating in the Himalayas - Shiva takes up most of the image"""
    # Create a pixel art canvas (same dimensions as other biomes)
    width = 64
    height = 32
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette inspired by Himalayan mountains and Shiva
    # Sky colors - sacred mountain sky
    SKY_BLUE = [135, 206, 250, 255]      # Bright sky blue
    SKY_LIGHT = [176, 224, 230, 255]     # Lighter blue
    SKY_GRADIENT = [100, 149, 237, 255]  # Cornflower blue for depth
    
    # Mountain colors - snow-capped Himalayas
    MOUNTAIN_DARK = [70, 80, 90, 255]    # Dark rocky base
    MOUNTAIN_MID = [100, 110, 120, 255]  # Mid-tone rock
    MOUNTAIN_LIGHT = [130, 140, 150, 255] # Light rock
    SNOW_WHITE = [255, 255, 255, 255]    # Snow caps
    SNOW_SHADOW = [230, 240, 250, 255]   # Snow shadows
    ICE_BLUE = [200, 220, 240, 255]      # Icy highlights
    
    # Shiva colors - divine blue skin and sacred elements
    SHIVA_BLUE = [65, 105, 225, 255]     # Lord Shiva's blue skin
    SHIVA_DARK_BLUE = [40, 60, 140, 255] # Darker blue for shadows
    SHIVA_LIGHT_BLUE = [100, 149, 237, 255] # Lighter blue highlights
    
    # Clothing and ornaments
    ORANGE_CLOTH = [255, 140, 0, 255]    # Saffron cloth/dhoti
    ORANGE_DARK = [205, 110, 0, 255]     # Dark orange shading
    GOLD = [255, 215, 0, 255]            # Golden ornaments
    GOLD_DARK = [218, 165, 32, 255]      # Gold shading
    
    # Hair and ash
    BLACK_HAIR = [30, 30, 30, 255]       # Matted hair
    BROWN_HAIR = [60, 40, 20, 255]       # Hair highlights
    ASH_GRAY = [192, 192, 192, 255]      # Sacred ash
    
    # Sacred elements
    THIRD_EYE_RED = [220, 20, 60, 255]   # Third eye
    CRESCENT_WHITE = [245, 245, 220, 255] # Moon crescent
    GANGA_BLUE = [70, 130, 180, 255]     # River Ganga in hair
    
    # Meditation platform
    STONE_GRAY = [105, 105, 105, 255]    # Stone platform
    STONE_LIGHT = [169, 169, 169, 255]   # Light stone
    
    # Draw gradient sky (peaceful mountain sky) - minimal sky since Shiva fills image
    for y in range(6):
        if y < 2:
            canvas[y, :] = SKY_LIGHT
        elif y < 4:
            canvas[y, :] = SKY_BLUE
        else:
            canvas[y, :] = SKY_GRADIENT
    
    # Draw simple mountain silhouettes in background (minimal - just to frame Shiva)
    # Left mountain edge
    for x in range(10):
        peak_height = int(3 + 2 * abs(np.sin(x * 0.4)))
        for y in range(6 - peak_height, 10):
            canvas[y, x] = MOUNTAIN_DARK
        if peak_height > 4:
            canvas[6 - peak_height, x] = SNOW_WHITE
    
    # Right mountain edge
    for x in range(54, 64):
        peak_height = int(3 + 2 * abs(np.sin((x - 54) * 0.4)))
        for y in range(6 - peak_height, 10):
            canvas[y, x] = MOUNTAIN_DARK
        if peak_height > 4:
            canvas[6 - peak_height, x] = SNOW_WHITE
    
    # Draw Lord Shiva - MUCH LARGER, taking up most of the image
    shiva_center_x = 32
    shiva_base_y = 28  # Moved down so head reaches near top
    
    # Legs (lotus position - crossed legs) - wider and more detailed
    for x in range(shiva_center_x - 7, shiva_center_x + 8):
        canvas[shiva_base_y, x] = ORANGE_CLOTH
        canvas[shiva_base_y + 1, x] = ORANGE_CLOTH
    # Left leg fold
    for x in range(shiva_center_x - 7, shiva_center_x - 2):
        canvas[shiva_base_y - 1, x] = SHIVA_BLUE
    # Right leg fold
    for x in range(shiva_center_x + 3, shiva_center_x + 8):
        canvas[shiva_base_y - 1, x] = SHIVA_BLUE
    # Feet visible
    canvas[shiva_base_y - 1, shiva_center_x - 8] = SHIVA_BLUE
    canvas[shiva_base_y, shiva_center_x - 8] = SHIVA_BLUE
    canvas[shiva_base_y - 1, shiva_center_x + 8] = SHIVA_BLUE
    canvas[shiva_base_y, shiva_center_x + 8] = SHIVA_BLUE
    
    # Torso (blue body) - much taller and wider
    for y in range(shiva_base_y - 10, shiva_base_y):
        for x in range(shiva_center_x - 5, shiva_center_x + 6):
            canvas[y, x] = SHIVA_BLUE
    
    # Muscular definition on torso
    canvas[shiva_base_y - 8, shiva_center_x - 3] = SHIVA_DARK_BLUE
    canvas[shiva_base_y - 8, shiva_center_x + 3] = SHIVA_DARK_BLUE
    canvas[shiva_base_y - 6, shiva_center_x - 2] = SHIVA_DARK_BLUE
    canvas[shiva_base_y - 6, shiva_center_x + 2] = SHIVA_DARK_BLUE
    
    # Arms in meditation pose - larger
    # Left arm
    for y in range(shiva_base_y - 7, shiva_base_y - 2):
        canvas[y, shiva_center_x - 6] = SHIVA_BLUE
        canvas[y, shiva_center_x - 7] = SHIVA_BLUE
    # Right arm  
    for y in range(shiva_base_y - 7, shiva_base_y - 2):
        canvas[y, shiva_center_x + 6] = SHIVA_BLUE
        canvas[y, shiva_center_x + 7] = SHIVA_BLUE
    # Hands in lap (mudra) - larger
    for x in range(shiva_center_x - 4, shiva_center_x + 5):
        canvas[shiva_base_y - 2, x] = SHIVA_LIGHT_BLUE
        canvas[shiva_base_y - 3, x] = SHIVA_LIGHT_BLUE
    
    # Golden ornaments on body - more elaborate
    # Necklace/chest ornament
    for x in range(shiva_center_x - 3, shiva_center_x + 4):
        canvas[shiva_base_y - 9, x] = GOLD
    canvas[shiva_base_y - 8, shiva_center_x] = GOLD
    canvas[shiva_base_y - 7, shiva_center_x] = GOLD
    # Arm bands
    canvas[shiva_base_y - 6, shiva_center_x - 6] = GOLD
    canvas[shiva_base_y - 6, shiva_center_x + 6] = GOLD
    canvas[shiva_base_y - 5, shiva_center_x - 6] = GOLD
    canvas[shiva_base_y - 5, shiva_center_x + 6] = GOLD
    
    # Shoulders
    canvas[shiva_base_y - 10, shiva_center_x - 4] = SHIVA_LIGHT_BLUE
    canvas[shiva_base_y - 10, shiva_center_x + 4] = SHIVA_LIGHT_BLUE
    
    # Neck
    for x in range(shiva_center_x - 2, shiva_center_x + 3):
        canvas[shiva_base_y - 11, x] = SHIVA_BLUE
    canvas[shiva_base_y - 12, shiva_center_x - 1] = SHIVA_BLUE
    canvas[shiva_base_y - 12, shiva_center_x] = SHIVA_BLUE
    canvas[shiva_base_y - 12, shiva_center_x + 1] = SHIVA_BLUE
    
    # Head (much larger)
    for y in range(shiva_base_y - 16, shiva_base_y - 12):
        for x in range(shiva_center_x - 4, shiva_center_x + 5):
            canvas[y, x] = SHIVA_BLUE
    # Round out the head
    canvas[shiva_base_y - 16, shiva_center_x - 3] = SHIVA_BLUE
    canvas[shiva_base_y - 16, shiva_center_x + 3] = SHIVA_BLUE
    canvas[shiva_base_y - 15, shiva_center_x - 5] = SHIVA_BLUE
    canvas[shiva_base_y - 15, shiva_center_x + 5] = SHIVA_BLUE
    canvas[shiva_base_y - 14, shiva_center_x - 5] = SHIVA_BLUE
    canvas[shiva_base_y - 14, shiva_center_x + 5] = SHIVA_BLUE
    canvas[shiva_base_y - 13, shiva_center_x - 5] = SHIVA_BLUE
    canvas[shiva_base_y - 13, shiva_center_x + 5] = SHIVA_BLUE
    
    # Facial features
    # Eyes (closed in meditation)
    canvas[shiva_base_y - 14, shiva_center_x - 2] = BLACK_HAIR
    canvas[shiva_base_y - 14, shiva_center_x - 3] = BLACK_HAIR
    canvas[shiva_base_y - 14, shiva_center_x + 2] = BLACK_HAIR
    canvas[shiva_base_y - 14, shiva_center_x + 3] = BLACK_HAIR
    
    # Third eye (red dot on forehead) - larger
    canvas[shiva_base_y - 15, shiva_center_x] = THIRD_EYE_RED
    canvas[shiva_base_y - 15, shiva_center_x - 1] = THIRD_EYE_RED
    canvas[shiva_base_y - 15, shiva_center_x + 1] = THIRD_EYE_RED
    canvas[shiva_base_y - 16, shiva_center_x] = THIRD_EYE_RED
    
    # Sacred ash markings (vibhuti lines on forehead)
    for x in range(shiva_center_x - 3, shiva_center_x + 4):
        canvas[shiva_base_y - 13, x] = ASH_GRAY
    
    # Matted hair (jata) - much more elaborate
    for y in range(shiva_base_y - 22, shiva_base_y - 16):
        for x in range(shiva_center_x - 6, shiva_center_x + 7):
            canvas[y, x] = BLACK_HAIR
    # Hair extends wider at top
    for x in range(shiva_center_x - 8, shiva_center_x + 9):
        canvas[shiva_base_y - 20, x] = BLACK_HAIR
        canvas[shiva_base_y - 21, x] = BLACK_HAIR
    # Hair highlights
    canvas[shiva_base_y - 19, shiva_center_x - 4] = BROWN_HAIR
    canvas[shiva_base_y - 19, shiva_center_x + 4] = BROWN_HAIR
    canvas[shiva_base_y - 20, shiva_center_x - 2] = BROWN_HAIR
    canvas[shiva_base_y - 20, shiva_center_x + 2] = BROWN_HAIR
    
    # Crescent moon in hair (left side) - larger
    canvas[shiva_base_y - 22, shiva_center_x - 7] = CRESCENT_WHITE
    canvas[shiva_base_y - 21, shiva_center_x - 7] = CRESCENT_WHITE
    canvas[shiva_base_y - 21, shiva_center_x - 8] = CRESCENT_WHITE
    canvas[shiva_base_y - 20, shiva_center_x - 8] = CRESCENT_WHITE
    canvas[shiva_base_y - 20, shiva_center_x - 9] = CRESCENT_WHITE
    
    # River Ganga flowing from hair (blue stream) - more prominent
    for y in range(shiva_base_y - 21, shiva_base_y - 10):
        canvas[y, shiva_center_x + 7] = GANGA_BLUE
        if y % 2 == 0:
            canvas[y, shiva_center_x + 8] = GANGA_BLUE
    
    # Cobra/Snake around neck (Vasuki)
    canvas[shiva_base_y - 11, shiva_center_x - 3] = BLACK_HAIR
    canvas[shiva_base_y - 11, shiva_center_x - 2] = BROWN_HAIR
    canvas[shiva_base_y - 11, shiva_center_x - 1] = BLACK_HAIR
    canvas[shiva_base_y - 12, shiva_center_x - 2] = THIRD_EYE_RED  # Snake head/eyes
    
    # Rudraksha beads - more visible
    canvas[shiva_base_y - 9, shiva_center_x - 2] = BROWN_HAIR
    canvas[shiva_base_y - 9, shiva_center_x + 2] = BROWN_HAIR
    canvas[shiva_base_y - 8, shiva_center_x - 1] = BROWN_HAIR
    canvas[shiva_base_y - 8, shiva_center_x + 1] = BROWN_HAIR
    
    # Trishul (trident) beside him (right side) - larger
    trident_x = shiva_center_x + 11
    for y in range(shiva_base_y - 18, shiva_base_y + 1):
        canvas[y, trident_x] = STONE_GRAY  # Staff
    # Trident prongs - taller
    for y in range(shiva_base_y - 23, shiva_base_y - 18):
        canvas[y, trident_x - 1] = STONE_LIGHT
        canvas[y, trident_x] = STONE_LIGHT
        canvas[y, trident_x + 1] = STONE_LIGHT
    # Trident tips
    canvas[shiva_base_y - 24, trident_x - 1] = STONE_LIGHT
    canvas[shiva_base_y - 24, trident_x] = GOLD
    canvas[shiva_base_y - 24, trident_x + 1] = STONE_LIGHT
    
    # Damaru (small drum) on left side - larger
    damaru_x = shiva_center_x - 11
    canvas[shiva_base_y - 15, damaru_x] = GOLD
    canvas[shiva_base_y - 15, damaru_x + 1] = GOLD
    canvas[shiva_base_y - 14, damaru_x] = GOLD_DARK
    canvas[shiva_base_y - 14, damaru_x + 1] = GOLD_DARK
    canvas[shiva_base_y - 13, damaru_x] = GOLD
    canvas[shiva_base_y - 13, damaru_x + 1] = GOLD
    
    # Simple ground at very bottom
    for y in range(shiva_base_y + 2, 32):
        for x in range(width):
            canvas[y, x] = MOUNTAIN_DARK if x % 2 == 0 else MOUNTAIN_MID
    
    return canvas

def main():
    """Create and save the Shiva mountains background"""
    print("Creating Shiva in the mountains background...")
    
    background = create_shiva_mountains_background()
    
    # Convert to PIL Image
    img = Image.fromarray(background, mode='RGBA')
    
    # Scale up by 8x to make it 512x256 (64 * 8 = 512, 32 * 8 = 256)
    # Using NEAREST to preserve pixel art style
    img_scaled = img.resize((512, 256), Image.NEAREST)
    
    # Save the image
    output_path = 'art/shiva_mountains_background.png'
    img_scaled.save(output_path)
    
    print(f"✅ Created {output_path}")
    print(f"   Base size: 64x32 pixels")
    print(f"   Scaled size: {img_scaled.size[0]}x{img_scaled.size[1]} pixels")
    print(f"   Style: Pixel art")
    print(f"   Scene: Lord Shiva meditating in the Himalayas with trident and sacred elements")

if __name__ == '__main__':
    main()
