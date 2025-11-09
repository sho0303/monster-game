#!/usr/bin/env python3
"""
Biome Debug Tool - Add this to help diagnose the biome monster selection issue

This tool adds debug output to the monster encounter system to help identify
when and why monsters from wrong biomes might be appearing.
"""

import sys
import os

def add_debug_mode():
    """Add debug output to the monster encounter system"""
    
    encounter_file = 'gui_monster_encounter.py'
    
    if not os.path.exists(encounter_file):
        print(f"Error: {encounter_file} not found!")
        return False
    
    # Read the current file
    with open(encounter_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if debug mode is already added
    if "BIOME_DEBUG_MODE = True" in content:
        print("Debug mode is already enabled!")
        return True
    
    # Add debug mode at the top of the file
    debug_import = '''
# BIOME DEBUG MODE - Remove this section when bug is fixed
BIOME_DEBUG_MODE = True
import datetime

def debug_log(message):
    """Log debug messages with timestamp"""
    if BIOME_DEBUG_MODE:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] BIOME DEBUG: {message}")

'''
    
    # Find the imports section and add our debug code
    if "import tkinter as tk" in content:
        content = content.replace("import tkinter as tk", debug_import + "import tkinter as tk")
    else:
        # Add at the beginning of the file after any existing comments
        lines = content.split('\n')
        insert_point = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith('#'):
                insert_point = i
                break
        lines.insert(insert_point, debug_import)
        content = '\n'.join(lines)
    
    # Now modify the _select_random_monster method to add debug output
    old_method_start = 'def _select_random_monster(self):'
    
    if old_method_start in content:
        # Find the method and add debug logging
        method_start = content.find(old_method_start)
        if method_start != -1:
            # Find the end of the method
            lines = content[method_start:].split('\n')
            indent = '        '  # 8 spaces for method indent
            
            # Insert debug logging at the start of the method
            debug_lines = [
                f'{indent}# DEBUG: Log encounter details',
                f'{indent}current_biome = getattr(self.gui, "current_biome", "grassland")',
                f'{indent}hero_level = self.gui.game_state.hero.get("level", 1)',
                f'{indent}debug_log(f"=== MONSTER ENCOUNTER STARTED ===")',
                f'{indent}debug_log(f"Current biome: {{current_biome}}")',
                f'{indent}debug_log(f"Hero level: {{hero_level}}")',
                f'{indent}debug_log(f"GUI type: {{type(self.gui).__name__}}")',
                '',
                f'{indent}import random'
            ]
            
            # Find where to insert (after the docstring)
            insert_pos = 1  # After the def line
            if '"""' in lines[1] or "'''" in lines[1]:
                # Skip docstring
                for i in range(2, len(lines)):
                    if '"""' in lines[i] or "'''" in lines[i]:
                        insert_pos = i + 1
                        break
            
            # Insert the debug lines
            for i, debug_line in enumerate(debug_lines):
                lines.insert(insert_pos + i, debug_line)
            
            # Reconstruct the content
            content = content[:method_start] + '\n'.join(lines)
    
    # Add debug output when a monster is selected
    old_return = 'return (key, monster_data)'
    new_return = '''debug_log(f"Selected monster: {key} (level {monster_data.get('level', '?')}, biome: {monster_data.get('biome', '?')})")
            debug_log(f"=== MONSTER ENCOUNTER COMPLETE ===")
            return (key, monster_data)'''
    
    content = content.replace(old_return, new_return)
    
    # Write the modified content back
    try:
        with open(encounter_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Debug mode added to {encounter_file}")
        print("\n🔍 Debug mode is now active!")
        print("   - Start the game and explore to see biome debug info")
        print("   - Look for lines starting with '[TIME] BIOME DEBUG:'")
        print("   - This will help identify when wrong-biome monsters appear")
        print("\n⚠️  To remove debug mode later, run: python remove_biome_debug.py")
        return True
        
    except Exception as e:
        print(f"❌ Error writing debug mode: {e}")
        return False

def create_removal_script():
    """Create a script to remove the debug mode"""
    removal_script = '''#!/usr/bin/env python3
"""Remove biome debug mode from gui_monster_encounter.py"""

import os

def remove_debug_mode():
    encounter_file = 'gui_monster_encounter.py'
    
    if not os.path.exists(encounter_file):
        print(f"Error: {encounter_file} not found!")
        return
    
    with open(encounter_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "BIOME_DEBUG_MODE = True" not in content:
        print("Debug mode is not currently enabled.")
        return
    
    # Remove debug imports and functions
    lines = content.split('\\n')
    cleaned_lines = []
    skip_mode = False
    
    for line in lines:
        if "# BIOME DEBUG MODE" in line:
            skip_mode = True
            continue
        elif skip_mode and (line.strip() == '' or line.startswith('BIOME_DEBUG_MODE') or line.startswith('import datetime') or 'def debug_log' in line or line.startswith('    """Log debug messages') or line.startswith('    if BIOME_DEBUG_MODE:') or line.startswith('        timestamp =') or line.startswith('        print(f"[{timestamp}]')):
            continue
        elif skip_mode and line.startswith('import tkinter as tk'):
            skip_mode = False
            cleaned_lines.append(line)
        elif not skip_mode:
            # Remove debug lines from the method
            if ('# DEBUG: Log encounter details' in line or
                'current_biome = getattr(self.gui, "current_biome"' in line or
                'hero_level = self.gui.game_state.hero.get("level"' in line or
                'debug_log(f"=== MONSTER ENCOUNTER' in line or
                'debug_log(f"Current biome:' in line or
                'debug_log(f"Hero level:' in line or
                'debug_log(f"GUI type:' in line or
                'debug_log(f"Selected monster:' in line):
                continue
            
            # Restore original return statement
            if 'debug_log(f"=== MONSTER ENCOUNTER COMPLETE ===' in line:
                continue
            if 'return (key, monster_data)' in line and 'debug_log' in line:
                cleaned_lines.append('            return (key, monster_data)')
                continue
                
            cleaned_lines.append(line)
    
    # Write cleaned content
    try:
        with open(encounter_file, 'w', encoding='utf-8') as f:
            f.write('\\n'.join(cleaned_lines))
        print(f"✅ Debug mode removed from {encounter_file}")
    except Exception as e:
        print(f"❌ Error removing debug mode: {e}")

if __name__ == '__main__':
    remove_debug_mode()
'''
    
    with open('remove_biome_debug.py', 'w', encoding='utf-8') as f:
        f.write(removal_script)

if __name__ == '__main__':
    print("🔧 Biome Debug Tool")
    print("==================")
    print("This tool will add debug output to help diagnose the biome monster selection issue.")
    print()
    
    success = add_debug_mode()
    if success:
        create_removal_script()
        print()
        print("📝 Next steps:")
        print("1. Run the game: python monster-game-gui.py")
        print("2. Load a save or start new game")
        print("3. Use the Explore button to encounter monsters")
        print("4. Check the console output for biome debug messages")
        print("5. When done, run: python remove_biome_debug.py")