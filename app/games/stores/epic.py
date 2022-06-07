import logging, json
from typing import List
from pathlib import Path

from ..game import Game
from ..game_store import GameStore
from ..game_container import GameContainer

EPIC_LAUNCHER_EXE32 = 'Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe'
EPIC_LAUNCHER_EXE64 = 'Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win64/EpicGamesLauncher.exe'

def command(game: 'Game') -> List[str]:
    '''
    Returns an array containing a command that will run a given game via the launcher
    '''

    launch_exec = game.container.path / 'drive_c' / EPIC_LAUNCHER_EXE64
    if not launch_exec.exists():
        launch_exec = game.container.path / 'drive_c' / EPIC_LAUNCHER_EXE32
    if not launch_exec.exists():
        logging.error('Epic Game Launcher executable not found')
        return []

    launch_args = f'com.epicgames.launcher://apps/{game.store_id}?action=launch&silent=true'

    return game.container.command(str(launch_exec), [launch_args])

def list_games(container: 'GameContainer') -> List['Game']:
    '''
    Searches for Epic Games Launcher games inside a container
    '''

    # Get path to manifests
    manifests = container.path / 'drive_c' / 'ProgramData' / 'Epic' / 'EpicGamesLauncher' / 'Data' / 'Manifests'
    if not manifests.exists():
        # Probably not installed or never run
        logging.debug(f'Epic Games Launcher is not installed in container: {container.name}')
        print(manifests)
        return []

    # Load games
    games = []
    for manifest_path in manifests.iterdir():

        # Ignore directories
        if not manifest_path.is_file():
            continue

        # Load manifest
        try:
            # Parse manifest as json
            manifest = json.load(manifest_path.open('r'))
            
            # Build executable path
            executable_path = Path(manifest['InstallLocation'].strip().replace('\\\\', '/')).parts[1:]
            executable_path = container.path / 'drive_c' / Path(*executable_path) / manifest['LaunchExecutable']

            # Create store catalog ID
            store_id = manifest['CatalogNamespace'] + ':' + manifest['CatalogItemId'] + ':' + manifest['AppName']

            # Add game
            games.append(Game(
                name = manifest['DisplayName'], 
                store_id = store_id, 
                executable = executable_path, 
                container = container, 
                store = GameStore.EPIC_GAMES
            ))

        except json.JSONDecodeError:
            logging.error('Failed to parse game manifest')

    return games