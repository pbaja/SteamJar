import logging
from pathlib import Path
from typing import List
from dataclasses import dataclass

from .game_container import GameContainer
from .game_store import GameStore

@dataclass
class Game:
    # Game name. Read from the registry or extracted from directory name
    name: str
    # Store this game comes from
    store: 'GameStore'
    # Parent container
    container: 'GameContainer'
    # Absolute executable path (/home/deck/.../drive_c/Program Files/..../game.exe)
    executable: 'Path'
    # Game identifier in store. Can be empty.
    store_id: str = ''

    def command(self) -> List[str]:
        # Ubisoft Connect
        if self.store == GameStore.UBISOFT_CONNECT:
            from .stores import ubisoft
            return ubisoft.command(self)
        # GOG Galaxy
        elif self.store == GameStore.GOG_GALAXY:
            from .stores import gog
            return gog.command(self)
        # Epic Games Launcher
        elif self.store == GameStore.EPIC_GAMES:
            from .stores import epic
            return epic.command(self)
        # Unsupported
        else:
            logging.error(f"Store {self.store} is not supported yet")
            return None