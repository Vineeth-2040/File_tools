# we are testing the functions in File_tools here.
from File_tools import search_filesystem, get_directory_info, exact_keyword_search, context_search
# testing 
path=r"E:\Fun_with_python\file_searcher\File_acessor.py"
result=context_search(path,"for file in files:",context_lines=1,threshold=0.3)
print(result)