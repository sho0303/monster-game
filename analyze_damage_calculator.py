#!/usr/bin/env python3
"""
Damage Calculator Analysis and Improvement Suggestions
"""

import random
import math

def current_damage_calculator(attack: int, defense: int) -> int:
    """Current damage calculation system"""
    strike = random.randint(1, max(1, attack)) * 2
    damage = strike - defense
    return max(1, damage)

def analyze_current_system():
    """Analyze the current damage calculation system"""
    
    print("🔍 CURRENT DAMAGE CALCULATOR ANALYSIS")
    print("=" * 80)
    
    # Hero stats (from YAML files)
    heroes = {
        'Billy (Ninja)': {'attack': 5, 'defense': 10, 'hp': 15, 'level': 1},
        'Dan (Warrior)': {'attack': 10, 'defense': 5, 'hp': 15, 'level': 1},
        'Eduardo (Magician)': {'attack': 15, 'defense': 5, 'hp': 10, 'level': 1}
    }
    
    # Monster stats (from YAML files)
    monsters = {
        'Bunny': {'attack': 1, 'defense': 1, 'hp': 8, 'level': 1},
        'Slime': {'attack': 1, 'defense': 6, 'hp': 3, 'level': 1}, 
        'Cyclops': {'attack': 7, 'defense': 10, 'hp': 55, 'level': 5},
        'Demon': {'attack': 22, 'defense': 15, 'hp': 85, 'level': 8},
        'Lich': {'attack': 25, 'defense': 5, 'hp': 99, 'level': 7},
        'Wyvern': {'attack': 19, 'defense': 10, 'hp': 107, 'level': 7}
    }
    
    print("📊 DAMAGE RANGE ANALYSIS:")
    print("-" * 50)
    
    for hero_name, hero in heroes.items():
        print(f"\\n👤 {hero_name} (ATK: {hero['attack']}, DEF: {hero['defense']}):")
        
        for monster_name, monster in monsters.items():
            # Calculate damage ranges (100 simulations)
            hero_damages = []
            monster_damages = []
            
            for _ in range(100):
                hero_dmg = current_damage_calculator(hero['attack'], monster['defense'])
                monster_dmg = current_damage_calculator(monster['attack'], hero['defense'])
                hero_damages.append(hero_dmg)
                monster_damages.append(monster_dmg)
            
            hero_avg = sum(hero_damages) / len(hero_damages)
            monster_avg = sum(monster_damages) / len(monster_damages)
            
            hero_range = f"{min(hero_damages)}-{max(hero_damages)}"
            monster_range = f"{min(monster_damages)}-{max(monster_damages)}"
            
            print(f"  vs {monster_name} (L{monster['level']}): Hero {hero_range} avg({hero_avg:.1f}) | Monster {monster_range} avg({monster_avg:.1f})")
    
    print("\\n⚠️  IDENTIFIED PROBLEMS:")
    print("-" * 50)
    print("1. 🎲 EXTREME RANDOMNESS: Damage varies from 1 to (attack*2 - defense)")
    print("   - Eduardo vs Bunny: 1-29 damage (2900% variance!)")
    print("   - Makes combat unpredictable and frustrating")
    
    print("\\n2. 🛡️ DEFENSE SCALING ISSUES:")
    print("   - High defense can completely negate attacks")
    print("   - Low attack vs high defense = always 1 damage")
    print("   - Slime (6 defense) nearly immune to Billy (5 attack)")
    
    print("\\n3. 📈 NO LEVEL CONSIDERATION:")
    print("   - Level 1 hero vs Level 8 monster uses same formula")
    print("   - No experience/skill advantage modeled")
    print("   - High-level monsters not appropriately challenging")
    
    print("\\n4. ⚔️ COMBAT DURATION ISSUES:")
    print("   - Some fights end in 1-2 hits due to lucky rolls")
    print("   - Other fights drag on with minimum damage")
    print("   - No tactical depth or strategy")

def improved_damage_calculator_v1(attacker_attack: int, defender_defense: int, 
                                attacker_level: int = 1, defender_level: int = 1) -> int:
    """Improved damage calculator with level consideration and reduced variance"""
    
    # Base damage with reduced randomness (70-130% of attack instead of 100-200%)
    base_roll = random.uniform(0.7, 1.3)
    base_damage = attacker_attack * base_roll
    
    # Level differential bonus/penalty (±10% per level difference)
    level_diff = attacker_level - defender_level
    level_modifier = 1.0 + (level_diff * 0.1)
    base_damage *= level_modifier
    
    # Defense reduction (diminishing returns - not linear)
    # Uses square root to prevent complete immunity
    defense_reduction = math.sqrt(defender_defense) * 1.5
    final_damage = base_damage - defense_reduction
    
    # Minimum damage based on level (prevents stalemates)
    min_damage = max(1, attacker_level)
    
    return max(min_damage, int(final_damage))

