from dataclasses import dataclass

@dataclass
class MyStat:
    # add something for the config file
    config_file: str
    is_game_loaded: bool
    game_loaded: dict
    game_loaded_name: str
    is_save_loaded: bool
    save_loaded: dict
    save_loaded_name: str
    is_assets_loaded: bool
    assets_loaded: dict
    
    def __post__init__(self, configFile: str):
        self.config_file = configFile
        self.is_game_loaded = False
        self.game_loaded = {}
        self.game_loaded_name = ""
        self.is_save_loaded = False
        self.save_loaded = {}
        self.save_loaded_name = ""
        self.is_assets_loaded = False
        self.assets_loaded = []

    def gameLoaded(self, game_object: dict, game_name: str):
        self.is_game_loaded = True
        self.game_loaded = game_object
        self.game_loaded_name = game_name
    
    def gameUnloaded(self):
        self.is_game_loaded = False
        self.game_loaded = ""
        self.game_loaded_name = ""

    def saveLoaded(self, save_object: dict, save_name: str):
        self.is_save_loaded = True
        self.save_loaded = save_object
        self.save_loaded_name = save_name
    
    def saveUnloaded(self):
        self.is_save_loaded = False
        self.save_loaded = ""
        self.save_loaded_name = ""

    def assetsLoaded(self, asset_objects: list):
        self.is_assets_loaded = True
        self.assets_loaded = asset_objects

    def assetsUnloaded(self):
        self.is_assets_loaded = False
        self.assets_loaded = ""

    # TODO space to store the numbers from a save
        # Counters, # of units.

    # TODO space to store current effects

    # TODO space to store current events

    # TODO space to store actors

    # TODO 
