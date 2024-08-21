from selenium import webdriver
from selenium.webdriver.common.by import By

import time

browser = webdriver.Chrome()

# 사이트 접속
browser.get('https://www.cve.org/Media/News/AllNews')

news_data = []

# 데이터 크롤링
for i in range(1, 11):
    browser.find_element(By.XPATH,
                         '//*[@id="cve-main-page-content"]/div/div[{}]/article/div/div/h2/a'.format(i)).click()

    id = ''.join(browser.current_url.split('/')[-4:])
    title = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/h1')
    date = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/span/div/time')
    content = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/div')

    news_data.append({'id': id, 'title': title.text, 'date': date.get_attribute('datetime'), 'content': content.text})

    browser.back()

    # 3초 딜레이
    time.sleep(3)

for news in news_data:
    print(news['id'], news['title'], news['date'], news['content'])
