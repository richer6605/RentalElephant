import psycopg2

HOST = "localhost"
PORT = 27017
USER = "USER"
PASSWORD = "PASSWORD"
DATABASE = "DATABASE"

def setup(table, cols):
    conn = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD)
    cur = conn.cursor()
    query = '''
             CREATE TABLE IF NOT EXISTS
                 {0} (
                      {1} text UNIQUE,
                      {2} text,
                      {3} text
                     )
             '''
    query = query.format(table, *cols)
    cur.execute(query)
    cur.close()
    conn.commit()
    conn.close()

def updateDB(feeds):
    conn = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD)
    cur = conn.cursor()
    for k,v in feeds.items():
        cols = ["id", "message", "updated_time"]
        setup(k, cols)
        query = '''
                INSERT INTO
                    {0} ({1}, {2}, {3})
                VALUES
                    (%({1})s, %({2})s, %({3})s)
                ON
                    CONFLICT ({1})
                DO UPDATE
                    SET ({1}, {2}, {3}) = (%({1})s, %({2})s, %({3})s)
                '''
        query = query.format(k, *cols)
        cur.executemany(query, v)
    cur.close()
    conn.commit()
    conn.close()
