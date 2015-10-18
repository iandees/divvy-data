# divvy-data
A script to grab Divvy station data at a regular interval and save it to a CSV.

# Historical Divvy Data

[Ian](https://github.com/iandees) has been running this script since Divvy started. You can download the historical station data recorded by this script here:

### Format

All of the CSV files have the same set of columns (in this order):

Column | Description
-------|------------
timestamp | The timestamp for when this data point was published. The format `yyyy-mm-dd hh:mm:ss`.
station_id | The integer Divvy station ID.
bikes_available | The number of bikes available at this station at the published time.
docks_available | The number of empty docks available at this station at the published time.
total_docks | The total number of docks at this station at the published time.
status | The status for the station. The various statuses aren't documented.

### All stations

These are gzipped CSV files that contains all datapoints from all stations for the given time period.

- [All of 2013](https://data.openstreetmap.us.s3.amazonaws.com/divvy/all_stations-2013.csv.gz)
- [All of 2014](https://data.openstreetmap.us.s3.amazonaws.com/divvy/all_stations-2014.csv.gz)
- [January 2015](http://data.openstreetmap.us.s3.amazonaws.com/divvy/all_stations-2015-01.csv.gz)
- [February 2015](http://data.openstreetmap.us.s3.amazonaws.com/divvy/all_stations-2015-02.csv.gz)
- [March 2015](http://data.openstreetmap.us.s3.amazonaws.com/divvy/all_stations-2015-03.csv.gz)
- [April 2015](http://data.openstreetmap.us.s3.amazonaws.com/divvy/all_stations-2015-04.csv.gz)
- [May 2015](http://data.openstreetmap.us.s3.amazonaws.com/divvy/all_stations-2015-05.csv.gz)
- [June 2015](http://data.openstreetmap.us.s3.amazonaws.com/divvy/all_stations-2015-06.csv.gz)
- [July 2015](http://data.openstreetmap.us.s3.amazonaws.com/divvy/all_stations-2015-07.csv.gz)
- [August 2015](http://data.openstreetmap.us.s3.amazonaws.com/divvy/all_stations-2015-08.csv.gz)
- [September 2015](http://data.openstreetmap.us.s3.amazonaws.com/divvy/all_stations-2015-09.csv.gz)
