import csv

with open("reviews.csv", "r",encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):
        print('line[{}] = {}'.format(i, line))
        if i==13:
            break