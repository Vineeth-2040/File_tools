import os
from datetime import datetime

def get_directory_info(folder_path,max_depth=1,current_positon=0):
    result=[]
    try :
        files=os.listdir(folder_path)
    except PermissionError:
        return result
    except FileNotFoundError:
        return result
            
    for file in files:
        full_path=os.path.join(folder_path,file)
        created_time = datetime.fromtimestamp(os.path.getctime(full_path)).strftime("%Y-%m-%d %H:%M:%S")
        modified_time = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M:%S")

        if os.path.isdir(full_path):
            result.append({"type":"dir","path":full_path+"/","name":file,"ext":None,"size":None,"created_time":created_time,"modified_time":modified_time})

            if current_positon < max_depth-1 :
                result.extend(get_directory_info(full_path,max_depth,current_positon+1))

        else:
            size=format_size(os.path.getsize(full_path))
            ext=os.path.splitext(file)[1].lower()
            result.append({"type":"file","path":full_path,"name":file,"ext":ext,"size":size,"created_time":created_time,"modified_time":modified_time,})
    return result


def format_size(bytes):
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024 ** 2:
        return f"{bytes / 1024:.1f} KB"
    elif bytes < 1024 ** 3:
        return f"{bytes / 1024**2:.1f} MB"
    else:
        return f"{bytes / 1024**3:.1f} GB"
    


# Testing
path= r"E:"
result=get_directory_info(path,3,2)
for item in result:
    print(f"{item['type'].upper()}: {item['name']} - Size: {item['size']} - Created: {item['created_time']} - Modified: {item['modified_time']}")
