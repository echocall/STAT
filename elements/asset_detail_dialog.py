from nicegui import app,ui
 # display asset detials

def asset_detail_dialog():
    with ui.dialog() as asset_detail, ui.card().classes("w-full"):
        selected_asset = app.storage.user.get("selected_asset", {})
        buy_costs = {}
        sell_prices = {}
        
        # there IS a selected asset
        if bool(selected_asset):
            buy_costs = selected_asset['buy_costs']
            sell_prices = selected_asset['sell_prices']
        
            with ui.card_section().classes('items-stretch'):
                ui.label(f'{selected_asset['name']}').classes('h3')

                ui.image(selected_asset['icon'])

                ui.label().bind_text_from(selected_asset['category'])

                ui.label().bind_text_from(selected_asset['description'])

                ui.label().bind_text_from(selected_asset['source'])

                ui.label("Asset Type").classes('font-bold')
                ui.label().bind_text_from(selected_asset['asset_type'])

                ui.label("Attributes").classes('font-bold')
                for attribute in selected_asset['attributes']:
                    ui.label().bind_text_from(attribute)

                ui.label("Buy Costs").classes('font-bold')
                for key, value in buy_costs.items():
                    ui.label(f'{key}: {value}')

                ui.label("Sell Prices").classes('font-bold')
                for key, value in sell_prices.items():
                    ui.label(f'{key}: {value}')

                ui.label().bind_text_from(selected_asset['special'])

                ui.label("Effects").classes('font-bold')
                for attribute in selected_asset['attributes']:
                    ui.label().bind_text_from(attribute)

                ui.image(selected_asset['image']).classes('object-scale-down')

        else:
            ui.label("Must select an asset to view its details!")
        with ui.card_actions():
            # Cancel out of dialog.
            ui.button("Close", on_click=asset_detail.close)
 