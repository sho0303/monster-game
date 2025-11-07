"""
Test script to display the original ninja and the new attack animation side by side
"""
from PIL import Image
import os

def compare_ninja_versions():
    """Display original ninja and attack version for comparison"""
    
    # Check if both files exist
    original_path = '../art/Ninja.png'
    attack_path = '../art/ninja_attack.png'
    
    if not os.path.exists(original_path):
        print(f"❌ Original ninja not found: {original_path}")
        return
        
    if not os.path.exists(attack_path):
        print(f"❌ Attack ninja not found: {attack_path}")
        return
    
    try:
        # Load both images
        original = Image.open(original_path)
        attack = Image.open(attack_path)
        
        print(f"✅ Original Ninja: {original.size}")
        print(f"✅ Attack Ninja: {attack.size}")
        
        # Create side-by-side comparison
        total_width = original.width + attack.width + 20  # 20px gap
        max_height = max(original.height, attack.height)
        
        # Create comparison canvas
        comparison = Image.new('RGBA', (total_width, max_height), (60, 60, 60, 255))
        
        # Paste images side by side
        comparison.paste(original, (0, 0))
        comparison.paste(attack, (original.width + 20, 0))
        
        # Save comparison
        comparison_path = '../art/ninja_comparison.png'
        comparison.save(comparison_path)
        
        print(f"✅ Created comparison: {comparison_path}")
        print(f"   Size: {comparison.size}")
        print(f"   Shows: Original ninja (left) vs Attack animation (right)")
        
        # Display info about the attack features
        print("\n🥷 Attack Animation Features:")
        print("   • Dynamic attacking pose with extended kunai")
        print("   • Motion blur trails behind moving limbs")
        print("   • Speed lines showing attack motion")
        print("   • Attack sparkles and impact effects")
        print("   • Flowing headband and sash movement")
        print("   • Dust kick-up from dynamic stance")
        print("   • Blue aura energy effects")
        print("   • Forward lunge position")
        
    except Exception as e:
        print(f"❌ Error creating comparison: {e}")

if __name__ == '__main__':
    compare_ninja_versions()