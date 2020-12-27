from flask import Flask, request, session, send_from_directory, json, redirect, url_for
from flask.helpers import make_response
from database import DataBase

app = Flask(__name__)
app.secret_key = '998244353'
db = DataBase()

######################################################################
# 登录
# login, login_page

@app.route('/login', methods=['POST'])
def login():
    user_info = request.json
    try:
        user_name = user_info['userName']
        password = user_info['password']
        if not db.check_user_info(user_name, password):
            response = make_response(json.dumps({"logged_in": False}))
            response.mimetype = "application/json"
            return response
    except:
        response = make_response(json.dumps({"logged_in": False}))
        response.mimetype = "application/json"
        return response
    session['logged_in'] = True
    session['user_name'] = user_name

    response = make_response(json.dumps({"logged_in": True}))
    response.mimetype = "application/json"
    return response


@app.route('/login_page')
def login_page():
    return send_from_directory('static', 'login_page.html')

######################################################################
# 注册
# register, register_page

@app.route('/register', methods=['POST'])
def register():
    user_info = request.json
    try:
        user_name = user_info['userName']
        password = user_info['password']
        register_success = db.register(user_name, password)
        if not register_success:
            response = make_response(json.dumps({"register_success": False}))
            response.mimetype = "application/json"
            return response
    except:
        response = make_response(json.dumps({"register_success": False}))
        response.mimetype = "application/json"
        return response
    session['register_success'] = True

    response = make_response(json.dumps({"register_success": True}))
    response.mimetype = "application/json"
    return response


@app.route('/register_page')
def register_page():
    return send_from_directory('static', 'register_page.html')

######################################################################
# 主页面: 显示提问
# get_questions, get_user_name, index, enter_question

@app.route('/get_questions', methods=['POST'])
def get_questions():
    if 'logged_in' not in session:
        response = make_response(json.dumps([]))
        response.mimetype = "application/json"
        return response
    page_index = request.json['page_index']
    questions = db.get_questions(page_index)
    response = make_response(json.dumps(questions))
    response.mimetype = "application/json"
    return response


@app.route('/get_user_name', methods=['GET'])
def get_user_name():
    if 'logged_in' not in session:
        response = make_response(json.dumps(""))
        response.mimetype = "application/json"
        return response
    response = make_response(json.dumps({'user_name': session['user_name']}))
    response.mimetype = "application/json"
    return response


@app.route('/question/<question_id>')
def enter_question(question_id):
    if 'logged_in' not in session:
        return redirect(url_for('login_page'))
    question_id = int(question_id)
    session['question_id'] = question_id
    return send_from_directory('static', 'answer.html')


@app.route('/')
@app.route('/index')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login_page'))
    return send_from_directory('static', 'index.html')


######################################################################
# 问题页面: 显示回答
# get_answers, get_user_name, get_header, submit_answer

@app.route('/get_answers', methods=['POST'])
def get_answers():
    if 'logged_in' not in session or 'question_id' not in session:
        response = make_response(json.dumps([]))
        response.mimetype = "application/json"
        return response
    question_id = session['question_id']
    page_index = request.json['page_index']
    answers = db.get_answers(question_id, page_index)
    response = make_response(json.dumps(answers))
    response.mimetype = "application/json"
    return response

# get_user_name 同上

@app.route('/get_header', methods=['GET'])
def get_header():
    if 'logged_in' not in session or 'question_id' not in session:
        response = make_response(json.dumps({'title': '', 'content': ''}))
        response.mimetype = "application/json"
        return response
    question_id = session['question_id']
    header = db.get_header(question_id)
    response = make_response(json.dumps(header))
    response.mimetype = "application/json"
    return response


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if 'logged_in' not in session or 'question_id' not in session:
        response = make_response(json.dumps(False))
        response.mimetype = "application/json"
        return response
    question_id = session['question_id']
    user_name = session['user_name']
    message = request.json['message']
    db.submit_answer(question_id, user_name, message)
    response = make_response(json.dumps(True))
    response.mimetype = "application/json"
    return response


######################################################################
# 提问页面

@app.route('/put_question', methods=['POST'])
def put_question():
    if 'logged_in' not in session:
        response = make_response(json.dumps(False))
        response.mimetype = "application/json"
        return response
    user_name = session['user_name']
    message_title = request.json['message_title']
    message_content = request.json['message_content']
    db.put_question(message_title, message_content, user_name)
    response = make_response(json.dumps(True))
    response.mimetype = "application/json"
    return response


@app.route('/put_question_page')
def put_question_page():
    if 'logged_in' not in session:
        return redirect(url_for('login_page'))
    return send_from_directory('static', 'put_question.html')


if __name__ == '__main__':
    app.run(debug=True)
    db.close()
