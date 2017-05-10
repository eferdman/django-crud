/**
 * Created by dyl on 5/4/17.
 */
var table = new Vue({
    el: '#table',
    data: {
        tables: [],
        currentTable: '',
        collapsed: true
    },
    methods: {
        populateTable: function () {
            var self = this;
            url = '/dtables/get_tables/';
            $.get(url, data => {
                tables = data.tables;
                tables.forEach(table =>
                    self.tables.push({
                        'id': table.id,
                        'name': table.table_name,
                        'columns' : table.columns
                    })
                )
            }).fail( err => {
                console.log(err);
            })
        },
        selectTable: function(table, event) {
            var self = this;
            self.currentTable = table
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

