from .dtable import DTable
from .dtcolumn import DTColumn
from dtables.models import Base, Users, Columns
from ..helpers import *


class DTSchemaStoreSQL:
    """A singleton instance of this class is responsible for getting and setting the schema for
       the Users and Columns tables only
       Add, Delete, Update rows in these tables. 
       """
    def __init__(self):
        pass

    def get_schema(self, table_id):
        dt_columns = []
        columns = session.query(Columns).filter_by(table_id=table_id).all()
        columns.sort(key=lambda x: x.sequence)
        for column in columns:
            dt_columns.append(DTColumn(column.id, column.name, column.type, column.sequence))

        internal_name = "table_{}".format(table_id)
        table_name = session.query(Users).filter_by(id=table_id).one().table_name

        return DTable(table_id, internal_name, table_name, dt_columns)

    def set_schema(self, dtable):
        if 'add_column' in dtable.modifications:
            dt_column = dtable.modifications['add_column']
            self.add_column(dt_column)

        # TODO: check if table "real name" exists or not when adding tables

    def add_column(self, dt_column):
        table_id = dt_column.table_id
        name = dt_column.name
        column_type = dt_column.column_type
        sequence = dt_column.sequence
        # add row to Columns table using sqlalchemy
        new_column = Columns(table_id=table_id, name=name, type=column_type, sequence=sequence)
        insert(new_column)

    # Add the new table to the schema
    # TODO: add this to set_schema
    def gen_table(self, user, table_name):
        new_user = Users(name=user, table_name=table_name)
        session.add(new_user)
        session.commit()

        internal_name = "table_{}".format(new_user.id)

        return DTable(new_user.id, internal_name, table_name, [])

    def get_tables(self):
        pass