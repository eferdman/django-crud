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
            dt_columns.append(DTColumn(column.id, column.name, column.type))

        internal_name = "table_{}".format(table_id)
        table_name = columns[0].user.table_name

        return DTable(table_id, internal_name, table_name, dt_columns)

    def set_schema(self, table):
        pass

    def gen_table(self, user, table_name):
        new_user = Users(name=user, table_name=table_name)
        session.add(new_user)
        session.commit()

        internal_name = "table_{}".format(new_user.id)
        return DTable(new_user.id, internal_name, table_name, [])

    def get_tables(self):
        pass