"""
Test script to display the original magician and the new attack animation side by side
"""
from PIL import Image
import os

def compare_magician_versions():
    """Display original magician and attack version for comparison"""
    
    # Check if both files exist
    import os
    base_dir = os.path.dirname(os.path.dirname(__file__))
    original_path = os.path.join(base_dir, 'art', 'Magician.png')
    attack_path = os.path.join(base_dir, 'art', 'magician_attack.png')
    
    if not os.path.exists(original_path):
        print(f"❌ Original magician not found: {original_path}")
        return
        
    if not os.path.exists(attack_path):
        print(f"❌ Attack magician not found: {attack_path}")
        return
    
    try:
        # Load both images
        original = Image.open(original_path)
        attack = Image.open(attack_path)
        
        print(f"✅ Original Magician: {original.size}")
        print(f"✅ Attack Magician: {attack.size}")
        
        # Create side-by-side comparison
        total_width = original.width + attack.width + 20  # 20px gap
        max_height = max(original.height, attack.height)
        
        # Create comparison canvas
        comparison = Image.new('RGBA', (total_width, max_height), (60, 60, 60, 255))
        
        # Paste images side by side
        comparison.paste(original, (0, 0))
        comparison.paste(attack, (original.width + 20, 0))
        
        # Save comparison
        comparison_path = os.path.join(base_dir, 'art', 'magician_comparison.png')
        comparison.save(comparison_path)
        
        print(f"✅ Created comparison: {comparison_path}")
        print(f"   Size: {comparison.size}")
        print(f"   Shows: Original magician (left) vs Attack animation (right)")
        
        # Display info about the attack features
        print("\\n🧙 Attack Animation Features:")
        print("   • Dramatic spell-casting pose with extended arms")
        print("   • Massive energy orb with radiating magic beams")
        print("   • Crystal explosion at staff tip")
        print("   • Glowing eyes channeling magical power")
        print("   • Energy crackling through beard and robes")
        print("   • Flowing fabric effects from magical wind")
        print("   • Lightning and energy sparks")
        print("   • Magical aura surrounding entire wizard")
        print("   • Ground crackling with spell energy")
        print("   • Bright golden trim glowing with power")
        
    except Exception as e:
        print(f"❌ Error creating comparison: {e}")

if __name__ == '__main__':
    compare_magician_versions()