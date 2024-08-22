import os
import json
import numpy as np
from dotenv import load_dotenv
from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

options = webdriver.ChromeOptions()
# 브라우저를 띄우지 않고 크롤링하는 옵션
options.add_argument('--headless')

WAIT_TIME = 30


def cve_crawler():
    # 기사 url 수집
    def cve_href_crawling():
        href_browser = webdriver.Chrome(options=options)
        href_wait = WebDriverWait(href_browser, WAIT_TIME)

        try:
            href_browser.get(os.getenv('CNV_URL'))

            href_list = []

            # 링크 가져오기
            while True:
                items = href_browser.find_elements(By.CSS_SELECTOR, '.media-content > .content > .title > a')

                for item in items:
                    href = item.get_attribute('href')
                    href_list.append(href)
                try:
                    href_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pagination-next'))).click()
                    href_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.content .title')))
                except Exception as e:
                    print(e)
                    break
        finally:
            href_browser.quit()

        return href_list

    url_list = cve_href_crawling()

    browser = webdriver.Chrome(options=options)
    wait = WebDriverWait(browser, WAIT_TIME)

    data = np.array([])

    for url in url_list:
        browser.get(url)

        # 로딩 대기
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.content > .title')))

        article_id = ''.join(url.split('/')[-4:])
        title = browser.find_element(By.CSS_SELECTOR, '.content > .title')
        date = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/span/div/time')
        content = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/div')

        data = np.append(data, np.array([{'source': 'cve', 'article_id': article_id, 'title': title.text,
                                          'published_at': date.get_attribute('datetime'),
                                          'content': content.get_attribute('innerHTML'),
                                          'content_text': content.text}]))

        print(title.text)

    return np.flip(data)


def cnnvd_crawler():
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, WAIT_TIME)

    try:
        # cnnvd 사이트 접속
        browser.get(os.getenv('CNNVD_URL'))

        data = np.array([])

        while True:
            # 로딩 상태가 아닐 때까지 대기
            wait.until(lambda browser: browser.find_element(By.CLASS_NAME, 'el-loading-mask').value_of_css_property(
                'display') == 'none')

            for request in browser.requests:
                if request.response and ("/netSecurityList" in request.url):
                    print(json.loads(request.response.body)['data']['pageIndex'])

                    # 이전 request 기록 삭제
                    del browser.requests
                    break

            try:
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-next'))).click()
            except Exception as e:
                print(e)
                break
    finally:
        browser.quit()

        # while True:
        #     for request in browser.requests:
        #         if request.response and ("/netSecurityList" in request.url):
        #             for res in json.loads(request.response.body)['data']['records']:
        #                 data = np.append(data, np.array(
        #                     [{'source': 'cnnvd', 'article_id': res['netSecurityId'], 'title': res['netSecurityName'],
        #                       'published_at': res['publishTime'],
        #                       'content': res['enclosureContent'], 'content_text': res['contentStr']}]))
    # finally:
    #     browser.quit()
    #
    # return np.flip(data)

    # while True:
    #     try:
    #         # 로딩 대기
    #         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.content .content-title')))
    #
    #         # netSecurityList response 값 가져오기
    #         for request in browser.requests:
    #             if request.response and ("/netSecurityList" in request.url):
    #                 for res in json.loads(request.response.body)['data']['records']:
    #                     data = np.append(data, np.array(
    #                         [{'source': 'cnnvd', 'article_id': res['netSecurityId'], 'title': res['netSecurityName'],
    #                           'published_at': res['publishTime'],
    #                           'content': res['enclosureContent'], 'content_text': res['contentStr']}]))
    #
    #         wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.el-pagination .btn-prev'))).click()
    #     except Exception as e:
    #         print(e)
    #         break

    # return np.flip(data)
