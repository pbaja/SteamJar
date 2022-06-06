from typing import Union

REGISTRY_PATH_DELIMITER = '\\\\'
REGISTRY_QUOTE_SIGN = '"'

class RegistryKey:
    '''
    Registry key containing content (key&value pairs) and child keys
    '''

    def __init__(self):
        self.children = {}
        self.content = {}

    def update(self, key, content) -> None:
        
        # Create or travel through keys
        current = self
        for part in key.split(REGISTRY_PATH_DELIMITER):
            if part not in current.children:
                current.children[part] = RegistryKey()
            current = current.children[part]

        # Add content
        for k, v in content:
            k = k.strip().strip(REGISTRY_QUOTE_SIGN)
            v = v.strip().strip(REGISTRY_QUOTE_SIGN)
            current.content[k] = v

    def __getitem__(self, key) -> Union['RegistryKey', None]:
        return self.children.get(key, self.content.get(key, None))

    def __repr__(self):
        return f'Content: {self.content}, Children: {self.children}'

def registry_get_key(path: 'Path', key: str) -> Union['RegistryKey', None]:
    '''
    Returns RegistryKey instance at a given path. None if does not exist.
    Path must point to an existing .reg file.
    '''

    with path.open('r') as file:

        # Ignore first line
        file.readline()

        # Prepare key
        key = key.lower().replace('/', '\\').replace('\\', '\\\\')
        data = RegistryKey()

        # Iterate over lines in file
        section = None
        content = []
        for line in file:
            
            # Ignore comments or empty lines
            if line[0] == ';' or line[0] == '#' or len(line.strip()) == 0:
                continue

            # New section
            elif line[0] == '[':
                # Parse previous section
                if section is not None:
                    data.update(section, content)
                    content.clear()
                    section = None
                    
                # New section. Discard if does not start with key
                r = line.rindex(']')
                section = line[1:r].lower()
                if not section.startswith(key):
                    section = None
            
            # New value. Ignore if we are not in section.
            elif len(line) > 0 and section is not None:
                k, v = line.split('=', 1)
                while v.strip()[-1] == '\\':
                    l = file.readline().strip()
                    v += l
                    
                content.append((k, v))
        
        # Finished
        unpacked = data
        for part in key.split('\\\\'):
            unpacked = unpacked[part]
            if unpacked is None:
                break
        return unpacked