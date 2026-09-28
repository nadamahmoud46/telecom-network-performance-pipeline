import random
import numpy as np
from datetime import date, timedelta

from db import get_connection


TOTAL_SUBSCRIPTIONS = 1_200_000
TOTAL_CUSTOMERS = 1_000_000


def generate_msisdn():

    prefix = np.random.choice(
        [
            "010",
            "011",
            "012",
            "015"
        ]
    )

    number = random.randint(
        10000000,
        99999999
    )

    return f"+20{prefix}{number}"



def generate_subscription_type():

    return np.random.choice(
        [
            "CONSUMER",
            "ENTERPRISE",
            "IOT"
        ],
        p=[
            0.80,
            0.18,
            0.02
        ]
    )



def choose_plan(subscription_type):

    if subscription_type == "ENTERPRISE":

        return 4


    elif subscription_type == "IOT":

        # IoT uses low plans
        return np.random.choice(
            [
                1,
                2
            ],
            p=[
                0.8,
                0.2
            ]
        )


    else:

        return np.random.choice(
            [
                1,
                2,
                3
            ],
            p=[
                0.40,
                0.45,
                0.15
            ]
        )



def generate_status():

    return np.random.choice(
        [
            "Active",
            "Suspended",
            "Terminated"
        ],
        p=[
            0.88,
            0.09,
            0.03
        ]
    )



def generate_subscriptions():

    conn = get_connection()
    cur = conn.cursor()


    batch=[]


    for i in range(1, TOTAL_SUBSCRIPTIONS+1):


        customer_id = random.randint(
            1,
            TOTAL_CUSTOMERS
        )


        sub_type = generate_subscription_type()


        plan_id = choose_plan(
            sub_type
        )


        activation_date = (
            date.today()
            -
            timedelta(
                days=random.randint(
                    30,
                    2000
                )
            )
        )


        batch.append(
            (
                i,
                customer_id,
                plan_id,
                generate_msisdn(),
                activation_date,
                generate_status(),
                sub_type
            )
        )


        if len(batch) == 10000:


            cur.executemany(
                """
                INSERT INTO network.subscriptions
                (
                    subscription_id,
                    customer_id,
                    plan_id,
                    msisdn,
                    activation_date,
                    status,
                    subscription_type
                )

                VALUES
                (
                    %s,%s,%s,%s,%s,%s,%s
                )
                """,
                batch
            )


            conn.commit()

            batch.clear()

            print(
                i,
                "subscriptions inserted"
            )


    conn.commit()

    cur.close()
    conn.close()


    print(
        "Subscriptions generation completed"
    )



if __name__ == "__main__":
    generate_subscriptions()