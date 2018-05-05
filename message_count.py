from pymongo import MongoClient
from bson.son import SON

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.qq_database
    collection = db.test_collection

    pipeline = [
        {"$group" : {"_id":"$userid", "count":{"$sum":1}, "username": {"$last": "$username"}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
    ]

    result = collection.aggregate(pipeline)
    for doc in result:
        print(doc)
