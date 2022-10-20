from bs4 import BeautifulSoup                           # pip install bs4
import requests                                         # pip install requests
import re
import time
import pandas as pd

#These are the maximum Lat/Long coordinates of the US.
N_Max = 47.45993360323442
E_Max = -66.88506404660163
S_Max = 24.544800887891085
W_Max = -124.74355915610697

#If we break the Latitude into 1/100ths, we need to decrease by this number
((N_Max - S_Max)/float(100))

#If we break the Longitude into 1/100ths, we need to decrease by this number
((E_Max - W_Max)/float(100))

#This sets up a client for us to use within the scraper. 
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}


def main(url):
    with requests.Session() as req:
        #breaking the North-South into 1/100ths
        #Try with a numbe rlike 5 before 100 and check if data is being filled.
        for y in range(100):
            N_Max = 47.45993360323442
            E_Max = -66.88506404660163
            s_iterator = 0.22915132715343334
            w_iterator = 0.5785849510950534
            N = N_Max - (y*s_iterator)
            S = N_Max - (y*s_iterator) - s_iterator
            #breaking the East-West into 1/100ths
            for x in range(100):
                #Sleep on each pull to avoid getting flagged as DDoS
                time.sleep(2)
                E = E_Max - (x*w_iterator)
                W = E_Max - (x*w_iterator) - w_iterator
                #Set the client up 
                req.headers.update(headers)
                req.head('https://www.zillow.com/homes/for_rent/')
                for item in range(1, 2):
                    # item can be used here to loop by refactoring `cat1` to be `cat2`
                    params = {
                        "searchQueryState": '{"pagination":{"currentPage":2},"usersSearchTerm":"Fairborn, OH/","mapBounds":{"west": ' + str(W) +' ,"east": ' + str(E) +' ,"south": ' + str(S) +' ,"north": ' + str(N) +' },"regionSelection":[{"regionId":4658,"regionType":6}],"isMapVisible":true,"filterState":{"isAllHomes":{"value":true},"sortSelection":{"value":"globalrelevanceex"}},"isListVisible":true,"mapZoom":12}',
                        "wants": '{"cat1":["mapResults"]}'
                    }
                    r = req.get(url, params=params)
                    df = pd.DataFrame(r.json()['cat1']['searchResults']['mapResults'])
                    print(df)
                    df.to_csv('zillowtest'+'Xgrid'+str(x)+'Ygrid'+str(y)+'.csv', index=False)
            
main('https://www.zillow.com/search/GetSearchPageState.htm')

#Code Output example for 1 zillow excel file
#zpid     price priceLabel  beds  baths    area  \
#0    122996411  $380,000      $380K   6.0    7.0  5477.0   
#1    114299212  $184,900      $185K   2.0    2.0  1369.0 
