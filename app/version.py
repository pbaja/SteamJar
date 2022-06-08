import sys, re
from pathlib import Path

version_path = Path(sys.argv[0]).parent / 'version.txt'
with version_path.open('r') as f:
    VERSION_STR = f.read()
    VERSION = tuple(map(lambda x: int(re.sub('\D', '', x)), VERSION_STR.split('.')))