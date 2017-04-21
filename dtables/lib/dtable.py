from collections import OrderedDict
from dtables.views import *

# represents a user generated table
class DTable:
    def __init__(self, name):
        self.name = name
        self.internal_name = name

        self.table = Table(name, sqlalchemy.MetaData(bind=engine), autoload=True)
        self.rows = session.query(self.table).all()

        # remembers order
        self.columns = OrderedDict()
        self.columns = []

    # expect DTColumn Objects
    def get_columns(self):
        return self.columns

    def get_data(self, table_id=None):
        if table_id:
            return session.query(self.table).filter_by(table_id=table_id).all()
        return self.rows

    # pass in a DTColumn object here
    # def add_column(self, dt_column):
    #     # validate that the object passed in is of type DTColumn
    #     if not (isinstance(dt_column, DTColumn)):
    #         raise Exception("Invalid DTColumn Object")
    #     name = dt_column.name
    #     self.columns.append(name)

    # need to match in order to remove the correct item
    def remove_column(self):
        pass

    # print the parameters and the columns, types
    def __repr__(self):
        return "<DTable {} {} {}>".format(self.internal_name, self.id, self.name)

    @staticmethod
    def move_column():
        print("HI")