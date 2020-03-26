import requests,csv
import random
import time
import re
from urllib import parse

#ip池
def ips():
    proxys = [
        {'HTTP': '116.196.87.86:20183'},
        {'HTTP': '113.194.29.19:9999'},
        {'HTTP': '113.195.19.111:9999'},
        {'HTTP': '175.43.57.15:9999'},
        {'HTTP': '171.13.202.155:9999'}
    ]
    proxy = random.choice(proxys)  # random.choice(),从列表中随机抽取一个对象
    return proxy


#UA池
def get_ua():
	user_agents = [
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
		'Opera/8.0 (Windows NT 5.1; U; en)',
		'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
		'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
		'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
	]
	user_agent = random.choice(user_agents) #random.choice(),从列表中随机抽取一个对象
	return user_agent


#UA  请求头
def headers(ua):
    headers = {
        'User-Agent': ua,
    }
    return headers


#构造翻页url
def nextpage():
    urls=[]
    for i in range(50,200):
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{}&page_type=searchall&page={}'.format(name,i)
        urls.append(url)
    return urls


#解析url获取数据并保存
def parsing(headers,ip):
    url1='https://m.weibo.cn/status/'
    for url in urls:
        response = requests.get(url,headers=headers,proxies=ip)
        for sj in response.json()['data']['cards']:
            try:
                text = sj['mblog']['text']
                # print(text)
                result = re.sub('<a  href.*?"surl-text">',"",text)
                result1 = re.sub("<a data.*?'url-icon'>", "", result)
                result2 = re.sub('src=.*?"surl-text">', "", result1)
                result3 = re.sub('<span.*?/>', "", result2)
                result4 = re.sub("<img style='width: 1rem;height: 1rem'", "", result3)
                result5 = re.sub('</span>', "", result4)
                result6 = re.sub('</a>', "", result5)
                result7 = re.sub('<br />', "", result6)
                result8 = re.sub('...<.*?>全文', "", result7)
                screen_name = sj['mblog']['user']['screen_name']
                id = sj['mblog']['id']
                reposts_count = sj['mblog']['reposts_count']
                comments_count = sj['mblog']['comments_count']
                attitudes_count = sj['mblog']['attitudes_count']
                created_at = sj['mblog']['created_at']
                print(screen_name,result8,reposts_count,comments_count,attitudes_count,url1+str(id),created_at, sep='|')
                writer.writerow((screen_name, result8, reposts_count, comments_count, attitudes_count, url1+str(id),created_at))
            except:
                pass
        time.sleep(2)



#启动函数
if __name__ == '__main__':
    str1 = input('请输入你要查询的内容')
    name = parse.quote(str1)
    fp = open('weibo.csv', 'a', newline='', encoding='utf-8')
    writer = csv.writer(fp)
    writer.writerow(('名字', '题目', '转发', '评论', '点赞', '链接', '日期'))
    ua = get_ua()
    headers = headers(ua)
    urls=nextpage()
    ip = ips()
    parsing(headers,ip)