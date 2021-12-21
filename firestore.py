import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate('firebasepk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

document_ref = db.collection(u'tweet').document(u'DFs7mCkSyt9f6LL7FO9e')

def getOldCases():
    return document_ref.get().to_dict()['cases']

def setOldCases(cases):
    document_ref.update({
        u'cases': cases
    })

