import base64
import time
import requests
import xmltodict
from common.common import common_tools
from config.wechat_config import *
from data.server import Data

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# doc:https://pay.weixin.qq.com/wiki/doc/api/tools/mch_pay.php?chapter=24_2

CODE_PAY_SUCCESS = 1000
CODE_PAY_FAIL = 1001
CODE_PARAM_ERR = 1002
CODE_FAIL_NO_BANK = 1003
CODE_FAIL_REQ = 1004
CODE_NOT_FIND_TAKE_WITHDRAW_RECORD = 1005

REPLY_STATUS = {
    1000: '请求成功, 支付成功。',
    1001: '请求成功, 支付失败。失败原因：',
    1002: '参数错误',
    1003: '银行卡信息有误',
    1004: '支付请求失败',
    1005: '未查询到该条提现申请',
}

# 微信支付通用工具
# 这个class不应该在文件外发生调用，仅用于继承↓
class wechat_eco_base(object):
    def return_msg(self, code, msg=''):
        return {
            'code': code,
            'msg': REPLY_STATUS[code] + msg
        }

    def create_md5_sign(self, dct):
        StringA = common_tools.sorted_dct_to_string(dct)
        StringA += '&key=' + WST.WECHAT_MCH_KEY
        md5_upper = common_tools.get_md5(StringA).upper()
        return md5_upper
        # 通过wechat mchkey进行签名

# ===================微信打款
class wechat_pay_to_card(wechat_eco_base):
    def __init__(self):
        self.api_url = WECHAT_TO_CARD_URL
        self.rsa_url = WECHAT_RSA_PUB_KEY_URL
        self.cert_path = WST.cert_path
        self.key_path = WST.key_path

    def pay_money(self, amount, account_number,bank_code,real_name):
        xml_data = self.make_req_data(amount,account_number,bank_code,real_name)
        if xml_data == None:
            self.return_msg(CODE_FAIL_NO_BANK)
            return

        res = self.request_api(xml_data)
        return res

    def request_api(self, xml_data):
        response = requests.post(self.api_url, data=xml_data, cert=(self.cert_path, self.key_path))
        content = response.content
        # print(content)
        content = xmltodict.parse(content, encoding='utf-8')['xml']
        # print('content', content)
        reply = {}
        reply['code'] = 0
        if content['return_code'] == 'SUCCESS':
            # 请求成功
            if content['result_code'] == 'SUCCESS':
                # 支付成功
                return_msg = content['return_msg']
                return self.return_msg(CODE_PAY_SUCCESS, return_msg)

            else:
                # 支付失败
                return_msg = content['err_code_des']  # 失败原因
                return self.return_msg(CODE_PAY_FAIL, return_msg)
        else:
            return self.return_msg(CODE_FAIL_REQ)

    def make_req_data(self,amount,account_number,bank_code,real_name):
        req_data = {
            'xml': {
                'amount': amount,  # 金额，分
                'bank_code': bank_code,
                'desc': self.create_desc(),
                'enc_bank_no': self.rsa_str(account_number),
                'enc_true_name': self.rsa_str(real_name),
                'mch_id': WST.WECHAT_MCH_ID,
                'nonce_str': common_tools.create_rand_string(WST.nonce_length),
                'partner_trade_no': self.get_trade_no(),
            }
        }
        stringSignTemp = req_data['xml']
        req_data['xml']['sign'] = self.create_md5_sign(stringSignTemp)
        req_xml = xmltodict.unparse(req_data).split('\n')[1]
        return req_xml

    def create_desc(self):
        return 'no_desc'

    # 订单号，唯一
    def get_trade_no(self):
        trade_no = str(int(time.time()))
        trade_no = common_tools.get_md5(trade_no)
        return str(trade_no)

    def get_rsa_public_key(self):
        req_data = {
            'xml': {
                'mch_id': "1541984561",
                'nonce_str': common_tools.create_rand_string(15),
                'sign_type': 'MD5'
            }
        }
        stringSignTemp = req_data['xml']
        req_data['xml']['sign'] = self.create_md5_sign(stringSignTemp)
        req_xml = xmltodict.unparse(req_data).split('\n')[1]
        response = requests.post(self.rsa_url, data=req_xml, cert=(self.cert_path, self.key_path))
        # print(response)
        content = response.text
        content = xmltodict.parse(content, encoding='utf-8')['xml']
        # print(content)
        return content

    # RSA 加密
    def rsa_str(self, str):
        pub = RSA.importKey(open(WST.pub_path, 'rb').read())
        cryp = PKCS1_OAEP.new(pub)
        encrypted = cryp.encrypt(str.encode('utf-8'))

        res = base64.b64encode(encrypted)
        return res.decode('utf-8')

    def get_paid_number(self):
        paid_order_number = str(int(time.time())) + common_tools.create_rand_string(6)
        return paid_order_number

