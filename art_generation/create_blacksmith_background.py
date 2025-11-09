from PIL import Image, ImageDraw
import random

def create_blacksmith_background(width=512, height=256, scale_factor=8):
    """Create a pixel art medieval blacksmith background"""
    
    # Create base image at lower resolution for pixel art effect
    base_width = width // scale_factor
    base_height = height // scale_factor
    img = Image.new('RGB', (base_width, base_height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Color palette for medieval blacksmith
    colors = {
        'wall_stone': (80, 80, 90),          # Dark stone walls
        'wall_stone_light': (100, 100, 110), # Lighter stone
        'floor_stone': (60, 60, 70),         # Stone floor
        'floor_stone_light': (75, 75, 85),   # Lighter floor stones
        'forge': (40, 20, 20),               # Dark forge base
        'forge_brick': (120, 60, 40),        # Forge bricks
        'fire_orange': (255, 140, 0),        # Fire orange
        'fire_red': (255, 69, 0),            # Fire red
        'fire_yellow': (255, 255, 100),      # Fire yellow core
        'coal': (30, 30, 30),                # Coal/charcoal
        'metal_iron': (100, 100, 100),       # Iron tools
        'metal_steel': (150, 150, 150),      # Steel/bright metal
        'metal_hot': (255, 100, 100),        # Hot glowing metal
        'anvil': (80, 80, 80),               # Anvil dark metal
        'anvil_top': (120, 120, 120),        # Anvil top surface
        'hammer_wood': (139, 115, 85),       # Hammer handle wood
        'hammer_head': (90, 90, 90),         # Hammer head
        'barrel_water': (40, 80, 120),       # Water barrel
        'steam': (220, 220, 220),            # Steam/smoke
        'rope': (139, 115, 85),              # Rope
        'leather': (101, 67, 33),            # Leather apron/bellows
        'chain': (110, 110, 110),            # Chains
        'spark': (255, 255, 0),              # Flying sparks
        'shadow': (20, 20, 25),              # Shadow areas
        'wood_beam': (101, 67, 33),          # Wood support beams
        'bellows': (80, 50, 30),             # Bellows leather
    }
    
    # Fill background with stone wall
    draw.rectangle([0, 0, base_width, base_height], fill=colors['wall_stone'])
    
    # Create stone wall texture
    for y in range(0, base_height, 3):
        for x in range(0, base_width, 6):
            # Alternate stone blocks
            if (x // 6 + y // 3) % 2 == 0:
                draw.rectangle([x, y, x + 5, y + 2], fill=colors['wall_stone_light'])
            # Add mortar lines
            draw.line([x + 5, y, x + 5, y + 2], fill=colors['shadow'])
            draw.line([x, y + 2, x + 5, y + 2], fill=colors['shadow'])
    
    # Create stone floor
    floor_start_y = base_height - 10
    for y in range(floor_start_y, base_height):
        draw.rectangle([0, y, base_width, y], fill=colors['floor_stone'])
        # Stone tile pattern
        for x in range(0, base_width, 4):
            if (x // 4 + y) % 2 == 0:
                draw.rectangle([x, y, x + 3, y], fill=colors['floor_stone_light'])
    
    # Create the forge (left side)
    forge_x = 4
    forge_y = floor_start_y - 12
    forge_width = 16
    forge_height = 12
    
    # Forge base structure
    draw.rectangle([forge_x, forge_y, forge_x + forge_width, forge_y + forge_height], 
                  fill=colors['forge'])
    
    # Forge brick pattern
    for y in range(forge_y, forge_y + forge_height - 4, 2):
        for x in range(forge_x, forge_x + forge_width, 3):
            draw.rectangle([x, y, x + 2, y + 1], fill=colors['forge_brick'])
    
    # Fire in forge
    fire_x = forge_x + 6
    fire_y = forge_y + 2
    fire_width = 6
    fire_height = 4
    
    # Fire base (coal)
    draw.rectangle([fire_x, fire_y + 2, fire_x + fire_width, fire_y + fire_height], 
                  fill=colors['coal'])
    
    # Fire flames
    flame_points = [
        (fire_x + 1, fire_y + 1, colors['fire_red']),
        (fire_x + 2, fire_y, colors['fire_orange']),
        (fire_x + 3, fire_y - 1, colors['fire_yellow']),
        (fire_x + 4, fire_y, colors['fire_orange']),
        (fire_x + 5, fire_y + 1, colors['fire_red']),
    ]
    
    for fx, fy, color in flame_points:
        if fy >= 0:
            draw.point((fx, fy), fill=color)
            draw.point((fx, fy + 1), fill=color)
    
    # Glowing hot metal in forge
    draw.rectangle([fire_x + 2, fire_y + 2, fire_x + 4, fire_y + 3], fill=colors['metal_hot'])
    
    # Smoke/steam rising from forge
    smoke_points = [(fire_x + 2, fire_y - 3), (fire_x + 4, fire_y - 4), (fire_x + 3, fire_y - 5)]
    for sx, sy in smoke_points:
        if sy >= 0:
            draw.point((sx, sy), fill=colors['steam'])
    
    # Create anvil (center)
    anvil_x = 25
    anvil_y = floor_start_y - 6
    
    # Anvil base
    draw.rectangle([anvil_x, anvil_y + 2, anvil_x + 6, anvil_y + 6], fill=colors['anvil'])
    # Anvil top surface
    draw.rectangle([anvil_x - 1, anvil_y, anvil_x + 7, anvil_y + 2], fill=colors['anvil_top'])
    # Anvil horn
    draw.rectangle([anvil_x + 6, anvil_y, anvil_x + 9, anvil_y + 1], fill=colors['anvil_top'])
    
    # Hammer on anvil
    hammer_x = anvil_x + 2
    hammer_y = anvil_y - 2
    # Hammer head
    draw.rectangle([hammer_x, hammer_y, hammer_x + 3, hammer_y + 1], fill=colors['hammer_head'])
    # Hammer handle
    draw.rectangle([hammer_x + 3, hammer_y, hammer_x + 7, hammer_y], fill=colors['hammer_wood'])
    
    # Hot metal being worked on anvil
    draw.rectangle([anvil_x + 1, anvil_y - 1, anvil_x + 2, anvil_y], fill=colors['metal_hot'])
    
    # Flying sparks around anvil
    spark_points = [(anvil_x - 2, anvil_y - 1), (anvil_x + 8, anvil_y - 2), (anvil_x + 3, anvil_y - 3)]
    for spx, spy in spark_points:
        if spy >= 0:
            draw.point((spx, spy), fill=colors['spark'])
    
    # Tool rack on wall (right side)
    rack_x = base_width - 18
    rack_y = 8
    
    # Horizontal tool rack beam
    draw.rectangle([rack_x, rack_y, rack_x + 14, rack_y + 1], fill=colors['wood_beam'])
    
    # Hanging tools
    tools = [
        # Tongs
        (rack_x + 2, rack_y + 2, colors['metal_iron']),
        # Hammers
        (rack_x + 5, rack_y + 2, colors['hammer_head']),
        (rack_x + 8, rack_y + 2, colors['hammer_head']),
        # Files
        (rack_x + 11, rack_y + 2, colors['metal_steel']),
    ]
    
    for tool_x, tool_y, tool_color in tools:
        # Hanging rope/chain
        draw.line([tool_x, rack_y + 1, tool_x, tool_y], fill=colors['chain'])
        # Tool
        draw.rectangle([tool_x - 1, tool_y, tool_x + 1, tool_y + 4], fill=tool_color)
    
    # Water barrel and quenching station (right side)
    barrel_x = base_width - 8
    barrel_y = floor_start_y - 8
    
    # Water barrel
    draw.ellipse([barrel_x, barrel_y, barrel_x + 6, barrel_y + 8], fill=colors['barrel_water'])
    # Metal bands on barrel
    draw.rectangle([barrel_x, barrel_y + 2, barrel_x + 6, barrel_y + 3], fill=colors['metal_iron'])
    draw.rectangle([barrel_x, barrel_y + 5, barrel_x + 6, barrel_y + 6], fill=colors['metal_iron'])
    
    # Steam rising from quenching
    steam_points = [(barrel_x + 2, barrel_y - 1), (barrel_x + 4, barrel_y - 2)]
    for stx, sty in steam_points:
        if sty >= 0:
            draw.point((stx, sty), fill=colors['steam'])
    
    # Bellows (next to forge)
    bellows_x = forge_x - 3
    bellows_y = forge_y + 6
    
    # Bellows body
    draw.polygon([(bellows_x, bellows_y), (bellows_x + 2, bellows_y - 2), 
                  (bellows_x + 4, bellows_y - 2), (bellows_x + 6, bellows_y)], 
                 fill=colors['bellows'])
    # Bellows handle
    draw.rectangle([bellows_x + 6, bellows_y - 1, bellows_x + 8, bellows_y], fill=colors['hammer_wood'])
    
    # Sword rack (left wall)
    sword_rack_x = 2
    sword_rack_y = 12
    
    # Rack
    draw.rectangle([sword_rack_x, sword_rack_y, sword_rack_x + 1, sword_rack_y + 8], fill=colors['wood_beam'])
    
    # Swords in various stages
    swords = [
        (sword_rack_x + 2, sword_rack_y + 1, colors['metal_steel']),      # Finished sword
        (sword_rack_x + 2, sword_rack_y + 3, colors['metal_iron']),       # Raw blade
        (sword_rack_x + 2, sword_rack_y + 5, colors['metal_hot']),        # Hot blade
    ]
    
    for sword_x, sword_y, sword_color in swords:
        # Blade
        draw.rectangle([sword_x, sword_y, sword_x + 8, sword_y], fill=sword_color)
        # Crossguard
        draw.rectangle([sword_x + 6, sword_y - 1, sword_x + 6, sword_y + 1], fill=colors['metal_iron'])
        # Handle
        draw.rectangle([sword_x + 7, sword_y, sword_x + 9, sword_y], fill=colors['hammer_wood'])
    
    # Workbench (bottom right)
    bench_x = base_width - 15
    bench_y = floor_start_y - 4
    
    # Bench surface
    draw.rectangle([bench_x, bench_y, bench_x + 12, bench_y + 4], fill=colors['wood_beam'])
    # Bench legs
    draw.rectangle([bench_x + 1, bench_y + 4, bench_x + 2, floor_start_y], fill=colors['wood_beam'])
    draw.rectangle([bench_x + 10, bench_y + 4, bench_x + 11, floor_start_y], fill=colors['wood_beam'])
    
    # Tools on workbench
    draw.rectangle([bench_x + 2, bench_y - 1, bench_x + 4, bench_y], fill=colors['hammer_head'])  # Small hammer
    draw.rectangle([bench_x + 6, bench_y - 1, bench_x + 7, bench_y], fill=colors['metal_steel'])   # File
    draw.rectangle([bench_x + 9, bench_y - 1, bench_x + 10, bench_y], fill=colors['metal_iron'])   # Punch
    
    # Coal pile (near forge)
    coal_x = forge_x + forge_width + 2
    coal_y = floor_start_y - 2
    
    for i in range(6):
        cx = coal_x + (i % 3)
        cy = coal_y - (i // 3)
        draw.point((cx, cy), fill=colors['coal'])
    
    # Ambient lighting effects
    # Forge glow on nearby surfaces
    glow_areas = [
        (forge_x - 2, forge_y + 4, 2, 4),  # Left wall glow
        (forge_x + forge_width, forge_y + 6, 4, 2),  # Floor glow
    ]
    
    for gx, gy, gw, gh in glow_areas:
        if gx >= 0 and gy >= 0:
            draw.rectangle([gx, gy, gx + gw, gy + gh], fill=colors['fire_red'])
    
    # Scale up the image for final output
    img_scaled = img.resize((width, height), Image.Resampling.NEAREST)
    
    return img_scaled

def main():
    """Create and save the blacksmith background"""
    print("Creating medieval blacksmith background...")
    
    # Create the background image
    blacksmith_bg = create_blacksmith_background(512, 256, 8)
    
    # Save the image
    output_path = "art/blacksmith_background.png"
    blacksmith_bg.save(output_path)
    print(f"Blacksmith background saved to: {output_path}")
    
    # Also create a larger version for high-res displays
    blacksmith_bg_large = create_blacksmith_background(1024, 512, 8)
    output_path_large = "art/blacksmith_background_large.png"
    blacksmith_bg_large.save(output_path_large)
    print(f"Large blacksmith background saved to: {output_path_large}")
    
    print("Blacksmith background creation complete!")
    print("\nFeatures created:")
    print("- Stone brick walls and floor")
    print("- Active forge with fire and hot metal")
    print("- Anvil with hammer and sparks")
    print("- Tool rack with hanging implements")
    print("- Water barrel for quenching")
    print("- Bellows for the forge")
    print("- Sword rack with blades in progress")
    print("- Workbench with small tools")
    print("- Coal pile and ambient forge lighting")
    print("- Steam and smoke effects")

if __name__ == "__main__":
    main()