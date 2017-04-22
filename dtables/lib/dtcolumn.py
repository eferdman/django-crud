import sqlalchemy.types as sa_types
from dtables.views import *


class DTColumn:
    def __init__(self, id, name, column_type):
        self.id = id
        self.name = name
        self.column_type = column_type
