import webbrowser
from pymongo import MongoClient

conn = MongoClient('localhost', port=27017)
db = conn.python # 库
table = db.pythondb # 表

def main():
    city=input('请输入要显示的城市：')
    print(city)
    data=list(table.find({
        "city":city
    }))
    print(len(data))
    locdatas=[]
    for doc in data:
        lng,lat=doc['point'].split(',')
        locdatas.append({
            'lng':lng,
            'lat':lat,
            'count':doc['count']//100
        })
        print(doc['name'])


if __name__ == "__main__":
    main()

# webbrowser.open_new_tab('heatmap.html')