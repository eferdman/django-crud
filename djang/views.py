from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import sqlalchemy.orm
from sqlalchemy import inspect, select, Table, Column, Integer, String, Unicode, MetaData, create_engine
from djang.models import Base, Users, Columns
from .helpers import *
import migrate.changeset


def index(request):
    if request.method == 'POST':
        user = request.POST.get('user_name', '')
        table_name = request.POST.get('table_name', '')
        new_user = Users(name=user, table_name=table_name)
        insert(new_user)

        # dynamically create the table one time
        generate_table(new_user.id)

        return HttpResponseRedirect('/djang')
    else:
        users = session.query(Users).all()
        context = {'users': users}
        return render(request, 'djang/index.html', context)


def edit_columns(request, table_id):
    table_name = 'table_{}'.format(table_id)
    columns = session.query(Columns).filter_by(table_id=table_id)
    print("edit_columns -- Rows in Columns:")
    for col in columns:
        print(col)
    if request.method == 'POST':
        if request.POST.get("add_column"):
            name = request.POST.get('name', '')
            type = request.POST.get('type', '')
            sequence = request.POST.get('sequence', '')

            # insert a row into the Columns table
            # TODO: check for duplicates
            new_column = Columns(table_id=table_id, name=name, type=type, sequence=sequence)
            insert(new_column)

            # add column to dynamically generated table
            add_column(table_name, name)

            return redirect('/djang/columns/{}'.format(table_id))
        elif request.POST.get("delete_column"):
            name = request.POST.get('col_to_delete', '')

            # delete row from Columns table
            old_column = session.query(Columns).filter_by(name=name).filter_by(table_id=table_id).one()
            delete(old_column)

            # delete corresponding column from dynamically generated table
            delete_column(table_name, name)

            return redirect('/djang/columns/{}'.format(table_id))
        elif request.POST.get("view_table"):
            return HttpResponseRedirect('/djang/table/{}'.format(table_id))
    else:
        # recreate columns object?
        context = {'columns': columns}
        return render(request, 'djang/columns.html', context)


def table_view(request, table_id):
    print("def table_view")
    columns = session.query(Columns).filter_by(table_id=table_id)
    print("table_view -- Rows in Columns:")
    for col in columns:
        print(col)
    table_name = 'table_{}'.format(table_id)
    table = Table(table_name, metadata, autoload=True)
    table_values = {}
    if request.method == 'POST':
        # insert new rows into user defined table
        # based on the rows in columns table
        if request.POST.get("add_row"):
            for column in columns:
                table_values[column.name] = request.POST.get(column.name)
            print("Table Values: {}".format(table_values))
            del_st = table.delete().where(table.c.name)
            conn = engine.connect()
            conn.execute(del_st)

            return redirect('/djang/table/{}'.format(table_id))
        # TODO: implement delete row, add button in view
        if request.POST.get("delete_row"):
            name = request.POST.get('row_to_delete', '')
            conn = engine.connect()
            delete_st = table.delete().where(table.c.name == name)
            conn.execute(delete_st)
            conn.close()
    else:
        # query the table -- not working for dynamically generated table
        # rows = session.query(table_name).all()

        table = {}

        inspector = inspect(engine)
        table_columns = [c for c in inspector.get_columns(table_name)]
        print("Inspector Columns: {}".format(table_columns))
        table['columns'] = [c['name'] for c in inspector.get_columns(table_name)]
        table['rows'] = get_rows(table_name)

        context = {'table': table}
        return render(request, 'djang/table.html', context)


# long way to query rows from the dynamically generated table
def get_rows(table_name):
    # pass in fresh MetaData() instance
    user_table = Table(table_name, MetaData(), autoload=True, autoload_with=engine)
    select_st = select([user_table])
    conn = engine.connect()
    res = conn.execute(select_st)
    conn.close()
    return res


def generate_table(table_id):
    class Dtable:
        pass

    table_name = 'table_{}'.format(table_id)

    # create table with only id column
    t = Table(table_name, metadata,
              Column('id', Integer, primary_key=True, autoload=True))
    # *(Column(col.name, String) for col in columns), extend_existing=True, autoload=True)
    metadata.create_all()
    mapper(Dtable, t)

# Add a column to the dynamically generated table
def add_column(table_name, column_name):
    table = Table(table_name, metadata)
    col = sqlalchemy.Column(column_name, String, default="default")
    col.create(table, populate_default=True)


# Delete a column from the dynamically generated table
def delete_column(table_name, column_name):
    table = Table(table_name, metadata)
    col = sqlalchemy.Column(column_name, String)
    col.drop(table)