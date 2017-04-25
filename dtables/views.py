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
            table_name = request.POST.get('table_name', '')

            new_table = sqlstore.get_schema(table_name)
            sqlstore.set_schema(new_table)
            datastore.set_schema(new_table)
        elif request.POST.get('delete_row'):
            id = request.POST.get('id', '')

            table = sqlstore.get_schema(table_name=None, table_id=id)
            table.delete()
            sqlstore.set_schema(table)
            datastore.set_schema(table)
    else:
        if request.GET.get("edit_columns"):
            id = request.GET.get('id', '')
            return HttpResponseRedirect('/dtables/columns/{}'.format(id))
        elif request.GET.get("edit_data"):
            id = request.GET.get('id', '')
            return HttpResponseRedirect('/dtables/table/{}'.format(id))
    users = session.query(Users).order_by(Users.id)
    context = {'users': users}
    return render(request, 'dtables/index.html', context)


def edit_columns(request, table_id):
    columns = session.query(Columns).filter_by(table_id=table_id).order_by(Columns.id).all()
    column_names = [c.name for c in columns]
    table_name = session.query(Users).filter_by(id=table_id).one().table_name
    table = {
        'columns': columns,
        'column_names': column_names,
        'table_name': table_name,
        'data_types': {
            'Text': 'String',
            'Checkbox': 'Boolean',
            'SelectBox': 'BigInteger',
            'Long Text': 'TEXT',
            'Date': 'Date',
            'Currency': 'DECIMAL',
            'Number': 'Float',
            'Timestamp': 'DateTime',
            'Time': 'VARCHAR(5)',
            'Integer': 'BigInteger'
        }
    }
    if request.method == 'POST':
        if request.POST.get("add_column"):
            name = request.POST.get('name', '')            # user defined name of column
            data_type = request.POST.get('data_type', '')  # user level data type
            db_data_type = table['data_types'][data_type]   # db level data type
            sequence = "5"

            # check if that column already exists before adding:
            if name not in column_names:
                schema = sqlstore.get_schema(None, table_id)
                schema.add_column(DTColumn(table_id, name, data_type, db_data_type, sequence))
                sqlstore.set_schema(schema)
                datastore.set_schema(schema)

        return HttpResponseRedirect('/dtables/columns/{}'.format(table_id))
    # redirect to table editing view
    if request.GET.get("back_to_table"):
        return HttpResponseRedirect('/dtables/table/{}'.format(table_id))

    context = {'table': table}
    return render(request, 'dtables/edit-columns_interactions.html', context)

def table_view(request, table_id):
    table = sqlstore.get_schema(None, table_id)
    context = {'table': table}
    return render(request, 'dtables/table-edit.html', context)