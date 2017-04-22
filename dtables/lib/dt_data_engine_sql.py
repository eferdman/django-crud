from sqlalchemy import Table, Column, DefaultClause
from ..helpers import *


class DTDataEngineSQL:
    """A singleton instance of this class is responsible for getting and setting the schema for
       user generated tables. 
       Adding, Removing, Altering Columns
       """
    def __init__(self):
        pass

    def set_schema(self, dtable):
        if not dtable.exists():
            self.gen_table(dtable.internal_name, dtable.table_id)
        else:
            pass

    # set up foreign key relationship here
    def gen_table(self, internal_name, table_id):
        t = Table(internal_name, metadata,
                  Column('id', Integer, primary_key=True),
                  Column('table_id', Integer, DefaultClause(str(table_id))))
        metadata.create_all()