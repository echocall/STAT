from handlers.assethandler import *
from nicegui import ui

save_data = {'name': 'Save A', 'base_game': 'Test', 
                     'create_date': '3/8/2025', 'date_last_save':'3/15/2025', 
                     'description':'A save for testing purposes.', 'asset_customs':True,
                      'asset_customs_path':'statassets\\datapacks\\test\\customs\\savea\\assets',
                       'actor_customs':False, 'asset_customs_path':'', 'event_customs':False,
                       'event_customs_path':'', 'effect_customs':False,'effect_customs_path':'',
                       'counters': {"Gold": 25, "Silver": 34, "Copper": 23, "Resources":'20', "Health": 84, "1st Level Spell Slots": 6},
                       'assets':{'Barracks': 2, 'Soldier': 4}, 'actors':{}, 
                       'current_events':{}, 'current_effects':{}, 'log_file_path':''}
assets = { 'Barracks':{'name':'Barracks', 'category':'Room', 'description':"A room for your soldiers to live in.",
                 'source':'Test', 'type':'Required', 'attributes':['Building', 'Unit Room'],
                 'buy_costs':{'Resources': 10}, 'sell_prices':{'Silver': 5},
                 'special':'Each Barrack can hold either 10 Soldiers or 10 Gunners. (They cannot share a grid after an ancient smear against rifles).',
                 'effects':[], 'icon':'','image':''},
                 # spell strike
                'Spell Strike':{'name':'Spell Strike', 'category':'Spell', 'description':"A quick spell that damages your enemy.",
                 'source':'Test', 'type':'Damage', 'attributes':['Damage', 'Arcane', 'Magic'],
                 'buy_costs':{"1st Level Spell Slot": 1, "Copper": 1}, 'sell_prices':{'none': 0},
                 'special':'Deals 1d6 damage to an enemy with a range of 60 ft.',
                 'effects':[], 'icon':'','image':''},
                 # soldier
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

print(sorted_assets)

assets_list = []
for category in sorted_assets:
    print("Category: ")
    print(category)
    print()
    print()
    assets_list = sorted_assets[category]
    print(assets_list)
for asset in assets_list: 
 #  for asset in sorted_assets[category]:
        with ui.card().tight():
            with ui.card_section():
                ui.label().bind_text_from(asset, 'name', backward=lambda name: f'Name: {name}')
                ui.label().bind_text_from(asset, 'description', backward=lambda description: f'{description}')
            with ui.card_actions().classes("w-full justify-end"):
                ui.button('Select Game', on_click=lambda: ui.notify('This will load the game.'))
print()
print()

"""asset_card_container = ui.row().classes("full flex items-center")
with asset_card_container:
    for asset in sorted_assets[category]:
        with ui.card().tight():
            with ui.card_section():
                ui.label().bind_text_from(asset, 'name', backward=lambda name: f'Name: {name}')
                ui.label().bind_text_from(asset, 'description', backward=lambda description: f'{description}')
            with ui.card_actions().classes("w-full justify-end"):
                ui.button('Select Game', on_click=lambda: ui.notify('This will load the game.'))"""

    # category = sorted_assets[key]
    # assets = sorted_category[category]
    # asset = assets[i]

ui.run()