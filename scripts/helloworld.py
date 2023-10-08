#!/usr/bin/env python3

import time
import yaml

from collections import deque
from ligo.scald.io import influx

# load influx config
CONFIG_PATH = "config/scald.yml"
with open(CONFIG_PATH, "r") as f:
    agg_config = yaml.safe_load(f)

# set up influx sink
agg_sink = influx.Aggregator(**agg_config["backends"]["default"])
agg_sink.load(path=CONFIG_PATH)

times = deque(maxlen = 100)
last_influx_write = None

while True:
    # append latest time
    times.append(time.now())

    # write to influx every 100 seconds
    if not last_influx_write or (time.now() - last_influx_write >= 100.):
        data = {
            "unused_key": {
                "time": list(times),
                "fields": {
                    "heartbeat": [1] * len(times),
                }
            }
        }
        agg_sink.store_columns("heartbeat", data, aggregate=None)

    # sleep for a second
    time.sleep(1)
