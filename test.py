import requests,json

config = {
    "appId" : "wxff5f3961d82b6e5b",
    "appSecret" : "b279a88d933460beca076daf4f4abca9",
    "templateId" : "E_PXClp9Usl91OhY-RdIA9reh1iXNFiUnvmPtSzWZZE"
}

url = 'https://api.weixin.qq.com/cgi-bin/token'
params = {
    "grant_type" : "client_credential",
    "appid" : config['appId'],
    "secret" : config['appSecret']
}

r = requests.get(url, params=params)
print(r.json())
token = r.json()['access_token']

def send_template_message(openid, msg):
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send'
    params = {
        "access_token" : token
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "touser" : openid ,
        "template_id" : config['templateId'],
        "data" : msg
    })
    return requests.post(url, params=params, data=data, headers=headers)

data = {
    "first" : {"value" : "你好"},
    "keyword1" : {"value" : "你好1"},
    "keyword2" : {"value" : "你好2"},
    "keyword3" : {"value" : "你好3"},
    "remark" : {"value" : "你好4"}
}

res = send_template_message('o8-jl53e_PjLcb6-rIIFr6PCsMII', data)
print(res.json())

