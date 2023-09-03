import psycopg2

def connect_postgres():
    conn = psycopg2.connect(database="postgres", host="localhost", user="postgres", password="segerlund97", port="5432")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tweets")

    cursor = cursor.fetchall()
    for i in range(len(cursor)):
        print(cursor[i])


connect_postgres()
