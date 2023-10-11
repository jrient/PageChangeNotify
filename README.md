# 页面内容变更检测&提醒

## 功能

1. 获取页面文本内容并保存到sqlite3数据库，之后每次执行脚本时检测页面内容是否有变化。
2. 提醒用户有页面内容变更的情况。

## 推送支持

1. [方糖](https://sct.ftqq.com/sendkey) 目前每日限额5条。
2. 其他正在开发中。。。

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

```json
{
    "pages" : [
        {
            // 自定义页面名称，仅用于提醒和日志
            "name": "页面名称",
            // 需要检测的页面链接
            "url" : "https://www.vodtw.la/book/3438/",
            // 检测页面内容的css选择器，如果不希望指定，可以留空
            "selector" : ".section-box",
            //子项目代理，指定当前页面使用代理 
            "proxy": {
                "http": ""
            },
        },
        {
            // 精简模式，使用全局代理
            // 不定义页面名称，则使用url作为页面名称
            "url" : "https://www.vodtw.la/book/6149/",
            "selector" : ".section-box"
        }
    ],
    // 全局代理 不使用代理可以留空
    "proxy": {
        "http": "",
        "https" : ""
    },
    // 方糖推送key
    "FTQQ_KEY" : "12312312312312312"
}

```
