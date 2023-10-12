'''
微信公众号消息
https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html

配置如下
{
    "app_id" : "x",
    "app_secret" : "x",
    "template_id" : "xx"
}
'''
import requests,json
from datetime import datetime

class WeixinNotify:
    def __init__(self, config):
        if 'app_id' not in config or 'type' not in config or 'app_secret' not in config or 'template_id' not in config or config['app_id'] == '' or config['app_secret'] == '':
            print('请配置 app_id, app_secret, template_id')
            exit()
        self.app_id = config['app_id']
        self.app_secret = config['app_secret']
        self.template_id = config['template_id']
        self.template_msg = config['template_msg']
        self.type = config['type']
        self.access_token = self.get_access_token()
        self.msg_data = {}

    # 生成模板消息
    def register_msg(self, data):
        self.msg_data = data
        original_json = json.dumps(self.template_msg)
        replacement_dict = {
            "{{__TITLE__}}": data['title'],
            "{{__DATETIME__}}": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "{{__CONTENT__}}": data['content'][:100],
            "{{__URL__}}": data['url']
        }
        for placeholder, replacement in replacement_dict.items():
            original_json = original_json.replace('"%s"' % placeholder, '"%s"' % replacement)
        return json.loads(original_json)

    # 获取access_token
    def get_access_token(self):
        params = {
            "grant_type" : "client_credential",
            "appid" : self.app_id,
            "secret" : self.app_secret
        }
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        r = requests.get(url, params=params).json()
        if 'access_token' not in r:
            print('获取access_token失败')
            print('错误信息为: %s' % r)
            exit()
        return r['access_token']
    
    def send_msg(self, openid_list, msg):
        msg_data = self.register_msg(msg)
        if self.type == 'tmpl':
            self.send_tmpl_msg(openid_list, msg_data)
        elif self.type == 'subscription':
            self.send_subscription_msg(openid_list, msg_data)
    
    # 发送订阅消息
    def send_subscription_msg(self, openid_list, msg):
        url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/bizsend'

        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "access_token" : self.access_token,
        }
        for openid in openid_list:
            data = json.dumps({
                "access_token" : self.access_token,
                "touser" : openid,
                "template_id" : self.template_id,
                "page": self.msg_data['url'],
                "data" : msg 
            })
            print(data)
            result = requests.post(url, params=params, data=data, headers=headers)
            print('微信公众号订阅推送：openid: %s, result: %s' % (openid, result.json()))
    
    
    # 发送模板消息
    def send_tmpl_msg(self, openid_list, msg):
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send'
        params = {
            "access_token" : self.access_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        for openid in openid_list:
            data = json.dumps({
                "touser" : openid ,
                "template_id" : self.template_id,
                "data" : msg
            })
            result = requests.post(url, params=params, data=data, headers=headers)
            print('微信公众号推送：openid: %s, result: %s' % (openid, result.json()))