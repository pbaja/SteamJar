import sys, re, urllib.request, logging
from pathlib import Path

def latest_version():
    url = 'https://raw.githubusercontent.com/pbaja/SteamJar/main/version.txt'
    with urllib.request.urlopen(url) as response:
        version_str = response.read().decode('utf-8')
        version = tuple(map(lambda x: int(re.sub('\D', '', x)), version_str.split('.')))
        return (version_str, version)

def current_version():
    version_path = Path(sys.argv[0]).parent / 'version.txt'
    with version_path.open('r') as f:
        version_str = f.read()
        version = tuple(map(lambda x: int(re.sub('\D', '', x)), version_str.split('.')))
        return (version_str, version)

VERSION_STR, VERSION = current_version()