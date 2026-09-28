from db import get_connection


plans = [

    (
        1,
        "Basic",
        "CONSUMER",
        75,
        6,
        600
    ),

    (
        2,
        "Medium",
        "CONSUMER",
        150,
        18,
        1600
    ),

    (
        3,
        "Premium",
        "CONSUMER",
        400,
        55,
        4000
    ),

    (
        4,
        "Corporate VIP",
        "ENTERPRISE",
        850,
        140,
        10000
    )
]


def generate_plans():

    conn = get_connection()
    cur = conn.cursor()


    cur.executemany(
        """
        INSERT INTO network.plans
        (
            plan_id,
            plan_name,
            plan_type,
            price,
            internet_gb,
            voice_minutes
        )
        VALUES
        (%s,%s,%s,%s,%s,%s)

        ON CONFLICT(plan_id)
        DO NOTHING
        """,
        plans
    )


    conn.commit()

    cur.close()
    conn.close()

    print("Plans generated successfully")


if __name__ == "__main__":
    generate_plans()