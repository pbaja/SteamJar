import logging
from dataclasses import dataclass, field
from .steam.shortcut import Shortcut
from .games.game import Game
from .images.entry_images import EntryImages
from .event import Event
from .steam.steam_user import SteamUser

class Entry:

    def __init__(self, user: SteamUser, shortcut: Shortcut, game: Game = None, enabled: bool = True):
        self.enabled = enabled
        self.game = game
        self.shortcut = shortcut

        self.images = EntryImages(self, user)
        self.enabled_event = Event()

    def set_enabled(self, enabled):
        if self.enabled != enabled:
            self.enabled_event.invoke(enabled)
            self.enabled = enabled