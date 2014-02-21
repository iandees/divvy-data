import socket
import requests
import json
from datetime import datetime, timedelta
import time
import pytz
import logging
import sys
import csv
import traceback
import os
import errno

def mkdirs(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise    

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

tz = pytz.timezone('America/Chicago')

logging.info("Starting to grab stations.")

latest_station_fingerprints = {}
lastTstamp = None
sleepTime = None
while True:
    if sleepTime:
        logging.info("Sleeping %.1f seconds." % sleepTime)
        time.sleep(sleepTime)

    start = time.time()

    delay = 3
    tries = 0
    while True:
        try:
            data = requests.get('http://www.divvybikes.com/stations/json/', timeout=10, headers={'User-Agent': 'DivvyScraper 1.0 (https://github.com/iandees/divvy-data)'}).json()
            tries += 1
            tstamp = data['executionTime']
            tstamp = datetime.strptime(tstamp, '%Y-%m-%d %I:%M:%S %p')
            #logging.debug("Naive timestamp is %s", timestamp.isoformat())
            tstamp = tz.localize(tstamp)
            #logging.debug("TZ-aware timestamp is %s", timestamp.isoformat())
            tstamp = tstamp.astimezone(pytz.UTC)
            #logging.debug("UTC timestamp is %s" % timestamp.isoformat())
            tries = 0
            break
            # 2013-09-10 05:13:02 PM
        except Exception, e:
            traceback.print_exc(e)
            logging.error("Try %s: Waiting %s seconds and trying again." % (tries, delay))
            time.sleep(delay)
            delay = delay * 2
            if delay > 30:
                delay = 30

    if lastTstamp and tstamp == lastTstamp:
        sleepTime = 20
        logging.info("Timestamp %s hasn't changed, so skipping this run." % tstamp)
        continue
    else:
        logging.info("Timestamp is %s." % tstamp)

    if lastTstamp:
        sleepTime = 60
    else:
        sleepTime = 60
    lastTstamp = tstamp

    date_str = tstamp.strftime('%Y-%m-%d')
    timestamp_str = tstamp.strftime('%Y-%m-%d %H:%M:%S')

    for station in data['stationBeanList']:
        station_dir = 'by_station/%03d' % station['id']
        station_day_path = '%s/%s.csv' % (station_dir, date_str)
        mkdirs(station_dir)

        station['timestamp'] = timestamp_str
        station['station_id'] = station['id']
        station['bikes_available'] = station['availableBikes']
        station['docks_available'] = station['availableDocks']
        station['total_docks'] = station['totalDocks']
        station['station_name'] = station['stationName']
        station['status'] = station['statusKey']

        if os.path.exists(station_day_path):
            with open(station_day_path, 'a') as f:
                writer = csv.DictWriter(f, ['timestamp', 'station_id', 'bikes_available', 'docks_available', 'total_docks', 'status'], extrasaction='ignore')
                writer.writerow(station)
        else:
            with open(station_day_path, 'w') as f:
                writer = csv.DictWriter(f, ['timestamp', 'station_id', 'bikes_available', 'docks_available', 'total_docks', 'status'], extrasaction='ignore')
                writer.writeheader()
                writer.writerow(station)

        station_info_path = '%s/info.csv' % station_dir

        station_hash = hash(station['stationName']) + hash(station['totalDocks']) + hash(station['latitude']) + hash(station['longitude']) + hash(station['statusKey'])
        if station['id'] not in latest_station_fingerprints or latest_station_fingerprints[station['id']] != station_hash:
            if os.path.exists(station_info_path):
                with open(station_info_path, 'a') as f:
                    writer = csv.DictWriter(f, ['timestamp', 'station_id', 'total_docks', 'status', 'latitude', 'longitude', 'station_name'], extrasaction='ignore')
                    writer.writerow(station)
            else:
                with open(station_info_path, 'w') as f:
                    writer = csv.DictWriter(f, ['timestamp', 'station_id', 'total_docks', 'status', 'latitude', 'longitude', 'station_name'], extrasaction='ignore')
                    writer.writeheader()
                    writer.writerow(station)
            latest_station_fingerprints[station['id']] = station_hash
    logging.info("Inserted %s stations in %.1f seconds." % (len(data['stationBeanList']), (time.time() - start)))

