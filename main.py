from crawler import *
from translate import *

# cve_news = cve_crawling()
cnnvd_news = cnnvd_crawling_test()

# cve 번역
# for news in cve_news:
#     print(ko_translate('en', news['title']))
#     print(ko_translate('en', news['description']))
#     print(ko_translate('en', news['content']))

# cnnvd 번역
for news in cnnvd_news:
    print(ko_translate('zh-cn', news['title']))
