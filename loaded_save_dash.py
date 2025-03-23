from nicegui import ui
from handlers.assethandler import *
from classes.CategoryLabel import CategoryLabel
from classes.AssetContainer import AssetContainer
import theme

# Dashboard for after a game has been selected, and a save has been loaded.
# Displays the user's information.
def create() -> None:
    @ui.page('/loadeddash')
    def view_saves():
       with theme.frame('View Saves'):
    # Getting assets sorted.
            save_data = {'name': 'Save A', 'base_game': 'Test', 
                     'create_date': '3/8/2025', 'date_last_save':'3/15/2025', 
                     'description':'A save for testing purposes.', 'asset_customs':True,
                      'asset_customs_path':'statassets\\datapacks\\test\\customs\\savea\\assets',
                       'actor_customs':False, 'asset_customs_path':'', 'event_customs':False,
                       'event_customs_path':'', 'effect_customs':False,'effect_customs_path':'',
                       'counters': {"Gold": 25, "Silver": 34, "Copper": 23, "Resources":'20', "Health": 84, "1st Level Spell Slots": 6},
                       'assets':{'Barracks': 2, 'Soldier': 4}, 'actors':{}, 
                       'current_events':{}, 'current_effects':{}, 'log_file_path':''}
            assets = { 
                 # Barracks
                 'Barracks':{'name':'Barracks', 'category':'Room', 'description':"A room for your soldiers to live in.",
                 'source':'Test', 'type':'Required', 'attributes':['Building', 'Unit Room'],
                 'buy_costs':{'Resources': 10}, 'sell_prices':{'Silver': 5},
                 'special':'Each Barrack can hold either 10 Soldiers or 10 Gunners. (They cannot share a grid after an ancient smear against rifles).',
                 'effects':[], 'icon':'','image':''},
                 # Spell Strike
                'Spell Strike':{'name':'Spell Strike', 'category':'Spell', 'description':"A quick spell that damages your enemy.",
                 'source':'Test', 'type':'Damage', 'attributes':['Damage', 'Arcane', 'Magic'],
                 'buy_costs':{"1st Level Spell Slot": 1, "Copper": 1}, 'sell_prices':{'none': 0},
                 'special':'Deals 1d6 damage to an enemy with a range of 60 ft.',
                 'effects':[], 'icon':'','image':''},
                 # Soldier
                'Soldier':{'name':'Soldier', 'category':'Unit', 'description':"A basic soldier.",
                 'source':'Test - Custom', 'type':'Offense', 'attributes':['Warrior', 'Unit', 'Human','Offense'],
                 'buy_costs':{'Gold': 2}, 'sell_prices':{'none': 0},
                 'special':'Deals 5 STR per solider in squad.',
                 'effects':[], 'icon':'','image':''},
                 # Warrior
                'Warrior':{'name':'Warrior', 'category':'Unit', 'description':"Warriors are strong, individualistic fighters.",
                 'source':'Test - Custom', 'type':'Offense', 'attributes':['Warrior', 'Unit', 'Human','Offense'],
                 'buy_costs':{'Gold': 4}, 'sell_prices':{'none': 0},
                 'special':'Deals 5 STR.',
                 'effects':[], 'icon':'','image':''},
            }
            sorted_assets = sort_assets(assets)
            owned_assets_unsorted = fetch_owned_assets(assets, save_data['assets'])
            sorted_owned_assets = sort_assets(owned_assets_unsorted)
            # The tabs
            with ui.tabs().classes('w-full') as tabs:
                main = ui.tab('Main')
                assets = ui.tab('Assets - Owned')
                store = ui.tab('Assets - Store')
            with ui.tab_panels(tabs, value=main).classes('full flex items-left'):
                with ui.tab_panel(main):
                        ui.label('Main tab')
                with ui.tab_panel(assets):
                        ui.label('Owned Assets tab')
                with ui.tab_panel(store):
                    ui.label('Assets Store tab')
                    # Creates each asset_container
                    for category in sorted_assets:
                        ui.separator()
                        asset_container = ui.row().classes("full flex")
                        with asset_container:
                            with ui.row():
                                CategoryLabel(category)
                            # Creates cards for each asset
                            for asset in sorted_assets[category]:
                                with ui.card().tight():
                                    with ui.card_section():
                                        ui.label().bind_text_from(asset, 'name', backward=lambda name: f'Name: {name}')
                                        ui.label().bind_text_from(asset, 'source', backward=lambda source: f'Source: {source}')
                                        ui.label().bind_text_from(asset, 'buy_costs', backward=lambda buy_costs: f'{buy_costs}')
                                        ui.label().bind_text_from(asset, 'sell_prices', backward=lambda sell_prices: f'{sell_prices}')
                                    with ui.card_actions().classes("w-full justify-end"):
                                        ui.button('Add Asset', on_click=lambda: ui.notify(f'You tried to add an asset to your owned assets.'))
                    
