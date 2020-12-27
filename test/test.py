import random
import os
import time
from database import DataBase

db = DataBase()

def log_run_time(text):
    def decorator(func):
        def wrapper(*args, **kw):
            start_time = time.time()  # 单位为秒
            output = func(*args, **kw)
            end_time = time.time()
            run_time = end_time - start_time
            local_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            file_path = os.path.join('log', text + '_' + local_time + '.txt')
            with open(file_path, 'w') as f:
                f.write('run time: ' + str(run_time) + '\n')
            return output
        return wrapper
    return decorator

# @log_run_time('insert')
def test_insert():
    cursor = db.db.cursor(buffered=True)
    value = random.randint(0, 100)
    sql = f'INSERT INTO test_table (value) VALUES ({value})'
    cursor.execute(sql)
    cursor.close()
    db.db.commit()

@log_run_time('query')
def test_query(value=None):
    if value is None:
        value = random.randint(0, 100)
    cursor = db.db.cursor(buffered=True)
    sql = f'SELECT * FROM test_table WHERE test_table.value = {value}'
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    # print(rows)

def add_index():
    cursor = db.db.cursor(buffered=True)
    sql = f'CREATE INDEX test_table_value_index ON test_table (value)'
    cursor.execute(sql)
    cursor.close()
    db.db.commit()


if __name__ == '__main__':
    # add_index()
    for _ in range(100):
        for __ in range(100):
            test_insert()
        test_query()
        time.sleep(0.5)
        print('[step {:0>3d}/100]'.format(_))
