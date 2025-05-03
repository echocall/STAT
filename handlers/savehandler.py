from helpers.crud import *
from helpers.utilities import *
from datetime import datetime
import traceback

def save_handler():
    print("TODO: Handle the saves of various games.")

# return a dictionary of all the saves associated with a game
def get_saves(saves_path: str) -> dict:
    save_names = []
    save_names = get_save_names(saves_path)
    full_save_path = ''
    
    save_files = {}
    for save in save_names:
        save_name = save.lower()
        full_save_path = saves_path + '\\' + save_name + '\\' + save_name + ".json"
        save_files[save_name] = load_save(save, full_save_path,)
    
    return save_files

# for creating a new save from the gui
def new_save_gui(datapack_path: str, save_path: str,
                  new_save_dict: dict, file_name: str) -> dict:
    write_result = {'result':False,'string':'', 'dict':{}}
    folders_create = False
    error_message = ""

    # Get the date of creation
    date_created = datetime.now().strftime('%b-%d-%Y %H:%M:%S')
    new_save_dict['create_date'] = date_created
    # last save date
    last_save_date = date_created
    new_save_dict['date_last_save'] = last_save_date

    # Create the folders for the customs.
    game_file = {}
    game_file = format_str_for_filename_super(new_save_dict['base_game'])
    
    if game_file['result']:
        customs_path = datapack_path + game_file['string'] + "\\customs\\"  + file_name + "\\"
        # assembling the paths that need to be made
        actor_customs_path = customs_path + "actors\\"
        asset_customs_path = customs_path + "assets\\"
        effect_customs_path = customs_path + "effects\\"
        events_customs_path = customs_path + "events\\"
    else:
        actor_customs_path = ""
        asset_customs_path = ""
        effect_customs_path = ""
        events_customs_path = ""
    new_save_dict['actor_customs_path'] = actor_customs_path
    new_save_dict['asset_customs_path'] = asset_customs_path
    new_save_dict['effect_customs_path'] = effect_customs_path
    new_save_dict['event_customs_path'] = events_customs_path
    new_save_dict['log_file_path'] = save_path + "\\" + game_file['string'] + "\\"
    
    folders_create = create_save_folders(file_name, new_save_dict['base_game'], datapack_path)
    if not folders_create:
        # warn user via error message
        error_mesage = "Error: failed to create directories for new save."
        g = 2+7

    save_path_full = save_path + '\\' + game_file['string'] + '\\' + file_name

    # create the folder where the save goes
    save_folder_blns = create_new_directory(save_path_full)

    write_result['result'] = create_new_json_file(file_name, save_path_full, new_save_dict)
    
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

def load_save(full_save_path: str) -> dict:
    load_save_result = {}
    load_save_result = single_json_getter_fullpath(full_save_path, 'save')
    if load_save_result['result']:
        save = load_save_result
        return save
    else:
        print("Error with returning save!")
        return {}

def check_template_bool(save: dict, template_path: str) -> bool:
    error_message = ''
    result = False
    try:
        save_template = get_template_json("save", template_path)
        result = dict_key_compare(save_template, save)
        return result
    except Exception:
        print(traceback.format_exc())
        return result

def get_new_save_name(name: str, file_path: str) -> dict:
    file_name = ""
    saves = []
    save_name = {"name": "", "file":""}
    valid = False

    while not valid:
        file_name = format_str_for_filename(name)

        # check that a game by that name doesn't already exists
        saves = multi_json_names_getter(file_path, "saves")
        
        if name in saves:
    # if file_name already exists, append placeholder and alert user
            valid = True
            save_name["name"] = name + "_Placeholder"
            save_name["file"] = file_name + "_placeholder"
        else:
            valid = True
            save_name["name"] = name
            save_name["file"] = file_name

    return  save_name

# TODO: Test
# Save a save dictionary to a JSON file
def update_save(save_dict: dict, save_path: str, template_path: str) -> dict:
    template_result = {}
    format_result = {}
    write_result = {}
    # check the template is okay
    try:
        template_result['result'] = check_template_bool(save_path, template_path)
    except:
        template_result['result'] = False
        template_result['message'] = 'Given object did not match save template.'
  
    # it matches the template!
    if template_result['result']:
        # try formatting the save name for a file
        try:
            format_result = format_str_for_filename_super(save_path['name'])
        except:
            format_result['message'] = 'Formatting name for save update failed.'

        # it formatted the name!
        if format_result['result']:
            # try writing to the json_file
            try:
                write_result = overwrite_json_file(save_dict, save_path, format_result['string'])
            except:
                write_result['success'] = False
                write_result['message'] = 'Overwriting to save json failed.'
            # successfully wrote!
            if write_result['success']:
                return write_result
            # did not successfully write
            else:
                return write_result
        # did not formate name
        else:
            return format_result
    # did not get a match on the template
    else:
        return template_result


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
def create_save_folders(file_name: str, game_name: str, datapack_path: str) -> bool:
    folder_created = False
    folders_created = {}
    result = False
    folders = []
    game_file = {}

    game_file = format_str_for_filename_super(game_name)
    
    if game_file['result']:
        customs_path = datapack_path+ "\\"+ game_file['string']  + "\\customs\\" + file_name + '\\'
        # assembling the paths that need to be made
        actors_customs_path = customs_path + "actors\\"
        asset_customs_path = customs_path + "assets\\"
        effect_customs_path = customs_path + "effects\\"
        events_customs_path = customs_path + "events\\"

        folders.append(actors_customs_path)
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

# TODO: implement
# delete a save
def delete_save(save_name: str, saves_path: str) -> bool:
    bln_result = False
    # Ensure custom assets fields are empty (whether due to deletion or moving)
    # delete save folders by calling: shutil.rmtree('/path/to/folder')

    return bln_result
