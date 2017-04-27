# this is called a handle
# call this class for
class DTableData:
    def __init__(self, schema, data_engine):
        # The Dtable object
        self.schema = schema
        # instance of dt_data_engine
        self.data_engine = data_engine

    # calls method on the data engine
    def get_row(self, id):
        row = self.data_engine.get_row(self.schema, id)
        return row

    def list_rows(self):
        rows = self.data_engine.list_rows(self.schema)
        return rows

    def add_row(self, dtable, data):
        self.data_engine.add_row(dtable, data)

    def update_row(self, dtable, row_id, data):
        self.data_engine.update_row(dtable, row_id, data)

    def delete_row(self, dtable, row_id):
        self.data_engine.delete_row(dtable, row_id)