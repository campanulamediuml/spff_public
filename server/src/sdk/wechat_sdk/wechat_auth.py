from urllib import request
import time
import json
from common.common import common_tools
from config import wechat_config
from config.wechat_config import WST


class wechat_auth_base(object):
    end_refresh_time = 300
    end_ticket_time = 0
    end_token_time = 0
    auth_ticket = None
    auth_token = None
    auth_token_url = 'cgi-bin/token'
    access_token_url = 'sns/oauth2/access_token'


    timer_type = {
        'ticket': end_ticket_time,
        'token': end_token_time
    }

    def update_ticket_attr(self, auth_ticket=None, sign_time=None, auth_token=None, token_time=None):
        if sign_time != None:
            wechat_auth_base.end_ticket_time = sign_time + int(time.time()) - wechat_auth_base.end_refresh_time
        if token_time != None:
            wechat_auth_base.end_token_time = token_time + int(time.time()) - wechat_auth_base.end_refresh_time

        wechat_auth_base.auth_ticket = auth_ticket
        wechat_auth_base.access_token = auth_token
        return

    def auth_not_expired(self, end_type):
        now = int(time.time())
        if now < wechat_auth_base.timer_type[end_type]:
            return True
        else:
            return False


    # 读取信息

    def get_access_token(self, code=None):
        if code == None:
            access_token = self.get_access_token_without_code()
        else:
            access_token = self.get_access_token_with_code(code)
        return access_token

    def get_access_token_without_code(self):
        if self.auth_not_expired(end_type="token") == True:
            if wechat_auth_base.auth_token != None:
                return wechat_auth_base.auth_token

        url = wechat_config.API_URL + wechat_auth_base.auth_token_url
        params_dict = {
            'grant_type': 'client_credential',
            'appid': WST.APP_ID,
            'secret': WST.APP_SECRET,
        }
        dct = wechat_auth_base.get_value_by_url(url, params_dict)
        if 'access_token' not in dct:
            print('get_access_token err %s' % dct)
            return None

        access_token = dct['access_token']
        token_time = dct['expires_in']
        self.update_ticket_attr(auth_token=access_token, token_time=token_time)
        return access_token
        # 不用code获取access_token

    def get_access_token_with_code(self, code):
        access_info = wechat_auth_base.get_access_info_by_code(code)
        if access_info == None:
            return

        access_token = access_info['access_token']
        return access_token
        # 用code获取

    @staticmethod
    def get_access_info_by_code(code):
        url = wechat_config.API_URL + wechat_auth_base.access_token_url
        args = {
            'appid': WST.APP_ID,
            'secret': WST.APP_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
        access_info = wechat_auth_base.get_value_by_url(url, args)
        if not access_info or 'errcode' in access_info:
            print('err wx_login readDct %s' % access_info)
            return
        return access_info
        # 获取包含accesstoken的信息

    @staticmethod
    def get_value_by_url(url, url_param_dict):
        url = url + '?' + common_tools.dict_to_url_params(url_param_dict)
        response = request.urlopen(url)
        readDct = response.read().decode('utf-8')
        data = json.loads(readDct)
        return data


class wechat_auth_ticket(wechat_auth_base):
    ticket_url = 'cgi-bin/ticket/getticket'

    def __init__(self):
        pass

    def sign_wechat(self, url):
        jsapi_ticket = self.get_jsapi_ticket()
        cfg = self.get_config(jsapi_ticket, url)
        cfg_string = common_tools.sorted_dct_to_string(cfg, need_lower=True)
        cfg['signature'] = common_tools.get_sha1(cfg_string)
        return cfg

    def get_config(self, jsapi_ticket, url):
        data = {
            'jsapi_ticket': jsapi_ticket,
            'nonceStr': common_tools.create_rand_string(15),
            'timestamp': int(time.time()),
            'url': url,
        }
        return data

    def get_jsapi_ticket(self):
        if self.auth_not_expired(end_type='ticket') == True:
            if wechat_auth_base.auth_ticket != None:
                return wechat_auth_base.auth_ticket
        url = wechat_config.API_URL + wechat_auth_ticket.ticket_url
        access_token = self.get_access_token()

        data = {
            'access_token': access_token,
            'type': 'jsapi',
        }
        dct = wechat_auth_base.get_value_by_url(url, data)
        if dct['errcode'] != 0:
            print('err get_jsapi_ticket %s %s' % (url, data))
            return ''

        auth_ticket = dct['ticket']
        sign_time = dct['expires_in']
        self.update_ticket_attr(auth_ticket=auth_ticket, sign_time=sign_time)
        return auth_ticket
        # 返回jsapi认证ticket


class wechat_auth_login(wechat_auth_base):
    wechat_user_info_url = 'sns/userinfo'
    def __init__(self):
        pass

    def login(self, code):
        access_info = wechat_auth_base.get_access_info_by_code(code)
        if access_info == None:
            return

        access_token = access_info['access_token']
        open_id = access_info['openid']
        scope = access_info['scope']

        if scope != 'snsapi_userinfo' and scope != 'snsapi_login':
            print('err wx_login scope readDct %s' % access_info)
            return

        res = self.wechat_get_user_info(access_token, open_id)
        return res

    def wechat_get_user_info(self, access_token, open_id):
        data = self.get_userinfo_by_web(access_token, open_id)
        print('wx_get_userinfo----%s' % data)
        if 'errcode' in data:
            print('err wx_get_userinfo readDct %s' % data)
            return

        nickname = data['nickname'].replace('"', '')
        nickname = nickname.replace("'", "")
        sex = data['sex']
        iconUrl = data['headimgurl']
        openid = data['openid']

        user_info = {
            'nickname': json.dumps(nickname).replace('\\', '\\\\'),
            'sex': sex,
            'avatar': iconUrl,
            'open_id': openid,
        }

        return user_info

    def get_userinfo_by_web(self, access_token, open_id):
        url = WST.API_URL + wechat_auth_login.wechat_user_info_url
        args = {
            'access_token': access_token,
            'openid': open_id,
            'lang': 'zh_CN',
        }
        return wechat_auth_base.get_value_by_url(url, args)


class wechat_auth_api(object):
    wat = wechat_auth_ticket()
    wlg = wechat_auth_login()

    @staticmethod
    def get_wechat_jsapi_ticket(url):
        return wechat_auth_api.wat.sign_wechat(url)

    @staticmethod
    def wechat_login(code):
        return wechat_auth_api.wlg.login(code)

# ===============================旧版静态方法