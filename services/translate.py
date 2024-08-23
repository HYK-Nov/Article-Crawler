from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='auto', target='ko')


def translate_text(text):
    try:
        if not text:
            return ''

        if len(text) > 500:
            return ' '.join(filter(None, (translator.translate(text[i:i + 500]) for i in range(0, len(text), 500))))
        else:
            return translator.translate(text) or ''
    except Exception as e:
        # 에러인 경우 빈 문자 반환
        return ''


def translate_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    content_text = []

    for element in soup.find_all(text=True):
        translated_text = translate_text(element.strip() or '')
        element.replace_with(translated_text)
        content_text.append(translated_text)

    return str(soup), ' '.join(content_text)
