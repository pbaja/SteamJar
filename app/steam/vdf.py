import logging, json

SECTION_HEADER = b'\0shortcuts\0'
NUL = b'\x00' # Set Start, Key End, Key+Value Delimiter
STX = b'\x02' # Int
SOH = b'\x01' # String
BS = b'\x08'  # Set End
DEBUG = False

def read_string(file, until):
    result = b''
    while True:
        char = file.read(1)
        if char == until:
            break
        result += char
    return result.decode()

def read_int(file):
    return int.from_bytes(file.read(4), byteorder='little')

def load(path):
    with path.open("rb") as file:

        # Read tokens
        stack = [{}]
        while True:
            char = file.read(1)

            # Beginning of a set
            if char == NUL:
                set_id = read_string(file, NUL)
                stack.append({"__id__": set_id})
            # End of set
            elif char == BS:
                if len(stack) > 1:
                    last = stack.pop()
                    last_id = last["__id__"]
                    del last["__id__"]
                    stack[-1].update({last_id: last})
            # String value
            elif char == SOH:
                key = read_string(file, NUL)
                value = read_string(file, NUL)
                stack[-1].update({key: value})
            # Integer value (4 bytes)
            elif char == STX:
                key = read_string(file, NUL)
                value = read_int(file)
                stack[-1].update({key: value})
            # End of file
            elif char == b'':
                break
            else:
                logging.error(f"Encountered unknown type char: {char}")

        # Result
        return stack.pop()

def write_set(file, set_id, data, indent=0):

    # Write set header
    file.write(NUL)
    file.write(set_id.encode())
    file.write(NUL)

    # Write set content
    for key, value in data.items():
        # Write set
        if isinstance(value, dict):
            write_set(file, key, value, indent+1)
        # Write key+value
        else:
            # Write string
            if isinstance(value, str):
                file.write(SOH)
                file.write(key.encode())
                file.write(NUL)
                file.write(value.encode())
                file.write(NUL)
            # Write int
            elif isinstance(value, int):
                file.write(STX)
                file.write(key.encode())
                file.write(NUL)
                file.write(value.to_bytes(4, byteorder='little'))
            # Unsupported type
            else:
                logging.error(f"Encountered unsupported type: ({type(value)}) {value}")
    
    # Write set footer
    file.write(BS)

    # This is weird and undocumented. Maybe Steam adds additional BS on root key?
    #TODO: Find out why
    if indent == 0:
        file.write(BS)

def save(path, data):
    with path.open("wb") as file:
        for set_id, set_data in data.items():
            write_set(file, set_id, set_data)