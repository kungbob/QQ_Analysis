# Testing the parsing function
import re
import datetime

line = "0000-00-00 00:00:00 abc( )(123456789)\n"
message_single_pattern = '^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (.*)((\(|<)(.*)(\)|>))\n$'

message_date = re.match(message_single_pattern, line).group(1)
message_time = re.match(message_single_pattern, line).group(2)
message_datetime = message_date + "T" + message_time + "Z"
print(message_datetime)
message_datetime_obj = datetime.datetime.strptime(message_datetime, "%Y-%m-%dT%H:%M:%SZ")
print(message_datetime_obj)

message_user = re.match(message_single_pattern, line).group(3)
print(message_user)
# Message_id
message_user_id = re.match(message_single_pattern, line).group(4)
print(message_user_id)
message_user_id = message_user_id[1:-1]
print(message_user_id)
