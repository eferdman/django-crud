/**
 * Created by dyl on 5/4/17.
 */
var table = new Vue({
    el: '#table',
    data: {
        users: [],
        collapsed: true
    },
    methods: {
        populateTable: function () {
            var self = this;
            url = '/dtables/get_tables/';
            $.get(url, function(data) {
                users = data.users;
                users.forEach(function (user) {
                    self.users.push({
                        'id': user.id,
                        'name': user.table_name
                    })
                });
            }).fail(function(err) {
                console.log(err);
            });
        },
        addTable: function(event) {
            var self = this;
            event.preventDefault();
            url = '/dtables/add_table/';
            table_name = $("#table_name").val();
            data = { 'table_name': table_name };

            $.post(url, data)
                .done(function( res ) {
                    console.log(res)
                    self.users.push({
                        'id': res.id,
                        'name': res.table_name
                    });
                    console.log("tables: " + self.users)
                }).fail(function( err ) {
                    console.log(err);
                });
        },
        deleteTable: function(event) {
            var self = this;
            id = $(event.target).closest("form").find("#id").val();
            data = {'id': id}
            url = '/dtables/delete_table/'
            $.post(url, data)
                .done( function( res ) {
                    id = parseInt(id);
                    var index = self.users.findIndex(x => x.id == id);
                    self.users.splice(index, 1);
                }).fail(function( err ) {
                    console.log(err);
                });
        }
    },
    beforeMount: function () {
        this.populateTable();
    }
});