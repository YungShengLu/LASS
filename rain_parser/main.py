#!/usr/bin/python3

import urllib.request
from bs4 import BeautifulSoup

class Rain:
    def __init__(self, time, county, temp, prob):
        self.time = time     # 時間 string
        self.county = county # 縣市 string
        self.temp = temp     # 溫度 string
        self.prob = prob     # 機率 string
        pass
    def __str__(self):
        return '{{"time": "{}", "county": "{}", "temp": "{}", "prob": "{}"}}'.format(self.time, self.county, self.temp, self.prob)
    def toJSON(self):
        return '{{"time": "{}", "county": "{}", "temp": "{}", "prob": "{}"}}'.format(self.time, self.county, self.temp, self.prob)
    def toCSV(self):
        return '{},{},{},{}'.format(self.time, self.county, self.temp, self.prob)

rains = []

def main():
#    link = 'http://www.cwb.gov.tw/V7/forecast/f_index.htm'
#    with urllib.request.urlopen(link) as f:
#        forecast = f.read().decode('UTF-8')
    with open('f_index.html', 'r') as f: # local test
        forecast = f.read()              # local test
    soup = BeautifulSoup(forecast, 'lxml')
    timeStr = soup.findAll('div', {'class': 'modifyedDate'})[0].string
    #print('[debug] %s' % timeStr)
    trs = soup.findAll('tr')
    #print('[debug] %s' % len(trs))
    #for i in range(len(trs)):
    #    print('trs[{}]: {}'.format(i, trs[i].prettify()))
    for tr in trs:
        tds = tr.findAll('td')
        if not tds:
            continue
        rain = Rain(timeStr, tds[0].a.string, tds[1].a.string, tds[2].a.string)
        #print(rain)
        rains.append(rain)
    #print(len(rains)) # 22
    pass

if __name__ == '__main__':
    main()
    #print('[debug] Python3 run successfully')
    pass

