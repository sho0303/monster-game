"""
Quest system for the monster game
"""
import random
from typing import TYPE_CHECKING

import config

if TYPE_CHECKING:
    from gui_interfaces import GameContextProtocol


class Quest:
    """Represents a single quest"""
    def __init__(self, quest_type, target, reward_xp, description):
        self.quest_type = quest_type  # 'kill_monster', etc.
        self.target = target  # monster name
        self.reward_xp = reward_xp
        self.description = description
        self.completed = False
        self.status = 'active'  # 'active', 'completed'

    def to_dict(self):
        """Convert quest to dictionary for storage in hero object"""
        return {
            'quest_type': self.quest_type,
            'target': self.target,
            'reward_xp': self.reward_xp,
            'description': self.description,
            'completed': self.completed,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, quest_dict):
        """Create quest from dictionary"""
        quest = cls(
            quest_dict['quest_type'],
            quest_dict['target'],
            quest_dict['reward_xp'],
            quest_dict['description']
        )
        quest.completed = quest_dict.get('completed', False)
        quest.status = quest_dict.get('status', 'active')
        return quest


class QuestManager:
    """Manages quests for the game"""
    def __init__(self, gui: 'GameContextProtocol'):
        """Initialize quest manager.
        
        Args:
            gui: Game context providing access to game_state, current_biome, and subsystems
        """
        self.gui = gui
        
    def initialize_hero_quests(self, hero):
        """Initialize quest list in hero object if not present"""
        if 'quests' not in hero:
            hero['quests'] = []
        
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
    
    def generate_kill_monster_quest(self):
        """Generate a random kill monster quest from current biome (avoiding duplicates)"""
        # Get all available monsters
        monsters = self.gui.game_state.monsters
        if not monsters:
            return None
        
        # Get current biome from GUI
        current_biome = getattr(self.gui, 'current_biome', 'grassland')
        
        # Get hero level for level-appropriate filtering
        hero = self.gui.game_state.hero
        hero_level = hero.get('level', 1)
        
        # Get existing quest targets to avoid duplicates
        existing_quest_targets = set()
        if hasattr(self.gui.game_state, 'hero') and self.gui.game_state.hero:
            active_quests = self.get_active_quests(self.gui.game_state.hero)
            existing_quest_targets = {quest.target for quest in active_quests if quest.quest_type == 'kill_monster'}
        
        # Filter monsters by:
        # 1. Current biome
        # 2. Level range (same as encounter system: hero_level - 2 to hero_level + 1)
        # 3. Not already a quest target
        available_biome_monsters = [
            (key, value) for key, value in monsters.items()
            if (value.get('biome', 'grassland') == current_biome and 
                value['level'] <= hero_level + config.QUEST_LEVEL_RANGE_MAX and
                value['level'] >= max(1, hero_level + config.QUEST_LEVEL_RANGE_MIN) and
                key not in existing_quest_targets)
        ]
        
        if not available_biome_monsters:
            # Check if there are level-appropriate monsters in this biome
            biome_level_monsters = [
                (key, value) for key, value in monsters.items()
                if (value.get('biome', 'grassland') == current_biome and
                    value['level'] <= hero_level + config.QUEST_LEVEL_RANGE_MAX and
                    value['level'] >= max(1, hero_level + config.QUEST_LEVEL_RANGE_MIN))
            ]
            
            if biome_level_monsters:
                # All level-appropriate monsters in biome have quests
                return "NO_QUESTS_AVAILABLE_BIOME"
            else:
                # No level-appropriate monsters in this biome
                # Try any biome with level-appropriate monsters
                available_all_monsters = [
                    (key, value) for key, value in monsters.items()
                    if (key not in existing_quest_targets and
                        value['level'] <= hero_level + config.QUEST_LEVEL_RANGE_MAX and
                        value['level'] >= max(1, hero_level + config.QUEST_LEVEL_RANGE_MIN))
                ]
                
                if not available_all_monsters:
                    # No level-appropriate monsters anywhere
                    return "NO_QUESTS_AVAILABLE_LEVEL"
                else:
                    # Pick from any level-appropriate monster
                    monster_name, monster_data = random.choice(
                        available_all_monsters
                    )
        else:
            # Pick a random monster from available biome monsters
            monster_name, monster_data = random.choice(
                available_biome_monsters
            )
        
        # Get the monster's XP value (with fallback to 1 if not specified)
        monster_xp = monster_data.get('xp', 1)
        monster_level = monster_data.get('level', 1)
        
        # Create biome-aware quest description with level
        biome_descriptions = {
            'grassland': f"Hunt a {monster_name} (Lv.{monster_level}) in the grasslands",
            'desert': f"Defeat a {monster_name} (Lv.{monster_level}) in the desert sands",
            'dungeon': f"Slay a {monster_name} (Lv.{monster_level}) in the dark dungeons",
            'ocean': f"Battle a {monster_name} (Lv.{monster_level}) in the ocean depths"
        }
        
        quest_description = biome_descriptions.get(
            current_biome,
            f"Kill a {monster_name} (Lv.{monster_level})"
        )
        
        # Create quest with monster's XP as reward
        quest = Quest(
            quest_type='kill_monster',
            target=monster_name,
            reward_xp=monster_xp,
            description=quest_description
        )
        
        return quest
    
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