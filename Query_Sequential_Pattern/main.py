#!/usr/bin/python3
_msg_monitors = """
air monitors in Tainan City: (id)
    airbox
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
    lass
        YK_160
        FT1_CCH01
"""
from influxdb import InfluxDBClient

def query_interval_by_device_id(client, measurement='', device_id='', late_time='now()', duration='7d'):
    # return type: Raw JSON from InfluxDB
    early_time = late_time + ' - '  + duration
    str_query = 'select "PM2.5" from ' + measurement + ' where "Device_id" = \'' + device_id + '\' and time <= ' + late_time + ' and time > ' + early_time
    return client.query(str_query).raw

def get_pm25s_from_query(json={}):
    # return type: list
    ret = []
    for value in json['series'][0]['values']:
        #print(value[1])
        ret.append(value[1])
    return ret

def pm25_to_pattern(pm25=0):
    # return type: str
    _pm25_levels = [11, 23, 35, 41, 47, 53, 58, 64, 70]
    _patterns =    ['a','b','c','d','e','f','g','h','i','j']
    for i in range(0, len(_pm25_levels)):
        if pm25 <= _pm25_levels[i]:
            return _patterns[i]
    return _patterns[len(_pm25_levels)]

def pm25s_to_patterns(pm25s=[]):
    # return type: list
    ret = []
    for pm25 in pm25s:
        ret.append(pm25_to_pattern(pm25))
    return ret

def main():
    client = InfluxDBClient(host='127.0.0.1', port=8086, database='PM25')
    #result = client.query('select * from lass order by time desc limit 10;', epoch='RFC3339')
    #result = client.query('select "" from lass where id=74DA3895DFF6 and time >= now() - 7d order by time;', epoch='RFC3339')
    #print("Result: {0}".format(result))
    #print(query_interval_by_device_id(client, 'lass', 'FT1_CCH01'))
    #result = query_interval_by_device_id(client, 'lass', 'FT1_CCH01')
    #print(result['series'][0]['name'])
    #get_pm25s_from_query(result)
    print(_msg_monitors)
    measurement, device_id = input('Input measurement and id: (seperated by space) ').split()
    print('measurement = {0}, device_id = {1}'.format(measurement, device_id))
    print('') # new line
    for d in range(0,7):
        result = query_interval_by_device_id(client, measurement, device_id, 'now() - ' + str(d) + 'd', '1d')
        #print(get_pm25s_from_query(result))
        print(''.join(pm25s_to_patterns(get_pm25s_from_query(result))))

if __name__=='__main__':
    main()
