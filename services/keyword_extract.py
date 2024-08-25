import numpy as np
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer

okt = Okt()


def extract_noun(text):
    tagged_words = okt.pos(text, stem=True, norm=True)

    return ' '.join([word for word, pos in tagged_words if pos == 'Noun' or pos == 'Alpha'])


def extract_tag(text, limit=5):
    # 불용어 제거
    vectorizer = TfidfVectorizer(stop_words='english')

    try:
        matrix = vectorizer.fit_transform([extract_noun(text)])

        score = np.array(matrix.sum(axis=0)).flatten()
        words = vectorizer.get_feature_names_out()

        words_score = sorted(list(zip(words, score)), key=lambda x: x[1], reverse=True)

        return [word for word, pos in words_score[:limit]]
    except ValueError as e:
        # 값이 없는 경우 기본 값 리턴
        return ['보안']
