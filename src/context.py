class Context:
    def __init__(self):
        self.variables = {}

    def add_variable(self, name, value, dtype=None):
        self.variables[name] = {'value': value, 'dtype': dtype}

    def update_variable(self, name, value):
        if name in self.variables:
            self.variables[name]['value'] = value
        else:
            raise NameError(f"Variable '{name}' not defined.")

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            raise NameError(f"Variable '{name}' not defined.")

    def has_variable(self, name):
        return name in self.variables

    def clear(self):
        self.variables.clear()