"""
Test script to display the original warrior and the new attack animation side by side
"""
from PIL import Image
import os

def compare_warrior_versions():
    """Display original warrior and attack version for comparison"""
    
    # Check if both files exist
    import os
    base_dir = os.path.dirname(os.path.dirname(__file__))
    original_path = os.path.join(base_dir, 'art', 'Warrior.png')
    attack_path = os.path.join(base_dir, 'art', 'warrior_attack.png')
    
    if not os.path.exists(original_path):
        print(f"❌ Original warrior not found: {original_path}")
        return
        
    if not os.path.exists(attack_path):
        print(f"❌ Attack warrior not found: {attack_path}")
        return
    
    try:
        # Load both images
        original = Image.open(original_path)
        attack = Image.open(attack_path)
        
        print(f"✅ Original Warrior: {original.size}")
        print(f"✅ Attack Warrior: {attack.size}")
        
        # Create side-by-side comparison
        total_width = original.width + attack.width + 20  # 20px gap
        max_height = max(original.height, attack.height)
        
        # Create comparison canvas
        comparison = Image.new('RGBA', (total_width, max_height), (60, 60, 60, 255))
        
        # Paste images side by side
        comparison.paste(original, (0, 0))
        comparison.paste(attack, (original.width + 20, 0))
        
        # Save comparison
        comparison_path = os.path.join(base_dir, 'art', 'warrior_comparison.png')
        comparison.save(comparison_path)
        
        print(f"✅ Created comparison: {comparison_path}")
        print(f"   Size: {comparison.size}")
        print(f"   Shows: Original warrior (left) vs Attack animation (right)")
        
        # Display info about the attack features
        print("\\n⚔️ Attack Animation Features:")
        print("   • Dynamic sword strike with extended reach")
        print("   • Powerful overhead swing with motion trails")
        print("   • Sword energy effects and impact sparks")
        print("   • Battle-ready stance with defensive shield")
        print("   • Armor gleaming with battle intensity")
        print("   • Motion blur showing rapid movement")
        print("   • Ground impact effects from powerful stance")
        print("   • Battle aura and warrior energy")
        print("   • Flowing hair and clothing from combat motion")
        print("   • Enhanced weapon and armor highlights")
        
    except Exception as e:
        print(f"❌ Error creating comparison: {e}")

if __name__ == '__main__':
    compare_warrior_versions()