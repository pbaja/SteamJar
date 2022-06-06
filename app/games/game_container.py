import logging
from pathlib import Path
from typing import List
from dataclasses import dataclass

from .registry import registry_get_key
from ..constants import BOTTLES_CLI_CMD
from .game_container_kind import GameContainerKind

@dataclass
class GameContainer:
    # Container kind. Used to generate command
    kind: GameContainerKind
    # Path to a container root directory. It must contain drive_c directory and system.reg file.
    path: Path
    # Display name. Can be empty.
    display_name: str = ''
    # Container name. If the kind is BOTTLE, the name equals bottle name. Can be empty.
    name: str = ''
    

    def command(self, executable: str, arguments: List[str] = None) -> List[str]:
        '''
        Returns an array, containing a command that should be run by Steam to run given executable, within this container
        '''

        # Run via Bottles
        if self.kind == GameContainerKind.BOTTLE:
            cmd = BOTTLES_CLI_CMD + ['run', '-b', self.name, '-e', executable]
            if arguments is not None:
                cmd += ['-a', " ".join(arguments)]
            return cmd
        # Run natively
        elif self.kind == GameContainerKind.NATIVE:
            return [executable] + arguments
        # Other methods of running are not supported yet
        else:
            logging.error(f'Could not run {self.display_name}. Kind {self.kind} is not yet supported')

    def registry(self, key) -> 'RegistryKey':
        '''
        Returns RegistryKey at a given key, or None if key has not been found
        '''

        return registry_get_key(self.path / 'system.reg', key)

    def list_games(self) -> ['Game']:
        '''
        Searches for games inside this container. Returns a list of games
        '''

        from .stores import gog
        games = gog.list_games(self)

        from .stores import ubisoft
        games += ubisoft.list_games(self)

        return games