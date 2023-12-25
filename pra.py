# Python3 샘플 코드 #


import requests

url = 'http://openapi.jeonju.go.kr/rest/jeonjufood/getFoodImgList'
params ={'serviceKey' : 'ExXNXy58F3dxtY2qOFNC7vI%2FCNdgppjuspW0e1q8FzEQPDWanhHuIBmdMsCUa84cnPDlnxbGhXpoONfGeiVqkg%3D%3D', 'authApiKey' : '', 'foodUid' : 'ff8080813703462a013711b5bd4104cf' }

response = requests.get(url, params=params)
print(response.content)
