from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import sqlalchemy, sqlalchemy.orm
from sqlalchemy.orm import sessionmaker
from djang.models import Base, Users, Columns

engine = sqlalchemy.create_engine('postgresql://liz:welcometodyl@localhost:5432/dyldb')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

def is_empty(table):
	return len(session.query(table).all()) == 0
 
def populate(data):
	session.add_all(data)
	session.commit()

def insert(row):
	session.add(row)
	session.commit()

def delete(row):
	session.delete(row)
	session.commit()

def get_row(table, id):
	return session.query(table).filter_by(id=id).first()

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

def edit_columns(request, table_id):
	if request.method == 'POST':
		name = request.POST.get('name', '')
		type = request.POST.get('type', '')
		sequence = request.POST.get('sequence', '')
		
		# can we use relationship to create a new column instead of explicitly using table_id?
		# user = session.query(Users).filter_by(id=table_id).one()
		
		new_column = Columns(table_id=table_id, name=name, type=type, sequence=sequence)
		insert(new_column)
		return HttpResponseRedirect('djang/columns/' + table_id)
	else:
		columns = session.query(Columns).all()
		context = {'columns': columns}
		return render(request, 'djang/columns.html', context)
