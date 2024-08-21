from services.crawler import *
from services.translate import *

cve_news = cve_crawling()
# cnnvd_news = cnnvd_crawling()

# cve 번역
for news in cve_news:
    print(translate_text(news['title']))
    print(translate_text(news['description']))
    print(translate_text(news['content']))

# cnnvd 번역
# for news in cnnvd_news:
#     print(translate_html_content(news['enclosure_content']))
