import os
import yaml
import random
import sys
from os import system, name
from time import sleep
from pygame import mixer

def play_sound(name):
    mixer.init()
    mixer.music.load(f'./sounds/{name}')
    mixer.music.play()

def clear():
   if name == 'nt':
      _= system('cls')
   else:
      _= system('clear')

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
        print(f"You hit for {damage} damage!!!\n")
        monster['hp'] = monster['hp'] - damage
        damage = damage_calculator(monster['attack'] , hero['defense'])
        print(f"{monster['name']} hit for {damage} damage!!!")
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
    if not 'item' in hero:
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
        print(f"{key}: {value}")
    print("\n")

def monster_status(monster):
    print("\nMonster stats:")
    for key, value in monster.items():
        print(f"{key}: {value}")
    print("\n")

def next_action():
    clear()
    hero_status(hero)
    answer = input("\nWhat would you like to do next (1) shop (2) fight a monster? (3) Use an item? ")
    valid = ['1','2', '3']
    if answer in valid:
        return(answer)

def shop(hero):
    clear()
    print('''
                                      __  ._._._.
______ ___.__.   _____ _____ ________/  |_| | | |
\____ <   |  |  /     \\__  \\_  __ \   __\ | | |
|  |_> >___  | |  Y Y  \/ __ \|  | \/|  |  \|\|\|
|   __// ____| |__|_|  (____  /__|   |__|  ______
|__|   \/            \/     \/             \/\/\/
    ''')
    play_sound('store.mp3')
    print("Welcome to the shop! here are the items!")
    store = open("store.yaml")
    store_yaml =  yaml.safe_load(store)

    for item in store_yaml:
        if 'class' in store_yaml[item]:
            if hero['class'] != store_yaml[item]['class']:
                continue
        if 'ascii_art' in store_yaml[item]:
            with open(store_yaml[item]['ascii_art'], 'r') as file:
                art = file.read()
                print(art)
        for info in store_yaml[item]:
            if info == 'ascii_art':
                continue
            print(f"  {info} : {store_yaml[item][info]}")
        print("\n")


    answer = input(f" Your gold is {hero['gold'] }, What would you like in the pymart ? ")
    if answer in store_yaml:
        print(f"you picked {answer} it cost {store_yaml[answer]['cost']}" )
        hero['item'] = []
        if answer == 'Health Potion':
            hero['item'] = store_yaml[answer]
            print(f" You got an item it is {hero['item']['name']}")
            hero['gold'] = hero['gold'] - store_yaml[answer]['cost']
            print(f"you spent {store_yaml[answer]['cost']} of gold you have {hero['gold']} gold left. The Health Potion increases life. ")
            sleep(2)
        elif store_yaml[answer]['cost'] > hero['gold']:
            print("you dont have enough money.")
        elif store_yaml[answer]['class'] != hero['class']:
            print(f"You are not the class {store_yaml[answer]['class']}")
        else:
            hero['gold'] = hero['gold'] - store_yaml[answer]['cost']
            print(f"you spent {store_yaml[answer]['cost']} of gold you have {hero['gold']} gold left ")
            hero['weapon'] = store_yaml[answer]['name']
            hero['attack'] = hero['weapon']['attack']
            print(f"{hero['name']} equiped!!\n\t{hero['weapon']}\n")
            sleep(3)

def fight_monster():
    key, value = random.choice(list(monsters.items()))
    monster = value
    key
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
            play_sound('tada.mp3')
            print(f"You fought the {monster['name']} and {result}!! You won {monster['gold']} gold.")
            hero['gold'] += monster['gold']
            monster['hp'] = monster['maxhp']
        if result == 'lost':
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
 /  _____/   /  _  \    /     \ \_   _____/   \   _  \   \ /   /\_   _____/\______   \  | | | |
/   \  ___  /  /_\  \  /  \ /  \ |    __)_    /  /_\  \   Y   /  |    __)_  |       _/  | | | |
\    \_\  \/    |    \/    Y    \|        \   \  \_/   \     /   |        \ |    |   \   \|\|\|
 \______  /\____|__  /\____|__  /_______  /    \_____  /\___/   /_______  / |____|_  /   ______
        \/         \/         \/        \/           \/                 \/         \/    \/\/\/
            ''')
            play_sound('death.mp3')
            sleep(3)
            sys.exit()
        sleep(3)
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
