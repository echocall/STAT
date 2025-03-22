# base from second example here: https://github.com/zauberzeug/nicegui/discussions/1791
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

    def on_change(self, e, check, *args):
        # checking if more than 0 characters
        if check == 'short':
            valid = self.is_too_short(e.value)
            self.inputs[e.sender.id] = valid
            self.update()
        # checking if we're using the custom too_short
        elif check == 'short_variable':
            valid = self.is_too_short_variable(e.value, args)
            self.inputs[e.sender.id] = valid
            self.update()
        # checking if too_long
        elif check == 'long':
            valid = self.is_too_long_variable(e.value, args)
            self.inputs[e.sender.id] = valid
            self.update()
         # checking if null
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