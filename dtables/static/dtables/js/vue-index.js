/**
 * Created by dyl on 5/4/17.
 */

var Table = function(id, name, columns, rows) {
    this.id = id
    this.name = name
    this.columns = columns
    this.rows = rows
}

var Row = function(id, values) {
    this.id = id
    this.values = values
    this.new_row_values = []
    for (i in this.values) {
        this.new_row_values.push("");
    }
}

var table = new Vue({
    el: '#table',
    data: {
        tables: [],
        currentTable: '',
        collapsed: true,
        table_view: false
    },
    methods: {
        test: function(object, event) {
            console.log(object);
        },
        testAdd: function(event) {
            var self = this;
            $( "td > #entry" ).each(function() {
                console.log( $( this ).val(), $(this).attr("name") );
            });
        },
        populateTable: function () {
            var self = this;
            url = '/dtables/get_tables/';

            $.get(url, data => {
                data.tables.forEach(table => {
                    rows = [];
                    table.rows.forEach(function(row) {
                        row_id = row['id']
                        delete row['id']
                        rows.push(new Row(row_id, row))
                    });
                    self.tables.push(new Table(table.id, table.table_name, table.columns, rows));
                })
            }).fail( err => {
                console.log(err);
            })
        },
        selectTable: function(table, event) {
            var self = this;
            self.currentTable = table;
            self.table_view = true;
        },
        addTable: function(event) {
            var self = this;
            event.preventDefault();
            url = '/dtables/add_table/';
            table_name = $("#table_name").val();
            data = { 'table_name': table_name };

            $.post(url, data)
                .done( res => {
                    console.log(res)
                    self.tables.push({
                        'id': res.id,
                        'name': res.table_name
                    });
                    console.log("tables: " + self.tables)
                }).fail( err => {
                    console.log(err);
                });
        },
        deleteTable: function(event) {
            var self = this;
            id = $(event.target).closest("form").find("#id").val();
            data = {'id': id}
            url = '/dtables/delete_table/'
            $.post(url, data)
                .done( res => {
                    id = parseInt(id);
                    var index = self.tables.findIndex(x => x.id == id);
                    self.tables.splice(index, 1);
                }).fail( err => {
                    console.log(err);
                });
        },
        updateTable: function(event) {
            var self = this;
            event.preventDefault();
            id = $(event.target).closest("form").find("#id").val();
            table_name = $(event.target).closest("form").find("#table-name").val();
            data = {'id': id, 'table-name': table_name }
            url = '/dtables/update_table/'
            $.post(url, data)
                .done( res => {
                    id = parseInt(id);
                    var index = self.tables.findIndex(x => x.id == id);
                    self.tables[index]['name'] = res.name;
                }).fail( err => {
                    console.log(err);
                })
        }
    },
    beforeMount: function () {
        this.populateTable();
    }

});

