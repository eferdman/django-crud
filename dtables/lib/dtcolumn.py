import sqlalchemy.types as sa_types
from dtables.views import *


class DTColumn:
    def __init__(self, id, table_id, name, column_type, db_data_type, sequence):
        self.id = id
        self.table_id = table_id
        self.name = name
        self.internal_name = "col_{}".format(id)
        self.column_type = column_type
        self.db_data_type = db_data_type
        self.sequence = sequence
