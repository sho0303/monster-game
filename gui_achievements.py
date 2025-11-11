#!/usr/bin/env python3
"""
Achievement System for PyQuest Monster Game
Tracks player accomplishments, collections, and milestones
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class Achievement:
    """Represents a single achievement"""
    
    def __init__(self, id: str, name: str, description: str, category: str, 
                 target_value: int = 1, reward_type: str = "gold", 
                 reward_value: int = 0, hidden: bool = False, 
                 prerequisite: Optional[str] = None):
        self.id = id
        self.name = name
        self.description = description
        self.category = category  # combat, exploration, collection, progression, special
        self.target_value = target_value  # How many to complete achievement
        self.reward_type = reward_type  # gold, title, item, stat_bonus
        self.reward_value = reward_value
        self.hidden = hidden  # Hidden until unlocked
        self.prerequisite = prerequisite  # Required achievement ID
        
        # Progress tracking
        self.current_progress = 0
        self.completed = False
        self.completed_at = None
        self.unlocked = False  # For hidden achievements
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert achievement to dictionary for save/load"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'target_value': self.target_value,
            'reward_type': self.reward_type,
            'reward_value': self.reward_value,
            'hidden': self.hidden,
            'prerequisite': self.prerequisite,
            'current_progress': self.current_progress,
            'completed': self.completed,
            'completed_at': self.completed_at,
            'unlocked': self.unlocked
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Achievement':
        """Create achievement from dictionary data"""
        achievement = cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            category=data['category'],
            target_value=data.get('target_value', 1),
            reward_type=data.get('reward_type', 'gold'),
            reward_value=data.get('reward_value', 0),
            hidden=data.get('hidden', False),
            prerequisite=data.get('prerequisite')
        )
        
        # Restore progress
        achievement.current_progress = data.get('current_progress', 0)
        achievement.completed = data.get('completed', False)
        achievement.completed_at = data.get('completed_at')
        achievement.unlocked = data.get('unlocked', False)
        
        return achievement

class AchievementManager:
    """Manages all achievements and player progress"""
    
    def __init__(self, gui=None):
        self.gui = gui
        self.achievements: Dict[str, Achievement] = {}
        self.player_stats = {
            'monsters_killed': {},  # {monster_name: count}
            'biomes_visited': set(),
            'quests_completed': 0,
            'side_quests_completed': 0,
            'bounties_completed': 0,
            'gold_earned_total': 0,
            'levels_gained': 0,
            'deaths': 0,
            'combats_won': 0,
            'combats_lost': 0,
            'secret_dungeon_discovered': False,
            'tavern_npcs_met': set(),
            'beers_consumed': 0,
            'fountain_uses': 0,
            'blacksmith_visits': 0,
            'items_purchased': 0,
            'side_quests_completed': 0,
            'total_gold_earned': 0,
            'bounties_completed': 0,
            'time_played_seconds': 0,
            'first_play_date': None,
            'last_play_date': None
        }
        
        # Initialize default achievements
        self._initialize_achievements()
    
    def _initialize_achievements(self):
        """Initialize all default achievements"""
        
        # Combat Achievements
        self.add_achievement(Achievement(
            id="first_blood",
            name="First Blood",
            description="Defeat your first monster",
            category="combat",
            target_value=1,
            reward_type="gold",
            reward_value=50
        ))
        
        self.add_achievement(Achievement(
            id="monster_slayer",
            name="Monster Slayer",
            description="Defeat 10 monsters",
            category="combat",
            target_value=10,
            reward_type="title",
            reward_value=0
        ))
        
        self.add_achievement(Achievement(
            id="beast_hunter",
            name="Beast Hunter",
            description="Defeat 50 monsters",
            category="combat",
            target_value=50,
            reward_type="gold",
            reward_value=500
        ))
        
        self.add_achievement(Achievement(
            id="apex_predator",
            name="Apex Predator",
            description="Defeat 100 monsters",
            category="combat",
            target_value=100,
            reward_type="stat_bonus",
            reward_value=5  # +5 attack permanently
        ))
        
        # Exploration Achievements
        self.add_achievement(Achievement(
            id="explorer",
            name="Explorer",
            description="Visit all basic biomes (Grassland, Desert, Ocean, Dungeon)",
            category="exploration",
            target_value=4,
            reward_type="gold",
            reward_value=200
        ))
        
        self.add_achievement(Achievement(
            id="secret_keeper",
            name="Secret Keeper",
            description="Discover the Secret Dungeon",
            category="exploration",
            target_value=1,
            reward_type="title",
            reward_value=0,
            hidden=True
        ))
        
        # Collection Achievements
        self.add_achievement(Achievement(
            id="grassland_master",
            name="Grassland Master", 
            description="Defeat every monster type in Grassland",
            category="collection",
            target_value=3,  # Assuming 3 grassland monsters
            reward_type="gold",
            reward_value=300
        ))
        
        self.add_achievement(Achievement(
            id="desert_conqueror",
            name="Desert Conqueror",
            description="Defeat every monster type in Desert",
            category="collection", 
            target_value=3,
            reward_type="gold",
            reward_value=400
        ))
        
        # Progression Achievements
        self.add_achievement(Achievement(
            id="level_up",
            name="Growing Stronger",
            description="Reach level 5",
            category="progression",
            target_value=5,
            reward_type="gold",
            reward_value=100
        ))
        
        self.add_achievement(Achievement(
            id="veteran",
            name="Veteran Adventurer", 
            description="Reach level 10",
            category="progression",
            target_value=10,
            reward_type="stat_bonus",
            reward_value=3  # +3 defense permanently
        ))
        
        # Special Achievements
        self.add_achievement(Achievement(
            id="tavern_regular",
            name="Tavern Regular",
            description="Consume 20 beers at the tavern",
            category="special",
            target_value=20,
            reward_type="title",
            reward_value=0
        ))
        
        self.add_achievement(Achievement(
            id="social_butterfly", 
            name="Social Butterfly",
            description="Meet all 6 types of tavern NPCs",
            category="special",
            target_value=6,
            reward_type="gold",
            reward_value=250,
            hidden=True
        ))
        
        self.add_achievement(Achievement(
            id="questmaster",
            name="Quest Master",
            description="Complete 25 quests (any type)",
            category="progression",
            target_value=25,
            reward_type="title",
            reward_value=0
        ))
        
        self.add_achievement(Achievement(
            id="death_defier",
            name="Death Defier",
            description="Survive 100 combat encounters",
            category="combat",
            target_value=100,
            reward_type="stat_bonus",
            reward_value=10  # +10 max HP permanently
        ))
    
    def add_achievement(self, achievement: Achievement):
        """Add an achievement to the manager"""
        self.achievements[achievement.id] = achievement
    
    def update_progress(self, achievement_id: str, increment: int = 1) -> bool:
        """Update progress on an achievement, return True if completed"""
        if achievement_id not in self.achievements:
            return False
        
        achievement = self.achievements[achievement_id]
        
        # Skip if already completed
        if achievement.completed:
            return False
        
        # Check prerequisite
        if achievement.prerequisite and not self.achievements[achievement.prerequisite].completed:
            return False
        
        # Update progress
        achievement.current_progress = min(achievement.current_progress + increment, achievement.target_value)
        
        # Check completion
        if achievement.current_progress >= achievement.target_value and not achievement.completed:
            achievement.completed = True
            achievement.completed_at = datetime.now().isoformat()
            achievement.unlocked = True
            
            # Award rewards
            self._award_achievement_reward(achievement)
            
            return True
        
        return False
    
    def _award_achievement_reward(self, achievement: Achievement):
        """Award the reward for completing an achievement"""
        if not self.gui or not self.gui.game_state or not self.gui.game_state.hero:
            return
        
        hero = self.gui.game_state.hero
        
        if achievement.reward_type == "gold":
            hero['gold'] = hero.get('gold', 0) + achievement.reward_value
        elif achievement.reward_type == "stat_bonus":
            # Determine which stat based on achievement
            if "attack" in achievement.description.lower() or achievement.id == "apex_predator":
                hero['attack'] = hero.get('attack', 0) + achievement.reward_value
            elif "defense" in achievement.description.lower() or achievement.id == "veteran":
                hero['defense'] = hero.get('defense', 0) + achievement.reward_value
            elif "hp" in achievement.description.lower() or achievement.id == "death_defier":
                hero['maxhp'] = hero.get('maxhp', 0) + achievement.reward_value
                hero['hp'] = hero.get('hp', 0) + achievement.reward_value
        elif achievement.reward_type == "title":
            if 'titles' not in hero:
                hero['titles'] = []
            if achievement.name not in hero['titles']:
                hero['titles'].append(achievement.name)
    
    def track_monster_defeat(self, monster_name: str, biome: str = None):
        """Track when a monster is defeated"""
        # Update monster kill count
        self.player_stats['monsters_killed'][monster_name] = self.player_stats['monsters_killed'].get(monster_name, 0) + 1
        
        total_kills = sum(self.player_stats['monsters_killed'].values())
        
        # Update combat achievements
        self.update_progress("first_blood", 0 if total_kills > 1 else 1)  # Only on first kill
        self.update_progress("monster_slayer", 1 if total_kills <= 10 else 0)
        self.update_progress("beast_hunter", 1 if total_kills <= 50 else 0) 
        self.update_progress("apex_predator", 1 if total_kills <= 100 else 0)
        self.update_progress("death_defier", 1)
        
        # Track biome-specific collections
        if biome:
            self._update_biome_collection_progress(monster_name, biome)
    
    def _update_biome_collection_progress(self, monster_name: str, biome: str):
        """Update progress for biome-specific collection achievements"""
        # This would need to be enhanced based on actual monster data
        # For now, simplified logic
        if biome == "grassland":
            # Count unique grassland monsters defeated
            grassland_monsters = [name for name, count in self.player_stats['monsters_killed'].items() 
                                if count > 0]  # Would need biome data to filter properly
            # Simplified - would need actual biome monster data
            
        elif biome == "desert":
            # Similar logic for desert
            pass
    
    def track_biome_visit(self, biome: str):
        """Track when a biome is visited"""
        self.player_stats['biomes_visited'].add(biome)
        
        # Update explorer achievement (basic biomes only)
        basic_biomes = {'grassland', 'desert', 'ocean', 'dungeon'}
        visited_basic = len(basic_biomes.intersection(self.player_stats['biomes_visited']))
        
        if visited_basic >= 4:
            self.update_progress("explorer", visited_basic - 3)  # Complete when all 4 visited
    
    def track_secret_dungeon_discovery(self):
        """Track secret dungeon discovery"""
        if not self.player_stats['secret_dungeon_discovered']:
            self.player_stats['secret_dungeon_discovered'] = True
            self.update_progress("secret_keeper", 1)
    
    def track_quest_completion(self, quest_type: str = "main"):
        """Track quest completion"""
        if quest_type == "main":
            self.player_stats['quests_completed'] += 1
        elif quest_type == "side":
            self.player_stats['side_quests_completed'] += 1
        elif quest_type == "bounty":
            self.player_stats['bounties_completed'] += 1
        
        total_quests = (self.player_stats['quests_completed'] + 
                       self.player_stats['side_quests_completed'] + 
                       self.player_stats['bounties_completed'])
        
        # Update quest master achievement
        if total_quests <= 25:
            self.update_progress("questmaster", 1)
    
    def track_tavern_npc_encounter(self, npc_type: str):
        """Track meeting different tavern NPCs"""
        self.player_stats['tavern_npcs_met'].add(npc_type)
        
        # Update social butterfly achievement
        if len(self.player_stats['tavern_npcs_met']) <= 6:
            self.achievements["social_butterfly"].current_progress = len(self.player_stats['tavern_npcs_met'])
            if len(self.player_stats['tavern_npcs_met']) >= 6:
                self.update_progress("social_butterfly", 0)
    
    def track_beer_consumption(self):
        """Track beer consumption"""
        self.player_stats['beers_consumed'] += 1
        
        # Update tavern regular achievement
        if self.player_stats['beers_consumed'] <= 20:
            self.update_progress("tavern_regular", 1)
    
    def track_level_gain(self, new_level: int):
        """Track level progression"""
        # Update level-based achievements
        if new_level >= 5:
            self.update_progress("level_up", new_level - 4)
        if new_level >= 10:
            self.update_progress("veteran", new_level - 9)
    
    def track_fountain_use(self):
        """Track fountain uses for achievements"""
        self.player_stats['fountain_uses'] += 1
        # Currently no specific fountain achievements, but tracking for future use
    
    def track_combat_win(self):
        """Track combat victories for achievements"""
        self.player_stats['combats_won'] += 1
        
        # Check combat-related achievements
        self.update_progress("first_victory", 1)
        self.update_progress("monster_hunter", 1)
        self.update_progress("experienced_fighter", 1)
    
    def track_monster_kill(self, monster_name: str):
        """Track monster kills (alias for track_monster_defeat for compatibility)"""
        self.track_monster_defeat(monster_name)
    
    def track_combat_loss(self):
        """Track combat losses for achievements"""
        self.player_stats['combats_lost'] = self.player_stats.get('combats_lost', 0) + 1
        # Could add achievements for perseverance, getting back up, etc.
    
    def track_death(self):
        """Track player deaths for achievements"""
        self.player_stats['deaths'] = self.player_stats.get('deaths', 0) + 1
        # Could add achievements for resurrection, learning from failure, etc.
    
    def track_blacksmith_visit(self):
        """Track blacksmith visits for achievements"""
        self.player_stats['blacksmith_visits'] = self.player_stats.get('blacksmith_visits', 0) + 1
        # Could add achievements for gear upgrades, crafting mastery, etc.
    
    def track_side_quest_completion(self):
        """Track side quest completion for achievements"""
        self.player_stats['side_quests_completed'] = self.player_stats.get('side_quests_completed', 0) + 1
        # Check side quest achievements
        self.update_progress("quest_giver", 1)
    
    def track_gold_earned(self, amount: int):
        """Track gold earned for achievements"""
        self.player_stats['total_gold_earned'] = self.player_stats.get('total_gold_earned', 0) + amount
        
        # Check wealth-related achievements
        total_gold = self.player_stats['total_gold_earned']
        if total_gold >= 1000:
            self.update_progress("wealthy", 1)
    
    def track_bounty_completion(self):
        """Track bounty completion for achievements"""
        self.player_stats['bounties_completed'] = self.player_stats.get('bounties_completed', 0) + 1
        # Could add specific bounty hunter achievements
    
    def get_achievements_by_category(self, category: str) -> List[Achievement]:
        """Get all achievements in a category"""
        return [ach for ach in self.achievements.values() if ach.category == category]
    
    def get_completed_achievements(self) -> List[Achievement]:
        """Get all completed achievements"""
        return [ach for ach in self.achievements.values() if ach.completed]
    
    def get_visible_achievements(self) -> List[Achievement]:
        """Get achievements that should be visible (not hidden or unlocked)"""
        return [ach for ach in self.achievements.values() 
                if not ach.hidden or ach.unlocked]
    
    def get_completion_percentage(self) -> float:
        """Get overall completion percentage"""
        visible_achievements = self.get_visible_achievements()
        if not visible_achievements:
            return 0.0
        
        completed = len([ach for ach in visible_achievements if ach.completed])
        return (completed / len(visible_achievements)) * 100
    
    def save_to_dict(self) -> Dict[str, Any]:
        """Save achievement data to dictionary for persistence"""
        return {
            'achievements': {aid: ach.to_dict() for aid, ach in self.achievements.items()},
            'player_stats': {
                **self.player_stats,
                'biomes_visited': list(self.player_stats['biomes_visited']),
                'tavern_npcs_met': list(self.player_stats['tavern_npcs_met'])
            }
        }
    
    def load_from_dict(self, data: Dict[str, Any]):
        """Load achievement data from dictionary"""
        if 'achievements' in data:
            for aid, ach_data in data['achievements'].items():
                if aid in self.achievements:
                    # Update existing achievement with saved progress
                    saved_ach = Achievement.from_dict(ach_data)
                    existing_ach = self.achievements[aid]
                    existing_ach.current_progress = saved_ach.current_progress
                    existing_ach.completed = saved_ach.completed
                    existing_ach.completed_at = saved_ach.completed_at
                    existing_ach.unlocked = saved_ach.unlocked
        
        if 'player_stats' in data:
            stats = data['player_stats']
            self.player_stats.update(stats)
            # Convert lists back to sets
            if 'biomes_visited' in stats:
                self.player_stats['biomes_visited'] = set(stats['biomes_visited'])
            if 'tavern_npcs_met' in stats:
                self.player_stats['tavern_npcs_met'] = set(stats['tavern_npcs_met'])
    
    def load_achievements(self, data: Dict[str, Any]):
        """Load achievement data (wrapper for load_from_dict to match save/load pattern)"""
        # Handle the format from save files
        if 'achievements' in data and isinstance(data['achievements'], list):
            # Convert list format to dict format
            achievements_dict = {}
            for ach_data in data['achievements']:
                if isinstance(ach_data, dict) and 'id' in ach_data:
                    achievements_dict[ach_data['id']] = ach_data
            
            # Update existing achievements with saved progress
            for aid, ach_data in achievements_dict.items():
                if aid in self.achievements:
                    existing_ach = self.achievements[aid]
                    existing_ach.current_progress = ach_data.get('current_progress', 0)
                    existing_ach.completed = ach_data.get('completed', False)
                    existing_ach.completed_at = ach_data.get('completed_at', None)
                    existing_ach.unlocked = ach_data.get('unlocked', True)
        
        # Load player stats
        if 'player_stats' in data:
            stats = data['player_stats']
            self.player_stats.update(stats)
            # Convert lists back to sets for specific fields
            if 'biomes_visited' in stats and isinstance(stats['biomes_visited'], list):
                self.player_stats['biomes_visited'] = set(stats['biomes_visited'])
            if 'tavern_npcs_met' in stats and isinstance(stats['tavern_npcs_met'], list):
                self.player_stats['tavern_npcs_met'] = set(stats['tavern_npcs_met'])