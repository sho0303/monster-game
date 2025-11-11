#!/usr/bin/env python3
"""
Crafting System for Monster Game
Handles materials, recipes, and crafting interface
"""

import yaml
import random
from collections import defaultdict

class CraftingMaterial:
    """Represents a crafting material"""
    def __init__(self, name, rarity, description, dropped_by, sell_value):
        self.name = name
        self.rarity = rarity
        self.description = description
        self.dropped_by = dropped_by or []
        self.sell_value = sell_value

class CraftingRecipe:
    """Represents a crafting recipe"""
    def __init__(self, name, item_type, stats, materials, level_requirement=1, class_requirement=None):
        self.name = name
        self.item_type = item_type  # 'head', 'chest', 'legs', 'boots', 'weapon_enhancement', 'special'
        self.stats = stats or {}
        self.materials = materials or {}
        self.level_requirement = level_requirement
        self.class_requirement = class_requirement

class CraftingManager:
    """Manages the crafting system"""
    
    def __init__(self, gui):
        self.gui = gui
        self.materials = {}
        self.recipes = {}
        self.load_crafting_data()
        
    def load_crafting_data(self):
        """Load crafting materials and recipes from YAML"""
        try:
            with open('crafting.yaml', 'r') as f:
                data = yaml.safe_load(f)
                
            # Load materials
            for material_data in data.get('Materials', []):
                material = CraftingMaterial(
                    name=material_data['name'],
                    rarity=material_data['rarity'],
                    description=material_data['description'],
                    dropped_by=material_data.get('dropped_by', []),
                    sell_value=material_data.get('sell_value', 1)
                )
                self.materials[material.name] = material
            
            # Load armor recipes
            armor_pieces = data.get('Armor_Pieces', {})
            for slot, pieces in armor_pieces.items():
                for piece_data in pieces:
                    recipe = CraftingRecipe(
                        name=piece_data['name'],
                        item_type=slot.lower(),
                        stats={k: v for k, v in piece_data.items() 
                               if k not in ['name', 'materials', 'level_requirement', 'class']},
                        materials=piece_data.get('materials', {}),
                        level_requirement=piece_data.get('level_requirement', 1),
                        class_requirement=piece_data.get('class')
                    )
                    self.recipes[recipe.name] = recipe
            
            # Load weapon enhancements
            for enhancement_data in data.get('Weapon_Enhancements', []):
                recipe = CraftingRecipe(
                    name=enhancement_data['name'],
                    item_type='weapon_enhancement',
                    stats={k: v for k, v in enhancement_data.items() 
                           if k not in ['name', 'materials', 'description']},
                    materials=enhancement_data.get('materials', {})
                )
                self.recipes[recipe.name] = recipe
                
            # Load special items
            for special_data in data.get('Special_Items', []):
                recipe = CraftingRecipe(
                    name=special_data['name'],
                    item_type='special',
                    stats={k: v for k, v in special_data.items() 
                           if k not in ['name', 'materials']},
                    materials=special_data.get('materials', {})
                )
                self.recipes[recipe.name] = recipe
                
            print(f"Loaded {len(self.materials)} materials and {len(self.recipes)} recipes")
            
        except FileNotFoundError:
            print("Warning: crafting.yaml not found. Crafting system disabled.")
        except Exception as e:
            print(f"Error loading crafting data: {e}")
    
    def initialize_hero_crafting(self, hero):
        """Initialize hero's crafting-related data"""
        if 'materials' not in hero:
            hero['materials'] = {}
        if 'equipment' not in hero:
            hero['equipment'] = {
                'head': None,
                'chest': None,
                'legs': None,
                'boots': None,
                'weapon_enhancements': []
            }
        if 'discovered_recipes' not in hero:
            hero['discovered_recipes'] = []
    
    def roll_material_drop(self, monster_name):
        """Roll for material drops when a monster is defeated"""
        drops = []
        
        # Find materials that can drop from this monster
        possible_materials = [
            material for material in self.materials.values()
            if monster_name in material.dropped_by
        ]
        
        if not possible_materials:
            return drops
            
        # Different drop rates based on rarity
        drop_rates = {
            'common': 0.4,    # 40% chance
            'uncommon': 0.15, # 15% chance
            'rare': 0.05      # 5% chance
        }
        
        for material in possible_materials:
            drop_chance = drop_rates.get(material.rarity, 0.1)
            if random.random() < drop_chance:
                # Roll for quantity (1-3 for common, 1-2 for uncommon, 1 for rare)
                if material.rarity == 'common':
                    quantity = random.randint(1, 3)
                elif material.rarity == 'uncommon':
                    quantity = random.randint(1, 2)
                else:  # rare
                    quantity = 1
                    
                drops.append((material.name, quantity))
        
        return drops
    
    def add_materials(self, hero, material_drops):
        """Add materials to hero's inventory"""
        self.initialize_hero_crafting(hero)
        
        for material_name, quantity in material_drops:
            if material_name in hero['materials']:
                hero['materials'][material_name] += quantity
            else:
                hero['materials'][material_name] = quantity
    
    def can_craft(self, hero, recipe_name):
        """Check if hero can craft a specific recipe"""
        if recipe_name not in self.recipes:
            return False, "Recipe not found"
            
        recipe = self.recipes[recipe_name]
        
        # Check level requirement
        if hero.get('level', 1) < recipe.level_requirement:
            return False, f"Requires level {recipe.level_requirement}"
        
        # Check class requirement
        if recipe.class_requirement and hero.get('class') != recipe.class_requirement:
            return False, f"Requires {recipe.class_requirement} class"
        
        # Check materials
        hero_materials = hero.get('materials', {})
        for material_name, required_amount in recipe.materials.items():
            if hero_materials.get(material_name, 0) < required_amount:
                return False, f"Need {required_amount} {material_name} (have {hero_materials.get(material_name, 0)})"
        
        return True, "Can craft"
    
    def craft_item(self, hero, recipe_name):
        """Craft an item using materials"""
        can_craft_result, reason = self.can_craft(hero, recipe_name)
        if not can_craft_result:
            return False, reason
            
        recipe = self.recipes[recipe_name]
        
        # Consume materials
        for material_name, required_amount in recipe.materials.items():
            hero['materials'][material_name] -= required_amount
            # Remove materials with 0 quantity
            if hero['materials'][material_name] <= 0:
                del hero['materials'][material_name]
        
        # Create the item based on type
        if recipe.item_type in ['head', 'chest', 'legs', 'boots']:
            # Add to equipment inventory (not equipped automatically)
            if 'crafted_equipment' not in hero:
                hero['crafted_equipment'] = []
            
            equipment_item = {
                'name': recipe.name,
                'type': recipe.item_type,
                'stats': recipe.stats.copy(),
                'crafted': True
            }
            hero['crafted_equipment'].append(equipment_item)
            
        elif recipe.item_type == 'weapon_enhancement':
            # Add to enhancement inventory
            if 'weapon_enhancements' not in hero:
                hero['weapon_enhancements'] = []
            
            enhancement = {
                'name': recipe.name,
                'stats': recipe.stats.copy(),
                'used': False
            }
            hero['weapon_enhancements'].append(enhancement)
            
        elif recipe.item_type == 'special':
            # Add to regular items
            if 'crafted_items' not in hero:
                hero['crafted_items'] = []
                
            special_item = {
                'name': recipe.name,
                'stats': recipe.stats.copy(),
                'type': 'special'
            }
            hero['crafted_items'].append(special_item)
        
        return True, f"Successfully crafted {recipe.name}!"
    
    def get_available_recipes(self, hero):
        """Get recipes the hero can potentially craft"""
        hero_class = hero.get('class', 'Warrior')
        hero_level = hero.get('level', 1)
        
        available = []
        for recipe_name, recipe in self.recipes.items():
            # Check class and level requirements
            if recipe.class_requirement and recipe.class_requirement != hero_class:
                continue
            if recipe.level_requirement > hero_level:
                continue
                
            # Check if recipe is discovered (for now, all recipes are available)
            # Later we can add recipe discovery mechanics
            available.append((recipe_name, recipe))
        
        return available
    
    def show_crafting_interface(self):
        """Display the crafting interface"""
        self.gui.clear_text()
        hero = self.gui.game_state.hero
        self.initialize_hero_crafting(hero)
        
        self.gui.print_text("🔨 CRAFTING WORKSHOP 🔨")
        self.gui.print_text("=" * 50)
        
        # Show current materials
        materials = hero.get('materials', {})
        if materials:
            self.gui.print_text("\n📦 Your Materials:")
            for material_name, quantity in sorted(materials.items()):
                material = self.materials.get(material_name)
                rarity_colors = {
                    'common': '#a0a0a0',
                    'uncommon': '#4a9eff', 
                    'rare': '#ff6b35'
                }
                rarity = material.rarity if material else 'common'
                color = rarity_colors.get(rarity, '#ffffff')
                
                material_parts = [
                    (f"  • {material_name}: ", "#ffffff"),
                    (f"{quantity}", color),
                    (f" ({rarity})", color)
                ]
                self.gui._print_colored_parts(material_parts)
        else:
            self.gui.print_text("\n📦 No materials yet. Defeat monsters to collect crafting materials!")
        
        # Show available recipes
        available_recipes = self.get_available_recipes(hero)
        if available_recipes:
            self.gui.print_text(f"\n🛠️  Available Recipes ({len(available_recipes)}):")
            
            buttons = []
            for i, (recipe_name, recipe) in enumerate(available_recipes[:8], 1):  # Show max 8
                can_craft_result, reason = self.can_craft(hero, recipe_name)
                
                if can_craft_result:
                    color = "#00ff88"
                    status = "✅"
                else:
                    color = "#ff6666"
                    status = "❌"
                
                # Build material requirements
                materials_text = ", ".join([f"{amt} {mat}" for mat, amt in recipe.materials.items()])
                
                recipe_parts = [
                    (f"  {i}. ", "#ffffff"),
                    (f"{recipe.name}", color),
                    (f" ({recipe.item_type})", "#ffaa00"),
                    (f" - {materials_text}", "#aaaaaa")
                ]
                self.gui._print_colored_parts(recipe_parts)
                
                if can_craft_result:
                    buttons.append(f"{i}. Craft {recipe.name}")
            
            # Add navigation buttons
            buttons.extend(["📋 View Materials", "🔙 Back to Town"])
            
            def on_craft_choice(choice):
                if choice <= len([r for r in available_recipes[:8] if self.can_craft(hero, r[0])[0]]):
                    # Find the craftable recipe by index
                    craftable_recipes = [(name, recipe) for name, recipe in available_recipes[:8] 
                                       if self.can_craft(hero, name)[0]]
                    if choice <= len(craftable_recipes):
                        recipe_name = craftable_recipes[choice - 1][0]
                        success, message = self.craft_item(hero, recipe_name)
                        
                        if success:
                            success_parts = [
                                ("🔨 ", "#ffffff"),
                                (message, "#00ff88")
                            ]
                            self.gui._print_colored_parts(success_parts)
                        else:
                            error_parts = [
                                ("❌ ", "#ffffff"),
                                (message, "#ff6666")
                            ]
                            self.gui._print_colored_parts(error_parts)
                        
                        self.gui.root.after(2000, self.show_crafting_interface)
                elif choice == len(buttons) - 1:  # View Materials
                    self.show_material_details()
                else:  # Back to Town
                    self.gui.town.enter_town()
            
            self.gui.set_buttons(buttons, on_craft_choice)
        else:
            self.gui.print_text("\n🔒 No recipes available for your class and level.")
            self.gui.set_buttons(["🔙 Back to Town"], lambda c: self.gui.town.enter_town())
    
    def show_material_details(self):
        """Show detailed material information"""
        self.gui.clear_text()
        hero = self.gui.game_state.hero
        
        self.gui.print_text("📋 MATERIAL ENCYCLOPEDIA 📋")
        self.gui.print_text("=" * 50)
        
        materials = hero.get('materials', {})
        
        if not materials:
            self.gui.print_text("No materials collected yet.")
        else:
            for material_name, quantity in sorted(materials.items()):
                material = self.materials.get(material_name)
                if material:
                    self.gui.print_text(f"\n{material.name} x{quantity}")
                    self.gui.print_text(f"  Rarity: {material.rarity.title()}")
                    self.gui.print_text(f"  Description: {material.description}")
                    self.gui.print_text(f"  Sell Value: {material.sell_value}g each")
                    self.gui.print_text(f"  Dropped by: {', '.join(material.dropped_by)}")
        
        self.gui.set_buttons(["🔙 Back to Crafting"], lambda c: self.show_crafting_interface())