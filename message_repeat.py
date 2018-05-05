from pymongo import MongoClient
from bson.son import SON
from collections import OrderedDict
import re

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.qq_database
    collection = db.test_collection

    pipeline = [
        {"$group" : {"_id":"$message", "count":{"$sum":1}, "repeater_id":{"$push": "$userid"}}},
        {"$sort": SON([("count", -1), ("_id", -1)])},
        {"$match": {"_id": {"$not": re.compile(".*[图片].*")}, "count": {"$gte": 10}}}
    ]

    result = collection.aggregate(pipeline, allowDiskUse=True)
    repeater_dict = dict()
    for doc in result:
        for userid in doc["repeater_id"]:
            if userid in repeater_dict:
                repeater_dict[userid] += 1
            else:
                repeater_dict[userid] = 1

    '''
    for key, value in repeater_dict.items():
        print(key, value)

    '''

    repeater_order_dict = OrderedDict(sorted(repeater_dict.items(), key=lambda x: x[1], reverse=True))

    for key, value in repeater_order_dict.items():
        pipeline_2 = [
            {"$match": {"userid": key}},
            {"$sort": SON([("_id", -1)])},
            {"$limit": 1}
        ]
        result_2 = collection.aggregate(pipeline_2)
        for user in result_2:
            username = user["username"]
        print(key, username, value)
