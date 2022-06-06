import random
from dataclasses import dataclass, asdict, field
from ..games.game import Game

@dataclass
class Shortcut:
    appid: int
    appname: str
    Exe: str = ''
    StartDir: str = ''
    icon: str = ''
    ShortcutPath: str = ''
    LaunchOptions: str = ''
    IsHidden: int = 0
    AllowDesktopConfig: int = 1
    AllowOverlay: int = 1
    openvr: int = 0
    Devkit: int = 0
    DevkitGameID: str = 0
    DevkitOverrideAppID: int = 0
    LastPlayTime: int = 0   # Unix timestamp when last launched. Never if 0.
    FlatpakAppID: str = ''
    tags: dict = field(default_factory = lambda: ({}))

    def to_dict(self) -> None:
        return asdict(self)

    def from_dict(data: dict) -> 'Shortcut':
        return Shortcut(**data)

    def from_game(game: Game) -> 'Shortcut':
        shortcut = Shortcut(appid = random.randint(0xB0000000, 0xFFFFFFFF), appname = game.name)
        shortcut.update_from_game(game)
        return shortcut

    def update_from_game(self, game: Game):
        command = list(map(lambda x: f'"{x}"' if ' ' in x else x, game.command()))
        self.Exe = f'"{command[0]}"'
        self.LaunchOptions = ' '.join(command[1:])