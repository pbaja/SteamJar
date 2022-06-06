import logging
from typing import List
from pathlib import Path 

from .game_container import GameContainer
from .game_container_kind import GameContainerKind


def list_containers() -> List['GameContainer']:
    '''
    Searches the system for a game containers
    '''

    containers = []

    # Search for bottles
    bottles_path = Path.home() / '.var' / 'app' / 'com.usebottles.bottles' / 'data' / 'bottles' / 'bottles'
    if bottles_path.exists():
        # Iterate over directory
        for bottle_path in bottles_path.iterdir():
            containers.append(GameContainer(
                display_name = bottle_path.stem,
                name = bottle_path.stem,
                kind = GameContainerKind.BOTTLE,
                path = bottle_path
            ))
    else:
        logging.warn('Bottles directory not found, are you sure Bottles is installed?')
    
    # Search for containers in steam
    # There:    ~/.steam/steam/steamapps/compatdata
    # Or There: ~/.var/app/com.valvesoftware.Steam/data/Steam/steamapps/compatdata
    #TODO

    # Search for wine
    # There:    ~/.wine/
    #TODO

    return containers