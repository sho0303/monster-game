import os
import yaml
import random
import sys
from os import system
from time import sleep
from pygame import mixer
import colorama
from colorama import Fore, Style
from game_state import GameState, initialize_game_state
from PIL import Image


class Display:
    """Handles all display-related functionality (ASCII art, screen clearing, etc.)"""
    
    @staticmethod
    def print_ascii(filename, color='\033[31m'):
        """Print ASCII art from file with color"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                ascii_art = file.read()
                print(f"{color}{ascii_art}{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"Warning: ASCII art file '{filename}' not found.")
        except Exception as e:
            print(f"Warning: Could not load ASCII art '{filename}': {e}")
    
    @staticmethod
    def show_image(filename, mode='ascii'):
        """Display a PNG image or ASCII art file
        
        Args:
            filename: Path to the image or ASCII file
            mode: 'ascii' to convert PNG to ASCII in terminal,
                  'viewer' to open PNG in default image viewer,
                  'auto' to detect file type and handle appropriately
        """
        # Auto-detect file type if mode is 'auto'
        if mode == 'auto':
            if filename.endswith('.txt'):
                mode = 'text'
            elif filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                mode = 'ascii'  # Default to ASCII representation in terminal
            else:
                mode = 'text'
        
        # Handle text/ASCII files
        if mode == 'text' or filename.endswith('.txt'):
            Display.print_ascii(filename, '\033[36m')
            return
        
        # Handle PNG/image files
        try:
            # Open the image
            img = Image.open(filename)
            
            if mode == 'viewer':
                # Open in default system image viewer
                img.show()
                print(f"Opening {filename} in image viewer...")
                return
            
            elif mode == 'ascii':
                # Convert to ASCII for terminal display
                # Resize for terminal display (smaller for better terminal fit)
                img = img.resize((40, 20), Image.NEAREST)
                
                # Convert to RGB (in case it has alpha channel)
                if img.mode == 'RGBA':
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])  # Use alpha as mask
                    img = background
                
                # Convert to grayscale for ASCII representation
                img = img.convert('L')
                
                # ASCII characters from dark to light
                ascii_chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']
                
                # Convert image to ASCII
                pixels = img.getdata()
                ascii_str = ''
                for i, pixel in enumerate(pixels):
                    ascii_str += ascii_chars[pixel // 25]
                    if (i + 1) % 40 == 0:
                        ascii_str += '\n'
                
                print(f"{Fore.CYAN}{ascii_str}{Style.RESET_ALL}")
            
            elif mode == 'both':
                # Show ASCII in terminal AND open in viewer
                Display.show_image(filename, mode='ascii')
                sleep(0.5)
                Display.show_image(filename, mode='viewer')
            
        except FileNotFoundError:
            print(f"Warning: Image file '{filename}' not found.")
        except Exception as e:
            print(f"Warning: Could not display image '{filename}': {e}")
    
    @staticmethod
    def clear():
        """Clear the terminal screen"""
        if os.name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')
    
    @staticmethod
    def print_fight_data(hero, monster):
        """Display hero and monster stats side by side during fight"""
        print_keys = ['name', 'defense', 'hp', 'attack']
        max_length = 0
        for key in print_keys:
            string = f"  {key}: {hero[key]}"
            if len(string) > max_length:
                max_length = len(string)

        for key in print_keys:
            string = f"  {key}: {hero[key]}"
            buffer = 5
            buffer = buffer + (max_length - len(string))
            string += (" " * buffer)
            string += f"{key}: {monster[key]}"
            print(string)
    
    @staticmethod
    def show_hero_status(hero):
        """Display hero stats with warrior art"""
        # Display hero art (PNG image converted to ASCII)
        Display.show_image('ascii_art/hero_warrior.png')
        
        print("\n⚔️  Hero Stats ⚔️")
        print("=" * 30)
        for key, value in hero.items():
            if key == 'xp':
                print(f"  {key}: {value}/{hero['level']*5}")
            elif key == 'item' and value is not None:
                print(f"  {key}: {value['name']}")
            else:
                print(f"  {key}: {value}")
        print("=" * 30)
        print()
    
    @staticmethod
    def show_monster_status(monster):
        """Display monster stats"""
        print("\nMonster stats:")
        for key, value in monster.items():
            print(f"{key}: {value}")
        print("\n")


class Audio:
    """Handles all audio/sound functionality"""
    
    @staticmethod
    def play_sound(name):
        """Play a sound file"""
        try:
            mixer.init()
            mixer.music.load(f'./sounds/{name}')
            mixer.music.play()
        except Exception as e:
            print(f"Warning: Could not play sound '{name}': {e}")



class Combat:
    """Handles all combat-related functionality"""
    
    def __init__(self):
        self.display = Display()
        self.audio = Audio()
    
    def calculate_damage(self, attack, defense):
        """Calculate damage with animation"""
        for i in range(1, 4):
            print("." * i)
            sleep(0.1)
        strike = random.randint(1, max(1, attack))
        strike = strike * 2
        damage = strike - defense
        return max(1, damage)
    
    def fight(self, hero, monster):
        """Execute a fight between hero and monster"""
        self.display.clear()
        self.audio.play_sound('buzzer.mp3')
        self.display.print_ascii('ascii_art/fighton.txt', '\033[31m')
        sleep(2)
        
        while hero['hp'] > 0 and monster['hp'] > 0:
            self.display.clear()
            self.display.print_fight_data(hero, monster)
            print("\n")
            
            # Hero attacks
            damage = self.calculate_damage(hero['attack'], monster['defense'])
            self.audio.play_sound('punch.mp3')
            print(f"You hit for {Fore.RED}{damage}{Style.RESET_ALL} damage!!!\n")
            monster['hp'] = monster['hp'] - damage
            
            # Monster attacks
            damage = self.calculate_damage(monster['attack'], hero['defense'])
            print(f"{monster['name']} hit for {Fore.RED}{damage}{Style.RESET_ALL} damage!!!")
            hero['hp'] = hero['hp'] - damage
            sleep(2)
        
        return 'won' if hero['hp'] > 0 else 'lost'
    
    def level_up(self, hero, monster):
        """Handle hero leveling up"""
        hero['xp'] += monster['level']
        if hero['xp'] >= hero['level'] * 5:
            self.audio.play_sound('levelup.wav')
            print("You have leveled up !!!!")
            print(f' Your level is now {hero["level"] + 1}')
            sleep(2)
            hero['maxhp'] = hero['maxhp'] * 2
            hero['hp'] = hero['maxhp']
            hero['xp'] = 0
            hero['level'] += 1


class Shop:
    """Handles shop-related functionality"""
    
    def __init__(self):
        self.display = Display()
        self.audio = Audio()
    
    def open(self, hero):
        """Open the shop interface"""
        self.audio.play_sound('store.mp3')
        try:
            with open("store.yaml") as store:
                store_yaml = yaml.safe_load(store)
        except FileNotFoundError:
            print("Error: store.yaml not found!")
            sleep(2)
            return
        except Exception as e:
            print(f"Error loading store: {e}")
            sleep(2)
            return
        
        category = self._select_category(store_yaml)
        if category is None:
            return
        
        item = self._select_item(store_yaml, category, hero)
        if item is None:
            return
        
        self._purchase_item(hero, item, category)
    
    def _select_category(self, store_yaml):
        """Display categories and return selected category"""
        valid = False
        while not valid:
            self.display.clear()
            self.display.print_ascii('ascii_art/pymart.txt', '\033[34m')
            i = 1
            valid_answer = {}
            for category in store_yaml:
                print(f"{i}. {category}")
                valid_answer[str(i)] = category
                i += 1
            choice = input("\nWhat's your selection? ")
            if choice in valid_answer:
                valid = True
                category = valid_answer[choice]
                self.display.clear()
                return category
        return None
    
    def _select_item(self, store_yaml, category, hero):
        """Display items and return selected item"""
        i = 1
        item_choices = {}
        for item in store_yaml[category]:
            if item['class'] != hero['class'] and item['class'] != 'All':
                continue
            if 'ascii_art' in item:
                with open(item['ascii_art'], 'r') as file:
                    art = file.read()
                    print(art)
            print(f"{Fore.GREEN}({i}){Style.RESET_ALL}")
            for key, value in item.items():
                if key == 'ascii_art':
                    continue
                else:
                    print(f"{key}: {value}")
                    item_choices[str(i)] = item
            i += 1
            print("\n")

        item_choices['x'] = True
        print(f"{Fore.GREEN}(x) to exit{Style.RESET_ALL}\n")

        valid = False
        while not valid:
            selection = input(f" Your gold is {Fore.YELLOW}{hero['gold']}{Style.RESET_ALL}, Which item would you like to purchase? ")
            if selection in item_choices:
                valid = True

        if selection == 'x':
            return None
        
        return item_choices[selection]
    
    def _purchase_item(self, hero, item, category):
        """Process item purchase"""
        if item['cost'] > hero['gold']:
            print(f"You can not afford {item['name']}")
            sleep(2)
            return
        
        hero['gold'] = hero['gold'] - item['cost']
        
        if category == 'Armour':
            hero['armour'] = item['name']
            hero['defense'] = item['defense']
        elif category == 'Weapons':
            hero['weapon'] = item['name']
            hero['attack'] = item['attack']
        elif category == 'Items':
            hero['item'] = item
        
        print(f"Equipping {item['name']} !!")
        sleep(2)


class Inventory:
    """Handles inventory and item usage"""
    
    @staticmethod
    def use_item(hero):
        """Use an item from hero's inventory"""
        if hero.get('item') is None:
            print(' You do not have an item yet')
            return
        
        if hero['item']['name'] == 'Health Potion':
            if hero['hp'] == hero['maxhp']:
                answer = input('you have max life the potion will not do anything. Are you sure you want to do this? ')
                if answer == 'yes':
                    print("OK!")
                elif answer == 'no':
                    return
                else:
                    print('that is not a valid answer')
                    return
            hero['hp'] = hero['maxhp']
            print(f' You used the {hero["item"]["name"]}. You now have {hero["hp"]} hp!')
            hero['item'] = None
        sleep(2)


