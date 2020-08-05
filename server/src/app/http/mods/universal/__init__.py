from app.http.mods.universal.handlers.search_by_kw import search_handler
from app.http.mods.universal.handlers.search_by_time import search_by_time_handler
from app.http.mods.universal.handlers.searche_by_id import search_by_case_id
# from app.http.mods.universal.handlers.upload_info import upload_handler
from app.http.mods.universal.handlers.wechat_auth import get_wechat_cfg,get_appid

route_list = [
    (r'/uni/getwechatcfg', get_wechat_cfg),
    (r'/uni/getappid', get_appid),

    (r'/uni/searchbytime', search_by_time_handler),
    (r'/uni/searchbykw', search_handler),
    (r'/uni/searchbyid',search_by_case_id),
    # (r'/uni/upload', upload_handler),
]