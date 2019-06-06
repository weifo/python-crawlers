import os
import time
import requests
from bs4 import BeautifulSoup

# 初始时间
starttime = time.time()
print(starttime)
# 新建文件夹
folder_path = "F:/learn-python/web-crawlers/word-cloud/"
os.makedirs(folder_path)
# 遍历
a = ['yi', 'er', 'san']
for i in a:
    for j in range(1, 55):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        url = 'http://www.pingfandeshijie.net/di-' + i + '-bu-' + str('%02d' % j) + '.html'
        response = requests.get(url=url, headers=headers)
        # 设置编码格式
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        # 获取章节情况
        h1 = soup.find('h1')
        print(h1.get_text())
        # 获取段落内容
        p = soup.find_all('p')
        for k in p:
            if '下一章' in k.get_text():
                break
            content = k.get_text().replace('S*锓', '')
            filename = h1.get_text() + '.txt'
            with open('F:\learn-python\web-crawlers\word-cloud\ ' + filename, 'a+') as f:
                try:
                    f.write(content + '')
                except:
                    pass
            f.close()
# 结束时间
endtime = time.time()
print(endtime)
# 程序运行总时间
print(round(endtime-starttime, 2))