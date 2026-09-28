import random


# -----------------------------
# Voice Call
# -----------------------------

VOICE_STATUS = [
    ("Completed", 0.965),
    ("Dropped", 0.015),
    ("Failed", 0.020)
]


TERMINATION = [
    ("NORMAL",0.85),
    ("DROP",0.10),
    ("NETWORK_FAILURE",0.05)
]


# -----------------------------
# Technology
# -----------------------------

TECH_DISTRIBUTION = [
    ("4G",0.85),
    ("5G",0.15)
]


# -----------------------------
# Peak Hours
# -----------------------------

PEAK_START = 19
PEAK_END = 23


# -----------------------------
# Utility
# -----------------------------

def weighted_choice(items):

    values = [x[0] for x in items]

    weights = [x[1] for x in items]

    return random.choices(values,weights=weights,k=1)[0]