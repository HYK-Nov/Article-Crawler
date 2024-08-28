import json
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

load_dotenv()

# Use a service account.
service_account_info = json.loads(os.getenv('FIRESTORE_KEY'))
cred = credentials.Certificate(service_account_info)

app = firebase_admin.initialize_app(cred)

db = firestore.client()

__all__ = ['db']
