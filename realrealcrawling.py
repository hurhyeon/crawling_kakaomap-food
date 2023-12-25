import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from time import sleep


options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')

driver = webdriver.Chrome('chromedriver', options=options)
driver.implicitly_wait(5)

data = pd.read_csv("combined.csv")
urls = data['place url']
names = data['place name']

placereviews = []

start = 40000
slicing = 10000
end = start+slicing

for index in range(start, min(len(urls), end)):
  driver.get(url = urls[index])
  place = []
  try:
    reviewcount = driver.find_element(By.XPATH, "//div//div//a//span[@class='color_g']").text
  except:
    continue
  reviewcount = int(reviewcount.strip('()'))
  print(urls[index])

  if reviewcount == 0:
    continue
  placename = names[index]
  try:
    score = driver.find_element(By.XPATH, "//div//em[@class='num_rate']")
  except:
    continue

  

  place.append(index)
  place.append(placename)
  place.append(score)
  print(placename)
  print(score)

  if reviewcount > 3 :
    try:
      morebutton = driver.find_element(By.XPATH, "//div//div//div//div//a[@class='link_more']")
      if morebutton.text == "메뉴 더보기":
        morebutton = driver.find_elements(By.XPATH, "//div//div//div//div//a[@class='link_more']")[1]
      while(morebutton.text == "후기 더보기"):
        morebutton.click()
        sleep(0.1)
    except:
      pass


  reviewerNames = driver.find_elements(By.XPATH, "//div[@class='unit_info']//a")
  reviewScores = driver.find_elements(By.XPATH, "//div[@class='star_info']//div//span[@class='ico_star star_rate']//span")
  reviewerAvg = driver.find_elements(By.XPATH, "//div[@class='unit_info']//span[@class='txt_desc']")
  reviercmts = driver.find_elements(By.XPATH, "//div[@class='comment_info']")

  for rev in range(min(len(reviewerNames),len(reviewScores), len(reviewerAvg), len(reviercmts))):
    review = []
    review.append(index)
    review.append(placename)
    review.append(reviewerNames[rev].text)
    reviewScore = reviewScores[rev].get_attribute('style')
    reviewScore = reviewScore[-5:]
    print(reviewScore)
    
    if reviewScore[0] ==':':
      reviewScore = int(reviewScore[1:3])
    else:
      reviewScore = int(reviewScore[0:3])
    reviewScore /= 20
    
    review.append(reviewScore)


    review.append(reviewerAvg[rev*2+1].text)
    cmd = reviercmts[rev].text
    slicindex = 0
    if len(cmd):
      for textindex in range(len(cmd)-1, 0, -1):
        if cmd[textindex] == '좋':
          slicindex = textindex
          break
    
    cmd = cmd[:slicindex]

    review.append(cmd.replace("더보기", ""))

    print(cmd)
    placereviews.append(review)


npreviews = np.array(placereviews)
df = pd.DataFrame(npreviews, columns=['index', 'place name',
        'reviewer', 'score', 'useravg', 'comment'])
df.to_csv("testreview1.csv", encoding='utf-8-sig')

