import sys, os, urllib3
import json
from collections import Counter
import numpy as np
from numpy import *

class_list = []
json = json.load(open('train.json'))
annotation_section = json['annotations']
categories_section = json['categories']

id_name_dic = {}

for item in categories_section:
    category_name = item['supercategory']
    id = item['id']
    id_name_dic[id] = category_name
    # print('Category name:{}, ID: {}'.format(category_name, id))

for item in annotation_section:
    label = item['category_id']
    class_list.append((label))

count = Counter(class_list)

classlabel = list(count)
print("Number of all categories:", len(classlabel))
num = list(count.values())

i = 0
print("=======Statistic Details===========")
for class_id in classlabel:
    print("Class Name: {}, Class ID: {}, Instances: {}".format(id_name_dic[classlabel[i]], classlabel[i], num[i]))
    i = i + 1
