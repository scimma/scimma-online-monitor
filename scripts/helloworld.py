#!/usr/bin/env python3

import time
import yaml

from collections import deque
from ligo.scald.io import influx

from optparse import OptionParser

def parse_command_line():
    parser = OptionParser()

    parser.add_option("--scald-config", metavar = "path", help = "sets ligo-scald options based on yaml configuration.")

    options, filenames = parser.parse_args()

    return options, filenames


options, filenames = parse_command_line()

# load influx config
config_path = options.scald_config
with open(config_path, "r") as f:
    agg_config = yaml.safe_load(f)

# set up influx sink
agg_sink = influx.Aggregator(**agg_config["backends"]["default"])
agg_sink.load(path=config_path)

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
