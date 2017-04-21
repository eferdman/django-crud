from django.shortcuts import render, HttpResponseRedirect
from dtables.models import Base, Users, Columns
from .helpers import *
from .lib.dt_schema_store_sql import DTSchemaStoreSQL
from .lib.dtable import DTable
from .lib.dtcolumn import DTColumn
from .lib.dt_data_engine_sql import DTDataEngineSQL
import migrate.changeset

engine = sqlalchemy.create_engine('postgresql+psycopg2://liz:welcometodyl@localhost:5432/dyldb')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
metadata = sqlalchemy.MetaData(bind=engine)

# sqlstore 'Singleton' will get/set schema definition
sqlstore = DTSchemaStoreSQL()

# datastore 'Singleton' will get/set schema and data for user gen tables
datastore = DTDataEngineSQL()


def index(request):
    # get the DTable object for the Users table
    schema = sqlstore.get_schema('users')
    data = schema.get_data()

    # add a column to the current DTable
    # schema.add_column(DTColumn('name', 'text'))

    # update both the schema and the user generated table
    # sqlstore.set_schema(12342, schema)
    # datastore.set_schema(12342, schema)

    # users = session.query(Users).order_by(Users.id)
    if request.GET.get("edit_columns"):
        id = request.GET.get('id', '')
        return HttpResponseRedirect('/dtables/columns/{}'.format(id))

    context = {'users': data}
    print(data)
    return render(request, 'dtables/index.html', context)


def edit_columns(request, table_id):
    # get the DTable object for the Columns Table
    schema = sqlstore.get_schema('columns')
    data = schema.get_data(table_id)
    print(data)

    context = {'table': data}
    return render(request, 'dtables/edit-columns_interactions.html', context)

def table_view(request, table_id):
    pass