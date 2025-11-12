import os
import yaml


class GameState:
    def __init__(self):
        self.hero = {}
        self.monsters = {}
        self.heros = {}
        self.hero_defaults = {}
        self.choices = {}


def yaml_file_to_dictionary(file, dict):
    with open(file, encoding='utf-8') as fh:
        fh_yaml = yaml.safe_load(fh)
        dict.update(fh_yaml)
    return dict


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


def initialize_game_state():
    state = GameState()

    # Load monsters
    files = os.listdir('monsters/')
    for file in files:
        state.monsters = yaml_file_to_dictionary(f"monsters/{file}", state.monsters)

    # Load heros
    files = os.listdir('heros/')
    for file in files:
        state.heros = yaml_file_to_dictionary(f"heros/{file}", state.heros)

    state.hero_defaults = state.heros
    i = 1
    for hero in state.heros:
        print(f"{hero}: {i}")
        state.choices[str(i)] = hero
        i += 1
        hero_status(state.heros[hero])

    return state
