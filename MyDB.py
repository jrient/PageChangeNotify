import sqlite3

db_name = 'mydb'
table_name = 'page_content'

def init_table():
    conn = sqlite3.connect('%s.db' % db_name)
    c = conn.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS %s (
        id INTEGER PRIMARY KEY,
        url TEXT not null,
        content TEXT not null,
        date timestamp not null default current_timestamp
    )
    ''' % table_name
    c.execute(sql)
    c.close()

def read_db(url):
    conn = sqlite3.connect('%s.db' % db_name)
    c = conn.cursor()
    sql = 'SELECT * FROM %s where url = "%s"' % (table_name, url)
    c.execute(sql)
    data = c.fetchone()
    c.close()
    return data

def write_db(url, content):
    conn = sqlite3.connect('%s.db' % db_name)
    c = conn.cursor()

    # 查找是否已经存在
    data = read_db(url)
    if data:
        sql = 'UPDATE %s SET content = "%s" WHERE url = "%s"' % (table_name, content, url)
    else:
        sql = 'INSERT INTO %s (url, content) VALUES ("%s", "%s")' % (table_name, url, content)
    c.execute(sql)
    conn.commit()
    c.close()