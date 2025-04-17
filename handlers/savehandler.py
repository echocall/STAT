from helpers.crud import *
from helpers.utilities import *
import datetime
import traceback

def save_handler():
    print("TODO: Handle the saves of various games.")

def get_game_saves(filePath: str) -> list:
    unsplitSaves = []
    splitSaveNames = []
    unsplitSaves = multi_json_names_getter(filePath, "saves")
    for save in unsplitSaves:
        name = save.split(".")
        splitSaveNames.append(name[0].capitalize())

    return splitSaveNames

# return a dictionary of all the saves associated with a game
def get_saves(file_path: str) -> dict:
    save_names = []
    save_names = get_save_names(file_path)
    
    save_files = {}
    for save in save_names:
        save_name = save.lower()
        save_files[save_name] = load_save(save, file_path, "saves")
    
    return save_files

# for creating a new save from the gui
def new_save_gui(datapack_path: str, save_path: str,
                  new_save_dict: dict, save_name: str) -> dict:
    write_result = {'result':False,'string':'', 'dict':{}}
    folders_create = False
    error_message = ""
    file_name = ""
    name_dict = {"name":"","file":""}

    # convert save_name into file_name
    name_dict['file'] = convert_save_name(save_name)
    new_save_dict['name'] = name_dict['name']
        
    # Get the date of creation
    date_created = datetime.strptime(str(datetime.today('EDT')), '%\d-%m-%Y %H:%M:%S')
    new_save_dict['create_date'] = date_created
    # last save date
    last_save_date = date_created
    new_save_dict['date_last_saved'] = last_save_date

    # Create the folders for the customs.
    game_file = {}
    game_file = format_str_for_filename_super(new_save_dict['base_game'])
    
    if game_file['result']:
        customs_path = datapack_path + "\\customs\\" + game_file['string'] + "\\" + name_dict['file'] 
        # assembling the paths that need to be made
        asset_customs_path = customs_path + "\\assets"
        effect_customs_path = customs_path + "\\effects"
        events_customs_path = customs_path + "\\events"
    else:
        asset_customs_path = ""
        effect_customs_path = ""
        events_customs_path = ""
    new_save_dict['asset_customs_path'] = asset_customs_path
    new_save_dict['effect_customs_path'] = effect_customs_path
    new_save_dict['event_customs_path'] = events_customs_path
    folders_create = create_save_folders(name_dict, new_save_dict['base_game'], datapack_path, save_path)
    if not folders_create:
        # warn user via error message
        error_mesage = "Error: failed to create directories for new save."
        g = 2+7

    write_result['result'] = create_new_json_file(file_name, save_path, new_save_dict)
    
    # If we wrote the dict to the .JSON file
    if write_result['result'] == True:
        write_result['string'] = 'Successfully wrote save to file.'
        write_result['dict'] = new_save_dict
        return write_result
    else:
        write_result['string'] = "Warning, could not write new save to JSON file."
        return write_result

def get_save_names(filePath: str) -> list:
    save_names = []
    save_names = multi_json_names_getter(filePath, "saves")

    return save_names

def convert_save_name(saveName: str) -> str:
    formatted_name = ""
    try:
        formatted_name = saveName.strip()
        formatted_name = formatted_name.lower()
        formatted_name = formatted_name.replace(" ", "_")
    except Exception:
            tb = sys.exception().__traceback__
            print(tb)
    return formatted_name

def load_save(save_name: str, file_path: str, type: str) -> dict:
    save = single_json_getter(save_name, file_path, type)
    return save

def select_save(file_path: str) -> dict:
    saves = []
    target_save = ''
    target_dict = {}
    save_object = {}

    # load list of game names from games folder.
    saves = multi_json_names_getter(file_path, 'saves')

    # call List_to_Menu
    target_save = list_to_menu('Select a save: ', saves)

    # load in the game_dict
    target_dict = single_json_getter(target_save, file_path, 'saves')

    return target_dict

# TODO: Test
# Save a save dictionary to a JSON file
def update_save(save_dict: dict, save_path: str) -> dict:
    file_name = ""
    result = {}

    file_name = convert_save_name(save_dict['name'])
    result = overwrite_json_file(save_dict, save_path, file_name)

    return result

# TODO: Create a new save file
def new_save(save_name: str, game: dict):
    print("TODO: Create a new save file.")
    file_save_name = ""
    new_save_file = {'name': "", 'create_date': "", "date_last_save": "",
                     "description": "", "asset_customs": False, "asset_customs_path": "",
                     "actor_customs": False,"actor_customs_path": "",
                     "event_customs": False, "event_customs_path": "",
                     "effect_customs": False, "effect_customs_path": "",
                     "counters":{}, "assets":{}, "actors":{}, "current_events":{},
                     "current_effects":{},"current_turn":0, "log_file_path":""}
    # build the save dict

    # Convert save_name to file_name friendly format
    file_save_name = format_str_for_filename(save_name)

    # Get default values from the game.
    new_save_file['name'] = save_name;
    new_save_file['']

# TODO:
def save_current():
    print("TODO: save current STAT instance to save file.")
    # Call update save functions in MySave

# TODO
def save_as_new_file():
    print("TODO: Create a new save file.")

# create the folders for a new save.
def create_save_folders(name_dict: dict, game_name: str, datapack_path: str) -> bool:
    folder_created = False
    folders_created = {}
    result = False
    folders = []
    game_file = {}

    game_file = format_str_for_filename_super(game_name)
    
    if game_file['result']:
        customs_path = datapack_path + "\\customs\\" + game_file['string'] + "\\" + name_dict['file'] 
        # assembling the paths that need to be made
        asset_customs_path = customs_path + "\\assets"
        effect_customs_path = customs_path + "\\effects"
        events_customs_path = customs_path + "\\events"

        folders.append(asset_customs_path)
        folders.append(effect_customs_path)
        folders.append(events_customs_path)

        # For each filepath to a directory, create that directory
        for folder in folders:
            folder_created = create_new_directory(folder)['created']
            folders_created['folder']=folder_created

        if False not in folders_created:
            result = True
    else:
        b = 2+2
        # TODO: error handling for if this doesn't work.
    
    return result