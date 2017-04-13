#!/usr/bin/python3
from influxdb import InfluxDBClient
def main():
    client = InfluxDBClient(host='127.0.0.1', port=8086, database='PM25')
    result = client.query('select * from lass order by time desc limit 10;', epoch='RFC3339')
    print("Result: {0}".format(result))

if __name__=='__main__':
    main()
