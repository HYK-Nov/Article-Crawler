from firebase_admin.firestore import firestore
from firebase.client import db


def get_article_id():
    articles_ref = db.collection("articles")
    docs = articles_ref.select(['article_id']).get()

    return [doc.to_dict().get('article_id') for doc in docs]


def insert_data(data_list):
    try:
        article_id_list = get_article_id()
        document = len(article_id_list)

        for data in data_list:
            document += 1
            doc_ref = db.collection("articles").document(str(document))
            doc_ref.set(data | {'created_at': firestore.SERVER_TIMESTAMP, 'view_count': 0, 'hot_score': 0})

        print("Data Inserted")

    except Exception as e:
        print(e)
