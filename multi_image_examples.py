"""
Example usage of multiple image display in the shop
This shows how to use the new show_images() method
"""

# Example usage in gui_shop.py:

def show_category_preview(self):
    """Show preview of all items in category using multiple images"""
    hero_class = self.gui.game_state.hero.get('class', '')
    items = self.store_data.get(self.current_category, [])
    
    # Filter items for hero's class
    available_items = [
        item for item in items 
        if item.get('class') == hero_class or item.get('class') == 'All'
    ]
    
    if not available_items:
        return
    
    # Collect all item images
    item_images = []
    for item in available_items:
        if 'ascii_art' in item and os.path.exists(item['ascii_art']):
            item_images.append(item['ascii_art'])
    
    if item_images:
        # Show multiple images based on count
        if len(item_images) == 1:
            self.gui.show_image(item_images[0])
        elif len(item_images) <= 2:
            self.gui.show_images(item_images, "horizontal")
        else:
            self.gui.show_images(item_images, "grid")

# Another example - comparison view:

def show_weapon_comparison(self):
    """Show weapon comparison using multiple images"""
    weapons = [
        'art/strong_sword.png',
        'art/weak_sword.png', 
        'art/magic_wand.png',
        'art/wizard_staff.png'
    ]
    
    # Show all weapons in a grid for comparison
    self.gui.show_images(weapons, "grid")
    
# Example - show multiple item types:

def show_all_ninja_gear(self):
    """Show all ninja equipment at once"""
    ninja_items = [
        'art/lightsaber.png',
        'art/nunchucks.png'
    ]
    
    # Show horizontally for easy comparison
    self.gui.show_images(ninja_items, "horizontal")

print("Multiple image display examples:")
print("1. gui.show_image('art/sword.png') - Single image (unchanged)")
print("2. gui.show_images(['art/sword1.png', 'art/sword2.png']) - Multiple images")
print("3. gui.show_images(images, 'horizontal') - Side by side")
print("4. gui.show_images(images, 'vertical') - Top to bottom")
print("5. gui.show_images(images, 'grid') - Grid layout")
print("6. gui.show_images(images, 'auto') - Automatic layout (default)")
print("7. gui.show_image(['art/img1.png', 'art/img2.png']) - List to show_image works too")