from pymongo import MongoClient
from datetime import datetime
from datetime import date
from datetime import timedelta

# client = MongoClient("mongodb://127.0.0.1:27017")
# db = client.blog
#
# # Reset.
# db.posts.delete_many({})
#
# # Get today.
# today = datetime.today()
# today_2 = date.today()
# print(today_2)
# print(type(today_2))
#
# dt = datetime.combine(date.today(), datetime.min.time())
#
# print(dt)
# print(type(dt))
#
# # Insert some blog posts.
# db.posts.insert_many([
#     {"title": "Intro Post", "date": today - timedelta(days=200)},
#     {"title": "Taking a Break", "date": today + timedelta(days=100)},
#     {"title": "Goodbye Blog", "date": today},
# ])
#
# # Find posts within last 150 days.
# print("FIND :: RECENT POSTS")
# cursor = db.posts.find({"date": {"$gt": today - timedelta(150)}})
# for doc in cursor:
#     print(doc)
#
# # Find posts more than 180 days ago.
# print("FIND :: OLDER POSTS")
# cursor = db.posts.find({"date": {"$gte": today}})
# for doc in cursor:
#     print(doc)
#

test_list = [{"id": 1, "data": "HappY"},
             {"id": 2, "data": "BirthDaY"},
             {"id": 3, "data": "Rash"}]

# printing original list
print("The original list is : " + str(test_list))

# using list comprehension
# to delete dictionary in list
res = [i for i in test_list if not (i['id'] == 2) and not (i['id'] == 3)]

# printing result
print("List after deletion of dictionary : " + str(res))