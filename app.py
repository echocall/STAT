import os
assets_file_path = 'C:\\Users\\strip\\Documents\\github\\STAT\\assets'
timesRun = 0

# Use Strategy design strategy to pick which filepath to use: UNITS, ROOMS, or IMAGES
# Run the iterative forloop for each of thos SEPARATELY to write files into list.
for directory, subdirlist, filelist in os.walk(assets_file_path):
    print(directory)
    print(subdirlist) 
    for f in filelist:
        print('\t' + f)

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