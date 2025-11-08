from PIL import Image, ImageDraw
import random

def create_fantasy_shop_background(width=512, height=256, scale_factor=8):
    """Create a pixel art fantasy shop background"""
    
    # Create base image at lower resolution for pixel art effect
    base_width = width // scale_factor
    base_height = height // scale_factor
    img = Image.new('RGB', (base_width, base_height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Color palette for fantasy shop
    colors = {
        'wall': (101, 67, 33),           # Dark brown wood
        'wall_light': (139, 90, 43),     # Lighter brown wood
        'floor': (83, 53, 10),           # Dark wood floor
        'floor_light': (101, 67, 33),    # Lighter wood floor
        'counter': (160, 100, 40),       # Counter wood
        'counter_top': (180, 120, 60),   # Counter top
        'shelf': (120, 80, 40),          # Shelf wood
        'shelf_light': (140, 100, 50),   # Lighter shelf
        'potion_red': (200, 50, 50),     # Red potion
        'potion_blue': (50, 100, 200),   # Blue potion
        'potion_green': (50, 200, 100),  # Green potion
        'potion_purple': (150, 50, 200), # Purple potion
        'bottle': (220, 220, 220),       # Glass bottle
        'gold': (255, 215, 0),           # Gold coins/items
        'silver': (192, 192, 192),       # Silver items
        'weapon': (100, 100, 100),       # Metal weapons
        'rope': (139, 115, 85),          # Rope/string
        'candle': (255, 255, 150),       # Candle flame
        'wax': (245, 245, 220),          # Candle wax
        'shadow': (40, 25, 5),           # Shadow areas
        'barrel': (101, 67, 33),         # Barrel wood
        'barrel_metal': (80, 80, 80),    # Barrel metal bands
    }
    
    # Fill background with wall color
    draw.rectangle([0, 0, base_width, base_height], fill=colors['wall'])
    
    # Create wood plank texture on walls
    for y in range(0, base_height, 4):
        # Alternate light and dark planks
        plank_color = colors['wall_light'] if (y // 4) % 2 == 0 else colors['wall']
        draw.rectangle([0, y, base_width, y + 3], fill=plank_color)
        # Add wood grain lines
        for x in range(2, base_width, 8):
            draw.point((x, y + 1), fill=colors['shadow'])
    
    # Create stone floor
    floor_start_y = base_height - 12
    for y in range(floor_start_y, base_height):
        draw.rectangle([0, y, base_width, y], fill=colors['floor'])
        if y % 2 == 0:
            for x in range(0, base_width, 8):
                draw.rectangle([x, y, x + 7, y], fill=colors['floor_light'])
    
    # Create merchant counter (bottom right)
    counter_x = base_width - 20
    counter_y = floor_start_y - 8
    counter_width = 20
    counter_height = 8
    
    # Counter base
    draw.rectangle([counter_x, counter_y, counter_x + counter_width, counter_y + counter_height], 
                  fill=colors['counter'])
    # Counter top
    draw.rectangle([counter_x, counter_y, counter_x + counter_width, counter_y + 1], 
                  fill=colors['counter_top'])
    
    # Add coins on counter
    for i in range(3):
        coin_x = counter_x + 2 + i * 4
        coin_y = counter_y - 1
        draw.ellipse([coin_x, coin_y, coin_x + 2, coin_y + 1], fill=colors['gold'])
    
    # Create wall shelves (left side)
    shelf_positions = [
        (2, 8, 16, 3),   # Top shelf
        (2, 16, 16, 3),  # Middle shelf
        (2, 24, 16, 3),  # Bottom shelf
    ]
    
    for shelf_x, shelf_y, shelf_w, shelf_h in shelf_positions:
        # Shelf base
        draw.rectangle([shelf_x, shelf_y, shelf_x + shelf_w, shelf_y + shelf_h], 
                      fill=colors['shelf'])
        # Shelf top highlight
        draw.rectangle([shelf_x, shelf_y, shelf_x + shelf_w, shelf_y + 1], 
                      fill=colors['shelf_light'])
        # Shelf shadow
        draw.rectangle([shelf_x, shelf_y + shelf_h - 1, shelf_x + shelf_w, shelf_y + shelf_h], 
                      fill=colors['shadow'])
    
    # Add potions on shelves
    potion_colors = [colors['potion_red'], colors['potion_blue'], colors['potion_green'], colors['potion_purple']]
    
    # Top shelf potions
    for i in range(4):
        potion_x = 4 + i * 3
        potion_y = 4
        # Bottle
        draw.rectangle([potion_x, potion_y, potion_x + 2, potion_y + 4], fill=colors['bottle'])
        # Potion liquid
        draw.rectangle([potion_x, potion_y + 1, potion_x + 2, potion_y + 3], 
                      fill=potion_colors[i % len(potion_colors)])
        # Cork
        draw.rectangle([potion_x, potion_y, potion_x + 2, potion_y], fill=colors['barrel'])
    
    # Middle shelf - weapons and tools
    weapon_positions = [(4, 12), (8, 12), (12, 12), (15, 12)]
    for i, (wx, wy) in enumerate(weapon_positions):
        if i % 2 == 0:
            # Sword
            draw.rectangle([wx, wy, wx + 1, wy + 4], fill=colors['weapon'])
            draw.rectangle([wx, wy + 4, wx + 1, wy + 5], fill=colors['barrel'])  # Handle
        else:
            # Staff/wand
            draw.rectangle([wx, wy, wx, wy + 4], fill=colors['barrel'])
            draw.point((wx, wy), fill=colors['gold'])  # Magical tip
    
    # Bottom shelf - books and scrolls
    for i in range(5):
        book_x = 3 + i * 2
        book_y = 20
        book_colors = [colors['potion_red'], colors['potion_blue'], colors['barrel'], colors['potion_green']]
        draw.rectangle([book_x, book_y, book_x + 1, book_y + 3], 
                      fill=book_colors[i % len(book_colors)])
    
    # Create hanging items (right side)
    for i in range(3):
        rope_x = base_width - 15 + i * 4
        rope_y = 4
        # Rope
        draw.line([rope_x, rope_y, rope_x, rope_y + 6], fill=colors['rope'])
        # Hanging item
        if i == 0:
            # Lantern
            draw.rectangle([rope_x - 1, rope_y + 6, rope_x + 1, rope_y + 9], fill=colors['weapon'])
            draw.point((rope_x, rope_y + 7), fill=colors['candle'])
        elif i == 1:
            # Shield
            draw.ellipse([rope_x - 1, rope_y + 6, rope_x + 2, rope_y + 9], fill=colors['silver'])
        else:
            # Herbs/dried goods
            draw.rectangle([rope_x - 1, rope_y + 6, rope_x + 1, rope_y + 8], fill=colors['potion_green'])
    
    # Add barrels in corner
    barrel_positions = [(base_width - 10, floor_start_y - 6), (base_width - 6, floor_start_y - 6)]
    for barrel_x, barrel_y in barrel_positions:
        # Barrel body
        draw.ellipse([barrel_x, barrel_y, barrel_x + 4, barrel_y + 6], fill=colors['barrel'])
        # Metal bands
        draw.rectangle([barrel_x, barrel_y + 1, barrel_x + 4, barrel_y + 2], fill=colors['barrel_metal'])
        draw.rectangle([barrel_x, barrel_y + 4, barrel_x + 4, barrel_y + 5], fill=colors['barrel_metal'])
    
    # Add candles for ambient lighting
    candle_positions = [(20, 6), (base_width - 25, 10)]
    for candle_x, candle_y in candle_positions:
        # Candle base
        draw.rectangle([candle_x, candle_y + 2, candle_x + 1, candle_y + 6], fill=colors['wax'])
        # Flame
        draw.point((candle_x, candle_y), fill=colors['candle'])
        draw.point((candle_x, candle_y + 1), fill=colors['potion_red'])
    
    # Add some ambient details
    # Cobwebs in corners
    web_points = [(1, 1), (base_width - 2, 2)]
    for web_x, web_y in web_points:
        draw.point((web_x, web_y), fill=colors['silver'])
        draw.point((web_x + 1, web_y + 1), fill=colors['silver'])
    
    # Add some scattered coins on floor
    for i in range(5):
        coin_x = random.randint(5, base_width - 10)
        coin_y = floor_start_y + random.randint(2, 8)
        draw.point((coin_x, coin_y), fill=colors['gold'])
    
    # Scale up the image for final output
    img_scaled = img.resize((width, height), Image.Resampling.NEAREST)
    
    return img_scaled

def main():
    """Create and save the fantasy shop background"""
    print("Creating fantasy shop background...")
    
    # Create the background image
    shop_bg = create_fantasy_shop_background(512, 256, 8)
    
    # Save the image
    output_path = "../art/shop_background.png"
    shop_bg.save(output_path)
    print(f"Fantasy shop background saved to: {output_path}")
    
    # Also create a larger version for high-res displays
    shop_bg_large = create_fantasy_shop_background(1024, 512, 8)
    output_path_large = "../art/shop_background_large.png"
    shop_bg_large.save(output_path_large)
    print(f"Large fantasy shop background saved to: {output_path_large}")
    
    print("Fantasy shop background creation complete!")
    print("\nFeatures created:")
    print("- Wood plank walls with texture")
    print("- Stone tile floor")
    print("- Wall-mounted shelves with potions, weapons, and books")
    print("- Merchant counter with gold coins")
    print("- Hanging items (lantern, shield, herbs)")
    print("- Storage barrels")
    print("- Ambient candle lighting")
    print("- Atmospheric details (cobwebs, scattered coins)")

if __name__ == "__main__":
    main()