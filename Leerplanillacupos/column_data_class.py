

class Column:
    ordinal_position: int
    position: int
    name: str
    alias: str
    defined:bool
    default_value: str

    def __init__(self, ordinal_position: int, position: int, name: str, alias: str, defined: bool, default_value: str = None):
        self.ordinal_position = ordinal_position
        self.position = position
        self.name = name
        self.alias = alias
        self.defined = defined
        self.default_value = default_value
