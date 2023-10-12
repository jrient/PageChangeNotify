# 页面内容变更检测&提醒

## 功能

1. 获取页面文本内容并保存到sqlite3数据库，之后每次执行脚本时检测页面内容是否有变化。
2. 提醒用户有页面内容变更的情况。

## 推送支持

1. [server酱(方糖)](https://sct.ftqq.com/sendkey) 目前每日限额5条。
2. [微信公众号](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html) 企业公众号可以使用，个人公众号不支持。

其他正在开发中。。。

## 使用方法

```shell
# 安装依赖
pip install -r requirements.txt
# 复制配置文件 填写自己的配置
cp config_example.json config.json
# 执行脚本
python main.py
```

## 配置项

config.json

```
{
    "pages" : [
        {
            # 自定义页面名称，仅用于提醒和日志
            "title": "页面名称",
            # 需要检测的页面链接
            "url" : "https://www.vodtw.la/book/3438/",
            # 检测页面内容的css选择器，如果不希望指定，可以留空
            "selector" : ".section-box",
            //子项目代理，指定当前页面使用代理 
            "proxy": {
                "http": ""
            },
        },
        {
            # 精简模式，使用全局代理
            # 不定义页面名称，则使用url作为页面名称
            "url" : "https://www.vodtw.la/book/6149/",
            "selector" : ".section-box"
        }
    ],
    # 全局代理 不使用代理可以留空
    "proxy": {
        "http": "",
        "https" : ""
    },
    # 发送消息的接收人 选择你设置的推送方式notify_set 配置即可
    "send_to": {
        # 微信公众号接收者的openid
        "weixin_notify" : [
            "aaa-jl53e_PjLcb6-rIIFr6PCsMII"
        ],
        # server酱的key
        "ftqq_notify": [
            "AAT41444TSOsl0RaT4cBm3FQsnJKKYR3c"
        ]
    },
    # 设置你选择的推送方式
    "notify_set" : "ftqq_notify",
    # 推送配置
    "notify_config" : {
        # 微信公众号配置
        "weixin_notify" : {
            # 目前微信支持模板消息和订阅消息，tmpl:模板消息，subscription:订阅消息
            "type" : "tmpl",
            # 微信公众平台 > 设置与开发 > 基本配置 > appid 和 appsecret
            "app_id" : "wxffffff",
            "app_secret" : "b2fasdfasdf",
            # 微信公众平台 > 广告与服务 > 模板消息 > 添加模板
            "template_id" : "E_PXClp9Usl91OhY",
            # 模板消息的详细内容， 设定模板变量 格式为 {{__变量__}}
            "template_msg": {
                # {{__TITLE__}} 标题
                "keyword1" : {"value" : "{{__TITLE__}}"},
                # {{__DATETIME__}} 时间日期
                "keyword2" : {"value" : "{{__DATETIME__}}"},
                # {{__URL__}} 链接
                "keyword3" : {"value" : "{{__URL__}}"},
                # {{__CONTENT__}} 差异内容
                "remark" : {"value" : "{{__CONTENT__}}"}
            }
        },
        # server酱配置 暂时无需配置内容
        "ftqq_notify": {}
    }
}

```

## 推送说明

### 支持的推送

| 推送方式 | 说明 |
| -- | -- |
| server酱(方糖)微信推送 | 免费版本每天限额5条 
| 微信公众号 | 企业公众号可以使用，个人公众号不支持，目前支持模板消息和订阅消息。 订阅消息改版后的一次性订阅消息不太好用，模板消息不支持链接跳转