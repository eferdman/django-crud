from collections import OrderedDict


# represents a user generated table
class DTable:
    def __init__(self, id, name, internal_name):
        self.id = id
        self.name = name
        self.internal_name = name

        # remembers order
        self.columns = OrderedDict()
        self.columns = []

    # expect DTColumn Objects
    def get_columns(self):
        return self.columns

    # Add a column to the dynamically generated table
    def add_column(table_name, column_name, column_type):
        table = Table(table_name, metadata)
        col = sqlalchemy.Column(column_name, getattr(sa_types, column_type))
        col.create(table, populate_default=True)

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

    def move_column(self):
        pass

    def __repr__(self):
        return "<DTable {} {} {}>".format(self.internal_name, self.id, self.name)