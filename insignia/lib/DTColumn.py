import sqlalchemy.types as sa_types


class DTColumn:
    def __init__(self, id, name, column_type, internal_name=None):
        self.id = id
        self.name = name
        self.column_type = sa_types.String
