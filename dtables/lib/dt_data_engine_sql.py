from .dtable_data import DTableData
from dtables.models import Base, Users, Columns
from ..helpers import *


class DTDataEngineSQL:
    """A singleton instance of this class is responsible for getting and setting the schema for
       user generated tables. 
       Adding, Removing, Altering Columns
       """
    def __init__(self):
        pass

    def set_schema(self, dtable):
        t = self.get_alchemy_table(dtable)
        if not t.exists():
            self.gen_table(dtable.internal_name)
        else:
            if 'add_column' in dtable.modifications:
                dt_column = dtable.modifications['add_column']
                self.add_column(dtable, dt_column)
            if 'delete_column' in dtable.modifications:
                column_id = dtable.modifications['delete_column'][0]
                column_type = dtable.modifications['delete_column'][1]
                self.delete_column(dtable, column_id, column_type)
            if 'delete_table' in dtable.modifications:
                table = self.get_alchemy_table(dtable)
                if table.exists():
                    table.drop()
            dtable.modifications = {}

    def add_column(self, dtable, dt_column):
        table_id = dt_column.table_id
        name = dt_column.name
        column_type = dt_column.db_data_type

        # query the db for the id of newly created column
        id = session.query(Columns).filter_by(table_id=table_id).filter_by(name=name).one().id
        # db column name in user defined table
        col_name = "col_{}".format(id)

        table = self.get_alchemy_table(dtable)
        col = sqlalchemy.Column(col_name, getattr(sa_types, column_type))
        col.create(table, populate_default=True)

    # Delete a column from the dynamically generated table
    def delete_column(self, dtable, column_id, column_type):
        column_name = "col_{}".format(column_id)
        table = self.get_alchemy_table(dtable, autoload=True)
        col = sqlalchemy.Column(column_name, getattr(sa_types, column_type))
        col.drop(table)

    # set up foreign key relationship here ?
    # Add a new table to the db
    def gen_table(self, internal_name):
        table = Table(internal_name, metadata, Column('id', Integer, primary_key=True))
        metadata.create_all()

    def get_row(self, dtable, id):
        table = self.get_alchemy_table(dtable)
        if table.exists():
            table = self.get_alchemy_table(dtable, autoload=True)
            if session.query(table).filter_by(id=id).count():
                dt_row = session.query(table).filter_by(id=id).one()
                return dt_row

    def list_rows(self, dtable):
        dt_rows = []
        table = self.get_alchemy_table(dtable)
        if table.exists():
            table = self.get_alchemy_table(dtable, autoload=True)
            dt_rows = session.query(table).order_by('id').all()
        return dt_rows

    def add_row(self, dtable, data):
        table = self.get_alchemy_table(dtable, autoload=True)
        insert = table.insert().values(data)
        conn = engine.connect().execute(insert)
        conn.close()

    def update_row(self, dtable, row_id, data):
        table = self.get_alchemy_table(dtable, autoload=True)
        session.query(table).filter_by(id=row_id).update(data, synchronize_session=False)
        session.commit()

    def delete_row(self, dtable, row_id):
        table = self.get_alchemy_table(dtable, autoload=True)
        delete_st = table.delete().where(table.c.id == row_id)
        conn = engine.connect().execute(delete_st)
        conn.close()

    def get_alchemy_table(self, dtable, autoload=False):
        if autoload:
            return Table(dtable.internal_name, sqlalchemy.MetaData(bind=engine), autoload=True)
        else:
            return Table(dtable.internal_name, sqlalchemy.MetaData(bind=engine))

    # need a function to return a dtable_data.py
    def get_data_handle(self, dtable_instance):
        return DTableData(dtable_instance, self)