from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import sqlalchemy, sqlalchemy.orm
from sqlalchemy import select, Table, Column, Integer, String, Unicode, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from djang.models import Base, Users, Columns
from .helpers import *

def index(request):
	if request.method == 'POST':
		user = request.POST.get('user_name', '')
		table_name = request.POST.get('table_name', '')
		new_user = Users(name=user, table_name=table_name)
		insert(new_user)
		return HttpResponseRedirect('/djang')
	else:
		if is_empty(Users):
			populate([Users('Liz', 'Languages')])
		users = session.query(Users).all()
		context = {'users': users}
		return render(request, 'djang/index.html', context)

def generate_table(table_id, columns):
	class Dtable():
		pass

	table_name = 'table_{}'.format(table_id)

	t = Table(table_name, metadata,
		Column('id', Integer, primary_key=True),
		*(Column(col.name, String) for col in columns) )
	metadata.create_all()
	mapper(Dtable, t)

def edit_columns(request, table_id):
	columns = session.query(Columns).filter_by(table_id=table_id)
	if request.method == 'POST':
		if request.POST.get("add_column"):
			name = request.POST.get('name', '')
			type = request.POST.get('type', '')
			sequence = request.POST.get('sequence', '')
			
			new_column = Columns(table_id=table_id, name=name, type=type, sequence=sequence)
			insert(new_column)

			return redirect('/djang/columns/{}'.format(table_id))
		elif request.POST.get("create_table"):
			generate_table(table_id, columns)
			return HttpResponseRedirect('/djang/table/{}'.format(table_id))
	else:
		context = {'columns': columns}
		return render(request, 'djang/columns.html', context)

def table_view(request, table_id):
	columns = session.query(Columns).filter_by(table_id=table_id)
	table_name = 'table_{}'.format(table_id)
	table = Table(table_name, metadata, autoload=True)
	table_values = {}
	if request.method == 'POST':
		# insert new rows into user defined table
		for column in columns:
			table_values[column.name] = request.POST.get(column.name)

		ins = table.insert().values(table_values)
		conn = engine.connect()
		result = conn.execute(ins)

		return redirect('/djang/table/{}'.format(table_id))
	else:
		# postgres bug
		#rows = session.query(table_name).all()

		# long way to query the user generated table
		table = metadata.tables[table_name]
		select_st = select([table])
		conn = engine.connect()
		res = conn.execute(select_st)
		columns.rows = res

		context = { 'columns' : columns }
		return render(request, 'djang/table.html', context)

