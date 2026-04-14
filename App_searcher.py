import os 
import shutil
from File_tools import search_filesystem



# claude
def get_installed_apps():

    apps = {}  # name -> full path
    
    # --- Part 1: Scan PATH folders ---
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    
    for folder in path_dirs:
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                if file.endswith(".exe"):
                    name = file.replace(".exe", "")
                    full_path = os.path.join(folder, file)
                    apps[name] = full_path

    # --- Part 2: Full disk scan for .exe files ---
    # your existing function already does this
    exe_files = scan_disk_by_extension(".exe")  # <-- your existing function
    
    for full_path in exe_files:
        name = os.path.basename(full_path).replace(".exe", "")
        if name not in apps:  # PATH results take priority
            apps[name] = full_path

    return apps  # { "code": "C:/...Code.exe", "figma": "C:/...Figma.exe" }



# 
def scan_apps():