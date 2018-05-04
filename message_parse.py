import os
import re
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.qq_database
    collection = db.test_collection

    script_path = os.path.dirname(__file__)
    relative_path = "data\data.txt"
    absolute_path = os.path.join(script_path, relative_path)

    message_group_pattern = '消息分组:(.*)\n'
    message_group_object = '消息对象:(.*)\n'

    group_pattern = ''
    group_object = ''

    with open(absolute_path, encoding="utf8") as fp:
        for line in fp:

            if line == "" or line == "\n" or line == "消息记录（此消息记录为文本格式，不支持重新导入）\n" :
                continue
            elif re.match(message_group_pattern, line):
                group_pattern = re.match(message_group_pattern, line).group(1)
                print(line)
            elif re.match(message_group_object, line):
                group_object = re.match(message_group_object, line).group(1)
                print(line)
            print(group_pattern)
            print(group_object)
