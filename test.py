import pandas as pd
import numpy as np
import requests

searching = '경기도', '한식'
url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
headers = {
    "Authorization": "KakaoAK cd12239e86cd67a7fdc5c228fe77162d"
}
places = requests.get(url, headers = headers).json()['documents']
placeList = list()

for i in range(1,4600):
    places = requests.get(url + str(i), headers = headers).json()['documents']

    for x in places:
        placeList.append(list(x.values()))

newplaces = np.array(placeList)

df = pd.DataFrame(newplaces, columns = ['adress name', 'category group code',
                                        'category group name', 'category name',
                                        'distance', 'id',' phone','place name',
                                        'place url', 'road adress name',
                                        'x', 'y'])

df.to_csv('test3.csv', encoding = 'utf-8-sig')