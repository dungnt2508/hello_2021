# # import re
# #
# #
# # def no_accent_vietnamese(s):
# #     s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
# #     s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
# #     s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
# #     s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
# #     s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
# #     s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
# #     s = re.sub(r'[ìíịỉĩ]', 'i', s)
# #     s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
# #     s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
# #     s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
# #     s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
# #     s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
# #     s = re.sub(r'[Đ]', 'D', s)
# #     s = re.sub(r'[đ]', 'd', s)
# #     return s
# #
# #
# # def create_user_name(s):
# #     str1 = no_accent_vietnamese(s).lower().split(" ")
# #
# #     user_name = str1[-1]
# #     for i in str1:
# #         if i != str1[-1]:
# #             user_name += i[0]
# #     print(user_name)
# #     return user_name
# #
# # if __name__ == '__main__':
# #     user_name = create_user_name("Nguyễn Tuấn Anh Admin")
# #
# # # Output
# # # Viet Nam Dat Nuoc Con Nguoi
# # # Welcome to Vietnam !
# # # VIET NAM DAT NUOC CON NGUOI
#
#
# str = "ntpdunggmail.com"
# print('@' in str)
#
#
#
# from datetime import datetime
# start_date = datetime.strptime('2020-03-10', "%Y-%m-%d")
# end_date = datetime.strptime('2021-03-25', "%Y-%m-%d")
# print((end_date-start_date).days)


from datetime import date

today = date.today()
print("Today's date:", today)



pipeline_filter = "[ { '$project': { '_id': 0, 'invoice_id': 1, 'item_kind': 1, 'item_name': 1, 'customer': 1, 'price_pawn': 1, 'rate': 1, 'price_rate': 1, 'from_date': 1, 'to_date': 1, 'user_created': 1, 'date_created': 1, 'status': 1, 'status_invoice': { '$switch': { 'branches': [ { 'case': { '$and': [ { '$lt': [ '$to_date', '%s' ] }, { '$in': [ '$status', [ 1, 2 ] ] } ] }, 'then': 0 }, { 'case': { '$and': [ { '$eq': [ '$to_date', '%s' ] }, { '$in': [ '$status', [ 1, 2 ] ] } ] }, 'then': 1 }, { 'case': { '$and': [ { '$gt': [ '$to_date', '%s' ] }, { '$in': [ '$status', [ 1, 2 ] ] } ] }, 'then': 2 } ], 'default': -1 } } } }, { '$match': { 'status_invoice': {'$toInt':'%s'} } } ]"

pipeline_filter = pipeline_filter%(today,today,today,2)
print(pipeline_filter)


a = "{:,.0f}".format(float(10000))
print(a)