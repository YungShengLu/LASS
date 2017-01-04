# this program will load ../Get_Last_PM2.5/gpsfile.json to gen ID in a given distance

import time, json
from region_graph import compute_dis
from math import radians, cos, sin, asin, sqrt

# def compute_dis(lon1, lat1, lon2, lat2):

def main():
    print("screen program: gen IDs list within a given distance")
    
    while 1:  

        with open('../Get_Latest_PM2.5/gpsfile.json') as data_file:    
            data = json.load(data_file)['sites']        # data is a list

        
        disBOUND = 5000                                 # 5 km
        numBOUND = 10
        nearBY = {}
        for d in data:
            if d['type'] == 'airbox' or d['type'] == 'lass':
                nearBY[d['id']] = []
                
                find = 0
                lon1 = d['lon']
                lat1 = d['lat']

                for check in data:
                    if (check['type'] == 'airbox' or check['type'] == 'lass') and check['id'] != d['id']:
                        lon2 = check['lon']
                        lat2 = check['lat']

                        # compute their distance
                        distance = compute_dis(lon1, lat1, lon2, lat2)
                        if distance <= disBOUND:
                            nearBY[d['id']].append(check['id'])
                            find += 1
                        if find == numBOUND:
                            break

        
        output = {disBOUND:nearBY}

        with open('/var/www/html/LASS/data/json/nearID.json', 'w') as fp:
            json.dump(output, fp, indent=4)



        print("sleeping")
        time.sleep(300)


if __name__ == '__main__':
    main()
    