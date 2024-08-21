import time
import json
from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def cve_crawler():
    def cve_href_crawling():
        browser = webdriver.Chrome()
        wait = WebDriverWait(browser, 10)

        try:
            browser.get('https://www.cve.org/Media/News/AllNews')

            link_list = []

            # 링크 가져오기
            while True:
                items = browser.find_elements(By.CSS_SELECTOR, '.media-content > .content > .title > a')

                for item in items:
                    href = item.get_attribute('href')
                    link_list.append(href)
                try:
                    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pagination-next'))).click()
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.content > .title')))
                except Exception as e:
                    print(e)
                    break
        finally:
            browser.quit()

        return link_list

    link_list = cve_href_crawling()

    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 30)

    data = []

    for link in link_list:
        browser.get(link)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.content > .title')))

        article_id = ''.join(link.split('/')[-4:])
        title = browser.find_element(By.CSS_SELECTOR, '.content > .title')
        date = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/span/div/time')
        content = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/div')

        data.append(
            {'type': 'cve', 'article_id': article_id, 'title': title.text,
             'published_at': date.get_attribute('datetime'), 'content': content.get_attribute('innerHTML'),
             'content_text': content.text})

    return data


def cnnvd_crawler():
    browser = webdriver.Chrome()

    data = []

    # cnnvd 사이트 접속
    browser.get('https://www.cnnvd.org.cn/home/netSecurity')

    # 로딩 대기
    time.sleep(15)

    # netSecurityList response 값 가져오기
    for request in browser.requests:
        if request.response and ("/netSecurityList" in request.url):
            data = [{'type': 'cnnvd', 'article_id': res['netSecurityId'], 'title': res['netSecurityName'],
                     'published_at': res['publishTime'],
                     'content': res['enclosureContent'], 'content_text': res['contentStr']} for res in
                    json.loads(request.response.body)['data']['records']]

    browser.quit()

    return data
