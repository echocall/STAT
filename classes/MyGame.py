from dataclasses import dataclass
import json

@dataclass
class MyGame:
    name: str
    description: str
    has_counters: bool
    counters: dict
    has_actors: bool
    default_actors: list
    has_assets: bool
    default_assets: list
    has_events: bool
    default_events: list
    has_effects: bool
    default_effects: list
    icon: str
    has_turns: bool
    turn_type: str
    start_turn: int
    image: str

    
    def __post__init__ (self, name: str, description: str, has_counters: bool, counters: dict,
                has_actors: bool, default_actors: list,
                  has_assets: bool,default_assets: list, 
                 has_events: bool, default_events: list, 
                 has_effects: bool, default_effects: list,
                   icon: str, has_turns: bool, 
                   turn_type: str, start_turn: int, image: str):
        self.name = name
        self.description = description
        self.has_counters = has_counters
        self.counters = counters
        self.has_actors = has_actors
        self.default_actors = default_actors
        self.has_assets = has_assets
        self.default_assets = default_assets
        self.has_events = has_events
        self.default_events = default_events
        self.has_effects = has_effects
        self.default_effects = default_effects
        self.icon = icon
        self.has_turns = has_turns
        self.turn_type = turn_type
        self.start_turn = start_turn
        self.image = image

    def set_from_dict(self, gameDict):
        if self is None and gameDict is not None:
            for key, value in gameDict.items():
                setattr(self, key, value)

    """
    def load_from_json(self, **my_json_object):
        
    """

    def __str__(self):
        return self.name +" : " + self.description

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def add_counter(self, counter_key, counter_value):
        self.counters[counter_key] = counter_value

    def remove_counter(self, counter_key):
        self.counters.pop(counter_key)
    
    def get_savepath(self):
        return self.save_files_path
    