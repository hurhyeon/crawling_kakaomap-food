import requests

searching = '홍대 스타벅스'

url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
headers = {
    "Authorization": "KakaoAK cd12239e86cd67a7fdc5c228fe77162d"
}
places = requests.get(url, headers = headers).json()['documents']
places

print(places)
