from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, db_name="CryptoResearchDB"):
        # Kết nối tới MongoDB localhost (mặc định cổng 27017)
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]