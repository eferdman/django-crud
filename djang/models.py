from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Users(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	table_name = Column(String)

	def __init__(self, name, table_name):
		self.name = name
		self.table_name = table_name

	def __repr__(self):
		return "<Users {} {}>".format(self.name, self.table_name)

class Columns(Base):
	__tablename__ = 'columns'
	id = Column(Integer, primary_key=True)
	table_id = Column(Integer, ForeignKey('users.id'))
	name = Column(String)
	type = Column(String)
	sequence = Column(Integer)

	user = relationship('Users', backref=backref('cars', lazy='dynamic'))
	
	def __init__(self, table_id, name, type, sequence):
		self.table_id = table_id
		self.name = name
		self.type = type
		self.sequence = sequence

	def __repr__(self):
		return "<Columns {} {} {} {}>".format(self.name, self.table_id, self.type, self.sequence)
