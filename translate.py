from googletrans import Translator

translator = Translator()


def ko_translate(lan, text):
    res = translator.translate(text, src=lan, dest='ko')
    return res.text
