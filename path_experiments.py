import os
import json
from pathlib import Path

# Use Strategy design strategy to pick which filepath to use: UNITS, ROOMS, or IMAGES
# Run the iterative forloop for each of thos SEPARATELY to write files into list.

"""
p = Path('C:\\Users\\strip\\Documents\\github\\STAT\\assets\\ROOMS')
subdirectories = [x for x in p.iterdir() if x.is_dir()]
print(subdirectories)

directory = Path('C:\\Users\\strip\\Documents\\github\\STAT\\assets'
"""

# splits subdirectories and create lists based on them. 
#for subdirectory in subdirectories:
    # Get the directories, go to each directory & write the contents to a list
    # If the directory contains a subdirectory: create a new list to hold the contents of the subdirectory
    # append new list to the outer list.
    # Final Product: Buffing[dorms,shrines[defense,fortune]]
path = Path('C:\\Users\\strip\\Documents\\github\\STAT\\assets\\ROOMS')
# gets list of all paths of the files ending in .json
jsonslist = list(path.glob('**/*.json'))
print("Printing jsonslist: ")
print(jsonslist)

units = []
# uses the paths from jsonslist to pull the data from each asset.
print("using the Paths.")
for path in jsonslist:
    with open(path) as f:
        units.append(json.load(f))

# print(units)
print(type(units[0]))


