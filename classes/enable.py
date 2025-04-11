# base from second example here: https://github.com/zauberzeug/nicegui/discussions/1791
class Enable:
    def __init__(self) -> None:
        self.inputs = {}
        self.no_errors = True
        self.interacted = {}  # Track if the user has interacted with a field

    def is_too_short(self, v):
        return v and len(v) > 0

    def is_too_short_variable(self, v, min_length):
        return v and len(v) > min_length

    def not_null(self, v):
        return v and v != None

    def is_too_long_variable(self, value, max_length):
        return value and len(value) < max_length

    def on_change(self, e, check, *args):
        # Mark the field as interacted
        self.interacted[e.sender.id] = True

        # Perform validation only if the field has been interacted with
        if check == 'short':
            valid = self.is_too_short(e.value)
            self.inputs[e.sender.id] = valid
        elif check == 'short_variable':
            valid = self.is_too_short_variable(e.value, args)
            self.inputs[e.sender.id] = valid
        elif check == 'long':
            valid = self.is_too_long_variable(e.value, args)
            self.inputs[e.sender.id] = valid
        else:
            valid = self.not_null(e.value)
            self.inputs[e.sender.id] = valid

        self.update()

    def update(self):
        for i in self.inputs.values():
            if i is not True:
                self.no_errors = False
                break
        else:
            self.no_errors = True