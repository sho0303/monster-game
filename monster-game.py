import os
import yaml
import random
import sys
from os import system, name
from time import sleep
from pygame import mixer
import colorama
from colorama import Fore, Style


def play_sound(name):
    mixer.init()
    mixer.music.load(f'./sounds/{name}')
    mixer.music.play()

def clear():
   if name == 'nt':
      _= system('cls')
   else:
      _= system('clear')

#def valid_answer(question):
#    list = ['1', '2', '3']

def print_fight_data(hero, monster):
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


def yaml_file_to_dictionary(file, dict):
    fh = open(file)
    fh_yaml = yaml.safe_load(fh)
    dict.update(fh_yaml)
    return dict

def fight_calculator(hero, monster):
    clear()
    play_sound('buzzer.mp3')
    print('''
___________.___  ________  ___ ______________   _______    _______    ._._._.
\_   _____/|   |/  _____/ /   |   \__    ___/   \   _  \   \      \   | | | |
 |    __)  |   /   \  ___/    ~    \|    |      /  /_\  \  /   |   \  | | | |
 |     \   |   \    \_\  \    Y    /|    |      \  \_/   \/    |    \  \|\|\|
 \___  /   |___|\______  /\___|_  / |____|       \_____  /\____|__  /  ______
     \/                \/       \/                     \/         \/   \/\/\/
    ''')
    sleep(3)
    while hero['hp'] > 0 and monster['hp'] > 0:
        clear()
        print_fight_data(hero, monster)
        print("\n")
        damage = damage_calculator(hero['attack'], monster['defense'])
        play_sound('punch.mp3')
        print(f"You hit for {Fore.RED}{damage}{Style.RESET_ALL} damage!!!\n")
        monster['hp'] = monster['hp'] - damage
        damage = damage_calculator(monster['attack'] , hero['defense'])
        print(f"{monster['name']} hit for {Fore.RED}{damage}{Style.RESET_ALL} damage!!!")
        hero['hp'] = hero['hp'] - damage
        sleep(3)
    if hero['hp'] < 1:
        return 'lost'
    else:
        return 'won'


def damage_calculator(attack, defense):
    i = 1
    while i < 4:
        print("." * i)
        i = i + 1
        sleep(0.1)
    strike = random.randint(1, attack)
    strike = strike * 2
    damage = strike - defense
    if damage <= 0:
        damage = 1
    return damage

def use_item(hero):
    if not 'item' in hero or hero['item'] == None:
        print(' You do not have an item yet')
        return
    if hero['item']['name'] == 'Health Potion':
        if hero['hp'] == hero['maxhp']:
            answer = input('you have max life the potion will not to anything. Are you sure you wand to do this?')
            if answer == 'yes':
                print("OK!")
            if answer == 'no':
                return
            else:
                print('that is not a valid answer')
                return
        hero['hp'] = hero['maxhp']
        print(f' You used the {hero["item"]["name"]}. You now have {hero["hp"]} hp!')
        hero['item'] = None
    sleep(2)

def hero_status(hero):
    print("\nHero stats:")
    for key, value in hero.items():
        if key == 'xp':
            print(f"{key}: {value}/{hero['level']*5}")
        elif key == 'item' and value != None:
            print(f"{key}: {value['name']}")
        else:
            print(f"{key}: {value}")
    print("\n")

def monster_status(monster):
    print("\nMonster stats:")
    for key, value in monster.items():
        print(f"{key}: {value}")
    print("\n")

def next_action():
    clear()
    print ('''
_______________.___. ________   ____ ______________ ____________________
\______   \__  |   | \_____  \ |    |   \_   _____//   _____/\__    ___/
 |     ___//   |   |  /  / \  \|    |   /|    __)_ \_____  \   |    |
 |    |    \____   | /   \_/.  \    |  / |        \/        \  |    |
 |____|    / ______| \_____\ \_/______/ /_______  /_______  /  |____|
           \/               \__>                \/        \/
    ''')
    hero_status(hero)
    answer = input("\nWhat would you like to do next (1) shop (2) fight a monster? (3) Use an item? ")
    valid = ['1','2', '3']
    if answer in valid:
        return(answer)

def shop(hero):
    play_sound('store.mp3')
    store = open("store.yaml")
    store_yaml =  yaml.safe_load(store)
    valid = False
    while valid == False:
        clear()
        print('''
                                          __  ._._._.
    ______ ___.__.   _____ _____ ________/  |_| | | |
    \____ <   |  |  /     \\__  \\_  __ \   __\ | | |
    |  |_> >___  | |  Y Y  \/ __ \|  | \/|  |  \|\|\|
    |   __// ____| |__|_|  (____  /__|   |__|  ______
    |__|   \/            \/     \/             \/\/\/
        ''')
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
            clear()

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
    while valid == False:
        selection = input(f" Your gold is {Fore.YELLOW}{hero['gold']}{Style.RESET_ALL}, Which item would you like to purchase? ")
        if selection in item_choices:
            valid = True

    if selection == 'x':
        return

    item = item_choices[selection]
    if item['cost'] > hero['gold']:
        print(f"You can not afford {item['name']}")
        sleep(2)
        return()
    else:
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


def level_up(hero , monster):
    hero['xp'] += monster['level']
    if hero['xp'] >= hero['level'] * 5:
        play_sound('levelup.wav')
        print("You have leveled up !!!!")
        print(f' Your level is now {hero["level"] + 1}')
        sleep(2)
        hero['maxhp'] = hero['maxhp'] * 2
        hero['hp'] = hero['maxhp']
        hero['xp'] = 0
        hero['level'] += 1


