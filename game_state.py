import os
import yaml
from logger_utils import get_logger

logger = get_logger(__name__)


class GameState:
    def __init__(self):
        self.hero = {}
        self.monsters = {}
        self.heros = {}
        self.hero_defaults = {}
        self.choices = {}


def _get_project_path(*parts):
    """Get path relative to project root."""
    base = os.path.dirname(__file__)
    return os.path.join(base, *parts)


def yaml_file_to_dictionary(file, target_dict):
    """Load YAML file into target dictionary with error handling.
    
    Args:
        file: Path to YAML file to load
        target_dict: Dictionary to update with loaded data
        
    Returns:
        The updated target_dict
    """
    try:
        with open(file, encoding='utf-8') as fh:
            fh_yaml = yaml.safe_load(fh)
            if fh_yaml and isinstance(fh_yaml, dict):
                target_dict.update(fh_yaml)
            else:
                logger.warning(f"Empty or invalid YAML structure in {file}")
    except FileNotFoundError:
        logger.error(f"YAML file not found: {file}")
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error in {file}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading {file}: {e}")
    
    return target_dict


def hero_status(hero):
    logger.info("Hero stats:")
    for key, value in hero.items():
        if key == 'xp':
            logger.info(f"{key}: {value}/{hero['level']*5}")
        elif key == 'item' and value is not None:
            logger.info(f"{key}: {value['name']}")
        else:
            logger.info(f"{key}: {value}")
    logger.info("")


def initialize_game_state():
    """Initialize game state by loading monsters and heroes from YAML files.
    
    Returns:
        GameState object with loaded data
    """
    state = GameState()

    # Load monsters with error handling
    try:
        monsters_dir = _get_project_path('monsters')
        if not os.path.isdir(monsters_dir):
            logger.error(f"Monsters directory not found: {monsters_dir}")
            return state
        
        files = os.listdir(monsters_dir)
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(monsters_dir, file)
                state.monsters = yaml_file_to_dictionary(file_path, state.monsters)
    except OSError as e:
        logger.error(f"Error accessing monsters directory: {e}")
        return state
    except Exception as e:
        logger.error(f"Unexpected error loading monsters: {e}")
        return state

    # Load heros with error handling
    try:
        heros_dir = _get_project_path('heros')
        if not os.path.isdir(heros_dir):
            logger.error(f"Heros directory not found: {heros_dir}")
            return state
        
        files = os.listdir(heros_dir)
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(heros_dir, file)
                state.heros = yaml_file_to_dictionary(file_path, state.heros)
    except OSError as e:
        logger.error(f"Error accessing heros directory: {e}")
        return state
    except Exception as e:
        logger.error(f"Unexpected error loading heros: {e}")
        return state

    state.hero_defaults = state.heros
    i = 1
    for hero in state.heros:
        logger.info(f"{hero}: {i}")
        state.choices[str(i)] = hero
        i += 1
        hero_status(state.heros[hero])

    return state
