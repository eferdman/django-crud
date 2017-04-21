from .dtable import DTable
from dtables.models import Base, Users, Columns
from ..helpers import *

class DTSchemaStoreSQL:
    """A singleton instance of this class is responsible for getting and setting the schema for
       the Users and Columns tables. (changing rows to the Users and Columns tables)
       """
    def __init__(self):
        pass

    def get_schema(self, name):
        return DTable(name)

    def get_tables(self):
        pass

    def set_schema(self, table):
        pass
