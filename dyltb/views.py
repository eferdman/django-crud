from django.shortcuts import render, get_object_or_404
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect
from .models import UserTables, Columns
from django.urls import reverse
from .models import UserTables, Columns

from sqlalchemy import Table, Column, Integer, Unicode, MetaData, create_engine
from sqlalchemy.orm import mapper, create_session

# Create your views here.
def index(request):
    if request.method == 'POST': 
        user_name = request.POST.get('user_name', '')
        table_name = request.POST.get('table_name', '')
        
        # Save a new row in the database
        user_table = UserTables(user_name=user_name, table_name=table_name)
        user_table.save()

        return HttpResponseRedirect('/dyltb')
    else:
        user_tables = UserTables.objects.all()
        context = {'user_tables': user_tables}
        return render(request, 'dyltb/index.html', context)

def edit_columns(request, table_id):
    if request.method == 'POST':
        if request.POST.get("add_column"):
            column_name = request.POST.get('column_name', '')
            column_type = request.POST.get('column_type', '')
            column_sequence = request.POST.get('column_sequence', '')

            # Save a new row in the database
            column = Columns(column_name=column_name,
                column_type=column_type, column_sequence=column_sequence,
                table_id=table_id)
            column.save()
            return HttpResponseRedirect('/dyltb/columns/' + table_id)
    else:
        # Find all rows that have the usertable_id 1
        columns = Columns.objects.filter(table_id=table_id).values()
        columns.table_id = table_id
        context = {'columns': columns}
        return render(request, 'dyltb/columns.html', context)

def create_table(request, table_id):
    columns = Columns.objects.filter(table_id=table_id).values()
    column_names = [col['column_name'] for col in columns]
    table_name = UserTables.objects.filter(pk=table_id).values()[0]['table_name']
    print("Table Name is: " + table_name)
    
    #TODO: Insert rows into table 
    if request.method == 'POST':
        q = session.query(table_name)
        print(q)
        #ins = q.insert().values(*("'{}'=request.POST.get('{}', '')".format(name) for name in column_names)
    else:
        class Dtable():
            pass
        # get the fields of Columns table
        fields = [field.name for field in Columns._meta.get_fields() if not field.is_relation]
        print(fields)
        engine = create_engine('postgresql://liz:welcometodyl@localhost:5432/dyldb')
        metadata = MetaData(bind=engine)
        
        # the rows in the Columns table which will be the new columns
        columns = Columns.objects.filter(table_id=table_id).values()
        column_names = [col['column_name'] for col in columns]
        print(column_names)
        columns.column_names = column_names

        # Create the table schema
        t = Table(table_name, metadata, 
            Column('id', Integer, primary_key=True), *(Column(col['column_name'], Unicode(255)) for col in columns))
        metadata.create_all()
        mapper(Dtable, t)
        session = create_session(bind=engine, autocommit=False)

        context = {'columns': columns}

        #create a context
        return render(request, 'dyltb/table.html', context)