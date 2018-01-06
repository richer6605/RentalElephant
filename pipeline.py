import pymongo

HOST = "localhost"
PORT = 27017
DATABASE = "rental_elephant"

def getCollection(collection):
    client = pymongo.MongoClient(HOST, PORT)
    database = client[DATABASE]
    collection = database[collection]
    return collection

def updateCollection(documents, collection):
    for d in documents:
        collection.update_many(d, {"$set": d}, upsert=True)
