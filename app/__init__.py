import logging, sys
from . import cli, gui
from .version import VERSION_STR

class RunMode:
    NONE = 0
    GUI = 1
    CLI = 2

def run_app():
    '''
    Main entry point. Run this function to start the application.
    '''
    
    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    logging.info(f"Running SteamJar v{VERSION_STR}")

    # Select run mode
    mode = RunMode.GUI
    if '--cli' in sys.argv: mode = RunMode.CLI
    if '--gui' in sys.argv: mode = RunMode.GUI
    
    # Run in GUI mode
    if mode == RunMode.GUI:
        result = gui.run()
        mode = RunMode.NONE if result else RunMode.CLI

    # Run in CLI mode
    if mode == RunMode.CLI:
        cli.run()