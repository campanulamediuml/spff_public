import requests
from werkzeug.security import generate_password_hash

from data.server import Data
from common.common import common_tools
# params = {
#     'username':'',
#     'pwhash':common_tools.get_md5('')
# }
# Data.insert('admin',params)
from dbmodel.model import case_content


# def change_pw_hash():
#     all_admin = Data.select('admin',[])
#     for admin in all_admin:
#         pw_hash = admin['pwhash']
#         pw_hash_new = generate_password_hash(pw_hash)
#         params = {
#             'pwhash':pw_hash_new
#         }
#         Data.update('admin',[('id','=',admin['id'])],params)
#
# # print(common_tools.get_md5(a))
# # print(common_tools.get_md5(b))
# def update_db_frame():
#     case_content()
#     all_case = Data.select('case_info',[])
#     for case in all_case:
#         params = {
#             'case_id':case['id'],
#             'content':case['content']
#         }
#         res = Data.select('case_content',[('case_id','=',case['id'])])
#         print(res)
#             # continue
#         Data.insert('case_content',params)
#
#     sql = 'alter table case_info drop column content'
#     Data.query(sql)
#
# if __name__=='__main__':
#     # change_pw_hash()
#     # update_db_frame()
#     pass