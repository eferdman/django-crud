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

        self.table = Table(self.internal_name, sqlalchemy.MetaData(bind=engine), autoload=True)
        self.rows = get_rows()
        self.columns = dt_columns

    # expect DTColumn Objects
    def get_columns(self):
        return self.columns
    
    def get_rows(self):
        rows = []
        if self.exists():
            rows = session.query(self.table).filter_by(table_id=table_id).all()
        return rows

    # pass in a DTColumn object here
    def add_column(self, dt_column):
        # validate that the object passed in is of type DTColumn
        if not (isinstance(dt_column, DTColumn)):
            raise Exception("Invalid DTColumn Object")
        name = dt_column.name
        self.columns.append(name)

    # need to match in order to remove the correct item
    def remove_column(self):
        pass

    def exists(self):
        return self.internal_name in meta.tables

    # print the parameters and the columns, types
    def __repr__(self):
        return "<DTable {} {} {}>".format(self.internal_name, self.id, self.table_name)