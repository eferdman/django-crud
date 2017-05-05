/**
 * Created by dyl on 5/4/17.
 */
var table = new Vue({
    el: '#table',
    data: {
        users: []
    },
    methods: {
        populateTable: function () {
            var self = this;
            self.message = "blah";
            $.ajax({
                url: '/dtables/test/',
                dataType: 'json',
                success: function (data) {
                    users = data.users;
                    users.forEach(function (user) {
                        console.log(user);
                        self.users.push({
                            'id': user.id,
                            'name': user.table_name
                        })
                    });

                },
                error: function (err) {
                    console.log("Error")
                    console.log(err);
                }
            });
        }
    },
    beforeMount: function () {
        this.populateTable();
    }
});

Vue.component('mycomponent', {
    props: ['user'],
    template: '<li>{{ user.name }}</li>'
});
