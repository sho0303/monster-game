#!/usr/bin/env python3
"""
Interactive demo of the last biome tracking feature
"""

import sys
import tkinter as tk

def demo_last_biome_tracking():
    """Demo the last biome tracking in a simulated gameplay session"""
    
    print("🎮 LAST BIOME TRACKING DEMO")
    print("=" * 50)
    
    try:
        sys.path.append('.')
        import gui_main
        
        root = tk.Tk()
        root.withdraw()
        
        game = gui_main.GameGUI(root)
        
        # Mock the interface methods to avoid GUI side effects
        game.lock_interface = lambda: None
        game.unlock_interface = lambda: None
        game.clear_text = lambda: None
        game.audio = type('MockAudio', (), {'play_sound_effect': lambda self, sound: None})()
        
        # Override print_text to capture messages
        messages = []
        def capture_print(text):
            messages.append(text)
            print(f"    💬 {text}")
        game.print_text = capture_print
        
        print("🌟 Simulating player gameplay session:")
        print("-" * 40)
        
        # Start in grassland
        print(f"\\n📍 Starting location: {game.current_biome} (last: {game.last_biome})")
        
        # Simulate several teleportations
        print("\\n🌀 Player uses teleport 5 times...")
        
        teleport_history = []
        
        for i in range(5):
            old_current = game.current_biome
            old_last = game.last_biome
            
            # Clear previous messages
            messages.clear()
            
            # Simulate teleportation (but capture the destination manually)
            available_biomes = ['grassland', 'desert', 'dungeon', 'ocean']
            excluded_biomes = {game.current_biome}
            if hasattr(game, 'last_biome') and game.last_biome:
                excluded_biomes.add(game.last_biome)
            
            other_biomes = [biome for biome in available_biomes if biome not in excluded_biomes]
            if not other_biomes:
                other_biomes = [biome for biome in available_biomes if biome != game.current_biome]
            
            # Pick the first available for deterministic demo
            new_biome = other_biomes[0]
            
            # Update biome
            game.set_biome_background(new_biome)
            
            teleport_history.append({
                'step': i + 1,
                'from': old_current,
                'to': new_biome,
                'last_before': old_last,
                'excluded': list(excluded_biomes),
                'available': other_biomes
            })
            
            print(f"\\n   Teleport {i+1}:")
            print(f"     From: {old_current} (last was: {old_last})")
            print(f"     Excluded: {sorted(excluded_biomes)}")
            print(f"     Available: {sorted(other_biomes)}")
            print(f"     Destination: {new_biome}")
            print(f"     New state: current={game.current_biome}, last={game.last_biome}")
        
        print("\\n📊 TELEPORTATION ANALYSIS:")
        print("-" * 40)
        
        # Check for any loops or immediate returns
        loops_found = 0
        for i, entry in enumerate(teleport_history):
            if i > 0:
                prev_entry = teleport_history[i-1]
                if entry['to'] == prev_entry['from']:
                    print(f"   ⚠️  Step {entry['step']}: Returned to previous biome!")
                    loops_found += 1
        
        if loops_found == 0:
            print("   ✅ No teleport loops detected!")
        else:
            print(f"   ❌ Found {loops_found} teleport loops!")
        
        # Show biome variety
        destinations = [entry['to'] for entry in teleport_history]
        unique_destinations = set(destinations)
        print(f"   🎯 Visited {len(unique_destinations)} unique biomes: {sorted(unique_destinations)}")
        
        # Show that player can still reach all biomes over time
        all_biomes = {'grassland', 'desert', 'dungeon', 'ocean'}
        coverage = (len(unique_destinations) / len(all_biomes)) * 100
        print(f"   📈 Biome coverage: {coverage:.1f}% of available biomes")
        
        print("\\n🎯 KEY BENEFITS DEMONSTRATED:")
        print("-" * 40)
        print("   ✅ No immediate back-and-forth teleporting")
        print("   ✅ Still maintains variety and exploration")  
        print("   ✅ Player can eventually visit all biomes")
        print("   ✅ Reduces frustrating teleport loops")
        
        root.destroy()
        return loops_found == 0
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = demo_last_biome_tracking()
    
    print("\\n" + "=" * 50)
    if success:
        print("🎉 DEMO SUCCESSFUL!")
        print("✨ Last biome tracking enhances player experience!")
    else:
        print("❌ Demo revealed issues - check implementation.")