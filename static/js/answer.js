var answers = new Vue({
    el: '#answers',
    data: {
        date: new Date(),
        user_name: '',
        page_index: 0,
        wait: 0,
        header: {title: '', content: ''},
        items: [],  // {a_id: int, content: str, likes: int, user_name: str}
        message: '',
    },
    methods: {
        get_header: function() {
            answers.wait = 1;
            axios({
                method: 'get',
                url: '/get_header'
            }).then(function(response) {
                answers.header = response.data;
                answers.wait = 0;
            })
        },
        get_answers: function() {
            answers.wait = 1;
            axios({
                method: 'post',
                url: '/get_answers',
                data: {
                    page_index: answers.page_index
                }
            }).then(function(response) {
                answers.items = response.data;
                answers.wait = 0;
            })
        },
        get_user_name: function() {
            answers.wait = 1;
            axios({
                method: 'get',
                url: '/get_user_name'
            }).then(function(response) {
                answers.user_name = response.data.user_name;
                answers.wait = 0;
            })
        },
        next_page: function() {
            if (answers.wait === 0) {
                if (answers.items.length > 0) {
                    answers.page_index += 1;
                    answers.get_answers();
                }
            }
        },
        previous_page: function() {
            if (answers.wait === 0) {
                if (answers.page_index > 0) {
                    answers.page_index -= 1;
                    answers.get_answers();
                }
            }
        },
        submit: function() {
            if (answers.wait === 0) {
                answers.wait = 1
                axios({
                    method: 'post',
                    url: '/submit_answer',
                    data: {
                        message: answers.message
                    }
                }).then(function(response) {
                    if (response.data === true) {
                        answers.get_answers();
                    }
                    else {
                        window.alert('submit failed');
                    }
                })
                answers.message = '';
            }
        }
    }
})

answers.get_header();
answers.get_answers();
answers.get_user_name();
