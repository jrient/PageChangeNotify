'''
负责分配推送
'''
from .WeixinNotify import WeixinNotify
from .FTQQNotify import FTQQNotify

# 微信公众号推送
SET_WEIXIN_notify = 'weixin_notify'
# server酱推送
SET_FTQQ_notify = 'ftqq_notify'

class Handler:
    
    def __init__(self, notify_set, notify_config, send_to):
        if notify_set not in notify_config:
            print('请配置 notify_set')
            exit()
        self.notify_set = notify_set
        self.notify_config = notify_config[notify_set]
        self.send_to = send_to[notify_set]
        
    def send_notify(self, title, content):
        if self.notify_set == SET_WEIXIN_notify:
            notify_module = WeixinNotify(self.notify_config)
            return notify_module.send_msg(self.send_to, notify_module.register_msg(title, content))
        elif self.notify_set == SET_FTQQ_notify:
            return FTQQNotify().send_msg(self.send_to, title, content)
        else:
            return None