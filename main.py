from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()

browser.get('https://www.cve.org/Media/News/AllNews')

news_titles = browser.find_elements(By.XPATH, '//*[@id="cve-main-page-content"]/div/div/article/div/div/h2/a')

for i in news_titles:
    print(i.text)
    print(i.get_attribute('href'))