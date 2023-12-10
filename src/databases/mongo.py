from pymongo import MongoClient
from bson import ObjectId
import os

# Configuration MongoDB
class MongoDB:
    # MongoDB configuration
    mongo_uri = os.getenv('MONGO_DB_URI')
    database_name = os.getenv('DATABASE_NAME')
    collection_name = os.getenv('COLLECTION_NAME')
    if not mongo_uri or not database_name or not collection_name:
        raise ValueError("MONGO_DB_URI, DATABASE_NAME, or COLLECTION_NAME environment variables are not set.")
    
    def __init__(self):
        client = MongoClient(self.mongo_uri)
        db = client[self.database_name]
        self.collection = db[self.collection_name]

    def find_all(self, projection=None):
        projection = projection or {'_id': 0}
        return list(self.collection.find({}, projection))

    def create_item(self, item):
        self.collection.insert_one(item)

    def delete_items(self):
       self.collection.drop()

    def delete_item(self, uri):
        self.collection.delete_one({'uri': uri})
