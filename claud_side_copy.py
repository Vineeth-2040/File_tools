import os
import shutil

def format_size(bytes):
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024 ** 2:
        return f"{bytes / 1024:.1f} KB"
    elif bytes < 1024 ** 3:
        return f"{bytes / 1024**2:.1f} MB"
    else:
        return f"{bytes / 1024**3:.1f} GB"

def get_directory_tree(root_path, max_depth=2, indent=0):
    tree = ""
    if indent == 0:
        tree += f"{root_path}\n"

    try:
        entries = sorted(os.listdir(root_path))
    except PermissionError:
        return tree + "  " * indent + "[Permission Denied]\n"

    for entry in entries:
        full_path = os.path.join(root_path, entry)
        prefix = "  " * indent

        if os.path.isdir(full_path):
            tree += f"{prefix}[DIR] {entry}/\n"
            if indent < max_depth - 1:
                tree += get_directory_tree(full_path, max_depth, indent + 1)
        else:
            size_str = format_size(os.path.getsize(full_path))
            tree += f"{prefix}[FILE] {entry} [{size_str}]\n"

    return tree

def move_file(src, dst):
    shutil.move(src, dst)
    print(f"Moved: {src} → {dst}")