# 微信支付
class wechat_paid_sdk(wechat_eco_base):
    def __init__(self):
        self.trade_type = 'JSAPI'
        self.appid = WST.APP_ID

    def get_unifiedorder(self, remote_ip, openid, gooddesc, money, out_trade_no, buyer):
        # money *= 100
        # 测试
        # money = 1
        # 微信浏览器：公众号支付
        unifieOrderRequest = self.get_req(remote_ip, gooddesc, money, out_trade_no)
        if buyer is not None:
            unifieOrderRequest['notify_url'] = WST.PLAYER_PAY_REDIRECT

        unifieOrderRequest['openid'] = openid
        url = PAY_URL + 'unifiedorder'
        res = self.get_value_by_url_pay_secret(url, unifieOrderRequest)
        return res


    def get_value_by_url_pay_secret(self,url, data):
        data['sign'] = self.create_md5_sign(data)
        data = common_tools.dict_to_xml(data)
        resp = requests.post(url, data.encode('utf-8'),headers={'Content-Type': 'text/xml'})
        readDct = resp.text.encode('ISO-8859-1').decode('utf-8')
        return xmltodict.parse(readDct)['xml']

    def get_req(self, remote_ip, gooddesc, money, out_trade_no):
        unifieOrderRequest = {
            'appid': self.appid,  # 公众账号ID
            'body': PAY_GOODDESC + '-' + gooddesc,  # 商品描述
            'mch_id': WST.WECHAT_MCH_ID,  # 商户号
            'nonce_str': common_tools.create_rand_string(15),  # 随机字符串
            'notify_url': WST.REDIRECT_URI,  # 微信支付结果异步通知地址
            'out_trade_no': out_trade_no,  # 商户订单号
            'sign_type': 'MD5',
            'spbill_create_ip': remote_ip,  # 终端IP
            'total_fee': int(money),  # 标价金额
            'trade_type': self.trade_type,  # 交易类型
        }
        return unifieOrderRequest

# ==================微信支付
class wechat_eco_api(object):
    pu = wechat_paid_sdk()
    pd = wechat_pay_to_card()

    @staticmethod
    def wechat_pay(remote_ip, openid, gooddesc, money, out_trade_no, buyer):
        return wechat_eco_api.pu.get_unifiedorder(remote_ip, openid, gooddesc, money, out_trade_no, buyer)

    # ===================微信打款
    # ↓sdk可调用接口
    @staticmethod
    def pay_to_card(amount,account_number,bank_code,real_name):
        return wechat_eco_api.pd.pay_money(amount,account_number,bank_code,real_name)
    # pd.get_rsa_public_key()
# ↑sdk可调用接口


def create_table():
    colums = [
        ('id', 'int', 'NOT NULL', 'AUTO_INCREMENT', 'primary key'),
        ('bank', 'varchar(512)', 'NOT NULL', 'default ""'),
        ('bank_id', 'int', 'NOT NULL'),
    ]
    Data.create('bank_number', colums)

    # sql = '''INSERT INTO bank_number(bank,bank_id)
    # VALUES('工商银行',1002),('农业银行',1005),('建设银行',1003),
    # ('中国银行',1026),('交通银行',1020),('招商银行',1001),('邮储银行',1066)
    #     ,('民生银行',1006),('平安银行',1010),('中信银行',1021),('浦发银行',1004),
    # ('兴业银行',1009),('光大银行',1022),('广发银行',1027),('华夏银行',1025),
    # ('宁波银行',1056),('北京银行',4836),('上海银行',1024),('南京银行',1054),('长子县融汇村镇银行',4755)
    #     ,('长沙银行',4216),('浙江泰隆商业银行',4051),('中原银行', 4753),('企业银行（中国）', 4761),('顺德农商银行',4036)
    # ,('衡水银行',4752),('长治银行',4756)
    #     ,('大同银行',4767),('河南省农村信用社',4115),('宁夏黄河农村商业银行',4150),('山西省农村信用社',4156),('安徽省农村信用社',4166)
    #     ,('甘肃省农村信用社',4157),('天津农村商业银行',4153),('广西壮族自治区农村信用社',4113)
    #     ,('陕西省农村信用社',4108),('深圳农村商业银行',4076),('宁波鄞州农村商业银行',4052),
    # ('浙江省农村信用社联合社',4764),('江苏省农村信用社联合社',4217),('江苏紫金农村商业银行股份有限公司',4072),
    # ('北京中关村银行股份有限公司',4769),('星展银行（中国）有限公司',4778),('枣庄银行股份有限公司',4766),
    # ('海口联合农村商业银行股份有限公司',4758),('南洋商业银行（中国）有限公司',4763);'''
    # Data.query(sql)


if __name__ == '__main__':
    wechat_eco_api.pay_to_card(000,'1233','1002','test')
    pass
