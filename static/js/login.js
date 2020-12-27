var formSignIn = new Vue({
    el: '#form-signin',
    data: {
        userName: '',
        password: ''
    },
    methods: {
        signin: function() {
            axios({
                method: 'post',
                url: '/login',
                data: {
                    userName: this.userName,
                    password: this.password
                }
            }).then(function(response) {
                if (response.data.logged_in === true) {
                    location.href = "index";
                }
                else {
                    alert("用户名密码错误");
                }
            })
        }
    }
})
