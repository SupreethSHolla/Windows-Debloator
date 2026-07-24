import winreg


def open_key(root, path):
    try:
        return winreg.OpenKey(root, path, 0, winreg.KEY_READ)
    except Exception:
        return None


def enum_subkeys(key):
    index = 0
    subkeys = []
    while True:
        try:
            subkeys.append(winreg.EnumKey(key, index))
            index += 1
        except OSError:
            break
    return subkeys


def read_value(key, name):
    try:
        value, _ = winreg.QueryValueEx(key, name)
        return value
    except Exception:
        return None


def close_key(key):
    if key:
        try:
            key.Close()
        except OSError:
            pass
