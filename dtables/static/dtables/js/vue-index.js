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
            $.ajax({
                url: '/dtables/get_tables/',
                dataType: 'json',
                success: function (data) {
                    users = data.users;
                    users.forEach(function (user) {
                        self.users.push({
                            'id': user.id,
                            'name': user.table_name
                        })
                    });

                },
                error: function (err) {
                    console.log(err);
                }
            });
        },
        addTable: function(event) {
            var self = this;
            // use $(event.target) to grab the element
            // that was clicked on
            table_name = $("#table_name").val();
            data = { 'table_name': table_name };
            $.ajax({
                url: '/dtables/add_table/',
                dataType: 'json',
                type: "POST",
                data: data,
                success: function(res) {
                    console.log(res)
                    self.users.push({
                        'id': res.id, 
                        'name': res.table_name
                    })
                },
                error: function(err) {
                    console.log(err);
                }
            })
        },
        deleteTable: function(event) {
            var self = this;
            id = $(event.target).siblings("input").val();
            data = {'id': id}
            $.ajax({
                url: '/dtables/delete_table/',
                dataType: 'json',
                type: "POST",
                data: data,
                success: function(response) {
                    var id = parseInt(id)
                    var index = self.users.findIndex(x => x.id == id);
                    self.users.splice(index);
                },
                error: function(err) {
                    console.log(err);
                }
            });
        }
    },
    beforeMount: function () {
        this.populateTable();
    }
});