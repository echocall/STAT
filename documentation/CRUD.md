#Overview 
CRUD.py handles the operations that touch the files themselves.

##Imports
json
pathlib -> Path
helper.utilities
traceback
os
shutil
datetime
nicegui -> app

###Create New JSON File
create_new_json_file(full_file_path: str, dict_to_convert: dict, include_debug: bool = False) -> dict
Overview: Handles writing the converted dict into JSON and then writing it into the file. Should write errors to log file.

####Arguments
 - takes full_file_path
 - takes dict_to_convert (to JSON)
 - optionally takes a boolean (include_debut)
 - Returns a dictionary

####Return 
result_dict {'result': bool, 'message': string, 'path': string of file path, 'debug': string of exception}

###Dependencies
Path : library -> handles formatting strings into windows format
convert_obj_to_json : utilities.py -> handles converting the dict into a json object.

###References
3 references
assethandler.py -> new_asset_gui
gamehandler.py -> new_game_gui
savehandler.py -> new_save_gui

###Create New Directory
create_new_directory(passed_directory_path: str, debug_mode: bool = False) -> dict
Overview: Handles creating a folder at the given directory path.

####Arguments
- passed_directory_path, required, full dictionary path as string
- debug_mode, optional, boolean

####Return
{'result':bool, 'message': string, 'debug': string of exception}

####Dependences
Path : library -> handles trying to write to the folder
Traceback: library -> for error tracking.

####References
3 references
gamehandler.py -> new_game_gui
gamehandler.py -> create_folders (defunct)
savehandler.py -> new_save_gui

