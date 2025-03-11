from dataclasses import dataclass
import datetime
import json

@dataclass
class MySave:
    name: str
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
    actors: dict
    current_events: dict
    current_effects: dict
    log_file_path: str

    def __post__init__(self, name, createDate, dateLastSave, description, 
                 assetCustoms, assetCustomsPath, actorCustoms, actorCustomsPath,
                 eventCustoms,eventCustomsPath, effectCustoms, effectCustomsPath,
                   counters, assets, actors, currentEvents,
                     currentEffects, logFilePath ):
        self.name = name
        self.create_date = createDate
        self.date_last_save = dateLastSave
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

    def create_from_dict(self,saveDict=None):
        if saveDict is not None:
            for key, value in saveDict.items():
                setattr(self, key, value)

    def update_counters(self, counterDict=None):
        if counterDict is not None:
            self.counters = counterDict

    def update_assets(self, assetDict=None):
        if assetDict is not None:
            self.assets = assetDict

    def update_actors(self, actorDict=None):
        if actorDict is not None:
            self.actors = actorDict
    
    def update_events(self, eventDict=None):
        if eventDict is not None:
            self.current_events = eventDict

    def update_effecs(self, effectDict=None):
        if effectDict is not None:
            self.current_effects = effectDict

    # other update stuff.
    def save(self):
        self.date_last_save = datetime.today('EDT')

    # to_JSON
    def to_JSON(self):
        return json.dumps(self,  indent=4)