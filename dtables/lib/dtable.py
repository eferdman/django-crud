from .dtcolumn import DTColumn


class DTable:
    def __init__(self, table_name, dt_columns=None, table_id=None, internal_name=None):
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

    def delete(self):
        self.modifications['delete_table'] = True

    def update_name(self, updated_name):
        self.modifications['update_name'] = updated_name

    def update_column_name(self, column_id, updated_name):
        self.modifications['update_column_name'] = (column_id, updated_name)

    # need to match in order to remove the correct item
    def delete_column(self, column_id, column_type):
        self.modifications['delete_column'] = (column_id, column_type)

    def update_column_sequence(self, column_id, new_sequence):
        self.modifications['update_column_sequence'] = (column_id, new_sequence)

    # print the parameters and the columns, types
    def __repr__(self):
        return "<DTable {} {} {}>".format(self.internal_name, self.table_id, self.table_name)