from services.crawler import *
from services.translate import *
from services.keyword_extract import extract_tag

# cve 크롤링
cve_news = cve_crawler()
# cnnvd 크롤링
cnnvd_news = cnnvd_crawler()

# cve 번역
translated_news_cve = [
    news | {
        'title': translate_text(news['title']),
        'content_html': (content_cve := translate_html_content(news['content_html'])[0]),
        'content_text': content_cve[1],
    }
    for news in cve_news
]

# cnnvd 번역
translated_news_cnnvd = [
    news | {
        'title': translate_text(news['title']),
        'content_html': (content_cnnvd := translate_html_content(news['content_html'])[0]),
        'content_text': content_cnnvd[1],
    }
    for news in cnnvd_news
]

# cve 태그 N개 생성 (default: 10)
for news in translated_news_cve:
    print(extract_tag(news['content_text']))

# cnnvd 태그 N개 생성 (default: 10)
for news in translated_news_cnnvd:
    print(extract_tag(news['content_text']))
