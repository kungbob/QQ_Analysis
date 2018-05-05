from pymongo import MongoClient
import os
import re
import datetime
import time

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.qq_database
    collection = db.test_collection

    script_path = os.path.dirname(__file__)
    relative_path = "data\data.txt"
    absolute_path = os.path.join(script_path, relative_path)

    message_group_pattern = '^消息分组:(.*)\n'
    message_group_object = '^消息对象:(.*)\n'
    message_single_pattern = '^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (.*)((\(|<)(.*)(\)|>))\n$'

    group_pattern = ''
    group_object = ''

    start = time.time()

    with open(absolute_path, encoding="utf8") as fp:
        for line in fp:
            if line == "" or line == "\n" or line == "消息记录（此消息记录为文本格式，不支持重新导入）\n" :
                continue
            elif re.match(message_group_pattern, line):
                group_pattern = re.match(message_group_pattern, line).group(1)
                #print(line)
            elif re.match(message_group_object, line):
                group_object = re.match(message_group_object, line).group(1)
                #print(line)
            elif re.match(message_single_pattern, line):
                #print(line)
                message_date = re.match(message_single_pattern, line).group(1)
                message_time = re.match(message_single_pattern, line).group(2)
                message_datetime = message_date + "T" + message_time + "Z"
                #print(message_datetime)
                message_datetime_obj = datetime.datetime.strptime(message_datetime, "%Y-%m-%dT%H:%M:%SZ")
                #print(message_datetime_obj)

                message_user = re.match(message_single_pattern, line).group(3)
                #print(message_user)
                # Message_id
                message_user_id = re.match(message_single_pattern, line).group(4)
                message_user_id = message_user_id[1:-1]
                #print(message_user_id)

                next_line = fp.readline()
                #print(next_line)
                message = next_line

                insert_db = {"datetime": message_datetime_obj,
                             "username": message_user,
                             "userid": message_user_id,
                             "message": message}

                collection.insert_one(insert_db)
    end = time.time()

    elapsed = end - start
    print(elapsed)
