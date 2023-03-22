import pymongo
from bson.objectid import ObjectId

class DBConnector:
    def __init__(self):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        self.db = client['mwizz_db']

    def db_insert(self, collection, data):
        print(data)
        result = self.db[collection].insert_one(data)
        return str(result.inserted_id)
    
    def db_fetch_status_for_id(self, collection, id):
        document_id = ObjectId(id)  
        data = self.db[collection].find_one({"_id": document_id})
        print(data)
        return (data['status'])

    def db_fetch_all_request_details(self, collection, product_name):
        print(product_name)
        data = list(self.db[collection].find({"productName": product_name}))
        for item in data:
            item["_id"] = str(item["_id"])
        return data
        