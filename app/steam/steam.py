import os, logging
from pathlib import Path
from typing import List

from .steam_user import SteamUser


STEAM_PATHS = [
    Path.home() / '.steam' / 'steam', 
    Path.home() / '.var' / 'app' / 'com.valvesoftware.Steam' / 'data' / 'Steam'
]

def list_users() -> List[SteamUser]:
    '''
        Returns a list of all user IDs
    '''

    users = []
    for steam_path in STEAM_PATHS:
        userdata_path = steam_path / 'userdata'
        if userdata_path.exists():
            for user_path in userdata_path.iterdir():
                user_id = user_path.stem
                if user_id.isdigit():
                    users.append(SteamUser(int(user_id), user_path))
    return users

def is_running() -> bool:
    '''
        Returns True if Steam is running
    '''

    for steam_path in STEAM_PATHS:
        path = steam_path.parent / 'steam.pid'
        if path.exists():
            # Read pid from file
            with path.open() as f:
                pid = int(f.read())
                try:
                    # Try to send signal 0 to a process. If successfull - process is running
                    os.kill(pid, 0)
                    return True
                except OSError:
                    pass
                    
    return False