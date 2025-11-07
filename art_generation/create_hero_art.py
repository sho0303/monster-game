from PIL import Image
import numpy as np

# Create a 32x32 pixel art image with transparent background
# RGBA format: (Red, Green, Blue, Alpha)
img_array = np.zeros((32, 32, 4), dtype=np.uint8)

# Define Minecraft-style colors
BROWN = [101, 67, 33, 255]          # Hair
SKIN = [255, 220, 177, 255]         # Skin tone
GRAY = [150, 150, 150, 255]         # Armor
SILVER = [192, 192, 192, 255]       # Sword blade
DARK_BROWN = [139, 69, 19, 255]     # Sword handle
BLACK = [0, 0, 0, 255]              # Eyes/outline
RED = [200, 0, 0, 255]              # Shirt
BLUE = [50, 100, 200, 255]          # Pants
DARK_GRAY = [80, 80, 80, 255]       # Dark armor/belt

# Helper function to draw rectangle
def draw_rect(arr, x, y, w, h, color):
    arr[y:y+h, x:x+w] = color

# Draw the Minecraft-style warrior
# Head (8x8)
draw_rect(img_array, 12, 4, 8, 4, BROWN)        # Hair top
draw_rect(img_array, 11, 7, 10, 1, BROWN)       # Hair sides
draw_rect(img_array, 12, 8, 8, 8, SKIN)         # Face
img_array[10, 14] = BLACK                        # Left eye
img_array[10, 17] = BLACK                        # Right eye
img_array[12, 14:18] = BLACK                     # Mouth

# Body (8x12)
draw_rect(img_array, 12, 16, 8, 12, RED)        # Torso/shirt
draw_rect(img_array, 13, 18, 6, 1, DARK_GRAY)   # Belt

# Arms (4x12 each)
draw_rect(img_array, 8, 16, 4, 12, RED)         # Left arm
draw_rect(img_array, 20, 16, 4, 12, RED)        # Right arm

# Legs (4x12 each)
draw_rect(img_array, 12, 28, 4, 4, BLUE)        # Left leg
draw_rect(img_array, 16, 28, 4, 4, BLUE)        # Right leg

# Armor details
draw_rect(img_array, 11, 16, 10, 2, GRAY)       # Shoulder armor
draw_rect(img_array, 8, 16, 3, 3, GRAY)         # Left shoulder pad
draw_rect(img_array, 21, 16, 3, 3, GRAY)        # Right shoulder pad
draw_rect(img_array, 12, 17, 8, 1, DARK_GRAY)   # Chest plate line

# Sword in right hand
draw_rect(img_array, 24, 18, 2, 8, SILVER)      # Blade
draw_rect(img_array, 23, 19, 4, 1, DARK_BROWN)  # Cross guard
draw_rect(img_array, 24, 26, 2, 3, DARK_BROWN)  # Handle
draw_rect(img_array, 24, 29, 2, 1, BROWN)       # Pommel

# Shield in left hand (optional)
draw_rect(img_array, 5, 20, 3, 5, GRAY)         # Shield
draw_rect(img_array, 6, 21, 1, 3, RED)          # Shield emblem

# Create PIL Image from numpy array
img = Image.fromarray(img_array, 'RGBA')

# Scale up 8x for better visibility (32x32 -> 256x256)
img = img.resize((256, 256), Image.NEAREST)

# Save the image
img.save('ascii_art/hero_warrior.png')
print("✅ Created hero_warrior.png - Minecraft-style pixel art warrior!")
print("   Size: 256x256 pixels")
print("   Format: PNG with transparent background")

