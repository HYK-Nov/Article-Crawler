import os
import json
from dotenv import load_dotenv
from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

options = webdriver.ChromeOptions()
# 브라우저를 띄우지 않고 크롤링하는 옵션
options.add_argument('--headless=new')
# 자동화 탐지 방지
options.add_argument('disable-blink-features=AutomationControlled')
# 자동화 표시 제거
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 자동화 확장 기능 비활성화
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(
    'user-agent=options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")')

# 최대 대기 시간
WAIT_TIME = 180


# 기사 url 수집
def cve_href_crawling():
    browser = webdriver.Chrome(options=options)
    wait = WebDriverWait(browser, WAIT_TIME)

    href_list = []

    try:
        browser.get(os.getenv('CNV_URL'))

        # 링크 가져오기
        while True:
            items = browser.find_elements(By.CSS_SELECTOR, '.media-content > .content > .title > a')

            for item in items:
                href = item.get_attribute('href')
                href_list.append(href)

            try:
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pagination-next'))).click()
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.content .title')))
            except Exception as e:
                print('CVE url error: ' + str(e))
                break
    finally:
        browser.quit()
        return list(reversed(href_list))


def cve_crawler():
    print('CVE 크롤링 시작')

    url_list = cve_href_crawling()

    browser = webdriver.Chrome(options=options)
    wait = WebDriverWait(browser, WAIT_TIME)

    data = []

    try:
        for url in url_list:
            browser.get(url)

            # 로딩 대기
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.content > .title')))

            article_id = ''.join(url.split('/')[-4:])
            title = browser.find_element(By.CSS_SELECTOR, '.content > .title')
            date = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/span/div/time')
            content = browser.find_element(By.XPATH, '//*[@id="cve-main-page-content"]/div/div')

            data.append({'source': 'cve',
                         'article_id': article_id,
                         'title': title.text,
                         'published_at': date.get_attribute('datetime'),
                         'content_html': content.get_attribute('innerHTML'),
                         'content_text': content.text})
    except Exception as e:
        print('CVE error: ' + str(e))
    finally:
        print('CVE 크롤링 종료')
        browser.quit()
        return data


def cnnvd_crawler():
    print('CNNVD 크롤링 시작')

    browser = webdriver.Chrome(options=options)
    wait = WebDriverWait(browser, WAIT_TIME)

    data = []

    try:
        # cnnvd 사이트 접속
        browser.get(os.getenv('CNNVD_URL'))

        while True:
            # 로딩 상태가 아닐 때까지 대기
            wait.until(lambda driver: driver.find_element(By.CLASS_NAME, 'el-loading-mask').value_of_css_property(
                'display') == 'none')

            for request in browser.requests:
                if request.response and ("/netSecurityList" in request.url):
                    for res in json.loads(request.response.body)['data']['records']:
                        data.append({'source': 'cnnvd',
                                     'article_id': res['netSecurityId'],
                                     'title': res['netSecurityName'],
                                     'published_at': res['publishTime'],
                                     'content_html': res['enclosureContent'],
                                     'content_text': res['contentStr']})

                    # 이전 request 기록 삭제
                    del browser.requests
                    break

            try:
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-next'))).click()
            except Exception as e:
                # 진행 불가 시 반복문 종료
                break

    except Exception as e:
        print('CNNVD error: ' + str(e))
    finally:
        print('CNNVD 크롤링 종료')
        browser.quit()
        return list(reversed(data))