def improved_damage_calculator_v2(attacker_attack: int, defender_defense: int,
                                attacker_level: int = 1, defender_level: int = 1) -> int:
    """Alternative improved calculator with percentage-based defense"""
    
    # Base damage with moderate randomness (80-120% of attack)
    variance = random.uniform(0.8, 1.2)
    base_damage = attacker_attack * variance
    
    # Level scaling (exponential growth, but controlled)
    level_bonus = (attacker_level ** 1.2) / (defender_level ** 1.1)
    base_damage *= level_bonus
    
    # Defense as damage reduction percentage (capped at 80% reduction)
    defense_percentage = min(0.8, defender_defense / (defender_defense + 20))
    final_damage = base_damage * (1 - defense_percentage)
    
    # Minimum damage scales with attacker level
    min_damage = max(1, attacker_level // 2 + 1)
    
    return max(min_damage, int(final_damage))

def compare_damage_systems():
    """Compare current vs improved damage systems"""
    
    print("\\n🔄 DAMAGE SYSTEM COMPARISON")
    print("=" * 80)
    
    # Test scenario: Level 1 Hero vs Level 5 Monster
    hero_stats = {'attack': 10, 'defense': 5, 'level': 1}
    monster_stats = {'attack': 7, 'defense': 10, 'level': 5}
    
    systems = {
        'Current': lambda a, d, al, dl: current_damage_calculator(a, d),
        'Improved V1': improved_damage_calculator_v1,
        'Improved V2': improved_damage_calculator_v2
    }
    
    print(f"Test: Hero L{hero_stats['level']} (ATK{hero_stats['attack']}/DEF{hero_stats['defense']}) vs Monster L{monster_stats['level']} (ATK{monster_stats['attack']}/DEF{monster_stats['defense']})")
    print("-" * 80)
    
    for system_name, calc_func in systems.items():
        hero_damages = []
        monster_damages = []
        
        for _ in range(1000):  # Large sample for accuracy
            hero_dmg = calc_func(hero_stats['attack'], monster_stats['defense'], 
                               hero_stats['level'], monster_stats['level'])
            monster_dmg = calc_func(monster_stats['attack'], hero_stats['defense'],
                                  monster_stats['level'], hero_stats['level'])
            hero_damages.append(hero_dmg)
            monster_damages.append(monster_dmg)
        
        hero_avg = sum(hero_damages) / len(hero_damages)
        monster_avg = sum(monster_damages) / len(monster_damages)
        hero_range = f"{min(hero_damages)}-{max(hero_damages)}"
        monster_range = f"{min(monster_damages)}-{max(monster_damages)}"
        
        # Calculate variance (lower is more consistent)
        hero_variance = max(hero_damages) / min(hero_damages) if min(hero_damages) > 0 else float('inf')
        monster_variance = max(monster_damages) / min(monster_damages) if min(monster_damages) > 0 else float('inf')
        
        print(f"{system_name:12} | Hero: {hero_range:6} avg({hero_avg:4.1f}) var({hero_variance:4.1f}x) | Monster: {monster_range:6} avg({monster_avg:4.1f}) var({monster_variance:4.1f}x)")

def suggest_implementation():
    """Suggest specific implementation improvements"""
    
    print("\\n💡 IMPLEMENTATION SUGGESTIONS")
    print("=" * 80)
    
    print("🎯 RECOMMENDED APPROACH: Improved V2")
    print("-" * 40)
    print("✅ Reduces variance from 2900% to ~50%")
    print("✅ Level differential creates meaningful progression")
    print("✅ Percentage-based defense prevents immunity")
    print("✅ Minimum damage scales with level")
    print("✅ Maintains tactical depth without extreme swings")
    
    print("\\n🔧 SPECIFIC CHANGES NEEDED:")
    print("-" * 40)
    print("1. Update game_logic.py damage_calculator() function")
    print("2. Update gui_combat.py calculate_damage() method")
    print("3. Add level parameters to damage calculations")
    print("4. Test with existing hero/monster balance")
    print("5. Adjust monster levels if needed for progression")
    
    print("\\n⚖️  BALANCE RECOMMENDATIONS:")
    print("-" * 40)
    print("🏆 Hero Progression:")
    print("   - Billy (Ninja): High defense, moderate attack - defensive playstyle")
    print("   - Dan (Warrior): Balanced attack/defense - reliable damage")
    print("   - Eduardo (Magician): High attack, low defense - glass cannon")
    
    print("\\n👹 Monster Scaling:")
    print("   - Early monsters (L1-2): 1-3 attack, 1-5 defense")
    print("   - Mid monsters (L3-5): 5-10 attack, 5-12 defense") 
    print("   - Late monsters (L6-8): 15-25 attack, 8-15 defense")
    print("   - Boss monsters: Higher HP, moderate attack/defense")
    
    print("\\n📈 Expected Combat Flow:")
    print("-" * 40)
    print("   - Early game: 3-5 rounds per fight")
    print("   - Mid game: 4-8 rounds per fight") 
    print("   - Late game: 6-12 rounds per fight")
    print("   - Boss fights: 10-20 rounds")
    print("   - Damage variance: ±25% instead of ±100%")

if __name__ == '__main__':
    analyze_current_system()
    compare_damage_systems() 
    suggest_implementation()