import elements.theme as theme
from elements.message import message
from classes.Enable import Enable
from nicegui import ui

# TODO: Fix returns & passing info in.
# TODO: don't call during the creation of a new game, wait until game has been created?
# COULD pass in the value in the game.name, or have a list of game names passed in in other call cases... hm...
enable = Enable()
async def create() -> None:
    @ui.page('/neweffect')
    def new_effect():
        with theme.frame('Create an Effect'), ui.card().classes("w-full"):
            message('Create an Effect')
            # Input name for the asset.
            with card().classes("w-full"):
                with ui.card_section().classes('w-80 items-stretch'):
                    ui.label('Enter a name for the new effect: ')
                    name_input = ui.input(label='Effectt Name', placeholder='50 character limit',
                                on_change=lambda e: name_chars_left.set_text(len(e) + ' of 50 characters used.'))
                    name_input.props('clearable')
                    name_input.validation={"Too short!": enable.is_too_short} 
                    name_chars_left = ui.label()

                with ui.card_section().classes('w-80 items-stretch'):
                    ui.label('Enter a category for the new asset: ')
                    category_input = ui.input(label='Category', placeholder='50 character limit',
                                on_change=lambda e: category_chars_left.set_text(len(e) + ' of 50 characters used.'))
                    category_input.props('clearable')
                    category_input.validation={"Too short!": enable.is_too_short} 
                    category_chars_left = ui.label()

                # Input description for the asset.
                with ui.card_section().classes('w-80 items-stretch'):
                    ui.label('Enter a description for the new asset:').classes()
                    description = ui.input(label='Effect Description', placeholder='500 character limit',
                                    on_change=lambda f: desc_chars_left.set_text(str(len(f.value)) + ' of 500 characters used.')).props('clearable')
                    # this handles the validation of the field.
                    description.validation={"Too long!": lambda b: enable.is_too_long_variable(b, 500)}
                    desc_chars_left = ui.label()
            
                # Name the source 
                with ui.card_section().classes('w-80 items-stretch'):
                    ui.label('Enter the source game for the Effect: ')
                    # TODO: Grab the game name from list of games.

            # For grouping/sorting different effects later
            with ui.card_section().classes('w-80 items-stretch'):
                ui.label("What type of effect is it?")
                effect_type = ui.radio({1: 'Helpful', 
                                        2: 'Harmful', 
                                        3: 'Situational'}).props('inline')

            # If there is a timing element(count down/count up)
            with ui.card_section().classes('w-80 items-stretch'):
                ui.label("Is there a timing element inolved based on turns/rounds for eithr duration or the triggering of the effect?")
                has_timing = ui.switch()

                # Timing element part 2
                ui.label("What kind of timing effect based on turns or rounds?")
                with ui.column().bind_visibility_from(has_timing,'value'):
                    ui.label("Is a count down or a count up?")
                    timing_type = ui.radio({1: 'Count Down', 
                                            2: 'Count Up',
                                            3: 'Other'}).props('inline')
                    
            # What count as valid targets for the effect?
            with ui.card_section().classes('w-80 items-stretch'):
                ui.label("What type of objects does the effect apply to?")
                effected_object = ui.radio({1: 'Actors', 
                                        2: 'Assets', 
                                        3: 'Counters',
                                        4: 'Effects'}).props('inline')

            # How does is the effect directed?
            with ui.card_section().classes('w-80 items-stretch'):
                ui.label("How do you want to select its target?")
                effect_targeting = ui.radio({1: 'Set at Creation', 
                                            2: 'Choose when Called', 
                                            3: 'All valid Objects'}).props('inline')

                    
            # Where does the effect come from?
            with ui.card_section().classes('w-80 items-stretch'):
                ui.label("What causes the effect?")
                effect_source = ui.radio({1: 'Actor', 
                                        2: 'Asset', 
                                        3: 'Counter',
                                        4: 'Other'}).props('inline')

            # Numerical amount change check
            with ui.card_section().classes('w-80 items-stretch'):
                ui.label("Does the effect cause a increase or decrease in an amount?")
                numeric_change = ui.switch()

                with ui.column().bind_visibility_from(numeric_change,'value'):
                    ui.label("Is it an increase or decrease?")
                    timing_type = ui.radio({1: 'Increases an amount', 
                                            2: 'Decreases an amount'}).props('inline')
        