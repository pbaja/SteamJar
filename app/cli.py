import logging, json, pprint
from .entry import Entry
from .steam import steam
from .steam.shortcut import Shortcut
from .games.containers import list_containers

def run():
    '''
    Starts the command line interface
    '''

    # Check if steam is running
    if steam.is_running():
        logging.warn("Steam is running. Please close it before saving the modified shortcuts.")

    # Get a list of game containers
    containers = list_containers()
    logging.info(f'Found {len(containers)} game containers')
    
    # Get a list of games in all game containers
    games = []
    for container in containers:
        games += container.list_games()
    logging.info(f'Found {len(games)} games in that containers')
    
    # Select user
    users = steam.list_users()
    user = None
    if len(users) == 1:
        user = users[0]
    elif len(users) == 0:
        logging.info('No steam users found! Aborting.')
        return None
    else:
        logging.info("Multiple users. Select user:")
        for idx, user in enumerate(users):
            logging.info(f" - {idx}: {user.name}")
        answer = input("Answer (0, 1, 2...): ")
        if len(answer) == 0:
            user = users[0]
        else:
            user = users[int(answer)]
    logging.info(f'Selected user: {user.name}')

    # Load user shortcuts
    shortcuts = user.load_shortcuts()
    logging.info(f'Loaded {len(shortcuts)} shortcuts from Steam')

    # Create entries from games
    entries = []
    for game in games:
        # Search for existing shortcut by game name
        for shortcut in shortcuts:
            if shortcut.appname == game.name:
                shortcut.update_from_game(game)
                entries.append(Entry(user, shortcut, game=game, enabled=True))
                break
        # Create new shortcut from game
        else:
            entries.append(Entry(user, Shortcut.from_game(game), game=game, enabled=True))
    
    # Add entries for shortcuts not already added
    for shortcut in shortcuts:
        if shortcut not in map(lambda e: e.shortcut, entries):
            entries.append(Entry(user, shortcut, game=None, enabled=True))

    # Wait for steam to close
    while steam.is_running():
        logging.info("Steam is running. Please close it to save shortcuts.")
        answer = input("Press Enter to retry or type `quit` to abort...").lower()
        if answer == 'force':
            logging.warn('Ignoring running steam. This is not recommended!')
            break
        elif answer == 'quit' or 'q':
            return
    
    # Print the shortcuts
    logging.info('Resulting shortcuts:')
    for entry in entries:
        shortcut = entry.shortcut
        exe = '...' if len(shortcut.Exe) > 16 else ''
        exe += shortcut.Exe[-16:].strip('"')
        opts = '...' if len(shortcut.LaunchOptions) > 16 else ''
        opts += shortcut.LaunchOptions[-16:].strip('"')
        logging.info(f' - Enabled: {entry.enabled}, Name: {shortcut.appname}, Exe: {exe}, LaunchOptions: {opts}"')

    # Select if save the shortcuts
    logging.info("Save new shortcuts?")
    response = input("Answer (Yes/no): ")
    if len(response) == 0 or response.lower() == 'y':
        user.save_shortcuts(map(lambda e: e.shortcut, entries))
        logging.info("Shortcuts saved")
    else:
        logging.info("Not saving shortcuts")
    