import json
import time
import random

from datetime import datetime, timedelta

from kafka import KafkaProducer


from generators.streaming.stream_db import (
    load_subscriptions,
    load_towers
)


from generators.streaming.stream_distributions import (
    weighted_choice
)


from generators.streaming.stream_utils import (
    is_peak_hour
)



TOPIC = "telecom_cdr_data"



# -----------------------------
# Traffic Distribution
# -----------------------------

TRAFFIC_TYPES = [

    ("Internet", 0.70),

    ("Video", 0.15),

    ("Voice", 0.10),

    ("SMS", 0.05)

]




# -----------------------------
# Duration Generator
# -----------------------------

def generate_duration(traffic_type):


    if traffic_type == "Internet":

        return random.randint(
            60,
            3600
        )


    if traffic_type == "Video":

        return random.randint(
            300,
            7200
        )


    if traffic_type == "Voice":

        return random.randint(
            30,
            1800
        )


    return random.randint(
        1,
        5
    )




# -----------------------------
# Data Volume Generator
# -----------------------------

def generate_data_volume(traffic_type):


    peak = is_peak_hour()



    if traffic_type == "Internet":


        if peak:

            return round(
                random.uniform(500,7000),
                2
            )


        return round(
            random.uniform(100,4000),
            2
        )



    if traffic_type == "Video":


        if peak:

            return round(
                random.uniform(1000,9000),
                2
            )


        return round(
            random.uniform(500,7000),
            2
        )



    if traffic_type == "Voice":


        return round(
            random.uniform(1,50),
            2
        )



    return round(
        random.uniform(0.001,1),
        3
    )





# -----------------------------
# CDR Generator
# -----------------------------

def generate_cdr(
        cdr_id,
        subscriptions,
        towers
):


    traffic = weighted_choice(
        TRAFFIC_TYPES
    )



    subscription = random.choice(
        subscriptions
    )


    subscription_id = subscription[0]



    tower = random.choice(
        towers
    )


    cell_id = tower["cell_id"]

    technology = tower["technology"]




    start_time = (

        datetime.now()

        -

        timedelta(
            seconds=random.randint(
                0,
                86400
            )
        )

    )



    return {


        "cdr_id":
            cdr_id,



        "subscription_id":
            subscription_id,



        "cell_id":
            cell_id,



        "technology":
            technology,



        "traffic_type":
            traffic,



        "start_time":
            start_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),



        "duration_seconds":
            generate_duration(
                traffic
            ),



        "data_volume_mb":
            generate_data_volume(
                traffic
            ),



        "event_time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    }





# -----------------------------
# Kafka Streaming
# -----------------------------

def main():


    producer = KafkaProducer(

        bootstrap_servers="localhost:9092",

        value_serializer=lambda x:
            json.dumps(x).encode("utf-8")

    )



    print(
        "Loading subscriptions..."
    )


    subscriptions = load_subscriptions()



    print(
        f"{len(subscriptions)} subscriptions loaded"
    )



    print(
        "Loading towers..."
    )


    towers = load_towers()



    print(
        f"{len(towers)} towers loaded"
    )



    print(
        "CDR data streaming started"
    )



    counter = 0



    while True:


        counter += 1



        record = generate_cdr(

            counter,

            subscriptions,

            towers

        )



        future = producer.send(

            TOPIC,

            record

        )



        try:


            metadata = future.get(

                timeout=10

            )


            print(record)

            print(metadata)



        except Exception as e:


            print(
                "Kafka Error:",
                e
            )



        time.sleep(
            0.1
        )





if __name__ == "__main__":

    main()