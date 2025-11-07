"""
Create a pixel art lightsaber PNG
"""
from PIL import Image, ImageDraw
import numpy as np

def create_lightsaber():
    """Create a Minecraft-style lightsaber"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    BLUE = [0, 100, 255, 255]        # Main blade color
    LIGHT_BLUE = [100, 200, 255, 255] # Blade highlights
    DARK_BLUE = [0, 50, 150, 255]    # Blade core
    CYAN = [0, 255, 255, 255]        # Bright blade edge
    WHITE = [255, 255, 255, 255]     # Brightest blade core
    SILVER = [192, 192, 192, 255]    # Hilt main body
    DARK_SILVER = [128, 128, 128, 255] # Hilt shading
    LIGHT_SILVER = [230, 230, 230, 255] # Hilt highlights
    BLACK = [0, 0, 0, 255]           # Hilt details/grip
    DARK_GRAY = [64, 64, 64, 255]    # Hilt accent
    GOLD = [255, 215, 0, 255]        # Activation button
    RED = [255, 50, 50, 255]         # Power indicator
    GREEN = [50, 255, 50, 255]       # Status LED
    
    # ENERGY BLADE (main lightsaber beam)
    blade_center_x = 16
    blade_start_y = 2
    blade_end_y = 18
    blade_width = 2
    
    # Outer glow effect (widest, faintest)
    for y in range(blade_start_y, blade_end_y):
        for x in range(blade_center_x - blade_width - 1, blade_center_x + blade_width + 2):
            if x >= 0 and x < size:
                canvas[y][x] = LIGHT_BLUE
    
    # Main blade body (bright blue energy)
    for y in range(blade_start_y, blade_end_y):
        for x in range(blade_center_x - blade_width, blade_center_x + blade_width + 1):
            if x >= 0 and x < size:
                canvas[y][x] = BLUE
    
    # Inner blade (brighter core)
    for y in range(blade_start_y, blade_end_y):
        for x in range(blade_center_x - blade_width + 1, blade_center_x + blade_width):
            if x >= 0 and x < size:
                canvas[y][x] = CYAN
    
    # Blade core (brightest center line)
    for y in range(blade_start_y, blade_end_y):
        canvas[y][blade_center_x] = WHITE
    
    # Blade tip (pointed energy focus)
    canvas[blade_start_y][blade_center_x] = WHITE
    canvas[blade_start_y + 1][blade_center_x - 1] = CYAN
    canvas[blade_start_y + 1][blade_center_x + 1] = CYAN
    
    # Energy crackling effects (random energy discharges)
    crackle_positions = [
        (blade_start_y + 3, blade_center_x - blade_width - 2),
        (blade_start_y + 7, blade_center_x + blade_width + 2),
        (blade_start_y + 11, blade_center_x - blade_width - 2),
        (blade_start_y + 14, blade_center_x + blade_width + 2),
    ]
    
    for crackle_y, crackle_x in crackle_positions:
        if 0 <= crackle_y < size and 0 <= crackle_x < size:
            canvas[crackle_y][crackle_x] = CYAN
    
    # EMITTER (where the blade emerges)
    emitter_y = blade_end_y
    
    # Emitter ring (silver focusing crystal housing)
    for x in range(blade_center_x - 3, blade_center_x + 4):
        canvas[emitter_y][x] = SILVER
    canvas[emitter_y][blade_center_x - 3] = DARK_SILVER
    canvas[emitter_y][blade_center_x + 3] = DARK_SILVER
    canvas[emitter_y][blade_center_x] = LIGHT_SILVER
    
    # Focusing crystal glimpse
    canvas[emitter_y][blade_center_x - 1] = CYAN
    canvas[emitter_y][blade_center_x + 1] = CYAN
    
    # HILT (lightsaber handle)
    hilt_start_y = emitter_y + 1
    hilt_end_y = hilt_start_y + 10
    hilt_width = 2
    
    # Main hilt body (sleek silver cylinder)
    for y in range(hilt_start_y, hilt_end_y):
        for x in range(blade_center_x - hilt_width, blade_center_x + hilt_width + 1):
            canvas[y][x] = SILVER
    
    # Hilt shading (left side darker)
    for y in range(hilt_start_y, hilt_end_y):
        canvas[y][blade_center_x - hilt_width] = DARK_SILVER
        canvas[y][blade_center_x + hilt_width] = LIGHT_SILVER
    
    # Grip sections (textured for holding)
    grip_positions = [
        hilt_start_y + 2,
        hilt_start_y + 4,
        hilt_start_y + 6,
        hilt_start_y + 8,
    ]
    
    for grip_y in grip_positions:
        canvas[grip_y][blade_center_x - hilt_width] = BLACK
        canvas[grip_y][blade_center_x + hilt_width] = BLACK
        canvas[grip_y][blade_center_x] = DARK_GRAY
    
    # Activation button (iconic lightsaber feature)
    button_y = hilt_start_y + 3
    canvas[button_y][blade_center_x - hilt_width - 1] = GOLD
    canvas[button_y + 1][blade_center_x - hilt_width - 1] = GOLD
    
    # Power level indicator LED
    canvas[button_y - 1][blade_center_x - hilt_width - 1] = GREEN
    
    # POMMEL (end cap)
    pommel_y = hilt_end_y
    
    # Pommel cap (wider end piece)
    for x in range(blade_center_x - hilt_width - 1, blade_center_x + hilt_width + 2):
        canvas[pommel_y][x] = SILVER
    
    # Pommel shading
    canvas[pommel_y][blade_center_x - hilt_width - 1] = DARK_SILVER
    canvas[pommel_y][blade_center_x + hilt_width + 1] = DARK_SILVER
    canvas[pommel_y][blade_center_x] = LIGHT_SILVER
    
    # Belt clip attachment point
    canvas[pommel_y][blade_center_x + hilt_width + 2] = DARK_GRAY
    
    # ADDITIONAL DETAILS
    # Charging port (technical detail)
    canvas[hilt_start_y + 7][blade_center_x + hilt_width + 1] = BLACK
    
    # Blade length adjustment dial
    canvas[hilt_start_y + 5][blade_center_x + hilt_width + 1] = DARK_SILVER
    
    # Emergency shutdown switch
    canvas[hilt_start_y + 1][blade_center_x + hilt_width + 1] = RED
    
    # Kyber crystal chamber indicator (small window)
    canvas[hilt_start_y + 6][blade_center_x - hilt_width - 1] = BLUE
    
    # Energy field effects around blade base
    energy_field_positions = [
        (emitter_y - 1, blade_center_x - 2),
        (emitter_y - 1, blade_center_x + 2),
        (emitter_y + 1, blade_center_x - 2),
        (emitter_y + 1, blade_center_x + 2),
    ]
    
    for field_y, field_x in energy_field_positions:
        if 0 <= field_y < size and 0 <= field_x < size:
            canvas[field_y][field_x] = LIGHT_BLUE
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'ascii_art/lightsaber.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art lightsaber with energy effects")
    print(f"   Features: Blue energy blade, silver hilt, activation controls")
    print(f"   Details: Emitter ring, grip texture, power indicators, energy glow")
    print(f"   Special: Kyber crystal chamber, crackling energy effects")

if __name__ == '__main__':
    create_lightsaber()