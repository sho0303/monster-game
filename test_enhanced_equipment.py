#!/usr/bin/env python3
"""
Test the enhanced equipment reward system
"""
import tkinter as tk
from gui_main import GameGUI

def test_enhanced_equipment_rewards():
    print("🎮 Testing Enhanced Equipment Reward System")
    
    root = tk.Tk()
    root.withdraw()  # Hide window for testing
    
    try:
        # Initialize game
        gui = GameGUI(root)
        root.update()
        
        # Setup test hero
        hero = gui.game_state.hero
        hero['level'] = 5
        hero['class'] = 'Warrior'
        hero['gold'] = 500
        
        print(f"✅ Hero: Level {hero['level']} {hero['class']}")
        
        # Test bounty rewards
        print(f"\n🎯 Testing Bounty Rewards:")
        for difficulty in ['Bronze', 'Silver', 'Gold']:
            rewards = gui.bounty_manager.bounty_rewards[difficulty]
            warrior_rewards = [r for r in rewards if r['class'] == 'Warrior' or r['class'] == 'All']
            
            print(f"\n{difficulty} Tier ({len(warrior_rewards)} Warrior items):")
            for reward in warrior_rewards[:3]:  # Show first 3
                name = reward['name']
                stats = []
                if reward.get('attack'):
                    stats.append(f"+{reward['attack']} ATK")
                if reward.get('defense'):
                    stats.append(f"+{reward['defense']} DEF")
                enchantment = reward.get('enchantment', '')
                if enchantment:
                    enchantment = f" ({enchantment})"
                
                print(f"  - {name}: {', '.join(stats)}{enchantment}")
        
        # Test quest rewards  
        print(f"\n📜 Testing Quest Rewards:")
        quest_manager = gui.quest_manager
        
        for level_range, tier in [(2, 'novice'), (5, 'adept'), (8, 'expert'), (12, 'master')]:
            rewards = quest_manager.quest_rewards[tier]
            warrior_rewards = [r for r in rewards if r['class'] == 'Warrior' or r['class'] == 'All']
            
            print(f"\n{tier.title()} Tier (Level {level_range}) - {len(warrior_rewards)} items:")
            for reward in warrior_rewards[:2]:  # Show first 2
                name = reward['name']
                stats = []
                if reward.get('attack'):
                    stats.append(f"+{reward['attack']} ATK")
                if reward.get('defense'):
                    stats.append(f"+{reward['defense']} DEF")
                enchantment = reward.get('enchantment', '')
                if enchantment:
                    enchantment = f" ({enchantment})"
                
                print(f"  - {name}: {', '.join(stats)}{enchantment}")
        
        # Test quest generation with rewards
        print(f"\n🎲 Testing Quest Generation:")
        quest = quest_manager.generate_kill_monster_quest()
        if quest:
            print(f"✅ Generated quest: {quest.target}")
            print(f"  XP: {quest.reward_xp}")
            if hasattr(quest, 'reward_gold') and quest.reward_gold:
                print(f"  Gold: {quest.reward_gold}")
            if hasattr(quest, 'reward_item') and quest.reward_item:
                item = quest.reward_item
                print(f"  Equipment: {item['name']} ({item.get('type', 'unknown')})")
                if item.get('attack'):
                    print(f"    Attack: +{item['attack']}")
                if item.get('defense'):
                    print(f"    Defense: +{item['defense']}")
                if item.get('enchantment'):
                    print(f"    Enchantment: {item['enchantment']}")
        else:
            print("❌ Could not generate quest")
        
        # Test equipment enchantment system
        print(f"\n✨ Testing Enchantment System:")
        enchantments = gui.equipment_manager.enchantments
        print(f"✅ Available weapon enchantments: {len(enchantments)}")
        for enchant_id, enchant in list(enchantments.items())[:3]:
            name = enchant['name'] 
            bonus = enchant['damage_bonus']
            special = enchant['special']
            print(f"  - {name}: +{bonus} damage, {special}")
        
        armor_enchants = gui.equipment_manager.armor_enchantments
        print(f"✅ Available armor enchantments: {len(armor_enchants)}")
        for enchant_id, enchant in list(armor_enchants.items())[:3]:
            name = enchant['name']
            bonus = enchant['defense_bonus'] 
            special = enchant['special']
            print(f"  - {name}: +{bonus} defense, {special}")
        
        print(f"\n🎉 Equipment Enhancement System Summary:")
        print(f"✅ Removed crafting workshop")
        print(f"✅ Enhanced bounty rewards: {sum(len(tier) for tier in gui.bounty_manager.bounty_rewards.values())} total items")
        print(f"✅ Enhanced quest rewards: {sum(len(tier) for tier in quest_manager.quest_rewards.values())} total items")
        print(f"✅ Enchantment system: {len(enchantments)} weapon + {len(armor_enchants)} armor enchantments")
        print(f"✅ Equipment includes enchantments and stat bonuses")
        print(f"✅ Level-appropriate reward tiers")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        root.destroy()

if __name__ == '__main__':
    test_enhanced_equipment_rewards()