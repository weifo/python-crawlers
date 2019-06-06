import jieba
import requests
import pandas as pd
import time
import random
from lxml import etree

def start_spider():
    base_url = 'https://movie.douban.com/subject/27622447/comments'
    start_url = base_url + '?start=0' 

    number = 1
    html = request_get(start_url) 

    while html.status_code == 200:
        # 获取下一页的 url
        selector = etree.HTML(html.text)
        nextpage = selector.xpath("//div[@id='paginator']/a[@class='next']/@href")
        nextpage = nextpage[0]
        next_url = base_url + nextpage
        # 获取评论
        comments = selector.xpath("//div[@class='comment']")
        allreviews = []
        for each in comments:
            allreviews.append(get_comments(each))

        data = pd.DataFrame(allreviews)
        # 写入csv文件,'a+'是追加模式
        try:
            if number == 1:
                csv_headers = ['用户', '是否看过', '五星评分', '评论时间', '有用数', '评论内容']
                data.to_csv('./reviews.csv', header=csv_headers, index=False, mode='a+', encoding='utf-8')
            else:
                data.to_csv('./reviews.csv', header=False, index=False, mode='a+', encoding='utf-8')
        except UnicodeEncodeError:
            print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

        data = []

        html = request_get(next_url)

def request_get(url):
    '''
    使用 Session 能够跨请求保持某些参数。
    它也会在同一个 Session 实例发出的所有请求之间保持 cookie
    '''
    timeout = 3

    UserAgent_List = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    ]

    header = {
        'User-agent': random.choice(UserAgent_List),
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/subject/24773958/?from=showing',
    }

    session = requests.Session()

    cookie = {
        # 'cookie': "ll='108288'; bid=j_NPtVWtzF8; __yadk_uid=7dAqmeVCeOEwQhS7sCfxROURsoAjBlhw; _ga=GA1.2.1940149470.1556983799; gr_user_id=4b47f038-c024-47b1-8f31-5eba0c375a05; _vwo_uuid_v2=DED6506C5ED3613BB15F45BED0EBEF8EA|cb2b09ebf6d875538bd7607fbb1b41b0; __gads=ID=28af6fcc35861014:T=1557806214:S=ALNI_MZzb-yqz64W3f6rp20W0OY_EgHHqg; trc_cookie_storage=taboola%2520global%253Auser-id%3Dd2562457-cbc1-417a-aa85-053c2d7ae564-tuct1cb37b2; __utmc=30149280; __utmc=223695111; douban-fav-remind=1; viewed="3369793_3336099_25661345"; __utmz=30149280.1559789713.15.9.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=30149280.1940149470.1556983799.1559789713.1559831977.16; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1559831996%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fq%3D%25E7%2581%25BF%25E7%2583%2582%25E4%25BA%25BA%25E7%2594%259F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.472159265.1556983799.1559629114.1559831996.11; __utmb=223695111.0.10.1559831996; __utmz=223695111.1559831996.11.9.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __utmb=30149280.5.10.1559831977; _pk_id.100001.4cf6=a11d7a54ddb3946c.1556983799.11.1559834121.1559629112."
    }

    time.sleep(random.randint(5, 15))  
    response = requests.get(url, headers=header, cookies=None, timeout = 3)
    if response.status_code != 200:
        print(response.status_code)
    return response

def get_comments(eachComment):
    commentlist = []
    user = eachComment.xpath("./h3/span[@class='comment-info']/a/text()")[0]  # 用户
    watched = eachComment.xpath("./h3/span[@class='comment-info']/span[1]/text()")[0]  # 是否看过
    rating = eachComment.xpath("./h3/span[@class='comment-info']/span[2]/@title")  # 五星评分
    if len(rating) > 0:
        rating = rating[0]

    comment_time = eachComment.xpath("./h3/span[@class='comment-info']/span[3]/@title")  # 评论时间
    if len(comment_time) > 0:
        comment_time = comment_time[0]
    else:
        # 有些评论是没有五星评分, 需赋空值
        comment_time = rating
        rating = ''

    votes = eachComment.xpath("./h3/span[@class='comment-vote']/span/text()")[0]  # "有用"数
    content = eachComment.xpath("./p/span/text()")[0]  # 评论内容

    commentlist.append(user)
    commentlist.append(watched)
    commentlist.append(rating)
    commentlist.append(comment_time)
    commentlist.append(votes)
    commentlist.append(content.replace('\n','').strip())
    # print(list)
    return commentlist

if __name__ == "__main__":
    start_spider()