from mysql.connector.pooling import MySQLConnectionPool, MySQLConnection, PooledMySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql import connector
import threading
import time

config = {
    "host": "localhost",
    "user": "root",
    "password": "huyuxuan",
    "database": "zhihu"
}

pool = MySQLConnectionPool(pool_size=2, pool_name="pool", **config)


class starThread(threading.Thread):

    def __init__(self, thread_id):
        super().__init__()
        self.thread_id = thread_id
    
    def run(self):
        db = pool.get_connection()
        cursor = db.cursor()
        query = "SELECT likes FROM answer_table WHERE a_id = 1;"
        cursor.execute(query)
        likes = cursor.fetchone()[0]
        cursor.close()

        print('thread id:', self.thread_id, 'old stars:', likes)

        time.sleep(2)
        
        likes += 1

        cursor = db.cursor()
        update = "UPDATE answer_table SET likes = {} WHERE a_id = 1;".format(likes)
        print('update:', update)
        cursor.execute(update)
        db.commit()
        print('thread id:', self.thread_id, 'new stars:', likes)
        cursor.close()


if __name__ == '__main__':
    thread1 = starThread(1)
    thread2 = starThread(2)
    thread1.start()
    thread2.start()
