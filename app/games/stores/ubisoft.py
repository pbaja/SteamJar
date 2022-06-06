import logging
from typing import List
from pathlib import Path

from ..game_store import GameStore
from ..game import Game

UBISOFT_CONNECT_EXEC = "UbisoftConnect.exe"

def command(game: 'Game'):
    '''
    Returns an array containing a command that will run a given game via the launcher
    '''

    try:
        # Load registry
        launcher = game.container.registry('Software/Wow6432Node/Ubisoft/Launcher')
        # Get launcher drectory from registry. For some reason it uses double slashes
        launcher_directory = launcher['InstallDir'].replace('\\\\', '/')
        # Remove first part from path (disk name)
        launcher_directory = Path(*Path(launcher_directory).parts[1:])

        # Create path and arguments
        launch_exec = game.container.path / "drive_c" / launcher_directory / UBISOFT_CONNECT_EXEC
        launch_args = f"uplay://launch/{game.store_id}/0"

        # Return list exec path and arguments
        return game.container.command(str(launch_exec), [launch_args])

    except TypeError:
        # Key not found in the registry. Ubisoft launcher is not installed.
        logging.warn('Tried launcing game, but Ubisoft Connect is not installed')
        return None


def list_games(container: 'GameContainer') -> List['Game']:
    '''
    Searches for Ubisoft Connect games inside a container
    '''

    # Load registry
    installs = container.registry('Software/Wow6432Node/Ubisoft/Launcher/Installs')
    if installs is None:
        # Key not found. Ubisoft Connect is not installed.
        logging.debug(f'Ubisoft Connect is not installed in container: {container.name}')
        return []

    # Load games
    games = []
    for install_id, install_key in installs.children.items():
        install_path = Path(install_key["InstallDir"].replace('\\\\', '/')).parts[1:]
        path = container.path / "drive_c" / Path(*install_path)
        games.append(Game(
            name=path.name, 
            store_id=install_id, 
            executable=path, 
            container=container, 
            store=GameStore.UBISOFT_CONNECT
        ))
    return games