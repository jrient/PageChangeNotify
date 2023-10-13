import requests, json, difflib, re, os
from bs4 import BeautifulSoup
from MyDB import init_table, read_db, write_db
from notify_modules import Handler
from datetime import datetime


class PageChangeNotify:

    def __init__(self, config):
        self.config = config
        self.pages = config['pages']
        self.proxy = config['proxy']

    def check_change(self):
        differ = difflib.Differ()
        for item in self.pages:
            url = item['url']
            try :
                if 'proxy' in item and isinstance(item['proxy'], dict):
                    proxy = item['proxy']
                else :
                    proxy = self.proxy
                header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                }
                html_text = requests.get(url, proxies=proxy, headers=header).text
                soup = BeautifulSoup(html_text, 'html.parser')
                if 'title' in item:
                    title = item['title']
                else :
                    title = soup.title.get_text()
                if 'selector' in item and item['selector'] != '':
                    soup = soup.select_one(item['selector'])
                all_text = re.sub(r'[\n"]+', '', soup.get_text())
            except Exception as e:
                print(title + ' : [error]' , e)
                continue
                # exit()
            
            db_result = read_db(url)
            if db_result is None:
                write_db(url, all_text)
                print(title + ' : [new page]')
            else :
                db_text = db_result[2]
                if all_text != db_text:
                    # d = list(differ.unified_diff(all_text.splitlines(), db_text.splitlines()))
                    # print('\n'.join(line for line in d if line.startswith('- ') or line.startswith('+ ')))
                    diff = difflib.unified_diff(db_text.split(), all_text.split(), lineterm='')
                    change_content = [line[1:] for line in diff if line.startswith('+')][1:]
                    change_content = ''.join(change_content)
                    print(title + ' : [have change]')
                    self.send_msg(title, change_content, url)
                    write_db(url, all_text)
                else :
                    print(title + ' : [no change]')

    def send_msg(self, title, content, url):
        Handler.Handler(self.config['notify_set'], self.config['notify_config'], self.config['send_to']).send_notify(title, content, url)


if __name__ == '__main__':
    print('start: ' + datetime.now())
    # 使用__file__变量获取当前脚本的位置
    current_file_location = os.path.dirname(__file__)
    config_file = os.path.join(current_file_location, 'config.json')
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    p = PageChangeNotify(config)
    # 初始化数据库
    init_table()

    # 检查是否有变化
    p.check_change()