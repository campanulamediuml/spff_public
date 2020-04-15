from app.http.mods.test_mod.handlers.test import test, onlineadmin

# from app.http.mods.test_mod.handlers.ws_sender import ws_sender


route_list = [
    (r'/test/test', test),
    (r'/test/onlineadmin', onlineadmin)
    # (r'/test/ws_sender', ws_sender),
]