import os


def get_folder_size_mb(path):
    if not path or not os.path.exists(path):
        return None

    total = 0
    try:
        for root, _, files in os.walk(path):
            for file in files:
                try:
                    total += os.path.getsize(os.path.join(root, file))
                except OSError:
                    pass
        return round(total / (1024 * 1024), 2)
    except Exception:
        return None
