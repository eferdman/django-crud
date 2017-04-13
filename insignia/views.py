from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
import sqlalchemy.orm
from sqlalchemy import inspect, select, Table, Column, Integer, String, Unicode, MetaData, create_engine
from insignia.models import Base, Users, Columns
from .helpers import *
import migrate.changeset


def index(request):
    if request.method == 'POST':
        if request.POST.get('create_table'):
            user = "DefaultUser"
            table_name = request.POST.get('table_name', '')
            new_user = Users(name=user, table_name=table_name)
            insert(new_user)

            # dynamically create the table
            generate_table(new_user.id)
        elif request.POST.get('delete_row'):
            id = request.POST.get('id', '')
            row_to_delete = session.query(Users).filter_by(id=id).one()
            delete(row_to_delete)

            # delete the corresponding table
            table_name = "table_{}".format(id)
            table = Table(table_name, metadata)
            if table.exists():
                table.drop()
        elif request.POST.get('update_row'):
            id = request.POST.get('id', '')
            row_to_update = session.query(Users).filter_by(id=id).one()
            row_to_update.table_name = "NewerTable"
            session.commit()
        return HttpResponseRedirect('/insignia')
    else:
        if request.GET.get("edit_columns"):
            id = request.GET.get('id', '')
            return HttpResponseRedirect('/insignia/columns/{}'.format(id))
        elif request.GET.get("edit_data"):
            id = request.GET.get('id', '')
            return HttpResponseRedirect('/insignia/table/{}'.format(id))
        else:
            users = session.query(Users).all()
            context = {'users': users}
            return render(request, 'insignia/index.html', context)


def validate(request):
    if request.is_ajax():
        user = request.POST.get('ajax_username', None)
        data = {'is_taken': True}
        return JsonResponse(data)


def edit_columns(request, table_id):
    table_name = 'table_{}'.format(table_id)
    table = {}
    table['columns'] = session.query(Columns).filter_by(table_id=table_id)
    table['table_name'] = session.query(Users).filter_by(id=table_id).one().table_name
    print("edit_columns -- Rows in Columns:")
    for col in table['columns']:
        print(col)
    if request.method == 'POST':
        if request.POST.get("add_column"):
            name = request.POST.get('name', '')
            type = "String"
            sequence = "5"

            # check if that column already exists:
            inspector = inspect(engine)
            column_names = [c['name'] for c in inspector.get_columns(table_name)]
            if name not in column_names:
                # insert a row into the Columns table
                new_column = Columns(table_id=table_id, name=name, type=type, sequence=sequence)
                insert(new_column)

                # add column to dynamically generated table
                add_column(table_name, name)
            return redirect('/insignia/columns/{}'.format(table_id))
        elif request.POST.get("delete_column"):
            id = request.POST.get('column_id', '')

            # delete row from Columns table
            old_column = session.query(Columns).filter_by(id=id).one()
            delete(old_column)

            # delete corresponding column from dynamically generated table
            delete_column(table_name, old_column.name)

            return redirect('/insignia/columns/{}'.format(table_id))
        elif request.POST.get("view_table"):
            return HttpResponseRedirect('/insignia/table/{}'.format(table_id))
    else:
        if request.GET.get("back_to_table"):
            return redirect('/insignia/table/{}'.format(table_id))
        else:
            context = {'table': table}
            return render(request, 'insignia/edit-columns_interactions.html', context)


def table_view(request, table_id):
    print("def table_view")
    columns = session.query(Columns).filter_by(table_id=table_id)
    print("table_view -- Rows in Columns:")
    for col in columns:
        print(col)
    table_name = 'table_{}'.format(table_id)
    table = Table(table_name, MetaData(bind=engine), autoload=True)
    table_values = {}
    if request.method == 'POST':
        # insert new rows into user defined table
        if request.POST.get("add_row"):
            for column in columns:
                table_values[column.name] = request.POST.get(column.name, '')
            print("Table Values: {}".format(table_values))
            ins = table.insert().values(table_values)
            conn = engine.connect()
            conn.execute(ins)
            conn.close()
        elif request.POST.get("delete_row"):
            row_id = request.POST.get('row_id', '')
            print("The Row ID is {}".format(row_id))
            conn = engine.connect()
            delete_st = table.delete().where(table.c.id == row_id)
            conn.execute(delete_st)
            conn.close()

        return redirect('/insignia/table/{}'.format(table_id))
    else:
        if request.GET.get("back_to_columns"):
            return HttpResponseRedirect('/insignia/columns/{}'.format(table_id))
        else:
            table = {}
            table['name'] = session.query(Users).filter_by(id=table_id).one().table_name

            inspector = inspect(engine)
            table_columns = [c for c in inspector.get_columns(table_name)]
            print("Inspector Columns: {}".format(table_columns))
            table['columns'] = [c['name'] for c in inspector.get_columns(table_name)]

            # pass in fresh metadata instance, make sure to bind to engine
            user_table = Table(table_name, MetaData(bind=engine), autoload=True)
            table['rows'] = session.query(user_table).all()

            context = {'table': table}
            return render(request, 'insignia/table-edit.html', context)