from config import config
# 订单不存在 或错误
TRADE_ERR = 0
# 未支付
TRADE_UNPAY = 1
# 支付ok
TRADE_PAY_OK = 2
# 支付失败
TRADE_PAY_FAIL = 3

API_URL = 'https://api.weixin.qq.com/'
PAY_URL = 'https://api.mch.weixin.qq.com/pay/'
WECHAT_TO_CARD_URL = 'https://api.mch.weixin.qq.com/mmpaysptrans/pay_bank'
WECHAT_RSA_PUB_KEY_URL = 'https://fraud.mch.weixin.qq.com/risk/getpublickey'
PAY_GOODDESC = ''

class WST():
    NAME = ''
    APP_ID = ''
    API_URL = 'https://api.weixin.qq.com/'
    APP_SECRET = ''
    WECHAT_MCH_ID = ''
    WECHAT_MCH_KEY = ''
    REDIRECT_URI = config.logical_url + ''
    REDIRECT_BIND_URL = ''
    JUMP_URL = 'your jump url'  # 这里是登陆以后的跳转，是否使用取决于你自己的需求
    PLAYER_PAY_REDIRECT = config.logical_url + ''
    pub_path = ''
    cert_path = ''
    key_path = ''
    nonce_length = 15