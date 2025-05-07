# STAT
 Snazzy Tabletop (Game) Assistant Tracker

The purpose of this app is to provide a useful tool for keeping track of various numbers, counters, items, and so on that accumulate while playing a game. Especiall for a longer running game that the player may have to pause and continue on various days.

Built with Python backend and NiceGUI for the front end, it provides a visual way of looking at the data that will eventually be nicer and easier to look at than a bunch of notes scrawled in a notepad. It aims to eventually help automate some of those tedious tasks like updating how much money the player has when they buy and sell an item in the game, keeping track of what effects ore events might be going on at any particular time, and other such functionality. It will also eventually automatically create and update a log file with the player's actions during a session of play so they can later look back at it.

Currently the user can create a Game file which will hold the default values and information they set. 
The user can use the View Game, or game_details page to view a game in more detail and edit it.
 - The user can save those changes to teh game file.
 - The user can also decide to delete the entire directory that game lives in from the details page.
   - This keeps lost heads from running around.
The user can also create a Save file for that game that will use the values in the game as the basis for its own creation.
The user can use the dashboard to adjust values of the counters of a game and save those changes to a file.
The user can also create an Asset to be tracked later, although full implementation of these is still a work in progress.
The user can view all the assets for a game, and delet an asset.


### INSTALL INSTRUCTIONS ####
- Fork the repository and open it in github
- In the console use "pip install -r requirements.txt" to install the requirements.
- 

- Run the program for the first time. This will allow STAT to try and find where it wants to live, generally a common folder path where it has write permissions.
- STAT itself can live anywhere, it uses hard-path files in its config.txt file to tell it where to find the folders it makes and the templates it needs.
  - What is important is keeping the file structure for those files intact, especially config.txt
- The zip folder for the templates has been included.
- You can check the config.txt to find where STAT has tried to find the best paths for it to write to.
- It tries to detect what operating system you're on, and then pick the most common available path.

STAT
├── config.txt
│   
└── statassets
    ├── games
    │   └── <game_name>
    │       ├── <game_name>.json
    │       ├── images
    │       │   └── <image_name>.png
    │       ├── saves
    │       ├── assets
    │       │   ├── Defaults
    │       │   └── Customs
    │       ├── effects
    │       │   ├── Defaults
    │       │   └── Customs
    │       └── events
    │           ├── Defaults
    │           └── Customs
    └── templates
        └── template_game.json
        └── template_save.json
        └── template_asset.json
        └── template_effect.json

If you need to run STAT from the python menu, fork the repository into the directory of your choice.
I've included a requirements.txt file that will enable you to install all the requirements into your python environment with "pip install -r requirements.txt" to get all the exact version of what I used.

More information can be found here: https://www.geeksforgeeks.org/how-to-install-python-packages-with-requirements-txt/


### STAT ###

### EXPLANATION OF TERMS: ###
Session - Any time you open up STAT to play a game can be thought of as a Session. Behind the scenes STAT is build to passively keep track of what you do during a Session via the dashboard. Eventually it'll be able to log all the actions you take so you can refer to that to remind yourself of what you did and why.


# Game # 
A game file in STAT is meant to capture what the starting conditions of a game. So if a game starts you off with 10 health, or 20 gold, you would set that in this game file as counters so every save you started afterwards would have those values. It also keeps track of Actors, Default Assets for the game (for later implementation of file parity), an icon, and a few other fields. You MUST have a Game created in order to make saves, assets, effects, or anything else in STAT.

# Counters #
The name says it. These keep track of numerical value. This can be used to keep track of health, money, or other more esoteric ideas like a wizard's spell slots. Assets will eventually interact with them through buy costs and sell prices, as will Effects and possibly Events when those are added in. The default vaules you put in your game folder will be automatically applied to any Save file you make of that game.

Example: I am starting a game of Winter Bunny Gardening, a game where you play as a rabbit trying to grow enough food to get you through the winter. For my counters I want to keep track of how much Wood I have as it is a resource that allows me to build more things. I also want to keep track of the number of Shiny Stones I have as those are used as currency, and I want to keep track of the Temperature because if it gets too low I can't grow anything. I put the following default values in:
Game: Winter Bunny Gardening
Wood: 10, Shiny Stones: 20, Temperature 78


# Actors #
These are saved as a list of names, and are useful when you want to have a name attached to an action that happens, or when targetting something (for the eventual logging feature) but don't need to store a lot of data about it. If I were playing D&D I could use an Actor to act as a stand in for an enemy who's stats I didn't know but I wanted to track what Effect I had applied to it.

Example: For Winter Bunny Gardening we have Player as a default actor, and we'll add 'Jack Frost' and 'Merchant' to keep track of when those figures show up in our logs.


# Assets #
These can be objects, rooms, or whatever else that exist within the game that you can accumulate. They will have built in mechanics for handling buying and selling based on what counters you have. They can store a lot of information in the multiple text fields as well. If you need to keep track of how much of something you have, you probably want an Asset. STAT will keep track of how many of each asset you have between sessions!

# Buy Costs and Sell Prices #
These two are two sides of the same coin, if you'll pardon the pun. A 'Buy Cost' generally means you have to pay X amount to add One of that asset to your owned amount. A 'Sell Price' is how much you get for getting rid of one of your owned assets of a particular type. In the future I hope to implement a more flexible math system, but I need to get these implemented first!

Example: For Winter Bunny Gardening I'll add a 'Field' with a Buy Cost of 20 Wood and a Sell Price of 5 Wood. This means in the future when I press the 'buy' button the application will automatically deduct 20 Wood from the appropriate counter and add '1' to my field count. When I press the 'Sell' button STAT will add 5 wood to my counter and deduct 1 Field from my tracked amount.

Deep Example: If I wanted to model something like Dungeons & Dragons or Pathfinder 2E as a wizard, I could use Counters to keep track of my spell slots of various levels (1st, 2nd, etcetera) and I could model my Spells as Assets so during combat I could 'buy' a spell to 'use' a Spell Slot of the appropriate type. If I wanted to use Spells at other spell levels than what I have the default asset set to, I could make it a Custom Asset.


# Effects # 
Once implemented these will be kept track of in a sidebar on the dashboard screen where the user will be able to easily keep visual track of them. They'll keep track of 'what' they are affecting whether that's a counter, asset, or actor, what their Source is, what they're doing, and other factors.
Sadly they are not yet implemented besides letting you look at the 'Create Effect' menu.

Example: In Winter Bunny Garden you sometimes have to deal with a flock of crows that hang around your farm for x number of turns and steal a Shiny Stone every turn. The best way to mock them up would be as an Effect as such:
Name: Crow Thieves! Target Type: Counter  Target: Shiny Stones  Duration: 3 Turns  Type: Negative Cost: -1 (Shiny Stones every turn)

Deep Example: For Pathfinder 2E I could use an Effect to model a buff I cast on myself and how long it lasts.
Mage Armor  Target Type: Actor   Target: Player   Duration: 5 Turns  Type: Positive
Cost: +5 (Armor Class)


TODO:
 - Dashboard Functionality improvement
   - Automatic adjustment and updating of counters when buying or selling an asset
   - Moving Assets from 'All Assets' to 'Owned' asset tab more cleanly
   - Implement Turns incrementing
 - Finish Create, Read, Update, Delete for Effects
 - Finish Delete for Save files
   - It needs a button, and a call to the appropriate function. Literally.
 - Finish View, Update, and Delete for Assets
 - Add Effects to the Dashboard
 - Implement Logging User Actions to File
 - Bug Fixing
   - I have tried to get this running somewhat cleanly for this deployment
 - ... and much, much more.