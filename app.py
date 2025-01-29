import os
from pathlib import Path

assets_file_path = 'C:\\Users\\strip\\Documents\\github\\STAT\\assets'
timesRun = 0

# Use Strategy design strategy to pick which filepath to use: UNITS, ROOMS, or IMAGES
# Run the iterative forloop for each of thos SEPARATELY to write files into list.
''' for directory, subdirlist, filelist in os.walk(assets_file_path):
    print(directory)
    print(subdirlist) 
    for f in filelist:
        print('\t' + f) '''

p = Path('C:\\Users\\strip\\Documents\\github\\STAT\\assets\\ROOMS')
subdirectories = [x for x in p.iterdir() if x.is_dir()]
print(subdirectories)

directory = Path('C:\\Users\\strip\\Documents\\github\\STAT\\assets')


# splits subdirectories and create lists based on them. 
#for subdirectory in subdirectories:
    # Get the directories, go to each directory & write the contents to a list
    # If the directory contains a subdirectory: create a new list to hold the contents of the subdirectory
    # append new list to the outer list.
    # Final Product: Buffing[dorms,shrines[defense,fortune]]
    
    # 

path = Path('C:\\Users\\strip\\Documents\\github\\STAT\\assets\\ROOMS')
jsonslist = list(path.glob('**/*.json'))
#print(jsonslist)

units = []

for path in jsonslist:
    units.append(path.read_text())

print(units)

# Order of operations: Fetch information from ROOMS or UNITS folders and throw into list
# Rewrite list to account for anything with the same RoomType or UnitType into its own mini-list inside the big list.
# Use the Rewritten list to generate the 'cards' in the GUI with the multiple objects of same Type being 'stacked' or opening when clicked.

# ???
# - "Unit" handler
# - "Room" handler
# - Treasurery manager
# - Enemy STR Calculator
# - Layer tracker
# - GUI
# - Player Combat STR tracker
# - Specials from Rooms tracker
# 


# Profit!!!