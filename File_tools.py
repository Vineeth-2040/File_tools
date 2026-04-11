import os 
from AS_list import get_directory_info
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



def exact_keyword_search(path, keyword, context_lines=2):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except PermissionError:
        return {"found": False, "reason": "permission denied"}
    except UnicodeDecodeError:
        return {"found": False, "reason": "not a text file"}

    matches = []

    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)

            snippet = []
            for j in range(start, end):
                snippet.append({
                    "line": j + 1,
                    "content": lines[j].rstrip()
                })

            matches.append({
                "matched_line": i + 1,
                "snippet": snippet
            })

    if not matches:
        return {"found": False, "reason": "keyword not found"}

    return {
        "found": True,
        "match_count": len(matches),
        "matches": matches
    }



def context_search(path, query, context_lines=2, threshold=0.5):

    STOP_WORDS = {
        "where", "did", "i", "write", "the", "a", "an", "is", "it",
        "in", "on", "at", "to", "for", "of", "and", "or", "my",
        "what", "how", "when", "was", "used", "use", "can", "you",
        "tell", "me", "find", "show", "get", "do", "this", "that"
    }

    # step 1 — tokenize query, remove stop words
    words = query.lower().split()
    keywords = [w for w in words if w not in STOP_WORDS]

    if not keywords:
        return {"found": False, "reason": "no meaningful keywords in query"}

    # step 2 — open file
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except PermissionError:
        return {"found": False, "reason": "permission denied"}
    except UnicodeDecodeError:
        return {"found": False, "reason": "not a text file"}

    # step 3 — score each line
    matches = []

    for i, line in enumerate(lines):
        line_lower = line.lower()
        line_words = line_lower.split()
        matched_words = [w for w in keywords if w in line_words]
        score = len(matched_words) / len(keywords)

        if score >= threshold:
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)

            snippet = []
            for j in range(start, end):
                snippet.append({
                    "line": j + 1,
                    "content": lines[j].rstrip()
                })

            matches.append({
                "matched_line": i + 1,
                "score": round(score, 2),
                "matched_words": matched_words,
                "snippet": snippet
            })

    if not matches:
        return {"found": False, "reason": "no lines met threshold", "keywords_searched": keywords}

    # step 4 — sort by score, best match first
    matches.sort(key=lambda x: x["score"], reverse=True)

    return {
        "found": True,
        "match_count": len(matches),
        "keywords_searched": keywords,
        "matches": matches
    }