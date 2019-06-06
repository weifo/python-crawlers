import matplotlib.pyplot as plt
from pymongo import MongoClient

plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams["font.family"] = "cursive"
conn = MongoClient('localhost', port=27017)
db = conn.python # 库
table = db.pythondb # 表
arr = [[0, 50], [50,100], [100, 200], [200,300], [300,500], [500,1000]]
name_arr = []
total_arr = []
for i in arr:
    result = table.count({'price': {'$gte': i[0], '$lt': i[1]}})
    name = '%s元 ~ %s元 ' % (i[0], i[1])
    name_arr.append(name)
    total_arr.append(result)

color = 'red', 'orange', 'green', 'blue', 'gray', 'goldenrod' # 各类别颜色
explode = (0.1, 0, 0, 0, 0, 0)  # 各类别的偏移半径

# 绘制饼状图
pie = plt.pie(total_arr, colors=color, explode=explode, labels=name_arr, shadow=True, autopct='%1.1f%%')

plt.axis('equal')
plt.title(u'热点旅游景区门票价格比例', fontsize=12)

plt.legend(loc=0, bbox_to_anchor=(0.82, 1))  # 图例
# 设置legend的字体大小
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=6)
# 显示图
plt.show()