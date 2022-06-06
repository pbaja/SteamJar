import logging
from typing import List
from pathlib import Path

from ..game import Game
from ..game_store import GameStore

def command(game: 'Game') -> List[str]:
    '''
    Returns an array containing a command that will run a given game via the launcher
    '''

    return game.container.command(str(game.executable))

def list_games(container: 'GameContainer') -> List['Game']:
    '''
    Searches for GOG Galaxy games inside a container
    '''

    # Load registry
    installs = container.registry('Software/Wow6432Node/GOG.com/Games')
    if installs is None:
        # Key not found. GOG Galaxy is not installed or has no games installed
        logging.debug(f'GOG Galaxy is not installed or has not games in container: {container.name}')
        return []

    # Load games
    games = []
    for install_id, install_key in installs.children.items():

        # Build executable path
        executable_path = Path(install_key["launchCommand"].strip().replace('\\\\', '/')).parts[1:]
        executable_path = container.path / "drive_c" / Path(*executable_path) 

        # Add game
        games.append(Game(
            name=install_key['gameName'], 
            store_id=install_id, 
            executable=executable_path, 
            container=container, 
            store=GameStore.GOG_GALAXY
        ))
    return games