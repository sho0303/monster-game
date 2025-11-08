#!/usr/bin/env python3
"""
Demo the quest summary feature in monster encounters
"""

def demo_quest_summary():
    """Demonstrate what the quest summary will look like after victory"""
    
    print("🎮 Victory Quest Summary Demo")
    print("=" * 50)
    
    print("\n🎉 Victory! You earned 50 gold!")
    
    # Simulate quest summary display
    print("\n📜 Current Quests (2/3 active):")
    print("   1. 🌱 Hunt a Spider in the grasslands → +2 XP")
    print("   2. 🏜️ Defeat a Cyclops in the desert sands → +5 XP")
    
    print("\n🏆 Quest Completed: Hunt a Spider in the grasslands (+2 XP)")
    print("   💫 Ready to level up! XP: 8 → 10/10 (Need 10 for Level 2)")
    
    print("\n" + "=" * 50)
    print("✨ New Quest Summary Features:")
    print("✅ Shows all active quests after each victory")
    print("✅ Displays biome context with emojis")
    print("✅ Shows XP rewards for each quest")
    print("✅ Indicates quest progress (2/3 active)")
    print("✅ Helps players track their objectives")
    
    print("\n🎯 Benefits:")
    print("• Better quest visibility and progress tracking")
    print("• Contextual biome information")
    print("• Encourages quest completion")
    print("• Enhanced post-combat experience")

if __name__ == "__main__":
    demo_quest_summary()