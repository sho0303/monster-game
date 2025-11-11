"""
Bounty Board system for the tavern
Offers special hunting quests with enhanced rewards
"""
import random


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
    def __init__(self, gui):
        self.gui = gui
        
        # Initialize bounty lists
        self.available_bounties = []
        self.active_bounties = []

        # Unique bounty rewards (not available in shop)
        self.bounty_rewards = {
            'Bronze': [
                # Warrior Weapons
                {'name': 'Hunter\'s Blade', 'attack': 25, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Keen Edge'},
                {'name': 'Iron Cleaver', 'attack': 23, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Crushing Blow'},
                {'name': 'Battle Axe', 'attack': 27, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Berserker\'s Fury'},
                {'name': 'Reinforced Mace', 'attack': 24, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Armor Break'},
                # Ninja Weapons
                {'name': 'Tracker\'s Bow', 'attack': 22, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Silent Shot'}, 
                {'name': 'Twin Daggers', 'attack': 20, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Dual Strike'},
                {'name': 'Shadow Blade', 'attack': 26, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Stealth Attack'},
                {'name': 'Throwing Stars', 'attack': 21, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Multi-Hit'},
                # Magician Weapons
                {'name': 'Scout\'s Staff', 'attack': 28, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Mana Burn'},
                {'name': 'Crystal Wand', 'attack': 25, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Spell Power'},
                {'name': 'Elemental Orb', 'attack': 29, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Fire Burst'},
                {'name': 'Arcane Rod', 'attack': 26, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Lightning Bolt'},
                # Armor Sets
                {'name': 'Hunter\'s Leather', 'defense': 18, 'class': 'All', 'type': 'armor', 'enchantment': 'Beast Ward'},
                {'name': 'Scout\'s Cloak', 'defense': 15, 'class': 'Ninja', 'type': 'armor', 'enchantment': 'Evasion'},
                {'name': 'Padded Mail', 'defense': 20, 'class': 'Warrior', 'type': 'armor', 'enchantment': 'Damage Resist'},
                {'name': 'Apprentice Robes', 'defense': 12, 'class': 'Magician', 'type': 'armor', 'enchantment': 'Magic Shield'},
                # Accessories  
                {'name': 'Lucky Charm', 'attack': 3, 'defense': 2, 'class': 'All', 'type': 'accessory', 'enchantment': 'Fortune'},
                {'name': 'Iron Ring', 'attack': 2, 'defense': 4, 'class': 'All', 'type': 'accessory', 'enchantment': 'Toughness'},
                {'name': 'Swift Boots', 'attack': 4, 'defense': 1, 'class': 'All', 'type': 'accessory', 'enchantment': 'Speed'},
            ],
            'Silver': [
                # Elite Warrior Weapons
                {'name': 'Elite Slayer Sword', 'attack': 35, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Monster Slayer'},
                {'name': 'Flamebrand Sword', 'attack': 33, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Fire Damage'},
                {'name': 'Frost Hammer', 'attack': 37, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Ice Shatter'},
                {'name': 'Thunder Axe', 'attack': 34, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Lightning Strike'},
                # Elite Ninja Weapons
                {'name': 'Shadow Strike Daggers', 'attack': 32, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Critical Mastery'},
                {'name': 'Venom Blade', 'attack': 30, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Poison Edge'},
                {'name': 'Wind Cutter', 'attack': 35, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Air Slash'},
                {'name': 'Phantom Bow', 'attack': 31, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Ghost Shot'},
                # Elite Magician Weapons
                {'name': 'Arcane Destructor', 'attack': 38, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Spell Surge'},
                {'name': 'Storm Staff', 'attack': 36, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Chain Lightning'},
                {'name': 'Void Scepter', 'attack': 40, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Dark Magic'},
                {'name': 'Crystal Focus', 'attack': 35, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Mana Overflow'},
                # Elite Armor
                {'name': 'Elite Guardian Mail', 'defense': 28, 'class': 'Warrior', 'type': 'armor', 'enchantment': 'Guardian\'s Will'},
                {'name': 'Phantom Suit', 'defense': 24, 'class': 'Ninja', 'type': 'armor', 'enchantment': 'Shadow Form'},
                {'name': 'Mystic Robes', 'defense': 22, 'class': 'Magician', 'type': 'armor', 'enchantment': 'Spell Reflection'},
                {'name': 'Dragon Scale Vest', 'defense': 30, 'class': 'All', 'type': 'armor', 'enchantment': 'Fire Immunity'},
                # Elite Accessories
                {'name': 'Champion\'s Ring', 'attack': 5, 'defense': 8, 'class': 'All', 'type': 'accessory', 'enchantment': 'Battle Prowess'},
                {'name': 'Mage\'s Amulet', 'attack': 8, 'defense': 4, 'class': 'Magician', 'type': 'accessory', 'enchantment': 'Arcane Power'},
                {'name': 'Assassin\'s Mask', 'attack': 7, 'defense': 5, 'class': 'Ninja', 'type': 'accessory', 'enchantment': 'Stealth Mastery'},
            ],
            'Gold': [
                # Legendary Warrior Weapons
                {'name': 'Dragonbane Greatsword', 'attack': 50, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Dragon Slayer'},
                {'name': 'Godslayer Blade', 'attack': 48, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Divine Strike'},
                {'name': 'Eternal Warhammer', 'attack': 52, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Immortal Fury'},
                {'name': 'Chaos Reaper', 'attack': 49, 'class': 'Warrior', 'type': 'weapon', 'enchantment': 'Chaos Storm'},
                # Legendary Ninja Weapons
                {'name': 'Void Assassin Katana', 'attack': 45, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Void Cut'},
                {'name': 'Soul Stealer', 'attack': 43, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Life Drain'},
                {'name': 'Time Ripper', 'attack': 47, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Time Slash'},
                {'name': 'Shadow Lord\'s Edge', 'attack': 44, 'class': 'Ninja', 'type': 'weapon', 'enchantment': 'Shadow Army'},
                # Legendary Magician Weapons
                {'name': 'Reality Shatter Orb', 'attack': 55, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Reality Break'},
                {'name': 'Cosmic Staff', 'attack': 53, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Star Fall'},
                {'name': 'Apocalypse Rod', 'attack': 57, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'World End'},
                {'name': 'Infinity Wand', 'attack': 54, 'class': 'Magician', 'type': 'weapon', 'enchantment': 'Limitless Power'},
                # Legendary Armor
                {'name': 'Titanforge Battleplate', 'defense': 40, 'class': 'Warrior', 'type': 'armor', 'enchantment': 'Titan\'s Strength'},
                {'name': 'Shadowmeld Armor', 'defense': 35, 'class': 'Ninja', 'type': 'armor', 'enchantment': 'Perfect Stealth'},
                {'name': 'Celestial Archmage Robes', 'defense': 32, 'class': 'Magician', 'type': 'armor', 'enchantment': 'Divine Magic'},
                {'name': 'God-Emperor\'s Mail', 'defense': 45, 'class': 'All', 'type': 'armor', 'enchantment': 'Imperial Authority'},
                # Legendary Accessories
                {'name': 'Master Hunter Crown', 'attack': 10, 'defense': 15, 'class': 'All', 'type': 'accessory', 'enchantment': 'Apex Predator'},
                {'name': 'Titan\'s Bracer', 'attack': 8, 'defense': 12, 'class': 'All', 'type': 'accessory', 'enchantment': 'Giant\'s Power'},
                {'name': 'Phoenix Feather Cloak', 'attack': 12, 'defense': 10, 'class': 'All', 'type': 'accessory', 'enchantment': 'Resurrection'},
                {'name': 'Demon Lord\'s Eye', 'attack': 15, 'defense': 8, 'class': 'All', 'type': 'accessory', 'enchantment': 'True Sight'},
            ]
        }
        
        # Special Equipment Sets - unlock all pieces for set bonuses
        self.equipment_sets = {
            'Hunter': {
                'pieces': ['Hunter\'s Blade', 'Hunter\'s Leather', 'Hunter\'s Boots', 'Hunter\'s Gloves'],
                'set_bonus': {'attack': 5, 'defense': 5, 'special': 'Track monsters easier'},
                'difficulty': 'Bronze'
            },
            'Elite Guardian': {
                'pieces': ['Elite Slayer Sword', 'Elite Guardian Mail', 'Guardian Helm', 'Guardian Gauntlets'],
                'set_bonus': {'attack': 10, 'defense': 10, 'special': 'Immune to critical hits'},
                'difficulty': 'Silver'  
            },
            'Legendary Dragon Slayer': {
                'pieces': ['Dragonbane Greatsword', 'Titanforge Battleplate', 'Dragon Scale Helm', 'Dragonhide Boots'],
                'set_bonus': {'attack': 20, 'defense': 20, 'special': 'Dragon damage immunity'},
                'difficulty': 'Gold'
            }
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
        
        # Restore active bounties (legacy support)
        for bounty_dict in bounty_data.get('active', []):
            bounty = Bounty.from_dict(bounty_dict)
            self.active_bounties.append(bounty)
        
        # Restore hero's bounties (new system)
        hero = self.gui.game_state.hero
        if 'hero_bounties' in bounty_data:
            hero['bounties'] = bounty_data['hero_bounties']
        else:
            # Legacy fallback - if no hero_bounties, initialize empty
            if 'bounties' not in hero:
                hero['bounties'] = []

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
        
        # Create elite version with 1.5x HP and Attack
        elite = {
            'name': f"Elite {base['name']}",
            'hp': int(base['hp'] * 1.5),
            'maxhp': int(base['maxhp'] * 1.5),
            'attack': int(base['attack'] * 1.5),
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

        # Filter by level range and biome - stricter level filtering
        level_min = max(1, hero_level - 1)
        level_max = hero_level + 1  # Reduced from +2 to +1
        
        suitable_monsters = [
            (name, data) for name, data in monsters.items()
            if (level_min <= data['level'] <= level_max and
                data.get('biome', 'grassland') == current_biome)
        ]

        if not suitable_monsters:
            # Fallback to any level-appropriate monster (still strict on level)
            suitable_monsters = [
                (name, data) for name, data in monsters.items()
                if level_min <= data['level'] <= level_max
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
        # Reduced reward multipliers for better balance
        gold_mult = {'Bronze': 1.5, 'Silver': 2.0, 'Gold': 2.5}
        base_gold = target_data.get('gold', 10)

        reward_gold = int(base_gold * gold_mult[difficulty])
        
        # Filter rewards by hero class
        hero = self.gui.game_state.hero
        hero_class = hero.get('class', 'Warrior')
        suitable_rewards = [
            reward for reward in self.bounty_rewards[difficulty]
            if reward.get('class') == hero_class or reward.get('class') == 'All'
        ]
        reward_item = random.choice(suitable_rewards) if suitable_rewards else self.bounty_rewards[difficulty][0]

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
        count_mult = {'Bronze': 3, 'Silver': 5, 'Gold': 7}
        target_count = count_mult[difficulty]

        gold_mult = {'Bronze': 1.0, 'Silver': 1.3, 'Gold': 1.6}
        base_gold = target_data.get('gold', 10)
        reward_gold = int(base_gold * target_count * gold_mult[difficulty])

        # Filter rewards by hero class
        hero = self.gui.game_state.hero
        hero_class = hero.get('class', 'Warrior')
        suitable_rewards = [
            reward for reward in self.bounty_rewards[difficulty]
            if reward.get('class') == hero_class or reward.get('class') == 'All'
        ]
        reward_item = random.choice(suitable_rewards) if suitable_rewards else self.bounty_rewards[difficulty][0]

        biome = target_data.get('biome', 'grassland')
        biome_names = {
            'grassland': 'grasslands',
            'desert': 'desert',
            'dungeon': 'dungeons', 
            'ocean': 'ocean depths'
        }
        biome_text = biome_names.get(biome, 'unknown lands')

        return Bounty(
            bounty_type='collector',
            target=target_name,
            target_count=target_count,
            reward_gold=reward_gold,
            reward_item=reward_item,
            description=f"Collect bounty: Defeat {target_count} "
                       f"{target_name}s in the {biome_text}",
            difficulty=difficulty
        )

    def _generate_elite_boss_bounty(self, target_name,
                                     target_data, difficulty):
        """Generate elite boss bounty (tougher version of monster)"""
        gold_mult = {'Bronze': 2.0, 'Silver': 2.8, 'Gold': 3.5}
        base_gold = target_data.get('gold', 10)
        reward_gold = int(base_gold * gold_mult[difficulty])

        # Filter rewards by hero class
        hero = self.gui.game_state.hero
        hero_class = hero.get('class', 'Warrior')
        suitable_rewards = [
            reward for reward in self.bounty_rewards[difficulty]
            if reward.get('class') == hero_class or reward.get('class') == 'All'
        ]
        reward_item = random.choice(suitable_rewards) if suitable_rewards else self.bounty_rewards[difficulty][0]

        biome = target_data.get('biome', 'grassland')
        biome_names = {
            'grassland': 'grasslands',
            'desert': 'desert',
            'dungeon': 'dungeons', 
            'ocean': 'ocean depths'
        }
        biome_text = biome_names.get(biome, 'unknown lands')

        return Bounty(
            bounty_type='elite_boss',
            target=f"Elite {target_name}",
            target_count=1,
            reward_gold=reward_gold,
            reward_item=reward_item,
            description=f"Defeat the Elite {target_name} in the {biome_text} - "
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
        """Get all active bounties (including completed ones awaiting reward claim)"""
        self.initialize_hero_bounties(hero)
        active = [
            b for b in hero['bounties']
            if b.get('status') == 'active'  # Include completed bounties until claimed
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
        return self.check_bounty_progress_with_elite(hero, monster_killed, False)
    
    def check_bounty_progress_with_elite(self, hero, monster_killed, is_elite_encounter):
        """Check if killing a monster progresses any active bounties, considering elite encounters"""
        active_bounties = self.get_active_bounties(hero)
        progressed = []

        for bounty in active_bounties:
            # Check for hunt and collector bounties
            if bounty.target == monster_killed and bounty.bounty_type != 'elite_boss':
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

            # Check for elite boss bounties - only progress if this was an elite encounter
            elif (bounty.bounty_type == 'elite_boss' and is_elite_encounter):
                # For elite bounties, compare the bounty target directly with the monster killed
                # (monster_killed should already be in "Elite MonsterName" format from combat system)
                if bounty.target == monster_killed:
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

        # Award equipment if specified
        if bounty.reward_item:
            reward = bounty.reward_item
            reward_type = reward.get('type', 'accessory')
            
            if reward_type == 'weapon':
                # Auto-equip weapon and update stats
                old_weapon = hero.get('weapon', 'None')
                hero['weapon'] = reward['name']
                
                # Store base attack if not already stored
                if 'base_attack' not in hero:
                    hero['base_attack'] = hero.get('attack', 5) - reward.get('attack', 0)
                
                # Update attack stat
                hero['attack'] = hero['base_attack'] + reward.get('attack', 0)
                
            elif reward_type == 'armor':
                # Auto-equip armor and update stats
                old_armor = hero.get('armour', 'None') 
                hero['armour'] = reward['name']
                
                # Store base defense if not already stored
                if 'base_defense' not in hero:
                    hero['base_defense'] = hero.get('defense', 5) - reward.get('defense', 0)
                
                # Update defense stat
                hero['defense'] = hero['base_defense'] + reward.get('defense', 0)
                
            else:  # accessory
                # Add to inventory for accessories
                if 'bounty_accessories' not in hero:
                    hero['bounty_accessories'] = []
                hero['bounty_accessories'].append(reward)

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

        # Show active bounties (separate completed from in-progress)
        if active:
            completed_bounties = [b for b in active if b.completed]
            in_progress_bounties = [b for b in active if not b.completed]
            
            # Show completed bounties first (ready to claim)
            if completed_bounties:
                self.gui.print_text("🏆 COMPLETED BOUNTIES (Ready to Claim):")
                for i, bounty in enumerate(completed_bounties, 1):
                    self._display_bounty(bounty, f"✅ Completed {i}")
                self.gui.print_text("")
            
            # Show in-progress bounties
            if in_progress_bounties:
                self.gui.print_text("📋 ACTIVE BOUNTIES (In Progress):")
                for i, bounty in enumerate(in_progress_bounties, 1):
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

        # Only show claim rewards if there are completed bounties
        completed_bounties = [b for b in active if b.completed] if active else []
        if completed_bounties:
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
            self.gui.print_text("   ⚡ Tip: Elite monsters have 25% spawn chance when fighting regular monsters")

        self.gui.print_text(f"   💰 Reward: {bounty.reward_gold} gold")
        if bounty.reward_item:
            reward = bounty.reward_item
            item_name = reward.get('name', 'Unknown Item')
            reward_type = reward.get('type', 'accessory')
            
            # Show type-specific icons and stats
            if reward_type == 'weapon':
                attack = reward.get('attack', 0)
                self.gui.print_text(f"   ⚔️ Weapon: {item_name} (+{attack} attack)")
            elif reward_type == 'armor':
                defense = reward.get('defense', 0)
                self.gui.print_text(f"   🛡️ Armor: {item_name} (+{defense} defense)")
            else:  # accessory
                attack = reward.get('attack', 0)
                defense = reward.get('defense', 0)
                bonus_text = []
                if attack > 0:
                    bonus_text.append(f"+{attack} attack")
                if defense > 0:
                    bonus_text.append(f"+{defense} defense")
                bonus_str = ", ".join(bonus_text) if bonus_text else "special powers"
                self.gui.print_text(f"   💍 Accessory: {item_name} ({bonus_str})")

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
        self.gui.print_text("\n🏆 SELECT BOUNTY TO CLAIM:\n")

        for i, bounty in enumerate(completed, 1):
            self._display_bounty(bounty, f"Reward {i}")

        # Create selection buttons
        buttons = [f"{i}. Claim Reward" for i in range(1, len(completed) + 1)]
        if len(completed) > 1:
            buttons.append("🎁 Claim All")
        buttons.append("❌ Cancel")

        def on_choice(choice):
            if choice <= len(completed):
                # Claim individual bounty
                selected = completed[choice - 1]
                if self.claim_bounty_reward(hero, selected):
                    self.gui.print_text(
                        f"\n✅ Claimed {selected.reward_gold} gold!"
                    )
                    if selected.reward_item:
                        reward = selected.reward_item
                        item_name = reward.get('name', 'Item')
                        reward_type = reward.get('type', 'accessory')
                        
                        if reward_type == 'weapon':
                            self.gui.print_text(f"⚔️ New weapon equipped: {item_name}")
                        elif reward_type == 'armor':
                            self.gui.print_text(f"🛡️ New armor equipped: {item_name}")
                        else:
                            self.gui.print_text(f"💍 Received accessory: {item_name}")
                    self.gui.root.after(2000, self.show_bounty_board)
            elif choice == len(completed) + 1 and len(completed) > 1:
                # Claim all bounties
                total_gold = 0
                items_received = []
                for bounty in completed:
                    if self.claim_bounty_reward(hero, bounty):
                        total_gold += bounty.reward_gold
                        if bounty.reward_item:
                            item_name = bounty.reward_item.get('name', 'Item')
                            items_received.append(item_name)
                
                self.gui.print_text(f"\n✅ Claimed {total_gold} gold total!")
                if items_received:
                    self.gui.print_text(f"🎁 Items received: {', '.join(items_received)}")
                self.gui.root.after(2000, self.show_bounty_board)
            else:
                # Cancel
                self.show_bounty_board()

        self.gui.set_buttons(buttons, on_choice)

    def _refresh_bounties(self):
        """Generate new bounties for the board"""
        hero = self.gui.game_state.hero
        self.initialize_hero_bounties(hero)

        # Remove only available bounties, keep active/completed ones
        hero['bounties'] = [b for b in hero['bounties'] if b.get('status') != 'available']

        # Generate 3 new unique bounties (1 of each difficulty)
        existing_targets = {b.get('target') for b in hero['bounties']}
        
        for difficulty in ['Bronze', 'Silver', 'Gold']:
            attempts = 0
            while attempts < 10:  # Prevent infinite loop
                bounty = self.generate_bounty(difficulty)
                if bounty and bounty.target not in existing_targets:
                    hero['bounties'].append(bounty.to_dict())
                    existing_targets.add(bounty.target)
                    break
                attempts += 1

        self.gui.print_text("\n🔄 Bounty board refreshed!")
        self.gui.print_text("   New bounties available!")
        self.gui.root.after(1000, self.show_bounty_board)

    def drop_bounty(self, hero, bounty_index):
        """Drop (remove) an active bounty by index"""
        self.initialize_hero_bounties(hero)
        active_bounties = [b for b in hero['bounties'] if b.get('status') == 'active' and not b.get('completed', False)]
        
        if 0 <= bounty_index < len(active_bounties):
            # Find the bounty to drop in the original list
            bounty_to_drop = active_bounties[bounty_index]
            # Remove it from the hero's bounties
            hero['bounties'] = [b for b in hero['bounties'] if not (
                b['target'] == bounty_to_drop['target'] and
                b['difficulty'] == bounty_to_drop['difficulty'] and
                b['bounty_type'] == bounty_to_drop['bounty_type'] and
                b.get('status') == 'active'
            )]
            return True
        return False
