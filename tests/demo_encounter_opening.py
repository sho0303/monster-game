#!/usr/bin/env python3
"""
Demo the quest summary at monster encounter opening screen
"""

def demo_encounter_opening():
    """Demonstrate the new quest display at encounter start"""
    
    print("🎮 Monster Encounter Opening Screen Demo")
    print("=" * 60)
    
    print("\n🌱 A Giant Spider emerges from the tall grass! 🌱")
    
    print("\n📜 Active Quests (2/3):")
    print("  ⭐ 🌱 Hunt a Spider in the grasslands → 2 XP ⭐ THIS FIGHT!")
    print("  • 🏜️ Defeat a Cyclops in the desert sands → 5 XP")
    
    print("\n" + "=" * 40)
    print("⚔️  COMBAT PREVIEW")
    print("=" * 40)
    print("🧙 Eduardo the wise          🕷️ Giant Spider")
    print("❤️  HP: 10/10                ❤️  HP: 15/15")
    print("⚔️  Attack: 15               ⚔️  Attack: 8")
    print("🛡️  Defense: 5               🛡️  Defense: 2")
    print("=" * 40)
    
    print("\n[⚔️ Fight] [🏃 Run]")
    
    print("\n" + "=" * 60)
    print("✨ Enhanced Opening Screen Features:")
    print("✅ Quest summary shown BEFORE the fight")
    print("✅ Matching quests highlighted with ⭐")
    print("✅ 'THIS FIGHT!' indicator for relevant quests")
    print("✅ Biome context with emojis")
    print("✅ XP rewards clearly visible")
    
    print("\n🎯 Benefits:")
    print("• Players know quest objectives before fighting")
    print("• Clear indication when encounter helps quest progress")
    print("• Better strategic decision making")
    print("• Enhanced motivation to engage in combat")
    print("• Immediate quest relevance feedback")
    
    print("\n📍 Quest Display Logic:")
    print("• Normal quest: • 🌱 Description → XP")
    print("• Matching quest: ⭐ 🌱 Description → XP ⭐ THIS FIGHT!")
    print("• No quests: 📜 No active quests - Visit Quests menu!")

if __name__ == "__main__":
    demo_encounter_opening()