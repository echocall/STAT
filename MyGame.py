from dataclasses import dataclass
import json

@dataclass
class MyGame:
    name: str
    description: str
    has_counters: bool
    counters: dict
    has_actors: bool
    actor_default_path: str
    default_actors: list
    has_assets: bool
    asset_default_path: str
    default_assets: list
    has_events: bool
    event_default_path: str
    default_events: list
    has_effects: bool
    effect_default_path: str
    default_effects: list
    icon: str
    save_files_ath: str
    has_turns: bool
    turn_type: str
    start_turn: int

    def __init__(self, gameDict=None):
        if gameDict is not None:
            for key, value in gameDict.items():
                setattr(self, key, value)
    
    def __init__(self, name, description, has_counters, counters, has_actors, actor_default_path,
                 default_actors, has_assets, asset_default_path, default_assets, 
                 has_events, event_default_path, default_events, has_effects, effect_default_path,
                 default_effects, icon, save_files_ath, has_turns, turn_type, start_turn):
        self.name = name
        self.description = description
        self.has_counters = has_counters
        self.counters = counters
        self.has_actors = has_actors
        self.actor_default_path = actor_default_path
        self.default_actors = default_actors
        self.has_assets = has_assets
        self.asset_default_path = asset_default_path
        self.default_assets = default_assets
        self.has_events = has_events
        self.event_default_path = event_default_path
        self.default_events = default_events
        self.has_effects = has_effects
        self.effect_default_path = effect_default_path
        self.default_effects = default_effects
        self.icon = icon
        self.save_files_ath = save_files_ath
        self.has_turns = has_turns
        self.turn_type = turn_type
        self.start_turn = start_turn