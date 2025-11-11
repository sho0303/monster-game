from PIL import Image, ImageDraw
import random

def create_tavern_background(width=800, height=400, scale_factor=8):
    """Create a pixel art medieval tavern background"""
    
    # Create base image at lower resolution for pixel art effect
    base_width = width // scale_factor
    base_height = height // scale_factor
    img = Image.new('RGB', (base_width, base_height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Color palette for medieval tavern
    colors = {
        'wall_wood': (101, 67, 33),          # Dark wood walls
        'wall_wood_light': (139, 115, 85),   # Lighter wood planks
        'floor_wood': (83, 53, 10),          # Dark wood floor
        'floor_wood_light': (101, 67, 33),   # Lighter floor planks
        'stone_hearth': (80, 80, 90),        # Stone fireplace
        'stone_light': (100, 100, 110),      # Light stone
        'fire_orange': (255, 140, 0),        # Fire orange
        'fire_red': (255, 69, 0),            # Fire red
        'fire_yellow': (255, 255, 100),      # Fire yellow core
        'ember': (200, 100, 50),             # Glowing embers
        'barrel_wood': (139, 115, 85),       # Wooden barrels
        'barrel_dark': (101, 67, 33),        # Barrel shading
        'metal_band': (100, 100, 100),       # Metal barrel bands
        'beer_amber': (255, 191, 0),         # Beer/ale color
        'foam_white': (255, 255, 255),       # Beer foam
        'mug_clay': (160, 82, 45),           # Clay mugs
        'mug_pewter': (120, 120, 120),       # Pewter tankards
        'table_wood': (139, 115, 85),        # Table wood
        'chair_wood': (101, 67, 33),         # Chair wood
        'rope': (139, 115, 85),              # Rope/hemp
        'leather': (101, 67, 33),            # Leather items
        'candlelight': (255, 255, 200),      # Candle flame
        'wax': (255, 248, 220),              # Candle wax
        'shadow': (20, 15, 10),              # Shadow areas
        'beam_wood': (83, 53, 10),           # Support beams
        'lantern_metal': (150, 150, 100),    # Brass lantern
        'glass_green': (100, 150, 100),      # Green bottles
        'cork': (160, 82, 45),               # Bottle corks
        'smoke': (180, 180, 180),            # Pipe smoke
        'cloth_red': (139, 0, 0),            # Red cloth/banner
        'cloth_blue': (25, 25, 112),         # Blue cloth
    }
    
    # Fill background with wood wall
    draw.rectangle([0, 0, base_width, base_height], fill=colors['wall_wood'])
    
    # Create wood plank wall texture
    for y in range(0, base_height, 2):
        for x in range(0, base_width):
            # Alternate wood grain
            if y % 4 == 0:
                draw.rectangle([x, y, x, y + 1], fill=colors['wall_wood_light'])
            # Wood plank lines
            if x % 8 == 0:
                draw.line([x, y, x, y + 1], fill=colors['shadow'])
    
    # Create wood plank floor
    floor_start_y = base_height - 8
    for y in range(floor_start_y, base_height):
        draw.rectangle([0, y, base_width, y], fill=colors['floor_wood'])
        # Wood plank pattern
        for x in range(0, base_width, 6):
            if (x // 6 + y) % 2 == 0:
                draw.rectangle([x, y, x + 5, y], fill=colors['floor_wood_light'])
            # Plank separations
            draw.line([x + 5, y, x + 5, y], fill=colors['shadow'])
    
    # Create fireplace (left side, moved slightly left to make room for centered bar)
    hearth_x = 1
    hearth_y = floor_start_y - 14
    hearth_width = 10
    hearth_height = 14
    
    # Fireplace stone structure
    draw.rectangle([hearth_x, hearth_y, hearth_x + hearth_width, hearth_y + hearth_height], 
                  fill=colors['stone_hearth'])
    
    # Stone brick pattern
    for y in range(hearth_y, hearth_y + hearth_height, 2):
        for x in range(hearth_x, hearth_x + hearth_width, 3):
            if (x // 3 + y // 2) % 2 == 0:
                draw.rectangle([x, y, x + 2, y + 1], fill=colors['stone_light'])
    
    # Fire in fireplace
    fire_x = hearth_x + 4
    fire_y = hearth_y + 8
    fire_width = 4
    fire_height = 6
    
    # Fire logs/wood
    draw.rectangle([fire_x, fire_y + 3, fire_x + fire_width, fire_y + fire_height], 
                  fill=colors['beam_wood'])
    
    # Fire flames
    flame_points = [
        (fire_x + 1, fire_y + 2, colors['fire_red']),
        (fire_x + 2, fire_y + 1, colors['fire_orange']),
        (fire_x + 3, fire_y, colors['fire_yellow']),
        (fire_x + 2, fire_y, colors['fire_yellow']),
        (fire_x + 1, fire_y + 1, colors['fire_orange']),
    ]
    
    for fx, fy, color in flame_points:
        if fy >= 0:
            draw.point((fx, fy), fill=color)
            draw.point((fx, fy + 1), fill=color)
    
    # Glowing embers
    ember_points = [(fire_x + 1, fire_y + 3), (fire_x + 3, fire_y + 4)]
    for ex, ey in ember_points:
        draw.point((ex, ey), fill=colors['ember'])
    
    # Smoke rising from fireplace
    smoke_points = [(fire_x + 2, fire_y - 2), (fire_x + 3, fire_y - 4), (fire_x + 4, fire_y - 6)]
    for sx, sy in smoke_points:
        if sy >= 0:
            draw.point((sx, sy), fill=colors['smoke'])
    
    # Bar counter (centered and doubled in size)
    bar_width = 48  # Doubled from 24
    bar_height = 12  # Doubled from 6
    bar_x = (base_width - bar_width) // 2  # Center the bar
    bar_y = floor_start_y - bar_height
    
    # Bar counter surface (doubled size)
    draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + 4], fill=colors['table_wood'])
    # Bar front with decorative panel
    draw.rectangle([bar_x, bar_y + 4, bar_x + bar_width, bar_y + bar_height], fill=colors['chair_wood'])
    
    # Decorative bar front pattern (scaled for larger bar)
    for i in range(0, bar_width, 8):
        draw.rectangle([bar_x + i + 2, bar_y + 6, bar_x + i + 6, bar_y + 10], fill=colors['table_wood'])
    
    # Bar stools (scaled for doubled bar size)
    stool_positions = [(bar_x + 4, bar_y + 8), (bar_x + 12, bar_y + 8), (bar_x + 20, bar_y + 8), (bar_x + 28, bar_y + 8), (bar_x + 36, bar_y + 8), (bar_x + 44, bar_y + 8)]
    for stool_x, stool_y in stool_positions:
        # Stool top (doubled size)
        draw.rectangle([stool_x, stool_y, stool_x + 6, stool_y + 2], fill=colors['table_wood'])
        # Stool leg (doubled size)
        draw.rectangle([stool_x + 2, stool_y + 2, stool_x + 4, stool_y + 4], fill=colors['chair_wood'])
    
    # Barrels behind bar (scaled and repositioned for doubled bar)
    barrel_positions = [(bar_x + 2, bar_y - 16), (bar_x + 10, bar_y - 16), (bar_x + 18, bar_y - 16), (bar_x + 30, bar_y - 16), (bar_x + 38, bar_y - 16), (bar_x + 46, bar_y - 16)]
    for barrel_x, barrel_y in barrel_positions:
        # Barrel body (doubled size)
        draw.ellipse([barrel_x, barrel_y, barrel_x + 8, barrel_y + 16], fill=colors['barrel_wood'])
        # Metal bands (doubled size)
        draw.rectangle([barrel_x, barrel_y + 4, barrel_x + 8, barrel_y + 6], fill=colors['metal_band'])
        draw.rectangle([barrel_x, barrel_y + 10, barrel_x + 8, barrel_y + 12], fill=colors['metal_band'])
        # Barrel tap (doubled size)
        draw.rectangle([barrel_x + 8, barrel_y + 7, barrel_x + 10, barrel_y + 9], fill=colors['metal_band'])
    
    # Mugs and tankards on bar (scaled for doubled bar)
    mug_positions = [
        (bar_x + 6, bar_y - 4, colors['mug_clay']),
        (bar_x + 14, bar_y - 4, colors['mug_pewter']),
        (bar_x + 22, bar_y - 4, colors['mug_clay']),
        (bar_x + 30, bar_y - 4, colors['mug_pewter']),
        (bar_x + 38, bar_y - 4, colors['mug_clay']),
        (bar_x + 46, bar_y - 4, colors['mug_pewter']),
    ]
    
    for mug_x, mug_y, mug_color in mug_positions:
        # Mug body (doubled size)
        draw.rectangle([mug_x, mug_y, mug_x + 4, mug_y + 4], fill=mug_color)
        # Beer foam (doubled size)
        draw.rectangle([mug_x, mug_y - 2, mug_x + 4, mug_y], fill=colors['foam_white'])
        # Beer (doubled size)
        draw.rectangle([mug_x, mug_y + 2, mug_x + 4, mug_y + 4], fill=colors['beer_amber'])
    
    # Hanging lantern (center ceiling)
    lantern_x = base_width // 2
    lantern_y = 4
    
    # Lantern chain
    draw.line([lantern_x, 0, lantern_x, lantern_y], fill=colors['metal_band'])
    # Lantern body
    draw.rectangle([lantern_x - 1, lantern_y, lantern_x + 1, lantern_y + 3], fill=colors['lantern_metal'])
    # Lantern light
    draw.point((lantern_x, lantern_y + 1), fill=colors['candlelight'])
    draw.point((lantern_x, lantern_y + 2), fill=colors['fire_yellow'])
    
    # Bottle shelf (right wall)
    shelf_x = base_width - 12
    shelf_y = 8
    shelf_width = 10
    
    # Shelf
    draw.rectangle([shelf_x, shelf_y, shelf_x + shelf_width, shelf_y + 1], fill=colors['table_wood'])
    
    # Bottles on shelf
    bottle_positions = [
        (shelf_x + 1, shelf_y - 4, colors['glass_green']),
        (shelf_x + 3, shelf_y - 5, colors['glass_green']),
        (shelf_x + 5, shelf_y - 4, colors['glass_green']),
        (shelf_x + 7, shelf_y - 5, colors['glass_green']),
        (shelf_x + 9, shelf_y - 4, colors['glass_green']),
    ]
    
    for bottle_x, bottle_y, bottle_color in bottle_positions:
        # Bottle body
        draw.rectangle([bottle_x, bottle_y, bottle_x + 1, bottle_y + 4], fill=bottle_color)
        # Cork
        draw.point((bottle_x, bottle_y - 1), fill=colors['cork'])
    
    # Bartender behind the bar (doubled size and centered)
    bartender_x = bar_x + bar_width // 2 - 4  # Center the bartender in the doubled bar
    bartender_y = bar_y - 24  # Adjust for doubled size
    
    # Bartender colors
    bartender_colors = {
        'skin': (255, 220, 177),
        'hair': (139, 69, 19),
        'shirt': (100, 149, 237),
        'apron': (255, 248, 220),
        'pants': (101, 67, 33),
    }
    
    # Bartender head (doubled size)
    draw.rectangle([bartender_x + 2, bartender_y, bartender_x + 6, bartender_y + 4], fill=bartender_colors['skin'])
    
    # Bartender hair (doubled size)
    draw.rectangle([bartender_x + 2, bartender_y - 2, bartender_x + 6, bartender_y], fill=bartender_colors['hair'])
    
    # Bartender eyes (doubled size)
    draw.rectangle([bartender_x + 2, bartender_y + 2, bartender_x + 3, bartender_y + 3], fill=colors['shadow'])
    draw.rectangle([bartender_x + 5, bartender_y + 2, bartender_x + 6, bartender_y + 3], fill=colors['shadow'])
    
    # Bartender body (shirt) (doubled size)
    draw.rectangle([bartender_x, bartender_y + 4, bartender_x + 8, bartender_y + 12], fill=bartender_colors['shirt'])
    
    # Bartender apron (doubled size)
    draw.rectangle([bartender_x + 2, bartender_y + 6, bartender_x + 6, bartender_y + 14], fill=bartender_colors['apron'])
    
    # Bartender arms (doubled size)
    draw.rectangle([bartender_x - 2, bartender_y + 6, bartender_x, bartender_y + 10], fill=bartender_colors['skin'])  # Left arm
    draw.rectangle([bartender_x + 8, bartender_y + 6, bartender_x + 10, bartender_y + 10], fill=bartender_colors['skin'])  # Right arm
    
    # Bartender legs (doubled size)
    draw.rectangle([bartender_x + 2, bartender_y + 14, bartender_x + 4, bartender_y + 20], fill=bartender_colors['pants'])
    draw.rectangle([bartender_x + 4, bartender_y + 14, bartender_x + 6, bartender_y + 20], fill=bartender_colors['pants'])
    
    # Bartender holding a mug (left hand) (doubled size)
    mug_x = bartender_x - 4
    mug_y = bartender_y + 8
    draw.rectangle([mug_x, mug_y, mug_x + 3, mug_y + 4], fill=colors['mug_pewter'])
    draw.rectangle([mug_x, mug_y - 2, mug_x + 3, mug_y], fill=colors['foam_white'])
    
    # Bartender rag (right hand) (doubled size)
    draw.rectangle([bartender_x + 10, bartender_y + 8, bartender_x + 12, bartender_y + 10], fill=colors['cloth_red'])
    
    # Wall decorations
    # Banner/tapestry (left wall)
    banner_x = hearth_x + hearth_width + 2
    banner_y = 6
    banner_width = 6
    banner_height = 8
    
    # Banner fabric
    draw.rectangle([banner_x, banner_y, banner_x + banner_width, banner_y + banner_height], 
                  fill=colors['cloth_red'])
    # Banner pole
    draw.rectangle([banner_x, banner_y - 2, banner_x + banner_width, banner_y], fill=colors['beam_wood'])
    # Banner design (simple cross)
    draw.line([banner_x + 2, banner_y + 2, banner_x + 4, banner_y + 2], fill=colors['cloth_blue'])
    draw.line([banner_x + 3, banner_y + 1, banner_x + 3, banner_y + 3], fill=colors['cloth_blue'])
    
    # Wooden beam supports
    beam_positions = [(8, 0, 1, base_height//2), (32, 0, 1, base_height//2), (48, 0, 1, base_height//2)]
    for beam_x, beam_y, beam_w, beam_h in beam_positions:
        draw.rectangle([beam_x, beam_y, beam_x + beam_w, beam_y + beam_h], fill=colors['beam_wood'])
    
    # Candlesticks around the room
    candle_positions = [(16, floor_start_y - 12), (44, floor_start_y - 10)]
    for candle_x, candle_y in candle_positions:
        # Candle base
        draw.rectangle([candle_x, candle_y + 2, candle_x + 1, candle_y + 4], fill=colors['lantern_metal'])
        # Candle
        draw.rectangle([candle_x, candle_y, candle_x + 1, candle_y + 2], fill=colors['wax'])
        # Flame
        draw.point((candle_x, candle_y - 1), fill=colors['candlelight'])
    
    # Fireplace glow effects
    glow_areas = [
        (hearth_x - 1, hearth_y + 10, 2, 4),  # Left wall glow
        (hearth_x + hearth_width, hearth_y + 12, 6, 2),  # Floor glow
    ]
    
    for gx, gy, gw, gh in glow_areas:
        if gx >= 0 and gy >= 0 and gx + gw < base_width and gy + gh < base_height:
            # Subtle orange glow
            for dx in range(gw):
                for dy in range(gh):
                    current_pixel = img.getpixel((gx + dx, gy + dy))
                    glow_pixel = (
                        min(255, current_pixel[0] + 30),
                        min(255, current_pixel[1] + 15),
                        current_pixel[2]
                    )
                    img.putpixel((gx + dx, gy + dy), glow_pixel)
    
    # Scale up the image for final output
    img_scaled = img.resize((width, height), Image.Resampling.NEAREST)
    
    return img_scaled

def main():
    """Create and save the tavern background"""
    print("Creating medieval tavern background...")
    
    # Create the background image at the correct canvas size
    tavern_bg = create_tavern_background(800, 400, 8)
    
    # Save the image
    output_path = "art/tavern_background.png"
    tavern_bg.save(output_path)
    print(f"Tavern background saved to: {output_path}")
    
    # Also create a larger version for high-res displays
    tavern_bg_large = create_tavern_background(1600, 800, 8)
    output_path_large = "art/tavern_background_large.png"
    tavern_bg_large.save(output_path_large)
    print(f"Large tavern background saved to: {output_path_large}")
    
    print("Tavern background creation complete!")
    print("\nFeatures created:")
    print("- Wooden plank walls and floors")
    print("- Stone fireplace with active fire")
    print("- Expanded bar counter with decorative panels")
    print("- Friendly bartender behind the bar")
    print("- Wooden barrels and bar stools")
    print("- Multiple drinking mugs with foam")
    print("- Hanging lantern with warm light")
    print("- Bottle shelf with green glass bottles")
    print("- Wall banner/tapestry decoration")
    print("- Wooden support beams")
    print("- Candlesticks for ambient lighting")
    print("- Fireplace glow effects")
    print("- Authentic medieval tavern atmosphere")

if __name__ == "__main__":
    main()