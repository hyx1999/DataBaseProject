var questions = new Vue({
    el: '#questions',
    data: {
        date: new Date(),
        user_name: '',
        wait: 0,
        page_index: 0,
        items: []  // {q_id: int, user_name: str, title: str, content: str}
    },
    methods: {
        get_questions: function() {
            questions.wait = 1;
            axios({
                method: 'post',
                url: '/get_questions',
                data: {
                    page_index: questions.page_index
                }
            }).then(function(response) {
                questions.wait = 0;
                questions.items = response.data;
            })            
        },
        get_user_name: function() {
            questions.wait = 1;
            axios({
                method: 'get',
                url: '/get_user_name'
            }).then(function(response) {
                questions.wait = 0;
                questions.user_name = response.data.user_name;
            })
        },
        next_page: function() {
            if (questions.wait === 0) {
                if (questions.items.length > 0) {
                    questions.page_index += 1;
                    questions.get_questions();
                }
            }
        },
        previous_page: function() {
            if (questions.wait === 0) {
                if (questions.page_index > 0) {
                    questions.page_index -= 1;
                    questions.get_questions();
                }
            }
        }
    }
})

questions.get_questions()
questions.get_user_name()
