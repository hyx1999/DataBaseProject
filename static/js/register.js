var formRegister = new Vue({
    el: '#form-register',
    data: {
        userName: '',
        password: '',
        confirmPassword: ''
    },
    methods: {
        register: function() {
            console.log('Hello World!');
            if (this.password != this.confirmPassword) {
                alert('密码与确认密码不一致!');
                return;
            }
            axios({
                method: 'post',
                url: '/register',
                data: {
                    userName: this.userName,
                    password: this.password
                }
            }).then(function(response) {
                console.log(response);
                if (response.data.register_success == true) {
                    location.href = "login_page";
                }
                else {
                    alert("注册失败");
                }
            })
        }
    }
})
