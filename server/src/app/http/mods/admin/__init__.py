from app.http.mods.admin.handlers.block_issue import block_info
from app.http.mods.admin.handlers.upload import upload_handler
from app.http.mods.admin.handlers.change_pw import change_pw
from app.http.mods.admin.handlers.admin_login import admin_login, admin_logout

route_list = [
    (r'/admin/login', admin_login),
    (r'/admin/logout', admin_logout),

    (r'/admin/upload', upload_handler),
    (r'/admin/change_pw',change_pw),
    (r'/admin/block',block_info)
]
# 管理员
