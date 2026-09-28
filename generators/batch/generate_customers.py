import numpy as np
import pandas as pd
from faker import Faker
from db import get_connection


fake = Faker()


CUSTOMERS = 1_000_000


city_distribution = {

    1:0.30,   # Cairo
    2:0.15,   # Giza
    3:0.10,   # Alexandria
    4:0.05,   # New Capital
    5:0.10,
    6:0.20,
    7:0.05,
    8:0.05

}


from datetime import date


def generate_birth_dates(size):

    current_year = date.today().year

    ages = np.random.choice(
        [
            22,
            35,
            50,
            65
        ],
        size=size,
        p=[
            0.25,
            0.40,
            0.25,
            0.10
        ]
    )


    birthdays = []

    for age in ages:

        birth_year = current_year - int(age)

        birth_date = fake.date_between_dates(
            date_start=date(
                birth_year,
                1,
                1
            ),
            date_end=date(
                birth_year,
                12,
                31
            )
        )

        birthdays.append(birth_date)


    return birthdays



def generate_customers():


    conn=get_connection()
    cur=conn.cursor()


    batch=[]


    city_ids=list(city_distribution.keys())
    city_prob=list(city_distribution.values())


    cities=np.random.choice(
        city_ids,
        CUSTOMERS,
        p=city_prob
    )


    segments=np.random.choice(
        [
            "Individual",
            "Business"
        ],
        CUSTOMERS,
        p=[
            0.92,
            0.08
        ]
    )


    genders=np.random.choice(
        [
            "Male",
            "Female"
        ],
        CUSTOMERS,
        p=[
            0.52,
            0.48
        ]
    )


    birthdays=generate_birth_dates(
        CUSTOMERS
    )



    for i in range(CUSTOMERS):

        batch.append(
            (
                i+1,
                genders[i],
                birthdays[i],
                segments[i],
                int(cities[i])
            )
        )


        if len(batch)==10000:


            cur.executemany(
                """
                INSERT INTO network.customers
                (
                customer_id,
                gender,
                birth_date,
                segment,
                city_id
                )
                VALUES
                (%s,%s,%s,%s,%s)
                """,
                batch
            )

            conn.commit()
            batch=[]

            print(i,"customers inserted")


    conn.commit()

    cur.close()
    conn.close()


    print("Customers generation completed")



if __name__=="__main__":
    generate_customers()