import gi, threading, logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .interface import messagebox
from .interface.window import Window
from .interface.select_option_dialog import SelectOptionDialog
from .entry import Entry
from .steam import steam
from .steam.shortcut import Shortcut
from .games.containers import list_containers
from . import utils

window = None
user = None
entries = []

def run() -> bool:
    '''
    Starts the graphical user interface
    '''
    if Gtk.init_check()[0] == False:
        logging.warn('Failed to run GUI. Falling back to CLI.')
        return False

    # Create window
    global window
    window = Window()
    window.view.on_reload_clicked(reload_games)
    window.view.on_enable_all_clicked(enable_all)
    window.view.on_download_clicked(download_images)
    window.view.on_save_clicked(save_shortcuts)
    window.show_all()

    # Initialize and enter endless loop
    if select_user(): 
        reload_games(False)
        Gtk.main()
    return True

def select_user():
    global user

    users = steam.list_users()

    if len(users) > 1:
        # Open dialog
        dialog = SelectOptionDialog(window, users, "Select user", "Multiple users found. Select user:", lambda u: u.name)
        dialog.show_all()
        dialog.run()

        # Get selection
        user = dialog.get_selected_value()
        logging.info(f'Selected user: {user.name}')
        dialog.destroy()
        return True

    elif len(users) == 1:
        user = users[0]
        logging.info(f'Auto selected user: {user.name}')
        return True

    else:
        logging.error('No Steam users found! Aborting.')
        return False

def reload_games(show_info=True):
    logging.info('Reloading game list...')

    # Get a list of game containers
    containers = list_containers()
    containers_len = len(containers)
    logging.info(f'Found {containers_len} game container{utils.suff(containers_len)}')

    # Get a list of games in all game containers
    games = []
    for container in containers:
        games += container.list_games()
    games_len = len(games)
    logging.info(f'Found {games_len} game{utils.suff(games_len)} in that container{utils.suff(containers_len)}')

    # Load user shortcuts
    shortcuts = user.load_shortcuts()
    logging.info(f'Loaded {len(shortcuts)} shortcuts from Steam')

    # Create entries
    global entries
    for shortcut in shortcuts:
        if shortcut.app_name not in map(lambda e: e.shortcut.app_name, entries):
            entries.append(Entry(user, shortcut, game=None, enabled=True))
            logging.debug(f'Added shortcut {shortcut.app_name}')

    # Create or update entries from games
    for game in games:
        # Search for existing shortcut by game name
        for entry in entries:
            if entry.shortcut.app_name == game.name:
                entry.game = game
                entry.shortcut.update_from_game(game)
                logging.debug(f'Updated game {game.name}')
                break
        # Create a new shortcut from game. Disabled by default.
        else:
            entries.append(Entry(user, Shortcut.from_game(game), game=game, enabled=False))
            logging.debug(f'Added game {game.name}')

    # Reload entries in window
    global window
    window.view.clear_entries()
    window.view.add_entries(entries)

    # Display information
    if show_info:
        messagebox.info(f'Found {games_len} game{suff(games_len)} in {containers_len} container{suff(containers_len)}', parent=window)

def enable_all():
    global entries
    for entry in entries:
        entry.set_enabled(True)

def download_images():
    global entries
    skipped = 0
    downloaded = 0

    for entry in entries:

        # Skip if entry is not enabled
        if not entry.enabled:
            skipped += 1
            continue

        # Download images if missing
        if entry.images.any_missing():

            # Search for game
            results = entry.images.search_game()
            game_id = -1

            # Select game
            if len(results) == 0:
                logging.info(f"No results for {entry.shortcut.app_name}")
                continue
            elif len(results) == 1:
                game_id = results[0].id
            else:
                # Open dialog
                dialog = SelectOptionDialog(window, results, "Select game", "Multiple games found. Select game:", lambda x: x.name)
                dialog.show_all()
                if dialog.run() != Gtk.ResponseType.OK:
                    dialog.destroy()
                    continue

                # Get selection
                game_id = dialog.get_selected_value().id
                dialog.destroy()
                utils.flush_gtk()
            
            # Download images
            entry.images.download_missing(game_id)
            downloaded += 1
    
    messagebox.info(f'Downloaded {downloaded} images, {skipped} skipped.', parent=window)

def save_shortcuts():

    if steam.is_running():
        messagebox.info('Steam is running. Please close it before saving shortcuts.', parent=window)
        return None

    global entries
    user.save_shortcuts(map(lambda e: e.shortcut, filter(lambda x: x.enabled, entries)))
    logging.info('Shortcuts saved')
    messagebox.info('Shortcuts saved', parent=window)

    
    