class MonsterEncounter:
    """Handles monster encounters and battles"""
    
    def __init__(self):
        self.display = Display()
        self.audio = Audio()
        self.combat = Combat()
    
    def start(self, game_state):
        """Start a monster encounter"""
        monster = self._select_random_monster(game_state)
        if monster is None:
            return
        
        print(f"A {monster['name']} has appeared!")
        self.display.show_monster_status(monster)
        
        action = self._get_player_choice()
        
        if action == '2':
            print("You've run away!")
            sleep(1.5)
        elif action == '1':
            self._execute_battle(game_state, monster)
    
    def _select_random_monster(self, game_state):
        """Select a random monster appropriate for hero's level"""
        valid_level = False
        attempts = 0
        while not valid_level and attempts < 100:
            key, value = random.choice(list(game_state.monsters.items()))
            if value['level'] <= game_state.hero['level'] * 2 and value['level'] >= game_state.hero['level'] - 1:
                return value.copy()  # Return a copy to preserve original
            attempts += 1
        return None
    
    def _get_player_choice(self):
        """Get player's choice to fight or run"""
        options = ['1', '2']
        valid = None
        while not valid:
            answer = input("Do you (1) fight or (2) run? ")
            if answer in options:
                return answer
        return '2'
    
    def _execute_battle(self, game_state, monster):
        """Execute the battle and handle results"""
        result = self.combat.fight(game_state.hero, monster)
        
        if result == 'won':
            self._handle_victory(game_state, monster)
        else:
            self._handle_defeat(game_state, monster)
        
        # Reset monster HP for next encounter
        monster['hp'] = monster['maxhp']
    
    def _handle_victory(self, game_state, monster):
        """Handle victory scenario"""
        self.display.clear()
        self.display.print_ascii('ascii_art/youwon.txt', '\033[33m')
        self.audio.play_sound('tada.mp3')
        sleep(2)
        self.display.clear()
        
        if monster.get('finalboss'):
            self._handle_final_victory(game_state)
        else:
            print(f"You fought the {monster['name']} and won!! You won {monster['gold']} gold.")
            game_state.hero['gold'] += monster['gold']
            self.combat.level_up(game_state.hero, monster)
    
    def _handle_final_victory(self, game_state):
        """Handle final boss victory"""
        print(f'Congratulations! You beat the final boss and won the game!!')
        self.display.clear()
        self.audio.play_sound('win.mp3')
        print(f' You won playing {game_state.hero["name"]} you beat Monster Game by Adam Walker and Aaron Walker!!!')
        sleep(4)
        self.display.clear()
        self.display.print_ascii('ascii_art/pyquest.txt', '\036[46m')
        sys.exit()
    
    def _handle_defeat(self, game_state, monster):
        """Handle defeat scenario"""
        self.display.clear()
        self.display.print_ascii('ascii_art/lost.txt', '\033[31m')
        self.audio.play_sound('death.mp3')
        sleep(2)
        self.display.clear()

        print(f'You lost to {monster["name"]} and lost all of your gold!')
        game_state.hero['gold'] = 0
        game_state.hero['lives_left'] -= 1
        game_state.hero['hp'] = game_state.hero['maxhp']
        
        if game_state.hero['lives_left'] < 1:
            self._handle_game_over()
    
    def _handle_game_over(self):
        """Handle game over scenario"""
        print('You are out of lives! You lost the game.')
        sleep(3)
        self.display.clear()
        self.display.print_ascii('ascii_art/lost.txt', '\033[31m')
        self.audio.play_sound('death.mp3')
        sleep(3)
        sys.exit()


