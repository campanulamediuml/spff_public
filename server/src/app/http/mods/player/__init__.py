from app.http.mods.player.handlers.player_login import player_login, player_logout

route_list = [
    (r'/player/login', player_login),
    (r'/player/logout', player_logout),
]
