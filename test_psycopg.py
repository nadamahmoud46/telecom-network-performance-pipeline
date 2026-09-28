import psycopg

try:
    conn = psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname="external",
        user="external",
        password="external",
    )

    cur = conn.cursor()
    cur.execute("SELECT version()")
    print(cur.fetchone())

except Exception as e:
    print(e)