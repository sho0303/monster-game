#!/usr/bin/env python3
"""
Bee Swarm Monster Art Generator
Creates pixel art for angry bee swarm
"""

import numpy as np
from PIL import Image
import os

def create_bee_swarm_art():
    """Create bee swarm pixel art"""
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    BLACK = [0, 0, 0, 255]
    YELLOW = [255, 215, 0, 255]
    DARK_YELLOW = [218, 165, 32, 255]
    WHITE = [240, 240, 240, 180]  # Semi-transparent for wings
    BROWN = [139, 69, 19, 255]
    
    # Create multiple bees in swarm formation
    bee_positions = [
        (12, 10), (18, 8), (16, 14), (10, 16), (20, 18), 
        (14, 20), (22, 12), (8, 12), (16, 22)
    ]
    
    for x_center, y_center in bee_positions:
        # Bee body (striped)
        canvas[y_center][x_center] = YELLOW
        canvas[y_center][x_center+1] = BLACK
        canvas[y_center][x_center+2] = YELLOW
        canvas[y_center+1][x_center:x_center+3] = YELLOW
        
        # Wings (transparent)
        if x_center > 2:
            canvas[y_center-1][x_center-1] = WHITE
            canvas[y_center-1][x_center-2] = WHITE
        if x_center < 28:
            canvas[y_center-1][x_center+3] = WHITE
            canvas[y_center-1][x_center+4] = WHITE
    
    return canvas

def create_bee_attack_art():
    """Create bee swarm attack animation"""
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    YELLOW = [255, 215, 0, 255]
    BLACK = [0, 0, 0, 255]
    WHITE = [240, 240, 240, 200]
    RED = [255, 0, 0, 255]  # Angry glow
    
    # More aggressive swarm pattern (diving at viewer)
    bee_positions = [
        (16, 4), (12, 8), (20, 8), (8, 12), (16, 12), (24, 12),
        (10, 16), (18, 16), (14, 20), (22, 20), (16, 24)
    ]
    
    for x_center, y_center in bee_positions:
        # Larger, more aggressive bees
        canvas[y_center][x_center:x_center+3] = YELLOW
        canvas[y_center+1][x_center:x_center+3] = BLACK
        canvas[y_center+2][x_center:x_center+3] = YELLOW
        
        # Wings blurred (motion)
        if x_center > 3:
            canvas[y_center][x_center-2:x_center] = WHITE
        if x_center < 26:
            canvas[y_center][x_center+3:x_center+5] = WHITE
        
        # Red angry eyes/glow
        canvas[y_center+1][x_center] = RED
    
    return canvas

def save_images():
    """Generate and save bee swarm images"""
    art_dir = "../art"
    if not os.path.exists(art_dir):
        os.makedirs(art_dir)
    
    # Regular bee swarm
    canvas = create_bee_swarm_art()
    img = Image.fromarray(canvas, 'RGBA')
    img_scaled = img.resize((256, 256), Image.NEAREST)
    img_scaled.save(f"{art_dir}/bee_swarm_monster.png")
    print(f"✅ Created: {art_dir}/bee_swarm_monster.png")
    
    # Attack animation
    attack_canvas = create_bee_attack_art()
    attack_img = Image.fromarray(attack_canvas, 'RGBA')
    attack_scaled = attack_img.resize((256, 256), Image.NEAREST)
    attack_scaled.save(f"{art_dir}/bee_swarm_monster_attack.png")
    print(f"✅ Created: {art_dir}/bee_swarm_monster_attack.png")

if __name__ == "__main__":
    print("🐝 Generating Bee Swarm Art...")
    save_images()
    print("🐝 Complete!")
