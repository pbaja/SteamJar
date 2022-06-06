from pathlib import Path

BOTTLES_PATH = Path.home() / '.var' / 'app' / 'com.usebottles.bottles' / 'data' / 'bottles' / 'bottles'
BOTTLES_CLI_CMD = ['/usr/bin/flatpak', 'run', '--command=bottles-cli', 'com.usebottles.bottles']