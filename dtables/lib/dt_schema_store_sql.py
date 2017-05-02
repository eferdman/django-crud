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
            if 'update_column_sequence' in dtable.modifications:
                column_id = dtable.modifications['update_column_sequence'][0]
                new_sequence = dtable.modifications['update_column_sequence'][1]
                self.update_column_sequence(dtable, column_id, new_sequence)
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

        if sequence < last_sequence:
            for column in columns[sequence+1:]:
                queried_column = session.query(Columns).\
                    filter_by(table_id=dtable.table_id).filter_by(sequence=column.sequence).one()
                queried_column.sequence = queried_column.sequence - 1
        session.commit()

    def update_column_sequence(self, dtable, column_id, new_sequence):
        new_sequence = int(new_sequence)
        columns = session.query(Columns).\
            filter_by(table_id=dtable.table_id).order_by(Columns.sequence).all()
        column_to_update = session.query(Columns).\
            filter_by(id=column_id).one()
        old_sequence = column_to_update.sequence
        if new_sequence < old_sequence:
            columns_to_alter = columns[new_sequence:old_sequence]
            columns_to_alter.reverse()
            for column in columns_to_alter:
                print("Updating column: {}".format(column))
                queried_column = session.query(Columns).\
                    filter_by(table_id=dtable.table_id).filter_by(sequence=column.sequence).one()
                queried_column.sequence = queried_column.sequence + 1
        else:
            for column in columns[old_sequence+1:new_sequence+1]:
                queried_column = session.query(Columns).\
                    filter_by(table_id=dtable.table_id).filter_by(sequence=column.sequence).one()
                queried_column.sequence = queried_column.sequence - 1

        column_to_update.sequence = new_sequence
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