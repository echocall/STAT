import traceback
from pathlib import Path, PurePath

print("in app.py")

print('===============================')
passedDirectoryPath = "C:/Users/strip/Documents/github/STAT/statassets/games"
objectType = 'game'
error_message = ""
unsplit_objects = []
object_names = []
str_directory_path = passedDirectoryPath
fetch_success = False

# casting to Path 
directory_path = Path(str_directory_path)

if directory_path.exists():
    # check each directory in the directory for **/*.json file
    jsonslist = sorted(Path(directory_path).glob('*/*.json'))
    
    # for each json file in the list, get the name.
    for x in (jsonslist):
        y = PurePath(x)
        unsplit_objects.append(y.name)
    fetch_success = True
    # Split the names
    for object in unsplit_objects:
        name = object.split(".")
        object_names.append(name[0])
else:
      # TODO: change to pass error_message back
    print("Incorrect Path: " + objectType + " directory for names not found!")

if(fetch_success == True):
    print (object_names)
else:
    print(error_message)