import os
import yaml
import random
from typing import Dict, Any


def _join_repo_path(*parts):
    base = os.path.dirname(__file__)
    return os.path.join(base, *parts)


def load_yaml_dir(dir_path: str) -> Dict[str, Any]:
    """Load all YAML files from a directory and merge them into a single dict.

    Each YAML file is expected to contain a mapping where the top-level key
    is the entity name (this mirrors the existing repo convention).
    """
    result = {}
    full_dir = _join_repo_path(dir_path)
    if not os.path.isdir(full_dir):
        return result
    for fname in os.listdir(full_dir):
        if not (fname.endswith('.yaml') or fname.endswith('.yml')):
            continue
        path = os.path.join(full_dir, fname)
        with open(path, 'r', encoding='utf-8') as fh:
            data = yaml.safe_load(fh) or {}
            # data is expected to be a mapping; update the result
            result.update(data)
    return result


def load_store(file_path: str = 'store.yaml') -> Dict[str, Any]:
    full = _join_repo_path(file_path)
    if not os.path.isfile(full):
        return {}
    with open(full, 'r', encoding='utf-8') as fh:
        return yaml.safe_load(fh) or {}


def damage_calculator(attack: int, defense: int, attacker_level: int = 1, defender_level: int = 1) -> int:
    """Improved damage calculator with level consideration and reduced variance
    
    Key improvements:
    - Reduced randomness (80-120% instead of 100-200%)
    - Level differential matters (±15% per level difference)
    - Percentage-based defense (prevents complete immunity)
    - Minimum damage scales with level
    - More predictable combat flow
    """
    # Base damage with controlled randomness (80-120% of attack)
    variance = random.uniform(0.8, 1.2)
    base_damage = attack * variance
    
    # Level differential bonus/penalty (±15% per level difference, capped at ±75%)
    level_diff = max(-5, min(5, attacker_level - defender_level))
    level_modifier = 1.0 + (level_diff * 0.15)
    base_damage *= level_modifier
    
    # Defense as damage reduction percentage (diminishing returns)
    defense_percentage = defense / (defense + 15)
    defense_percentage = min(0.85, defense_percentage)  # Cap at 85% reduction
    
    final_damage = base_damage * (1 - defense_percentage)
    
    # Minimum damage scales with attacker level
    min_damage = max(1, (attacker_level + 1) // 2)
    
    return max(min_damage, int(round(final_damage)))


def fight_round(hero: Dict[str, Any], monster: Dict[str, Any]) -> Dict[str, Any]:
    """Perform a single combat round between hero and monster.

    Returns a dict with the damage done and updated hp values. Does not
    perform any I/O or sleeps — the caller (UI) controls presentation.
    """
    # Get levels for damage calculation
    hero_level = hero.get('level', 1)
    monster_level = monster.get('level', 1)
    
    hero_damage = damage_calculator(hero.get('attack', 1), monster.get('defense', 0), hero_level, monster_level)
    monster['hp'] = max(0, monster.get('hp', 0) - hero_damage)

    monster_damage = damage_calculator(monster.get('attack', 1), hero.get('defense', 0), monster_level, hero_level)
    hero['hp'] = max(0, hero.get('hp', 0) - monster_damage)

    result = {
        'hero_damage': hero_damage,
        'monster_damage': monster_damage,
        'hero_hp': hero['hp'],
        'monster_hp': monster['hp'],
        'hero_dead': hero['hp'] <= 0,
        'monster_dead': monster['hp'] <= 0,
    }
    return result


def level_up(hero: Dict[str, Any], monster: Dict[str, Any]) -> bool:
    """Grant XP for defeating a monster and handle leveling.

    Returns True if the hero leveled up.
    """
    hero['xp'] = hero.get('xp', 0) + monster.get('level', 0)
    leveled = False
    if hero['xp'] >= hero.get('level', 1) * 5:
        hero['maxhp'] = hero.get('maxhp', 1) * 2
        hero['hp'] = hero['maxhp']
        hero['xp'] = 0
        hero['level'] = hero.get('level', 1) + 1
        leveled = True
    return leveled


if __name__ == '__main__':
    # quick smoke-run when executed directly
    heros = load_yaml_dir('heros')
    monsters = load_yaml_dir('monsters')
    store = load_store('store.yaml')
    print(f"Loaded {len(heros)} heros, {len(monsters)} monsters, store categories: {len(store)}")
