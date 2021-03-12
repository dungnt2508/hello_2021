# import re
#
#
# def no_accent_vietnamese(s):
#     s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
#     s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
#     s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
#     s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
#     s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
#     s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
#     s = re.sub(r'[ìíịỉĩ]', 'i', s)
#     s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
#     s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
#     s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
#     s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
#     s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
#     s = re.sub(r'[Đ]', 'D', s)
#     s = re.sub(r'[đ]', 'd', s)
#     return s
#
#
# def create_user_name(s):
#     str1 = no_accent_vietnamese(s).lower().split(" ")
#
#     user_name = str1[-1]
#     for i in str1:
#         if i != str1[-1]:
#             user_name += i[0]
#     print(user_name)
#     return user_name
#
# if __name__ == '__main__':
#     user_name = create_user_name("Nguyễn Tuấn Anh Admin")
#
# # Output
# # Viet Nam Dat Nuoc Con Nguoi
# # Welcome to Vietnam !
# # VIET NAM DAT NUOC CON NGUOI


str = "ntpdunggmail.com"
print('@' in str)



from datetime import datetime
start_date = datetime.strptime('2020-03-10', "%Y-%m-%d")
end_date = datetime.strptime('2021-03-25', "%Y-%m-%d")
print((end_date-start_date).days)