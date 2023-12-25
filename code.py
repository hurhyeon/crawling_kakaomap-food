import pandas as pd
import numpy as np
import requests

query = "한식"
url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
headers = {
    "Authorization": "KakaoAK cd12239e86cd67a7fdc5c228fe77162d"
}
params =   {"query": f"{query}",
            "size": f"{15}",
            }
places = list()
placeList = list()
logList = list()

step = 0.001



xstart = 126.88316487661238
ystart = 37.69539100550791
xend = 126.91195598852781
yend = 37.7186471618891


sumstep = ((step) / (xend-xstart)) * ((step) / (yend-ystart))
print(sumstep)
sum = 0.

for x in np.linspace(xstart, xend, int((xend - xstart)/step)):
    for y in np.linspace(ystart, yend, int((yend - ystart)/step)):

        print ("x : {} , y : {}".format(x, y))
        params['rect'] = "{},{},{},{}".format(x,y,x-step,y+step)
        for i in range(1,3):
            params['page'] = f"{i}"
            try:
                places = requests.get(url,params = params, headers = headers).json()['documents']
        
                for z in places:
                    placeList.append(list(z.values()))
            except KeyError:
                returnback = requests.get(url,params = params, headers = headers).json()
                
                print("Reached limit at {} {} {} {}".format(x,y,x-step, y+step))
                logList.append("Limit at {} {} {} {}".format(x,y,x-step, y+step))

                if(len(places)):
                    places.pop()
                if(len(places)):
                    newplaces = np.array(placeList)
                
                    df = pd.DataFrame(newplaces, columns = ['adress', 'category', 'place name',
                                                            'place url', 'road adress name'
                                                            ,'x', 'y'])
                
                    df.to_csv('Places.csv', encoding = 'utf-8-sig')

                
                newlogs = np.array(logList)
                ldf = pd.DataFrame(logList, columns = ['logs'])
                ldf.to_csv('Logs.csv', mode ='a', encoding = 'utf-8-sig')

                exit()
        sum += sumstep
        print('{} % 진행'.format(sum * 100))
    
    
newplaces = np.array(placeList)
newplaces = np.delete(newplaces, [1,2,4,5,6], axis=1)

df = pd.DataFrame(newplaces, columns = ['adress name', 'category', 'place name',
                                        'place url', 'road adress name',
                                        'x', 'y'])

df.to_csv('places.csv', encoding = 'utf-8-sig')