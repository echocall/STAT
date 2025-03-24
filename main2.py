from handlers.assethandler import *
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

counters = {'Gold': 10, "Silver": 25, "Copper": 100, "Health": 100, "1st Level Spell Slot": 3}

sorted_assets = sort_assets_by_category(assets)
owned_assets_unsorted = fetch_owned_assets(assets, save_data['assets'])
sorted_owned_assets = sort_assets_by_category(owned_assets_unsorted)

print(sorted_assets)

print()
print()
for counter in counters:
    print(counter)
    print(counters[counter])

assets_list = []
print()
print()

