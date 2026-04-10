import os
import shutil

def get_directory_info(folder_path,max_depth=3):
    current_positon=0
    result=[]
    if os.path.exists(folder_path):
        files=os.listdir(folder_path)
        for file in files:
            full_path=os.path.join(folder_path,file)
            if os.path.isdir(full_path):
                size=format_size(os.path.getsize(full_path))
                created_time=os.path.getctime(full_path)
                modified_time=os.path.getmtime(full_path)
                result.append({"type":"dir","name":file,"size":size,"created_time":created_time,"modified_time":modified_time})

                if max_depth-1> current_positon :
                    current_positon+=1
                    get_directory_info(full_path,max_depth)

            else:
                size=format_size(os.path.getsize(full_path))
                created_time=os.path.getctime(full_path)
                modified_time=os.path.getmtime(full_path)
                result.append({"type":"file","name":file,"size":size,"created_time":created_time,"modified_time":modified_time})



    else : 
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