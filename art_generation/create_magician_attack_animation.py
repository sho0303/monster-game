"""
Create an animated attack version of the magician character
Shows the magician casting a powerful spell with magic effects and dynamic pose
"""
from PIL import Image, ImageDraw
import numpy as np

def create_magician_attack():
    """Create a Minecraft-style magician in spell-casting attack animation"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    GRAY_BEARD = [180, 180, 180, 255]    # Gray beard
    WHITE_BEARD = [240, 240, 240, 255]   # Beard highlight
    SKIN = [255, 220, 177, 255]          # Skin tone
    PURPLE_ROBE = [120, 50, 180, 255]    # Purple robe
    DARK_PURPLE = [70, 30, 110, 255]     # Robe shadow
    BLUE_ROBE = [50, 80, 200, 255]       # Blue accents
    DARK_BLUE = [30, 50, 130, 255]       # Blue shadow
    GOLD = [255, 215, 0, 255]            # Gold trim
    DARK_GOLD = [200, 160, 0, 255]       # Gold shadow
    BROWN_STAFF = [101, 67, 33, 255]     # Wooden staff
    DARK_BROWN = [70, 45, 20, 255]       # Staff shadow
    CYAN_MAGIC = [0, 255, 255, 255]      # Magic glow
    BLUE_MAGIC = [100, 150, 255, 255]    # Magic orb
    BLACK = [0, 0, 0, 255]               # Eyes, outlines
    PURPLE_HAT = [100, 40, 150, 255]     # Wizard hat
    
    # Attack spell colors
    BRIGHT_CYAN = [0, 255, 255, 255]     # Bright magic
    WHITE_ENERGY = [255, 255, 255, 255]   # Pure energy
    ELECTRIC_BLUE = [30, 144, 255, 255]   # Lightning effect
    VIOLET_ENERGY = [138, 43, 226, 255]   # Violet magic
    YELLOW_SPARK = [255, 255, 0, 255]     # Energy sparks
    ORANGE_ENERGY = [255, 165, 0, 255]    # Fire magic
    LIGHT_PURPLE = [200, 100, 255, 180]   # Magic aura
    
    # WIZARD HAT (tilted dramatically in casting pose)
    hat_start_x = 10  # Shifted left due to leaning
    hat_start_y = 0
    
    # Hat tip (pointy top, tilted)
    canvas[hat_start_y][hat_start_x + 2] = PURPLE_HAT
    canvas[hat_start_y][hat_start_x + 3] = PURPLE_HAT
    
    canvas[hat_start_y + 1][hat_start_x + 1] = PURPLE_HAT
    canvas[hat_start_y + 1][hat_start_x + 2] = PURPLE_HAT
    canvas[hat_start_y + 1][hat_start_x + 3] = PURPLE_HAT
    canvas[hat_start_y + 1][hat_start_x + 4] = PURPLE_HAT
    
    canvas[hat_start_y + 2][hat_start_x] = PURPLE_HAT
    canvas[hat_start_y + 2][hat_start_x + 1] = PURPLE_HAT
    canvas[hat_start_y + 2][hat_start_x + 2] = PURPLE_HAT
    canvas[hat_start_y + 2][hat_start_x + 3] = PURPLE_HAT
    canvas[hat_start_y + 2][hat_start_x + 4] = PURPLE_HAT
    canvas[hat_start_y + 2][hat_start_x + 5] = PURPLE_HAT
    
    # Hat brim (flowing with motion)
    for x in range(hat_start_x, hat_start_x + 8):
        if x < size:
            canvas[hat_start_y + 3][x] = PURPLE_HAT
    
    # Magical stars on hat (glowing brighter during spell)
    canvas[hat_start_y + 2][hat_start_x + 2] = YELLOW_SPARK
    canvas[hat_start_y + 1][hat_start_x + 3] = WHITE_ENERGY
    
    # Magic energy flowing from hat
    canvas[hat_start_y][hat_start_x + 4] = BRIGHT_CYAN
    canvas[hat_start_y][hat_start_x + 5] = CYAN_MAGIC
    
    # HEAD (8x8, intense concentration)
    head_start_x = 11  # Slightly shifted in casting pose
    head_start_y = 4
    
    # Face (skin tone) - focused expression
    for y in range(head_start_y, head_start_y + 5):
        for x in range(head_start_x, head_start_x + 8):
            if x < size:
                canvas[y][x] = SKIN
    
    # Eyes (intense glowing with magic)
    canvas[head_start_y + 2][head_start_x + 2] = CYAN_MAGIC  # Glowing eyes
    canvas[head_start_y + 2][head_start_x + 5] = CYAN_MAGIC
    
    # Glowing eyebrows (magic energy)
    canvas[head_start_y + 1][head_start_x + 2] = WHITE_ENERGY
    canvas[head_start_y + 1][head_start_x + 5] = WHITE_ENERGY
    
    # Long gray beard (flowing with magical wind)
    for y in range(head_start_y + 4, head_start_y + 8):
        for x in range(head_start_x + 1, head_start_x + 7):
            if x < size:
                canvas[y][x] = GRAY_BEARD
    
    # Beard flowing motion effect
    canvas[head_start_y + 5][head_start_x + 7] = GRAY_BEARD if head_start_x + 7 < size else None
    canvas[head_start_y + 6][head_start_x + 8] = WHITE_BEARD if head_start_x + 8 < size else None
    
    # Magical energy in beard
    canvas[head_start_y + 5][head_start_x + 3] = BRIGHT_CYAN
    canvas[head_start_y + 6][head_start_x + 4] = WHITE_ENERGY
    
    # BODY (8x12) - Purple robe with energy flowing through it
    body_start_x = 11
    body_start_y = 12
    
    # Beard continues down chest (with magical glow)
    for y in range(body_start_y, body_start_y + 4):
        for x in range(body_start_x + 2, body_start_x + 6):
            if x < size:
                canvas[y][x] = GRAY_BEARD
    
    # Magical energy in chest beard
    canvas[body_start_y + 1][body_start_x + 3] = CYAN_MAGIC
    canvas[body_start_y + 2][body_start_x + 4] = BRIGHT_CYAN
    
    # Purple robe base (with energy crackling through it)
    for y in range(body_start_y, body_start_y + 12):
        for x in range(body_start_x, body_start_x + 8):
            if x < size and y < size and canvas[y][x][3] == 0:  # Don't overwrite beard
                canvas[y][x] = PURPLE_ROBE
    
    # Robe shadows on sides with energy glow
    for y in range(body_start_y + 4, body_start_y + 12):
        if y < size:
            canvas[y][body_start_x] = DARK_PURPLE
            if body_start_x + 7 < size:
                canvas[y][body_start_x + 7] = DARK_PURPLE
    
    # Gold trim on robe (glowing with power)
    for x in range(body_start_x + 1, body_start_x + 7):
        if x < size:
            canvas[body_start_y + 4][x] = YELLOW_SPARK  # Brighter gold
            canvas[body_start_y + 5][x] = GOLD
    
    # Magical energy coursing through robe
    canvas[body_start_y + 7][body_start_x + 3] = ELECTRIC_BLUE
    canvas[body_start_y + 7][body_start_x + 4] = BRIGHT_CYAN
    canvas[body_start_y + 8][body_start_x + 3] = VIOLET_ENERGY
    canvas[body_start_y + 8][body_start_x + 4] = ELECTRIC_BLUE
    
    # LEFT ARM (extended dramatically for spell casting)
    left_arm_x = 5   # Extended further out for dramatic pose
    left_arm_y = 10  # Raised higher for casting
    
    # Purple sleeve (flowing with motion)
    for y in range(left_arm_y, left_arm_y + 8):
        for x in range(left_arm_x, left_arm_x + 6):  # Extended arm
            if x < size and y < size:
                canvas[y][x] = PURPLE_ROBE
    
    # Sleeve flowing effect
    for i in range(3):
        trail_x = left_arm_x - i - 1
        if trail_x >= 0:
            canvas[left_arm_y + 2][trail_x] = LIGHT_PURPLE
            canvas[left_arm_y + 3][trail_x] = LIGHT_PURPLE
    
    # Hand (channeling energy)
    canvas[left_arm_y + 7][left_arm_x + 4] = SKIN
    canvas[left_arm_y + 7][left_arm_x + 5] = SKIN
    
    # MASSIVE SPELL EFFECT from left hand
    spell_x = left_arm_x + 6
    spell_y = left_arm_y + 6
    
    # Central energy orb (much larger and brighter)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            orb_x = spell_x + dx
            orb_y = spell_y + dy
            if 0 <= orb_x < size and 0 <= orb_y < size:
                if abs(dx) + abs(dy) <= 2:
                    if abs(dx) + abs(dy) == 0:
                        canvas[orb_y][orb_x] = WHITE_ENERGY  # Core
                    elif abs(dx) + abs(dy) == 1:
                        canvas[orb_y][orb_x] = BRIGHT_CYAN   # Inner ring
                    else:
                        canvas[orb_y][orb_x] = CYAN_MAGIC    # Outer ring
    
    # Energy beams radiating outward
    beam_positions = [
        (spell_x + 3, spell_y),     # Right beam
        (spell_x + 4, spell_y),
        (spell_x + 5, spell_y),
        (spell_x + 2, spell_y - 2), # Up-right beam
        (spell_x + 2, spell_y + 2), # Down-right beam
        (spell_x + 3, spell_y - 1), # Diagonal beams
        (spell_x + 3, spell_y + 1),
    ]
    
    for bx, by in beam_positions:
        if 0 <= bx < size and 0 <= by < size:
            canvas[by][bx] = ELECTRIC_BLUE
    
    # Magical sparks around spell
    spark_positions = [
        (spell_x + 4, spell_y - 1, YELLOW_SPARK),
        (spell_x + 4, spell_y + 1, ORANGE_ENERGY),
        (spell_x + 3, spell_y - 2, WHITE_ENERGY),
        (spell_x + 3, spell_y + 2, VIOLET_ENERGY),
        (spell_x + 5, spell_y - 1, BRIGHT_CYAN),
        (spell_x + 5, spell_y + 1, ELECTRIC_BLUE),
    ]
    
    for sx, sy, color in spark_positions:
        if 0 <= sx < size and 0 <= sy < size:
            canvas[sy][sx] = color
    
    # RIGHT ARM (holding staff, raised in casting pose)
    right_arm_x = 19  # Positioned for dramatic staff raise
    right_arm_y = 8   # Raised higher for spell casting
    
    # Purple sleeve
    for y in range(right_arm_y, right_arm_y + 10):
        for x in range(right_arm_x, right_arm_x + 4):
            if x < size and y < size:
                canvas[y][x] = PURPLE_ROBE
    
    # Hand gripping staff
    canvas[right_arm_y + 8][right_arm_x + 1] = SKIN
    canvas[right_arm_y + 8][right_arm_x + 2] = SKIN
    
    # Wooden staff (angled dramatically)
    staff_positions = [
        (right_arm_x + 2, right_arm_y - 4),
        (right_arm_x + 2, right_arm_y - 3),
        (right_arm_x + 2, right_arm_y - 2),
        (right_arm_x + 2, right_arm_y - 1),
        (right_arm_x + 2, right_arm_y),
        (right_arm_x + 2, right_arm_y + 1),
        (right_arm_x + 2, right_arm_y + 2),
        (right_arm_x + 2, right_arm_y + 3),
        (right_arm_x + 2, right_arm_y + 4),
        (right_arm_x + 2, right_arm_y + 5),
        (right_arm_x + 2, right_arm_y + 6),
        (right_arm_x + 2, right_arm_y + 7),
        (right_arm_x + 2, right_arm_y + 8),
    ]
    
    for sx, sy in staff_positions:
        if 0 <= sx < size and 0 <= sy < size:
            canvas[sy][sx] = BROWN_STAFF
    
    # MASSIVE CRYSTAL EXPLOSION at top of staff
    crystal_x = right_arm_x + 2
    crystal_y = right_arm_y - 5
    
    # Central crystal (much brighter)
    if 0 <= crystal_x < size and 0 <= crystal_y < size:
        canvas[crystal_y][crystal_x] = WHITE_ENERGY
    
    # Crystal energy burst
    crystal_burst = [
        (crystal_x, crystal_y - 1, BRIGHT_CYAN),
        (crystal_x, crystal_y + 1, BRIGHT_CYAN),
        (crystal_x - 1, crystal_y, ELECTRIC_BLUE),
        (crystal_x + 1, crystal_y, ELECTRIC_BLUE),
        (crystal_x - 1, crystal_y - 1, YELLOW_SPARK),
        (crystal_x + 1, crystal_y - 1, YELLOW_SPARK),
        (crystal_x - 1, crystal_y + 1, VIOLET_ENERGY),
        (crystal_x + 1, crystal_y + 1, VIOLET_ENERGY),
        (crystal_x, crystal_y - 2, ORANGE_ENERGY),
        (crystal_x, crystal_y + 2, ORANGE_ENERGY),
    ]
    
    for cx, cy, color in crystal_burst:
        if 0 <= cx < size and 0 <= cy < size:
            canvas[cy][cx] = color
    
    # LEFT LEG (4x8) - Stable casting stance
    left_leg_x = 11
    left_leg_y = 24
    
    for y in range(left_leg_y, min(left_leg_y + 8, size)):
        for x in range(left_leg_x, left_leg_x + 3):
            if x < size:
                canvas[y][x] = PURPLE_ROBE
    
    # RIGHT LEG (4x8) - Braced for spell power
    right_leg_x = 16
    right_leg_y = 24
    
    for y in range(right_leg_y, min(right_leg_y + 8, size)):
        for x in range(right_leg_x, right_leg_x + 4):  # Wider stance
            if x < size:
                canvas[y][x] = PURPLE_ROBE
    
    # Magical shoes (glowing with power)
    for x in range(left_leg_x, left_leg_x + 3):
        if x < size and left_leg_y + 6 < size:
            canvas[left_leg_y + 6][x] = ELECTRIC_BLUE  # Glowing shoes
            if left_leg_y + 7 < size:
                canvas[left_leg_y + 7][x] = DARK_BLUE
    
    for x in range(right_leg_x, right_leg_x + 4):
        if x < size and right_leg_y + 6 < size:
            canvas[right_leg_y + 6][x] = ELECTRIC_BLUE
            if right_leg_y + 7 < size:
                canvas[right_leg_y + 7][x] = DARK_BLUE
    
    # Magical ground effects (energy crackling at feet)
    ground_effects = [
        (left_leg_x - 1, left_leg_y + 8, CYAN_MAGIC),
        (left_leg_x + 1, left_leg_y + 8, BRIGHT_CYAN),
        (right_leg_x + 1, right_leg_y + 8, VIOLET_ENERGY),
        (right_leg_x + 3, right_leg_y + 8, YELLOW_SPARK),
    ]
    
    for gx, gy, color in ground_effects:
        if 0 <= gx < size and 0 <= gy < size:
            canvas[gy][gx] = color
    
    # Enhanced gold trim on sleeves (glowing with spell power)
    canvas[left_arm_y + 1][left_arm_x + 2] = YELLOW_SPARK
    canvas[left_arm_y + 1][left_arm_x + 3] = GOLD
    canvas[right_arm_y + 1][right_arm_x + 1] = YELLOW_SPARK
    canvas[right_arm_y + 1][right_arm_x + 2] = GOLD
    
    # Magical aura surrounding the entire magician
    aura_positions = [
        (head_start_x - 1, head_start_y + 2),
        (head_start_x + 8, head_start_y + 3),
        (body_start_x - 1, body_start_y + 6),
        (body_start_x + 8, body_start_y + 8),
    ]
    
    for ax, ay in aura_positions:
        if 0 <= ax < size and 0 <= ay < size:
            canvas[ay][ax] = LIGHT_PURPLE
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    import os
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'art', 'magician_attack.png')
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Animated magician spell-casting attack")
    print(f"   Features: Dramatic casting pose, massive energy spell, crystal explosion")
    print(f"   Animation: Flowing robes, glowing eyes, energy beams, magical aura")
    print(f"   Effects: Lightning magic, energy orbs, sparks, ground crackling")

if __name__ == '__main__':
    create_magician_attack()