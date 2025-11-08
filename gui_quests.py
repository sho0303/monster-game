"""
Quest system for the monster game
"""
import random


class Quest:
    """Represents a single quest"""
    def __init__(self, quest_type, target, reward_xp, description):
        self.quest_type = quest_type  # 'kill_monster', etc.
        self.target = target  # monster name
        self.reward_xp = reward_xp
        self.description = description
        self.completed = False

    def to_dict(self):
        """Convert quest to dictionary for storage in hero object"""
        return {
            'quest_type': self.quest_type,
            'target': self.target,
            'reward_xp': self.reward_xp,
            'description': self.description,
            'completed': self.completed
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
        return quest


class QuestManager:
    """Manages quests for the game"""
    def __init__(self, gui):
        self.gui = gui
        
    def initialize_hero_quests(self, hero):
        """Initialize quest list in hero object if not present"""
        if 'quests' not in hero:
            hero['quests'] = []
    
    def generate_kill_monster_quest(self):
        """Generate a random kill monster quest"""
        # Get all available monsters
        monsters = self.gui.game_state.monsters
        if not monsters:
            return None
            
        # Pick a random monster
        monster_name = random.choice(list(monsters.keys()))
        monster_data = monsters[monster_name]
        
        # Get the monster's XP value (with fallback to 1 if not specified)
        monster_xp = monster_data.get('xp', 1)
        
        # Create quest with monster's XP as reward
        quest = Quest(
            quest_type='kill_monster',
            target=monster_name,
            reward_xp=monster_xp,
            description=f"Kill a {monster_name}"
        )
        
        return quest
    
    def add_quest(self, hero, quest):
        """Add a quest to hero's quest list"""
        self.initialize_hero_quests(hero)
        hero['quests'].append(quest.to_dict())
    
    def get_active_quests(self, hero):
        """Get all active (non-completed) quests for hero"""
        self.initialize_hero_quests(hero)
        return [Quest.from_dict(q) for q in hero['quests'] if not q.get('completed', False)]
    
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
    
    def clear_completed_quests(self, hero):
        """Remove completed quests from hero's quest list"""
        self.initialize_hero_quests(hero)
        hero['quests'] = [q for q in hero['quests'] if not q.get('completed', False)]