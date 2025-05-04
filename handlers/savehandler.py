from helpers.crud import *
from helpers.utilities import *
from datetime import datetime
import traceback

def save_handler():
    print("TODO: Handle the saves of various games.")

# return a dictionary of all the saves associated with a game
def get_saves(saves_directory_path: str) -> dict:
    save_names = []
    save_names = get_save_names(saves_directory_path)
    full_save_path = ''
    
    save_files = {}
    for save in save_names:
        save_name = save.lower()
        full_save_path = saves_directory_path + '\\' + save_name + '\\' + save_name + ".json"
        save_files[save_name] = single_json_getter_fullpath(full_save_path, 'save')
    
    return save_files

# for creating a new save from the gui
def new_save_gui( save_directory_path: str,
                  new_save_dict: dict, file_name: str) -> dict:
    write_result = {'result': False, 'string': '', 'dict': {}, 'debug': []}

    try:
        save_base_path = save_directory_path + '\\' + new_save_dict['name']

        # Get the date of creation
        date_created = datetime.now().strftime('%b-%d-%Y %H:%M:%S')
        new_save_dict['create_date'] = date_created
        # last save date
        last_save_date = date_created
        new_save_dict['date_last_save'] = last_save_date

        write_result = create_new_json_file(save_base_path, new_save_dict)
        debug_log_path = save_directory_path / f"{file_name}_debug.log"
        
        # If we wrote the dict to the .JSON file
        if write_result['result'] == True:
            write_result['string'] = 'Successfully wrote save to file.'
            write_result['dict'] = new_save_dict
            return write_result
        else:
            write_result['string'] = "Warning, could not write new save to JSON file."

    except Exception:
            error_info = traceback.format_exc()
            write_result['string'] = "Unhandled exception occurred."
            write_result['debug'].append({'exception': error_info})

    # Save debug info to log file
    try:
        debug_text = json.dumps(write_result['debug'], indent=2)
        debug_log_path.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists
        with open(debug_log_path, 'w') as log_file:
            log_file.write(debug_text)
    except Exception as log_exception:
        write_result['debug'].append({'log_error': str(log_exception)})

    return write_result

def get_save_names(directory_path: str) -> list:
    save_names = []
    save_names_result = multi_file_names_getter(directory_path, "saves")
    if save_names_result['result']:
        save_names = save_names_result['list']
    else:
        print("Error! Problem with fetching save names.")
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

# return a result dictionary from getting a single json file
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

def get_new_save_name(directory_path: str, name: str, ) -> dict:
    file_name = ""
    saves = []
    save_name = {"name": "", "file":""}
    valid = False

    while not valid:
        file_name = format_str_for_filename(name)

        # check that a game by that name doesn't already exists
        saves_result = multi_file_names_getter(directory_path, "saves")
        
        if saves_result['result']:
            saves = saves_result['list']
        else:
            print("Error! Could not get the file saves name.")
        
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

# TODO:
def save_current(old_save: dict, new_save: dict):
    print("TODO: save current STAT instance to save file.")
    # Call update save functions in MySave

# TODO
def save_as_new_file():
    print("TODO: Create a new save file.")


# TODO: implement
# delete a save
def delete_save(save_name: str, saves_path: str) -> bool:
    bln_result = False
    # Ensure custom assets fields are empty (whether due to deletion or moving)
    # delete save folders by calling: shutil.rmtree('/path/to/folder')

    return bln_result
