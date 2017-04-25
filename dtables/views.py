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

sqlstore = DTSchemaStoreSQL()
datastore = DTDataEngineSQL()


def index(request):
    if request.method == 'POST':
        # user creates a new table
        if request.POST.get('create_table'):
            user = "DefaultUser"
            table_name = request.POST.get('table_name', '')

            new_table = sqlstore.gen_table(user, table_name)
            datastore.set_schema(new_table)
            return render(request, 'dtables/index.html', context)
    else:
        if request.GET.get("edit_columns"):
            id = request.GET.get('id', '')
            return HttpResponseRedirect('/dtables/columns/{}'.format(id))

        users = session.query(Users).order_by(Users.id)
        context = {'users': users}
        return render(request, 'dtables/index.html', context)


def edit_columns(request, table_id):
    # redirect to table editing view
    if request.GET.get("back_to_table"):
        return HttpResponseRedirect('/dtables/table/{}'.format(table_id))

    columns = session.query(Columns).filter_by(table_id=table_id).order_by(Columns.id).all()
    context = {'table': columns}
    return render(request, 'dtables/edit-columns_interactions.html', context)


def table_view(request, table_id):
    table = sqlstore.get_schema(table_id)
    context = {'table': table}
    return render(request, 'dtables/table-edit.html', context)