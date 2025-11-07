"""
Create a pixel art golden armor PNG
"""
from PIL import Image, ImageDraw
import numpy as np

def create_golden_armor():
    """Create a Minecraft-style golden armor piece (chestplate)"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette (golden theme matching wizard staff style)
    GOLD = [255, 215, 0, 255]        # Main golden color
    DARK_GOLD = [184, 134, 11, 255]  # Gold shading
    LIGHT_GOLD = [255, 255, 100, 255] # Gold highlights
    BRONZE = [205, 127, 50, 255]     # Secondary metal
    DARK_BRONZE = [139, 69, 19, 255] # Bronze shading
    LIGHT_BRONZE = [222, 184, 135, 255] # Bronze highlights
    COPPER = [184, 115, 51, 255]     # Accent metal
    DARK_COPPER = [120, 80, 40, 255] # Copper shading
    SILVER = [192, 192, 192, 255]    # Metal trim
    DARK_SILVER = [128, 128, 128, 255] # Silver shading
    WHITE = [255, 255, 255, 255]     # Bright highlights
    BLACK = [0, 0, 0, 255]           # Deep shadows/outline
    RED = [139, 0, 0, 255]           # Ruby gems
    DARK_RED = [100, 0, 0, 255]      # Ruby shading
    LIGHT_RED = [220, 50, 50, 255]   # Ruby highlights
    
    # BREASTPLATE MAIN BODY (natural chest contour - realistic shape)
    # Create a breastplate that follows natural chest anatomy
    
    chest_pixels = []
    
    # Define breastplate with natural chest curves (not rectangular)
    center_x = 16
    
    # Build breastplate row by row with proper chest contours
    breastplate_shape = {
        # Row: (left_offset, right_offset) from center
        6: (2, 2),    # Neck area - narrow
        7: (3, 3),    # Upper chest - getting wider
        8: (4, 4),    # Upper chest
        9: (5, 5),    # Mid upper chest - widest part
        10: (5, 5),   # Main chest area
        11: (5, 5),   # Main chest area
        12: (5, 5),   # Main chest area
        13: (5, 5),   # Main chest area
        14: (4, 4),   # Lower chest - starting to taper
        15: (4, 4),   # Lower chest
        16: (4, 4),   # Lower chest
        17: (3, 3),   # Waist area - narrowing
        18: (3, 3),   # Waist area
        19: (2, 2),   # Lower waist - narrow
        20: (2, 2),   # Bottom edge
    }
    
    # Create the natural breastplate shape
    for y, (left_offset, right_offset) in breastplate_shape.items():
        for x in range(center_x - left_offset, center_x + right_offset + 1):
            if 0 <= x < size:
                chest_pixels.append((y, x))
    
    # Fill main chestplate with gold
    for y, x in chest_pixels:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = GOLD
    
    # Add shading to left side (darker) - natural breastplate shading
    shadow_pixels = []
    for y in range(6, 21):
        if y in breastplate_shape:
            left_offset, _ = breastplate_shape[y]
            # Add shadow to leftmost and second-leftmost pixels
            shadow_x1 = center_x - left_offset
            shadow_x2 = center_x - left_offset + 1
            if 0 <= shadow_x1 < size:
                shadow_pixels.append((y, shadow_x1))
            if 0 <= shadow_x2 < size:
                shadow_pixels.append((y, shadow_x2))
    
    for y, x in shadow_pixels:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = DARK_GOLD
    
    # Add highlights to right side (brighter) - natural breastplate highlights
    highlight_pixels = []
    for y in range(6, 21):
        if y in breastplate_shape:
            _, right_offset = breastplate_shape[y]
            # Add highlights to rightmost and second-rightmost pixels
            highlight_x1 = center_x + right_offset
            highlight_x2 = center_x + right_offset - 1
            if 0 <= highlight_x1 < size:
                highlight_pixels.append((y, highlight_x1))
            if 0 <= highlight_x2 < size and y % 2 == 0:  # Every other row
                highlight_pixels.append((y, highlight_x2))
        # Central shine down the middle
        if y % 3 == 0:
            highlight_pixels.append((y, center_x))
    
    for y, x in highlight_pixels:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = LIGHT_GOLD
    
    # DECORATIVE ELEMENTS FOR NATURAL BREASTPLATE
    
    # Central ornamental crest (proportional to chest)
    crest_center_x, crest_center_y = 16, 12
    
    # Central emblem - elegant cross design
    emblem_pixels = [
        # Vertical bar (smaller, more proportional)
        (crest_center_y - 1, crest_center_x), (crest_center_y, crest_center_x), (crest_center_y + 1, crest_center_x),
        # Horizontal bar
        (crest_center_y, crest_center_x - 1), (crest_center_y, crest_center_x + 1),
    ]
    
    for y, x in emblem_pixels:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BRONZE
    
    # Central highlight
    canvas[crest_center_y][crest_center_x] = LIGHT_BRONZE
    
    # Ruby gems at natural chest positions (shoulder points and lower chest)
    chest_gems = [(8, 13), (8, 19), (16, 14), (16, 18)]  # Natural positioning
    for y, x in chest_gems:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = RED
            # Add gem highlights
            if x + 1 < size:
                canvas[y][x+1] = LIGHT_RED
    
    # METAL TRIM AND BANDS (following natural breastplate contours)
    
    # Edge trim following the natural shape
    trim_pixels = []
    
    for y in range(6, 21):
        if y in breastplate_shape:
            left_offset, right_offset = breastplate_shape[y]
            # Add trim to the edges
            left_edge = center_x - left_offset
            right_edge = center_x + right_offset
            
            if 0 <= left_edge < size:
                trim_pixels.append((y, left_edge))
            if 0 <= right_edge < size:
                trim_pixels.append((y, right_edge))
    
    # Apply silver trim to edges
    for y, x in trim_pixels:
        canvas[y][x] = SILVER
    
    # Top neckline trim
    neckline_y = 6
    if neckline_y in breastplate_shape:
        left_offset, right_offset = breastplate_shape[neckline_y]
        for x in range(center_x - left_offset, center_x + right_offset + 1):
            if 0 <= x < size:
                canvas[neckline_y][x] = SILVER
    
    # Bottom waistline trim  
    waistline_y = 20
    if waistline_y in breastplate_shape:
        left_offset, right_offset = breastplate_shape[waistline_y]
        for x in range(center_x - left_offset, center_x + right_offset + 1):
            if 0 <= x < size:
                canvas[waistline_y][x] = BRONZE
    
    # MAGICAL ENHANCEMENTS (like staff's magical elements)
    
    # Golden runes along the sides
    rune_positions = [
        (10, 14), (12, 15), (14, 16), (16, 15)  # Mystical markings
    ]
    
    for y, x in rune_positions:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = WHITE  # Glowing runes
    
    # Armor rivets/studs (functional details)
    rivet_positions = [
        (9, 14), (9, 18), (11, 13), (11, 19), (13, 14), (13, 18), (15, 15), (15, 17)
    ]
    
    for y, x in rivet_positions:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = COPPER
            # Add small highlight
            if y > 0:
                canvas[y-1][x] = LIGHT_BRONZE
    
    # HEROIC MUSCULAR BREASTPLATE DEFINITION
    
    # Pronounced pectoral muscles (masculine chest definition)
    left_pectoral = [
        # Left pec outer curve
        (8, 12), (9, 11), (10, 11), (11, 12), (12, 12), (13, 13),
        # Left pec inner definition
        (9, 14), (10, 14), (11, 15), (12, 15)
    ]
    
    right_pectoral = [
        # Right pec outer curve  
        (8, 20), (9, 21), (10, 21), (11, 20), (12, 20), (13, 19),
        # Right pec inner definition
        (9, 18), (10, 18), (11, 17), (12, 17)
    ]
    
    # Apply dark shading for muscle definition
    for y, x in left_pectoral + right_pectoral:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = DARK_GOLD
    
    # Central sternum/chest separation (valley between pecs)
    sternum_line = [(9, 16), (10, 16), (11, 16), (12, 16)]
    for y, x in sternum_line:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = DARK_GOLD
    
    # Abdominal muscle definition (six-pack abs)
    abs_definition = [
        # Upper abs (row 1)
        (14, 14), (14, 15),  # Left upper ab
        (14, 17), (14, 18),  # Right upper ab
        
        # Middle abs (row 2) 
        (16, 14), (16, 15),  # Left middle ab
        (16, 17), (16, 18),  # Right middle ab
        
        # Lower abs (row 3)
        (18, 15), (18, 17),  # Lower abs (smaller)
        
        # Ab separation lines
        (15, 14), (15, 18),  # Horizontal separators
        (17, 14), (17, 18),  # More horizontal separators
        (14, 16), (15, 16), (16, 16), (17, 16), (18, 16)  # Central linea alba
    ]
    
    for y, x in abs_definition:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = DARK_GOLD
    
    # Muscle highlights (raised muscle areas)
    muscle_highlights = [
        # Pectoral muscle peaks
        (9, 13), (9, 19),  # Peak of each pec
        (10, 13), (10, 19), # Secondary pec highlights
        
        # Ab muscle highlights
        (14, 14), (14, 18),  # Upper ab peaks
        (16, 14), (16, 18),  # Middle ab peaks
    ]
    
    for y, x in muscle_highlights:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = LIGHT_GOLD
    
    # FINAL NATURAL BREASTPLATE DETAILS
    
    # Natural breastplate outline (no boxy frame)
    outline_pixels = []
    
    # Create outline following the natural contours
    for y in range(5, 22):  # One row above and below the actual breastplate
        if y + 1 in breastplate_shape:
            left_offset, right_offset = breastplate_shape[y + 1]
            # Add outline pixels just outside the shape
            left_outline = center_x - left_offset - 1
            right_outline = center_x + right_offset + 1
            
            if 0 <= left_outline < size:
                outline_pixels.append((y + 1, left_outline))
            if 0 <= right_outline < size:
                outline_pixels.append((y + 1, right_outline))
    
    # Top and bottom outlines
    for y in [5, 21]:  # Just above and below the breastplate
        if y + 1 in breastplate_shape or y - 1 in breastplate_shape:
            shape_y = y + 1 if y + 1 in breastplate_shape else y - 1
            left_offset, right_offset = breastplate_shape[shape_y]
            for x in range(center_x - left_offset, center_x + right_offset + 1):
                if 0 <= x < size:
                    outline_pixels.append((y, x))
    
    for y, x in outline_pixels:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BLACK
    
    # Elegant highlights for premium golden breastplate
    premium_highlights = []
    # Central vertical shine line (subtle)
    for y in range(8, 19, 2):
        premium_highlights.append((y, center_x))
    
    # Curved highlights following chest contours
    highlight_positions = [(9, 15), (9, 17), (11, 14), (11, 18), (15, 15), (15, 17)]
    premium_highlights.extend(highlight_positions)
    
    for y, x in premium_highlights:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = WHITE
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save image
    output_path = 'golden_armor.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Minecraft-style pixel art golden chestplate")
    print(f"   Materials: Gold main body, bronze/copper accents, silver trim")
    print(f"   Details: Ruby shoulder gems, mystical runes, armor rivets")
    print(f"   Features: 3D shading, shoulder guards, ornamental crest")
    print(f"   Quality: Premium golden armor with magical enhancements")

if __name__ == '__main__':
    create_golden_armor()