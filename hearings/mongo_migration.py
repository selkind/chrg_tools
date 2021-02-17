from mongo_connect import MongoConnect

connection = MongoConnect.get_connection()
db = connection.test
cursor = db.voteview_members.find()
unique_keys = {}
for i in cursor:
    for j in i.keys():
        if j not in unique_keys:
            unique_keys[j] = 1
        else:
            unique_keys[j] += 1

for i in sorted(unique_keys.keys()):
    print(i, unique_keys[i])
