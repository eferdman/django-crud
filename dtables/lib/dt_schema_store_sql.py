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

    def get_schema(self, table_name, table_id=None):
        if table_id:
            dt_columns = []
            columns = session.query(Columns).filter_by(table_id=table_id).all()
            columns.sort(key=lambda x: x.sequence)
            for column in columns:
                dt_columns.append(DTColumn(column.id, column.name, column.type, None, column.sequence))

            internal_name = "table_{}".format(table_id)
            table_name = session.query(Users).filter_by(id=table_id).one().table_name

            return DTable(table_name, dt_columns, table_id, internal_name)
        else:
            return DTable(table_name)

    def set_schema(self, dtable):
        if not dtable.table_id:
            self.gen_table(dtable)
        else:
            if 'add_column' in dtable.modifications:
                dt_column = dtable.modifications['add_column']
                self.add_column(dt_column)
            if 'delete_column' in dtable.modifications:
                column = dtable.modifications['delete_column']
                self.delete_column(column)
            if 'delete_table' in dtable.modifications:
                row_to_delete = session.query(Users).filter_by(id=dtable.table_id).one()
                self.delete(row_to_delete)

        # TODO: check if table "real name" exists or not when adding tables

    def add_column(self, dt_column):
        table_id = dt_column.table_id
        name = dt_column.name
        column_type = dt_column.db_data_type
        sequence = dt_column.sequence

        new_column = Columns(table_id=table_id, name=name, type=column_type, sequence=sequence)
        self.insert(new_column)

    def delete_column(self, column):
        session.delete(column)
        session.commit()

    # Add the new table to the schema
    def gen_table(self, dtable):
        new_table = Users(name="Default User", table_name=dtable.table_name)
        self.insert(new_table)

        dtable.table_id = new_table.id
        dtable.internal_name = "table_{}".format(new_table.id)

    def insert(self, row):
        session.add(row)
        session.commit()

    def get_tables(self):
        pass