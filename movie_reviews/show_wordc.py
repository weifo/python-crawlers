import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# print(dir(wordcloud))
def split_word():
    with open('reviews.csv', mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        content_list = []
        for row in reader:
            try:
                content_list.append(row[5])
            except IndexError:
                pass

        content = ''.join(content_list)

        seg_list = jieba.cut(content, cut_all=False)
        result = '\n'.join(seg_list)
        
        # 绘制圆形
        x, y = np.ogrid[:1500,:1500]
        mask = (x - 700) ** 2 + (y - 700) ** 2 > 700 ** 2
        mask = 255 * mask.astype(int)

        wc = WordCloud(
            background_color='white',
            mask=mask,
            # font_path='C:WindowsFonts华康俪金黑W8.TTF',
            max_words=20000,
            max_font_size=250,
            min_font_size=15,
            color_func=random_color_func,
            prefer_horizontal=1,
            random_state=50
        )
        myword = wc.generate(result)  # 生成词云
        # 展示词云图
        plt.imshow(myword)
        plt.axis("off")
        plt.show()
        wc.to_file('py_book.png')
        

# 设置文本随机颜色
def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    h, s, l = random.choice([(188, 72, 53), (253, 63, 56), (12, 78, 69)])
    return "hsl({}, {}%, {}%)".format(h, s, l)

if __name__ == "__main__":
    split_word()
    # print(dir(WordCloud))

