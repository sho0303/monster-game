"""
Save/Load system for the monster game using YAML
"""
import os
import sys
import yaml
from datetime import datetime
from pathlib import Path


class SaveLoadManager:
    """Manages saving and loading game states using YAML files"""
    
    def __init__(self, gui):
        self.gui = gui
        self.saves_dir = self._get_save_directory()
        self._ensure_saves_directory()
    
    def _get_save_directory(self):
        """Get the appropriate save directory based on how the game is running"""
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller executable - use persistent location
            # Try to use the directory where the exe is located
            exe_dir = Path(sys.executable).parent
            saves_dir = exe_dir / "saves"
            
            # If we can't write there (e.g., Program Files), use user's documents
            try:
                saves_dir.mkdir(exist_ok=True)
                test_file = saves_dir / ".write_test"
                test_file.touch()
                test_file.unlink()
                return saves_dir
            except (PermissionError, OSError):
                # Fall back to user's documents folder
                if os.name == 'nt':  # Windows
                    docs = Path.home() / "Documents" / "PyQuest Monster Game" / "saves"
                else:  # Linux/Mac
                    docs = Path.home() / ".pyquest" / "saves"
                return docs
        else:
            # Running from source - use local saves directory
            return Path("saves")
    
    def _ensure_saves_directory(self):
        """Create saves directory if it doesn't exist"""
        try:
            self.saves_dir.mkdir(exist_ok=True)
            # Create a README file to explain the save format
            readme_path = self.saves_dir / "README.txt"
            if not readme_path.exists():
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write("MonsterGame Save Files\n")
                    f.write("====================\n\n")
                    f.write("This directory contains YAML save files for the MonsterGame.\n")
                    f.write("Each save file preserves the complete hero state including:\n")
                    f.write("- Hero stats (level, HP, attack, defense, etc.)\n")
                    f.write("- Inventory and equipment\n")
                    f.write("- Active quests and progress\n")
                    f.write("- Current game location and biome\n")
                    f.write("- Play statistics\n\n")
                    f.write("Save files are in YAML format for easy reading and debugging.\n")
        except Exception as e:
            print(f"Warning: Could not create saves directory: {e}")
    
    def get_available_saves(self):
        """Get list of available save files"""
        try:
            save_files = []
            for file_path in self.saves_dir.glob("*.yaml"):
                try:
                    # Load basic info from save file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        save_data = yaml.safe_load(f)
                    
                    save_info = {
                        'filename': file_path.name,
                        'path': file_path,
                        'hero_name': save_data.get('hero', {}).get('name', 'Unknown'),
                        'hero_class': save_data.get('hero', {}).get('class', 'Unknown'),
                        'level': save_data.get('hero', {}).get('level', 1),
                        'save_date': save_data.get('save_metadata', {}).get('save_date', 'Unknown'),
                        'current_biome': save_data.get('game_state', {}).get('current_biome', 'grassland')
                    }
                    save_files.append(save_info)
                except Exception as e:
                    print(f"Warning: Could not read save file {file_path}: {e}")
            
            # Sort by save date (most recent first)
            save_files.sort(key=lambda x: x['save_date'], reverse=True)
            return save_files
        except Exception as e:
            print(f"Error getting save files: {e}")
            return []
    
    def save_game(self, hero, current_biome=None, save_name=None):
        """Save current game state to YAML file"""
        try:
            # Generate save name if not provided
            if save_name is None:
                hero_name = hero.get('name', 'Hero')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_name = f"{hero_name}_{timestamp}.yaml"
            elif not save_name.endswith('.yaml'):
                save_name += '.yaml'
            
            # Prepare save data structure
            save_data = {
                'hero': self._prepare_hero_data(hero),
                'game_state': {
                    'current_biome': current_biome or getattr(self.gui, 'current_biome', 'grassland'),
                    'last_biome': getattr(self.gui, 'last_biome', 'grassland')
                },
                'bounties': self._prepare_bounty_data(),
                'achievements': self._prepare_achievement_data(),
                'save_metadata': {
                    'save_date': datetime.now().isoformat(),
                    'game_version': '1.0',
                    'save_name': save_name
                }
            }
            
            # Save to file
            save_path = self.saves_dir / save_name
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(save_data, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            return {
                'success': True,
                'filename': save_name,
                'path': save_path
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def load_game(self, save_path):
        """Load game state from YAML file"""
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = yaml.safe_load(f)
            
            # Validate save data structure
            if not isinstance(save_data, dict):
                raise ValueError("Invalid save file format")
            
            if 'hero' not in save_data:
                raise ValueError("Save file missing hero data")
            
            # Extract data
            hero_data = save_data['hero']
            game_state = save_data.get('game_state', {})
            bounty_data = save_data.get('bounties', {})
            save_metadata = save_data.get('save_metadata', {})
            
            # Ensure hero has all required fields
            hero_data = self._validate_hero_data(hero_data)
            
            return {
                'success': True,
                'hero': hero_data,
                'current_biome': game_state.get('current_biome', 'grassland'),
                'last_biome': game_state.get('last_biome', 'grassland'),
                'bounties': bounty_data,
                'achievements': save_data.get('achievements', {'achievements': [], 'player_stats': {}}),
                'save_metadata': save_metadata
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_save(self, save_path):
        """Delete a save file"""
        try:
            if isinstance(save_path, str):
                save_path = Path(save_path)
            
            if save_path.exists():
                save_path.unlink()
                return {'success': True}
            else:
                return {'success': False, 'error': 'Save file not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _prepare_hero_data(self, hero):
        """Prepare hero data for saving, ensuring all fields are serializable"""
        # Create a clean copy of hero data
        hero_data = {}
        
        # Copy all basic fields
        basic_fields = ['name', 'class', 'level', 'xp', 'hp', 'maxhp', 'attack', 'defense', 
                       'gold', 'lives_left', 'age', 'weapon', 'armour']
        
        for field in basic_fields:
            if field in hero:
                hero_data[field] = hero[field]
        
        # Handle items - ensure they're serializable (new multi-item system)
        if 'items' in hero and hero['items']:
            hero_data['items'] = {}
            for item_name, item_info in hero['items'].items():
                hero_data['items'][item_name] = {
                    'data': dict(item_info['data']),
                    'quantity': item_info['quantity']
                }
        else:
            hero_data['items'] = {}
        
        # Handle legacy single item - migrate to new system
        if 'item' in hero and hero['item'] is not None:
            if not hero_data['items']:
                hero_data['items'] = {}
            old_item = hero['item']
            item_name = old_item['name']
            hero_data['items'][item_name] = {'data': dict(old_item), 'quantity': 1}
            hero_data['item'] = None  # Clear legacy field
        else:
            hero_data['item'] = None
        
        # Handle quests - ensure they're serializable
        if 'quests' in hero and hero['quests']:
            hero_data['quests'] = []
            for quest in hero['quests']:
                if hasattr(quest, '__dict__'):
                    # Convert quest object to dictionary
                    quest_dict = {
                        'quest_type': quest.quest_type,
                        'target': quest.target,
                        'description': quest.description,
                        'reward_xp': quest.reward_xp,
                        'completed': getattr(quest, 'completed', False),
                        'status': getattr(quest, 'status', 'active')
                    }
                    hero_data['quests'].append(quest_dict)
                else:
                    # Already a dictionary
                    hero_data['quests'].append(dict(quest))
        else:
            hero_data['quests'] = []
        
        return hero_data
    
    def _prepare_bounty_data(self):
        """Prepare bounty data for saving"""
        if not hasattr(self.gui, 'bounty_manager'):
            return {'available': [], 'active': []}
        
        bounty_manager = self.gui.bounty_manager
        
        # Serialize available bounties
        available_bounties = []
        for bounty in bounty_manager.available_bounties:
            available_bounties.append(bounty.to_dict())
        
        # Serialize active bounties
        active_bounties = []
        for bounty in bounty_manager.active_bounties:
            active_bounties.append(bounty.to_dict())
        
        return {
            'available': available_bounties,
            'active': active_bounties
        }
    
    def _prepare_achievement_data(self):
        """Prepare achievement data for saving"""
        if not hasattr(self.gui, 'achievement_manager'):
            return {'achievements': [], 'player_stats': {}}
        
        achievement_manager = self.gui.achievement_manager
        
        # Serialize achievements - achievements is a dictionary, not a list
        achievements_data = []
        for achievement_id, achievement in achievement_manager.achievements.items():
            achievements_data.append({
                'id': achievement.id,
                'name': achievement.name,
                'description': achievement.description,
                'category': achievement.category,
                'target_value': achievement.target_value,
                'current_progress': achievement.current_progress,
                'completed': achievement.completed,
                'completed_at': achievement.completed_at,
                'hidden': achievement.hidden,
                'unlocked': achievement.unlocked,
                'reward_type': achievement.reward_type,
                'reward_value': achievement.reward_value
            })
        
        return {
            'achievements': achievements_data,
            'player_stats': achievement_manager.player_stats
        }
    
    def _validate_hero_data(self, hero_data):
        """Validate and fill in missing hero data fields with defaults"""
        # Default values for all hero fields
        defaults = {
            'name': 'Unknown Hero',
            'class': 'Warrior',
            'level': 1,
            'xp': 0,
            'hp': 15,
            'maxhp': 15,
            'attack': 5,
            'defense': 5,
            'gold': 50,
            'lives_left': 3,
            'age': 25,
            'weapon': 'Basic Weapon',
            'armour': 'Basic Armour',
            'item': None,
            'items': {},
            'quests': []
        }
        
        # Fill in missing fields
        validated_data = defaults.copy()
        validated_data.update(hero_data)
        
        # Ensure numeric fields are actually numeric
        numeric_fields = ['level', 'xp', 'hp', 'maxhp', 'attack', 'defense', 'gold', 'lives_left', 'age']
        for field in numeric_fields:
            try:
                validated_data[field] = int(validated_data[field])
            except (ValueError, TypeError):
                validated_data[field] = defaults[field]
        
        # Ensure quests is a list
        if not isinstance(validated_data['quests'], list):
            validated_data['quests'] = []
        
        # Migrate old single item system to new multi-item system
        if 'item' in validated_data and validated_data['item'] is not None:
            if 'items' not in validated_data or not validated_data['items']:
                validated_data['items'] = {}
            old_item = validated_data['item']
            if isinstance(old_item, dict) and 'name' in old_item:
                item_name = old_item['name']
                validated_data['items'][item_name] = {'data': old_item, 'quantity': 1}
            validated_data['item'] = None  # Clear legacy field
        
        # Ensure items is a dictionary
        if 'items' not in validated_data or not isinstance(validated_data['items'], dict):
            validated_data['items'] = {}
        
        return validated_data
    
    def show_save_interface(self):
        """Display save game interface"""
        self.gui.clear_text()
        self.gui.print_text("💾 SAVE GAME 💾\n")
        
        # Show save location
        save_location_parts = [
            ("Save Location: ", "#888888"),
            (str(self.saves_dir.absolute()), "#00aaff")
        ]
        self.gui._print_colored_parts(save_location_parts)
        self.gui.print_text("")
        
        hero = self.gui.game_state.hero
        hero_name = hero.get('name', 'Hero')
        hero_level = hero.get('level', 1)
        current_biome = getattr(self.gui, 'current_biome', 'grassland')
        
        # Show current game info
        save_info_parts = [
            ("Current Hero: ", "#ffffff"),
            (f"{hero_name} (Level {hero_level})", "#ffaa00"),
            (f" in {current_biome.title()}", "#00ff00")
        ]
        self.gui._print_colored_parts(save_info_parts)
        
        # Generate default save name
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        default_name = f"{hero_name}_L{hero_level}_{current_biome}"
        
        self.gui.print_text(f"\nSave as: {default_name}.yaml")
        self.gui.print_text("Save location: saves/")
        
        # Show existing saves
        existing_saves = self.get_available_saves()
        if existing_saves:
            self.gui.print_text(f"\nExisting saves ({len(existing_saves)}):")
            for i, save_info in enumerate(existing_saves[:5], 1):  # Show up to 5 recent saves
                save_display_parts = [
                    (f"  {i}. ", "#888888"),
                    (save_info['hero_name'], "#ffaa00"),
                    (f" L{save_info['level']}", "#00aaff"),
                    (f" ({save_info['current_biome']})", "#00ff00"),
                    (f" - {save_info['save_date'][:10]}", "#888888")
                ]
                self.gui._print_colored_parts(save_display_parts)
        
        self.gui.print_text("\nProceed with save?")
        
        def on_save_choice(choice):
            if choice == 1:
                # Perform save
                result = self.save_game(hero, current_biome, default_name)
                
                if result['success']:
                    success_parts = [
                        ("✅ Game saved successfully! ", "#00ff00"),
                        (f"File: {result['filename']}", "#ffffff")
                    ]
                    self.gui._print_colored_parts(success_parts)
                    self.gui.audio.play_sound_effect('success.mp3')  # Play success sound if available
                else:
                    error_parts = [
                        ("❌ Save failed: ", "#ff6666"),
                        (result['error'], "#ffffff")
                    ]
                    self.gui._print_colored_parts(error_parts)
                
                self.gui.root.after(2500, self.gui.main_menu)
            else:
                # Cancel save
                self.gui.main_menu()
        
        self.gui.set_buttons(["💾 Save Game", "❌ Cancel"], on_save_choice)
    
    def show_load_interface(self):
        """Display load game interface"""
        self.gui.clear_text()
        self.gui.print_text("📁 LOAD SAVED GAME 📁\n")
        
        # Get available saves
        available_saves = self.get_available_saves()
        
        if not available_saves:
            self.gui.print_text("No saved games found.")
            self.gui.print_text("Create a new hero to start playing!")
            
            def on_no_saves_choice(choice):
                if choice == 1:
                    self.gui.select_hero()
                
            self.gui.set_buttons(["🔙 Back to Hero Selection"], on_no_saves_choice)
            return
        
        # Display available saves
        self.gui.print_text(f"Found {len(available_saves)} saved game(s):\n")
        
        for i, save_info in enumerate(available_saves[:10], 1):  # Show up to 10 saves
            # Format save date for display
            try:
                save_date = datetime.fromisoformat(save_info['save_date'])
                date_str = save_date.strftime("%Y-%m-%d %H:%M")
            except:
                date_str = save_info['save_date'][:16] if len(save_info['save_date']) > 16 else save_info['save_date']
            
            save_display_parts = [
                (f"{i}. ", "#ffffff"),
                (save_info['hero_name'], "#ffaa00"),
                (f" (Level {save_info['level']} {save_info['hero_class']})", "#00aaff"),
                (f" - {save_info['current_biome'].title()}", "#00ff00"),
                (f"\n   Saved: {date_str}", "#888888")
            ]
            self.gui._print_colored_parts(save_display_parts)
            self.gui.print_text("")  # Add spacing
        
        self.gui.print_text("Select a save file to load:")
        
        def on_load_choice(choice):
            if choice <= len(available_saves):
                # Load selected save
                save_info = available_saves[choice - 1]
                result = self.load_game(save_info['path'])
                
                if result['success']:
                    # Successfully loaded - set up game state
                    self.gui.game_state.hero = result['hero']
                    
                    # Restore biome and last biome
                    if hasattr(self.gui, 'set_biome_background'):
                        # Restore last_biome first to maintain proper tracking
                        if 'last_biome' in result:
                            self.gui.last_biome = result['last_biome']
                        self.gui.set_biome_background(result['current_biome'])
                    
                    # Reinitialize quest system with loaded quests
                    if hasattr(self.gui, 'quest_manager'):
                        self.gui.quest_manager.initialize_hero_quests(self.gui.game_state.hero)
                    
                    # Restore bounty data
                    if hasattr(self.gui, 'bounty_manager') and 'bounties' in result:
                        self.gui.bounty_manager.load_bounties(result['bounties'])
                    
                    # Restore achievement data
                    if hasattr(self.gui, 'achievement_manager') and 'achievements' in result:
                        self.gui.achievement_manager.load_achievements(result['achievements'])
                    
                    # Show success message
                    load_parts = [
                        ("✅ Game loaded successfully! ", "#00ff00"),
                        (f"Welcome back, {result['hero']['name']}!", "#ffaa00")
                    ]
                    self.gui._print_colored_parts(load_parts)
                    
                    # Go to main menu
                    self.gui.root.after(2000, self.gui.main_menu)
                else:
                    # Load failed
                    error_parts = [
                        ("❌ Load failed: ", "#ff6666"),
                        (result['error'], "#ffffff")
                    ]
                    self.gui._print_colored_parts(error_parts)
                    self.gui.root.after(3000, self.show_load_interface)
            else:
                # Back to hero selection
                self.gui.select_hero()
        
        # Create buttons for each save + back button
        buttons = [f"📁 Load Save {i}" for i in range(1, min(len(available_saves) + 1, 11))]
        buttons.append("🔙 Back")
        
        self.gui.set_buttons(buttons, on_load_choice)