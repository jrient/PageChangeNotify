import requests, json, difflib, re, os
from bs4 import BeautifulSoup
from MyDB import init_table, read_db, write_db



class PageChangeNotify:

    def __init__(self, config):
        self.pages = config['pages']

    def check_change(self):
        differ = difflib.Differ()
        for item in self.pages:
            url = item['url']
            try :
                html_text = requests.get(url).text
                soup = BeautifulSoup(html_text, 'html.parser')
                title = soup.title.get_text()
                if 'selector' in item and item['selector'] != '':
                    soup = soup.select_one(item['selector'])
                all_text = re.sub(r'[\n"]+', '', soup.get_text())
            except Exception as e:
                print(url + ' : [error]' , e)
                exit()
            
            db_result = read_db(url)
            if db_result is None:
                write_db(url, all_text)
                print(url + ' : [new page]')
            else :
                db_text = db_result[2]
                if all_text != db_text:
                    # d = list(differ.unified_diff(all_text.splitlines(), db_text.splitlines()))
                    # print('\n'.join(line for line in d if line.startswith('- ') or line.startswith('+ ')))
                    diff = difflib.unified_diff(db_text.split(), all_text.split(), lineterm='')
                    change_content = [line[1:] for line in diff if line.startswith('+')][1:]
                    change_content = ''.join(change_content)
                    self.send_msg(url, title, change_content)
                    print(url + ' : [have change]')
                    write_db(url, all_text)
                else :
                    print(url + ' : [no change]')

    def send_msg(self, url, title, content):
        print(url, title, content)
        api_key = os.getenv("FTQQ_KEY")
        if not api_key:
            print('请设置环境变量 FTQQ_KEY')
            exit()
        url = "https://sctapi.ftqq.com/%s.send" % api_key
        requests.post(url, {
            'title': title,
            'desp': content
        })

        

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    p = PageChangeNotify(config)
    # 初始化数据库
    init_table()

    # 检查是否有变化
    p.check_change()


