"""
Scorpion Monster Creator
Creates pixel art for a menacing scorpion - armored body, large claws, curved stinger tail.
Inspired by the realistic scorpion with dark exoskeleton and threatening posture.

Resolution: 64x64 pixels (scaled 4x to 256x256)
Style: Pixel art with detailed armored segments
Palette: Dark browns, blacks, reddish tones for stinger
"""

from PIL import Image
import numpy as np


def create_scorpion_default():
    """Create the default threatening scorpion pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - inspired by the scorpion image
    SHELL_DARK = [40, 35, 30, 255]          # Dark exoskeleton
    SHELL_BROWN = [60, 50, 40, 255]         # Brown shell
    SHELL_LIGHT = [80, 70, 55, 255]         # Light brown
    SHELL_HIGHLIGHT = [100, 85, 65, 255]    # Highlights on shell
    SEGMENT_DARK = [35, 30, 25, 255]        # Segment shadows
    SEGMENT_LINE = [25, 20, 18, 255]        # Segment lines
    CLAW_DARK = [45, 40, 35, 255]           # Claw base
    CLAW_BROWN = [65, 55, 45, 255]          # Claw color
    CLAW_LIGHT = [85, 75, 60, 255]          # Claw highlights
    STINGER_RED = [100, 40, 35, 255]        # Red stinger base
    STINGER_DARK = [80, 30, 25, 255]        # Dark stinger
    STINGER_TIP = [60, 20, 18, 255]         # Stinger tip (darker)
    LEG_DARK = [35, 30, 28, 255]            # Leg color
    LEG_JOINT = [50, 45, 38, 255]           # Leg joints
    EYE_BLACK = [15, 12, 10, 255]           # Eyes
    TEXTURE_SPOT = [70, 60, 48, 255]        # Texture spots
    
    center_x = 32
    base_y = 50
    
    # === LEGS (8 legs total, 4 per side) ===
    # Left legs
    for leg_num in range(4):
        leg_base_y = base_y - 8 - leg_num * 4
        leg_base_x = center_x - 8
        
        # Leg segments (3 segments per leg)
        for segment in range(3):
            seg_length = 5 - segment
            seg_angle = segment * 2
            seg_down = segment * 3
            
            for lx in range(seg_length):
                leg_x = leg_base_x - lx - seg_angle
                leg_y = leg_base_y + seg_down + lx // 2
                if 0 <= leg_x < width and 0 <= leg_y < height:
                    for ly in range(2):
                        if 0 <= leg_y + ly < height:
                            canvas[leg_y + ly][leg_x] = LEG_JOINT if lx == 0 else LEG_DARK
    
    # Right legs
    for leg_num in range(4):
        leg_base_y = base_y - 8 - leg_num * 4
        leg_base_x = center_x + 8
        
        for segment in range(3):
            seg_length = 5 - segment
            seg_angle = segment * 2
            seg_down = segment * 3
            
            for lx in range(seg_length):
                leg_x = leg_base_x + lx + seg_angle
                leg_y = leg_base_y + seg_down + lx // 2
                if 0 <= leg_x < width and 0 <= leg_y < height:
                    for ly in range(2):
                        if 0 <= leg_y + ly < height:
                            canvas[leg_y + ly][leg_x] = LEG_JOINT if lx == 0 else LEG_DARK
    
    # === BODY (segmented abdomen) ===
    body_y = base_y - 8
    
    # Body segments (5 segments getting smaller)
    for segment in range(5):
        seg_y = body_y - segment * 4
        seg_width = 10 - segment
        
        for sy in range(4):
            for sx in range(-seg_width, seg_width + 1):
                body_x = center_x + sx
                body_ypos = seg_y - sy
                if 0 <= body_x < width and 0 <= body_ypos < height:
                    # Armored segment appearance
                    if sy == 0 or sy == 3:
                        # Segment lines
                        canvas[body_ypos][body_x] = SEGMENT_LINE
                    elif abs(sx) > seg_width - 2:
                        canvas[body_ypos][body_x] = SHELL_DARK
                    elif sx < -4:
                        canvas[body_ypos][body_x] = SHELL_BROWN
                    elif sx < 0:
                        canvas[body_ypos][body_x] = SHELL_LIGHT
                    elif sx < 4:
                        canvas[body_ypos][body_x] = SHELL_HIGHLIGHT
                    else:
                        canvas[body_ypos][body_x] = SHELL_BROWN
    
    # Texture spots on segments
    for segment in range(4):
        spot_y = body_y - segment * 4 - 2
        for spot_x in range(-6, 7, 4):
            if abs(spot_x) > 2:
                sx = center_x + spot_x
                if 0 <= sx < width and 0 <= spot_y < height:
                    canvas[spot_y][sx] = TEXTURE_SPOT
    
    # === TAIL (curved upward then back down with wicked tip) ===
    tail_start_y = body_y - 20
    tail_start_x = center_x
    
    # Tail segments - arc up then curve down
    for segment in range(10):
        if segment < 5:
            # Going up
            seg_y = tail_start_y - segment * 3
            seg_x = tail_start_x + segment // 2
        else:
            # Curving back down
            arc_segment = segment - 5
            seg_y = tail_start_y - 15 + arc_segment * 2
            seg_x = tail_start_x + 2 + arc_segment
        
        seg_width = 4 - segment // 4
        
        for sy in range(3):
            for sx in range(-seg_width, seg_width + 1):
                tail_x = seg_x + sx
                tail_y = seg_y - sy
                if 0 <= tail_x < width and 0 <= tail_y < height:
                    if sy == 0 or sy == 2:
                        canvas[tail_y][tail_x] = SEGMENT_LINE
                    elif sx < 0:
                        canvas[tail_y][tail_x] = SHELL_BROWN
                    else:
                        canvas[tail_y][tail_x] = SHELL_LIGHT
    
    # Stinger bulb (at the curve down point)
    stinger_base_x = tail_start_x + 7
    stinger_base_y = tail_start_y - 5
    
    for sy in range(5):
        stinger_width = 3 - sy // 2
        for sx in range(-stinger_width, stinger_width + 1):
            stinger_x = stinger_base_x + sx
            stinger_y = stinger_base_y - sy
            if 0 <= stinger_x < width and 0 <= stinger_y < height:
                if sy < 2:
                    canvas[stinger_y][stinger_x] = STINGER_RED
                elif sx < 0:
                    canvas[stinger_y][stinger_x] = STINGER_DARK
                else:
                    canvas[stinger_y][stinger_x] = STINGER_RED
    
    # Wicked stinger point (pointing down and forward)
    for sp in range(6):
        point_x = stinger_base_x + sp // 2
        point_y = stinger_base_y - 5 + sp
        if 0 <= point_x < width and 0 <= point_y < height:
            canvas[point_y][point_x] = STINGER_TIP
    
    # === CEPHALOTHORAX (head/thorax section) ===
    head_y = body_y - 8
    
    for hy in range(8):
        head_width = 9 - hy // 3
        for hx in range(-head_width, head_width + 1):
            head_x = center_x + hx
            head_ypos = head_y - hy
            if 0 <= head_x < width and 0 <= head_ypos < height:
                # Armored head
                if abs(hx) > head_width - 2:
                    canvas[head_ypos][head_x] = SHELL_DARK
                elif hx < -4:
                    canvas[head_ypos][head_x] = SHELL_BROWN
                elif hx < 0:
                    canvas[head_ypos][head_x] = SHELL_LIGHT
                elif hx < 4:
                    canvas[head_ypos][head_x] = SHELL_HIGHLIGHT
                else:
                    canvas[head_ypos][head_x] = SHELL_BROWN
    
    # === EYES (small, on top of head) ===
    eye_y = head_y - 6
    for eye_offset in [-2, 2]:
        eye_x = center_x + eye_offset
        if 0 <= eye_x < width and 0 <= eye_y < height:
            canvas[eye_y][eye_x] = EYE_BLACK
    
    # === PEDIPALPS (small front appendages near mouth) ===
    for pedi_offset in [-6, 6]:
        pedi_x = center_x + pedi_offset
        pedi_y = head_y - 2
        
        for py in range(4):
            for px in range(2):
                ped_x = pedi_x + px * (1 if pedi_offset > 0 else -1)
                ped_y = pedi_y + py
                if 0 <= ped_x < width and 0 <= ped_y < height:
                    canvas[ped_y][ped_x] = LEG_DARK
    
    # === CLAWS (large pincers - WIDE OPEN) ===
    # Left claw
    left_claw_x = center_x - 12
    left_claw_y = head_y - 4
    
    # Claw arm
    for ax in range(8):
        for ay in range(3):
            arm_x = left_claw_x + ax
            arm_y = left_claw_y + ay
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = CLAW_BROWN if ay == 1 else CLAW_DARK
    
    # Claw pincer (wide open - clearly visible)
    for cy in range(8):
        claw_width = 3 - cy // 4
        claw_spread = cy // 2
        for cx in range(claw_width):
            # Upper pincer (angled up more)
            claw_x = left_claw_x - cx
            claw_y = left_claw_y - cy - claw_spread
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = CLAW_LIGHT if cx == 0 else CLAW_BROWN
            
            # Lower pincer (angled down more)
            claw_y = left_claw_y + 3 + cy + claw_spread
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = CLAW_DARK if cx == 0 else CLAW_BROWN
    
    # Right claw
    right_claw_x = center_x + 12
    right_claw_y = head_y - 4
    
    # Claw arm
    for ax in range(8):
        for ay in range(3):
            arm_x = right_claw_x - ax
            arm_y = right_claw_y + ay
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = CLAW_BROWN if ay == 1 else CLAW_DARK
    
    # Claw pincer (wide open - clearly visible)
    for cy in range(8):
        claw_width = 3 - cy // 4
        claw_spread = cy // 2
        for cx in range(claw_width):
            # Upper pincer (angled up more)
            claw_x = right_claw_x + cx
            claw_y = right_claw_y - cy - claw_spread
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = CLAW_LIGHT if cx == 0 else CLAW_BROWN
            
            # Lower pincer (angled down more)
            claw_y = right_claw_y + 3 + cy + claw_spread
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = CLAW_DARK if cx == 0 else CLAW_BROWN
    
    return canvas


def create_scorpion_attack():
    """Create the attacking scorpion - stinger striking forward."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    SHELL_DARK = [40, 35, 30, 255]
    SHELL_BROWN = [60, 50, 40, 255]
    SHELL_LIGHT = [80, 70, 55, 255]
    SHELL_HIGHLIGHT = [100, 85, 65, 255]
    SEGMENT_DARK = [35, 30, 25, 255]
    SEGMENT_LINE = [25, 20, 18, 255]
    CLAW_DARK = [45, 40, 35, 255]
    CLAW_BROWN = [65, 55, 45, 255]
    CLAW_LIGHT = [85, 75, 60, 255]
    STINGER_RED = [100, 40, 35, 255]
    STINGER_DARK = [80, 30, 25, 255]
    STINGER_TIP = [60, 20, 18, 255]
    LEG_DARK = [35, 30, 28, 255]
    LEG_JOINT = [50, 45, 38, 255]
    EYE_BLACK = [15, 12, 10, 255]
    TEXTURE_SPOT = [70, 60, 48, 255]
    MOTION_BLUR = [100, 40, 35, 150]
    
    center_x = 32
    base_y = 50
    
    # === LEGS (more spread, aggressive stance) ===
    # Left legs
    for leg_num in range(4):
        leg_base_y = base_y - 8 - leg_num * 4
        leg_base_x = center_x - 8
        
        for segment in range(3):
            seg_length = 6 - segment
            seg_angle = segment * 3
            seg_down = segment * 3
            
            for lx in range(seg_length):
                leg_x = leg_base_x - lx - seg_angle
                leg_y = leg_base_y + seg_down + lx // 2
                if 0 <= leg_x < width and 0 <= leg_y < height:
                    for ly in range(2):
                        if 0 <= leg_y + ly < height:
                            canvas[leg_y + ly][leg_x] = LEG_JOINT if lx == 0 else LEG_DARK
    
    # Right legs
    for leg_num in range(4):
        leg_base_y = base_y - 8 - leg_num * 4
        leg_base_x = center_x + 8
        
        for segment in range(3):
            seg_length = 6 - segment
            seg_angle = segment * 3
            seg_down = segment * 3
            
            for lx in range(seg_length):
                leg_x = leg_base_x + lx + seg_angle
                leg_y = leg_base_y + seg_down + lx // 2
                if 0 <= leg_x < width and 0 <= leg_y < height:
                    for ly in range(2):
                        if 0 <= leg_y + ly < height:
                            canvas[leg_y + ly][leg_x] = LEG_JOINT if lx == 0 else LEG_DARK
    
    # === BODY (segmented) ===
    body_y = base_y - 8
    
    for segment in range(5):
        seg_y = body_y - segment * 4
        seg_width = 10 - segment
        
        for sy in range(4):
            for sx in range(-seg_width, seg_width + 1):
                body_x = center_x + sx
                body_ypos = seg_y - sy
                if 0 <= body_x < width and 0 <= body_ypos < height:
                    if sy == 0 or sy == 3:
                        canvas[body_ypos][body_x] = SEGMENT_LINE
                    elif abs(sx) > seg_width - 2:
                        canvas[body_ypos][body_x] = SHELL_DARK
                    elif sx < -4:
                        canvas[body_ypos][body_x] = SHELL_BROWN
                    elif sx < 0:
                        canvas[body_ypos][body_x] = SHELL_LIGHT
                    elif sx < 4:
                        canvas[body_ypos][body_x] = SHELL_HIGHLIGHT
                    else:
                        canvas[body_ypos][body_x] = SHELL_BROWN
    
    # Texture spots
    for segment in range(4):
        spot_y = body_y - segment * 4 - 2
        for spot_x in range(-6, 7, 4):
            if abs(spot_x) > 2:
                sx = center_x + spot_x
                if 0 <= sx < width and 0 <= spot_y < height:
                    canvas[spot_y][sx] = TEXTURE_SPOT
    
    # === TAIL (CURVED FORWARD FOR STRIKE - arcs down with wicked tip) ===
    tail_start_y = body_y - 20
    tail_start_x = center_x
    
    # Tail arcing forward and down over body
    for segment in range(12):
        # Arc calculation - goes up then curves forward and down
        if segment < 5:
            # Going up
            seg_y = tail_start_y - segment * 3
            seg_x = tail_start_x + segment // 2
        elif segment < 9:
            # Arcing forward at top
            arc_seg = segment - 5
            seg_y = tail_start_y - 15 + arc_seg
            seg_x = tail_start_x + 2 - arc_seg * 2
        else:
            # Coming down for strike
            down_seg = segment - 9
            seg_y = tail_start_y - 11 + down_seg * 2
            seg_x = tail_start_x - 6 - down_seg
        
        seg_width = 4 - segment // 5
        
        for sy in range(3):
            for sx in range(-seg_width, seg_width + 1):
                tail_x = seg_x + sx
                tail_y = seg_y - sy
                if 0 <= tail_x < width and 0 <= tail_y < height:
                    if sy == 0 or sy == 2:
                        canvas[tail_y][tail_x] = SEGMENT_LINE
                    elif sx < 0:
                        canvas[tail_y][tail_x] = SHELL_BROWN
                    else:
                        canvas[tail_y][tail_x] = SHELL_LIGHT
    
    # Stinger bulb (positioned at downward curve)
    stinger_base_x = tail_start_x - 9
    stinger_base_y = tail_start_y - 5
    
    for sy in range(6):
        stinger_width = 4 - sy // 2
        for sx in range(-stinger_width, stinger_width + 1):
            stinger_x = stinger_base_x + sx
            stinger_y = stinger_base_y - sy
            if 0 <= stinger_x < width and 0 <= stinger_y < height:
                if sy < 3:
                    canvas[stinger_y][stinger_x] = STINGER_RED
                elif sx < 0:
                    canvas[stinger_y][stinger_x] = STINGER_DARK
                else:
                    canvas[stinger_y][stinger_x] = STINGER_RED
    
    # Wicked stinger point (aimed downward for strike)
    for sp in range(6):
        point_x = stinger_base_x - sp // 2
        point_y = stinger_base_y - 6 + sp
        if 0 <= point_x < width and 0 <= point_y < height:
            canvas[point_y][point_x] = STINGER_TIP
    
    # === CEPHALOTHORAX ===
    head_y = body_y - 8
    
    for hy in range(8):
        head_width = 9 - hy // 3
        for hx in range(-head_width, head_width + 1):
            head_x = center_x + hx
            head_ypos = head_y - hy
            if 0 <= head_x < width and 0 <= head_ypos < height:
                if abs(hx) > head_width - 2:
                    canvas[head_ypos][head_x] = SHELL_DARK
                elif hx < -4:
                    canvas[head_ypos][head_x] = SHELL_BROWN
                elif hx < 0:
                    canvas[head_ypos][head_x] = SHELL_LIGHT
                elif hx < 4:
                    canvas[head_ypos][head_x] = SHELL_HIGHLIGHT
                else:
                    canvas[head_ypos][head_x] = SHELL_BROWN
    
    # === EYES ===
    eye_y = head_y - 6
    for eye_offset in [-2, 2]:
        eye_x = center_x + eye_offset
        if 0 <= eye_x < width and 0 <= eye_y < height:
            canvas[eye_y][eye_x] = EYE_BLACK
    
    # === PEDIPALPS ===
    for pedi_offset in [-6, 6]:
        pedi_x = center_x + pedi_offset
        pedi_y = head_y - 2
        
        for py in range(4):
            for px in range(2):
                ped_x = pedi_x + px * (1 if pedi_offset > 0 else -1)
                ped_y = pedi_y + py
                if 0 <= ped_x < width and 0 <= ped_y < height:
                    canvas[ped_y][ped_x] = LEG_DARK
    
    # === CLAWS (RAISED, THREATENING - WIDE OPEN) ===
    # Left claw (raised higher)
    left_claw_x = center_x - 12
    left_claw_y = head_y - 8
    
    # Claw arm
    for ax in range(8):
        for ay in range(3):
            arm_x = left_claw_x + ax
            arm_y = left_claw_y + ay
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = CLAW_BROWN if ay == 1 else CLAW_DARK
    
    # Claw pincer (wide open, clearly visible)
    for cy in range(9):
        claw_width = 4 - cy // 4
        claw_spread = cy // 2
        for cx in range(claw_width):
            # Upper pincer (spread wide)
            claw_x = left_claw_x - cx
            claw_y = left_claw_y - cy - claw_spread
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = CLAW_LIGHT if cx == 0 else CLAW_BROWN
            
            # Lower pincer (spread wide)
            claw_y = left_claw_y + 3 + cy + claw_spread
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = CLAW_DARK if cx == 0 else CLAW_BROWN
    
    # Right claw (raised)
    right_claw_x = center_x + 12
    right_claw_y = head_y - 6
    
    # Claw arm
    for ax in range(8):
        for ay in range(3):
            arm_x = right_claw_x - ax
            arm_y = right_claw_y + ay
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = CLAW_BROWN if ay == 1 else CLAW_DARK
    
    # Claw pincer (wide open, clearly visible)
    for cy in range(9):
        claw_width = 4 - cy // 4
        claw_spread = cy // 2
        for cx in range(claw_width):
            # Upper pincer (spread wide)
            claw_x = right_claw_x + cx
            claw_y = right_claw_y - cy - claw_spread
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = CLAW_LIGHT if cx == 0 else CLAW_BROWN
            
            # Lower pincer (spread wide)
            claw_y = right_claw_y + 3 + cy + claw_spread
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = CLAW_DARK if cx == 0 else CLAW_BROWN
    
    # === MOTION EFFECTS (stinger strike blur) ===
    for blur in range(8):
        blur_x = stinger_base_x - 13 - blur
        blur_y = stinger_base_y - 6 + blur // 3
        if 0 <= blur_x < width and 0 <= blur_y < height:
            canvas[blur_y][blur_x] = MOTION_BLUR
    
    return canvas


def main():
    print("Creating scorpion monster images...")
    
    scorpion_default = create_scorpion_default()
    scorpion_attack = create_scorpion_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(scorpion_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('art/scorpion_monster.png')
    print(f"✓ Saved: art/scorpion_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(scorpion_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('art/scorpion_monster_attack.png')
    print(f"✓ Saved: art/scorpion_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Scorpion monster creation complete!")
    print("\nFeatures:")
    print("- Default: Threatening pose with tail curved up, claws open, 8 legs")
    print("- Attack: Stinger striking forward, claws raised, aggressive stance")
    print("\nStyle: Realistic armored scorpion with segmented body")
    print("Colors: Dark brown exoskeleton, reddish stinger, segmented armor plating")


if __name__ == '__main__':
    main()
