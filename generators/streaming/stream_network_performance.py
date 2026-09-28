import json
import time
import random

from datetime import datetime

from kafka import KafkaProducer

from generators.streaming.stream_utils import (
    throughput_4g,
    throughput_5g,
    upload_speed,
    latency,
    packet_loss,
    availability,
    is_peak_hour
)

from generators.streaming.stream_distributions import (
    weighted_choice,
    TECH_DISTRIBUTION
)


TOPIC = "telecom_network_performance"


TOTAL_CELLS = 1500



# -----------------------------
# Active Users
# -----------------------------

def generate_active_users():

    if is_peak_hour():

        return random.randint(
            3000,
            8000
        )


    return random.randint(
        500,
        4000
    )



# -----------------------------
# Network Condition
# -----------------------------

def network_condition(
    availability_value,
    packet_loss_value
):

    if availability_value < 98:

        return "Critical"


    if packet_loss_value > 1:

        return "Degraded"


    return "Normal"




# -----------------------------
# Cell Generator
# -----------------------------

def generate_cell():

    cell_id = (
        f"CELL_{random.randint(1,TOTAL_CELLS):06d}"
    )


    technology = weighted_choice(
        TECH_DISTRIBUTION
    )


    return cell_id, technology




# -----------------------------
# KPI Generator
# -----------------------------

def generate_kpi(measurement_id):


    cell_id, technology = generate_cell()



    download_mbps = (

        throughput_4g()

        if technology == "4G"

        else throughput_5g()

    )


    upload = upload_speed(
        technology
    )


    latency_value = latency(
        technology
    )


    packet_loss_value = packet_loss()


    availability_value = availability()



    return {


        "measurement_id":
            measurement_id,


        "cell_id":
            cell_id,


        "technology":
            technology,


        "download_mbps":
            download_mbps,


        "upload_mbps":
            upload,


        "latency_ms":
            latency_value,


        "packet_loss":
            packet_loss_value,


        "availability":
            availability_value,


        "active_users":
            generate_active_users(),


        "network_condition":
            network_condition(
                availability_value,
                packet_loss_value
            ),


        "event_time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    }




# -----------------------------
# Streaming
# -----------------------------

def main():



    producer = KafkaProducer(

        bootstrap_servers="localhost:9092",

        value_serializer=lambda x:
            json.dumps(x).encode("utf-8")

    )


    print(
        "Network Performance streaming started"
    )


    counter = 0



    while True:


        counter += 1


        data = generate_kpi(
            counter
        )


        future = producer.send(
            TOPIC,
            data
        )


        try:


            metadata = future.get(
                timeout=10
            )


            print(data)

            print(metadata)



        except Exception as e:


            print(
                "Kafka Error:",
                e
            )



        time.sleep(
            0.5
        )




if __name__ == "__main__":

    main()