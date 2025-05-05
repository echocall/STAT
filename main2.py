from nicegui import ui
from elements.message import message
from elements.UserConfirm import UserConfirm

message("This here.")

# Import this class from your file if it's defined elsewhere:
# from your_module import UserConfirm

@ui.page('/')
def index():
    message('Hello there')
    confirm = UserConfirm()

    def delete_item():
        print("Item deleted!")

    ui.button("Delete Item", on_click=lambda: confirm.show_popup(
        "Do you really want to delete this item?", delete_item
    ))

ui.run()