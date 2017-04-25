from collections import OrderedDict
from dtables.views import *
from sqlalchemy import inspect
from .dtcolumn import DTColumn


# represents a user generated table
class DTable:
    def __init__(self, table_id, internal_name, table_name, dt_columns):
        self.table_id = table_id
        self.internal_name = internal_name
        self.table_name = table_name
        self.columns = dt_columns
        self.modifications = {}

    # expect DTColumn Objects
    def get_columns(self):
        return self.columns

    # pass in a DTColumn object here
    def add_column(self, dt_column):
        # validate that the object passed in is of type DTColumn
        if not (isinstance(dt_column, DTColumn)):
            raise Exception("Invalid DTColumn Object")
        self.modifications['add_column'] = dt_column

    # need to match in order to remove the correct item
    def remove_column(self):
        pass

    # print the parameters and the columns, types
    def __repr__(self):
        return "<DTable {} {} {}>".format(self.internal_name, self.table_id, self.table_name)