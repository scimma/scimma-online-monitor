#!/usr/bin/python3
###
### Author: ree55@psu.edu
### Date:   Oct 12, 2023 
### Desc:   Run helloworld.py with influx credentials taken from an AWS secret.
###

import os
import pytz
import sys
import utils

from datetime import datetime, timezone

region       = "us-west-2"
influxSecret = "dev-influxdb-hop-writer-creds" 
configPath   = "config/scald.yml"

# get influxSecret from environment
if (os.environ.get("INFLUX_SECRET") is not None):
    influxSecret = os.environ.get("INFLUX_SECRET")

# get INFLUX_USER and INFLUX_PASS
if (os.environ.get("INFLUX_USER") is not None):
   influxUser = os.environ.get("INFLUX_USER")
else:
   influxUser = utils.getInfluxUser(region, influxSecret)
   os.environ["INFLUX_USER"] = influxUser

if (os.environ.get("INFLUX_PASS") is not None):
   influxPass = os.environ.get("INFLUX_PASS")
else:
   influxPass = utils.getInfluxPass(region, influxSecret)
   os.environ["INFLUX_PASS"] = influxPass

# Line buffer stdout and stderr
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

print("======================================")
print("== Starting helloworld.py")
print("Date: %s" % datetime.now(pytz.timezone('America/New_York')))
print("======================================")
exitVal = os.system(f"/root/helloworld.py --scald-config={configPath}")
print(f"exited with os.system returning: {exitVal}")
