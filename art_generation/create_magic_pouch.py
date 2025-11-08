"""
Create a pixel art magic pouch PNG in the style of the health potion
"""
from PIL import Image, ImageDraw
import numpy as np

def create_magic_pouch():
    """Create a Minecraft-style magic coin pouch/money bag"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette (inspired by health potion style)
    BROWN = [139, 69, 19, 255]       # Main pouch leather color
    DARK_BROWN = [101, 67, 33, 255]  # Pouch shading
    LIGHT_BROWN = [205, 133, 63, 255] # Pouch highlights
    TAN = [210, 180, 140, 255]       # Lighter leather tone
    GOLD = [255, 215, 0, 255]        # Gold coins and trim
    DARK_GOLD = [184, 134, 11, 255]  # Gold shading
    LIGHT_GOLD = [255, 255, 224, 255] # Gold highlights
    YELLOW = [255, 255, 0, 255]      # Bright coin shine
    ROPE = [160, 82, 45, 255]        # Drawstring rope
    DARK_ROPE = [101, 67, 33, 255]   # Rope shading
    SILVER = [192, 192, 192, 255]    # Silver coins/buckles
    WHITE = [255, 255, 255, 255]     # Bright reflections
    PURPLE = [138, 43, 226, 255]     # Magical aura
    MAGENTA = [255, 0, 255, 255]     # Magical sparkles
    PINK = [255, 182, 193, 255]      # Magical glow
    GREEN = [0, 255, 0, 255]         # Money magic
    
    # POUCH BASE SHAPE (bulbous money bag)
    pouch_center_x = 16
    pouch_bottom_y = 26
    pouch_top_y = 12
    pouch_max_width = 6
    
    # Main pouch body (rounded bag shape, wider at bottom)
    for y in range(pouch_top_y, pouch_bottom_y + 1):
        # Calculate width based on y position (egg-like shape)
        progress = (y - pouch_top_y) / (pouch_bottom_y - pouch_top_y)
        
        if progress < 0.3:  # Top narrow section
            width = int(pouch_max_width * 0.4)
        elif progress < 0.7:  # Middle expanding section
            width = int(pouch_max_width * (0.4 + (progress - 0.3) * 1.5))
        else:  # Bottom full width
            width = pouch_max_width
        
        for x in range(pouch_center_x - width, pouch_center_x + width + 1):
            if 0 <= x < size:
                canvas[y][x] = BROWN
    
    # DRAWSTRING TOP
    drawstring_y = pouch_top_y - 1
    drawstring_width = 3
    
    # Gathered fabric at top
    for x in range(pouch_center_x - drawstring_width, pouch_center_x + drawstring_width + 1):
        canvas[drawstring_y][x] = DARK_BROWN
    
    # Rope/string going around the top
    canvas[drawstring_y][pouch_center_x - drawstring_width - 1] = ROPE
    canvas[drawstring_y][pouch_center_x + drawstring_width + 1] = ROPE
    canvas[drawstring_y - 1][pouch_center_x - drawstring_width] = ROPE
    canvas[drawstring_y - 1][pouch_center_x + drawstring_width] = ROPE
    
    # POUCH SHADING AND HIGHLIGHTS
    for y in range(pouch_top_y, pouch_bottom_y + 1):
        progress = (y - pouch_top_y) / (pouch_bottom_y - pouch_top_y)
        
        if progress < 0.3:
            width = int(pouch_max_width * 0.4)
        elif progress < 0.7:
            width = int(pouch_max_width * (0.4 + (progress - 0.3) * 1.5))
        else:
            width = pouch_max_width
        
        # Left side shading
        if pouch_center_x - width >= 0:
            canvas[y][pouch_center_x - width] = DARK_BROWN
        # Right side highlights
        if pouch_center_x + width < size:
            canvas[y][pouch_center_x + width] = LIGHT_BROWN
    
    # Central highlight stripe
    for y in range(pouch_top_y + 2, pouch_bottom_y - 1):
        canvas[y][pouch_center_x] = TAN
    
    # COIN DETAILS ON POUCH
    # Gold coin embossed on front
    coin_center_x = pouch_center_x + 1
    coin_center_y = pouch_top_y + 6
    
    # Main coin circle
    coin_positions = [
        (coin_center_y - 1, coin_center_x - 1),
        (coin_center_y - 1, coin_center_x),
        (coin_center_y - 1, coin_center_x + 1),
        (coin_center_y, coin_center_x - 2),
        (coin_center_y, coin_center_x - 1),
        (coin_center_y, coin_center_x),
        (coin_center_y, coin_center_x + 1),
        (coin_center_y, coin_center_x + 2),
        (coin_center_y + 1, coin_center_x - 1),
        (coin_center_y + 1, coin_center_x),
        (coin_center_y + 1, coin_center_x + 1),
    ]
    
    for coin_y, coin_x in coin_positions:
        if 0 <= coin_y < size and 0 <= coin_x < size:
            canvas[coin_y][coin_x] = GOLD
    
    # Coin highlight
    canvas[coin_center_y][coin_center_x - 1] = LIGHT_GOLD
    canvas[coin_center_y - 1][coin_center_x] = LIGHT_GOLD
    
    # Coin shading
    canvas[coin_center_y][coin_center_x + 1] = DARK_GOLD
    canvas[coin_center_y + 1][coin_center_x] = DARK_GOLD
    
    # SPILLING COINS (money overflowing)
    # Coins near the pouch
    spilled_coins = [
        # Coin 1 (bottom right)
        [(pouch_bottom_y + 2, pouch_center_x + 4),
         (pouch_bottom_y + 2, pouch_center_x + 5),
         (pouch_bottom_y + 3, pouch_center_x + 3),
         (pouch_bottom_y + 3, pouch_center_x + 4),
         (pouch_bottom_y + 3, pouch_center_x + 5),
         (pouch_bottom_y + 3, pouch_center_x + 6),
         (pouch_bottom_y + 4, pouch_center_x + 4),
         (pouch_bottom_y + 4, pouch_center_x + 5)],
        
        # Coin 2 (bottom left, silver)
        [(pouch_bottom_y + 1, pouch_center_x - 5),
         (pouch_bottom_y + 1, pouch_center_x - 4),
         (pouch_bottom_y + 2, pouch_center_x - 6),
         (pouch_bottom_y + 2, pouch_center_x - 5),
         (pouch_bottom_y + 2, pouch_center_x - 4),
         (pouch_bottom_y + 2, pouch_center_x - 3),
         (pouch_bottom_y + 3, pouch_center_x - 5),
         (pouch_bottom_y + 3, pouch_center_x - 4)],
    ]
    
    # Draw gold coin
    for coin_y, coin_x in spilled_coins[0]:
        if 0 <= coin_y < size and 0 <= coin_x < size:
            canvas[coin_y][coin_x] = GOLD
    
    # Draw silver coin
    for coin_y, coin_x in spilled_coins[1]:
        if 0 <= coin_y < size and 0 <= coin_x < size:
            canvas[coin_y][coin_x] = SILVER
    
    # Coin highlights
    canvas[pouch_bottom_y + 3][pouch_center_x + 4] = LIGHT_GOLD  # Gold coin
    canvas[pouch_bottom_y + 2][pouch_center_x - 4] = WHITE       # Silver coin
    
    # MAGICAL EFFECTS (miser magic)
    # Purple aura around the pouch (money protection magic)
    aura_positions = [
        (pouch_top_y - 2, pouch_center_x - 3),
        (pouch_top_y + 2, pouch_center_x - 8),
        (pouch_top_y + 8, pouch_center_x + 8),
        (pouch_top_y + 12, pouch_center_x - 9),
        (pouch_top_y + 16, pouch_center_x + 9),
        (pouch_bottom_y - 2, pouch_center_x - 7),
    ]
    
    for aura_y, aura_x in aura_positions:
        if 0 <= aura_y < size and 0 <= aura_x < size:
            canvas[aura_y][aura_x] = PURPLE
    
    # Green sparkles (money magic)
    sparkle_positions = [
        (pouch_top_y - 3, pouch_center_x + 2),
        (pouch_top_y + 4, pouch_center_x - 6),
        (pouch_top_y + 10, pouch_center_x + 7),
        (pouch_top_y + 14, pouch_center_x - 8),
        (pouch_bottom_y + 1, pouch_center_x - 2),
        (pouch_bottom_y + 1, pouch_center_x + 2),
    ]
    
    for sparkle_y, sparkle_x in sparkle_positions:
        if 0 <= sparkle_y < size and 0 <= sparkle_x < size:
            canvas[sparkle_y][sparkle_x] = GREEN
    
    # Golden glow effects (wealth protection)
    glow_positions = [
        (pouch_top_y + 3, pouch_center_x - 5),
        (pouch_top_y + 9, pouch_center_x + 6),
        (pouch_top_y + 15, pouch_center_x - 6),
        (pouch_bottom_y - 1, pouch_center_x + 5),
    ]
    
    for glow_y, glow_x in glow_positions:
        if 0 <= glow_y < size and 0 <= glow_x < size:
            canvas[glow_y][glow_x] = YELLOW
    
    # POUCH TEXTURE DETAILS
    # Leather stitching pattern
    stitch_y = pouch_top_y + 8
    for x in range(pouch_center_x - 4, pouch_center_x + 5, 2):
        if 0 <= x < size:
            canvas[stitch_y][x] = DARK_BROWN
    
    # Metal buckle/clasp
    buckle_y = pouch_top_y + 4
    buckle_x = pouch_center_x - 2
    canvas[buckle_y][buckle_x] = SILVER
    canvas[buckle_y][buckle_x + 1] = WHITE
    
    # ROPE DETAILS
    # Drawstring knots
    canvas[drawstring_y - 2][pouch_center_x - 2] = ROPE
    canvas[drawstring_y - 2][pouch_center_x + 2] = ROPE
    canvas[drawstring_y - 3][pouch_center_x - 2] = DARK_ROPE
    canvas[drawstring_y - 3][pouch_center_x + 2] = DARK_ROPE
    
    # FINAL MAGICAL TOUCHES
    # Protective ward symbols (small magical marks)
    ward_positions = [
        (pouch_top_y + 12, pouch_center_x - 3),
        (pouch_top_y + 18, pouch_center_x + 2),
    ]
    
    for ward_y, ward_x in ward_positions:
        if 0 <= ward_y < size and 0 <= ward_x < size:
            canvas[ward_y][ward_x] = MAGENTA
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = '../art/magic_pouch.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art magic coin pouch with mystical protection")
    print(f"   Features: Leather bag, drawstring top, spilling coins")
    print(f"   Details: Embossed gold coin, metal buckle, leather stitching")
    print(f"   Magic: Purple aura, green sparkles, protective wards")
    print(f"   Theme: Wealth protection and money preservation magic")

if __name__ == '__main__':
    create_magic_pouch()