class Game:
    """Main game controller class"""
    
    def __init__(self):
        self.display = Display()
        self.audio = Audio()
        self.shop = Shop()
        self.inventory = Inventory()
        self.monster_encounter = MonsterEncounter()
        self.game_state = None
    
    def start(self):
        """Start the game"""
        self.display.clear()
        self.audio.play_sound('start.mp3')
        self.display.print_ascii('ascii_art/pyquest.txt', '\033[35m')
        
        # Initialize game state
        self.game_state = initialize_game_state()
        
        # Hero selection
        self._select_hero()
        
        # Main game loop
        self._game_loop()
    
    def _select_hero(self):
        """Handle hero selection"""
        while not self.game_state.hero:
            answer = input("What hero would you like? (1), (2), (3): ")
            if answer in ['1', '2', '3']:
                print("You chose hero:")
                print(self.game_state.choices[answer], "\n")
                self.game_state.hero = self.game_state.heros[self.game_state.choices[answer]].copy()
                self.game_state.hero['name'] = self.game_state.choices[answer]
                self.game_state.hero['lives_left'] = 3
                self.game_state.hero['gold'] = 50
                self.game_state.hero['level'] = 1
                self.game_state.hero['xp'] = 0
                sleep(2)
    
    def _game_loop(self):
        """Main game loop"""
        actions = {
            "1": lambda: self.shop.open(self.game_state.hero),
            "2": lambda: self.monster_encounter.start(self.game_state),
            "3": lambda: self.inventory.use_item(self.game_state.hero)
        }
        
        while True:
            action = self._get_next_action()
            if action in actions:
                actions[action]()
            sleep(1)
            self.display.clear()
    
    def _get_next_action(self):
        """Get player's next action"""
        self.display.clear()
        self.display.print_ascii('ascii_art/pyquest.txt', '\033[35m')
        self.display.show_hero_status(self.game_state.hero)
        answer = input("\nWhat would you like to do next (1) shop (2) fight a monster? (3) Use an item? ")
        valid = ['1', '2', '3']
        if answer in valid:
            return answer
        return None


# Entry point
if __name__ == '__main__':
    game = Game()
    game.start()

