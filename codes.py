import pandas as pd
import numpy as np
import requests
import collections

query = "한식"
params = {
            }

url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
headers = {
    "Authorization": "KakaoAK 1168d5470dcbd5177abd32917433f470"
}

##카카오 API
def whole_region(start_x,start_y,end_x,end_y):
    #print(start_x,start_y,end_x,end_y)
    page_num = 1
    # 데이터가 담길 리스트
    all_data_list = []
    while(1):
        params = {"query": f"{query}", "cagetory_group_code" : 'FD6',
                "page": page_num, "rect": f'{start_x},{start_y},{end_x},{end_y}'}
        resp = requests.get(url, params=params, headers=headers)
        search_count = resp.json()['meta']['total_count']
        
        if search_count > 45:
            dividing_x = (start_x + end_x) / 2
            dividing_y = (start_y + end_y) / 2
            ## 4등분 중 왼쪽 아래
            all_data_list.extend(whole_region(start_x,start_y,dividing_x,dividing_y))
            ## 4등분 중 오른쪽 아래
            all_data_list.extend(whole_region(dividing_x,start_y,end_x,dividing_y))
            ## 4등분 중 왼쪽 위
            all_data_list.extend(whole_region(start_x,dividing_y,dividing_x,end_y))
            ## 4등분 중 오른쪽 위
            all_data_list.extend(whole_region(dividing_x,dividing_y,end_x,end_y))
            return all_data_list
        
        else:
            if resp.json()['meta']['is_end']:
                all_data_list.extend(resp.json()['documents'])
                return all_data_list
            # 아니면 다음 페이지로 넘어가서 데이터 저장
            else:
                page_num += 1
                all_data_list.extend(resp.json()['documents'])

                print(all_data_list[0])

def overlapped_data(start_x, start_y, step, end_x, end_y):
    # 최종 데이터가 담길 리스트
    overlapped_result = []

    # 지도를 사각형으로 나누면서 데이터 받아옴
    for i in np.linspace(start_x, end_x, 10):  
        end_x = start_x + step
        initial_start_y = start_y
        for j in np.linspace(start_y, end_y, 10):
            end_y = initial_start_y + step
            each_result= whole_region(start_x,initial_start_y,end_x,end_y)
            overlapped_result.extend(each_result)
            initial_start_y = end_y
        start_x = end_x
    
    return overlapped_result


start_y = 37.46
start_x = 126.79
step = 0.01
end_y =  37.68
end_x = 127.21

datas = overlapped_data(start_x, start_y, step, end_x, end_y)
results = list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(d.items())) for d in datas)))


places = np.array(results)
placeList = []
for place in places:
    if "서울" not in place['road_address_name']:
        continue
    placeList.append(list(place.values()))


placeList = np.array(placeList)
placeList = np.delete(placeList, [1,2,4,5,6], axis=1)

df = pd.DataFrame(placeList, columns = ['adress', 'category', 'place name',
                                                            'place url', 'road adress name'
                                                            ,'x', 'y'])

df.to_csv('places.csv', encoding = 'utf-8-sig')


'''
step = 0.005
xstart = 126.88316487661238
ystart = 37.69539100550791
xend = 126.91195598852781
yend = 37.7186471618891


places = list()
placeList = list()
logList = list()


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
print(newplaces)
newplaces = np.delete(newplaces, [1,2,4,5,6], axis=1)

df = pd.DataFrame(newplaces, columns = ['adress name', 'category', 'place name',
                                        'place url', 'road adress name',
                                        'x', 'y'])

df.to_csv('places.csv', encoding = 'utf-8-sig')
'''