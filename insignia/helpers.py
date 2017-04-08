import sqlalchemy
from sqlalchemy.orm import sessionmaker, mapper, Session
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