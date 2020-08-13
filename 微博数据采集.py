# 支持自定义页数,关键词
# 提取时间,内容,名字,转发,评论,点赞

import requests
import csv
from urllib import parse


class Weibo():
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"})
        self.session.get("https://m.weibo.cn")

    def get_url(self):
        self.url = []
        for i in range(2, key2):
            url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{}&page_type=searchall&page={}'.format(
                key1, i)
            self.url.append(url)

    def chaxun(self):
        weibo.get_url()
        for url in self.url:
            headers = {
                'Host': 'm.weibo.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-Requested-With': 'XMLHttpRequest',
                'MWeibo-Pwa': '1',
                'X-XSRF-TOKEN': 'f2cc47',
                'Connection': 'keep-alive',
                'Referer': 'https://m.weibo.cn/search?containerid=100103type=1&q={}'.format(key1),
                # 'Cookie': '_T_WM=76913041359; XSRF-TOKEN=f2cc47; WEIBOCN_FROM=1110006030; MLOGIN=0; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%26fid%3D100103type%253D1%2526q%253Dvivo%2Bs7%26uicode%3D10000011',
                'TE': 'Trailers',
            }
            res = self.session.get(url, headers=headers)
            for i in res.json()['data']['cards']:
                # 时间
                time = i['mblog']['created_at']
                # 内容
                text = i['mblog']['raw_text'].replace(' ', '').replace('\n', '').replace('\r', '')
                # 名字
                screen_name = i['mblog']['user']['screen_name']
                # 转发
                reposts_count = i['mblog']['reposts_count']
                # 评论
                comments_count = i['mblog']['comments_count']
                # 点赞
                attitudes_count = i['mblog']['attitudes_count']
                print(screen_name, text, reposts_count,comments_count, attitudes_count, time)
                writer.writerow((screen_name, text, reposts_count,comments_count, attitudes_count, time))


if __name__ == "__main__":
    fp = open('weibo.csv', 'a', newline='', encoding='utf-8')
    writer = csv.writer(fp)
    writer.writerow(('名字', '内容', '转发', '评论', '点赞', '日期'))
    name = input('请输入要查询的关键词')
    key1 = parse.quote(name)
    key2 = int(input('请输入最大页数'))
    weibo = Weibo()
    weibo.chaxun()
