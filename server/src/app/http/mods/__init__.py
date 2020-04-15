from app.http.mods import test_mod
from app.http.mods import player
from app.http.mods import admin
from app.http.mods import universal


def create_route():
    route_list = []
    route_list.extend(test_mod.route_list)
    route_list.extend(player.route_list)
    route_list.extend(admin.route_list)
    route_list.extend(universal.route_list)

    return route_list
