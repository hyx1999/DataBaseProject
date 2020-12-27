var put_question = new Vue({
    el: '#put_question',
    data: {
        date: new Date(),
        wait: 0,
        message_title: '',
        message_content: ''
    },
    methods: {
        submit: function() {
            if (put_question.wait === 0) {
                put_question.wait = 1;
                axios({
                    method: 'post',
                    url: '/put_question',
                    data: {
                        message_title: put_question.message_title,
                        message_content: put_question.message_content
                    }
                }).then(function(response) {
                    if (response.data === true) {
                        location.href = '/index';
                    }
                    else {
                        window.alert('submit failed')
                    }
                    put_question.wait = 0;
                })
                put_question.message_title = '';
                put_question.message_content = '';
            }
        }
    }
})
