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
