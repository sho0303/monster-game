"""
Bounty Board system for the tavern
Offers special hunting quests with enhanced rewards
"""
import random
from typing import TYPE_CHECKING

import config

if TYPE_CHECKING:
    from gui_interfaces import GameContextProtocol


class Bounty:
    """Represents a single bounty"""
    def __init__(self, bounty_type, target, target_count, reward_gold,
                 reward_item, description, difficulty):
        self.bounty_type = bounty_type  # 'hunt', 'collector', 'elite_boss'
        self.target = target  # Monster name
        self.target_count = target_count  # How many to kill
        self.current_count = 0  # Progress tracker
        self.reward_gold = reward_gold
        self.reward_item = reward_item  # Item name or None
        self.description = description
        self.difficulty = difficulty  # 'Bronze', 'Silver', 'Gold'
        self.completed = False
        self.status = 'available'  # 'available', 'active', 'completed'

    def to_dict(self):
        """Convert bounty to dictionary for storage"""
        return {
            'bounty_type': self.bounty_type,
            'target': self.target,
            'target_count': self.target_count,
            'current_count': self.current_count,
            'reward_gold': self.reward_gold,
            'reward_item': self.reward_item,
            'description': self.description,
            'difficulty': self.difficulty,
            'completed': self.completed,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, bounty_dict):
        """Create bounty from dictionary"""
        bounty = cls(
            bounty_dict['bounty_type'],
            bounty_dict['target'],
            bounty_dict['target_count'],
            bounty_dict['reward_gold'],
            bounty_dict.get('reward_item'),
            bounty_dict['description'],
            bounty_dict['difficulty']
        )
        bounty.current_count = bounty_dict.get('current_count', 0)
        bounty.completed = bounty_dict.get('completed', False)
        bounty.status = bounty_dict.get('status', 'available')
        return bounty


