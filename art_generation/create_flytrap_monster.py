"""
Flytrap Monster Creator
Creates pixel art for a carnivorous Venus flytrap with snapping jaws.
Inspired by the Venus flytrap with trigger hairs and jaw-like trap.

Resolution: 64x64 pixels (scaled 4x to 256x256)
Style: Pixel art with organic plant features
Palette: Bright green body, red/pink interior, yellow-green spikes
"""

from PIL import Image
import numpy as np


def create_flytrap_default():
    """Create the default open flytrap pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - inspired by Venus flytrap
    GREEN_BRIGHT = [120, 200, 50, 255]     # Bright outer green
    GREEN_BASE = [90, 160, 40, 255]        # Medium green
    GREEN_DARK = [60, 120, 30, 255]        # Dark green shadows
    GREEN_LIGHT = [150, 220, 80, 255]      # Light green highlights
    RED_INTERIOR = [200, 50, 60, 255]      # Red interior
    RED_DARK = [150, 30, 40, 255]          # Dark red
    PINK_LIGHT = [220, 100, 110, 255]      # Pink highlights
    SPIKE_YELLOW = [180, 200, 60, 255]     # Yellow-green spikes
    SPIKE_LIGHT = [200, 220, 100, 255]     # Light spike tips
    TRIGGER_HAIR = [140, 180, 50, 255]     # Trigger hairs
    STEM_GREEN = [80, 140, 35, 255]        # Stem/base
    STEM_DARK = [50, 100, 25, 255]         # Stem shadow
    
    center_x = 32
    base_y = 58
    
    # === STEM/BASE ===
    for sy in range(25):
        stem_width = 4 - sy // 10
        for sx in range(-stem_width, stem_width + 1):
            stem_x = center_x + sx
            stem_y = base_y - sy
            if 0 <= stem_x < width and 0 <= stem_y < height:
                if sx < 0:
                    canvas[stem_y][stem_x] = STEM_DARK
                else:
                    canvas[stem_y][stem_x] = STEM_GREEN if sx < 2 else GREEN_DARK
    
    # === LOWER JAW (bottom trap lobe) ===
    jaw_y = base_y - 26
    
    # Lower jaw body
    for jy in range(12):
        jaw_width = 14 - jy // 2
        for jx in range(-jaw_width, jaw_width + 1):
            jaw_x = center_x + jx
            jaw_ypos = jaw_y + jy
            if 0 <= jaw_x < width and 0 <= jaw_ypos < height:
                # Outer green shell
                if abs(jx) > jaw_width - 3:
                    canvas[jaw_ypos][jaw_x] = GREEN_DARK if jx < 0 else GREEN_BASE
                # Interior red/pink
                elif jy < 8:
                    if jy < 2:
                        canvas[jaw_ypos][jaw_x] = RED_DARK if abs(jx) > 6 else RED_INTERIOR
                    else:
                        canvas[jaw_ypos][jaw_x] = RED_INTERIOR if abs(jx) < 8 else PINK_LIGHT
                else:
                    canvas[jaw_ypos][jaw_x] = GREEN_BASE
    
    # Lower jaw spikes (teeth-like projections)
    for spike_num in range(11):
        spike_x_offset = -15 + spike_num * 3
        spike_length = 8 - abs(spike_num - 5) // 2
        for sy in range(spike_length):
            spike_x = center_x + spike_x_offset
            spike_y = jaw_y - sy
            if 0 <= spike_x < width and 0 <= spike_y < height:
                if sy < spike_length - 2:
                    canvas[spike_y][spike_x] = SPIKE_YELLOW if sy < 2 else SPIKE_LIGHT
                else:
                    canvas[spike_y][spike_x] = GREEN_LIGHT
    
    # === UPPER JAW (top trap lobe) ===
    upper_jaw_y = jaw_y - 8
    
    # Upper jaw body
    for jy in range(12):
        jaw_width = 14 - jy // 2
        for jx in range(-jaw_width, jaw_width + 1):
            jaw_x = center_x + jx
            jaw_ypos = upper_jaw_y - jy
            if 0 <= jaw_x < width and 0 <= jaw_ypos < height:
                # Outer green shell
                if abs(jx) > jaw_width - 3:
                    canvas[jaw_ypos][jaw_x] = GREEN_BRIGHT if jx > 0 else GREEN_BASE
                # Interior red/pink
                elif jy > 4:
                    if jy > 9:
                        canvas[jaw_ypos][jaw_x] = RED_DARK if abs(jx) > 6 else RED_INTERIOR
                    else:
                        canvas[jaw_ypos][jaw_x] = RED_INTERIOR if abs(jx) < 8 else PINK_LIGHT
                else:
                    canvas[jaw_ypos][jaw_x] = GREEN_BRIGHT
    
    # Upper jaw spikes
    for spike_num in range(11):
        spike_x_offset = -15 + spike_num * 3
        spike_length = 8 - abs(spike_num - 5) // 2
        for sy in range(spike_length):
            spike_x = center_x + spike_x_offset
            spike_y = upper_jaw_y - 12 - sy
            if 0 <= spike_x < width and 0 <= spike_y < height:
                if sy < spike_length - 2:
                    canvas[spike_y][spike_x] = SPIKE_YELLOW if sy < 2 else SPIKE_LIGHT
                else:
                    canvas[spike_y][spike_x] = GREEN_LIGHT
    
    # === TRIGGER HAIRS (inside the trap) ===
    # Three prominent trigger hairs
    for hair_num in range(3):
        hair_x_offset = -6 + hair_num * 6
        hair_base_y = jaw_y + 4
        
        # Each hair is slightly curved
        for hy in range(8):
            hair_curve = hy // 3
            hair_x = center_x + hair_x_offset + hair_curve
            hair_y = hair_base_y - hy
            if 0 <= hair_x < width and 0 <= hair_y < height:
                canvas[hair_y][hair_x] = TRIGGER_HAIR if hy < 6 else GREEN_LIGHT
    
    # === VEINS/TEXTURE (on interior) ===
    # Add vein patterns to interior
    for vein in range(4):
        vein_y_offset = 2 + vein * 2
        for vx in range(-8, 9):
            vein_x = center_x + vx
            vein_y = jaw_y + vein_y_offset
            if 0 <= vein_x < width and 0 <= vein_y < height:
                if canvas[vein_y][vein_x][3] > 0 and canvas[vein_y][vein_x][0] > 150:
                    canvas[vein_y][vein_x] = RED_DARK
    
    # === LEAVES (small side leaves at base) ===
    # Left leaf
    for ly in range(6):
        leaf_width = 3 - ly // 3
        for lx in range(-leaf_width, leaf_width + 1):
            leaf_x = center_x - 10 + lx - ly
            leaf_y = base_y - 12 + ly
            if 0 <= leaf_x < width and 0 <= leaf_y < height:
                canvas[leaf_y][leaf_x] = GREEN_DARK if lx < 0 else GREEN_BASE
    
    # Right leaf
    for ly in range(6):
        leaf_width = 3 - ly // 3
        for lx in range(-leaf_width, leaf_width + 1):
            leaf_x = center_x + 10 + lx + ly
            leaf_y = base_y - 12 + ly
            if 0 <= leaf_x < width and 0 <= leaf_y < height:
                canvas[leaf_y][leaf_x] = GREEN_BASE if lx < 0 else GREEN_BRIGHT
    
    return canvas


def create_flytrap_attack():
    """Create the attacking flytrap - WIDE OPEN mouth showing big fangs."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    GREEN_BRIGHT = [120, 200, 50, 255]
    GREEN_BASE = [90, 160, 40, 255]
    GREEN_DARK = [60, 120, 30, 255]
    GREEN_LIGHT = [150, 220, 80, 255]
    RED_INTERIOR = [200, 50, 60, 255]
    RED_DARK = [150, 30, 40, 255]
    PINK_LIGHT = [220, 100, 110, 255]
    SPIKE_YELLOW = [180, 200, 60, 255]
    SPIKE_LIGHT = [200, 220, 100, 255]
    FANG_WHITE = [240, 240, 230, 255]
    FANG_SHADOW = [200, 200, 180, 255]
    TRIGGER_HAIR = [140, 180, 50, 255]
    STEM_GREEN = [80, 140, 35, 255]
    STEM_DARK = [50, 100, 25, 255]
    
    center_x = 32
    base_y = 58
    
    # === STEM/BASE (same as default) ===
    for sy in range(25):
        stem_width = 4 - sy // 10
        for sx in range(-stem_width, stem_width + 1):
            stem_x = center_x + sx
            stem_y = base_y - sy
            if 0 <= stem_x < width and 0 <= stem_y < height:
                if sx < 0:
                    canvas[stem_y][stem_x] = STEM_DARK
                else:
                    canvas[stem_y][stem_x] = STEM_GREEN if sx < 2 else GREEN_DARK
    
    # === LOWER JAW (WIDER OPEN - bottom trap lobe) ===
    jaw_y = base_y - 26
    
    # Lower jaw body (slightly larger opening)
    for jy in range(14):
        jaw_width = 16 - jy // 2
        for jx in range(-jaw_width, jaw_width + 1):
            jaw_x = center_x + jx
            jaw_ypos = jaw_y + jy
            if 0 <= jaw_x < width and 0 <= jaw_ypos < height:
                # Outer green shell
                if abs(jx) > jaw_width - 3:
                    canvas[jaw_ypos][jaw_x] = GREEN_DARK if jx < 0 else GREEN_BASE
                # Interior red/pink
                elif jy < 10:
                    if jy < 2:
                        canvas[jaw_ypos][jaw_x] = RED_DARK if abs(jx) > 8 else RED_INTERIOR
                    else:
                        canvas[jaw_ypos][jaw_x] = RED_INTERIOR if abs(jx) < 10 else PINK_LIGHT
                else:
                    canvas[jaw_ypos][jaw_x] = GREEN_BASE
    
    # Lower jaw spikes (normal teeth)
    for spike_num in range(11):
        spike_x_offset = -15 + spike_num * 3
        spike_length = 6 - abs(spike_num - 5) // 3
        for sy in range(spike_length):
            spike_x = center_x + spike_x_offset
            spike_y = jaw_y - sy
            if 0 <= spike_x < width and 0 <= spike_y < height:
                if sy < spike_length - 2:
                    canvas[spike_y][spike_x] = SPIKE_YELLOW if sy < 2 else SPIKE_LIGHT
                else:
                    canvas[spike_y][spike_x] = GREEN_LIGHT
    
    # === BIG FANGS ON LOWER JAW (2 prominent fangs) ===
    for fang_offset in [-6, 6]:
        for fy in range(10):
            fang_width = 2 - fy // 6
            for fx in range(-fang_width, fang_width + 1):
                fang_x = center_x + fang_offset + fx
                fang_y = jaw_y - fy
                if 0 <= fang_x < width and 0 <= fang_y < height:
                    if fy < 8:
                        canvas[fang_y][fang_x] = FANG_WHITE if fx >= 0 else FANG_SHADOW
                    else:
                        canvas[fang_y][fang_x] = SPIKE_YELLOW
    
    # === UPPER JAW (WIDER OPEN - top trap lobe) ===
    upper_jaw_y = jaw_y - 12
    
    # Upper jaw body (larger opening)
    for jy in range(14):
        jaw_width = 16 - jy // 2
        for jx in range(-jaw_width, jaw_width + 1):
            jaw_x = center_x + jx
            jaw_ypos = upper_jaw_y - jy
            if 0 <= jaw_x < width and 0 <= jaw_ypos < height:
                # Outer green shell
                if abs(jx) > jaw_width - 3:
                    canvas[jaw_ypos][jaw_x] = GREEN_BRIGHT if jx > 0 else GREEN_BASE
                # Interior red/pink
                elif jy > 4:
                    if jy > 11:
                        canvas[jaw_ypos][jaw_x] = RED_DARK if abs(jx) > 8 else RED_INTERIOR
                    else:
                        canvas[jaw_ypos][jaw_x] = RED_INTERIOR if abs(jx) < 10 else PINK_LIGHT
                else:
                    canvas[jaw_ypos][jaw_x] = GREEN_BRIGHT
    
    # Upper jaw spikes
    for spike_num in range(11):
        spike_x_offset = -15 + spike_num * 3
        spike_length = 6 - abs(spike_num - 5) // 3
        for sy in range(spike_length):
            spike_x = center_x + spike_x_offset
            spike_y = upper_jaw_y - 14 - sy
            if 0 <= spike_x < width and 0 <= spike_y < height:
                if sy < spike_length - 2:
                    canvas[spike_y][spike_x] = SPIKE_YELLOW if sy < 2 else SPIKE_LIGHT
                else:
                    canvas[spike_y][spike_x] = GREEN_LIGHT
    
    # === BIG FANGS ON UPPER JAW (2 prominent fangs pointing down) ===
    for fang_offset in [-6, 6]:
        for fy in range(10):
            fang_width = 2 - fy // 6
            for fx in range(-fang_width, fang_width + 1):
                fang_x = center_x + fang_offset + fx
                fang_y = upper_jaw_y - 14 - fy
                if 0 <= fang_x < width and 0 <= fang_y < height:
                    if fy < 8:
                        canvas[fang_y][fang_x] = FANG_WHITE if fx >= 0 else FANG_SHADOW
                    else:
                        canvas[fang_y][fang_x] = SPIKE_YELLOW
    
    # === TRIGGER HAIRS (standing alert, menacing) ===
    # Four trigger hairs
    for hair_num in range(4):
        hair_x_offset = -9 + hair_num * 6
        hair_base_y = jaw_y + 4
        
        # Each hair slightly curved and longer
        for hy in range(10):
            hair_curve = hy // 3
            hair_x = center_x + hair_x_offset + hair_curve
            hair_y = hair_base_y - hy
            if 0 <= hair_x < width and 0 <= hair_y < height:
                canvas[hair_y][hair_x] = TRIGGER_HAIR if hy < 8 else GREEN_LIGHT
    
    # === VEINS/TEXTURE (more prominent on interior) ===
    for vein in range(5):
        vein_y_offset = 2 + vein * 2
        for vx in range(-10, 11):
            vein_x = center_x + vx
            vein_y = jaw_y + vein_y_offset
            if 0 <= vein_x < width and 0 <= vein_y < height:
                if canvas[vein_y][vein_x][3] > 0 and canvas[vein_y][vein_x][0] > 150:
                    canvas[vein_y][vein_x] = RED_DARK
    
    # === LEAVES (small side leaves at base) ===
    # Left leaf
    for ly in range(6):
        leaf_width = 3 - ly // 3
        for lx in range(-leaf_width, leaf_width + 1):
            leaf_x = center_x - 10 + lx - ly
            leaf_y = base_y - 12 + ly
            if 0 <= leaf_x < width and 0 <= leaf_y < height:
                canvas[leaf_y][leaf_x] = GREEN_DARK if lx < 0 else GREEN_BASE
    
    # Right leaf
    for ly in range(6):
        leaf_width = 3 - ly // 3
        for lx in range(-leaf_width, leaf_width + 1):
            leaf_x = center_x + 10 + lx + ly
            leaf_y = base_y - 12 + ly
            if 0 <= leaf_x < width and 0 <= leaf_y < height:
                canvas[leaf_y][leaf_x] = GREEN_BASE if lx < 0 else GREEN_BRIGHT
    
    return canvas


def main():
    print("Creating flytrap monster images...")
    
    flytrap_default = create_flytrap_default()
    flytrap_attack = create_flytrap_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(flytrap_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('art/flytrap_monster.png')
    print(f"✓ Saved: art/flytrap_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(flytrap_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('art/flytrap_monster_attack.png')
    print(f"✓ Saved: art/flytrap_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Flytrap monster creation complete!")
    print("\nFeatures:")
    print("- Default: Open trap with red interior, trigger hairs, and interlocking spikes")
    print("- Attack: Violent snapping motion with closed jaws and motion effects")
    print("\nStyle: Carnivorous Venus flytrap-inspired pixel art")
    print("Colors: Bright green exterior, red/pink interior, yellow-green spikes")


if __name__ == '__main__':
    main()
