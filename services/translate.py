from bs4 import BeautifulSoup
from googletrans import Translator

translator = Translator()


def translate_text(text, dest_lan='ko'):
    res = translator.translate(text, dest=dest_lan)
    return res.text


def translate_html_content(html_content, dest_lan='ko'):
    soup = BeautifulSoup(html_content, 'html.parser')

    for element in soup.find_all(text=True):
        if element.strip():
            translated_text = translate_text(element, dest_lan=dest_lan)
            element.replace_with(translated_text)

    return str(soup)