class BountyManager:
    """Manages bounty board system"""
    def __init__(self, gui: 'GameContextProtocol'):
        """Initialize with game context.
        
        Args:
            gui: Game context providing UI, state, and subsystem access
        """
        self.gui = gui
        
        # Initialize bounty lists
        self.available_bounties = []
        self.active_bounties = []

        # Unique bounty rewards (not available in shop)
        self.bounty_rewards = {
            'Bronze': [
                {'name': 'Hunter\'s Trophy', 'attack': 5, 'class': 'All'},
                {'name': 'Bounty Medal', 'defense': 3, 'class': 'All'},
                {'name': 'Lucky Charm', 'attack': 3,
                 'defense': 2, 'class': 'All'},
            ],
            'Silver': [
                {'name': 'Elite Hunter Badge', 'attack': 10, 'class': 'All'},
                {'name': 'Champion\'s Ring', 'defense': 8, 'class': 'All'},
                {'name': 'Slayer\'s Pendant', 'attack': 7,
                 'defense': 5, 'class': 'All'},
            ],
            'Gold': [
                {'name': 'Legendary Bounty Crown', 'attack': 15,
                 'defense': 10, 'class': 'All'},
                {'name': 'Master Hunter Amulet', 'attack': 20,
                 'class': 'All'},
                {'name': 'Titan\'s Bracer', 'defense': 15, 'class': 'All'},
            ]
        }

    def load_bounties(self, bounty_data):
        """Load bounties from save data"""
        # Clear current bounties
        self.available_bounties = []
        self.active_bounties = []
        
        # Restore available bounties
        for bounty_dict in bounty_data.get('available', []):
            bounty = Bounty.from_dict(bounty_dict)
            self.available_bounties.append(bounty)
        
        # Restore active bounties
        for bounty_dict in bounty_data.get('active', []):
            bounty = Bounty.from_dict(bounty_dict)
            self.active_bounties.append(bounty)

    def check_for_elite_encounter(self, hero, monster_name):
        """
        Check if there's an active elite boss bounty for this monster
        Returns elite monster data if bounty is active, None otherwise
        """
        active_bounties = self.get_active_bounties(hero)
        
        for bounty in active_bounties:
            if (bounty.bounty_type == 'elite_boss' and
                bounty.target == f"Elite {monster_name}"):
                # Create and return elite version
                return self.create_elite_monster(monster_name)
        
        return None
    
    def create_elite_monster(self, base_monster_name):
        """Create an elite version of a monster with boosted stats"""
        monsters = self.gui.game_state.monsters
        if base_monster_name not in monsters:
            return None
        
        base = monsters[base_monster_name].copy()
        
        # Create elite version with enhanced stats
        elite = {
            'name': f"Elite {base['name']}",
            'hp': int(base['hp'] * config.ELITE_STAT_MULTIPLIER),
            'maxhp': int(base['maxhp'] * config.ELITE_STAT_MULTIPLIER),
            'attack': int(base['attack'] * config.ELITE_STAT_MULTIPLIER),
            'defense': base['defense'],  # Keep defense same
            'gold': int(base.get('gold', 10) * 2),  # 2x gold
            'level': base['level'] + 1,  # 1 level higher
            'xp': base.get('xp', 1) * 2,  # 2x XP
            'art': base.get('art', 'art/crossed_swords.png'),
            'attack_sound': base.get('attack_sound', 'buzzer.mp3'),
            'biome': base.get('biome', 'grassland'),
            'is_elite': True  # Mark as elite
        }
        
        return elite
    
    def initialize_hero_bounties(self, hero):
        """Initialize bounty list in hero object if not present"""
        if 'bounties' not in hero:
            hero['bounties'] = []

        # Normalize bounties to dictionaries
        normalized = []
        for item in hero['bounties']:
            if isinstance(item, dict):
                normalized.append(item)
            elif hasattr(item, 'to_dict'):
                normalized.append(item.to_dict())
        hero['bounties'] = normalized

    def generate_bounty(self, difficulty=None):
        """Generate a random bounty based on hero level"""
        monsters = self.gui.game_state.monsters
        if not monsters:
            return None

        hero = self.gui.game_state.hero
        hero_level = hero.get('level', 1)

        # Auto-determine difficulty based on hero level if not specified
        if difficulty is None:
            if hero_level <= 3:
                difficulty = 'Bronze'
            elif hero_level <= 6:
                difficulty = random.choice(['Bronze', 'Silver'])
            else:
                difficulty = random.choice(['Silver', 'Gold'])

        # Get level-appropriate monsters
        current_biome = getattr(self.gui, 'current_biome', 'grassland')

        # Filter by level range and biome
        suitable_monsters = [
            (name, data) for name, data in monsters.items()
            if (data['level'] <= hero_level + config.QUEST_LEVEL_RANGE_MAX and
                data['level'] >= max(1, hero_level + config.QUEST_LEVEL_RANGE_MIN) and
                data.get('biome', 'grassland') == current_biome)
        ]

        if not suitable_monsters:
            # Fallback to any level-appropriate monster
            suitable_monsters = [
                (name, data) for name, data in monsters.items()
                if (data['level'] <= hero_level + config.QUEST_LEVEL_RANGE_MAX and
                    data['level'] >= max(1, hero_level + config.QUEST_LEVEL_RANGE_MIN))
            ]

        if not suitable_monsters:
            return None

        # Choose random bounty type
        bounty_type = random.choice(['hunt', 'collector', 'elite_boss'])

        # Select target monster
        target_name, target_data = random.choice(suitable_monsters)

        # Generate bounty based on type
        if bounty_type == 'hunt':
            return self._generate_hunt_bounty(
                target_name, target_data, difficulty
            )
        elif bounty_type == 'collector':
            return self._generate_collector_bounty(
                target_name, target_data, difficulty
            )
        else:  # elite_boss
            return self._generate_elite_boss_bounty(
                target_name, target_data, difficulty
            )

    def _generate_hunt_bounty(self, target_name, target_data, difficulty):
        """Generate a hunt bounty (kill 1 specific monster)"""
        # Reward multipliers
        gold_mult = {'Bronze': 2, 'Silver': 3, 'Gold': 4}
        base_gold = target_data.get('gold', 10)

        reward_gold = base_gold * gold_mult[difficulty]
        reward_item = random.choice(self.bounty_rewards[difficulty])

        biome = target_data.get('biome', 'grassland')
        descriptions = {
            'grassland': f"Hunt down the {target_name} in the grasslands",
            'desert': f"Track and eliminate the {target_name} in the desert",
            'dungeon': f"Slay the {target_name} lurking in the dungeons",
            'ocean': f"Defeat the {target_name} in the ocean depths"
        }

        return Bounty(
            bounty_type='hunt',
            target=target_name,
            target_count=1,
            reward_gold=reward_gold,
            reward_item=reward_item,
            description=descriptions.get(
                biome, f"Eliminate the {target_name}"
            ),
            difficulty=difficulty
        )

    def _generate_collector_bounty(self, target_name, target_data, difficulty):
        """Generate collector bounty (kill multiple of same monster)"""
        # Count based on difficulty
        count_mult = {
            'Bronze': config.BOUNTY_COLLECTOR_MIN_KILLS,
            'Silver': (config.BOUNTY_COLLECTOR_MIN_KILLS + config.BOUNTY_COLLECTOR_MAX_KILLS) // 2,
            'Gold': config.BOUNTY_COLLECTOR_MAX_KILLS
        }
        target_count = count_mult[difficulty]

        gold_mult = {'Bronze': 1.5, 'Silver': 2, 'Gold': 2.5}
        base_gold = target_data.get('gold', 10)
        reward_gold = int(base_gold * target_count * gold_mult[difficulty])

        reward_item = random.choice(self.bounty_rewards[difficulty])

        return Bounty(
            bounty_type='collector',
            target=target_name,
            target_count=target_count,
            reward_gold=reward_gold,
            reward_item=reward_item,
            description=f"Collect bounty: Defeat {target_count} "
                       f"{target_name}s",
            difficulty=difficulty
        )

    def _generate_elite_boss_bounty(self, target_name,
                                     target_data, difficulty):
        """Generate elite boss bounty (tougher version of monster)"""
        gold_mult = {'Bronze': 3, 'Silver': 4, 'Gold': 5}
        base_gold = target_data.get('gold', 10)
        reward_gold = base_gold * gold_mult[difficulty]

        reward_item = random.choice(self.bounty_rewards[difficulty])

        return Bounty(
            bounty_type='elite_boss',
            target=f"Elite {target_name}",
            target_count=1,
            reward_gold=reward_gold,
            reward_item=reward_item,
            description=f"Defeat the Elite {target_name} - "
                       f"A legendary {difficulty} ranked threat!",
            difficulty=difficulty
        )

    def get_available_bounties(self, hero):
        """Get all available bounties"""
        self.initialize_hero_bounties(hero)
        available = [
            b for b in hero['bounties']
            if b.get('status') == 'available'
        ]
        return [Bounty.from_dict(b) for b in available]

    def get_active_bounties(self, hero):
        """Get all active bounties"""
        self.initialize_hero_bounties(hero)
        active = [
            b for b in hero['bounties']
            if b.get('status') == 'active' and not b.get('completed', False)
        ]
        return [Bounty.from_dict(b) for b in active]

    def accept_bounty(self, hero, bounty):
        """Accept a bounty and make it active"""
        self.initialize_hero_bounties(hero)

        # Find and update the bounty
        for b in hero['bounties']:
            if (b['target'] == bounty.target and
                b['difficulty'] == bounty.difficulty and
                b['status'] == 'available'):
                b['status'] = 'active'
                return True
        return False

    def check_bounty_progress(self, hero, monster_killed):
        """Check if killing a monster progresses any active bounties"""
        active_bounties = self.get_active_bounties(hero)
        progressed = []

        for bounty in active_bounties:
            # Check for hunt and collector bounties
            if bounty.target == monster_killed:
                bounty.current_count += 1

                # Update in hero's bounties list
                for b in hero['bounties']:
                    if (b['target'] == bounty.target and
                        b['difficulty'] == bounty.difficulty and
                        b['status'] == 'active'):
                        b['current_count'] = bounty.current_count

                        # Check if completed
                        if bounty.current_count >= bounty.target_count:
                            b['completed'] = True
                            bounty.completed = True

                progressed.append(bounty)

            # Check for elite boss bounties
            elif (bounty.bounty_type == 'elite_boss' and
                  f"Elite {monster_killed}" == bounty.target):
                bounty.current_count = 1
                bounty.completed = True

                # Update in hero's bounties
                for b in hero['bounties']:
                    if (b['target'] == bounty.target and
                        b['difficulty'] == bounty.difficulty):
                        b['current_count'] = 1
                        b['completed'] = True

                progressed.append(bounty)

        return progressed

    def claim_bounty_reward(self, hero, bounty):
        """Claim reward for completed bounty"""
        if not bounty.completed:
            return False

        # Award gold
        hero['gold'] += bounty.reward_gold

        # Award item if specified
        if bounty.reward_item:
            if 'bounty_items' not in hero:
                hero['bounty_items'] = []
            hero['bounty_items'].append(bounty.reward_item)

        # Track bounty completion for achievements
        if hasattr(self.gui, 'achievement_manager'):
            self.gui.achievement_manager.track_bounty_completion()
            self.gui.achievement_manager.track_gold_earned(bounty.reward_gold)

        # Remove bounty from hero's list
        hero['bounties'] = [
            b for b in hero['bounties']
            if not (b['target'] == bounty.target and
                    b['difficulty'] == bounty.difficulty and
                    b.get('completed', False))
        ]

        return True

    def show_bounty_board(self):
        """Display the bounty board interface"""
        hero = self.gui.game_state.hero
        self.initialize_hero_bounties(hero)

        self.gui.clear_text()
        self.gui.print_text("\n" + "="*60)
        self.gui.print_text("🎯  BOUNTY BOARD  🎯")
        self.gui.print_text("="*60 + "\n")

        # Get available and active bounties
        available = self.get_available_bounties(hero)
        active = self.get_active_bounties(hero)

        # Show active bounties
        if active:
            self.gui.print_text("📋 ACTIVE BOUNTIES:")
            for i, bounty in enumerate(active, 1):
                self._display_bounty(bounty, f"Active {i}")
            self.gui.print_text("")

        # Show available bounties
        if available:
            self.gui.print_text("📜 AVAILABLE BOUNTIES:")
            for i, bounty in enumerate(available, 1):
                self._display_bounty(bounty, f"Bounty {i}")
        else:
            self.gui.print_text("No bounties available right now.")
            self.gui.print_text("Check back after completing some quests!\n")

        # Menu options
        buttons = []
        callbacks = []

        if available:
            buttons.append("✅ Accept Bounty")
            callbacks.append(lambda: self._accept_bounty_menu())

        if active:
            buttons.append("🏆 Claim Rewards")
            callbacks.append(lambda: self._claim_rewards_menu())

        buttons.append("🔄 Refresh Board")
        callbacks.append(lambda: self._refresh_bounties())

        buttons.append("🏠 Back to Town")
        callbacks.append(lambda: self.gui.town.enter_town())

        def on_choice(choice):
            callbacks[choice - 1]()

        self.gui.set_buttons(buttons, on_choice)

    def _display_bounty(self, bounty, label):
        """Display a single bounty"""
        difficulty_colors = {
            'Bronze': '🥉',
            'Silver': '🥈',
            'Gold': '🥇'
        }
        icon = difficulty_colors.get(bounty.difficulty, '📌')

        self.gui.print_text(f"\n{icon} {label} - {bounty.difficulty}")
        self.gui.print_text(f"   {bounty.description}")

        if bounty.bounty_type == 'collector':
            progress = f" ({bounty.current_count}/{bounty.target_count})"
            self.gui.print_text(f"   Progress:{progress}")
        elif bounty.bounty_type == 'elite_boss':
            self.gui.print_text("   Type: Elite Boss Fight")

        self.gui.print_text(f"   💰 Reward: {bounty.reward_gold} gold")
        if bounty.reward_item:
            item_name = bounty.reward_item.get('name', 'Unknown Item')
            self.gui.print_text(f"   🎁 Item: {item_name}")

        if bounty.completed:
            self.gui.print_text("   ✅ COMPLETED - Ready to claim!")

    def _accept_bounty_menu(self):
        """Menu for accepting a bounty"""
        hero = self.gui.game_state.hero
        available = self.get_available_bounties(hero)

        if not available:
            self.gui.print_text("\nNo available bounties to accept!")
            self.gui.root.after(1500, self.show_bounty_board)
            return

        self.gui.clear_text()
        self.gui.print_text("\n🎯 SELECT BOUNTY TO ACCEPT:\n")

        for i, bounty in enumerate(available, 1):
            self._display_bounty(bounty, f"Option {i}")

        buttons = [f"{i}. Accept" for i in range(1, len(available) + 1)]
        buttons.append("❌ Cancel")

        def on_choice(choice):
            if choice <= len(available):
                selected = available[choice - 1]
                self.accept_bounty(hero, selected)
                self.gui.print_text(
                    f"\n✅ Accepted: {selected.description}"
                )
                self.gui.root.after(1500, self.show_bounty_board)
            else:
                self.show_bounty_board()

        self.gui.set_buttons(buttons, on_choice)

    def _claim_rewards_menu(self):
        """Menu for claiming completed bounty rewards"""
        hero = self.gui.game_state.hero
        active = self.get_active_bounties(hero)
        completed = [b for b in active if b.completed]

        if not completed:
            self.gui.print_text("\nNo completed bounties to claim!")
            self.gui.root.after(1500, self.show_bounty_board)
            return

        self.gui.clear_text()
        self.gui.print_text("\n🏆 CLAIM BOUNTY REWARDS:\n")

        for bounty in completed:
            self._display_bounty(bounty, "Completed")
            if self.claim_bounty_reward(hero, bounty):
                self.gui.print_text(
                    f"\n✅ Claimed {bounty.reward_gold} gold!"
                )
                if bounty.reward_item:
                    item_name = bounty.reward_item.get('name', 'Item')
                    self.gui.print_text(f"🎁 Received: {item_name}")

        self.gui.root.after(2000, self.show_bounty_board)

    def _refresh_bounties(self):
        """Generate new bounties for the board"""
        hero = self.gui.game_state.hero
        self.initialize_hero_bounties(hero)

        # Generate 3 new bounties (1 of each difficulty)
        for difficulty in ['Bronze', 'Silver', 'Gold']:
            bounty = self.generate_bounty(difficulty)
            if bounty:
                hero['bounties'].append(bounty.to_dict())

        self.gui.print_text("\n🔄 Bounty board refreshed!")
        self.gui.root.after(1000, self.show_bounty_board)

