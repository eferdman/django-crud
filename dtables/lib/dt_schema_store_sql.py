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
                dt_columns.append(DTColumn(column.id, column.table_id, column.name, column.type, None))

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
                column_id = dtable.modifications['delete_column'][0]
                column = session.query(Columns).filter_by(id=column_id).one()
                self.delete_column(dtable, column)
            if 'delete_table' in dtable.modifications:
                table = session.query(Users).filter_by(id=dtable.table_id).one()
                self.delete(table)
            if 'update_name' in dtable.modifications:
                updated_name = dtable.modifications['update_name']
                self.update_name(dtable, updated_name)
                dtable.modifications = {}
            if 'update_column_name' in dtable.modifications:
                column_id = dtable.modifications['update_column_name'][0]
                updated_name = dtable.modifications['update_column_name'][1]
                self.update_column_name(column_id, updated_name)
                dtable.modifications = {}

    def update_name(self, dtable, updated_name):
        table = session.query(Users).filter_by(id=dtable.table_id).one()
        table.table_name = updated_name
        session.commit()

    def update_column_name(self, column_id, updated_name):
        column = session.query(Columns).filter_by(id=column_id).one()
        column.name = updated_name
        session.commit()

    def add_column(self, dt_column):
        table_id = dt_column.table_id
        name = dt_column.name
        column_type = dt_column.db_data_type

        columns = session.query(Columns).filter_by(table_id=table_id).order_by(Columns.sequence).all()
        if not columns:
            sequence = 0
        else:
            sequence = columns.pop().sequence + 1

        new_column = Columns(table_id=table_id, name=name, type=column_type, sequence=sequence)
        self.insert(new_column)

    def delete_column(self, dtable, column):
        columns = session.query(Columns).filter_by(table_id=dtable.table_id).order_by(Columns.sequence).all()

        sequence = column.sequence
        last_sequence = len(columns) - 1

        session.delete(column)
        session.commit()

        if sequence < last_sequence:
            next_sequence = sequence + 1
            for column in columns[sequence+1:]:
                queried_column = session.query(Columns).\
                    filter_by(table_id=dtable.table_id).filter_by(sequence=next_sequence).one()
                queried_column.sequence -= 1
                next_sequence += 1
        session.commit()

    def delete(self, row):
        session.delete(row)
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