import random, re
from dataclasses import dataclass, asdict, field
from ..games.game import Game

@dataclass
class Shortcut:
    appid: int
    appname: str
    exe: str = ''
    start_dir: str = ''
    icon: str = ''
    shortcut_path: str = ''
    launch_options: str = ''
    is_hidden: int = 0
    allow_desktop_config: int = 1
    allow_overlay: int = 1
    openvr: int = 0
    devkit: int = 0
    devkit_game_id: str = 0
    devkit_override_app_id: int = 0
    last_play_time: int = 0   # Unix timestamp when last launched. Never if 0.
    flatpak_app_id: str = ''
    tags: dict = field(default_factory = lambda: ({}))

    def to_dict(self) -> None:
        return asdict(self)

    def from_dict(data: dict) -> 'Shortcut':
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        snake_data = {pattern.sub('_', k).lower().replace('i_d', 'id'): v for k, v in data.items()}
        return Shortcut(**snake_data)

    def from_game(game: Game) -> 'Shortcut':
        shortcut = Shortcut(appid = random.randint(0xB0000000, 0xFFFFFFFF), appname = game.name)
        shortcut.update_from_game(game)
        return shortcut

    def update_from_game(self, game: Game):
        command = list(map(lambda x: f'"{x}"' if ' ' in x else x, game.command()))
        self.Exe = f'"{command[0]}"'
        self.LaunchOptions = ' '.join(command[1:])