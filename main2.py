from nicegui import ui
from elements.message import message
from elements.UserConfirm import UserConfirm

message("This here.")

# Import this class from your file if it's defined elsewhere:
# from your_module import UserConfirm

new_amount = {'amount': 0}

new_turn = {'start_value': 110}


# the __setitem__ is equivalent to new_amount['amount'] = e.value, but is allowed inside a lambda function.
amount = ui.number('amount', value='100', 
                   on_change=lambda e: new_amount.__setitem__('amount', int(e.value) if e.value is not None else 0))

result = ui.label()


if new_turn['start_value'] > -1:
    print(int(new_turn['start_value']))
else:
    print('Oh no, oh no, oh no oh no oh no.')


ui.button("Get Amount Value", on_click=lambda: print(new_amount))

ui.run(native=True)