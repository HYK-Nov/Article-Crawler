from services.crawler import *
from services.translate import *
from services.keyword_extract import extract_tag
from firebase.snippets import insert_data, get_article_id

article_id_list = get_article_id()

# cve 크롤링
cve_news = cve_crawler()
# cnnvd 크롤링
cnnvd_news = cnnvd_crawler()

cve_news = [news for news in cve_news if news['article_id'] not in article_id_list]
cnnvd_news = [news for news in cnnvd_news if news['article_id'] not in article_id_list]

# cve
if len(cve_news) > 0:
    # cve 번역
    print('cve_번역')
    for news in cve_news:
        news['title'] = translate_text(news['title'])
        news['content_html'], news['content_text'] = translate_html_content(news['content_html'])
    print('cve_번역 종료')

    # cve 태그 N개 생성 (default: 5)
    print('cve_태그')
    for news in cve_news:
        news.update({'tag': extract_tag(news['content_text'])})
    print('cve_태그 종료')

    insert_data(cve_news)

# cnnvd
if len(cnnvd_news) > 0:
    # cnnvd 번역
    print('cnnvd_번역')
    for news in cnnvd_news:
        news['title'] = translate_text(news['title'])
        news['content_html'], news['content_text'] = translate_html_content(news['content_html'])
    print('cnnvd_번역 종료')

    # cnnvd 태그 N개 생성 (default: 5)
    print('cnnvd_태그')
    for news in cnnvd_news:
        news.update({'tag': extract_tag(news['content_text'])})
    print('cnnvd_태그 종료')

    insert_data(cnnvd_news)
