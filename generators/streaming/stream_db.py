from psycopg2 import connect
from generators.config import POSTGRES_CONFIG


def get_cells():
    conn = connect(**POSTGRES_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT cell_id, technology
        FROM network.cell_towers
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "cell_id": row[0],
            "technology": row[1]
        }
        for row in rows
    ]


def get_subscriptions():
    conn = connect(**POSTGRES_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM network.subscriptions
        LIMIT 5
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

load_subscriptions = get_subscriptions
load_towers = get_cells