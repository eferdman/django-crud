import sqlalchemy
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, mapper

from djang.models import Base

engine = sqlalchemy.create_engine('postgresql+psycopg2://liz:welcometodyl@localhost:5432/dyldb')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
metadata = sqlalchemy.MetaData(bind=engine)


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


def get_row_by_id(table, id):
	return session.query(table).filter_by(id=id).first()


def get_rows_by_id(table, id):
	return session.query(table).filter_by(id=id)

# long way to query rows from the dynamically generated table
# def get_rows(table_name):
    # pass in fresh MetaData() instance metadatas
    # user_table = Table(table_name, MetaData(), autoload=True, autoload_with=engine)
    # select_st = select([user_table])
    # conn = engine.connect()
    # res = conn.execute(select_st)
    # conn.close()
    # return res

def generate_table(table_id):
    class Dtable:
        pass

    table_name = 'table_{}'.format(table_id)

    # create table with only id column
    t = Table(table_name, metadata,
              Column('id', Integer, primary_key=True))
    # delete autoload = True;
    # *(Column(col.name, String) for col in columns), extend_existing=True, autoload=True)
    metadata.create_all()
    mapper(Dtable, t)


# Add a column to the dynamically generated table
def add_column(table_name, column_name):
    table = Table(table_name, metadata)
    col = sqlalchemy.Column(column_name, String, default="default")
    col.create(table, populate_default=True)
    print("Type of Column: {}".format(type(col)))


# Delete a column from the dynamically generated table
def delete_column(table_name, column_name):
    table = Table(table_name, metadata)
    col = sqlalchemy.Column(column_name, String)
    col.drop(table)