"""
Enhanced Equipment and Customization System
"""
import json
import random


class EquipmentManager:
    """Manages enhanced weapon and armor customization"""
    
    def __init__(self, gui):
        self.gui = gui
        
        # Enchantment types and their effects
        self.enchantments = {
            'fire': {'name': 'Fire', 'damage_bonus': 3, 'special': 'burn_chance', 'color': '#ff4444'},
            'ice': {'name': 'Ice', 'damage_bonus': 2, 'special': 'slow_chance', 'color': '#4488ff'},
            'lightning': {'name': 'Lightning', 'damage_bonus': 4, 'special': 'crit_chance', 'color': '#ffff44'},
            'poison': {'name': 'Poison', 'damage_bonus': 2, 'special': 'poison_chance', 'color': '#44ff44'},
            'shadow': {'name': 'Shadow', 'damage_bonus': 3, 'special': 'miss_chance', 'color': '#8844ff'},
            'holy': {'name': 'Holy', 'damage_bonus': 5, 'special': 'heal_chance', 'color': '#ffaa44'},
        }
        
        # Armor enchantments
        self.armor_enchantments = {
            'reinforced': {'name': 'Reinforced', 'defense_bonus': 3, 'special': 'damage_reduction'},
            'magical': {'name': 'Magical', 'defense_bonus': 2, 'special': 'mana_regen'},
            'blessed': {'name': 'Blessed', 'defense_bonus': 4, 'special': 'holy_protection'},
            'draconic': {'name': 'Draconic', 'defense_bonus': 5, 'special': 'fire_immunity'},
            'spectral': {'name': 'Spectral', 'defense_bonus': 3, 'special': 'dodge_chance'},
        }
        
        # Upgrade levels for equipment
        self.upgrade_levels = {
            0: {'name': '', 'multiplier': 1.0, 'cost_multiplier': 1.0},
            1: {'name': '+1', 'multiplier': 1.2, 'cost_multiplier': 2.0},
            2: {'name': '+2', 'multiplier': 1.4, 'cost_multiplier': 3.0},
            3: {'name': '+3', 'multiplier': 1.6, 'cost_multiplier': 4.0},
            4: {'name': '+4', 'multiplier': 1.8, 'cost_multiplier': 5.0},
            5: {'name': '+5', 'multiplier': 2.0, 'cost_multiplier': 6.0},
        }
        
        # Gem slots and effects
        self.gems = {
            'ruby': {'name': 'Ruby', 'effect': 'attack', 'bonus': 2, 'color': '#ff0000'},
            'sapphire': {'name': 'Sapphire', 'effect': 'defense', 'bonus': 2, 'color': '#0066ff'},
            'emerald': {'name': 'Emerald', 'effect': 'hp', 'bonus': 5, 'color': '#00ff00'},
            'diamond': {'name': 'Diamond', 'effect': 'all_stats', 'bonus': 1, 'color': '#ffffff'},
            'onyx': {'name': 'Onyx', 'effect': 'crit_damage', 'bonus': 10, 'color': '#444444'},
            'topaz': {'name': 'Topaz', 'effect': 'gold_bonus', 'bonus': 15, 'color': '#ffaa00'},
        }
    
    def show_equipment_menu(self):
        """Show the main equipment customization menu"""
        self.gui.clear_text()
        self.gui.set_background_image('art/blacksmith_background.png')
        
        self.gui.print_text("⚒️  EQUIPMENT CUSTOMIZATION  ⚒️")
        self.gui.print_text("=" * 60)
        
        hero = self.gui.game_state.hero
        
        # Show current equipment
        self._display_current_equipment()
        
        self.gui.print_text("\n🔧 What would you like to do?")
        
        menu_options = [
            "⚔️ Upgrade Weapon",
            "🛡️ Upgrade Armor", 
            "✨ Add Enchantment",
            "💎 Socket Gems",
            "🔍 View Equipment Details",
            "🏠 Back to Town"
        ]
        
        def on_menu_choice(choice):
            if choice == 1:
                self._show_weapon_upgrade()
            elif choice == 2:
                self._show_armor_upgrade()
            elif choice == 3:
                self._show_enchantment_menu()
            elif choice == 4:
                self._show_gem_socketing()
            elif choice == 5:
                self._show_equipment_details()
            elif choice == 6:
                self.gui.town.enter_town()
        
        self.gui.set_buttons(menu_options, on_menu_choice)
    
    def _display_current_equipment(self):
        """Display hero's current equipment with enhancements"""
        hero = self.gui.game_state.hero
        
        # Initialize equipment data if not exists
        if 'equipment_data' not in hero:
            hero['equipment_data'] = {}
        
        # Current weapon
        weapon_name = hero.get('weapon', 'None')
        weapon_data = hero['equipment_data'].get('weapon', {})
        
        self.gui.print_text(f"\n⚔️ Current Weapon: {self._format_equipment_name(weapon_name, weapon_data)}")
        if weapon_name != 'None':
            self._print_equipment_stats('weapon', weapon_data)
        
        # Current armor
        armor_name = hero.get('armour', 'None')
        armor_data = hero['equipment_data'].get('armor', {})
        
        self.gui.print_text(f"\n🛡️ Current Armor: {self._format_equipment_name(armor_name, armor_data)}")
        if armor_name != 'None':
            self._print_equipment_stats('armor', armor_data)
        
        # Show gold
        gold_parts = [
            ("\n💰 Gold: ", "#ffffff"),
            (str(hero.get('gold', 0)), "#ffdd00")
        ]
        self.gui._print_colored_parts(gold_parts)
    
    def _format_equipment_name(self, base_name, equipment_data):
        """Format equipment name with upgrades and enchantments"""
        if base_name == 'None':
            return base_name
        
        formatted_name = base_name
        
        # Add upgrade level
        upgrade_level = equipment_data.get('upgrade_level', 0)
        if upgrade_level > 0:
            upgrade_info = self.upgrade_levels[upgrade_level]
            formatted_name = f"{formatted_name} {upgrade_info['name']}"
        
        # Add enchantment
        enchantment = equipment_data.get('enchantment')
        if enchantment:
            enchant_info = self.enchantments.get(enchantment) or self.armor_enchantments.get(enchantment)
            if enchant_info:
                formatted_name = f"{enchant_info['name']} {formatted_name}"
        
        return formatted_name
    
    def _print_equipment_stats(self, equipment_type, equipment_data):
        """Print detailed equipment statistics"""
        hero = self.gui.game_state.hero
        
        if equipment_type == 'weapon':
            base_attack = self._get_base_weapon_attack()
            total_attack = self._calculate_weapon_attack(equipment_data)
            
            stats_parts = [
                ("   Attack: ", "#ffffff"),
                (str(base_attack), "#cccccc"),
                (" → ", "#ffffff"),
                (str(total_attack), "#ff4444")
            ]
            self.gui._print_colored_parts(stats_parts)
            
        elif equipment_type == 'armor':
            base_defense = self._get_base_armor_defense()
            total_defense = self._calculate_armor_defense(equipment_data)
            
            stats_parts = [
                ("   Defense: ", "#ffffff"),
                (str(base_defense), "#cccccc"),
                (" → ", "#ffffff"),
                (str(total_defense), "#4444ff")
            ]
            self.gui._print_colored_parts(stats_parts)
        
        # Show gems if any
        gems = equipment_data.get('gems', [])
        if gems:
            gem_text = "   Gems: "
            for gem in gems:
                gem_info = self.gems.get(gem)
                if gem_info:
                    gem_text += f"💎{gem_info['name']} "
            self.gui.print_text(gem_text)
        
        # Show special effects
        enchantment = equipment_data.get('enchantment')
        if enchantment:
            enchant_info = self.enchantments.get(enchantment) or self.armor_enchantments.get(enchantment)
            if enchant_info and 'special' in enchant_info:
                self.gui.print_text(f"   Special: {enchant_info['special'].replace('_', ' ').title()}")
    
    def _show_weapon_upgrade(self):
        """Show weapon upgrade options"""
        hero = self.gui.game_state.hero
        weapon_name = hero.get('weapon', 'None')
        
        if weapon_name == 'None':
            self.gui.clear_text()
            self.gui.print_text("❌ You need to equip a weapon first!")
            self.gui.print_text("Visit the shop to purchase a weapon.")
            self.gui.root.after(3000, self.show_equipment_menu)
            return
        
        self.gui.clear_text()
        self.gui.print_text("⚔️ WEAPON UPGRADE ⚔️")
        self.gui.print_text("=" * 40)
        
        if 'equipment_data' not in hero:
            hero['equipment_data'] = {}
        if 'weapon' not in hero['equipment_data']:
            hero['equipment_data']['weapon'] = {}
        
        weapon_data = hero['equipment_data']['weapon']
        current_level = weapon_data.get('upgrade_level', 0)
        
        # Show current weapon stats
        self.gui.print_text(f"\nCurrent Weapon: {self._format_equipment_name(weapon_name, weapon_data)}")
        self._print_equipment_stats('weapon', weapon_data)
        
        if current_level >= 5:
            self.gui.print_text(f"\n✨ Weapon is already at maximum upgrade level!")
            self.gui.root.after(3000, self.show_equipment_menu)
            return
        
        # Show upgrade options
        next_level = current_level + 1
        next_upgrade = self.upgrade_levels[next_level]
        
        base_cost = 100
        upgrade_cost = int(base_cost * next_upgrade['cost_multiplier'])
        
        self.gui.print_text(f"\n🔧 Upgrade to {weapon_name} {next_upgrade['name']}:")
        self.gui.print_text(f"   💰 Cost: {upgrade_cost} gold")
        
        new_attack = self._calculate_weapon_attack({
            **weapon_data,
            'upgrade_level': next_level
        })
        current_attack = self._calculate_weapon_attack(weapon_data)
        
        attack_parts = [
            ("   Attack: ", "#ffffff"),
            (str(current_attack), "#cccccc"),
            (" → ", "#ffffff"),
            (str(new_attack), "#ff4444")
        ]
        self.gui._print_colored_parts(attack_parts)
        
        # Check if player can afford it
        player_gold = hero.get('gold', 0)
        if player_gold >= upgrade_cost:
            upgrade_options = [
                f"⚒️ Upgrade for {upgrade_cost} gold",
                "🔙 Back to Equipment Menu"
            ]
        else:
            upgrade_options = [
                f"❌ Not enough gold (need {upgrade_cost})",
                "🔙 Back to Equipment Menu"
            ]
        
        def on_upgrade_choice(choice):
            if choice == 1 and player_gold >= upgrade_cost:
                self._perform_weapon_upgrade(upgrade_cost, next_level)
            else:
                self.show_equipment_menu()
        
        self.gui.set_buttons(upgrade_options, on_upgrade_choice)
    
    def _perform_weapon_upgrade(self, cost, new_level):
        """Perform the weapon upgrade"""
        hero = self.gui.game_state.hero
        weapon_data = hero['equipment_data']['weapon']
        
        # Deduct gold
        hero['gold'] -= cost
        
        # Upgrade weapon
        weapon_data['upgrade_level'] = new_level
        
        # Recalculate stats
        old_attack = hero.get('attack', 0)
        new_attack = self._calculate_total_attack()
        hero['attack'] = new_attack
        
        self.gui.clear_text()
        self.gui.print_text("✨ WEAPON UPGRADED! ✨")
        self.gui.print_text("=" * 30)
        
        upgrade_info = self.upgrade_levels[new_level]
        weapon_name = hero.get('weapon')
        
        self.gui.print_text(f"\n⚔️ {weapon_name} {upgrade_info['name']}")
        
        attack_parts = [
            ("Attack: ", "#ffffff"),
            (str(old_attack), "#cccccc"),
            (" → ", "#ffffff"),
            (str(new_attack), "#ff4444")
        ]
        self.gui._print_colored_parts(attack_parts)
        
        # Play upgrade sound
        self.gui.audio.play_sound_effect('blacksmith-hammer.mp3')
        
        self.gui.root.after(3000, self.show_equipment_menu)
    
    def _show_enchantment_menu(self):
        """Show enchantment options"""
        hero = self.gui.game_state.hero
        
        self.gui.clear_text()
        self.gui.print_text("✨ ENCHANTMENT FORGE ✨")
        self.gui.print_text("=" * 40)
        
        # Check if player has equipment to enchant
        weapon_name = hero.get('weapon', 'None')
        armor_name = hero.get('armour', 'None')
        
        if weapon_name == 'None' and armor_name == 'None':
            self.gui.print_text("❌ You need equipment to enchant!")
            self.gui.print_text("Visit the shop first.")
            self.gui.root.after(3000, self.show_equipment_menu)
            return
        
        enchant_options = []
        
        if weapon_name != 'None':
            enchant_options.append("⚔️ Enchant Weapon")
        
        if armor_name != 'None':
            enchant_options.append("🛡️ Enchant Armor")
        
        enchant_options.append("🔙 Back to Equipment Menu")
        
        def on_enchant_choice(choice):
            if weapon_name != 'None' and choice == 1:
                self._show_weapon_enchantments()
            elif armor_name != 'None' and (choice == 2 or (weapon_name == 'None' and choice == 1)):
                self._show_armor_enchantments()
            else:
                self.show_equipment_menu()
        
        self.gui.set_buttons(enchant_options, on_enchant_choice)
    
    def _show_weapon_enchantments(self):
        """Show available weapon enchantments"""
        hero = self.gui.game_state.hero
        
        self.gui.clear_text()
        self.gui.print_text("⚔️ WEAPON ENCHANTMENTS ⚔️")
        self.gui.print_text("=" * 40)
        
        if 'equipment_data' not in hero:
            hero['equipment_data'] = {}
        if 'weapon' not in hero['equipment_data']:
            hero['equipment_data']['weapon'] = {}
        
        weapon_data = hero['equipment_data']['weapon']
        current_enchant = weapon_data.get('enchantment')
        
        if current_enchant:
            enchant_info = self.enchantments[current_enchant]
            self.gui.print_text(f"Current enchantment: {enchant_info['name']}")
            self.gui.print_text("You can overwrite it with a new enchantment.\n")
        
        # Show available enchantments
        enchant_options = []
        base_cost = 150
        
        for enchant_id, enchant_info in self.enchantments.items():
            cost = base_cost + (enchant_info['damage_bonus'] * 25)
            
            enchant_text = f"✨ {enchant_info['name']} (+{enchant_info['damage_bonus']} attack)"
            enchant_options.append(enchant_text)
            
            # Show cost and effect
            self.gui.print_text(f"{len(enchant_options)}. {enchant_info['name']} Enchantment")
            self.gui.print_text(f"   💰 Cost: {cost} gold")
            self.gui.print_text(f"   ⚔️ Bonus: +{enchant_info['damage_bonus']} attack")
            self.gui.print_text(f"   ✨ Special: {enchant_info['special'].replace('_', ' ').title()}")
            self.gui.print_text("")
        
        enchant_options.append("🔙 Back to Enchantment Menu")
        
        def on_enchant_select(choice):
            if choice <= len(self.enchantments):
                enchant_id = list(self.enchantments.keys())[choice - 1]
                enchant_info = self.enchantments[enchant_id]
                cost = base_cost + (enchant_info['damage_bonus'] * 25)
                self._apply_weapon_enchantment(enchant_id, cost)
            else:
                self._show_enchantment_menu()
        
        self.gui.set_buttons(enchant_options, on_enchant_select)
    
    def _apply_weapon_enchantment(self, enchant_id, cost):
        """Apply enchantment to weapon"""
        hero = self.gui.game_state.hero
        player_gold = hero.get('gold', 0)
        
        if player_gold < cost:
            self.gui.clear_text()
            self.gui.print_text(f"❌ Not enough gold!")
            self.gui.print_text(f"Need: {cost} gold")
            self.gui.print_text(f"Have: {player_gold} gold")
            self.gui.root.after(3000, self._show_weapon_enchantments)
            return
        
        # Apply enchantment
        hero['gold'] -= cost
        weapon_data = hero['equipment_data']['weapon']
        weapon_data['enchantment'] = enchant_id
        
        # Update attack
        old_attack = hero.get('attack', 0)
        new_attack = self._calculate_total_attack()
        hero['attack'] = new_attack
        
        # Store base attack if not already stored
        if 'base_attack' not in hero:
            base_weapon_attack = self._get_base_weapon_attack()
            hero['base_attack'] = hero.get('attack', 5) - base_weapon_attack
        
        enchant_info = self.enchantments[enchant_id]
        
        self.gui.clear_text()
        self.gui.print_text("✨ ENCHANTMENT COMPLETE! ✨")
        self.gui.print_text("=" * 35)
        
        weapon_name = hero.get('weapon')
        
        enchant_parts = [
            (f"\n{enchant_info['name']} ", enchant_info['color']),
            (weapon_name, "#ffffff")
        ]
        self.gui._print_colored_parts(enchant_parts)
        
        attack_parts = [
            ("Attack: ", "#ffffff"),
            (str(old_attack), "#cccccc"),
            (" → ", "#ffffff"),
            (str(new_attack), "#ff4444")
        ]
        self.gui._print_colored_parts(attack_parts)
        
        self.gui.print_text(f"Special Effect: {enchant_info['special'].replace('_', ' ').title()}")
        
        # Play enchantment sound
        self.gui.audio.play_sound_effect('magic.mp3')
        
        self.gui.root.after(4000, self.show_equipment_menu)
    
    def _get_base_weapon_attack(self):
        """Get the base weapon attack from store data"""
        hero = self.gui.game_state.hero
        weapon_name = hero.get('weapon', 'None')
        
        if weapon_name == 'None':
            return hero.get('base_attack', 5)
        
        # Load store data to get base weapon stats
        try:
            import yaml
            with open('store.yaml', 'r') as f:
                store_data = yaml.safe_load(f)
            
            for weapon in store_data.get('Weapons', []):
                if weapon['name'] == weapon_name:
                    return weapon.get('attack', 0)
        except:
            pass
        
        return hero.get('base_attack', 5)
    
    def _get_base_armor_defense(self):
        """Get the base armor defense from store data"""
        hero = self.gui.game_state.hero
        armor_name = hero.get('armour', 'None')
        
        if armor_name == 'None':
            return hero.get('base_defense', 5)
        
        # Load store data to get base armor stats
        try:
            import yaml
            with open('store.yaml', 'r') as f:
                store_data = yaml.safe_load(f)
            
            for armor in store_data.get('Armour', []):
                if armor['name'] == armor_name:
                    return armor.get('defense', 0)
        except:
            pass
        
        return hero.get('base_defense', 5)
    
    def _calculate_weapon_attack(self, weapon_data):
        """Calculate total weapon attack with all bonuses"""
        base_attack = self._get_base_weapon_attack()
        
        # Apply upgrade multiplier
        upgrade_level = weapon_data.get('upgrade_level', 0)
        upgrade_multiplier = self.upgrade_levels[upgrade_level]['multiplier']
        attack = int(base_attack * upgrade_multiplier)
        
        # Apply enchantment bonus
        enchantment = weapon_data.get('enchantment')
        if enchantment and enchantment in self.enchantments:
            attack += self.enchantments[enchantment]['damage_bonus']
        
        # Apply gem bonuses
        gems = weapon_data.get('gems', [])
        for gem in gems:
            if gem in self.gems:
                gem_info = self.gems[gem]
                if gem_info['effect'] == 'attack':
                    attack += gem_info['bonus']
                elif gem_info['effect'] == 'all_stats':
                    attack += gem_info['bonus']
        
        return attack
    
    def _calculate_armor_defense(self, armor_data):
        """Calculate total armor defense with all bonuses"""
        base_defense = self._get_base_armor_defense()
        
        # Apply upgrade multiplier
        upgrade_level = armor_data.get('upgrade_level', 0)
        upgrade_multiplier = self.upgrade_levels[upgrade_level]['multiplier']
        defense = int(base_defense * upgrade_multiplier)
        
        # Apply enchantment bonus
        enchantment = armor_data.get('enchantment')
        if enchantment and enchantment in self.armor_enchantments:
            defense += self.armor_enchantments[enchantment]['defense_bonus']
        
        # Apply gem bonuses
        gems = armor_data.get('gems', [])
        for gem in gems:
            if gem in self.gems:
                gem_info = self.gems[gem]
                if gem_info['effect'] == 'defense':
                    defense += gem_info['bonus']
                elif gem_info['effect'] == 'all_stats':
                    defense += gem_info['bonus']
        
        return defense
    
    def _calculate_total_attack(self):
        """Calculate hero's total attack including base stats and equipment"""
        hero = self.gui.game_state.hero
        
        # Get base attack
        base_attack = hero.get('base_attack', 5)
        
        # Calculate weapon contribution
        if 'equipment_data' in hero and 'weapon' in hero['equipment_data']:
            weapon_attack = self._calculate_weapon_attack(hero['equipment_data']['weapon'])
            return base_attack + weapon_attack
        else:
            # Simple weapon bonus if no enhancement data
            weapon_attack = self._get_base_weapon_attack()
            return weapon_attack
    
    def _calculate_total_defense(self):
        """Calculate hero's total defense including base stats and equipment"""
        hero = self.gui.game_state.hero
        
        # Get base defense
        base_defense = hero.get('base_defense', 5)
        
        # Calculate armor contribution
        if 'equipment_data' in hero and 'armor' in hero['equipment_data']:
            armor_defense = self._calculate_armor_defense(hero['equipment_data']['armor'])
            return base_defense + armor_defense
        else:
            # Simple armor bonus if no enhancement data
            armor_defense = self._get_base_armor_defense()
            return armor_defense
    
    def _show_armor_enchantments(self):
        """Show available armor enchantments"""
        hero = self.gui.game_state.hero
        
        self.gui.clear_text()
        self.gui.print_text("🛡️ ARMOR ENCHANTMENTS 🛡️")
        self.gui.print_text("=" * 40)
        
        if 'equipment_data' not in hero:
            hero['equipment_data'] = {}
        if 'armor' not in hero['equipment_data']:
            hero['equipment_data']['armor'] = {}
        
        armor_data = hero['equipment_data']['armor']
        current_enchant = armor_data.get('enchantment')
        
        if current_enchant:
            enchant_info = self.armor_enchantments[current_enchant]
            self.gui.print_text(f"Current enchantment: {enchant_info['name']}")
            self.gui.print_text("You can overwrite it with a new enchantment.\n")
        
        # Show available enchantments
        enchant_options = []
        base_cost = 120
        
        for enchant_id, enchant_info in self.armor_enchantments.items():
            cost = base_cost + (enchant_info['defense_bonus'] * 20)
            
            enchant_text = f"✨ {enchant_info['name']} (+{enchant_info['defense_bonus']} defense)"
            enchant_options.append(enchant_text)
            
            # Show cost and effect
            self.gui.print_text(f"{len(enchant_options)}. {enchant_info['name']} Enchantment")
            self.gui.print_text(f"   💰 Cost: {cost} gold")
            self.gui.print_text(f"   🛡️ Bonus: +{enchant_info['defense_bonus']} defense")
            self.gui.print_text(f"   ✨ Special: {enchant_info['special'].replace('_', ' ').title()}")
            self.gui.print_text("")
        
        enchant_options.append("🔙 Back to Enchantment Menu")
        
        def on_enchant_select(choice):
            if choice <= len(self.armor_enchantments):
                enchant_id = list(self.armor_enchantments.keys())[choice - 1]
                enchant_info = self.armor_enchantments[enchant_id]
                cost = base_cost + (enchant_info['defense_bonus'] * 20)
                self._apply_armor_enchantment(enchant_id, cost)
            else:
                self._show_enchantment_menu()
        
        self.gui.set_buttons(enchant_options, on_enchant_select)
    
    def _apply_armor_enchantment(self, enchant_id, cost):
        """Apply enchantment to armor"""
        hero = self.gui.game_state.hero
        player_gold = hero.get('gold', 0)
        
        if player_gold < cost:
            self.gui.clear_text()
            self.gui.print_text(f"❌ Not enough gold!")
            self.gui.print_text(f"Need: {cost} gold")
            self.gui.print_text(f"Have: {player_gold} gold")
            self.gui.root.after(3000, self._show_armor_enchantments)
            return
        
        # Apply enchantment
        hero['gold'] -= cost
        armor_data = hero['equipment_data']['armor']
        armor_data['enchantment'] = enchant_id
        
        # Update defense
        old_defense = hero.get('defense', 0)
        new_defense = self._calculate_total_defense()
        hero['defense'] = new_defense
        
        # Store base defense if not already stored
        if 'base_defense' not in hero:
            base_armor_defense = self._get_base_armor_defense()
            hero['base_defense'] = hero.get('defense', 5) - base_armor_defense
        
        enchant_info = self.armor_enchantments[enchant_id]
        
        self.gui.clear_text()
        self.gui.print_text("✨ ENCHANTMENT COMPLETE! ✨")
        self.gui.print_text("=" * 35)
        
        armor_name = hero.get('armour')
        
        self.gui.print_text(f"\n{enchant_info['name']} {armor_name}")
        
        defense_parts = [
            ("Defense: ", "#ffffff"),
            (str(old_defense), "#cccccc"),
            (" → ", "#ffffff"),
            (str(new_defense), "#4444ff")
        ]
        self.gui._print_colored_parts(defense_parts)
        
        self.gui.print_text(f"Special Effect: {enchant_info['special'].replace('_', ' ').title()}")
        
        # Play enchantment sound
        self.gui.audio.play_sound_effect('magic.mp3')
        
        self.gui.root.after(4000, self.show_equipment_menu)
    
    def _show_gem_socketing(self):
        """Show gem socketing interface"""
        self.gui.clear_text()
        self.gui.print_text("💎 GEM SOCKETING 💎")
        self.gui.print_text("=" * 30)
        self.gui.print_text("\n🚧 Coming Soon!")
        self.gui.print_text("Gem socketing will be available in a future update.")
        self.gui.print_text("Gems will provide additional stat bonuses to equipment.")
        
        self.gui.root.after(3000, self.show_equipment_menu)
    
    def _show_equipment_details(self):
        """Show detailed equipment information"""
        hero = self.gui.game_state.hero
        
        self.gui.clear_text()
        self.gui.print_text("🔍 EQUIPMENT DETAILS 🔍")
        self.gui.print_text("=" * 40)
        
        # Detailed weapon info
        weapon_name = hero.get('weapon', 'None')
        if weapon_name != 'None':
            self.gui.print_text(f"\n⚔️ WEAPON ANALYSIS")
            self.gui.print_text("-" * 20)
            
            if 'equipment_data' in hero and 'weapon' in hero['equipment_data']:
                weapon_data = hero['equipment_data']['weapon']
                formatted_name = self._format_equipment_name(weapon_name, weapon_data)
                self.gui.print_text(f"Name: {formatted_name}")
                
                # Base stats
                base_attack = self._get_base_weapon_attack()
                total_attack = self._calculate_weapon_attack(weapon_data)
                self.gui.print_text(f"Base Attack: {base_attack}")
                self.gui.print_text(f"Total Attack: {total_attack}")
                
                # Upgrade info
                upgrade_level = weapon_data.get('upgrade_level', 0)
                if upgrade_level > 0:
                    upgrade_info = self.upgrade_levels[upgrade_level]
                    self.gui.print_text(f"Upgrade Level: {upgrade_level}/5 ({upgrade_info['multiplier']}x)")
                
                # Enchantment info
                enchantment = weapon_data.get('enchantment')
                if enchantment:
                    enchant_info = self.enchantments[enchantment]
                    self.gui.print_text(f"Enchantment: {enchant_info['name']} (+{enchant_info['damage_bonus']})")
                    self.gui.print_text(f"Special: {enchant_info['special'].replace('_', ' ').title()}")
            else:
                self.gui.print_text(f"Name: {weapon_name}")
                self.gui.print_text("No enhancements applied")
        
        # Detailed armor info
        armor_name = hero.get('armour', 'None')
        if armor_name != 'None':
            self.gui.print_text(f"\n🛡️ ARMOR ANALYSIS")
            self.gui.print_text("-" * 20)
            
            if 'equipment_data' in hero and 'armor' in hero['equipment_data']:
                armor_data = hero['equipment_data']['armor']
                formatted_name = self._format_equipment_name(armor_name, armor_data)
                self.gui.print_text(f"Name: {formatted_name}")
                
                # Base stats
                base_defense = self._get_base_armor_defense()
                total_defense = self._calculate_armor_defense(armor_data)
                self.gui.print_text(f"Base Defense: {base_defense}")
                self.gui.print_text(f"Total Defense: {total_defense}")
                
                # Upgrade info
                upgrade_level = armor_data.get('upgrade_level', 0)
                if upgrade_level > 0:
                    upgrade_info = self.upgrade_levels[upgrade_level]
                    self.gui.print_text(f"Upgrade Level: {upgrade_level}/5 ({upgrade_info['multiplier']}x)")
                
                # Enchantment info
                enchantment = armor_data.get('enchantment')
                if enchantment:
                    enchant_info = self.armor_enchantments[enchantment]
                    self.gui.print_text(f"Enchantment: {enchant_info['name']} (+{enchant_info['defense_bonus']})")
                    self.gui.print_text(f"Special: {enchant_info['special'].replace('_', ' ').title()}")
            else:
                self.gui.print_text(f"Name: {armor_name}")
                self.gui.print_text("No enhancements applied")
        
        if weapon_name == 'None' and armor_name == 'None':
            self.gui.print_text("\n❌ No equipment to analyze!")
            self.gui.print_text("Visit the shop to purchase weapons and armor.")
        
        self.gui.root.after(5000, self.show_equipment_menu)