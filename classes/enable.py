# from https://github.com/zauberzeug/nicegui/discussions/1791
class Enable:
    def __init__(self) -> None:
        self.inputs = {}
        self.no_errors = True

    def is_too_short(self, v):
        return v and len(v) > 0
    
    # made this myself
    def is_too_short_variable(self, v, min_length):
        return v and len(v) > min_length
    
    # added this
    def not_null(self,v):
        return v and v != None
    
    # added this
    def is_too_long_variable(self, value, max_length):
        return value and len(value) < max_length

    def on_change(self, e):
        valid = self.is_too_short(e.value)
        self.inputs[e.sender.id] = valid
        self.update()

    def update(self):
        for i in self.inputs.values():
            if i is not True:
                self.no_errors = False
                break
        else:
            self.no_errors = True