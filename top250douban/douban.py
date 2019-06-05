from lxml import etree
import requests
import csv


movielist,movieurls=[],[]
def getUrl():
    for i in range(10):
        url='https://movie.douban.com/top250?start={}'.format(i*25)
        crawlPage(url)

def crawlPage(url):
    html=requests.get(url).text
    s=etree.HTML(html)
    infos=['div[1]/a/span/text()','div[2]/p[1]/text()','div[2]/div/span[2]/text()','div[2]/p[2]/span/text()']
    for i in range(25):
        moviedict={}
        for idx,val in enumerate(infos):
            rawarr=s.xpath('//*[@id="content"]/div/div[1]/ol/li[{}]/div/div[2]/{}'.format(i+1,val))
            if idx==0:
                arr=map(lambda x:x.strip(),rawarr)
                moviedict['title']=' '.join(arr)
            elif idx==1:
                # print(rawarr)
                moviedict['category']=rawarr[1].strip()
            elif idx==2:
                moviedict['rating']=rawarr[0].strip()
            else:
                moviedict['quote']=rawarr[0].strip()
        movielist.append(moviedict)

getUrl()
with open('top250movies.csv', mode='w',encoding='utf-8',newline='') as csv_file:
    fieldnames = ['title', 'category', 'rating','quote']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames,dialect='excel')
    writer.writeheader()
    for row in movielist:
        writer.writerow(row)
        # writer.writerow({
        #     'title':row['title'],
        #     'category':row['category'],
        #     'rating':row['rating'],
        #     'quote':row['quote']        
        #     })


# print(p[1].strip())