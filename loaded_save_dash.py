from nicegui import ui
import theme

def create() -> None:
    @ui.page('/loadeddash')
    def view_saves():
        with theme.frame('- View Saves -'):
            saves = {'name': 'Save A', 'base_game': 'Test', 
                     'create_date': '3/8/2025', 'date_last_save':'3/15/2025', 
                     'description':'A save for testing purposes.', 'asset_customs':True,
                      'asset_customs_path':'statassets\\datapacks\\test\\customs\\savea\\assets',
                       'actor_customs':False, 'asset_customs_path':'', 'event_customs':False,
                       'event_customs_path':'', 'effect_customs':False,'effect_customs_path':'',
                       'counters': {"Gold": 25, "Silver": 34, "Copper": 23, "Health": 84, "1st Level Spell Slots": 6},
                       'assets':{'Barracks': 2, 'Soldier': 4}, 'actors':{}, 
                       'current_events':{}, 'current_effects':{}, 'log_file_path':''}
            
        with ui.tabs().classes('w-full') as tabs:
            main = ui.tab('Main')
            assets = ui.tab('Assets - Owned')
            store = ui.tab('Assets - Store')
        with ui.tab_panels(tabs, value=main).classes('w-full'):
            with ui.tab_panel(main):
                ui.label('Main tab')
            with ui.tab_panel(assets):
                ui.label('Assets tab')
            with ui.tab_panel(store):
                ui.label('Assets Store tab')