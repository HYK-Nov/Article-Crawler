from crawler import *
from translate import *

cve_news = cve_crawling()
cnnvd_news = cnnvd_crawling()

for news in cve_news:
    print(ko_translate('en', news['title']))
    print(ko_translate('en', news['content']))
