import random

from datetime import datetime


def is_peak_hour():

    hour = datetime.now().hour

    return 19 <= hour <= 23


# ---------------------------
# Voice Duration
# ---------------------------

def generate_call_duration():

    r = random.random()

    if r < 0.70:
        return random.randint(60,120)

    if r < 0.95:
        return random.randint(120,300)

    return random.randint(300,1800)


# ---------------------------
# 4G Throughput
# ---------------------------

def throughput_4g():

    if is_peak_hour():

        return round(random.uniform(15,28),2)

    return round(random.uniform(25,45),2)


# ---------------------------
# 5G Throughput
# ---------------------------

def throughput_5g():

    if is_peak_hour():

        return round(random.uniform(120,250),2)

    return round(random.uniform(180,450),2)


# ---------------------------
# Upload
# ---------------------------

def upload_speed(technology):

    if technology=="4G":
        return round(random.uniform(5,15),2)

    return round(random.uniform(30,80),2)


# ---------------------------
# Latency
# ---------------------------

def latency(technology):

    if technology=="4G":

        if is_peak_hour():
            return round(random.uniform(45,70),2)

        return round(random.uniform(30,55),2)

    return round(random.uniform(8,20),2)


# ---------------------------
# Packet Loss
# ---------------------------

def packet_loss():

    if is_peak_hour():

        return round(random.uniform(0.4,1.3),3)

    return round(random.uniform(0.1,0.7),3)


# ---------------------------
# Availability
# ---------------------------

def availability():

    if random.random()<0.01:

        return round(random.uniform(90,98),2)

    return round(random.uniform(99.5,100),2)