import os

def read_file(file_path):
    try:
        return os.listdir(file_path)
    
    except Exception as e:
        print("Error:", e)
        return []

path = r"D:\SteamLibrary"
files = read_file(path)

for file in files:
    fullpath = os.path.join(path, file)
    if os.path.isfile(fullpath):
        print("|-",file)
    elif os.path.isdir(fullpath):
        print("|-",file)
        inner_file=read_file(fullpath)
        for ifile in inner_file:
            print("  ","|-",ifile)
