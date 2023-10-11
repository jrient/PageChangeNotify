'''
server酱
https://sct.ftqq.com/sendkey

{
    "key" : "xx"
}
'''
import requests

class FTQQNotify:
    def send_msg(self, send_to, title, content):
        for key in send_to:
            url = "https://sctapi.ftqq.com/%s.send" % key
            result = requests.post(url, {
                'title': title,
                'desp': content
            })
            print('server酱推送：openid: %s, result: %s' % (key, result.json()))