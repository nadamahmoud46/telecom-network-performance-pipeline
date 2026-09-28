import psycopg
import random

from generators.config import DB_CONFIG


TOWERS_COUNT = 1500


def generate_cell_towers():

    conn = psycopg.connect(**DB_CONFIG)
    cur = conn.cursor()


    # Load cities coordinates
    cur.execute("""
        SELECT
            city_id,
            latitude,
            longitude,
            city_name
        FROM network.cities
    """)


    cities = cur.fetchall()


    # city weights based on telecom density
    city_weights = []

    for city in cities:

        city_id = city[0]

        if city_id == 1:       # Cairo
            weight = 30

        elif city_id == 2:     # Giza
            weight = 20

        elif city_id == 3:     # Alexandria
            weight = 15

        elif city_id in [4,5]:
            weight = 8

        else:
            weight = 2


        city_weights.append(weight)



    batch=[]


    for i in range(1,TOWERS_COUNT+1):

        city=random.choices(
            cities,
            weights=city_weights
        )[0]


        city_id = city[0]
        base_lat = float(city[1])
        base_lon = float(city[2])


        # Technology distribution

        technology=random.choices(
            ["4G","5G"],
            weights=[85,15]
        )[0]


        # 5G concentrated in major cities

        if technology=="5G":

            if city_id not in [1,2,3]:
                technology="4G"



        # tower coordinates around city

        latitude = round(
            base_lat + random.uniform(-0.08,0.08),
            6
        )


        longitude = round(
            base_lon + random.uniform(-0.08,0.08),
            6
        )



        batch.append(
            (
                f"CELL_{i:06d}",
                technology,
                latitude,
                longitude,
                city_id
            )
        )


        if len(batch)==500:


            cur.executemany(
                """
                INSERT INTO network.cell_towers
                (
                    cell_id,
                    technology,
                    latitude,
                    longitude,
                    city_id
                )
                VALUES
                (%s,%s,%s,%s,%s)
                """,
                batch
            )


            conn.commit()

            print(
                f"{i} towers inserted"
            )

            batch=[]



    if batch:

        cur.executemany(
            """
            INSERT INTO network.cell_towers
            VALUES (%s,%s,%s,%s,%s)
            """,
            batch
        )

        conn.commit()



    cur.close()
    conn.close()


    print("Cell towers generation completed")



if __name__=="__main__":
    generate_cell_towers()