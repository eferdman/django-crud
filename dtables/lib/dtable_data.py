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

    def list_rows(self, id):
        rows = self.data_engine.list_rows(self.schema)
        return rows