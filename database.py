from mysql import connector
from threading import Lock

myLock = Lock()

def synchronized(lock):
    """ Synchronization decorator. """

    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap

class DataBase(object):
    def __init__(self):
        self.cnx = connector.connect(
            host="localhost",
            user="root",
            password="huyuxuan",
            database="zhihu",
            auth_plugin='mysql_native_password'
        )
        self.QUESTION_ONE_PAGE_MAX_ROWS = 5
        self.ANSWER_ONE_PAGE_MAX_ROWS = 20

    @synchronized(myLock)
    def check_user_info(self, user_name: str, password: str):
        cursor = self.cnx.cursor(buffered=False)
        args = [user_name, 0]
        result = cursor.callproc('check_user_info', args)

        cursor.close()
        if result[1] != password:
            return False
        return True
    
    @synchronized(myLock)
    def register(self, user_name: str, password: str):
        cursor = self.cnx.cursor(buffered=False)
        args = [user_name, password, 0]
        result = cursor.callproc('register', args)

        cursor.close()
        if result[2] != 1:
            return False
        return True
    
    @synchronized(myLock)
    def get_questions(self, page_index: int):
        cursor = self.cnx.cursor(buffered=False)
        cursor.callproc('get_questions')
        cursor.execute('SELECT * FROM temporary_question_table')
        rows = list(cursor.fetchall())
        rows = [{'q_id': a, 'title': b, 'content': c, 'user_name': d} for a, b, c, d in rows]
        rows = rows[page_index * self.QUESTION_ONE_PAGE_MAX_ROWS: (page_index + 1) * self.QUESTION_ONE_PAGE_MAX_ROWS]

        cursor.close()
        return rows
    
    @synchronized(myLock)
    def get_header(self, question_id: int):
        cursor = self.cnx.cursor(buffered=False)
        cursor.execute(f'SELECT question_table.title, question_table.content FROM question_table WHERE question_table.q_id = {question_id};')
        rows = list(cursor.fetchall())
        rows = [{'title': a, 'content': b} for a, b in rows]

        cursor.close()
        return rows[0]
    
    @synchronized(myLock)
    def get_answers(self, question_id: int, page_index: int):
        cursor = self.cnx.cursor(buffered=False)
        cursor.callproc('get_answers', [question_id])
        cursor.execute('SELECT * FROM temporary_answer_table')
        rows = list(cursor.fetchall())
        rows = [{'a_id': a, 'content': b, 'likes': c, 'user_name': d} for a, b, c, d in rows]
        rows = rows[page_index * self.ANSWER_ONE_PAGE_MAX_ROWS: (page_index + 1) * self.ANSWER_ONE_PAGE_MAX_ROWS]

        cursor.close()
        return rows
    
    @synchronized(myLock)
    def submit_answer(self, question_id: int, user_name: str, message: str):
        cursor = self.cnx.cursor(buffered=False)
        cursor.execute(f'SELECT user_table.user_id FROM user_table WHERE user_table.user_name = \'{user_name}\';')
        user_id = list(cursor.fetchall())[0][0]
        cursor.execute(f'INSERT INTO answer_table (q_id, user_id, content, likes) VALUES ({question_id}, \'{user_id}\', \'{message}\', 0);')
        self.cnx.commit()
        cursor.close()
    
    @synchronized(myLock)
    def put_question(self, message_title: str, message_content: str, user_name: str):
        cursor = self.cnx.cursor(buffered=False)
        cursor.execute(f'SELECT user_table.user_id FROM user_table WHERE user_table.user_name = \'{user_name}\';')
        user_id = list(cursor.fetchall())[0][0]
        cursor.execute(f'INSERT INTO question_table (title, content, label, user_id) VALUES (\'{message_title}\', \'{message_content}\', 1, {user_id});')
        self.cnx.commit()
        cursor.close()

    def close(self):
        # self.cnx.close()
        pass

if __name__ == '__main__':
    db = DataBase()
    # print(cnx.check_user_info('hyx1999', '123456'))
    # print(cnx.register('hyx2000', '123456'))
    # print(db.get_questions(0))
    # print(db.get_answers(1, 0))
    # print(db.get_header(1))
    # db.submit_answer(1, 'hyx1999', '...')
    db.put_question('rt', '...', 'hyx1999')
    db.close()
