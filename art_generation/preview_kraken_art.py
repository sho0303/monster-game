#!/usr/bin/env python3
"""
Preview the generated Kraken art
"""

from PIL import Image
import os

def preview_kraken_art():
    """Display information about the generated Kraken art"""
    art_dir = "art"
    
    regular_path = os.path.join(art_dir, "kraken_monster.png")
    attack_path = os.path.join(art_dir, "kraken_monster_attack.png")
    
    if os.path.exists(regular_path) and os.path.exists(attack_path):
        # Load images
        regular_img = Image.open(regular_path)
        attack_img = Image.open(attack_path)
        
        print("🐙 KRAKEN MONSTER ART GENERATED SUCCESSFULLY! 🐙")
        print("=" * 60)
        print(f"📁 Regular Kraken Art: {regular_path}")
        print(f"   📏 Size: {regular_img.size}")
        print(f"   🎨 Mode: {regular_img.mode}")
        print()
        print(f"⚔️ Attack Kraken Art: {attack_path}")
        print(f"   📏 Size: {attack_img.size}")
        print(f"   🎨 Mode: {attack_img.mode}")
        print()
        print("🎯 FEATURES:")
        print("   • Massive octopus-like sea creature")
        print("   • 8 writhing tentacles with sucker details")
        print("   • Menacing red glowing eyes")
        print("   • Sharp beak for devastating attacks")
        print("   • Ancient barnacles showing age and power")
        print("   • Deep sea purple/dark color scheme")
        print("   • 256x256 pixel art (32x32 scaled up 8x)")
        print("   • Attack version features:")
        print("     - Whirlpool effects")
        print("     - Lightning crackling around body")
        print("     - Aggressive tentacle positioning")
        print("     - Violent water eruptions")
        print("     - Venom dripping from beak")
        print()
        print("🎮 GAME INTEGRATION:")
        print("   • Already configured in monsters/Kraken.yaml")
        print("   • Level 9 boss monster with 117 HP")
        print("   • Ocean biome encounter")
        print("   • 29 attack, 20 defense, 90 gold reward")
        print()
        print("✨ The Kraken awaits brave adventurers in the depths!")
        
        return regular_img, attack_img
    else:
        print("❌ Kraken art files not found. Please run create_kraken_art.py first.")
        return None, None

if __name__ == "__main__":
    preview_kraken_art()