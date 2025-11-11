"""
Quest system for the monster game
"""
import random


class Quest:
    """Represents a single quest"""
    def __init__(self, quest_type, target, reward_xp, description, reward_gold=0, reward_item=None):
        self.quest_type = quest_type  # 'kill_monster', etc.
        self.target = target  # monster name
        self.reward_xp = reward_xp
        self.reward_gold = reward_gold  # Gold reward
        self.reward_item = reward_item  # Equipment reward (dict with name, attack, defense, etc.)
        self.description = description
        self.completed = False
        self.status = 'active'  # 'active', 'completed'
        
        # New fields for enhanced quest system
        self.target_biome = None
        self.is_cross_biome = False
        self.hero_level_when_created = 1

    def to_dict(self):
        """Convert quest to dictionary for storage in hero object"""
        return {
            'quest_type': self.quest_type,
            'target': self.target,
            'reward_xp': self.reward_xp,
            'reward_gold': getattr(self, 'reward_gold', 0),
            'reward_item': getattr(self, 'reward_item', None),
            'description': self.description,
            'completed': self.completed,
            'status': self.status,
            'target_biome': getattr(self, 'target_biome', None),
            'is_cross_biome': getattr(self, 'is_cross_biome', False),
            'hero_level_when_created': getattr(self, 'hero_level_when_created', 1)
        }

    @classmethod
    def from_dict(cls, quest_dict):
        """Create quest from dictionary"""
        quest = cls(
            quest_dict['quest_type'],
            quest_dict['target'],
            quest_dict['reward_xp'],
            quest_dict['description'],
            quest_dict.get('reward_gold', 0),
            quest_dict.get('reward_item', None)
        )
        quest.completed = quest_dict.get('completed', False)
        quest.status = quest_dict.get('status', 'active')
        quest.target_biome = quest_dict.get('target_biome', None)
        quest.is_cross_biome = quest_dict.get('is_cross_biome', False)
        quest.hero_level_when_created = quest_dict.get('hero_level_when_created', 1)
        return quest


