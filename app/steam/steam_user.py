import json
from pathlib import Path
from dataclasses import dataclass
from typing import List

from . import vdf
from .shortcut import Shortcut


class SteamUser:
    name: str
    steam_id: int
    path: Path
    
    def __init__(self, steam_id, path):

        # Try to parse username from localconfig.vdf
        name = 'OfflineUser' if steam_id == 0 else f'{steam_id}'
        local_config_path = path / 'config' / 'localconfig.vdf'
        if local_config_path.exists():
            with local_config_path.open('r') as file:
                for line in file:
                    name_tag = '\x09\x09"PersonaName"\x09\x09'
                    if line.startswith(name_tag):
                        name = line[len(name_tag)+1:-2]
                        break

        # Save values
        self.name = name
        self.steam_id = steam_id
        self.path = path

    def load_shortcuts(self) -> List[Shortcut]:
        '''
            Loads all shortcuts from userdata/USER_ID/config/shortcuts.vdf
        '''

        shortcuts = []
        user_shortcuts_path = self.path / 'config' / 'shortcuts.vdf'
        if user_shortcuts_path.exists():
            data = vdf.load(user_shortcuts_path)
            for shortcut in data['shortcuts'].values():
                shortcuts.append(Shortcut.from_dict(shortcut))
        return shortcuts

    def save_shortcuts(self, shortcuts: List[Shortcut]) -> None:
        '''
            Saves all shortcuts to userdata/USER_ID/config/shortcuts.vdf
        '''

        user_config_path = self.path / 'config'
        if user_config_path.exists():
            # Convert arrays to dicts
            shortcuts_dict = {}
            for idx, shortcut in enumerate(shortcuts):
                shortcuts_dict[str(idx)] = shortcut.to_dict()

            # Create or update shortcuts file
            user_shortcuts_path = user_config_path / 'shortcuts.vdf'
            vdf.save(user_shortcuts_path, {'shortcuts': shortcuts_dict})