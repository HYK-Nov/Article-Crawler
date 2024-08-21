from services.crawler import *
from services.translate import *

# cve 크롤링
cve_news = cve_crawler()
# cnnvd 크롤링
cnnvd_news = cnnvd_crawler()

# cve 번역
for news in cve_news:
    print(translate_text(news['title']))
    print(translate_html_content(news['content']))

# cnnvd 번역
for news in cnnvd_news:
    print(translate_text(news['title']))
    print(translate_html_content(news['content']))
