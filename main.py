from services.crawler import *
from services.translate import *
from services.keyword_extract import extract_tag

# cve 크롤링
cve_news = cve_crawler()
# cnnvd 크롤링
cnnvd_news = cnnvd_crawler()

# cve 번역
for news in cve_news:
    news['title'] = translate_text(news['title'])
    news['content_html'], news['content_text'] = translate_html_content(news['content_html'])

# cnnvd 번역
for news in cnnvd_news:
    news['title'] = translate_text(news['title'])
    news['content_html'], news['content_text'] = translate_html_content(news['content_html'])

# cve 태그 N개 생성 (default: 5)
for news in cve_news:
    print(extract_tag(news['content_text']))

# cnnvd 태그 N개 생성 (default: 5)
for news in cnnvd_news:
    print(extract_tag(news['content_text']))
