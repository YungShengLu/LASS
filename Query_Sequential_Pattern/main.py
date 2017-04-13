#!/usr/bin/python3
"""
air monitors in Tainan: (id)
    74DA38AF489E
    74DA38AF487A
    74DA38AF4842
    74DA38AF482E
    74DA38AF4812
    74DA38AF479A
    74DA3895E068
    74DA3895E04C
    74DA3895DFF6
    74DA3895C39E
    74DA388FF4F8
    28C2DDDD479F
    28C2DDDD479C
    28C2DDDD415F
    YK_160
    FT1_CCH01
"""
from influxdb import InfluxDBClient
def query_interval_by_device_id(client, measurement='', device_id='', start_time='now()', duration='7d'):
    # return type: Raw JSON from InfluxDB
    return client.query('select "PM2.5" from ' + measurement + ' where "Device_id" = \'' + device_id + '\' and time >= ' + start_time + ' - ' + duration).raw

def main():
    client = InfluxDBClient(host='127.0.0.1', port=8086, database='PM25')
    #result = client.query('select * from lass order by time desc limit 10;', epoch='RFC3339')
    #result = client.query('select "" from lass where id=74DA3895DFF6 and time >= now() - 7d order by time;', epoch='RFC3339')
    #print("Result: {0}".format(result))
    print(query_interval_by_device_id(client, 'lass', 'FT1_CCH01'))

if __name__=='__main__':
    main()
