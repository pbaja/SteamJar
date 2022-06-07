import random
from ..games.game import Game

DEFAULTS = {
    'appid': 0,
    'appname': '',
    'Exe': '',
    'StartDir': '',
    'icon': '',
    'ShortcutPath': '',
    'LaunchOptions': '',
    'IsHidden': 0,
    'AllowDesktopConfig': 0,
    'AllowOverlay': 0,
    'openvr': 0,
    'Devkit': 0,
    'DevkitGameID': '',
    'DevkitOverrideAppID': 0,
    'LastPlayTime': 0,
    'FlatpakAppID': '',
    'tags': {}
}

class Shortcut:

    def __init__(self, data: dict):
        self._data = data

    def to_dict(self):

        #TODO: Is this neccesary?
        if 'exe' in self._data:
            self._data['exe'] = self._data['Exe']
            del self._data['Exe']

        return DEFAULTS | self._data

    def from_game(game: Game) -> 'Shortcut':
        shortcut = Shortcut({})
        shortcut.app_id = random.randint(0xB0000000, 0xFFFFFFFF)
        shortcut.app_name = game.name
        shortcut.update_from_game(game)
        return shortcut

    def update_from_game(self, game: Game):
        command = list(map(lambda x: f'"{x}"' if ' ' in x else x, game.command()))
        self.executable = f'"{command[0]}"'
        self.launch_options = ' '.join(command[1:])

    @property
    def app_id(self):
        return self._data.get('appid', DEFAULTS['appid'])

    @app_id.setter
    def app_id(self, value):
        self._data['appid'] = value
    
    @property
    def app_name(self):
        return self._data.get('appname', DEFAULTS['appname'])
    
    @app_name.setter
    def app_name(self, value):
        self._data['appname'] = value

    @property
    def executable(self):
        return self._data.get('Exe', DEFAULTS['Exe'])

    @executable.setter
    def executable(self, value):
        self._data['Exe'] = value

    @property
    def launch_options(self):
        return self._data.get('LaunchOptions', DEFAULTS['LaunchOptions'])

    @launch_options.setter
    def launch_options(self, value):
        self._data['LaunchOptions'] = value