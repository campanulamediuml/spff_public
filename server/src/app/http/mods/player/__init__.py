from app.http.mods.player.handlers.player_login import player_login, player_logout
from app.http.mods.player.handlers.player_upload import upload_handler

route_list = [
    (r'/player/login', player_login),
    (r'/player/logout', player_logout),
    (r'/player/upload', upload_handler),
]
