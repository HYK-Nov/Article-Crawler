import time
import json
from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By


def cve_crawling():
    browser = webdriver.Chrome()

    # 사이트 접속
    browser.get('https://www.cve.org/Media/News/AllNews')

    data = []

    # 데이터 크롤링
    for i in range(1, 11):
        browser.find_element(By.XPATH,
                             '//*[@id="cve-main-page-content"]/div/div[{}]/article/div/div/h2/a'.format(i)).click()

        article_id = ''.join(browser.current_url.split('/')[-4:])
        title = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/h1')
        date = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/span/div/time')
        description = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/div/div[1]/p')
        content = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/div/div[2]/p')

        data.append(
            {'article_id': article_id, 'title': title.text, 'date': date.get_attribute('datetime'),
             'description': description.text, 'content': content.text})

        browser.back()

        # 3초 딜레이
        time.sleep(3)

    return data


def cnnvd_crawling_test():
    browser = webdriver.Chrome()

    data = []

    # cnnvd 사이트 접속
    browser.get('https://www.cnnvd.org.cn/home/netSecurity')

    # 로딩 대기
    time.sleep(15)

    # netSecurityList response 값 가져오기
    for request in browser.requests:
        if request.response and ("/netSecurityList" in request.url):
            data = [{'article_id': res['netSecurityId'], 'title': res['netSecurityName'],
                     'published_at': res['publishTime'],
                     'content': res['enclosureContent'], 'content_text': res['contentStr']} for res in
                    json.loads(request.response.body)['data']['records']]

    return data