def fight_monster():
    valid_level = False
    while not valid_level:
        key, value = random.choice(list(monsters.items()))
        if value['level'] <= hero['level'] * 2 and value['level'] >= hero['level'] - 1:
            monster = value
            valid_level = True
    print(f"A {key} has appeared!")
    monster_status(monster)
    options = ['1', '2']
    valid = None
    while not valid:
        answer = input("Do you (1) fight or (2) run? ")
        if answer in options:
            valid = True
        else:
            continue
    if answer == '2':
        print("You've run away!")
        sleep(2)
    elif answer == '1':
        result = fight_calculator(hero, monster)
        if result == 'won':
            clear()
            print('''
_____.___.________   ____ ___     __      __________    _______      ._._._.
\__  |   |\_____  \ |    |   \   /  \    /  \_____  \   \      \     | | | |
 /   |   | /   |   \|    |   /   \   \/\/   //   |   \  /   |   \    | | | |
 \____   |/    |    \    |  /     \        //    |    \/    |    \    \|\|\|
 / ______|\_______  /______/       \__/\  / \_______  /\____|__  /    ______
 \/               \/                    \/          \/         \/     \/\/\/
            ''')
            play_sound('tada.mp3')
            sleep(2.5)
            clear()
            sleep(1)
            if 'finalboss' in monster:
                if monster['finalboss'] == True:
                    print(f'Congradulations! You beat the final boss and won the game!!')
                    clear()
                    play_sound('win.mp3')
                    print(f' You won playing {hero["name"]} you beat Monster Game by Adam Walker and Aaron Walker!!!')
                    sleep(5)
                    clear()
                    print('''
          ________    _____      _____  ___________   ___________   _________________________   ._._._.
         /  _____/  /  _  \    /     \ \_   _____/   \   _  \   \ /   /\_   _____/\______   \   | | | |
        /   \  ___  /  /_\  \  /  \ /  \ |    __)_    /  /_\  \   Y   /  |    __)_  |       _/  | | | |
        \    \_\  \/    |    \/    Y    \|        \   \  \_/   \     /   |        \ |    |   \   \|\|\|
         \______  /\____|__  /\____|__  /_______  /    \_____  /\___/   /_______  / |____|_  /   ______
                \/         \/         \/        \/           \/                 \/         \/    \/\/\/
                    ''')
                    sys.exit()

                else:
                    print(f"You fought the {monster['name']} and {result}!! You won {monster['gold']} gold.")
                    hero['gold'] += monster['gold']
                    level_up(hero,monster)
        if result == 'lost':
            clear()
            print('''
_____.___.________   ____ ___    .____    ________    ____________________   ._._._.
\__  |   |\_____  \ |    |   \   |    |   \_____  \  /   _____/\__    ___/   | | | |
 /   |   | /   |   \|    |   /   |    |    /   |   \ \_____  \   |    |      | | | |
 \____   |/    |    \    |  /    |    |___/    |    \/        \  |    |       \|\|\|
 / ______|\_______  /______/     |_______ \_______  /_______  /  |____|       ______
 \/               \/                     \/       \/        \/                \/\/\/
            ''')
            sleep(2.5)
            clear()

            print(f'You lost to {monster["name"]} and lost all of your gold!')
            hero['gold'] = 0
            hero['lives_left'] -= 1
            hero['hp'] = hero['maxhp']
        if hero['lives_left'] < 1:
            print('You are out of lives! You lost the game.')
            sleep(3)
            clear()

            print('''
  ________    _____      _____  ___________   ___________   _________________________   ._._._.
 /  _____/  /  _  \    /     \ \_   _____/   \   _  \   \ /   /\_   _____/\______   \   | | | |
/   \  ___  /  /_\  \  /  \ /  \ |    __)_    /  /_\  \   Y   /  |    __)_  |       _/  | | | |
\    \_\  \/    |    \/    Y    \|        \   \  \_/   \     /   |        \ |    |   \   \|\|\|
 \______  /\____|__  /\____|__  /_______  /    \_____  /\___/   /_______  / |____|_  /   ______
        \/         \/         \/        \/           \/                 \/         \/    \/\/\/
            ''')
            play_sound('death.mp3')
            sleep(3)
            sys.exit()
        sleep(3)
        monster['hp'] = monster['maxhp']
    print("\n")


clear()
play_sound('start.mp3')
print ('''
_______________.___. ________   ____ ______________ ____________________
\______   \__  |   | \_____  \ |    |   \_   _____//   _____/\__    ___/
 |     ___//   |   |  /  / \  \|    |   /|    __)_ \_____  \   |    |
 |    |    \____   | /   \_/.  \    |  / |        \/        \  |    |
 |____|    / ______| \_____\ \_/______/ /_______  /_______  /  |____|
           \/               \__>                \/        \/
''')
monsters = {}
files = os.listdir('monsters/')
for file in files:
    monsters = yaml_file_to_dictionary(f"monsters/{file}", monsters)

heros = {}
files = os.listdir('heros/')
for file in files:
    heros = yaml_file_to_dictionary(f"heros/{file}", heros)

hero_defaults = heros
i = 1
choices = {}
for hero in heros:
    print(f"{hero}: {i}")
    choices[str(i)] = hero
    i += 1
    hero_status(heros[hero])

hero = {}
while not hero:
    answer = input("What hero would you like? (1), (2), (3): ")
    if answer in ['1', '2', '3']:
        print("You chose hero:")
        print(choices[answer], "\n")
        hero = heros[choices[answer]]
        hero['name'] = choices[answer]
        hero['lives_left'] = 3
        hero['gold'] = 50
        hero['level'] = 1
        hero['xp'] = 0
        sleep(2)

while True:
    next = next_action()
    if next == "1":
        shop(hero)
    if next == "2":
        fight_monster()
    if next == "3":
        use_item(hero)
    sleep(1)
    clear()
