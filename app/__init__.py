import logging, sys
from . import cli, gui
from .version import VERSION_STR

def run_app():
    '''
    Main entry point. Run this function to start the application.
    '''
    
    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    logging.info(f"Running SteamJar v{VERSION_STR}")

    # Run application
    run_cli = sys.stdin and sys.stdin.isatty() and '--gui' not in sys.argv
    if not run_cli:
        run_cli = not gui.run()
    if run_cli:
        cli.run()