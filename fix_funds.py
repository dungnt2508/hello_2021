from pymongo import MongoClient

client = MongoClient(port=27017)
db = client.app_demo

db.funds.update_many({"collect.source.source":"Anh Hiếu"},{"$set":{"collect.source.source":"Anh Quân"}})
db.funds.update_many({"spent.source.source":"Anh Hiếu"},{"$set":{"spent.source.source":"Anh Quân"}})
db.funds.update_many({"collect.source.source":"Anh Thiệu"},{"$set":{"collect.source.source":"Khác"}})
db.funds.update_many({"spent.source.source":"Anh Thiệu"},{"$set":{"spent.source.source":"Khác"}})

print("done !")