class QuestManager:
    """Manages quests for the game"""
    def __init__(self, gui):
        self.gui = gui
        # Quest limits per hero level to prevent farming
        self.MAX_QUESTS_PER_LEVEL = 2  # Only 2 quests per level
        
        # Biome progression requirements
        self.BIOME_UNLOCK_LEVELS = {
            'grassland': 1,   # Starting biome
            'desert': 3,      # Unlock at level 3
            'ocean': 5,       # Unlock at level 5  
            'dungeon': 7      # Unlock at level 7
        }
        
        # Cross-biome mission chance (forces exploration)
        self.CROSS_BIOME_MISSION_CHANCE = 0.6  # 60% chance for cross-biome quest
        
        # Quest Equipment Rewards by level tier
        self.quest_rewards = {
            'novice': [  # Levels 1-3
                {'name': 'Rusty Sword', 'attack': 12, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Basic Edge'},
                {'name': 'Training Bow', 'attack': 10, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Steady Aim'},
                {'name': 'Apprentice Wand', 'attack': 14, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Magic Spark'},
                {'name': 'Cloth Armor', 'defense': 8, 'class': 'All', 'type': 'armor', 'enchantment': 'Basic Protection'},
                {'name': 'Simple Ring', 'attack': 1, 'defense': 2, 'class': 'All', 'type': 'accessory', 'enchantment': 'Minor Boost'},
            ],
            'adept': [  # Levels 4-6
                {'name': 'Steel Blade', 'attack': 20, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Sharp Edge'},
                {'name': 'Composite Bow', 'attack': 18, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Piercing Shot'},
                {'name': 'Journeyman Staff', 'attack': 22, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Mana Focus'},
                {'name': 'Reinforced Leather', 'defense': 15, 'class': 'All', 'type': 'armor', 'enchantment': 'Sturdy Guard'},
                {'name': 'Veteran\'s Badge', 'attack': 3, 'defense': 4, 'class': 'All', 'type': 'accessory', 'enchantment': 'Combat Experience'},
            ],
            'expert': [  # Levels 7-9
                {'name': 'Masterwork Sword', 'attack': 30, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Perfect Balance'},
                {'name': 'Elven Longbow', 'attack': 28, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'True Shot'},
                {'name': 'Master\'s Rod', 'attack': 32, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Spell Mastery'},
                {'name': 'Chainmail Vest', 'defense': 22, 'class': 'All', 'type': 'armor', 'enchantment': 'Metal Ward'},
                {'name': 'Expert\'s Medallion', 'attack': 5, 'defense': 6, 'class': 'All', 'type': 'accessory', 'enchantment': 'Skill Boost'},
            ],
            'master': [  # Levels 10+
                {'name': 'Legendary Claymore', 'attack': 40, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Heroic Might'},
                {'name': 'Shadowstrike Bow', 'attack': 38, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Shadow Arrow'},
                {'name': 'Archmage\'s Scepter', 'attack': 42, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Ultimate Power'},
                {'name': 'Plate Armor', 'defense': 30, 'class': 'All', 'type': 'armor', 'enchantment': 'Fortress'},
                {'name': 'Master\'s Crown', 'attack': 8, 'defense': 10, 'class': 'All', 'type': 'accessory', 'enchantment': 'Supreme Authority'},
            ]
        }
        
    def initialize_hero_quests(self, hero):
        """Initialize quest list in hero object if not present"""
        if 'quests' not in hero:
            hero['quests'] = []
        
        # Initialize quest tracking per level
        if 'quests_completed_by_level' not in hero:
            hero['quests_completed_by_level'] = {}
        
        # Ensure all quests are stored as dictionaries for consistency
        normalized_quests = []
        for quest_item in hero['quests']:
            if isinstance(quest_item, dict):
                # Already a dictionary - keep as is
                normalized_quests.append(quest_item)
            elif hasattr(quest_item, 'to_dict'):
                # Quest object - convert to dictionary
                normalized_quests.append(quest_item.to_dict())
        
        hero['quests'] = normalized_quests
    
    def get_quests_completed_at_level(self, hero, level):
        """Get number of quests completed at specific hero level"""
        self.initialize_hero_quests(hero)
        return hero['quests_completed_by_level'].get(str(level), 0)
    
    def can_take_more_quests(self, hero):
        """Check if hero can take more quests at current level"""
        current_level = hero.get('level', 1)
        completed_at_level = self.get_quests_completed_at_level(hero, current_level)
        active_quests = len(self.get_active_quests(hero))
        
        total_quests_this_level = completed_at_level + active_quests
        return total_quests_this_level < self.MAX_QUESTS_PER_LEVEL
    
    def get_available_biomes_for_hero(self, hero):
        """Get list of biomes hero has unlocked based on level and discoveries"""
        hero_level = hero.get('level', 1)
        available_biomes = []
        
        for biome, required_level in self.BIOME_UNLOCK_LEVELS.items():
            if hero_level >= required_level:
                available_biomes.append(biome)
        
        # Add secret dungeon if discovered through bartender
        if hero.get('secret_dungeon_discovered', False):
            available_biomes.append('secret_dungeon')
        
        return available_biomes
    
    def generate_kill_monster_quest(self):
        """Generate a proper quest with level limits and cross-biome missions"""
        hero = self.gui.game_state.hero
        
        # Check if hero can take more quests at current level
        if not self.can_take_more_quests(hero):
            return "QUEST_LIMIT_REACHED"
        
        monsters = self.gui.game_state.monsters
        if not monsters:
            return None
        
        hero_level = hero.get('level', 1)
        current_biome = getattr(self.gui, 'current_biome', 'grassland')
        
        # Get available biomes for hero level
        available_biomes = self.get_available_biomes_for_hero(hero)
        
        # Get existing quest targets to avoid duplicates
        active_quests = self.get_active_quests(hero)
        existing_quest_targets = {quest.target for quest in active_quests if quest.quest_type == 'kill_monster'}
        
        # Determine if this should be a cross-biome mission
        should_be_cross_biome = (
            len(available_biomes) > 1 and  # Hero has unlocked multiple biomes
            random.random() < self.CROSS_BIOME_MISSION_CHANCE  # Random chance
        )
        
        if should_be_cross_biome:
            # Force exploration - pick a different biome
            target_biomes = [biome for biome in available_biomes if biome != current_biome]
            if target_biomes:
                target_biome = random.choice(target_biomes)
                quest_type_prefix = "🌍 EXPLORATION MISSION: "
            else:
                target_biome = current_biome  # Fallback to current if only one available
                quest_type_prefix = ""
        else:
            target_biome = current_biome
            quest_type_prefix = ""
        
        # Find level-appropriate monsters in target biome
        level_range = 2  # Allow ±2 levels for variety
        suitable_monsters = [
            (name, data) for name, data in monsters.items()
            if (data.get('biome', 'grassland') == target_biome and
                abs(data['level'] - hero_level) <= level_range and
                name not in existing_quest_targets and
                data['level'] >= 1)  # Ensure positive level
        ]
        
        if not suitable_monsters:
            # No suitable monsters in target biome - try any unlocked biome
            for backup_biome in available_biomes:
                suitable_monsters = [
                    (name, data) for name, data in monsters.items()
                    if (data.get('biome', 'grassland') == backup_biome and
                        abs(data['level'] - hero_level) <= level_range and
                        name not in existing_quest_targets and
                        data['level'] >= 1)
                ]
                if suitable_monsters:
                    target_biome = backup_biome
                    break
        
        if not suitable_monsters:
            return "NO_SUITABLE_MONSTERS"
        
        # Select random monster from suitable options
        monster_name, monster_data = random.choice(suitable_monsters)
        monster_level = monster_data.get('level', 1)
        
        # Calculate XP reward based on level difference and cross-biome bonus
        base_xp = monster_data.get('xp', monster_level)
        level_multiplier = 1.0
        
        if monster_level > hero_level:
            level_multiplier = 1.5  # Bonus for higher level monsters
        elif monster_level < hero_level - 1:
            level_multiplier = 0.8  # Reduced XP for easier monsters
        
        # Cross-biome mission bonus
        cross_biome_bonus = 1.5 if target_biome != current_biome else 1.0
        
        # Final XP calculation
        final_xp = int(base_xp * level_multiplier * cross_biome_bonus)
        
        # Create quest description
        biome_descriptions = {
            'grassland': f"🌾 Travel to the Grasslands and hunt a {monster_name} (Lv.{monster_level})",
            'desert': f"🏜️ Journey to the Desert and defeat a {monster_name} (Lv.{monster_level})", 
            'dungeon': f"🏰 Venture into the Dungeons and slay a {monster_name} (Lv.{monster_level})",
            'ocean': f"🌊 Sail to the Ocean and battle a {monster_name} (Lv.{monster_level})",
            'secret_dungeon': f"🕳️ Descend into the Secret Dungeon and destroy a {monster_name} (Lv.{monster_level})"
        }
        
        quest_description = quest_type_prefix + biome_descriptions.get(
            target_biome,
            f"Find and kill a {monster_name} (Lv.{monster_level})"
        )
        
        # Add XP bonus info to description
        if cross_biome_bonus > 1.0:
            quest_description += f" (+{int((cross_biome_bonus-1)*100)}% XP bonus for exploration!)"
        
        # Generate equipment and gold rewards
        hero_class = self.gui.game_state.hero.get('class', 'Warrior')
        reward_item, reward_gold = self.select_quest_reward(hero_class, hero_level)
        
        # Add reward info to description
        reward_desc = f"\nRewards: {final_xp} XP"
        if reward_gold > 0:
            reward_desc += f", {reward_gold} gold"
        if reward_item:
            reward_desc += f", {reward_item['name']}"
            if reward_item.get('enchantment'):
                reward_desc += f" ({reward_item['enchantment']})"
        quest_description += reward_desc
        
        # Create enhanced quest object with biome info
        quest = Quest(
            quest_type='kill_monster',
            target=monster_name,
            reward_xp=final_xp,
            description=quest_description,
            reward_gold=reward_gold,
            reward_item=reward_item
        )
        
        # Add biome info to quest for tracking
        quest_dict = quest.to_dict()
        quest_dict['target_biome'] = target_biome
        quest_dict['is_cross_biome'] = target_biome != current_biome
        quest_dict['hero_level_when_created'] = hero_level
        
        return Quest.from_dict(quest_dict)
    
    def add_quest(self, hero, quest):
        """Add a quest to hero's quest list"""
        self.initialize_hero_quests(hero)
        hero['quests'].append(quest.to_dict())
    
    def get_active_quests(self, hero):
        """Get all active (non-completed) quests for hero"""
        self.initialize_hero_quests(hero)
        # Filter dictionaries first, then convert to Quest objects
        active_quest_dicts = [q for q in hero['quests'] if not q.get('completed', False)]
        return [Quest.from_dict(q) for q in active_quest_dicts]
    
    def complete_quest(self, hero, quest):
        """Mark quest as completed and give rewards"""
        self.initialize_hero_quests(hero)
        
        # Find and mark quest as completed
        for q in hero['quests']:
            if (q['quest_type'] == quest.quest_type and 
                q['target'] == quest.target and 
                not q.get('completed', False)):
                q['completed'] = True
                
                # Give XP reward
                hero['xp'] += quest.reward_xp
                
                # Give gold reward
                if hasattr(quest, 'reward_gold') and quest.reward_gold > 0:
                    hero['gold'] = hero.get('gold', 0) + quest.reward_gold
                
                # Give equipment reward
                if hasattr(quest, 'reward_item') and quest.reward_item:
                    # Add to inventory or equipment system
                    if not hasattr(hero, 'inventory'):
                        hero['inventory'] = []
                    
                    # Create equipment entry
                    equipment_entry = quest.reward_item.copy()
                    equipment_entry['source'] = 'quest_reward'
                    equipment_entry['cost'] = 0  # Quest rewards are free
                    
                    hero['inventory'].append(equipment_entry)
                
                # Track quest completion by level (for quest limits)
                current_level = str(hero.get('level', 1))
                if current_level not in hero['quests_completed_by_level']:
                    hero['quests_completed_by_level'][current_level] = 0
                hero['quests_completed_by_level'][current_level] += 1
                
                # Track quest completion for achievements
                if hasattr(self, 'gui') and hasattr(self.gui, 'achievement_manager'):
                    self.gui.achievement_manager.track_quest_completion()
                
                return True
        
        return False
    
    def check_quest_completion(self, hero, monster_killed):
        """Check if killing a monster completes any quests"""
        completed_quests = []
        active_quests = self.get_active_quests(hero)
        
        for quest in active_quests:
            if quest.quest_type == 'kill_monster' and quest.target == monster_killed:
                if self.complete_quest(hero, quest):
                    completed_quests.append(quest)
        
        return completed_quests
    
    def drop_quest(self, hero, quest_index):
        """Drop (remove) an active quest by index"""
        self.initialize_hero_quests(hero)
        active_quests = [q for q in hero['quests'] if not q.get('completed', False)]
        
        if 0 <= quest_index < len(active_quests):
            # Find the quest to drop in the original list
            quest_to_drop = active_quests[quest_index]
            # Remove it from the hero's quests
            hero['quests'] = [q for q in hero['quests'] if not (
                q['quest_type'] == quest_to_drop['quest_type'] and
                q['target'] == quest_to_drop['target'] and
                q.get('completed', False) == quest_to_drop.get('completed', False)
            )]
            return True
        return False
    
    def clear_completed_quests(self, hero):
        """Remove completed quests from hero's quest list"""
        self.initialize_hero_quests(hero)
        hero['quests'] = [q for q in hero['quests'] if not q.get('completed', False)]
    
    def get_hero_reward_tier(self, hero_level):
        """Determine reward tier based on hero level"""
        if hero_level <= 3:
            return 'novice'
        elif hero_level <= 6:
            return 'adept'
        elif hero_level <= 9:
            return 'expert'
        else:
            return 'master'
    
    def select_quest_reward(self, hero_class, hero_level, include_gold=True):
        """Select appropriate equipment reward for quest completion"""
        reward_tier = self.get_hero_reward_tier(hero_level)
        available_rewards = self.quest_rewards[reward_tier]
        
        # Filter rewards by hero class
        class_rewards = [r for r in available_rewards if r['class'] == hero_class or r['class'] == 'All']
        
        if not class_rewards:
            return None, 0
        
        # Select random equipment
        equipment = random.choice(class_rewards).copy()
        
        # Calculate gold reward based on level
        gold_reward = 0
        if include_gold:
            base_gold = 15 + (hero_level * 5)  # 20-70+ gold based on level
            gold_reward = random.randint(int(base_gold * 0.8), int(base_gold * 1.2))
        
        return equipment, gold_reward