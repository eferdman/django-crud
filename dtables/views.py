from django.shortcuts import render, HttpResponseRedirect
from dtables.models import Base, Users, Columns
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from .lib.dt_schema_store_sql import DTSchemaStoreSQL
from .lib.dtcolumn import DTColumn
from .lib.dt_data_engine_sql import DTDataEngineSQL
from django.http import JsonResponse
import json
import migrate.changeset

engine = sqlalchemy.create_engine('postgresql+psycopg2://liz:welcometodyl@localhost:5432/dyldb')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
metadata = sqlalchemy.MetaData(bind=engine)

sqlstore = DTSchemaStoreSQL(session, metadata)
datastore = DTDataEngineSQL(engine, session, metadata)


def test(request):
    return render(request, 'dtables/vue-index.html')

def index(request):
    print("Django Rendering page")
    return render(request, 'dtables/index.html')


def update_table(request):
    updated_name = request.POST['table-name']
    id = int(request.POST['id'])

    table = sqlstore.get_schema(table_name=updated_name, table_id=id)
    table.update_name(updated_name)
    sqlstore.set_schema(table)
    return JsonResponse({'id': id, 'name': updated_name})


def delete_table(request):
    print(request.POST['id'])
    id = int(request.POST['id'])

    table = sqlstore.get_schema(table_name=None, table_id=id)
    table.delete()
    sqlstore.set_schema(table)
    datastore.set_schema(table)
    return JsonResponse({'id': id})


def add_table(request):
    table_name = request.POST['table_name']

    new_table = sqlstore.get_schema(table_name)
    sqlstore.set_schema(new_table)
    datastore.set_schema(new_table)

    data = {}
    data['id'] = new_table.table_id
    data['table_name'] = new_table.table_name
    return JsonResponse(data)


def get_tables(request):
    tables = session.query(Users).order_by(Users.id).all()
    context = {'tables': tables}
    json = {}
    json['tables'] = []
    for table in tables:
        obj = {}
        obj['id'] = table.id
        obj['table_name'] = table.table_name
        sql_columns = session.query(Columns). \
            filter_by(table_id=table.id). \
            order_by(Columns.sequence). \
            all()
        obj['columns'] = []
        for column in sql_columns:
            obj['columns'].append({
                'id': column.id,
                'name': column.name,
                'type': column.type,
                'sequence': column.sequence
            })
        json['tables'].append(obj)

    return JsonResponse(json)


def edit_columns(request, table_id):
    if request.method == 'POST':
        if request.POST.get("add_column"):
            columns = session.query(Columns). \
                filter_by(table_id=table_id). \
                order_by(Columns.sequence). \
                all()
            column_names = [c.name for c in columns]
            data_types = {
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
            name = request.POST.get('name', '')            # user defined name of column
            data_type = request.POST.get('data_type', '')  # user level data type
            db_data_type = data_types[data_type]           # db level data type

            # check if that column already exists before adding:
            if name not in column_names:
                schema = sqlstore.get_schema(None, table_id)
                schema.add_column(DTColumn(None, table_id, name, data_type, db_data_type))
                sqlstore.set_schema(schema)
                datastore.set_schema(schema)
        elif request.POST.get("delete_column"):
            column_id = request.POST.get('column_id', '')
            schema = sqlstore.get_schema(None, table_id)
            column_type = session.query(Columns).filter_by(id=column_id).one().type
            schema.delete_column(column_id, column_type)
            sqlstore.set_schema(schema)
            datastore.set_schema(schema)
        elif request.POST.get("update_column_name"):
            if request.POST.get('updated_value'):
                updated_name = request.POST.get('updated_value', '')
                column_id = request.POST.get('id', '')

                table = sqlstore.get_schema(table_name=None, table_id=table_id)
                table.update_column_name(column_id, updated_name)
                sqlstore.set_schema(table)
        elif request.POST.get("update_column_seq"):
            if request.POST.get("updated_value"):
                new_sequence = request.POST.get('updated_value', '')
                column_id = request.POST.get('id', '')

                table = sqlstore.get_schema(table_name=None, table_id=table_id)
                table.update_column_sequence(column_id, new_sequence)
                sqlstore.set_schema(table)

    # redirect to table editing view
    if request.GET.get("back_to_table"):
        return HttpResponseRedirect('/dtables/table/{}'.format(table_id))

    columns = session.query(Columns). \
        filter_by(table_id=table_id). \
        order_by(Columns.sequence)
    columns = columns.all()
    column_names = [c.name for c in columns]
    table_name = session.query(Users). \
        filter_by(id=table_id). \
        one().table_name
    table = {
        'columns': columns,
        'column_names': column_names,
        'table_name': table_name,
        'table_id': table_id,
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
    context = {'table': table}
    return render(request, 'dtables/edit-columns.html', context)


def table_view(request, table_id):
    table_name = 'table_{}'.format(table_id)
    dtable = sqlstore.get_schema(table_name, table_id)
    handle = datastore.get_data_handle(dtable)
    rows = handle.list_rows()
    print("Rows in Table: {}".format(rows))
    table = {
        'rows': rows,
        'columns': dtable.columns,
        'table_name': dtable.table_name
    }
    data = {}
    if request.method == 'POST':
        if request.POST.get("add_row"):
            for column in table['columns']:
                col_name = "col_{}".format(column.id)
                data[col_name] = request.POST.get(column.name, '')
            print("Table Values: {}".format(data))
            handle.add_row(dtable, data)
        elif request.POST.get("delete_row"):
            row_id = request.POST.get('row_id', '')
            handle.delete_row(dtable, row_id)
        elif request.POST.get("update_data"):
            if request.POST.get('updated_value'):
                updated_value = request.POST.get('updated_value', '')
                row_id = request.POST.get('id', '')
                index = request.POST.get('entry_index', '')

                row = handle.get_row(row_id)
                column_name = row.keys()[int(index)]
                data = {column_name: updated_value}
                handle.update_row(dtable, row_id, data)

    if request.GET.get("back_to_columns"):
        return HttpResponseRedirect('/dtables/columns/{}'.format(table_id))

    context = {'table': table}
    return render(request, 'dtables/table-edit.html', context)