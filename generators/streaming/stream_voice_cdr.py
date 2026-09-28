import json
import random
import time

from datetime import datetime, timedelta

from kafka import KafkaProducer


from generators.streaming.stream_db import (
    load_subscriptions,
    load_towers
)


from generators.streaming.stream_distributions import (
    weighted_choice,
    VOICE_STATUS,
    TERMINATION
)


from generators.streaming.stream_utils import (
    generate_call_duration
)



KAFKA_SERVER = "localhost:9092"

TOPIC_NAME = "telecom_voice_cdr"


EVENTS_PER_SECOND = 50




producer = KafkaProducer(

    bootstrap_servers=KAFKA_SERVER,

    value_serializer=lambda x:
        json.dumps(x).encode("utf-8")

)



print(
    "Connected:",
    producer.bootstrap_connected()
)




# -----------------------------
# Generate Voice CDR
# -----------------------------

def generate_voice_cdr(
        cdr_id,
        subscriptions,
        towers
):


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
                3600
            )
        )

    )



    call_status = weighted_choice(
        VOICE_STATUS
    )



    termination = weighted_choice(
        TERMINATION
    )



    # keep status and termination realistic

    if call_status == "Completed":

        termination = "NORMAL"


    elif call_status == "Dropped":

        termination = "DROP"



    else:

        termination = "NETWORK_FAILURE"




    return {


        "cdr_id":
            cdr_id,



        "subscription_id":
            subscription_id,



        "start_time":
            start_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),



        "duration_seconds":
            generate_call_duration(),



        "cell_id":
            cell_id,



        "technology":
            technology,



        "call_status":
            call_status,



        "termination_cause":
            termination,



        "event_time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    }





# -----------------------------
# Streaming
# -----------------------------

def main():


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
        "Voice CDR streaming started..."
    )



    counter = 0



    while True:


        counter += 1



        event = generate_voice_cdr(

            counter,

            subscriptions,

            towers

        )



        future = producer.send(

            TOPIC_NAME,

            event

        )



        try:


            metadata = future.get(
                timeout=10
            )


            print(event)

            print(metadata)



        except Exception as e:


            print(
                "Kafka Error:",
                e
            )



        time.sleep(

            1 / EVENTS_PER_SECOND

        )





if __name__ == "__main__":

    main()