from dataclasses import dataclass
import datetime
import json

@dataclass
class MySave:
    name: str
    base_game: str
    create_date: str
    date_last_save: str
    description: str
    asset_customs: bool
    asset_customs_path: str
    actor_customs: bool
    actor_customs_path: str
    event_customs: bool
    event_customs_path: str
    effect_customs: bool
    effect_customs_path: str
    counters: dict
    assets: dict
    actors: list
    current_events: dict
    current_effects: dict
    current_turn: int
    log_file_path: str

    def __post__init__(self, name, baseGame, createDate, dateLastSave, description, 
                 assetCustoms, assetCustomsPath, actorCustoms, actorCustomsPath,
                 eventCustoms,eventCustomsPath, effectCustoms, effectCustomsPath,
                   counters, assets, actors, currentEvents,
                     currentEffects, logFilePath ):
        self.name = name
        self.base_game = baseGame
        self.create_date = datetime.strptime(str(createDate), '%\d-%m-%Y %H:%M:%S')
        self.date_last_save = datetime.strptime(str(dateLastSave), '%\d-%m-%Y %H:%M:%S')
        self.description = description
        self.asset_customs = assetCustoms
        self.asset_customs_path = assetCustomsPath
        self.actor_customs = actorCustoms
        self.actor_customs_path = actorCustomsPath
        self.event_customs = eventCustoms
        self.event_customs_path = eventCustomsPath
        self.effect_customs = effectCustoms
        self.effect_customs_path = effectCustomsPath
        self.counters = counters
        self.assets = assets
        self.actors = actors
        self.current_events = currentEvents
        self.current_effects = currentEffects
        self.log_file_path = logFilePath

    def __str__(self):
        return self.name + " Created: " + self.create_date + "  Last Saved: " + self.date_last_save

    def create_from_dict(self,saveDict=None):
        if saveDict is not None:
            for key, value in saveDict.items():
                setattr(self, key, value)

    def update_save(self, saveDict=None):
        if saveDict is not None:
            for key, value in saveDict.items():
                setattr(self, key, value)

    def set_counters(self, counterDict=None):
        if counterDict is not None:
            self.counters = counterDict

    def set_assets(self, assetDict=None):
        if assetDict is not None:
            self.assets = assetDict

    def set_actors(self, actorDict=None):
        if actorDict is not None:
            self.actors = actorDict
    
    def set_events(self, eventDict=None):
        if eventDict is not None:
            self.current_events = eventDict

    def set_effecs(self, effectDict=None):
        if effectDict is not None:
            self.current_effects = effectDict

    # Time stuff.
    def create(self):
        self.create_date = datetime.strptime(str(datetime.today('EDT')), '%\d-%m-%Y %H:%M:%S')
    
    def save(self):
        self.date_last_save = datetime.strptime(str(datetime.today('EDT')), '%\d-%m-%Y %H:%M:%S')

    # to_JSON
    def to_JSON(self):
        return json.dumps(self, indent=4)