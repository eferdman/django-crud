from sqlalchemy import Table, Column, DefaultClause
from ..helpers import *
from .dtable_data import DTableData
from dtables.models import Base, Users, Columns

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
            if 'delete_table' in dtable.modifications:
                table = self.get_alchemy_table(dtable)
                if table.exists():
                    table.drop()

    def add_column(self, dtable, dt_column):
        table_id = dt_column.table_id
        name = dt_column.name
        column_type = dt_column.db_data_type

        # query the db for the id of newly created column
        id = session.query(Columns).filter_by(table_id=table_id).filter_by(name=name).one().id
        # db column name in user defined table
        col_name = "col_{}".format(id)

        # add column to dynamically generated table
        add_column(dtable.internal_name, col_name, column_type)

    # set up foreign key relationship here ?
    # Add a new table to the db
    def gen_table(self, internal_name):
        table = Table(internal_name, metadata, Column('id', Integer, primary_key=True))
        metadata.create_all()

    def get_row(self, dtable, id):
        table = self.get_alchemy_table(dtable)
        if table.exists():
            if session.query(table).filter_by(id=id).count():
                dt_row = session.query(table).filter_by(id=id).one()
                return dt_row

    def list_rows(self, dtable):
        dt_rows = []
        table = self.get_alchemy_table(dtable)
        if table.exists():
            dt_rows = session.query(table).all()
        return dt_rows

    def get_alchemy_table(self, dtable, autoload=False):
        if autoload:
            return Table(dtable.internal_name, sqlalchemy.MetaData(bind=engine), autoload=True)
        else:
            return Table(dtable.internal_name, sqlalchemy.MetaData(bind=engine))

    # need a function to return a dtable_data.py
    def get_data_handle(self, dtable_instance):
        return DTableData(dtable_instance, self)