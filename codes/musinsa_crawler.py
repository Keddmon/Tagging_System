from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

path = 'C:/FRS/codes/chromedriver.exe'
driver = webdriver.Chrome(path)

 # 크롤링 시작 페이지
page_num = 1
 # 마지막 페이지 설정
last_page_num = 1
year = '2022'
month = 11
 # 정렬 순서
ordw = 'inc'

'''
submitdate: 최신 순
hit: 조회 순
comment: 댓글 많은 순
inc: 추천 순
d_comment: 최신 댓글 순
'''

styles = ['image'] # 크롤링 할 스타일 설정

'''
'americancasual',
'casual',
'chic',
'dandy',
'formal',
'girlish',
'golf',
'homewear',
'retro',
'romantic',
'sports',
'street',
'gorpcore'
'''

driver.maximize_window()
for style in styles:
    # 자동으로 페이지 이동
    while page_num <= last_page_num: 
        # url = 'https://www.musinsa.com/mz/brandsnap?style_type={}&ordw={}&_m={}&_y={}&p={}#listStart'.format(style, ordw, month, year, page_num)
        url = 'https://www.musinsa.com/mz/brandsnap?ordw={}&_m={}&_y={}&p={}#listStart'.format(ordw, month, year, page_num)
        # url 접속
        driver.get(url)


        img_num = 0
         # 60 고정 : 무신사 이미지 수 60장
        while img_num < 50:
            elements = driver.find_elements(By.CSS_SELECTOR, '.articleImg')
             # 이미지 접속
            elements[img_num].click()
             # url 파싱 
            img_url = driver.find_elements(By.CSS_SELECTOR, '.view-photo')[0].get_attribute('src')

            # 기본적으로 스타일 이름 폴더로 지정, 폴더 없으면 생성
            if not os.path.isdir(style):
                os.mkdir(style)

            try:
                 # img_url에서 이미지 다운로드, style 폴더에 'page_num-img_num.jpg' 형태로 저장
                urlretrieve(img_url, '{}/{}-{}-{}.jpg'.format(style, year, month, img_num))    
             # 오류 시 오류 선언하고 pass
            except :
                print('some error!(style: {}, year: {}, month: {}, img num: {})'.format(style, year, month, img_num))
                pass

             # url 재접속 (오류 최소화)
            driver.get(url)
            img_num += 1
        page_num += 1
     # 하나의 스타일에 대한 cycle이 다 돌고 재설정
    page_num = 1