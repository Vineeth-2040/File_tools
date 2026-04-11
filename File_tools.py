import os 
from AS_list import get_directory_info


def search_filesystem(root, query=None, ext=None, max_depth=3, file_type=None):
    
    # check permission first
    if not os.access(root, os.R_OK):
        return {"found": False, "permission": "denied", "count": 0, "items": []}
    
    result = get_directory_info(root, max_depth)

    if file_type:
        result = [f for f in result if f["type"] == file_type]
    if ext:
        result = [f for f in result if f["ext"] == ext]
    if query:
        result = [f for f in result if query.lower() in f["name"].lower()]

    if not result:
        return {"found": False, "permission": "granted", "count": 0, "items": []}
    
    return {"found": True, "permission": "granted", "count": len(result), "items": result}


    


